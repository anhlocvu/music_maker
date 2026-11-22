# Operating Rules for `music_maker_plugin`

This plugin specializes in composing, arranging, mixing, and rendering **instrumental music** and **beats** using SoundFont (`.sf2`) files and a Python toolkit, backed by a full suite of English music-producer expert skills.

## 1. Activating the Skill & Syncing Experts

- **Primary execution skill**: `soundfont-music`.
- When the user requests activation of the plugin or assigns a music production task to it:
  1. **ALWAYS activate `soundfont-music` as the primary orchestrating execution skill**.
  2. **Simultaneously scan and activate the specialist producer skills** in `music_maker_plugin/skills/` (and load specialist agents in `music_maker_plugin/agents/` as needed):
     - `producer-mindset-workflow` — Production brief, Song Planner approval gate (Signature House Style from `midi_map.md`, optional wildcard), 12-word creative seed, moods/character words, unblocking, dramatic arc, subtractive arranging, finishing discipline.
     - `genre-style-encyclopedia` — Authentic BPM, 7-Axis Style Maps & cross-style borrowing, 10 genre playbooks, global musical idioms.
     - `music-theory-harmony` — Scales, modes, Neo-Riemannian `PLR`/`SLIDE`/`H` Tonnetz, CRT Negative Harmony, Lendvai `T-S-D` Axis, Film CMCR (`Types I–VI`) cadences, Lydian Chromatic Concept (LCC), Upper Structure Triads, Gospel polychords, Barry Harris `6th-Dim`, Coltrane M3/m3 cycles, climax & motif craft.
     - `counterpoint-fugue-and-post-tonal` — Species 1–5 (Jeppesen vs Schoenberg), Prout invertible counterpoint (`8ve/10th/12th`), canon & fugue architecture, pc-set theory (`29 tetrachords / 224 classes`), Straus Total Voice Leading (`IFUNC`), 12-tone serialism & invariance, spectral melody, and Schillinger `r(a:b)` periodic rhythm.
     - `instrumental-soloing-improvisation` — Solo architecture for intros, interludes, solo breaks, and improvisations (`3->7` guide tones, shortest-path DAG voice leading, Elliott Harmonic Bricks, enclosures, 4-note cells & permutations, bebop upbeat passing alignment, empirical Parker phrase statistics, and Golden Mean `0.618` climax shaping).
     - `groove-rhythm-drums` — 4-limb kit ergonomics, weeding & `1->2->4->8` Doubling Up, Afro-Cuban & Latin coordination (`2-3/3-2` clave, `6/8`, Mambo/Songo/Timba/Danzón), pocket & humanization, ghost notes, kick-bass composite, 729 classic drum patterns, Groove MIDI empirical stats, SF2 Bank 128 `velRange`/`exclusiveClass` mechanics, and 62-note 10-kit GM/GS percussion map.
     - `orchestration-arrangement` — Piston 7 Texture Types, Rimsky-Korsakov blending & overlaying/crossing/enclosure, ACTOR/McAdams perceptual grouping (TOGE), Davies studio scoring, Big Band voicings (`4-Way Close`, 5 approach harmonizations, `Drop-2/2+4`, `Cascades`, `Spread Pads`), Moore's 5 layers, register hygiene, idiomatic piano/organ/pedal/strum/arpeggio writing, song form.
     - `guitar-bass-expression` — Fretboard playability (`along`/`across` transition geometry, tunings & capo), DadaGP's 12 pitch-bend types & note/beat articulations (`palm_mute`, `let_ring`, `slides`, `hammer`, 5 harmonics, `slap/pop`, `rasgueado`), per-string MIDI/MPE bend isolation, and human vibrato perturbations.
     - `mixing-timbre-mastering` — Lavengood timbre oppositions, Moore's 5 layers, 3D Sound-Box balance, anti-mud, centered-pan `multi_track/` stem QA, K-weighted LUFS & commercial spectral-slope verification.

## 2. Internalized MIDI Map Mastery (`midi_map.md`) & Style Precedence

