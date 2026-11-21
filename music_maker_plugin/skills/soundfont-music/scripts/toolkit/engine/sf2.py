"""Minimal SoundFont 2 reader and sampler, pure Python + numpy.

Reads presets straight out of an .sf2 file (sample data is memory-mapped, so
huge multi-hundred-MB fonts don't get loaded into RAM) and renders
single notes to stereo float32 arrays.
"""
import struct
import numpy as np
from scipy.signal import lfilter

# generator numbers we care about
START_OFS, END_OFS, STARTLOOP_OFS, ENDLOOP_OFS = 0, 1, 2, 3
START_COARSE, END_COARSE, STARTLOOP_COARSE, ENDLOOP_COARSE = 4, 12, 45, 50
FILTER_FC, FILTER_Q = 8, 9
PAN = 17
DELAY_VOL, ATTACK_VOL, HOLD_VOL, DECAY_VOL, SUSTAIN_VOL, RELEASE_VOL = 33, 34, 35, 36, 37, 38
INSTRUMENT, KEY_RANGE, VEL_RANGE = 41, 43, 44
KEYNUM, VELOCITY, ATTENUATION = 46, 47, 48
COARSE_TUNE, FINE_TUNE, SAMPLE_ID, SAMPLE_MODES = 51, 52, 53, 54
SCALE_TUNING, OVERRIDE_ROOT = 56, 58

RANGE_GENS = (KEY_RANGE, VEL_RANGE)
# generators that are NOT added from the preset level (sample addressing etc.)
NON_ADDITIVE = {START_OFS, END_OFS, STARTLOOP_OFS, ENDLOOP_OFS, START_COARSE,
                END_COARSE, STARTLOOP_COARSE, ENDLOOP_COARSE, KEYNUM, VELOCITY,
                SAMPLE_MODES, OVERRIDE_ROOT, SAMPLE_ID, INSTRUMENT}

DEFAULTS = {FILTER_FC: 13500, DELAY_VOL: -12000, ATTACK_VOL: -12000,
            HOLD_VOL: -12000, DECAY_VOL: -12000, SUSTAIN_VOL: 0,
            RELEASE_VOL: -12000, SCALE_TUNING: 100, OVERRIDE_ROOT: -1,
            KEYNUM: -1, VELOCITY: -1}


def _tc(timecents):
    """SF2 timecents -> seconds."""
    return 2.0 ** (timecents / 1200.0)


class Zone:
    __slots__ = ("gens", "klo", "khi", "vlo", "vhi")

    def __init__(self, gens):
        self.gens = gens
        self.klo, self.khi = gens.get(KEY_RANGE, (0, 127))
        self.vlo, self.vhi = gens.get(VEL_RANGE, (0, 127))

    def matches(self, key, vel):
        return self.klo <= key <= self.khi and self.vlo <= vel <= self.vhi


class Preset:
    def __init__(self, sf, name, bank, program, zones):
        self.sf, self.name, self.bank, self.program = sf, name, bank, program
        self.zones = zones  # list of (merged gens dict, sample header)

    def __repr__(self):
        return f"<Preset {self.bank:03d}:{self.program:03d} {self.name!r}>"

    def render(self, key, vel, dur, sr=44100, tail=None, cents=0, vibrato=None, bend=None):
        """Render a note: `dur` seconds held, then release. Returns (n, 2) float32."""
        out = None
        for gens, shdr in self.zones:
            lo, hi = gens.get(KEY_RANGE, (0, 127))
            vlo, vhi = gens.get(VEL_RANGE, (0, 127))
            if not (lo <= key <= hi and vlo <= vel <= vhi):
                continue
            voice = self.sf._voice(gens, shdr, key, vel, dur, sr, tail, cents, vibrato, bend)
            if voice is None:
                continue
            if out is None:
                out = voice
            else:
                if len(voice) > len(out):
                    out, voice = voice, out
                out[:len(voice)] += voice
        return out if out is not None else np.zeros((1, 2), np.float32)


