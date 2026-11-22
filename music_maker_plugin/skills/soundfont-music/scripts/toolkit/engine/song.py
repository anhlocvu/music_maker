"""Tiny song format + renderer.

Write parts as step strings, one token per step:
    "C5 - E5 G5 | . . A4+C5+E5 -"
      C5     start a note (octave number required, sharps with #, flats with b)
      A4+C5  chord (several notes starting together)
      -      hold the previous note one more step
      .      rest
      |      bar line, ignored (just for readability)
    Tokens can carry a velocity with @: "C5@90"
      D5^E5  guitar bend: pick D5, bend up to E5 fast, hold (works downward too)
      B5>E4  glide/slide: start at B5 and slide evenly to E4 over the note length
Drum parts use drum names instead of notes: "kick . snare . kick kick snare ."
"""
import math
import os
import re
import wave
import numpy as np
from scipy.signal import fftconvolve

from .sf2 import SoundFont, build_bend_curve
from . import instruments

SR = 44100
NOTE_BASE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
DRUMS = {  # General MIDI drum map
    "kick": 36, "kick2": 35, "snare": 38, "snare2": 40, "rim": 37, "clap": 39,
    "hat": 42, "ohat": 46, "phat": 44, "crash": 49, "ride": 51, "tom1": 50,
    "tom2": 47, "tom3": 45, "tom4": 43, "tamb": 54, "cowbell": 56,
    "splash": 55, "china": 52, "shaker": 70, "triangle": 81, "otri": 81,
    "mtri": 80, "bongo": 60, "conga": 63, "timbale": 65, "agogo": 67,
}


def note_number(name):
    """'C#4' -> 61, 'Bb2' -> 46. Middle C is C4 = 60."""
    if name.lower() in DRUMS:
        return DRUMS[name.lower()]
    letter = name[0].upper()
    i, acc = 1, 0
    while i < len(name) and name[i] in "#b":
        acc += 1 if name[i] == "#" else -1
        i += 1
    return 12 * (int(name[i:]) + 1) + NOTE_BASE[letter] + acc


