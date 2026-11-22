# Feature Specification: Ultra-Advanced Harmony, Counterpoint, Post-Tonal & Orchestral/Big-Band Arranging

**Feature Branch**: `002-advanced-harmony-and-orchestration`
**Created**: 2026-11-22
**Status**: Pending User Approval
**Input**: Distill the 107 extracted plain-text music theory, counterpoint, jazz voicing, post-tonal/spectral, orchestral, and big-band arranging documents in `tai lieu/` into `music_maker_plugin` using `llm-prompt-optimizer` (RSCIT, 5-step CoT, Few-Shot, Grounding, Prompt Compression), plus upgrade the `soundfont-music` Python toolkit (`engine/harmony.py`, `engine/voicing.py`, `engine/review.py`) via TDD.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ultra-Advanced Harmony & Reharmonization (`music-theory-harmony` + Python `harmony.py`) (Priority: P1)
As an AI composer/theorist, I need grounded mastery of Neo-Riemannian transformations (`P/L/R/S/N/H`), Tonnetz geometry, Negative Harmony (axis involution), Bartók/Lendvai symmetrical Axis System, Upper-Structure Triads, George Russell's Lydian Chromatic Concept, Barry Harris 6th-Diminished families, Coltrane cycles, and Gospel/Neo-Soul passing chords—backed by executable Python helpers (`plr_transform`, `negative_harmony_pcs`, `coltrane_cycle`, `barry_harris_scale`, `upper_structure_triad`, expanded `QUALITIES`)—so compositions exhibit sophisticated harmonic color rather than basic diatonic/pop loops.

**Independent Test**:
- Run `unittest` on `tools/tests/test_toolkit_advanced_harmony.py` verifying Neo-Riemannian `P/L/R/S/N/H`, Negative Harmony mapping, Coltrane cycles, Barry Harris 6th-dim scales, and polychord/altered chord parsing.
- Verify `music-theory-harmony/SKILL.md` and new `references/harmony/` + `assets/advanced-harmony-catalog.yaml` pass `pyyaml` parsing and `agy plugin validate --strict`.

### User Story 2 - New Specialist Skill: `counterpoint-fugue-and-post-tonal` (Priority: P1)
As an AI composer writing polyphonic, contrapuntal, cinematic modernist, or avant-garde instrumental passages, I need a dedicated skill distilling strict/free species counterpoint, double/invertible counterpoint (8ve/10th/12th), canon, fugue exposition/answer/countersubject/episodes/stretto (Prout & Belkin), pitch-class set theory & 12-tone operations/combinatoriality (OMTv1, Hook, Straus, Absil), and spectral/post-spectral overtone pitch modeling (MTO Donaldson).

**Independent Test**:
- Verify `music_maker_plugin/skills/counterpoint-fugue-and-post-tonal/SKILL.md` and its `references/` + `assets/` pass `agy plugin validate --strict music_maker_plugin` and `llm-prompt-optimizer` audit checklist (RSCIT, CoT, Few-Shot, Grounding).

### User Story 3 - Master Orchestral, Timbre-Grouping & Big-Band Arranging (`orchestration-arrangement` + Python `voicing.py`/`review.py`) (Priority: P1)
As an AI orchestrator/arranger, I need master-level orchestral craft (Piston, Berlioz/Strauss, Cecil Forsyth, Widor, Prout *The Orchestra Vol. 1–2*, Rimsky-Korsakov Ch. VI+ tutti/groups), psychoacoustic timbre grouping (ACTOR / McAdams Concurrent, Sequential, Segmental grouping & vocality/multiphonics; Belkin *Artistic Orchestration*; Tim Davies Hollywood scoring), and Big-Band/Jazz ensemble arranging (Frans Absil, Evan Rogers, Dan Haerle, Tim Davies: 4-Way Close, Drop-2, Drop-3, Drop-2+4, So What / Quartal voicings, Thickened-Line Sax Soli, Open Brass Spreads)—backed by Python `voicing.py` (`drop2`, `drop3`, `drop24`, `so_what_voicing`, `quartal_stack`, `upper_structure_voicing`) and `review.py` masking/clumping diagnostics.

**Independent Test**:
- Run `unittest` verifying `drop2`, `drop3`, `drop24`, `so_what_voicing`, `quartal_stack`, `upper_structure_voicing`, and `review_song()` same-family register clumping / masking warnings.
- Run `agy plugin validate --strict music_maker_plugin`.

