# Tasks: `007-piano-bass-arranging-skills`

**Input**: Design documents from `specs/007-piano-bass-arranging-skills/`
**Status**: Completed & Verified

## Phase 1: Source Distillation Audit (`tai lieu/` — 33 `.txt` files)
- [x] T001 Audit & extract exact rules/formulas from all Piano & Rhythm Section `.txt` sources (`JB-Dyas`, `Dan-Haerle`, `OMT`, `Pease-Pullig`, `UC-Piano-Comping`, `UMiami-AfroCuban`, `Migu`, `Ron-Drotos`, `Stevens`, `Autumn-Leaves`, `Frans-Absil`, `Contemporary-Jazz-Arranging`, `UOML`, `Hutchinson`, `Aebersold-RedBook`, `Ithaca`, `MidwestClinic-*`, `HandsUpForTrad`, `SOS-Arranging`)
- [x] T002 Audit & extract exact rules/formulas from all Bass & Rhythm Section `.txt` sources (`JB-Dyas-Linear-Bass`, `MrBlancq`, `Walking-Bass-Fundamentals`, `Rubim-de-Toledo`, `Berklee-Online-Bass-Handbook`, `OnlineBass-100-Funk`, `Aebersold-Latin-Bass-Tumbao`, `SOS-Bass-*`, `OMT-Pop-Rock-Texture`, `Ithaca`, `MidwestClinic-*`, `Frans-Absil`)

## Phase 2: Skill 1 — `piano-comping-and-voicing`
- [x] T003 Create `music_maker_plugin/skills/piano-comping-and-voicing/references/00-navigation.md`
- [x] T004 Create `references/voicing-systems-and-voice-leading.md`
- [x] T005 Create `references/jazz-comping-and-rhythm-section-interplay.md`
- [x] T006 Create `references/pop-rock-and-contemporary-accompaniment.md`
- [x] T007 Create `references/afro-cuban-latin-piano-and-independence.md`
- [x] T008 Create `music_maker_plugin/skills/piano-comping-and-voicing/SKILL.md` using `llm-prompt-optimizer`

## Phase 3: Skill 2 — `bass-arranging-and-line-craft`
- [x] T009 Create `music_maker_plugin/skills/bass-arranging-and-line-craft/references/00-navigation.md`
- [x] T010 Create `references/linear-and-walking-bass-construction.md`
- [x] T011 Create `references/african-rhythm-tumbao-funk-and-motown-grooves.md`
- [x] T012 Create `references/kick-bass-lock-and-low-end-clarity.md`
- [x] T013 Create `music_maker_plugin/skills/bass-arranging-and-line-craft/SKILL.md` using `llm-prompt-optimizer`

## Phase 4: Ecosystem Upgrades, Wiring & Verification (ECC)
- [x] T014 Update `orchestration-arrangement/{SKILL.md,references/instrument-idiom/piano-keyboards.md}` and `groove-rhythm-drums/{SKILL.md,references/bass.md}`
- [x] T015 Wire cross-links in `soundfont-music/SKILL.md`, `rules/AGENTS.md`, `agents/*.md`, `THIRD_PARTY.md`, `plugin.json` (`1.10.0`), and `README.md`
- [x] T016 Verify zero `tai lieu/` references inside `music_maker_plugin/`, run source-accuracy cross-audit, run `agy plugin validate --strict music_maker_plugin`, run `code-reviewer`, and log to `GEMINI.md`
