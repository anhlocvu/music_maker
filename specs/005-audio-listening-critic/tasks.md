# Tasks: Professional Audio Listening Critic Agent (`audio-listening-critic`) & Multi-Duration Segment QA

**Input**: Design documents from `specs/005-audio-listening-critic/`  
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md`

## Phase 1: TDD Red Phase (US2)

- [x] T001 [US2] Write failing TDD unit tests (`slice_wav`, `build_auto_profile_windows`, `slice_wav_segments`, and `slice_audio.py` CLI) in `tools/tests/test_toolkit_audio_slice.py`

## Phase 2: Variable-Duration WAV Segment Slicer (US2)

- [x] T002 [US2] Implement `slice_wav`, `build_auto_profile_windows`, and `slice_wav_segments` in `music_maker_plugin/skills/soundfont-music/scripts/toolkit/engine/analysis.py`
- [x] T003 [US2] Create CLI `music_maker_plugin/skills/soundfont-music/scripts/toolkit/slice_audio.py` and verify `tools/tests/test_toolkit_audio_slice.py` passes

## Phase 3: Prompt-Optimized Audio Listening Critic Agent (US1)

- [x] T004 [US1] Create `music_maker_plugin/agents/audio-listening-critic.md` engineered with `llm-prompt-optimizer` (RSCIT, 6-step CoT, Macro/Meso/Micro variable-duration listening + stem cross-check, 5-axis rubric, 2 Few-Shot examples matching Output Format, anti-hallucination guardrails, Output Template at end)

## Phase 4: Ecosystem Synchronization (US3)

- [x] T005 [P] [US3] Update `music_maker_plugin/rules/AGENTS.md`, `music_maker_plugin/agents/README.md`, `music_maker_plugin/agents/soundfont-mix-engineer.md`, and `music_maker_plugin/agents/executive-producer.md`
- [x] T006 [P] [US3] Update `music_maker_plugin/skills/soundfont-music/SKILL.md`, `music_maker_plugin/skills/soundfont-music/references/toolkit.md`, `music_maker_plugin/skills/mixing-timbre-mastering/SKILL.md`, `music_maker_plugin/skills/mixing-timbre-mastering/references/dsp-and-audio-verification.md`, `music_maker_plugin/skills/producer-mindset-workflow/SKILL.md`, and `music_maker_plugin/skills/groove-rhythm-drums/SKILL.md`
- [x] T007 [US3] Bump `music_maker_plugin/plugin.json` to `1.8.0` and update `README.md`

## Phase 5: Verification, End-to-End Listening Check & Logging

- [x] T008 Run full `unittest` suite in `tools/tests/` and `agy plugin validate --strict music_maker_plugin`
- [x] T009 Run `code-reviewer` subagent across all new/modified files and resolve any CRITICAL/HIGH/MEDIUM issues
- [x] T010 Run end-to-end multi-duration listening verification on `kpop_ballad_c_65bpm.wav` (cleaning up temporary clips afterward) and log completed work in `GEMINI.md`
