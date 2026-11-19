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
import os
import wave
import numpy as np
from scipy.signal import fftconvolve

from .sf2 import SoundFont
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
                 transpose=0, release=None, cents=0, vibrato=None, autopan=None):
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
                        for nm in tok.split("+"):
                            bend = None
                            for sym, kind in (("^", "bend"), (">", "glide")):
                                if sym in nm:
                                    nm, to = nm.split(sym)
                                    bend = (note_number(to) - note_number(nm), kind)
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
        buf = np.zeros((n, 2), np.float32)
        cache = {}
        for start, beats, key, vel, bend in t.events:
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
            i = int(self.beats_to_sec(s) * SR)
            m = min(len(v), n - i)
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
    def export_midi(self, path, tracks=None, channel=None, bends=True, markers=None):
        """Write a type-1 MIDI file. `channel=None` gives each track its own channel
        (drums on 10); `channel=0` puts everything on channel 1, which is what a
        one-plugin-per-track Reaper setup like BassMidi expects. Bends, glides and
        vibrato are written as pitch-wheel data (range +/-2 semitones)."""
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
            msgs = []  # (tick, order, message kwargs)
            for s, b, k, v, bend in t.events:
                msgs.append((int(s * tpb), 2, dict(type="note_on", note=max(0, min(127, k)), velocity=v)))
                msgs.append((max(int(s * tpb), int((s + b) * tpb) - 1), 0,
                             dict(type="note_off", note=max(0, min(127, k)), velocity=0)))
                if bends and (bend or t.vibrato) and b > 0:
                    msgs.extend(self._pitchwheel(t, s, b, bend, tpb))
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

    def _pitchwheel(self, t, start, beats, bend, tpb):
        """Sample the note's pitch curve every ~15 ms as pitch-wheel messages."""
        from .sf2 import pitch_curve
        dur = self.beats_to_sec(beats)
        rate = 66  # messages per second
        n = max(2, int(dur * rate))
        ratio = pitch_curve(int(dur * SR), SR, dur, t.vibrato, bend)[:: max(1, int(SR / rate))][:n]
        out, prev = [], None
        for i, r in enumerate(ratio):
            semis = 12 * np.log2(r)
            val = int(max(-8192, min(8191, semis / 2.0 * 8192)))
            if val != prev:
                tick = int((start + self.beats_to_sec(0) + i / rate * self.bpm / 60.0) * tpb)
                out.append((tick, 1, dict(type="pitchwheel", pitch=val)))
                prev = val
        out.append((int((start + beats) * tpb), 1, dict(type="pitchwheel", pitch=0)))
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
