# Song Planner Protocol (Pre-Composition Sheet & Approval Gate)

Adapted for `music_maker_plugin` from the `song-planner` workflow. Use this before writing Python score code whenever creating a new track from a brief, a user-played riff/MIDI, or a structural reference.

## Core Discipline: No House Style

- **Never impose default tempos, tunings, forms, or section lengths.** Every musical choice must trace to the user's request, the author's `midi/` style profile (`analyze_midi.py`), or an intentional creative seed (e.g., drawing 12 words from `assets/association-words.tsv` when open parameters remain).
- If the brief says vague adjectives like "fast" or "epic", ground them using `references/character-words.md` / `references/moods.md` or ask in **one short batch** of clarifying questions.

## Workflow Steps

1. **Gather Input**: Collect the user's brief, any played riff/MIDI (`music_maker_plugin/midi/`), or a reference song.
   - **From a riff the user played**: The user's riff/MIDI is the anchor—preserve its notes, timing, and feel unchanged (`load_midi_into_track`). Build other sections as contrast or development around it; never silently quantize or rewrite their motif unless asked.
   - **From a reference song**: Extract **form and energy arc only** (section order, bar counts, tempo feel, breakdown placement). Never copy the reference's riffs, melodies, chord voicings, or drum patterns.
2. **One-Batch Clarification**: Ask once, in a single concise batch, only for missing material choices that block the composition (tempo/feel, key/low note, rough length or loop vs. one-shot, soundfont/instrument palette, energy arc). Respect anything the user explicitly delegated.
3. **12-Word Association Seed (Optional Anti-Cliché Anchor)**: For open creative parameters (title, scene mood, harmonic color, contrast shift), draw 12 words from `assets/association-words.tsv` (or accept the user's words) and weave them into one coherent musical image so two similar briefs never converge to the same cliché.
4. **Draft the Song Sheet (Plan Before Code)**:
   - Record BPM, meter, key/mode, total bars/loop points, instruments, and section-by-section roles (what changes, where energy peaks, where it breathes).
   - Include **at least one `wildcard` section or arrangement idea** (`[wildcard]`) so the draft isn't only the most predictable reading of the brief.
5. **Explicit Approval Gate**: Present the Song Sheet clearly and wait for the user's explicit approval (or edits) before writing `songs/<name>.py` and rendering audio + `multi_track/` stems.
6. **Narrow Revision Loop**: After rendering and running quantitative QA (`engine/review.py` + `engine/analysis.py`), revise only the targeted bars/tracks that need improvement rather than throwing out the whole arrangement.