class SoundFont:
    def __init__(self, path):
        self.path = path
        self._parse()
        self._preset_cache = {}

    # ---------------------------------------------------------------- parsing
    def _parse(self):
        with open(self.path, "rb") as f:
            riff, size, kind = struct.unpack("<4sI4s", f.read(12))
            if riff != b"RIFF" or kind != b"sfbk":
                raise ValueError(f"{self.path} is not a SoundFont 2 file")
            end = 8 + size
            pdta = {}
            while f.tell() < end - 8:
                cid, csize = struct.unpack("<4sI", f.read(8))
                if cid == b"LIST":
                    ltype = f.read(4)
                    lend = f.tell() + csize - 4
                    while f.tell() < lend - 8:
                        sid, ssize = struct.unpack("<4sI", f.read(8))
                        if ltype == b"sdta" and sid == b"smpl":
                            self._smpl_offset = f.tell()
                            self._smpl_count = ssize // 2
                            f.seek(ssize + (ssize & 1), 1)
                        elif ltype == b"pdta":
                            pdta[sid] = f.read(ssize)
                            if ssize & 1:
                                f.read(1)
                        else:
                            f.seek(ssize + (ssize & 1), 1)
                    f.seek(lend)
                else:
                    f.seek(csize + (csize & 1), 1)
        self.samples = np.memmap(self.path, dtype="<i2", mode="r",
                                 offset=self._smpl_offset, shape=(self._smpl_count,))

        def records(cid, fmt):
            size = struct.calcsize(fmt)
            data = pdta[cid]
            return [struct.unpack_from(fmt, data, i) for i in range(0, len(data) - size + 1, size)]

        self._phdr = records(b"phdr", "<20sHHHIII")
        self._pbag = records(b"pbag", "<HH")
        self._pgen = records(b"pgen", "<H2s")
        self._inst = records(b"inst", "<20sH")
        self._ibag = records(b"ibag", "<HH")
        self._igen = records(b"igen", "<H2s")
        self._shdr = records(b"shdr", "<20sIIIIIBbHH")

        self.presets = {}
        for i in range(len(self._phdr) - 1):  # last is EOP terminator
            name, prog, bank = self._phdr[i][:3]
            self.presets[(bank, prog)] = _clean(name)

    @staticmethod
    def _gen_value(oper, raw):
        if oper in RANGE_GENS:
            return (raw[0], raw[1])
        if oper in (INSTRUMENT, SAMPLE_ID, SAMPLE_MODES):
            return struct.unpack("<H", raw)[0]
        return struct.unpack("<h", raw)[0]

    def _zones(self, bag_from, bag_to, bags, gens, terminal):
        """Return (global_gens, [zone_gens,...]) for a preset or instrument."""
        glob, zones = {}, []
        for b in range(bag_from, bag_to):
            g0, g1 = bags[b][0], bags[b + 1][0]
            z = {}
            for oper, raw in gens[g0:g1]:
                z[oper] = self._gen_value(oper, raw)
            if terminal in z:
                zones.append(z)
            elif b == bag_from and z:
                glob = z
        return glob, zones

    def preset(self, bank, program):
        key = (bank, program)
        if key in self._preset_cache:
            return self._preset_cache[key]
        idx = next((i for i in range(len(self._phdr) - 1)
                    if self._phdr[i][2] == bank and self._phdr[i][1] == program), None)
        if idx is None:
            raise KeyError(f"{self.path}: no preset {bank}:{program}")
        name = _clean(self._phdr[idx][0])
        pglob, pzones = self._zones(self._phdr[idx][3], self._phdr[idx + 1][3],
                                    self._pbag, self._pgen, INSTRUMENT)
        merged = []
        for pz in pzones:
            pgens = dict(pglob)
            pgens.update(pz)
            ii = pgens[INSTRUMENT]
            iglob, izones = self._zones(self._inst[ii][1], self._inst[ii + 1][1],
                                        self._ibag, self._igen, SAMPLE_ID)
            for iz in izones:
                g = dict(DEFAULTS)
                g.update(iglob)
                g.update(iz)
                # key/vel ranges intersect with preset zone ranges
                for r in RANGE_GENS:
                    a = g.get(r, (0, 127))
                    b = pgens.get(r, (0, 127))
                    g[r] = (max(a[0], b[0]), min(a[1], b[1]))
                if g[KEY_RANGE][0] > g[KEY_RANGE][1] or g[VEL_RANGE][0] > g[VEL_RANGE][1]:
                    continue
                for oper, val in pgens.items():
                    if oper in NON_ADDITIVE or oper in RANGE_GENS:
                        continue
                    g[oper] = g.get(oper, DEFAULTS.get(oper, 0)) + val
                merged.append((g, self._shdr[g[SAMPLE_ID]]))
        p = Preset(self, name, bank, program, merged)
        self._preset_cache[key] = p
        return p

    def find(self, text, bank=None):
        """Find presets whose name contains `text` (case-insensitive)."""
        t = text.lower()
        return [(b, p, n) for (b, p), n in sorted(self.presets.items())
                if t in n.lower() and (bank is None or b == bank)]

    # --------------------------------------------------------------- playback
    def _voice(self, g, shdr, key, vel, dur, sr, tail, extra_cents=0, vibrato=None, bend=None):
        _, start, end, sloop, eloop, srate, orig_pitch, pcorr, _, stype = shdr
        if stype & 0x8000:  # ROM sample, can't play
            return None
        start += g.get(START_OFS, 0) + 32768 * g.get(START_COARSE, 0)
        end += g.get(END_OFS, 0) + 32768 * g.get(END_COARSE, 0)
        sloop += g.get(STARTLOOP_OFS, 0) + 32768 * g.get(STARTLOOP_COARSE, 0)
        eloop += g.get(ENDLOOP_OFS, 0) + 32768 * g.get(ENDLOOP_COARSE, 0)
        end = min(end, self._smpl_count)
        if end - start < 2 or srate == 0:
            return None
        looped = g.get(SAMPLE_MODES, 0) & 1 and start <= sloop < eloop <= end and eloop - sloop > 1

        if g.get(KEYNUM, -1) >= 0:
            key = g[KEYNUM]
        if g.get(VELOCITY, -1) >= 0:
            vel = g[VELOCITY]
        root = g[OVERRIDE_ROOT] if g[OVERRIDE_ROOT] >= 0 else orig_pitch
        if root > 127:
            root = 60
        cents = ((key - root) * g[SCALE_TUNING] + g.get(COARSE_TUNE, 0) * 100
                 + g.get(FINE_TUNE, 0) + pcorr + extra_cents)
        step = 2.0 ** (cents / 1200.0) * srate / sr

        # envelope (seconds)
        delay = _tc(g[DELAY_VOL]) if g[DELAY_VOL] > -12000 else 0.0
        attack = _tc(g[ATTACK_VOL]) if g[ATTACK_VOL] > -12000 else 0.0
        hold = _tc(g[HOLD_VOL]) if g[HOLD_VOL] > -12000 else 0.0
        decay = _tc(g[DECAY_VOL])
        sustain = 10.0 ** (-max(0, min(1440, g[SUSTAIN_VOL])) / 200.0)
        release = min(_tc(g[RELEASE_VOL]), 8.0)
        release = max(release, 0.01)
        if tail is not None:
            release = min(release, tail)

        n_on = int(dur * sr)
        n_total = n_on + int(release * sr)
        if not looped:
            n_total = min(n_total, int((end - start - 1) / step) + 1)
        if n_total <= 0:
            return None

        if vibrato or bend:
            inc = step * pitch_curve(n_total, sr, dur, vibrato, bend)
            pos = np.concatenate(([0.0], np.cumsum(inc[:-1])))
            if not looped:
                pos = np.minimum(pos, end - start - 2)
        else:
            pos = np.arange(n_total, dtype=np.float64) * step
        if looped:
            llen = eloop - sloop
            rel = start + pos
            over = rel >= eloop
            rel[over] = sloop + np.mod(rel[over] - sloop, llen)
            idx = rel
        else:
            idx = start + pos
        i0 = idx.astype(np.int64)
        frac = (idx - i0).astype(np.float32)
        lo_i, hi_i = i0.min(), min(i0.max() + 2, self._smpl_count)
        seg = np.asarray(self.samples[lo_i:hi_i], dtype=np.float32) / 32768.0
        a = seg[i0 - lo_i]
        j = i0 + 1
        if looped:
            j = np.where(j >= eloop, sloop, j)
        j = np.minimum(j - lo_i, len(seg) - 1)
        b = seg[j]
        wave = a + (b - a) * frac

        env = _envelope(n_total, n_on, sr, delay, attack, hold, decay, sustain, release)
        wave *= env

        fc = g[FILTER_FC]
        if fc < 13000:
            hz = min(8.176 * 2.0 ** (fc / 1200.0), sr * 0.45)
            alpha = 1.0 - np.exp(-2 * np.pi * hz / sr)
            wave = lfilter([alpha], [1, alpha - 1], wave).astype(np.float32)

        att_cb = max(0, g.get(ATTENUATION, 0)) * 0.4  # EMU-style scaling, like FluidSynth
        gain = 10.0 ** (-att_cb / 200.0) * (vel / 127.0) ** 2
        pan = max(-500, min(500, g.get(PAN, 0))) / 1000.0 + 0.5
        l, r = np.cos(pan * np.pi / 2), np.sin(pan * np.pi / 2)
        out = np.empty((n_total, 2), np.float32)
        out[:, 0] = wave * (gain * l * 1.4142)
        out[:, 1] = wave * (gain * r * 1.4142)
        return out


