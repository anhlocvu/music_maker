# Implementation Plan: Professional Audio Listening Critic Agent (`audio-listening-critic`) & Multi-Duration Segment QA

**Branch**: `005-audio-listening-critic` | **Date**: 2026-11-25 | **Spec**: [spec.md](file:///C:/Users/LCBoy/Desktop/data/github%20repository/music_maker/specs/005-audio-listening-critic/spec.md)

## Summary

1. **Zero-Dependency Variable-Duration WAV Segment Slicer (`soundfont-music/scripts/toolkit/`)**:
   - Extend `engine/analysis.py` with `slice_wav(...)`, `build_auto_profile_windows(...)`, and `slice_wav_segments(...)` using Python stdlib `wave` so any PCM WAV (`int16`/`int32`, mono/stereo) can be sliced into sample-accurate time clips of arbitrary durations without adding third-party dependencies.
   - Add CLI `slice_audio.py` supporting `--start`/`--duration`/`--end`, `--windows "start:dur,..."`, `--auto-profile` (scales Macro/Meso/Micro windows to song duration and optional `--bpm` / `--loop-seam`), `--out` / `--out-dir`, and JSON output.
2. **Prompt-Optimized Specialist Agent (`music_maker_plugin/agents/audio-listening-critic.md`)**:
   - Built strictly with `llm-prompt-optimizer`:
     - **RSCIT** structure (`Role`, `Situation`, `Constraints`, `Instructions`, `Template` at the end).
     - **6-Step Chain-of-Thought**: Quantitative Intake → Macro Full-Mix Listen → Tailored Multi-Duration Audit Window Planning → Meso (15–30s) & Micro (3–10s) Zoomed Listening + `multi_track/` Stem Cross-Check → 5-Axis Professional Ear Scorecard (`CRITICAL`/`HIGH`/`MEDIUM`/`LOW`) → `PASS` / `REVISE` Verdict with Engineering Handoff + Zero-Code Producer Summary.
     - **2 Few-Shot Examples** illustrating `REVISE` (catching chorus low-mid mud, buried snare, synthetic lead, and a 6s drift bend) and `PASS` (tight dynamic ballad/loop verification).
     - **Anti-Hallucination & Grounding Guardrail**: Never invent unheard instruments, timestamps, or ear claims; mark uncertain segments and re-slice a tighter duration window or stem.
     - **Zero-Code User Persona**: Internal engineering handoffs use exact toolkit/track terminology, while the Producer Summary speaks purely as a mastering/studio producer.
3. **Ecosystem Synchronization & Validation (ECC)**:
   - Update `rules/AGENTS.md`, `agents/README.md`, `agents/soundfont-mix-engineer.md`, `agents/executive-producer.md`, `skills/soundfont-music/SKILL.md`, `skills/soundfont-music/references/toolkit.md`, `skills/mixing-timbre-mastering/SKILL.md`, `skills/mixing-timbre-mastering/references/dsp-and-audio-verification.md`, `plugin.json` (`1.8.0`), and `README.md`.
   - TDD unit tests in `tools/tests/test_toolkit_audio_slice.py`, full `unittest` suite, `agy plugin validate --strict music_maker_plugin`, `code-reviewer` subagent review, live multi-duration test on `kpop_ballad_c_65bpm.wav` (with temporary audit clips cleaned up), and `GEMINI.md` logging.

## Technical Context

- **Language / Runtime**: Python 3.10+ stdlib (`wave`, `argparse`, `json`, `pathlib`, `shutil`) + existing `numpy`/`scipy`/`mido` toolkit stack; Markdown agent/skill definitions.
- **Target Scope**: `music_maker_plugin/` (agents, rules, skills, `plugin.json`), `tools/tests/`, root `README.md`, `GEMINI.md`.
- **Constraints**:
  - English inside `music_maker_plugin/` (matching all existing agents and skills); Vietnamese for user conversation and `GEMINI.md`.
  - Preserve Zero-Code User Persona in user-facing summaries and strict `midi_map.md` silence.
  - No leftover temporary `.wav` audit clips in the workspace root after validation.

## Constitution Check

- Minimal, self-contained library functions in `engine/analysis.py` exposed via CLI (`slice_audio.py`) with JSON output.
- TDD enforced: write failing tests in `tools/tests/test_toolkit_audio_slice.py` before implementing `slice_wav` / `slice_wav_segments` / `slice_audio.py`.
- Strict validation gates (`unittest`, `agy plugin validate --strict`, `code-reviewer`) required before completion.
