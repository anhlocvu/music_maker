---
name: soundfont-music
description: Compose, arrange and render music in Python with SoundFonts (.sf2) - game soundtracks (battle, town, boss, encounter themes), chiptune, orchestral or band arrangements, seamless loops for game engines, and MIDI for a DAW such as Reaper. Use when the user wants to write, extend or render a song with soundfonts or Python, design music for a scene or emotion, apply music theory (harmony, modes, melody, voice leading, orchestration), add bends/vibrato/panning/release-cut effects, import a Reaper .RPP project, or export loopable WAV/MIDI.
---

# Making music with Python + SoundFonts

A self-contained toolkit lives in `scripts/toolkit/` (pure numpy SoundFont sampler, no
FluidSynth needed). Copy it into the user's working folder the first time, write songs
as Python files in `songs/`, and render them.

```
cp -r <this skill>/scripts/toolkit <project>/music_toolkit     # once
cd <project>/music_toolkit
python render.py <song>          # -> out/<song>.wav + out/<song>.mid
python list_presets.py main piano
```
Needs `numpy`, `scipy`, `mido` (`pip install mido`). Read `references/toolkit.md` for
the full API before writing a song.

## Step 1: ask for soundfonts
No soundfonts ship with the skill. Before composing, **ask the user which .sf2 files to
use** (a General MIDI font for the core band/orchestra, plus any character fonts they
like - chiptune, console rips, specific instruments). Then register them at the top of
the song file:
```python
from engine import instruments
instruments.register_font("main", r"C:/fonts/MyGM.sf2")      # GM names use "main"
instruments.register_font("chip", r"C:/fonts/Chip.sf2")      # use as ("chip", bank, prog)
```
Run `list_presets.py <key>` on each font and pick presets from what is really there.
If the user has no fonts yet, the built-in synths (`nes_pulse25`, `nes_triangle`,
`nes_noise`, `osc_sine`...) work with none. Files in cloud-synced folders (Dropbox,
OneDrive) may be online-only - read the file once, or ask the user to make it available
offline, before rendering; a large font can take minutes to download.

## Originality - the one hard rule
Write **original** melodies, bass lines, rhythms and drum grooves. Do not transcribe or
closely paraphrase copyrighted songs, not even "just the bass, chords and drums", and not
with a few notes changed. Stock building blocks are fine and are what genres are made of:
common chord progressions, scales and modes, chromatic approach notes, pedal tones,
instrument choices, tempos and keys. When a user asks for a copyrighted piece, offer an
original track in a similar style or sound setup, or an empty kit they fill in by ear
themselves. The user's own compositions (their DAW projects, their melodies) can be used
and extended freely.

## Workflow
1. **Learn MIDI library first (`midi/`)** - run `python analyze_midi.py` to inspect all `.mid` files and multi-track MIDI project folders in `music_maker_plugin/midi/`. Pay close attention to the exact **file names** (`drum.mid`, `bass.mid`, `piano.mid`, etc.) since the user names files after instruments. Study how the user plays, fills, voices chords, drums, and uses dynamics/pedal.
2. **Brief** - instrumental music or beat (no lead vocals unless requested): scene, emotion, loop or one-shot, length, key, tempo. Use `references/game-music-design.md`.
3. **Theory plan** - form (sections and bar counts), chord progression per section, mode, melody motif. Use `references/music-theory.md`.
4. **Palette** - soundfonts from Step 1, presets chosen with `list_presets.py`.
5. **Write** the song file from `songs/_template.py`: sections as chord lists, parts built per bar with helper functions, tracks placed with `at=` beat positions. For piano, e-piano, harp, guitar, or strings needing sustain/space, enable sustain pedal (`t.pedal(...)` / `t.pedal_steps(...)`) and use rolled/arpeggiated voicings (`t.strum(...)`, `t.arpeggio(...)`).
6. **Render and verify** - you can't listen, so check with a short numpy script after every render: each track's first/last beat matches the form, nothing runs past the end, rms/peak are sane, notes/bends are what you intended. Tell the user you verified structure and levels, not how it sounds.
7. **Deliver** mix WAV + MIDI + **`multi_track/` audio stems** (`song.export_stems(out_dir, keep_pan=False)` or via `python render.py <song>`), keeping track effects intact while centering pan (`pan=0`) so the user can mix and edit every track in a DAW; for games, loop files via `render_loop()`.

## Hard-won gotchas
- Every bar needs the right number of tokens for its `step` (16 at 0.25 in 4/4). Build
  bars with helpers, slice lists (`(notes * 6)[:16]`), then check `track.length()` -
  misaligned bars drift silently.
- Loops that shrink a value geometrically (accelerating rolls) need a floor, or never end.
- Transposing a whole song: give pitched tracks `transpose=SHIFT`, never drums. A preset
  detuned with `cents=+500` needs its notes written 5 semitones lower to stay in key.
- More than 15 pitched tracks: `export_midi` shares channels between tracks with the
  same instrument.
- An output WAV locked by a media player: `render.py` writes `_v2` instead.
- Windows Git Bash: heredoc Python containing backslashes can break; use file edits.

## Loops for games
`song.render_loop(loop_start_beat, loop_end_beat, "out/name")` renders the loop twice and
keeps the second pass (so reverb tails wrap), writing `_intro.wav`, `_loop.wav` and
`_looped.wav` (with a `smpl` loop chunk), and prints LOOPSTART/LOOPLENGTH in samples.
Make the music itself loop: no final hit, the last bar leads into the first (dominant or
half-step approach chord, drum fill into the crash), no notes held past the loop end.
MIDI: `export_midi(path, markers=[(start, "loopStart"), (end, "loopEnd")])`.

## References
- `references/toolkit.md` - engine API: Song/Track, step strings, bends, glides, vibrato,
  autopan, release cut, synths, Reaper import, MIDI/loop export.
- `references/music-theory.md` - harmony and function, voice leading, progressions,
  modes, melody and motif development, rhythm, orchestration and texture, form.
- `references/game-music-design.md` - emotion to musical choices, game structure,
  adaptive music, leitmotifs, and arranging techniques that worked in practice.
