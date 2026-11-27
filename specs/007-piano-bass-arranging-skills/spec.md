# Feature Specification: Piano Comping & Bass Arranging Skills (`piano-comping-and-voicing`, `bass-arranging-and-line-craft`)

**Feature Branch**: `007-piano-bass-arranging-skills`  
**Created**: 2026-11-27  
**Status**: Completed & Verified  
**Input**: User request: Activate `llm-prompt-optimizer` to accurately distill 100% of the newly collected Piano, Bass, and Rhythm-Section Arranging documents in `tai lieu/` (33 extracted `.txt` files) into dedicated/upgraded skills with zero fabrication.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-Genre Piano Comping, Voicings & Hand-Independence Skill (Priority: P1)
As a music producer using `music_maker_plugin`, I want a dedicated **`piano-comping-and-voicing`** skill covering Rootless Type A/B & shell voicings, Dan Haerle & Pease-Pullig voicings, lazy `3–7`/`9–13` voice leading, Wynton Kelly comping & anticipation, Pop/Rock LH-RH role separation (`1-5-8` bass vs. chord/melody), and Afro-Cuban montuno/clave 2-hand independence so piano arrangements stop sounding erratic or muddy and lock cleanly with bass, guitar, and vocals.

**Independent Test**:
- Verify `music_maker_plugin/skills/piano-comping-and-voicing/SKILL.md` and its 4 reference files trace every voicing formula, spacing rule, rhythmic comping rule, and case study directly to the extracted `.txt` files in `tai lieu/piano/` and `tai lieu/rhythm-section-arranging/` with zero fabricated claims.

### User Story 2 - Advanced Bass Line Construction, Groove & Kick-Bass Lock Skill (Priority: P1)
As a music producer, I want a dedicated **`bass-arranging-and-line-craft`** skill covering linear walking bass construction (scales, arpeggios, chromatics, Dyas's Cycle Patterns, 4-step walking construction), West African rhythmic retentions (tresillo, habanera, cinquillo, 2-3/3-2 clave, Cuban tumbao, samba, reggae), Funk/Motown/R&B/Pop bass craft (ghost notes, chucking, space, note-length control), and Kick-Bass lock & low-end frequency/register clarity so basslines drive both harmony and groove cohesively.

**Independent Test**:
- Verify `music_maker_plugin/skills/bass-arranging-and-line-craft/SKILL.md` and its 3 reference files trace every cycle pattern, rhythmic clave/tumbao rule, frequency band, and bass technique directly to the extracted `.txt` files in `tai lieu/bass/` and `tai lieu/rhythm-section-arranging/` with zero fabrication.

### User Story 3 - Existing Skill Upgrades, Ecosystem Wiring & Strict Validation (Priority: P1)
As a maintainer, I want `orchestration-arrangement` (`piano-keyboards.md`, `SKILL.md`) and `groove-rhythm-drums` (`bass.md`, `SKILL.md`) updated with clean handoffs to the two new skills, and all cross-links wired across `soundfont-music/SKILL.md`, `rules/AGENTS.md`, `agents/`, `THIRD_PARTY.md`, `plugin.json` (`1.10.0`), and `README.md`, verified via source cross-audit, `agy plugin validate --strict`, and `code-reviewer`.

**Independent Test**:
- Run `agy plugin validate --strict music_maker_plugin` (expect 0 errors/warnings, `skills 14`), verify zero `tai lieu/` path leaks inside `music_maker_plugin/`, and pass `code-reviewer` with 0 CRITICAL/HIGH issues.

### Edge Cases
- **Scanned/Un-extracted PDF (`Bill-Dobbins-Jazz-Arranging-and-Composing.pdf`)**: Contains 0 text characters (`pages=148, chars=0`). Must NOT be cited or guessed from; only the 33 text-extracted `.txt` files in `tai lieu/` are used as ground-truth sources.
- **Music-glyph-heavy `.txt` files (`Autumn-Leaves`, `Ron-Drotos`, `Stevens`)**: Extract only explicitly readable prose lessons, labels, and chord symbols; never hallucinate unprinted staff notes.
- **Skill Boundaries**: Preserve `pop-ballad-arranging` for Pop Ballad specifics (`C3–C6` + ballad CC64 + descending slash bass), `guitar-bass-expression` for fretted pitch-bends/MPE/tunings, and `piano-and-chamber.md` for SoundFont Steinway/Osiris presets & solo classical rubato.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: Create `music_maker_plugin/skills/piano-comping-and-voicing/SKILL.md` + `references/00-navigation.md` + 4 thematic reference files engineered via `llm-prompt-optimizer` (RSCIT, Anti-Hallucination Guardrail, Positive Coordination Rules, 6-step CoT, 2 Few-Shot examples matching Output Format, Token-compressed Navigation Map, Output Format at end).
- **FR-002**: Create `music_maker_plugin/skills/bass-arranging-and-line-craft/SKILL.md` + `references/00-navigation.md` + 3 thematic reference files engineered via `llm-prompt-optimizer` with the same structural rigor.
- **FR-003**: Accurately distill all 33 extracted `.txt` documents in `tai lieu/{piano,bass,rhythm-section-arranging}/` into those reference files with exact source citations and zero fabrication, while keeping `tai lieu/` intact on disk for the user.
- **FR-004**: Upgrade cross-references in `orchestration-arrangement/references/instrument-idiom/piano-keyboards.md`, `orchestration-arrangement/SKILL.md`, `groove-rhythm-drums/references/bass.md`, `groove-rhythm-drums/SKILL.md`, `soundfont-music/SKILL.md`, `rules/AGENTS.md`, `agents/{executive-producer,composer-theorist,groove-arranger,orchestral-bigband-arranger,soundfont-mix-engineer}.md`, `THIRD_PARTY.md`, `plugin.json` (`1.10.0`), and `README.md`.
- **FR-005**: Enforce Dual Top-Priority Parallel Study (`References ‖ midi_map.md`) and Zero-Code User Persona in both new skills, with zero references to `tai lieu/` inside `music_maker_plugin/`.

### Success Criteria
- **SC-001**: 100% of the 33 extracted `.txt` source documents in `tai lieu/` are accurately represented in the two new skills with 0 invented rules, numbers, or citations.
- **SC-002**: `agy plugin validate --strict music_maker_plugin` passes with 0 errors and 0 warnings (`skills 14 · agents 6 · rules 1`).
- **SC-003**: `code-reviewer` reports 0 CRITICAL or HIGH issues; work is logged in `GEMINI.md`.

## Assumptions
- `tai lieu/` remains preserved on disk untouched as the user's local study library.
- No Python `engine/` source files require modification; this upgrade operates purely on skills, references, agents, rules, and plugin metadata.