def pitch_lfo(n, sr, rate=5.5, depth=30.0, delay=0.15, fade=0.2):
    """Per-sample pitch ratio for vibrato: `depth` cents at `rate` Hz, starting
    after `delay` seconds and fading in over `fade` seconds."""
    t = np.arange(n, dtype=np.float64) / sr
    ramp = np.clip((t - delay) / max(fade, 1e-3), 0.0, 1.0)
    cents = depth * ramp * np.sin(2 * np.pi * rate * np.maximum(t - delay, 0.0))
    return 2.0 ** (cents / 1200.0)


def build_bend_curve(style="bend_release", semis=2.0, smooth=True, vibrato_waves=3):
    """Build a hashable normalized pitch-bend curve ('norm', smooth, ((frac, semis), ...)).

    Styles:
      - 'bend_release': pick at 0, bend to `semis`, hold briefly, release to 0
      - 'bend_hold':    pick at 0, bend fast to `semis`, hold until note end
      - 'delayed_bend': hold clean at 0, bend up to `semis` mid-note, release to 0
      - 'pre_bend':     start already bent at `semis`, release down to 0
      - 'scoop':        start below by `-abs(semis)` and scoop smoothly up to 0
      - 'dive':         hold 0, dive down to `-abs(semis)`, return to 0
      - 'bend_vibrato': hand-played pitch-wheel vibrato waves (0 -> peak -> 0)
      - 'glide':        linear slide from 0 to `semis` across the note
    """
    s = float(semis)
    if style == "bend_hold":
        pts = ((0.0, 0.0), (0.18, s), (1.0, s))
    elif style == "delayed_bend":
        pts = ((0.0, 0.0), (0.25, 0.0), (0.45, s), (0.68, s), (0.90, 0.0), (1.0, 0.0))
    elif style == "pre_bend":
        pts = ((0.0, s), (0.20, s), (0.68, 0.0), (1.0, 0.0))
    elif style == "scoop":
        pts = ((0.0, -abs(s)), (0.24, 0.0), (1.0, 0.0))
    elif style == "dive":
        d = -abs(s)
        pts = ((0.0, 0.0), (0.35, 0.0), (0.62, d), (0.72, d), (0.92, 0.0), (1.0, 0.0))
    elif style == "bend_vibrato":
        waves = max(1, int(vibrato_waves))
        start_f, end_f = 0.14, 0.94
        span = (end_f - start_f) / waves
        raw = [(0.0, 0.0), (start_f, 0.0)]
        for idx in range(waves):
            t0 = start_f + idx * span
            amp = s * (1.0 - 0.10 * idx / max(1, waves))
            raw.append((round(t0 + span * 0.45, 5), round(amp, 4)))
            raw.append((round(t0 + span * 0.92, 5), 0.0))
        raw.append((1.0, 0.0))
        pts = tuple(raw)
    elif style == "glide":
        return ("norm", False, ((0.0, 0.0), (1.0, s)))
    else:  # 'bend_release'
        pts = ((0.0, 0.0), (0.22, s), (0.50, s), (0.82, 0.0), (1.0, 0.0))
    return ("norm", bool(smooth), pts)


