# Implementation Plan: Target-Aware Pitch Bending & Inline MIDI-Map Style Adoption

**Branch**: `001-pitch-bend-and-midi-map-style` | **Date**: 2026-11-22 | **Spec**: [spec.md](file:///C:/Users/LCBoy/Desktop/data/github%20repository/music_maker/specs/001-pitch-bend-and-midi-map-style/spec.md)

## Summary
1. Ground target-note pitch bending in the 4 extracted arXiv papers (`tai lieu/pitch_bending/*.md`) plus verified scale-degree bending theory, contributing `references/pitch-bend-target-grammar.md` to `guitar-bass-expression` and linking it across `instrumental-soloing-improvisation` and `music-theory-harmony`.
2. Upgrade `soundfont-music` toolkit (`song.py`, `expression.py`, `review.py`, `midi_io.py`, `analyze_midi.py`) via TDD so:
   - `midi_map.md` embeds bend summaries inline per note, deduplicates CC64 intervals cleanly, removes separate `All Pitch Bend Events` dumps, and places `Project README` at the top of each project.
   - `Track.bend()`/`bend_last()` accept `target="E5"`, `expressive_bends()` enforces scale/chord-safe target pitches, and `review_song()` flags `out_of_scale_bends`.
3. Optimize skills with `llm-prompt-optimizer` to establish `midi_map.md` + `readme.md` precedence over `genre-style-encyclopedia` / `producer-mindset-workflow` / `orchestration-arrangement` / `mixing-timbre-mastering` generic defaults.

## Technical Context
- **Language/Version**: Python 3.11+ (`uv run`)
- **Primary Dependencies**: `numpy`, `scipy`, `mido` (toolkit); `pymupdf4llm` (already used to extract PDFs)
- **Testing**: `unittest` (`tools/tests/test_toolkit_*.py`) + `agy plugin validate --strict music_maker_plugin`
- **Constraints**: Maintain 100% backwards compatibility on `Track`/`Song`/`analyze_midi` APIs; keep `midi_map.md` lines well under 46,080 bytes; never leak `midi_map.md` or `tai lieu/` paths inside user-facing outputs or skill source citations.

## Project Structure
```text
specs/001-pitch-bend-and-midi-map-style/
├── spec.md
├── plan.md
└── tasks.md

music_maker_plugin/
├── rules/AGENTS.md
├── midi_map.md
└── skills/
    ├── guitar-bass-expression/
    │   ├── SKILL.md
    │   └── references/pitch-bend-target-grammar.md
    ├── soundfont-music/
    │   ├── SKILL.md
    │   ├── references/toolkit.md
    │   └── scripts/toolkit/{analyze_midi.py,engine/{midi_io,song,expression,review}.py}
    ├── instrumental-soloing-improvisation/SKILL.md
    ├── music-theory-harmony/SKILL.md
    ├── genre-style-encyclopedia/{SKILL.md,references/style-maps.md}
    ├── producer-mindset-workflow/SKILL.md
    ├── orchestration-arrangement/SKILL.md
    └── mixing-timbre-mastering/SKILL.md

tools/tests/
├── test_toolkit_bends.py
└── test_toolkit_specs.py
```
