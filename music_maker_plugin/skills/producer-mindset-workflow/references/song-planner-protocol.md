# Song Planner Protocol (Pre-Composition Sheet & Approval Gate)

Adapted for `music_maker_plugin` from the `song-planner` workflow. Use this before creating any new track from a brief, a user-played riff/MIDI, or a structural reference. Always present Song Sheets and updates in **pure musical/production language** (never mention Python, source code, scripts, or function names to the user).

## Core Discipline: Parallel Knowledge (`Docs ‖ midi_map.md`) & Proactive Flow

- **Dual Top-Priority Parallel Study**: Consult specialist theory/arrangement guides **in parallel with** `music_maker_plugin/midi_map.md`—both are co-equal #1 priorities. `midi_map.md` holds internalized performance nuances that written docs alone cannot fully capture.
- **Never impose a generic AI default tempo, tuning, form, or mechanical grid.** Ground musical choices in the user's request and your **unchained Signature House Style** from `music_maker_plugin/midi_map.md` (use `assets/association-words.tsv` only when open creative parameters remain and the brief asks for fresh imagery).
- **Proactive Transitions & Fills**: Treat the user's section list as a core skeleton—proactively include connecting transitions (turnarounds, pre-chorus lifts, short bridges/interludes), drum fills/pickups, and fuzzy boundaries in the Song Sheet so the arrangement never feels abruptly pasted together.
- **100% Unchained Style Adoption (`midi_map.md`)**: Before drafting the Song Sheet and continuously during every instrument phase, silently read broad sections of `music_maker_plugin/midi_map.md` (not only matching genres). You have full permission to **directly reuse or emulate 100%** of its chord progressions, voicings/strums, basslines, drum fills, velocity accents, CC64 pedal timing, and pitch-bend/vibrato-by-bend phrasing—never dilute or steer away from `midi_map.md` out of fear of "copying". Treat these habits as innate personal instinct and **never mention `midi_map.md` or "your MIDI library" to the end user**.
- If the brief says vague adjectives like "fast" or "epic", ground them using `references/character-words.md` / `references/moods.md` or ask in **one short batch** of clarifying questions.

## Workflow Steps

1. **Gather Input**: Collect the user's brief, any user-provided MIDI file, or an external reference song (while silently consulting `music_maker_plugin/midi_map.md` in parallel with specialist docs).
   - **From a riff/MIDI file provided by the user**: Preserve its notes, timing, pedals, and pitch bends unchanged, building other sections around it without silently quantizing or stripping its human feel.
   - **From an external copyrighted reference song**: Extract **form and energy arc only** (section order, bar counts, tempo feel, breakdown placement). Never copy an external third-party reference's riffs, melodies, chord voicings, or drum patterns. (This restriction does **not** apply to `midi_map.md`.)
2. **One-Batch Clarification**: Ask once, in a single concise batch, only for missing material choices that block the composition (tempo/feel, key/low note, rough length or loop vs. one-shot, soundfont/instrument palette, energy arc). Respect anything the user explicitly delegated.
3. **12-Word Association Seed (Optional Anti-Cliché Anchor)**: When open creative parameters remain and the user wants fresh theme imagery, optionally draw 12 words from `assets/association-words.tsv` (or accept the user's words).
4. **Draft the Song Sheet (Plan Before Production)**:
   - Record BPM, meter, key/mode, total bars/loop points, instruments, expressive articulation/pitch-bend plan, **connecting transitions & drum fills**, and section-by-section roles (what changes, where energy peaks, where it breathes).
   - Optionally include a `wildcard` arrangement idea (`[wildcard]`) **only** if it complements the style or the user asks for an unexpected twist—do not force jarring wildcards that contradict the core `midi_map.md` idiom.
5. **Explicit Approval Gate**: Present the Song Sheet clearly in pure musical terms and wait for the user's explicit approval (or edits) before producing the arrangement, stereo mix, MIDI, and `multi_track/` stems.
6. **Narrow Revision Loop**: After rendering and running quantitative QA (`engine/review.py` + `engine/analysis.py`), revise only the targeted bars/tracks that need improvement rather than throwing out the whole arrangement.