class Track:
    def __init__(self, song, name, instrument, volume=1.0, pan=0.0, reverb=0.25,
                 transpose=0, release=None, cents=0, vibrato=None, autopan=None,
                 bend_range=2.0):
        self.song, self.name = song, name
        self.instrument = instrument
        self.volume, self.pan, self.reverb = volume, pan, reverb
        self.transpose = transpose
        self.cents = cents  # fine detune, e.g. -1200 for "detuned by -1200 cents"
        # vibrato=(rate Hz, depth cents, delay s[, fade s]); only notes held past the delay wobble
        self.vibrato = vibrato
        # autopan=(period in beats, depth 0..1): each note is panned by a sine
        # sweep across the stereo field based on when it starts
        self.autopan = autopan
        self.release = release
        self.bend_range = float(bend_range)
        self.events = []  # (start_beat, beats, key, velocity, bend or None)
        self.pedals = []  # (start_beat, end_beat) sustain pedal CC64 intervals

    @staticmethod
    def _parse_chord_keys(chord, transpose=0):
        """Convert a chord string ('C4+E4+G4') or sequence into sorted MIDI keys."""
        items = chord.split("+") if isinstance(chord, str) else list(chord)
        keys = [
            (k if isinstance(k, int) else note_number(k.strip())) + transpose
            for k in items
        ]
        return sorted(keys)

    def pedal(self, start_beat, end_beat):
        """Hold sustain pedal (CC 64) down from `start_beat` to `end_beat`."""
        if end_beat > start_beat:
            self.pedals.append((float(start_beat), float(end_beat)))
        return self

    def pedal_steps(self, step=4.0, start=0.0, end=None, lift=0.05):
        """Re-pedal every `step` beats, lifting briefly by `lift` beats at changes."""
        end_pos = self.length() if end is None else float(end)
        cur = float(start)
        while cur < end_pos - 1e-6:
            nxt = min(cur + step, end_pos)
            ped_end = nxt - lift if nxt - cur > lift * 2 else nxt
            self.pedal(cur, ped_end)
            cur += step
        return self

    def strum(self, chord, beats=2.0, spread=0.05, at=None, vel=90,
              direction="up", humanize_vel=5):
        """Roll/strum a chord across notes, keeping total span `beats`."""
        pos = self._end() if at is None else float(at)
        keys = self._parse_chord_keys(chord, self.transpose)
        if direction == "down":
            keys = list(reversed(keys))
        n = max(1, len(keys))
        actual_spread = min(spread, (beats * 0.5) / n) if n > 1 else 0.0
        for idx, key in enumerate(keys):
            offset = idx * actual_spread
            note_dur = max(0.05, beats - offset)
            note_vel = max(1, min(127, int(vel - min(humanize_vel, idx * 2))))
            self.events.append((pos + offset, note_dur, key, note_vel, None))
        self._cursor = pos + beats
        return self

    def arpeggio(self, chord, step=0.25, beats=None, at=None, pattern="up",
                 vel=85, hold=True):
        """Arpeggiate a chord over `beats` (or one pattern cycle if None)."""
        pos = self._end() if at is None else float(at)
        keys = self._parse_chord_keys(chord, self.transpose)
        if not keys:
            return self
        if pattern == "down":
            order = list(reversed(keys))
        elif pattern == "updown" and len(keys) > 2:
            order = keys + list(reversed(keys[1:-1]))
        elif isinstance(pattern, (list, tuple)):
            order = [keys[i % len(keys)] for i in pattern]
        else:
            order = keys

        total_beats = float(beats) if beats is not None else len(order) * step
        steps = max(1, int(round(total_beats / step)))
        span_end = pos + total_beats
        for idx in range(steps):
            start = pos + idx * step
            key = order[idx % len(order)]
            dur = max(step, span_end - start) if hold else step
            note_vel = max(1, min(127, int(vel - (idx % 2) * 4)))
            self.events.append((start, dur, key, note_vel, None))
        self._cursor = span_end
        return self

    @staticmethod
    def _parse_bend_target(spec, base_key):
        """Convert either a note name ('E5') or relative semitone ('+2', '-1.5') to semitone offset."""
        s = spec.strip()
        try:
            return float(s)
        except ValueError:
            return float(note_number(s) - base_key)

    @classmethod
    def _parse_step_bend(cls, nm):
        """Parse inline bend syntax: ^ (bend or bend-release), ~ (delayed bend-release), > (glide)."""
        if "^" in nm:
            parts = nm.split("^")
            base_nm = parts[0]
            base_key = note_number(base_nm)
            if len(parts) == 2:
                return base_nm, (cls._parse_bend_target(parts[1], base_key), "bend")
            if len(parts) >= 3:
                p1 = cls._parse_bend_target(parts[1], base_key)
                p2 = cls._parse_bend_target(parts[2], base_key)
                return base_nm, ("norm", True, ((0.0, 0.0), (0.24, p1), (0.52, p1), (0.82, p2), (1.0, p2)))
        if "~" in nm:
            parts = nm.split("~")
            base_nm = parts[0]
            base_key = note_number(base_nm)
            p1 = cls._parse_bend_target(parts[1], base_key)
            p2 = cls._parse_bend_target(parts[2], base_key) if len(parts) >= 3 else 0.0
            return base_nm, ("norm", True, ((0.0, 0.0), (0.22, 0.0), (0.48, p1), (0.64, p1), (0.88, p2), (1.0, p2)))
        if ">" in nm:
            base_nm, to = nm.split(">", 1)
            base_key = note_number(base_nm)
            return base_nm, (cls._parse_bend_target(to, base_key), "glide")
        return nm, None

    def _build_bend_spec(self, curve=None, style="bend_release", semis=2.0,
                         smooth=True, unit="norm", vibrato_waves=3):
        """Normalize an explicit curve or named preset into a hashable bend spec."""
        if curve is not None:
            pts = []
            for t_val, s_val in curve:
                t_sec = self.song.beats_to_sec(float(t_val)) if unit == "beats" else float(t_val)
                pts.append((round(t_sec, 6), round(float(s_val), 5)))
            tag = "norm" if unit == "norm" else "points"
            return (tag, bool(smooth), tuple(pts))
        return build_bend_curve(style=style, semis=semis, smooth=smooth, vibrato_waves=vibrato_waves)

    def note(self, note, beats=1.0, at=None, vel=90, bend=None):
        """Add a single note or '+' chord at `at` (defaults to cursor) with optional bend curve."""
        pos = self._end() if at is None else float(at)
        keys = self._parse_chord_keys(note, self.transpose)
        v = max(1, min(127, int(vel)))
        for k in keys:
            self.events.append((pos, float(beats), k, v, bend))
        self._cursor = pos + float(beats)
        return self

    def bend(self, note, beats=1.0, curve=None, style="bend_release", semis=2.0,
             at=None, vel=90, smooth=True, unit="norm", vibrato_waves=3):
        """Add a note/chord with a rich multi-point or preset pitch-bend curve."""
        bend_spec = self._build_bend_spec(
            curve=curve, style=style, semis=semis,
            smooth=smooth, unit=unit, vibrato_waves=vibrato_waves,
        )
        return self.note(note, beats=beats, at=at, vel=vel, bend=bend_spec)

    def bend_last(self, curve=None, style="bend_release", semis=2.0,
                  smooth=True, unit="norm", vibrato_waves=3):
        """Attach or replace the pitch-bend curve on the most recently added event(s)."""
        if not self.events:
            return self
        bend_spec = self._build_bend_spec(
            curve=curve, style=style, semis=semis,
            smooth=smooth, unit=unit, vibrato_waves=vibrato_waves,
        )
        last_start = self.events[-1][0]
        updated = []
        for s, d, k, v, b in self.events:
            if abs(s - last_start) < 1e-6:
                updated.append((s, d, k, v, bend_spec))
            else:
                updated.append((s, d, k, v, b))
        self.events = updated
        return self

    def seq(self, text, step=0.25, at=None, vel=100, repeat=1):
        """Add a step pattern. `step` is in beats (0.25 = 16th notes).
        Starts at `at` beats (default: where this track last ended)."""
        pos = self._end() if at is None else at
        for _ in range(repeat):
            pending = []  # notes currently sounding: [start, beats, key, vel]
            for tok in text.replace("|", " ").split():
                if tok == "-":
                    for n in pending:
                        n[1] += step
                else:
                    self.events.extend(tuple(n) for n in pending)
                    pending = []
                    if tok not in (".", "r"):
                        v = vel
                        if "@" in tok:
                            tok, v = tok.split("@")
                            v = int(v)
                        for nm in re.split(r"\+(?=[A-Za-z])", tok):
                            nm, bend = self._parse_step_bend(nm)
                            pending.append([pos, step, note_number(nm) + self.transpose, v, bend])
                pos += step
            self.events.extend(tuple(n) for n in pending)
        self._cursor = pos
        return self

    def rest(self, beats):
        self._cursor = self._end() + beats
        return self

    def _end(self):
        return getattr(self, "_cursor", 0.0)

    def _effective_beats(self, start, beats):
        """Extend held duration when sustain pedal covers the note's release."""
        note_end = start + beats
        ext_end = note_end
        for p_start, p_end in self.pedals:
            if p_start - 1e-6 <= note_end <= p_end and p_end > ext_end:
                ext_end = p_end
        return ext_end - start

    def length(self):
        return max((e[0] + self._effective_beats(e[0], e[1]) for e in self.events), default=0.0)


