# Data Model & CLI Contract: Audio Segment Slicing & Critique

## 1. Engine Functions (`engine/analysis.py`)

### `slice_wav(wav_path, out_path, start_s=0.0, duration_s=None, end_s=None) -> dict`
- Reads PCM WAV headers (`nchannels`, `sampwidth`, `framerate`, `nframes`) via `wave.open(..., "rb")`.
- Validates `start_s >= 0` and `< total_duration_s` (unless file is empty; raises `ValueError` on invalid window or empty slice).
- Clamps `end_s` to `total_duration_s`.
- Writes exact PCM frame slice preserving `nchannels`, `sampwidth`, and `framerate`.
- Returns dict:
  - `path`: `str` (output WAV path)
  - `source`: `str` (source WAV path)
  - `start_s`: `float`
  - `end_s`: `float`
  - `duration_s`: `float`
  - `total_duration_s`: `float`
  - `sample_rate`: `int`
  - `channels`: `int`
  - `clamped`: `bool`

### `build_auto_profile_windows(total_duration_s, bpm=None, loop_seam_s=None) -> list[dict]`
- Produces multi-duration windows adapted to track length:
  - Short cues (`<= 25s`): macro/full slice or opening (6–8s) + mid/climax (6–8s) + seam/ending (4–6s).
  - Medium/Full tracks (`> 25s`): variable-duration profile covering:
    - `intro_micro` (~8–10s near start)
    - `verse_meso` (~18–25s around 22–30% mark)
    - `transition_micro` (~8–10s around 42–48% mark)
    - `chorus_climax_meso` (~25–30s around 55–72% mark)
    - `bridge_detail_micro` (~10–12s around 75–82% mark)
    - `outro_micro` (~10–12s at end)
  - Deduplicates/clamps windows cleanly inside `[0, total_duration_s]`.

### `slice_wav_segments(wav_path, out_dir, windows=None, auto_profile=False, bpm=None, loop_seam_s=None) -> dict`
- Extracts multiple labeled segments into `out_dir` and returns `{source, total_duration_s, sample_rate, channels, segments: [...]}`.

## 2. CLI (`slice_audio.py`)
- `python slice_audio.py <wav> --start 85 --duration 15 --out clip.wav`
- `python slice_audio.py <wav> --windows "0:10,55:22,95:30,210:8" --out-dir audit_clips`
- `python slice_audio.py <wav> --auto-profile [--bpm 65] --out-dir audit_clips`
- Outputs JSON report to stdout.
