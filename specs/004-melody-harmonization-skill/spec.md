# Feature Specification: Melody Harmonization & Reharmonization Skill (`melody-harmonization`)

**Feature Branch**: `004-melody-harmonization-skill`  
**Created**: 2026-11-23  
**Status**: Approved (Implementing)  
**Input**: Synthesize all 32 verified plain-text source documents in `tai lieu/txt/` (Trevor de Clercq, Temperley & de Clercq, AccoMontage2, AutoHarmonizer, Ted Greene, and Open Music Theory v2) into a dedicated, hallucination-free, `llm-prompt-optimizer`-engineered skill (`melody-harmonization`) that activates both when harmonizing a user-supplied melody/vocal/MIDI and whenever designing or upgrading chord progressions for any track. Remove all contents of `tai lieu/` after complete verification.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Harmonizing a User-Supplied Melody into a Musical Progression & Beat (Priority: P1)
As a songwriter or producer who provides a melody (MIDI, notes, or vocal topline), I want the AI to analyze melodic skeleton notes, beat strengths, key/mode, and harmonic rhythm (~2s pacing) before choosing chords—rather than naively forcing a triad under every note or defaulting to generic `I–V–vi–IV` loops.

**Independent Test**:
- Verify `skills/melody-harmonization/SKILL.md` and `references/melodic-skeleton-and-harmonic-rhythm.md` define Beat Strength (`0–3`), Melodic Skeleton extraction, ~2s Harmonic Rhythm budgeting, Melodic-Harmonic Divorce, and Harmonic-Bass Divorce strictly matching `00`, `01`, `02`, `03`, `05`.

### User Story 2 - Universal Progression Design, Reharmonization & 100% Source-Faithful Lookup (Priority: P1)
As a producer building or upgrading chord progressions for any song (even without an input melody), I want the AI to use `melody-harmonization` anytime to apply Cadence-First phrase planning, 3-level harmonization scoring, Ted Greene's 9 harmonic improvement concepts, pre-destination chord movement tables, scale-chord mappings, and OMT2 Jazz/Pop voice leading—with 100% fidelity to the source documents and zero fabrication.

**Independent Test**:
- Cross-check every chord table in `assets/harmonic-tendencies-and-approaches.yaml` and every rule in `references/*.md` directly against `tai lieu/txt/*` (`00`–`34`) before cleanup, verifying 0 invented rules, 0 missing edge warnings, and valid YAML syntax.

### User Story 3 - `llm-prompt-optimizer` Discipline, Plugin Integration & `tai lieu/` Cleanup (Priority: P1)
As the maintainer of `music_maker_plugin`, I want the new skill wired across `rules/AGENTS.md`, `soundfont-music/SKILL.md`, `music-theory-harmony/references/00-navigation.md`, `agents/*.md`, `THIRD_PARTY.md`, and `plugin.json` (`1.7.0`), validated via `agy plugin validate --strict music_maker_plugin` and `code-reviewer`, and all temporary files inside `tai lieu/` deleted once verified.

**Independent Test**:
- Run strict plugin validation (`agy plugin validate --strict music_maker_plugin`), YAML parse verification, and `code-reviewer` audit, then confirm `tai lieu/` is empty.

## Functional Requirements
- **FR-001**: Create `music_maker_plugin/skills/melody-harmonization/SKILL.md` using `llm-prompt-optimizer` (RSCIT, 5-step CoT, 2 Few-Shot examples grounded in sources, anti-hallucination constraints, compressed format, output template at end), triggered universally for melody harmonization, reharmonization, and chord progression design.
- **FR-002**: Distill 100% of the 32 extracted documents (`tai lieu/txt/00_*` through `34_*`) accurately with zero fabrication across `references/00-navigation.md`, 4 `references/*.md` files, and 2 `assets/*` files (`harmonic-tendencies-and-approaches.yaml` + `melody-harmonization-checklists.md`), cross-referencing `music-theory-harmony` where Pop schemas already exist instead of duplicating.
- **FR-003**: Do NOT add unnecessary Python analysis modules to `soundfont-music/scripts/toolkit/engine/`.
- **FR-004**: Wire `melody-harmonization` into `rules/AGENTS.md`, `soundfont-music/SKILL.md`, `music-theory-harmony/references/00-navigation.md`, `agents/composer-theorist.md`, `agents/executive-producer.md`, `THIRD_PARTY.md`, and `plugin.json` (`1.7.0`).
- **FR-005**: Validate strictly (`agy plugin validate --strict music_maker_plugin`, `pyyaml`, `code-reviewer`), delete all contents inside `tai lieu/` after verification, and log completion in `GEMINI.md`.

## Success Criteria
- **SC-001**: 100% of chord tables, formulas, and concepts in `skills/melody-harmonization/` trace verbatim/accurately to `tai lieu/txt/*` with zero fabricated data.
- **SC-002**: `agy plugin validate --strict music_maker_plugin` and `pyyaml` validation pass with 0 errors/warnings.
- **SC-003**: `code-reviewer` passes with 0 CRITICAL or HIGH issues; `tai lieu/` is emptied after final verification.
