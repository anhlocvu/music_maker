# Song Planner Protocol (Pre-Composition Sheet & Approval Gate)

Adapted for `music_maker_plugin` from the `song-planner` workflow. Use this before writing Python score code whenever creating a new track from a brief, a user-played riff/MIDI, or a structural reference.

## Core Discipline: No House Style

- **Never impose a generic AI default tempo, tuning, form, or mechanical grid.** Every musical choice must trace to the user's request, your internalized craft from `music_maker_plugin/midi_map.md`, or an intentional creative seed (e.g., drawing 12 words from `assets/association-words.tsv` when open parameters remain).
- **Silent Style Assimilation (`midi_map.md`)**: Before drafting the Song Sheet and continuously during every instrument phase, silently read broad sections of `music_maker_plugin/midi_map.md` (not only matching genres) to absorb 100% of its chord-progression tendencies, strumming/rolling spread, velocity accents, CC64 pedal timing, pitch-bend phrasing, and groove/fill habits. Treat these habits as innate personal instinct—**never mention `midi_map.md` or "your MIDI library" to the end user**.
- If the brief says vague adjectives like "fast" or "epic", ground them using `references/character-words.md` / `references/moods.md` or ask in **one short batch** of clarifying questions.

## Workflow Steps

1. **Gather Input**: Collect the user's brief, any user-provided MIDI file, or an external reference song (while silently consulting `music_maker_plugin/midi_map.md` in the background).
   - **From a riff/MIDI file provided by the user**: Preserve its notes, timing, and feel unchanged (`load_midi_into_track`), building other sections around it without silently quantizing or stripping its human feel.
   - **From an external reference song**: Extract **form and energy arc only** (section order, bar counts, tempo feel, breakdown placement). Never copy an external reference's riffs, melodies, chord voicings, or drum patterns.
2. **One-Batch Clarification**: Ask once, in a single concise batch, only for missing material choices that block the composition (tempo/feel, key/low note, rough length or loop vs. one-shot, soundfont/instrument palette, energy arc). Respect anything the user explicitly delegated.
3. **12-Word Association Seed (Optional Anti-Cliché Anchor)**: For open creative parameters (title, scene mood, harmonic color, contrast shift), draw 12 words from `assets/association-words.tsv` (or accept the user's words) and weave them into one coherent musical image so two similar briefs never converge to the same cliché.
4. **Draft the Song Sheet (Plan Before Code)**:
   - Record BPM, meter, key/mode, total bars/loop points, instruments, and section-by-section roles (what changes, where energy peaks, where it breathes).
   - Include **at least one `wildcard` section or arrangement idea** (`[wildcard]`) so the draft isn't only the most predictable reading of the brief.
5. **Explicit Approval Gate**: Present the Song Sheet clearly and wait for the user's explicit approval (or edits) before writing `songs/<name>.py` and rendering audio + `multi_track/` stems.
6. **Narrow Revision Loop**: After rendering and running quantitative QA (`engine/review.py` + `engine/analysis.py`), revise only the targeted bars/tracks that need improvement rather than throwing out the whole arrangement.