def _eval_bend_points(n, sr, dur, points, smooth=True, normalized=False):
    """Evaluate piecewise linear or smoothstep control points over `n` samples."""
    if not points:
        return np.zeros(n, dtype=np.float64)
    scale = max(dur, 1e-3) if normalized else 1.0
    pts = sorted((float(t) * scale, float(s)) for t, s in points)
    dedup_t, dedup_s = [], []
    for t_val, s_val in pts:
        if dedup_t and abs(t_val - dedup_t[-1]) < 1e-9:
            dedup_s[-1] = s_val
        else:
            dedup_t.append(t_val)
            dedup_s.append(s_val)
    t = np.arange(n, dtype=np.float64) / sr
    if len(dedup_t) == 1:
        return np.full(n, dedup_s[0], dtype=np.float64)
    ts = np.asarray(dedup_t, dtype=np.float64)
    ss = np.asarray(dedup_s, dtype=np.float64)
    if not smooth:
        return np.interp(t, ts, ss)
    out = np.empty(n, dtype=np.float64)
    out[t <= ts[0]] = ss[0]
    out[t >= ts[-1]] = ss[-1]
    for i in range(len(ts) - 1):
        mask = (t >= ts[i]) & (t < ts[i + 1])
        if not np.any(mask):
            continue
        u = (t[mask] - ts[i]) / max(ts[i + 1] - ts[i], 1e-9)
        u = u * u * (3.0 - 2.0 * u)
        out[mask] = ss[i] + (ss[i + 1] - ss[i]) * u
    return out


