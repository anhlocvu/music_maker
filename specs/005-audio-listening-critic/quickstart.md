# Quickstart Validation Guide: `audio-listening-critic`

## 1. Unit Tests (TDD)
```powershell
uv run --with numpy --with scipy --with mido python -B -m unittest discover -s tools/tests -v
```
Expected: All existing tests + new `test_toolkit_audio_slice.py` tests pass.

## 2. CLI Slicing Smoke Check on Real Audio
```powershell
uv run python -B music_maker_plugin/skills/soundfont-music/scripts/toolkit/slice_audio.py kpop_ballad_c_65bpm.wav --auto-profile --bpm 65 --out-dir tmp_audit_clips
```
Expected: JSON output listing multi-duration WAV clips (micro 8–12s and meso 20–30s segments) inside `tmp_audit_clips/`, readable directly with `Read`. Clean up `tmp_audit_clips/` immediately after listening verification.

## 3. Strict Plugin Validation
```powershell
agy plugin validate --strict music_maker_plugin
```
Expected: `Validation passed` with `skills 11 · agents 6 · rules 1` (0 errors, 0 warnings).
