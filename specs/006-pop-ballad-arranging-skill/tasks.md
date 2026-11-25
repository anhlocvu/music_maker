# Tasks: `pop-ballad-arranging` Skill & Ecosystem Integration

## Phase 1: Specify & Source Audit
- [x] T001 Create `specs/006-pop-ballad-arranging-skill/{spec.md,plan.md,tasks.md,checklists/requirements.md}` and update `.specify/feature.json`
- [x] T002 Audit and distill exact facts from all 26 `.txt` source documents in `tai lieu/`

## Phase 2: Modular Reference Guides (100% Source-Grounded)
- [x] T003 Create `references/form-tension-and-ballad-case-studies.md`
- [x] T004 Create `references/bass-pop-ballad-craft.md`
- [x] T005 Create `references/piano-pop-ballad-voicings-and-pedal.md`
- [x] T006 Create `references/guitar-pop-ballad-patterns-and-interplay.md`
- [x] T007 Create `references/strings-pop-ballad-orchestration.md`
- [x] T008 Create `references/drums-and-percussion-pop-ballad.md`
- [x] T009 Create `references/tutti-kicks-setups-and-transitions.md`
- [x] T010 Create `references/00-navigation.md`

## Phase 3: Prompt-Optimized Skill Entrypoint & Ecosystem Wiring
- [x] T011 Create `SKILL.md` (`llm-prompt-optimizer`: RSCIT + 6-step CoT + Few-Shot + Anti-Hallucination + Template)
- [x] T012 Cross-link into `genre-style-encyclopedia/references/playbooks/pop-and-ballad.md`, `soundfont-music/SKILL.md`, `orchestration-arrangement/SKILL.md`, `groove-rhythm-drums/SKILL.md`, `rules/AGENTS.md`
- [x] T013 Update `agents/*.md`, `THIRD_PARTY.md`, `plugin.json` (`1.9.0`), and `README.md`

## Phase 4: Verification & Logging
- [x] T014 Perform 100% source-accuracy check across all new files against `tai lieu/*.txt` (resolved 2 HIGH, 5 MEDIUM, 4 LOW findings from `code-reviewer`)
- [x] T015 Run `agy plugin validate --strict music_maker_plugin` and `code-reviewer` check
- [x] T016 Log completed work in `GEMINI.md`
