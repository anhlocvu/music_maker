# Research Notes: Multi-Duration Audio Listening QA

## Decision 1: How to enable "nghe từng đoạn với từng thời lượng khác nhau" natively
- **Decision**: Implement a pure-stdlib `wave` segment slicer (`slice_wav`, `slice_wav_segments`, `build_auto_profile_windows`) inside `engine/analysis.py` + `slice_audio.py` CLI, paired with `Read` (`read_file`) multimodal `audio/wav` inspection.
- **Rationale**: `read_file` loads an entire `.wav` file natively without start/end timestamp arguments. Slicing targeted time ranges (e.g., 3–10s micro clips, 15–30s meso clips, 45–60s macro spans) into short `.wav` clips lets the critic agent zoom into exact transitions, drum fills, pitch bends, sustain-pedal changes, loop seams, and `multi_track/` stem comparisons with zero external dependencies (`ffmpeg` not required).
- **Alternatives considered**:
  - Relying solely on full-file `Read`: misses micro-glitches (clicks, subtle bend drifts, brief masking) in long 4–6 minute tracks.
  - Requiring `ffmpeg` or `pydub`: breaks portability on clean Windows/Python environments without `ffmpeg` on `PATH`.

## Decision 2: Prompt Engineering Architecture (`llm-prompt-optimizer`)
- **Decision**: Structure `music_maker_plugin/agents/audio-listening-critic.md` using full RSCIT, a 6-step Chain-of-Thought protocol, 2 contrasting Few-Shot examples (`REVISE` vs `PASS`), explicit anti-hallucination rules (`Uncertain -> slice tighter window`), positive alternatives for constraints, and placing the explicit Output Format template at the end of the prompt.
- **Rationale**: Placing the Output Template at the end after examples maximizes format compliance, while Few-Shot examples prevent generic praise and anchor timestamped evidence.

## Decision 3: Updating "Cannot Listen" Rules to Dual-Verification QA
- **Decision**: Replace `"you can't listen / never claim to have listened"` across `soundfont-music/SKILL.md`, `mixing-timbre-mastering/SKILL.md`, `dsp-and-audio-verification.md`, and `executive-producer.md` with **Dual-Verification Audio QA**: never claim ear impressions without actually reading the WAV/slices via `Read`, and always pair direct listening with quantitative `analyze_audio.py` metrics.
- **Rationale**: Preserves honesty and anti-hallucination while unlocking real acoustic listening QA.
