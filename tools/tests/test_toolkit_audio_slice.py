"""TDD tests for variable-duration WAV slicing in engine.analysis and slice_audio.py CLI."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
import wave

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLKIT_DIR = os.path.join(
    REPO_ROOT, "music_maker_plugin", "skills", "soundfont-music", "scripts", "toolkit"
)
if TOOLKIT_DIR not in sys.path:
    sys.path.insert(0, TOOLKIT_DIR)

from engine import analysis  # noqa: E402


def _write_test_wav(
    path: str,
    duration_s: float = 12.0,
    sr: int = 22050,
    freq: float = 440.0,
    channels: int = 2,
    sampwidth: int = 2,
) -> None:
    n = int(round(duration_s * sr))
    t = np.arange(n, dtype=np.float64) / sr
    left = 0.4 * np.sin(2.0 * np.pi * freq * t)
    if channels == 2:
        right = 0.25 * np.sin(2.0 * np.pi * (freq * 1.5) * t)
        data = np.stack([left, right], axis=1)
    else:
        data = left[:, None]

    if sampwidth == 2:
        raw = np.clip(data * 32767.0, -32768, 32767).astype("<i2").tobytes()
    elif sampwidth == 3:
        ints = np.clip(data * 8388607.0, -8388608, 8388607).astype("<i4")
        raw = ints.view(np.uint8).reshape(-1, 4)[:, :3].tobytes()
    else:
        raise ValueError(f"Unsupported test sampwidth {sampwidth}")

    with wave.open(path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sr)
        wf.writeframes(raw)


class TestAudioSlicing(unittest.TestCase):
    def test_slice_wav_preserves_format_and_clamps_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "full.wav")
            clip = os.path.join(tmp, "clip.wav")
            _write_test_wav(src, duration_s=10.0, sr=22050)

            meta = analysis.slice_wav(src, clip, start_s=7.5, duration_s=5.0)
            self.assertTrue(os.path.isfile(clip))
            self.assertAlmostEqual(meta["start_s"], 7.5, places=3)
            self.assertAlmostEqual(meta["end_s"], 10.0, places=3)
            self.assertAlmostEqual(meta["duration_s"], 2.5, places=3)
            self.assertTrue(meta["clamped"])

            with wave.open(clip, "rb") as wf:
                self.assertEqual(wf.getnchannels(), 2)
                self.assertEqual(wf.getsampwidth(), 2)
                self.assertEqual(wf.getframerate(), 22050)
                self.assertAlmostEqual(wf.getnframes() / 22050.0, 2.5, places=3)

    def test_slice_wav_preserves_mono_24bit_and_end_s(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "mono24.wav")
            clip = os.path.join(tmp, "mono24_clip.wav")
            _write_test_wav(src, duration_s=6.0, sr=16000, channels=1, sampwidth=3)

            meta = analysis.slice_wav(src, clip, start_s=1.25, end_s=3.75)
            self.assertFalse(meta["clamped"])
            self.assertAlmostEqual(meta["duration_s"], 2.5, places=3)
            with wave.open(clip, "rb") as wf:
                self.assertEqual(wf.getnchannels(), 1)
                self.assertEqual(wf.getsampwidth(), 3)
                self.assertEqual(wf.getframerate(), 16000)

    def test_slice_wav_rejects_invalid_and_non_finite_windows(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "full.wav")
            clip = os.path.join(tmp, "bad.wav")
            _write_test_wav(src, duration_s=4.0)

            for bad_kwargs in (
                {"start_s": 5.0, "duration_s": 1.0},
                {"start_s": -1.0, "duration_s": 1.0},
                {"start_s": 1.0, "duration_s": 0.0},
                {"start_s": 1.0, "duration_s": 1.0, "end_s": 2.0},
                {"start_s": float("nan"), "duration_s": 1.0},
                {"start_s": 0.5, "duration_s": float("inf")},
            ):
                with self.assertRaises(ValueError):
                    analysis.slice_wav(src, clip, **bad_kwargs)

    def test_auto_profile_windows_vary_durations_by_song_length(self):
        tiny = analysis.build_auto_profile_windows(total_duration_s=0.05)
        self.assertEqual(len(tiny), 1)
        self.assertAlmostEqual(tiny[0]["duration_s"], 0.05, places=3)

        short_windows = analysis.build_auto_profile_windows(total_duration_s=16.0, loop_seam_s=8.0)
        self.assertGreaterEqual(len(short_windows), 3)
        self.assertTrue(any(w["label"] == "loop_seam_micro" for w in short_windows))
        for w in short_windows:
            self.assertGreaterEqual(w["start_s"], 0.0)
            self.assertLessEqual(w["start_s"] + w["duration_s"], 16.0 + 1e-6)

        mid_windows = analysis.build_auto_profile_windows(total_duration_s=30.0, bpm=65)
        starts = [w["start_s"] for w in mid_windows]
        self.assertEqual(starts, sorted(starts))

        long_windows = analysis.build_auto_profile_windows(total_duration_s=240.0, bpm=65)
        self.assertGreaterEqual(len(long_windows), 5)
        durations = {round(w["duration_s"], 1) for w in long_windows}
        self.assertGreaterEqual(len(durations), 2, "Auto profile should include mixed micro and meso durations")

    def test_slice_wav_segments_multi_windows_and_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "song.wav")
            out_dir = os.path.join(tmp, "clips")
            _write_test_wav(src, duration_s=30.0)

            with self.assertRaises(ValueError):
                analysis.slice_wav_segments(src, out_dir, windows=[])
            with self.assertRaises(ValueError):
                analysis.slice_wav_segments(
                    src,
                    out_dir,
                    windows=[{"start_s": 0.0, "duration_s": 2.0}],
                    auto_profile=True,
                )

            rep = analysis.slice_wav_segments(
                src,
                out_dir,
                windows=[
                    {"label": "micro_fill", "start_s": 2.0, "duration_s": 4.0},
                    {"label": "meso_chorus", "start_s": 10.0, "duration_s": 12.0},
                ],
            )
            self.assertEqual(len(rep["segments"]), 2)
            self.assertAlmostEqual(rep["segments"][0]["duration_s"], 4.0, places=2)
            self.assertAlmostEqual(rep["segments"][1]["duration_s"], 12.0, places=2)
            for seg in rep["segments"]:
                self.assertTrue(os.path.isfile(seg["path"]))

    def test_slice_audio_cli_modes_and_error_handling(self):
        cli_path = os.path.join(TOOLKIT_DIR, "slice_audio.py")
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "cli_song.wav")
            _write_test_wav(src, duration_s=45.0)

            # 1. Explicit labeled + unlabeled --windows
            win_dir = os.path.join(tmp, "cli_windows")
            proc = subprocess.run(
                [sys.executable, cli_path, src, "--windows", "intro:0:5,12:15,35:8", "--out-dir", win_dir],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(proc.stdout)
            self.assertEqual(len(data["segments"]), 3)
            self.assertEqual(data["segments"][0]["label"], "intro")
            self.assertAlmostEqual(data["segments"][1]["duration_s"], 15.0, places=2)

            # 2. --auto-profile --bpm
            auto_dir = os.path.join(tmp, "cli_auto")
            proc_auto = subprocess.run(
                [sys.executable, cli_path, src, "--auto-profile", "--bpm", "65", "--out-dir", auto_dir],
                capture_output=True,
                text=True,
                check=True,
            )
            auto_data = json.loads(proc_auto.stdout)
            self.assertGreaterEqual(len(auto_data["segments"]), 4)
            for seg in auto_data["segments"]:
                self.assertTrue(os.path.isfile(seg["path"]))

            # 3. Single-clip --start --end --out
            single_out = os.path.join(tmp, "single.wav")
            proc_single = subprocess.run(
                [sys.executable, cli_path, src, "--start", "5", "--end", "11", "--out", single_out],
                capture_output=True,
                text=True,
                check=True,
            )
            single_data = json.loads(proc_single.stdout)
            self.assertAlmostEqual(single_data["duration_s"], 6.0, places=2)
            self.assertTrue(os.path.isfile(single_out))

            # 4. Conflicting modes, orphaned flags, and empty --windows must fail cleanly
            for bad_args in (
                [src, "--duration", "10", "--out", single_out],
                [src, "--windows", "0:5", "--auto-profile"],
                [src, "--windows", ""],
            ):
                bad = subprocess.run(
                    [sys.executable, cli_path, *bad_args],
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(bad.returncode, 0)
                self.assertNotIn("Traceback", bad.stderr)


if __name__ == "__main__":
    unittest.main()