class Song:
    def __init__(self, title, bpm=120, swing=0.0, master=0.8, room=1.6, pitch=0):
        self.title, self.bpm, self.swing = title, bpm, swing
        self.pitch = pitch  # master pitch in cents, applied to every track
        self.master, self.room = master, room
        self.tracks = []

    def track(self, name, instrument, **kw):
        t = Track(self, name, instrument, **kw)
        self.tracks.append(t)
        return t

    def beats_to_sec(self, b):
        return b * 60.0 / self.bpm

    def _render_track(self, t, n, keep_pan=True):
        """Render a single Track to a stereo dry buffer of length `n` samples."""
        preset = instruments.load(t.instrument)
        excl_fn = getattr(preset, "exclusive_class", None)
        choke_secs = {}
        if excl_fn is not None and t.events:
            ordered = sorted(enumerate(t.events), key=lambda item: (item[1][0], item[1][2]))
            active_excl = {}
            for idx, (start, _beats, key, vel, _bend) in ordered:
                excl = excl_fn(key, vel)
                if excl > 0:
                    s_eff = start + (self.swing * 0.5 if self.swing and (start * 2) % 1 == 0.5 else 0.0)
                    s_sec = self.beats_to_sec(s_eff)
                    if excl in active_excl:
                        prev_idx, prev_sec = active_excl[excl]
                        if s_sec > prev_sec + 1e-6:
                            choke_secs[prev_idx] = s_sec
                    active_excl[excl] = (idx, s_sec)

        buf = np.zeros((n, 2), np.float32)
        cache = {}
        fade_len = max(1, int(0.01 * SR))
        for idx, (start, beats, key, vel, bend) in enumerate(t.events):
            s = start
            if self.swing and (start * 2) % 1 == 0.5:  # delay off-beat 8ths
                s += self.swing * 0.5
            eff_beats = t._effective_beats(start, beats)
            dur = self.beats_to_sec(eff_beats) * 0.98
            ck = (key, vel, round(dur, 3), bend)
            if ck not in cache:
                cache[ck] = preset.render(key, vel, dur, SR, tail=t.release,
                                          cents=t.cents + self.pitch, vibrato=t.vibrato,
                                          bend=bend)
            v = cache[ck]
            s_sec = self.beats_to_sec(s)
            i = int(s_sec * SR)
            m = min(len(v), n - i)
            if idx in choke_secs:
                choke_samples = max(1, int((choke_secs[idx] - s_sec) * SR))
                if choke_samples < m:
                    v = v[:choke_samples].copy()
                    fl = min(fade_len, len(v))
                    v[-fl:] *= np.linspace(1.0, 0.0, fl, dtype=np.float32)[:, None]
                    m = len(v)
            if m > 0:
                if keep_pan and t.autopan:
                    period, depth = t.autopan
                    pn = max(-1.0, min(1.0, t.pan + depth * np.sin(2 * np.pi * start / period)))
                    a = (pn + 1) / 2
                    buf[i:i + m, 0] += v[:m, 0] * np.cos(a * np.pi / 2) * 1.4142
                    buf[i:i + m, 1] += v[:m, 1] * np.sin(a * np.pi / 2) * 1.4142
                else:
                    buf[i:i + m] += v[:m]
        pan = t.pan if keep_pan else 0.0
        p = 0.5 if (keep_pan and t.autopan) else (pan + 1) / 2
        buf[:, 0] *= t.volume * np.cos(p * np.pi / 2) * 1.4142
        buf[:, 1] *= t.volume * np.sin(p * np.pi / 2) * 1.4142
        return buf, preset.name

    # ------------------------------------------------------------------ audio
    def render(self, path=None, trim=True):
        """Mix every track. Writes a WAV if `path` is given; always returns the
        stereo float array (normalized). trim=False keeps the full length, which
        matters when cutting exact loop points out of the result."""
        length = max((t.length() for t in self.tracks), default=0.0)
        n = int(self.beats_to_sec(length) * SR) + SR * 4
        dry = np.zeros((n, 2), np.float32)
        wet = np.zeros((n, 2), np.float32)
        for t in self.tracks:
            buf, pname = self._render_track(t, n, keep_pan=True)
            dry += buf
            wet += buf * t.reverb
            print(f"  rendered {t.name:<12} ({pname})")
        mix = dry + _reverb(wet, self.room)
        if trim:  # trim trailing silence
            nz = np.nonzero(np.abs(mix).max(axis=1) > 1e-4)[0]
            mix = mix[: (nz[-1] + 1 if len(nz) else 1)]
        peak = np.abs(mix).max() or 1.0
        mix *= self.master / peak
        if path:
            _write_wav(path, mix)
        return mix

    def export_stems(self, out_dir, keep_pan=False, trim=True):
        """Export every track as an aligned WAV stem inside `out_dir`.

        Preserves instrument/track effects (reverb, vibrato, release, pedal, bends)
        while centering track pan (`keep_pan=False`) by default for DAW mixing.
        """
        if not self.tracks:
            return []
        os.makedirs(out_dir, exist_ok=True)
        length = max((t.length() for t in self.tracks), default=0.0)
        n = int(self.beats_to_sec(length) * SR) + SR * 4

        stems = []
        names = []
        mix_sum = np.zeros((n, 2), np.float32)
        for t in self.tracks:
            buf, pname = self._render_track(t, n, keep_pan=keep_pan)
            wet = _reverb(buf * t.reverb, self.room) if (t.reverb > 0 and self.room > 0) else 0.0
            stem = buf + wet
            stems.append(stem)
            names.append((t.name, pname))
            mix_sum += stem

        end_idx = n
        if trim:
            nz = np.nonzero(np.abs(mix_sum).max(axis=1) > 1e-4)[0]
            end_idx = (int(nz[-1]) + 1) if len(nz) else 1

        mix_peak = float(np.abs(mix_sum[:end_idx]).max()) or 1.0
        stem_peak = max((float(np.abs(s[:end_idx]).max()) for s in stems), default=1.0) or 1.0
        scale = min(self.master / mix_peak, 0.98 / stem_peak)

        written = []
        for idx, (stem, (tname, pname)) in enumerate(zip(stems, names), start=1):
            safe = "".join(c if c.isalnum() or c in "-_ " else "_" for c in tname).strip().replace(" ", "_")
            stem_path = os.path.join(out_dir, f"{idx:02d}_{safe or 'track'}.wav")
            _write_wav(stem_path, stem[:end_idx] * scale)
            written.append(stem_path)
            print(f"  stem     {tname:<12} ({pname}) -> {os.path.basename(stem_path)}")
        return written

    def render_loop(self, loop_start, loop_end, out_base):
        """Render a game-ready loop. The song plays once from 0 to `loop_end` (beats),
        then [loop_start, loop_end) again; the second copy is kept as the loop so the
        reverb tail from the loop's end is already ringing into its start. Writes
          <out_base>_intro.wav   everything before loop_start
          <out_base>_loop.wav    one seamless pass of the loop
          <out_base>_looped.wav  intro + loop with a 'smpl' loop chunk (loop points
                                 most engines/samplers read), plus LOOPSTART/LOOPLENGTH
                                 sample counts printed for engines that want tags
        Returns (loop_start_sample, loop_length_samples)."""
        import copy
        span = loop_end - loop_start
        twice = copy.copy(self)
        twice.tracks = []
        for t in self.tracks:
            c = copy.copy(t)
            c.events = [e for e in t.events if e[0] < loop_end] + \
                       [(s + span, *rest) for s, *rest in t.events if loop_start <= s < loop_end]
            c.pedals = [(s, min(e, loop_end)) for s, e in t.pedals if s < loop_end] + \
                       [(max(s, loop_start) + span, min(e, loop_end) + span)
                        for s, e in t.pedals if e > loop_start and s < loop_end]
            twice.tracks.append(c)
        mix = twice.render(trim=False)
        a = int(round(self.beats_to_sec(loop_start) * SR))
        n = int(round(self.beats_to_sec(span) * SR))
        intro, loop = mix[:a], mix[a + n: a + 2 * n]
        _write_wav(out_base + "_intro.wav", intro)
        _write_wav(out_base + "_loop.wav", loop)
        _write_wav(out_base + "_looped.wav", np.concatenate([intro, loop]), loop=(a, a + n))
        print(f"  loop: LOOPSTART={a} LOOPLENGTH={n} samples @ {SR} Hz "
              f"({self.beats_to_sec(loop_start):.3f}s + {self.beats_to_sec(span):.3f}s)")
        return a, n

    # ------------------------------------------------------------------- midi
    def export_midi(self, path, tracks=None, channel=None, bends=True, markers=None,
                    mpe=False, mpe_bend_range=None):
        """Write a type-1 MIDI file. `channel=None` gives each track its own channel
        (drums on 10); `channel=0` puts everything on channel 1, which is what a
        one-plugin-per-track Reaper setup like BassMidi expects. Set `mpe=True` to emit
        MPE 1.0 Lower Zone configuration (RPN 00 06) and allocate overlapping notes
        across Member Channels so polyphonic per-note bends never bleed."""
        import mido
        tpb = 480
        mid = mido.MidiFile(ticks_per_beat=tpb)
        meta = mido.MidiTrack()
        meta.append(mido.MetaMessage("track_name", name=self.title, time=0))
        meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(self.bpm), time=0))
        last = 0
        for beat, text in sorted(markers or []):   # e.g. [(8, "loopStart"), (248, "loopEnd")]
            tick = int(beat * tpb)
            meta.append(mido.MetaMessage("marker", text=text, time=tick - last))
            last = tick
        mid.tracks.append(meta)
        tracks = tracks or self.tracks

        if mpe:
            has_drums = any(instruments.resolve(t.instrument)[1] >= 127 for t in tracks)
            n_members = 8 if has_drums else 15
            member_chs = list(range(1, 1 + n_members))
            pitched_tracks = [t for t in tracks if instruments.resolve(t.instrument)[1] < 127]
            if mpe_bend_range is not None:
                zone_range = max(1, min(96, int(round(mpe_bend_range))))
            else:
                needed = [int(round(self._effective_bend_range(t))) for t in pitched_tracks]
                zone_range = max(1, min(96, max(needed + [48])))

            # Emit MPE Configuration Message (RPN 00 06) on Lower Zone Master Channel 0
            cfg = mido.MidiTrack()
            cfg.append(mido.MetaMessage("track_name", name="MPE Lower Zone Setup", time=0))
            cfg.append(mido.Message("control_change", channel=0, control=101, value=0, time=0))
            cfg.append(mido.Message("control_change", channel=0, control=100, value=6, time=0))
            cfg.append(mido.Message("control_change", channel=0, control=6, value=n_members, time=0))
            cfg.append(mido.Message("control_change", channel=0, control=38, value=0, time=0))
            for mch in member_chs:
                cfg.append(mido.Message("control_change", channel=mch, control=101, value=0, time=0))
                cfg.append(mido.Message("control_change", channel=mch, control=100, value=0, time=0))
                cfg.append(mido.Message("control_change", channel=mch, control=6, value=zone_range, time=0))
                cfg.append(mido.Message("control_change", channel=mch, control=38, value=0, time=0))
            mid.tracks.append(cfg)

            member_free_tick = {c: -1 for c in member_chs}
            member_bent = {c: False for c in member_chs}
            member_prog = {}
            for t in tracks:
                fkey, bank, prog = instruments.resolve(t.instrument)
                is_drum = bank >= 127
                label = t.instrument if isinstance(t.instrument, str) else f"{fkey} {bank}:{prog}"
                tr = mido.MidiTrack()
                tr.append(mido.MetaMessage("track_name", name=f"{t.name} [{label}]", time=0))
                if is_drum:
                    msgs = []
                    for s, b, k, v, _bend in t.events:
                        s_tick = int(s * tpb)
                        e_tick = max(s_tick + 1, int((s + b) * tpb) - 1)
                        msgs.append((s_tick, 2, 9, dict(type="note_on", note=max(0, min(127, k)), velocity=v)))
                        msgs.append((e_tick, 0, 9, dict(type="note_off", note=max(0, min(127, k)), velocity=0)))
                    msgs.sort(key=lambda m: (m[0], m[1]))
                    last = 0
                    for tick, _, mch, kw in msgs:
                        tr.append(mido.Message(channel=mch, time=tick - last, **kw))
                        last = tick
                    mid.tracks.append(tr)
                    continue

                if fkey != "synth" and len(pitched_tracks) == 1:
                    tr.append(mido.Message("control_change", channel=0, control=0, value=min(bank, 127), time=0))
                    tr.append(mido.Message("program_change", channel=0, program=prog % 128, time=0))
                if len(pitched_tracks) == 1:
                    tr.append(mido.Message("control_change", channel=0, control=10,
                                           value=int((t.pan + 1) * 63.5), time=0))

                msgs = []  # (tick, order, ch, kwargs)
                ordered = sorted(t.events, key=lambda ev: (ev[0], ev[2]))
                prog_key = (fkey, bank, prog)
                for s, b, k, v, bend in ordered:
                    s_tick = int(s * tpb)
                    e_tick = max(s_tick + 1, int((s + b) * tpb) - 1)
                    same_prog_idle = [
                        c for c in member_chs
                        if member_free_tick[c] <= s_tick and member_prog.get(c) == prog_key
                    ]
                    idle = same_prog_idle or [c for c in member_chs if member_free_tick[c] <= s_tick]
                    mch = idle[0] if idle else min(member_chs, key=lambda c: member_free_tick[c])
                    if fkey != "synth" and member_prog.get(mch) != prog_key:
                        msgs.append((s_tick, 0, mch, dict(type="control_change", control=0, value=min(bank, 127))))
                        msgs.append((s_tick, 0, mch, dict(type="program_change", program=prog % 128)))
                        member_prog[mch] = prog_key
                    has_bend = bool(bends and (bend or t.vibrato) and b > 0)
                    if member_bent[mch]:
                        msgs.append((s_tick, 1, mch, dict(type="pitchwheel", pitch=0)))
                        member_bent[mch] = False
                    msgs.append((s_tick, 2, mch, dict(type="note_on", note=max(0, min(127, k)), velocity=v)))
                    msgs.append((e_tick, 0, mch, dict(type="note_off", note=max(0, min(127, k)), velocity=0)))
                    if has_bend:
                        for pw_tick, pw_ord, pw_kw in self._pitchwheel(t, s, b, bend, tpb, bend_range=float(zone_range)):
                            if pw_tick <= e_tick:
                                msgs.append((pw_tick, pw_ord, mch, pw_kw))
                        member_bent[mch] = True
                    member_free_tick[mch] = max(member_free_tick[mch], e_tick + 1)
                for p_start, p_end in t.pedals:
                    if p_end > p_start:
                        msgs.append((int(round(p_start * tpb)), 1, 0, dict(type="control_change", control=64, value=127)))
                        msgs.append((int(round(p_end * tpb)), 0, 0, dict(type="control_change", control=64, value=0)))
                msgs.sort(key=lambda m: (m[0], m[1], m[2]))
                last = 0
                for tick, _, mch, kw in msgs:
                    tr.append(mido.Message(channel=mch, time=tick - last, **kw))
                    last = tick
                mid.tracks.append(tr)
            mid.save(path)
            return path

        free = [c for c in range(16) if c != 9]          # 15 melodic channels
        pitched = [t for t in tracks if instruments.resolve(t.instrument)[1] < 127]
        # one channel per track if they fit; otherwise tracks with the same
        # instrument share a channel (their pans then share one CC10)
        share = len(pitched) > len(free)
        assigned = {}
        for t in tracks:
            fkey, bank, prog = instruments.resolve(t.instrument)
            is_drum = bank >= 127
            if channel is not None:
                ch = channel
            elif is_drum:
                ch = 9
            else:
                key = (fkey, bank, prog) if share else id(t)
                if key not in assigned:
                    if len(assigned) >= len(free):
                        raise ValueError("more than 15 different pitched instruments; "
                                         "export some tracks separately")
                    assigned[key] = free[len(assigned)]
                ch = assigned[key]
            label = t.instrument if isinstance(t.instrument, str) else f"{fkey} {bank}:{prog}"
            tr = mido.MidiTrack()
            tr.append(mido.MetaMessage("track_name", name=f"{t.name} [{label}]", time=0))
            if fkey != "synth":
                tr.append(mido.Message("control_change", channel=ch, control=0, value=min(bank, 127), time=0))
                tr.append(mido.Message("program_change", channel=ch, program=prog % 128, time=0))
            tr.append(mido.Message("control_change", channel=ch, control=10,
                                   value=int((t.pan + 1) * 63.5), time=0))
            bend_range = self._effective_bend_range(t)
            if bends and abs(bend_range - 2.0) > 1e-6:
                semi_int = max(1, min(24, int(round(bend_range))))
                bend_range = float(semi_int)
                tr.append(mido.Message("control_change", channel=ch, control=101, value=0, time=0))
                tr.append(mido.Message("control_change", channel=ch, control=100, value=0, time=0))
                tr.append(mido.Message("control_change", channel=ch, control=6, value=semi_int, time=0))
                tr.append(mido.Message("control_change", channel=ch, control=38, value=0, time=0))
            msgs = []  # (tick, order, message kwargs)
            for s, b, k, v, bend in t.events:
                msgs.append((int(s * tpb), 2, dict(type="note_on", note=max(0, min(127, k)), velocity=v)))
                msgs.append((max(int(s * tpb), int((s + b) * tpb) - 1), 0,
                             dict(type="note_off", note=max(0, min(127, k)), velocity=0)))
                if bends and (bend or t.vibrato) and b > 0:
                    msgs.extend(self._pitchwheel(t, s, b, bend, tpb, bend_range=bend_range))
            for p_start, p_end in t.pedals:
                if p_end > p_start:
                    msgs.append((int(round(p_start * tpb)), 1, dict(type="control_change", control=64, value=127)))
                    msgs.append((int(round(p_end * tpb)), 0, dict(type="control_change", control=64, value=0)))
            msgs.sort(key=lambda m: (m[0], m[1]))
            last = 0
            for tick, _, kw in msgs:
                tr.append(mido.Message(channel=ch, time=tick - last, **kw))
                last = tick
            mid.tracks.append(tr)
        mid.save(path)
        return path

    @staticmethod
    def _effective_bend_range(t):
        """Determine pitch-wheel semitone range needed for all bends/vibrato on track `t`."""
        max_semi = float(getattr(t, "bend_range", 2.0))
        vib_semi = abs(float(t.vibrato[1])) / 100.0 if t.vibrato else 0.0
        for _, _, _, _, bend in t.events:
            if not bend:
                continue
            if bend[0] in ("norm", "points"):
                peak = max((abs(float(s)) for _, s in bend[2]), default=0.0)
            else:
                peak = abs(float(bend[0]))
            max_semi = max(max_semi, peak + vib_semi)
        return max(2.0, float(math.ceil(max_semi - 1e-6)))

    def _pitchwheel(self, t, start, beats, bend, tpb, bend_range=2.0):
        """Sample the note's pitch curve every ~15 ms as pitch-wheel messages."""
        from .sf2 import pitch_curve
        dur = self.beats_to_sec(beats)
        rate = 66  # messages per second
        n = max(2, int(dur * rate))
        n_samples = max(2, int(dur * SR))
        curve = pitch_curve(n_samples, SR, dur, t.vibrato, bend)
        step_idx = max(1, int(SR / rate))
        ratio = curve[::step_idx][:n]
        out, prev = [], None
        for i, r in enumerate(ratio):
            semis = 12.0 * np.log2(r)
            val = int(round(max(-8192, min(8191, semis / bend_range * 8192.0))))
            if val != prev:
                tick = int(round((start + (i / rate) * self.bpm / 60.0) * tpb))
                out.append((tick, 1, dict(type="pitchwheel", pitch=val)))
                prev = val
        out.append((int(round((start + beats) * tpb)), 1, dict(type="pitchwheel", pitch=0)))
        return out


