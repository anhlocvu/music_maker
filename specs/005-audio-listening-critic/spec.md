# Feature Specification: Professional Audio Listening Critic Agent (`audio-listening-critic`) & Multi-Duration Segment QA

**Feature Branch**: `005-audio-listening-critic`  
**Created**: 2026-11-25  
**Status**: Approved (Implementing)  
**Input**: User description: "Create a professional Audio Listening Critic agent using `llm-prompt-optimizer` that directly listens to rendered `.wav` mixes and `multi_track/` stems across variable-duration segments (macro, meso, micro) to evaluate real-world musical quality instead of relying solely on Python numeric metrics."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Direct Multi-Duration Listening Critique of Rendered Mixes & Stems (Priority: P1)

As a music producer using `music_maker_plugin`, I want a dedicated specialist agent (`audio-listening-critic`) that listens directly to the rendered stereo mix WAV and—when zooming in for deep inspection—slices and listens to targeted segments of varying durations (e.g., 3–10s micro clips for bends/fills/clicks, 15–30s meso clips for transitions/choruses, and full/macro passes for form/arc), plus `multi_track/` stem cross-checks, so real musical flaws that numeric scripts miss are caught before delivery.

**Why this priority**: Quantitative metrics (LUFS, peak, spectral slope) cannot detect MIDI-sounding presets, muddy mid-range masking in a chorus, clumsy drum fills, smeared sustain pedal, or unnatural pitch-bend phrasing. Direct listening across tailored durations is the core capability requested.

**Independent Test**:
- Verify `music_maker_plugin/agents/audio-listening-critic.md` exists, follows `llm-prompt-optimizer` (RSCIT, step-by-step CoT, Few-Shot examples, anti-hallucination guardrails, explicit output template at the end), and instructs multi-scale variable-duration listening + stem cross-checking.
- Run the agent's workflow on `kpop_ballad_c_65bpm.wav` (macro + sliced meso/micro segments) and verify it produces timestamped, evidence-backed findings without fabricating unheard details.

---

### User Story 2 - Zero-Dependency Variable-Duration WAV Segment Slicer (`slice_audio.py`) (Priority: P1)

As the `audio-listening-critic` agent (or sound engineer), I need a fast, reliable CLI utility (`slice_audio.py`) and engine helper (`engine.analysis.slice_wav` / `slice_wav_segments`) that can extract exact arbitrary time windows (`--start` + `--duration`, `--windows`, or `--auto-profile`) from any WAV file into temporary audit clips so the agent can inspect sections at different durations cleanly.

**Why this priority**: Direct file reading loads an entire WAV at once. To inspect subtle articulation, transitions, or specific bars carefully across varying durations, the agent needs deterministic, sample-accurate segment slicing without extra third-party audio dependencies.

**Independent Test**:
- Run `tools/tests/test_toolkit_audio_slice.py` verifying single-window slicing, multi-duration `--windows` extraction, auto-profile multi-scale window generation, boundary clamping, and exact sample-rate/channel/bit-depth preservation.

---

### User Story 3 - Ecosystem Synchronization & Replacing "Cannot Listen" Constraints (Priority: P1)

As the maintainer of `music_maker_plugin`, I want all plugin rules, skills, and sibling agents updated so the outdated `"you cannot listen to audio"` rule is replaced with a **Dual-Verification Audio QA** standard (Quantitative NumPy DSP + Direct Multi-Duration Listening QA), while preserving Zero-Code User Persona and strict plugin validation.

**Why this priority**: Currently `rules/AGENTS.md`, `soundfont-music/SKILL.md`, `mixing-timbre-mastering/SKILL.md`, `dsp-and-audio-verification.md`, and `executive-producer.md` forbid claiming to listen to audio or omit the listening QA stage, which blocks the new agent from participating in the standard production loop.

**Independent Test**:
- Run `agy plugin validate --strict music_maker_plugin` and verify 0 errors/warnings with 6 specialist agents registered; verify zero stale `"you can't listen"` / `"cannot physically listen"` contradictions remain.

---

### Edge Cases

