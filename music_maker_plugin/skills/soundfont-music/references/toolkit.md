# Toolkit API

## Files
| file | what it does |
|---|---|
| `engine/sf2.py` | SoundFont 2.04 parser + sampler (memory-mapped, `sampleModes` 0/1/3, `exclusiveClass` choke); `pitch_curve`, `pitch_lfo` |
| `engine/synth.py` | built-in oscillators: `nes_pulse6/12/25/50`, `nes_triangle`, `nes_noise`, `osc_sine`, `osc_triangle` |
| `engine/instruments.py` | `register_font(key, path)`, `GM` / `KITS` name tables, `INSTRUMENTS` (name -> ("main", bank, program)), `load()` |
| `engine/song.py` | `Song`, `Track`, step-string parser, pedal/strum/arpeggio, `exclusiveClass` choke, mixer + reverb, WAV/stems/MIDI/MPE/loop export |
| `engine/midi_io.py` | `parse_midi_file`, `discover_midi_sources`, `load_midi_into_track` (notes + CC64 pedals) |
| `engine/rpp.py` | `load_rpp(path)` reads a Reaper project into a Song |
| `engine/harmony.py` | `parse(symbol)`, `chord_at(timeline, beat)`, `pitch_class`, `midi_to_name` |
| `engine/voicing.py` | `voice_lead(...)` DP voice-leading with `LOW_INTERVAL_LIMITS` + `apply_voicings(...)` |
| `engine/expression.py` | `humanize_track(...)` / `humanize_song(...)`, `expressive_bends(...)`, `make_bend_curve(...)`: timing/velocity humanization + phrasing-aware pitch bends |
| `engine/patterns.py` | `list_patterns(...)`, `pattern_to_steps(...)` (729 classic drum patterns), `drum_stats_suggest(...)` (Groove MIDI stats) |
| `engine/review.py` | `review_song(...)`, `symbolic_metrics(...)` & `format_review(...)`: detects mud, rubs, parallels, static loops, plus GTR-CTRL `PCE`/`GC`/`PIP`/`UIP` |
| `engine/analysis.py` | `analyze_wav(...)` & `analyze_song_mix(...)`: K-weighted LUFS, 6-band balance, spectral slope vs `tonal-references.json`, stem check |
| `render.py` | `python render.py [song ...]`; exports mix WAV, MIDI, and `out/<song>/multi_track/*.wav` stems |
| `review_song.py` | `python review_song.py <song>` runs score-level diagnostics before/after rendering |
| `analyze_audio.py` | `python analyze_audio.py out/<song>.wav --stems out/<song>/multi_track --ref pop` runs quantitative NumPy QA |
| `analyze_midi.py` | Optional CLI analyzer (`python analyze_midi.py [dir]`) used by `tools/generate_midi_map.py` to build `music_maker_plugin/midi_map.md` or inspect a single standalone `.mid`/folder |
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
| `D5^E5^D5` / `D5^+2^0` | bend-and-release: start D5, bend smoothly to peak (E5 / +2st), release to end (D5 / 0st) |
| `D5~E5` | delayed bend-release: hold clean D5 first, swell up to E5 mid-note, release back to D5 |
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

## Multi-Stage Pitch Bend & Vibrato-by-Bend
```python
from engine import expression

# 1. Preset bends (bend_release, delayed_bend, pre_bend, scoop, dive, bend_vibrato, glide)
t.bend("G5", beats=2.0, style="bend_release", semis=2.0, vel=94)
t.bend("F2", beats=2.0, style="delayed_bend", semis=2.0, vel=88)   # bass hold -> bend +2st -> release
t.bend("C5", beats=1.5, style="dive", semis=1.5, vel=90)           # dive down -1.5st -> return
t.bend("A5", beats=3.0, style="bend_vibrato", semis=0.75, vibrato_waves=3)

# 2. Custom multi-point curve in beats or normalized (0..1)
t.bend("D5", beats=2.0, unit="beats",
       curve=[(0.0, 0.0), (0.3, 2.0), (0.9, 2.0), (1.4, 0.0), (1.8, -1.0), (2.0, 0.0)])

# 3. Attach bend to the last added note(s), or auto-enrich sustained/peak notes
t.seq("G5 - - -", step=0.5).bend_last(style="bend_release", semis=2.0)
expression.expressive_bends(t, role="guitar", seed=42, max_semi=2.0, min_dur=0.75)
```
Note: `export_midi()` automatically emits **RPN `0,0` (Pitch Bend Sensitivity)** when bends exceed `±2` semitones, and `load_midi_into_track()` imports both CC64 pedals and pitch-bend curves.

## Output
- `song.render("out/x.wav")` -> normalized array (and WAV if a path is given).
- `song.export_stems("out/x/multi_track", keep_pan=False)` -> exports each track as an aligned WAV stem (keeps reverb/vibrato/release/bends/pedal; centers pan at `0.0` so DAW mixing starts clean).
- `song.export_midi("out/x.mid", markers=[(8, "loopStart"), (248, "loopEnd")])` (includes CC 64 sustain pedal events; pass `mpe=True, mpe_bend_range=24` for MPE 1.0 Lower Zone `RPN 00 06` and per-note member channel bends).
- `song.render_loop(start_beat, end_beat, "out/x")` -> `_intro`, `_loop`, `_looped` (smpl chunk).
- Verify with numpy: duration, rms/peak per second, per-track first/last beat,
  loop seam jump `abs(loop[0]-loop[-1])` vs typical sample steps.
