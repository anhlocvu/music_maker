# Operating Rules for `music_maker_plugin`

This plugin specializes in composing, arranging, mixing, and rendering **instrumental music** and **beats** using SoundFont (`.sf2`) files and a Python toolkit, backed by a full suite of English music-producer expert skills.

## 1. Activating the Skill & Syncing Experts

- **Primary execution skill**: `soundfont-music`.
- When the user requests activation of the plugin or assigns a music production task to it:
  1. **ALWAYS activate `soundfont-music` as the primary orchestrating execution skill**.
  2. **Simultaneously scan and activate the specialist producer skills** in `music_maker_plugin/skills/` (and load specialist agents in `music_maker_plugin/agents/` as needed):
     - `producer-mindset-workflow` — Production brief, creative constraints, unblocking, dramatic arc, subtractive arranging, finishing discipline.
     - `genre-style-encyclopedia` — Authentic BPM, rhythm/harmony pillars, global musical idioms, hybrid blending.
     - `music-theory-harmony` — Scales, modes, functional/pop/jazz harmony, voice leading, counterpoint, motifs.
     - `groove-rhythm-drums` — Drum kit roles, pocket, humanization, ghost notes, `3+3+2`, kick-bass composite locking.
     - `orchestration-arrangement` — Register spacing, Rimsky-Korsakov blending & economy of colour, idiomatic pedal/strum/arpeggio writing, song form.
     - `mixing-timbre-mastering` — Lavengood timbre oppositions, Moore's 5 layers, 3D Sound-Box balance, anti-mud, centered-pan `multi_track/` stem QA, NumPy audio verification.

## 2. Learn from the Entire MIDI Library Before Starting Work (`midi/`)

- Before laying out or composing a new piece, it is **MANDATORY** to check and run the MIDI analysis script (`python analyze_midi.py` pointed at the `music_maker_plugin/midi/` directory) to learn from all existing MIDI data.
- The `midi/` library may contain:
  - Individual `.mid` / `.midi` files (single-track or multi-track).
  - **MIDI project folders** containing multiple `.mid` files separated by instrument (e.g., `drum.mid`, `bass.mid`, `piano.mid`, `lead.mid`, etc.).
- **Instrument identification via filenames**: Always read the exact **file names (`filename`)** and **project folder names** output by `analyze_midi.py`, because the author names files after the corresponding instruments.
- **MIDI learning mindset**: The MIDI files in `midi/` were performed and arranged by the author (the user) personally. Treat them as the core reference material for learning the author's **playing style, voicing spread, section-transition fills, drumming technique (kick/snare/hat/ghost notes/fills), bass lines, voicing arrangements, dynamics, and arrangement thinking**. If the author requests continuing an arrangement from an existing MIDI sketch, load that MIDI data directly into the new piece.

## 3. Pedal (Sustain) Technique & Instrument Spreading

- For instruments that need natural sustain, such as **piano, e-piano, harp, guitar, strings, bell/celesta, etc.**, do not leave chords dry and stiff in sections that call for emotion or a wide sonic space:
  - **Proactively enable Pedal mode (`track.pedal(...)`)** for sections where you want to preserve sustain (this both keeps the sound smooth and long-lasting when rendering WAV and records standard MIDI CC 64 `Sustain Pedal`). Remember to release/re-press the pedal on chord changes to avoid muddy sound.
  - **Proactively spread instruments (`track.strum(...)` / `track.arpeggio(...)`)** or offset chord notes in time naturally in accompaniment piano, harp, and guitar sections.

## 4. Multi-Track Audio Export Rules (`multi_track/`)

- After finalizing a piece, in addition to the MIDI file and the full mix WAV, it is **MANDATORY** to create a `multi_track/` directory (inside the song's output directory, e.g., `out/<song>/multi_track/`) and export **all tracks as separate `.wav` audio files** so the user can bring them into a DAW for mixing or editing.
- **Rules for effects & pan handling in multi-track export**:
  - **Preserve all instrument effects** (reverb, vibrato, release, bend/glide, timbre, relative volume balance, etc.).
  - **DO NOT preserve track `pan`** in the multi-track export (all track stems are centered / `pan=0`, letting the user freely pan them in the DAW).
  - All stem files must have their starting point aligned at `beat 0` (same time reference), so they snap into the DAW grid right away when dropped in.
