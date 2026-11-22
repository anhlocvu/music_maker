# Feature Specification: Target-Aware Pitch Bending & Inline MIDI-Map Style Adoption

**Feature Branch**: `001-pitch-bend-and-midi-map-style`
**Created**: 2026-11-22
**Status**: Approved by User
**Input**: Fix unguided/out-of-key AI pitch bending using extracted technical/theory references, refactor `midi_map.md` generation to embed pitch bends inline with notes and place project `readme.md` first without auto-classifying genres, and remove skill/rule precedence conflicts preventing `midi_map.md` style adoption (optimized with `llm-prompt-optimizer`).

## User Scenarios & Testing

### User Story 1 - Inline Pitch Bend & Prominent README in `midi_map.md` (Priority: P1)
As a producer, I want `midi_map.md` to attach each pitch-bend gesture directly onto its sounding note (like duration and velocity) instead of dumping thousands of detached pitchwheel events, and to show each project's `readme.md` immediately under the project header without auto-guessing styles.

**Independent Test**: Run `tools/generate_midi_map.py` on `music_maker_plugin/midi/` and verify:
- Zero `All Pitch Bend Events` blocks exist.
- Bent notes in `guitar lead-Overdrive Guitar.mid`, `guitar_lead-Les Sus_0_30.mid`, and `bass-MM JZ.F_0_33.mid` show inline `bend=...` with semitones and target note names.
- `### Project README` appears before `### File:` inside each project section.
- No line exceeds `read_file`'s 46,080-byte limit.

### User Story 2 - Target-Aware Pitch Bending in Skills & Python Toolkit (Priority: P1)
As an AI composer/arranger, I need music-theory target-note bending rules (`guitar-bass-expression` + linked skills) and target-aware Python APIs (`Track.bend(..., target=...)`, scale/chord-aware `expressive_bends()`, and `review_song()` bent-pitch audit) so bends always aim at valid chord/scale tones instead of random out-of-key offsets.

**Independent Test**: Run `unittest` on `tools/tests/test_toolkit_bends.py` verifying `target="E5"`, scale-aware `expressive_bends()`, and `out_of_scale_bends` reporting in `review_song()`.

### User Story 3 - Unblocked `midi_map.md` Style Precedence Across All Skills (Priority: P2)
As a user testing a ballad or other style present in `music_maker_plugin/midi/`, I want all skills (`genre-style-encyclopedia`, `producer-mindset-workflow`, `orchestration-arrangement`, `mixing-timbre-mastering`, `soundfont-music`) to prioritize `midi_map.md` + `readme.md` over generic textbook defaults.

**Independent Test**: Validate `music_maker_plugin` with `agy plugin validate --strict` and inspect all `SKILL.md` / reference updates for consistent RSCIT + positive-instruction precedence.

## Functional Requirements
- **FR-001**: Extract downloaded pitch-bending PDFs into plain-text Markdown in `tai lieu/pitch_bending/` and ground new reference docs strictly in extracted content and verified music theory.
- **FR-002**: `engine/midi_io.py` and `analyze_midi.py` MUST attach pitch-bend summaries inline on affected notes (showing direction, semitones, gesture type, and target pitch) and MUST NOT emit separate `All Pitch Bend Events` blocks.
- **FR-003**: `analyze_midi.py` MUST render `### Project README` immediately under each project heading and MUST NOT fabricate automatic style classifications overriding `readme.md`.
- **FR-004**: `Track.bend()` and `Track.bend_last()` in `engine/song.py` MUST support an optional `target` note parameter while keeping full backwards compatibility with `semis`.
- **FR-005**: `expression.expressive_bends()` MUST validate bend target pitches against the active `harmony`/`scale`/`key` (or inferred diatonic scale) and avoid out-of-scale bends.
- **FR-006**: `review.review_song()` MUST audit large bends (`>= 0.8 st`) against the active chord/scale and report `out_of_scale_bends`.
- **FR-007**: All updated skill files MUST follow `llm-prompt-optimizer` (RSCIT, CoT, Few-Shot, Grounding, positive instructions) and establish explicit `midi_map.md` precedence over generic genre defaults.

## Success Criteria
- **SC-001**: `python tools/generate_midi_map.py` completes with exit code 0, max line length < 46,080 bytes, and 0 `All Pitch Bend Events` sections.
- **SC-002**: All unit tests in `tools/tests/` pass after final edits (`100%` pass rate).
- **SC-003**: `agy plugin validate --strict music_maker_plugin` passes with 0 errors and 0 warnings.