def _reverb(x, seconds):
    """Cheap stereo hall: convolve with decaying noise."""
    if seconds <= 0 or not np.any(x):
        return x
    rng = np.random.default_rng(7)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    decay = np.exp(-6.9 * t / seconds)
    pre = int(0.02 * SR)
    out = np.empty_like(x)
    for c in range(2):
        ir = rng.standard_normal(n) * decay
        ir[:pre] = 0
        ir /= np.sqrt(np.sum(ir ** 2))
        out[:, c] = fftconvolve(x[:, c], ir)[: len(x)] * 0.5
    return out


def _write_wav(path, data, loop=None):
    """16-bit stereo WAV. loop=(start, end) sample frames adds a 'smpl' chunk with one
    forward loop, which samplers and many game engines use as loop points."""
    import struct
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    pcm = (np.clip(data, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    if loop:
        start, end = loop
        smpl = struct.pack("<9I", 0, 0, int(1e9 / SR), 60, 0, 0, 0, 1, 0) + \
            struct.pack("<6I", 0, 0, start, end - 1, 0, 0)          # end is inclusive
        with open(path, "r+b") as f:
            f.seek(0, 2)
            f.write(b"smpl" + struct.pack("<I", len(smpl)) + smpl)
            size = f.tell()
            f.seek(4)
            f.write(struct.pack("<I", size - 8))
