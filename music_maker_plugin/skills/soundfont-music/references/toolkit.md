# Toolkit API

## Files
| file | what it does |
|---|---|
| `engine/sf2.py` | SoundFont 2 parser + sampler (memory-mapped, handles huge fonts); `pitch_curve`, `pitch_lfo` |
| `engine/synth.py` | built-in oscillators: `nes_pulse6/12/25/50`, `nes_triangle`, `nes_noise`, `osc_sine`, `osc_triangle` |
| `engine/instruments.py` | `register_font(key, path)`, `GM` / `KITS` name tables, `INSTRUMENTS` (name -> ("main", bank, program)), `load()` |
| `engine/song.py` | `Song`, `Track`, step-string parser, pedal/strum/arpeggio, mixer + reverb, WAV/stems/MIDI/loop export |
| `engine/midi_io.py` | `parse_midi_file`, `discover_midi_sources`, `load_midi_into_track` (notes + CC64 pedals) |
| `engine/rpp.py` | `load_rpp(path)` reads a Reaper project into a Song |
| `engine/harmony.py` | `parse(symbol)`, `chord_at(timeline, beat)`, `pitch_class`, `midi_to_name` |
| `engine/voicing.py` | `voice_lead(...)` DP voice-leading with `LOW_INTERVAL_LIMITS` + `apply_voicings(...)` |
| `engine/expression.py` | `humanize_track(...)` / `humanize_song(...)`: phase-correction timing, `1/f^beta` velocity drift, phrase arches, cymbal cycles |
| `engine/patterns.py` | `list_patterns(...)`, `pattern_to_steps(...)` (729 classic drum patterns), `drum_stats_suggest(...)` (Groove MIDI stats) |
| `engine/review.py` | `review_song(...)` & `format_review(...)`: detects low-interval mud, minor 2nd/9th rubs, parallels, static loops |
| `engine/analysis.py` | `analyze_wav(...)` & `analyze_song_mix(...)`: K-weighted LUFS, 6-band balance, spectral slope vs `tonal-references.json`, stem check |
| `render.py` | `python render.py [song ...]`; exports mix WAV, MIDI, and `out/<song>/multi_track/*.wav` stems |
| `review_song.py` | `python review_song.py <song>` runs score-level diagnostics before/after rendering |
| `analyze_audio.py` | `python analyze_audio.py out/<song>.wav --stems out/<song>/multi_track --ref pop` runs quantitative NumPy QA |
| `analyze_midi.py` | `python analyze_midi.py [dir]` scans all MIDI project folders in `midi/` and outputs **all notes (with exact beat, duration, velocity), all CC64 pedal intervals, all pitch-bend events**, human-feel stats, plus each project's full `readme.md` text |
| `list_presets.py` | `python list_presets.py <font key> [search]` prints ready-to-paste tuples |

## Song and Track
```python
from engine.song import Song, note_number
song = Song("Title", bpm=120, room=1.5, swing=0.0, pitch=0)   # pitch: master cents
t = song.track("lead", "piano",            # name in INSTRUMENTS, or ("font", bank, prog)
               volume=0.8, pan=-0.2,        # pan -1..1
               reverb=0.3,                  # send amount
               transpose=0, cents=0,        # semitones / fine detune
               vibrato=(5.5, 30, 0.15, 0.2),# rate Hz, depth cents, delay s, fade s
               autopan=(2, 0.8),            # period beats, depth: sweeps notes L/R in tempo
               release=0.02)                # cap the release: 0.02 = "release cut" staccato
t.seq("C5 - E5 G5 | C6 - - - |", step=0.5, at=16, vel=100, repeat=1)
t.rest(4)                                   # move the cursor
t.events                                    # [(start_beat, beats, key, vel, bend)]
```
`seq` continues from where the track last ended unless `at=` is given. Tracks can also
be filled directly via `t.events` (used for generated patterns like accelerating rolls).

## Step strings (one token per step)
| token | meaning |
|---|---|
| `C5` `F#3` `Bb4` | note (C4 = middle C = 60) |
| `C4+E4+G4` | chord |
| `-` | hold previous note one more step |
| `.` | rest |
| `\|` | bar line (ignored) |
| `C5@60` | velocity |
| `D5^E5` | guitar-style bend: start D5, bend up to E5 in ~0.1 s, hold |
| `B5>E4` | glide: slide evenly from B5 to E4 over the note |
| `kick snare hat ohat crash ride tom1..4 clap rim tamb shaker cowbell ...` | GM drum names |
For non-GM kits (e.g. GS ETHNIC: E2 hyoshigi, F#2/G2 kotsuzumi, D6 shaker) use note names.

## Useful helpers to write in song files
- Build bars from a chord list: `" | ".join(f"{CH[c]} . . {CH[c]} ..." for c in FORM)`.
- Diatonic harmony a third below, octave doubling, `cut()` (holds -> rests for staccato),
  `shift_chord(chord, semis)` for register changes and half-step "slide-in" stabs.
- Syncopated bass: 16ths on a 3+3+2 grid, chromatic approach a half step below the next
  root, and anticipate the next root on the last 16th tied over the bar line.

## Reaper import
`load_rpp(path, font_overrides={"missing.sf2": "local.sf2"})` -> Song with tempo, each
track's name/volume/pan, inline MIDI items, and the BassMidi VSTi's soundfont + preset
(bank at state byte 2715, program at 2719). Other instruments fall back to the GM piano in the "main" font.
Per-track MIDI for dragging back into Reaper: `song.export_midi(path, tracks=[t], channel=0)`
(pitch bends/vibrato are written as pitch-wheel data, +/-2 semitone range).

## Pedal & Rải nhạc cụ (Sustain, Strum, Arpeggio)
```python
# Rải hợp âm piano/guitar/harp (spread=0.05 beats giữa các nốt)
t.strum("C4+E4+G4+B4", beats=4.0, spread=0.05, vel=88, direction="up")

# Đánh rải arpeggio theo nhịp step=0.25, giữ ngân tới cuối ô nhịp
t.arpeggio("A3+C4+E4+G4", step=0.25, beats=4.0, pattern="updown", vel=82, hold=True)

# Đạp sustain pedal (kéo dài vang tự nhiên khi render WAV + ghi MIDI CC 64)
t.pedal(0, 3.95)                  # đạp từ beat 0, nhả nhẹ trước beat 4
t.pedal_steps(step=4.0, lift=0.05) # tự động đạp/nhả lại mỗi 4 beats
```

## Output
- `song.render("out/x.wav")` -> normalized array (and WAV if a path is given).
- `song.export_stems("out/x/multi_track", keep_pan=False)` -> exports each track as an aligned WAV stem (keeps reverb/vibrato/release/bends/pedal; centers pan at `0.0` so DAW mixing starts clean).
- `song.export_midi("out/x.mid", markers=[(8, "loopStart"), (248, "loopEnd")])` (includes CC 64 sustain pedal events).
- `song.render_loop(start_beat, end_beat, "out/x")` -> `_intro`, `_loop`, `_looped` (smpl chunk).
- Verify with numpy: duration, rms/peak per second, per-track first/last beat,
  loop seam jump `abs(loop[0]-loop[-1])` vs typical sample steps.