- What happens when a requested slice window (`start_s` + `duration_s`) exceeds the total WAV duration or starts past the end? The slicer clamps safely to `[0, total_duration]` or fails cleanly with a descriptive error if the start offset is beyond the file end.
- What happens when inspecting a short game loop (`< 20s`) vs a long ballad (`> 5m`)? `--auto-profile` scales window durations proportionally (short micro/seam windows for loops; macro + 15–30s meso + 4–10s micro windows for full tracks).
- What happens if an audio passage is quiet, ambiguous, or clipped in a full-mix pass? The agent MUST slice a tighter duration window and/or inspect the corresponding `multi_track/` stem rather than guessing.
- What happens if temporary audit clips are created in a project output folder? The workflow documents cleaning up temporary audit clips after review so output folders stay tidy (`out/<song>.wav`, `out/<song>.mid`, `out/<song>/multi_track/`).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Create `music_maker_plugin/agents/audio-listening-critic.md` engineered with `llm-prompt-optimizer` (RSCIT structure, 6-step Chain-of-Thought protocol, 2 grounded Few-Shot examples, strict anti-hallucination guardrails, positive alternatives, and Output Template placed at the end).
- **FR-002**: The `audio-listening-critic` agent MUST support and instruct **Multi-Duration Segmented Listening**: Macro (full mix or large section spans), Meso (15–30s section/transition windows), Micro (3–10s surgical windows for fills, pitch bends, sustain pedal, and loop seams), and `multi_track/` stem isolation.
- **FR-003**: The `audio-listening-critic` agent MUST evaluate audio across a 5-axis professional rubric (Timbral Realism, Mix Balance & 3D Sound-Box, Groove & Transitions, Expressive Articulation, Emotional Arc & Genre Authenticity) with severity levels (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), `PASS`/`REVISE` verdict, internal engineering handoffs, and a Zero-Code producer summary for end users.
- **FR-004**: Implement `slice_wav()` and `slice_wav_segments()` in `music_maker_plugin/skills/soundfont-music/scripts/toolkit/engine/analysis.py` plus CLI `slice_audio.py` supporting `--start`/`--duration`, `--windows`, `--auto-profile`, and JSON output, using only Python standard library (`wave`, `json`, `argparse`, `pathlib`).
- **FR-005**: Update `music_maker_plugin/rules/AGENTS.md`, `agents/README.md`, `agents/soundfont-mix-engineer.md`, `agents/executive-producer.md`, `skills/soundfont-music/SKILL.md`, `skills/soundfont-music/references/toolkit.md`, `skills/mixing-timbre-mastering/SKILL.md`, `skills/mixing-timbre-mastering/references/dsp-and-audio-verification.md`, `plugin.json` (`1.8.0`), and `README.md` to establish Dual-Verification Audio QA.
- **FR-006**: Write TDD unit tests for audio slicing (`tools/tests/test_toolkit_audio_slice.py`), run all toolkit tests, validate with `agy plugin validate --strict music_maker_plugin`, run `code-reviewer`, and test the listening critic workflow end-to-end on `kpop_ballad_c_65bpm.wav` (cleaning up temporary slices afterward).

### Key Entities

- **Audio Listening Critic Agent (`audio-listening-critic`)**: Specialist QA producer agent evaluating real-world audio via `Read` and `slice_audio.py`.
- **Audit Window / Segment Clip**: A bounded time slice `(label, start_s, end_s, duration_s, wav_path)` extracted from a mix or stem for focused listening.
- **5-Axis Critique Report**: Structured verdict (`PASS` | `REVISE`) pairing measured NumPy stats with timestamped ear findings and fix routing.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `tools/tests/` passes 100% of unit tests including new audio-slicing boundary and multi-duration tests.
- **SC-002**: `agy plugin validate --strict music_maker_plugin` passes with 0 errors and 0 warnings (`skills 11 · agents 6 · rules 1`).
- **SC-003**: `code-reviewer` reports 0 CRITICAL and 0 HIGH issues across all new and modified files.
- **SC-004**: End-to-end validation on `kpop_ballad_c_65bpm.wav` produces verified multi-duration sliced clips and a grounded, timestamped critique report with 0 temporary files left in the workspace root.

## Assumptions

- Host environments supporting `music_maker_plugin` provide a multimodal `Read` tool capable of reading `.wav` files (`audio/wav`).
- Python standard library `wave` supports PCM WAV files generated by `soundfont-music` (`int16` / `int32` WAV); non-PCM compressed audio is out of scope for `slice_audio.py`.