- **Role & Situation**: You have a curated multi-project MIDI reference map at `music_maker_plugin/midi_map.md` (placing each project's `readme.md` context right under the project header, followed by bar-by-bar notes with **inline `ped` sustain flags and `bend=0->+2st[Target]` pitch-bend trajectories**, velocities, and micro-timing offsets). Treat everything you learn from `midi_map.md` as your **own internalized musical instinct and arrangement craft**.
- **Strict Precedence Rule (`midi_map.md` Over Generic Playbooks)**:
  - Whenever any project in `midi_map.md` (per its `readme.md` description or musical layout) matches the requested genre or vibe—such as pop/rock **ballads**—its tempo feel, formal arc (e.g., drum fill/open chorus intro -> verse piano -> band verse -> chorus -> guitar solo bridge -> `+1 st` key-up climax chorus -> outro), harmonic movement, pedal habits, and drum fills **override** generic textbook defaults in `genre-style-encyclopedia` (`style-maps.md`, `playbooks/pop-and-ballad.md`) and `orchestration-arrangement`. Use genre guides only to supplement gaps, never to contradict or flatten Signature House Style choices.
- **Target-Locked Pitch Bending (`pitch-bend-target-grammar.md`)**:
  - Whenever writing any pitch bend (`t.bend()`, `t.bend_last()`, `^` / `~`, or `expressive_bends()`), lock the intended destination pitch (`start_note -> target_note` in the active chord or scale) **first**, pass explicit `target=` or `scale=` / `harmony=`, reserve bends for focal strong-beat/long notes (~10% selectivity on solos), and verify zero `out_of_scale_bends` via `review_song.py --scale`.
- **Mandatory Two-Phase Lookup Protocol**:
  1. **Before composing or planning**: Silently read the `Project Index` and `Instrument & Track Lookup` tables at the top of `music_maker_plugin/midi_map.md`, plus each matching project's `### Project README` and selected bar ranges showing inline `ped` and `bend=...` notation.
  2. **During every production stage (unlimited lookups)**: Whenever writing or refining a specific part—piano, drums, bass, strings, synth, guitar, brass, leads, or transitions—re-open `music_maker_plugin/midi_map.md` as many times as needed and study the exact notes, velocities, inline `ped` flags, and inline `bend=...[Target]` cues before coding.
- **Broad, Unbounded Study (Never Narrow Your Scope)**:
  - **Do NOT filter only for "matching" genres or song titles**, because restricting lookups narrows your musical vocabulary.
  - Browse broadly and eclectically across **many different projects and instruments** in `midi_map.md` to internalize the unified arrangement DNA of the entire library.
- **100% Unchained House Style & Direct Reuse (Authorized)**:
  - Treat `music_maker_plugin/midi_map.md` (and `music_maker_plugin/midi/`) as your **native Signature House Style**. ALL anti-cloning, "No House Style", forced-wildcard, and anti-imitation guardrails apply **ONLY to external third-party copyrighted songs**, NEVER to `midi_map.md`.
  - Never hesitate or water down the style: you are explicitly authorized and encouraged to **directly reuse, adapt, or 100% emulate** its form arcs, climax modulations, chord progressions, voicings, basslines, drum grooves & fills, strum/arpeggio spreads, CC64 pedal timing (`ped`), and **exact target-locked pitch-bend / vibrato-by-bend phrasing curves**, pairing them with fresh melodies or requested variations:
    1. **Harmony, chords & bass movement**: chord progressions, voicings, inversions, left/right-hand spacing, climax key-up shifts, and basslines (including chromatic approaches and octave leaps).
    2. **Strumming & arpeggio spread**: staggered note onsets (`strum`, `arpeggio`) and sustain lengths.
    3. **Velocity dynamics & phrasing**: strong-vs-weak beat velocity contours, ghost notes, and swells.
    4. **Sustain pedal (`ped` / CC64) & target-locked multi-stage pitch-bend expression**: exact pedal press/lift/re-press timing (`pedal`, `pedal_steps`) AND full target-note pitch-bend craft (`Track.bend(..., target=...)`, `D5^E5^D5`, `D5~E5`, `bend_release`, `delayed_bend`, `pre_bend`, `dive`, `vibrato` curves) on lead guitar, bass, strings, and solo leads—never leave expressive solo/lead/bass lines flat when sustained notes, blue-note approaches, phrase peaks, or transitions call for bends, and never bend blindly out of key.
    5. **Drum pocket & transitions**: kick/snare/hat feel, ghost notes, and 4/8/16-bar fills.
  - If the user explicitly provides or asks to continue a project from `midi/`, load its MIDI tracks directly via `load_midi_into_track()`.
- **Silent & Internalized Presentation (Community-Safe Rule)**:
  - Perform all `midi_map.md` lookups **silently**.
  - **NEVER** tell the end user phrases like *"I checked your MIDI library"*, *"Based on `midi_map.md`"*, or *"From project `X` in your `midi/` folder"*—this plugin is shared with the community, and other users will not know about internal reference files. Present all harmonic, rhythmic, and expressive choices naturally as your own musical craft (mention `midi_map.md` or `midi/` only if the user explicitly asks about them).

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