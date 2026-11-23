# Tasks: `melody-harmonization` Skill & Ecosystem Integration

## Phase 1: Assets & Source-Exact Tables
- [x] T001 Create `music_maker_plugin/skills/melody-harmonization/assets/harmonic-tendencies-and-approaches.yaml` faithfully encoding Ted Greene `24`, `25`, `26`
- [x] T002 Create `music_maker_plugin/skills/melody-harmonization/assets/melody-harmonization-checklists.md`

## Phase 2: Modular Reference Guides (100% Source-Grounded)
- [x] T003 Create `references/melodic-skeleton-and-harmonic-rhythm.md` (`00`, `01`, `02`, `03`, `05`, `18`, `19`)
- [x] T004 Create `references/phrase-architecture-and-scoring.md` (`04`, `12`, `16`, `17`, `34`)
- [x] T005 Create `references/ted-greene-substitution-and-approach-toolkit.md` (`07`, `09`, `10`, `11`, `20`–`23`, `26`, `28`, `29`)
- [x] T006 Create `references/voice-leading-embellishment-and-modulation.md` (`13`–`15`, `30`–`33`)
- [x] T007 Create `references/00-navigation.md`

## Phase 3: Prompt-Optimized Skill Entrypoint & Ecosystem Wiring
- [x] T008 Create `SKILL.md` (`llm-prompt-optimizer`: RSCIT + 5-step CoT + Few-Shot + Anti-Hallucination + Template)
- [x] T009 Wire into `rules/AGENTS.md`, `skills/soundfont-music/SKILL.md`, `skills/music-theory-harmony/references/00-navigation.md`, `agents/composer-theorist.md`, `agents/executive-producer.md`
- [x] T010 Update `music_maker_plugin/THIRD_PARTY.md` and bump `music_maker_plugin/plugin.json` to `1.7.0`

## Phase 4: Verification, Cleanup & Logging
- [x] T011 Verify YAML syntax + run `agy plugin validate --strict music_maker_plugin`
- [x] T012 Run `code-reviewer` subagent across all new/edited plugin files & source cross-check
- [x] T013 Delete all contents inside `tai lieu/` and verify directory is empty
- [x] T014 Log completed work in `GEMINI.md`