def pitch_curve(n, sr, dur, vibrato=None, bend=None):
    """Per-sample pitch ratio combining vibrato and a bend.

    Supports:
      - `(semis, "bend")` / `(semis, "glide")` legacy 2-tuples
      - `("norm", smooth, ((frac, semis), ...))` normalized over `dur`
      - `("points", smooth, ((sec, semis), ...))` seconds from note start
    """
    ratio = pitch_lfo(n, sr, *vibrato) if vibrato else np.ones(n)
    if bend:
        tag = bend[0]
        if tag in ("norm", "points"):
            _, smooth, points = bend
            semis_curve = _eval_bend_points(
                n, sr, dur, points, smooth=bool(smooth), normalized=(tag == "norm")
            )
            ratio = ratio * 2.0 ** (semis_curve / 12.0)
        else:
            semis, kind = bend
            t = np.arange(n, dtype=np.float64) / sr
            span = min(0.11, dur * 0.6) if kind == "bend" else max(dur, 1e-3)
            x = np.clip(t / span, 0.0, 1.0)
            shape = x * x * (3 - 2 * x) if kind == "bend" else x   # smoothstep for bends
            ratio = ratio * 2.0 ** (semis * shape / 12.0)
    return ratio


def _envelope(n, n_on, sr, delay, attack, hold, decay, sustain, release):
    t = np.arange(n, dtype=np.float32) / sr
    env = np.empty(n, np.float32)
    t_a = delay + attack
    t_h = t_a + hold
    env[:] = sustain
    # delay / attack / hold
    env[t < delay] = 0.0
    m = (t >= delay) & (t < t_a)
    if attack > 0:
        env[m] = (t[m] - delay) / attack
    env[(t >= t_a) & (t < t_h)] = 1.0
    # decay: exponential-ish (linear in dB) toward sustain; decay time = time to -100 dB
    m = t >= t_h
    if decay > 0:
        db = -100.0 * (t[m] - t_h) / decay
        lvl = 10.0 ** (db / 20.0)
        env[m] = np.maximum(lvl, sustain)
    # release from whatever level we were at when the key was let go
    if n_on < n:
        lvl0 = env[n_on - 1] if n_on > 0 else 0.0
        tr = (np.arange(n - n_on, dtype=np.float32)) / sr
        env[n_on:] = lvl0 * 10.0 ** ((-100.0 * tr / release) / 20.0)
    return env


def _clean(raw):
    return raw.split(b"\0", 1)[0].decode("latin-1").strip()


if __name__ == "__main__":
    import sys
    sf = SoundFont(sys.argv[1])
    needle = sys.argv[2] if len(sys.argv) > 2 else ""
    for (b, p), n in sorted(sf.presets.items()):
        if needle.lower() in n.lower():
            print(f"{b:3d}:{p:3d}  {n}")