### User Story 4 - Agent Sync & Optional 5th Specialist Agent + Ecosystem Integration (Priority: P2)
As a plugin user, I want `music_maker_plugin` agents (`composer-theorist`, `groove-arranger`, `executive-producer`, `soundfont-mix-engineer`, plus optional 5th agent `orchestral-bigband-arranger`), `rules/AGENTS.md`, `soundfont-music/SKILL.md`, `references/toolkit.md`, `plugin.json` (`1.5.0`), `THIRD_PARTY.md`, and `README.md` seamlessly wired to the upgraded skills and toolkit, while preserving silent `midi_map.md` precedence and zero exposure of `tai lieu/` paths.

**Independent Test**:
- `agy plugin validate --strict music_maker_plugin` passes with 0 errors and 0 warnings.
- `Select-String` confirms zero leaked `tai lieu/` references inside `music_maker_plugin/`.

### Edge Cases
- **Backwards compatibility**: Existing `harmony.parse()`, `voicing.voice_lead()`, and `review.review_song()` signatures and return structures MUST remain 100% backwards-compatible.
- **Genre framing**: Strict counterpoint (no parallel 5ths/8ves) and Neo-Riemannian / post-tonal techniques MUST be framed by genre/style context so they never override pop/house/ballad `midi_map.md` idioms.
- **OCR artifacts in source texts**: Extracted texts from historical scans (Berlioz/Strauss, Forsyth, Widor, Prout, Piston) contain occasional OCR typos; distilled references MUST verify musical pitches, ranges, and formulas rigorously rather than copying OCR noise.

## Functional Requirements
- **FR-001**: All new/updated skills and agents MUST follow `llm-prompt-optimizer` (RSCIT, 5-step CoT, Few-Shot transformations, positive instructions, grounding rules, prompt compression).
- **FR-002**: Upgrade `music-theory-harmony` with 3–4 focused reference files + 1 YAML catalog covering Neo-Riemannian/Tonnetz, Negative Harmony & Axis System, and Advanced Jazz/Lydian Chromatic/Barry Harris/Coltrane/Gospel harmony, updating `SKILL.md` and `references/00-navigation.md`.
- **FR-003**: Create new skill `music_maker_plugin/skills/counterpoint-fugue-and-post-tonal/` (`SKILL.md`, `references/`, `assets/`).
- **FR-004**: Upgrade `orchestration-arrangement` with 3 focused reference files covering Classical Master Orchestration (Piston/Berlioz-Strauss/Forsyth/Widor/Prout/Rimsky Ch.VI+), Timbre Grouping & Modern Scoring (ACTOR/McAdams/Belkin/Tim Davies), and Big-Band & Sectional Ensemble Voicings (Absil/Rogers/Haerle/Davies), updating `SKILL.md`.
- **FR-005**: Upgrade `soundfont-music/scripts/toolkit/engine/harmony.py` (extended chord qualities + polychords + `plr_transform`, `negative_harmony_pcs`, `coltrane_cycle`, `barry_harris_scale`, `upper_structure_triad`), `engine/voicing.py` (`drop2`, `drop3`, `drop24`, `so_what_voicing`, `quartal_stack`, `upper_structure_voicing`), and `engine/review.py` (timbral masking / register clumping check + harmonic richness summary) following strict TDD.
- **FR-006**: Update `music_maker_plugin/rules/AGENTS.md`, `agents/`, `soundfont-music/{SKILL.md,references/toolkit.md}`, `plugin.json` (`1.5.0`), `THIRD_PARTY.md`, and `README.md`.
- **FR-007**: Cite only verified public-domain/open-access authors and theories in `THIRD_PARTY.md` and skill references—never expose local `tai lieu/` file paths inside plugin files.

## Success Criteria
- **SC-001**: All unit tests in `tools/tests/` (existing 17 tests + new advanced harmony/voicing/review tests) pass 100%.
- **SC-002**: `pyyaml` validates all new YAML assets; `py_compile` passes on all edited Python files.
- **SC-003**: `agy plugin validate --strict music_maker_plugin` passes with 0 errors and 0 warnings.
- **SC-004**: Zero `tai lieu/` path leaks inside `music_maker_plugin/`.
