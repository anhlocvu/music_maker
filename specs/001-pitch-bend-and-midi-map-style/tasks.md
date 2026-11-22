# Tasks: Target-Aware Pitch Bending & Inline MIDI-Map Style Adoption

## Phase 1: Tests First (TDD Red)
- [x] T001 Add unit tests in `tools/tests/test_toolkit_bends.py` for: (a) inline note bend formatting & README-first ordering in `midi_io.summarize_track` / `analyze_midi.format_markdown` with zero separate `All Pitch Bend Events`; (b) `Track.bend(target=...)` and `Track.bend_last(target=...)`; (c) scale/chord-aware `expressive_bends()` avoiding out-of-scale bends (e.g., `E5` in C major never bends `+2st` to `F#5`); (d) `review_song()` detecting `out_of_scale_bends`.

## Phase 2: Toolkit & `midi_map.md` Implementation (TDD Green)
- [x] T002 Upgrade `music_maker_plugin/skills/soundfont-music/scripts/toolkit/engine/midi_io.py` and `analyze_midi.py` to summarize bends inline on notes (with target pitch & gesture type), deduplicate near-identical CC64 pedals + mark `ped` inline where helpful, remove `All Pitch Bend Events`, and place `### Project README` first in each project block.
- [x] T003 Upgrade `engine/song.py` (`Track.bend` / `Track.bend_last` `target=` support), `engine/expression.py` (scale/chord-aware `expressive_bends()`), and `engine/review.py` (`out_of_scale_bends` audit).
- [x] T004 Regenerate `music_maker_plugin/midi_map.md` via `tools/generate_midi_map.py` and verify max line length < 46,080 bytes.

## Phase 3: Skills & Rules Upgrades (`llm-prompt-optimizer`)
- [x] T005 Author `music_maker_plugin/skills/guitar-bass-expression/references/pitch-bend-target-grammar.md` grounded in extracted arXiv PDFs (`arxiv_2308_12307`, `arxiv_2401_13498`, `arxiv_1910_09021`, `arxiv_0906_0127`) and verified scale-degree bending theory.
- [x] T006 Update `guitar-bass-expression/SKILL.md`, `instrumental-soloing-improvisation/SKILL.md`, `music-theory-harmony/SKILL.md`, and `soundfont-music/references/toolkit.md` with target-pitch locking protocol.
- [x] T007 Update `music_maker_plugin/rules/AGENTS.md`, `soundfont-music/SKILL.md`, `producer-mindset-workflow/SKILL.md`, `genre-style-encyclopedia/{SKILL.md,references/style-maps.md}`, `orchestration-arrangement/SKILL.md`, and `mixing-timbre-mastering/SKILL.md` to enforce `midi_map.md` + `readme.md` precedence without generic textbook overrides.

## Phase 4: Verification, Review & Logging
- [x] T008 Run `unittest`, `agy plugin validate --strict music_maker_plugin`, and `code-reviewer` subagent review; clean up any scratch/temp artifacts if requested; update `GEMINI.md`.
