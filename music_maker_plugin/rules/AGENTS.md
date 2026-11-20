# Operating Rules for `music_maker_plugin`

This plugin specializes in composing, arranging, mixing, and rendering **instrumental music** and **beats** using SoundFont (`.sf2`) files and a Python toolkit, backed by a full suite of English music-producer expert skills.

## 1. Activating the Skill & Syncing Experts

- **Primary execution skill**: `soundfont-music`.
- When the user requests activation of the plugin or assigns a music production task to it:
  1. **ALWAYS activate `soundfont-music` as the primary orchestrating execution skill**.
  2. **Simultaneously scan and activate the specialist producer skills** in `music_maker_plugin/skills/` (and load specialist agents in `music_maker_plugin/agents/` as needed):
     - `producer-mindset-workflow` — Production brief, Song Planner approval gate (`No House Style`, wildcard), 12-word creative seed, moods/character words, unblocking, dramatic arc, subtractive arranging, finishing discipline.
     - `genre-style-encyclopedia` — Authentic BPM, 7-Axis Style Maps & cross-style borrowing, 10 genre playbooks, global musical idioms.
     - `music-theory-harmony` — Scales, modes, functional/pop/jazz harmony, voice leading, counterpoint, climax & motif craft.
     - `groove-rhythm-drums` — Drum kit roles, pocket, humanization, ghost notes, `3+3+2`, kick-bass composite locking, 729 classic drum patterns & Groove MIDI empirical stats.
     - `orchestration-arrangement` — Register spacing, low-interval hygiene, Rimsky-Korsakov blending & economy of colour, idiomatic piano/organ/pedal/strum/arpeggio writing, song form.
     - `mixing-timbre-mastering` — Lavengood timbre oppositions, Moore's 5 layers, 3D Sound-Box balance, anti-mud, centered-pan `multi_track/` stem QA, K-weighted LUFS & commercial spectral-slope verification.

## 2. Learn & Adopt Style from All MIDI Projects (`midi/`)

- Before laying out or composing a new piece, it is **MANDATORY** to run the MIDI analysis script (`python analyze_midi.py` pointed at `music_maker_plugin/midi/`) so it scans **every MIDI project folder** in `midi/` (e.g., `midi/ballad beat/`) and outputs **all notes, velocities, micro-timing offsets, chord voicings/rolls, CC64 pedal intervals, and pitch-bend events** for every track together with the full text of each project's `readme.md`.
- Each project folder inside `midi/` contains:
  - Multi-track `.mid` / `.midi` files separated by instrument (e.g., `drum.mid`, `bass.mid`, `piano.mid`, `lead.mid`, etc.).
  - A `readme.md` file (written in English by the author) summarizing the project's style, genre, BPM, mood, and arrangement notes.
- **Instrument & context identification**: Always read BOTH the exact **file names (`filename`) / project folder names**, the **full note/pedal/bend dump**, AND the **full `readme.md` text** output by `analyze_midi.py`, because the author names files after instruments and documents style/tempo intent in `readme.md`.
- **Author Style Adoption & Creative Synthesis (Permitted & Encouraged)**:
  - All MIDI projects in `midi/` were performed and arranged personally by the author. **External anti-cloning / copyright guardrails DO NOT apply to the author's own `midi/` library.**
  - You are **explicitly authorized and encouraged to deeply emulate ("adopt") the author's personal playing and arrangement DNA** across `midi/`, so AI-written MIDI loses its robotic/mechanical stiffness and sounds genuinely human:
    1. **Chord progression & voicing style**: how the author moves chords, inverts voicings, spaces left/right hand registers, and walks bass notes.
    2. **Chord strumming & arpeggio spread**: exact roll timing/spread (`strum`, `arpeggio`), staggered note onsets, and sustain durations.
    3. **Velocity dynamics & accents**: strong-vs-weak beat velocity curves, ghost notes, phrase swells, and dynamic contrast across bars.
    4. **Sustain pedal (CC64) habits**: when the author presses, holds, and cleanly lifts/re-presses pedal around chord changes (`pedal`, `pedal_steps`).
    5. **Pitch-bend & expression techniques**: how the author uses pitchwheel/bends (bend direction, semitone depth, timing before/during sustained notes, release/glide habits).
    6. **Drum pocket & transition fills**: kick/snare/hat feel, ghost notes, and 4/8/16-bar fill vocabulary.
  - **Balance imitation with fresh creativity**: Use the author's `midi/` craft DNA as the living, human foundation, then bring original melodic ideas, fresh harmonic/structural variations, and creative touches suited to the new brief. If the author requests continuing an arrangement from an existing MIDI project, load its MIDI tracks directly into the new piece.

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

# Project directory structure rules

It includes a main directory: /
Inside the main directory is the project directory: /project
Inside the project directory, individual projects will be placed there, each with a src folder, an output file, and a multi-track directory.
If the project folder is not found in the home directory, create it automatically.