# Tasks: Dual Top-Priority Knowledge, Zero-Code Producer Persona & Proactive Transitions/Fills

## Phase 1: SpecKit Setup
- [x] T001 Create `specs/003-dual-knowledge-and-producer-persona/{spec.md,plan.md,tasks.md,checklists/requirements.md}` and update `.specify/feature.json`.

## Phase 2: Core Rules Optimization (`llm-prompt-optimizer`)
- [x] T002 Refactor `music_maker_plugin/rules/AGENTS.md` with RSCIT structure, Dual Top-Priority Parallel Knowledge (`Specialist Docs ‖ midi_map.md`), Zero-Code Producer Persona (+ Few-Shot replacements), and Proactive Transitions/Drum Fills while preserving pedal/strum, `multi_track/`, and `/project` structure rules.

## Phase 3: Skills & Agents Synchronization
- [x] T003 Update `music_maker_plugin/skills/soundfont-music/SKILL.md`, `producer-mindset-workflow/{SKILL.md,references/song-planner-protocol.md}`, `groove-rhythm-drums/SKILL.md`, and `orchestration-arrangement/SKILL.md`.
- [x] T004 Update remaining specialist skills (`music-theory-harmony`, `genre-style-encyclopedia`, `guitar-bass-expression`, `instrumental-soloing-improvisation`, `mixing-timbre-mastering`, `counterpoint-fugue-and-post-tonal`) to reflect Dual Top-Priority parallel study (`Specialist Docs ‖ midi_map.md`).
- [x] T005 Update all 5 agents in `music_maker_plugin/agents/` (`executive-producer.md`, `composer-theorist.md`, `groove-arranger.md`, `orchestral-bigband-arranger.md`, `soundfont-mix-engineer.md`) for parallel `Docs ‖ midi_map.md`, proactive transitions/fills, and zero-code user reporting.

## Phase 4: Manifest, Docs, Validation & Review
- [x] T006 Update `music_maker_plugin/plugin.json` (`1.6.0`) and `README.md`.
- [x] T007 Run `agy plugin validate --strict music_maker_plugin` and `code-reviewer` subagent review; fix any findings; log session to `GEMINI.md` and mark all tasks complete.
