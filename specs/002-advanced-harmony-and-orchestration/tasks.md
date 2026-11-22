# Tasks: Ultra-Advanced Harmony, Counterpoint, Post-Tonal & Orchestral/Big-Band Arranging

## Phase 1: Tests First (TDD Red)
- [x] T001 Create `tools/tests/test_toolkit_advanced.py` covering: (a) extended `QUALITIES` (`7alt`, `maj9#11`, `13#11`, `sowhat`, polychords `D|C7`); (b) `plr_transform()` (`P/L/R/S/N/H`), `negative_harmony_pcs()`, `coltrane_cycle()`, `barry_harris_scale()`, `upper_structure_triad()`; (c) `drop2()`, `drop3()`, `drop24()`, `so_what_voicing()`, `quartal_stack()`, `upper_structure_voicing()`; (d) `review_song()` same-family register clumping diagnostic and backwards compatibility.

## Phase 2: Python Toolkit Implementation (TDD Green)
- [x] T002 Upgrade `music_maker_plugin/skills/soundfont-music/scripts/toolkit/engine/harmony.py` with extended chord qualities, polychord parsing, Neo-Riemannian `plr_transform()`, `negative_harmony_pcs()`, `coltrane_cycle()`, `barry_harris_scale()`, and `upper_structure_triad()`.
- [x] T003 Upgrade `music_maker_plugin/skills/soundfont-music/scripts/toolkit/engine/voicing.py` with `drop2()`, `drop3()`, `drop24()`, `so_what_voicing()`, `quartal_stack()`, and `upper_structure_voicing()`.
- [x] T004 Upgrade `music_maker_plugin/skills/soundfont-music/scripts/toolkit/engine/review.py` with same-family register clumping / timbral masking diagnostic while keeping all existing diagnostics intact.

## Phase 3: Distill `tai lieu/` into Skills & Assets (`llm-prompt-optimizer`)
- [x] T005 Upgrade `music-theory-harmony`: author `references/harmony/{neo-riemannian-and-tonnetz,negative-harmony-and-polarity,advanced-jazz-gospel-voicings}.md` and `assets/advanced-harmony-catalog.yaml`; update `SKILL.md` and `references/00-navigation.md`.
- [x] T006 Create new skill `counterpoint-fugue-and-post-tonal`: author `SKILL.md`, `references/{00-navigation,strict-and-invertible-counterpoint,fugue-and-canon-architecture,post-tonal-set-and-serial-theory,spectral-and-schillinger-techniques}.md`, and `assets/post-tonal-and-fugue-catalog.yaml`.
- [x] T007 Upgrade `orchestration-arrangement`: author `references/orchestration/{classical-masters-orchestration,timbre-grouping-and-modern-scoring,big-band-and-sectional-voicings}.md` and update `SKILL.md`.

## Phase 4: Ecosystem Sync, Verification, Code Review & Cleanup
- [x] T008 Update `soundfont-music/{SKILL.md,references/toolkit.md}`, `music_maker_plugin/rules/AGENTS.md`, `agents/` (including new `orchestral-bigband-arranger.md`), `plugin.json` (`1.5.0`), `THIRD_PARTY.md`, and `README.md`.
- [x] T009 Run `unittest`, `py_compile`, `pyyaml` check, `agy plugin validate --strict music_maker_plugin`, `tai lieu` leak check, and `code-reviewer` subagent review; fix all findings; log completed work in `GEMINI.md` and clean `tai lieu/` as requested.
