"""CLI to slice variable-duration WAV segments for direct multi-scale listening QA.

Usage:
  python slice_audio.py mix.wav --start 85 --duration 15 --out audit/chorus.wav
  python slice_audio.py mix.wav --windows "0:10,55:22,95:30,210:8" --out-dir audit_clips
  python slice_audio.py mix.wav --auto-profile --bpm 65 --out-dir audit_clips
"""
import argparse
import json
import math
import os
import sys
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from engine.analysis import slice_wav, slice_wav_segments


def _parse_windows(spec: str):
    windows = []
    for idx, item in enumerate(spec.split(","), start=1):
        token = item.strip()
        if not token:
            continue
        parts = token.split(":")
        if len(parts) == 2:
            start_s, dur_s = float(parts[0]), float(parts[1])
            if not (math.isfinite(start_s) and math.isfinite(dur_s)):
                raise ValueError(f"Non-finite window values in '{token}'")
            label = f"win_{idx:02d}_{int(round(start_s))}s_{int(round(dur_s))}s"
        elif len(parts) == 3:
            label = parts[0].strip() or f"win_{idx:02d}"
            start_s, dur_s = float(parts[1]), float(parts[2])
            if not (math.isfinite(start_s) and math.isfinite(dur_s)):
                raise ValueError(f"Non-finite window values in '{token}'")
        else:
            raise ValueError(f"Invalid window spec '{token}'. Expected start:duration or label:start:duration")
        windows.append({"label": label, "start_s": start_s, "duration_s": dur_s})
    if not windows:
        raise ValueError("No valid windows parsed from --windows")
    return windows


def main(argv):
    p = argparse.ArgumentParser(description="Slice variable-duration WAV segments for direct listening QA")
    p.add_argument("wav", help="Path to source WAV file")
    p.add_argument("--start", type=float, default=None, help="Single-clip start time in seconds")
    p.add_argument("--duration", type=float, default=None, help="Single-clip duration in seconds")
    p.add_argument("--end", type=float, default=None, help="Single-clip end time in seconds")
    p.add_argument("--out", default=None, help="Output WAV path for single-clip mode")
    p.add_argument("--windows", default=None, help="Comma-separated 'start:dur' or 'label:start:dur' list")
    p.add_argument("--auto-profile", action="store_true", help="Auto-generate micro + meso multi-duration profile")
    p.add_argument("--bpm", type=float, default=None, help="Optional song BPM to align auto-profile bar lengths")
    p.add_argument("--loop-seam", type=float, default=None, help="Optional loop seam timestamp in seconds")
    p.add_argument("--out-dir", default="audit_clips", help="Output directory for multi-clip modes")
    args = p.parse_args(argv)

    single_flags = any(v is not None for v in (args.start, args.duration, args.end, args.out))
    has_windows = args.windows is not None
    active_modes = sum([bool(single_flags), bool(has_windows), bool(args.auto_profile)])
    if active_modes > 1:
        p.error("Single-clip flags (--start/--duration/--end/--out), --windows, and --auto-profile are mutually exclusive")

    try:
        if single_flags:
            if args.start is None:
                p.error("--start is required when using single-clip flags (--duration/--end/--out)")
            if not args.out:
                p.error("--out is required when using --start")
            rep = slice_wav(args.wav, args.out, start_s=args.start, duration_s=args.duration, end_s=args.end)
        elif has_windows:
            windows = _parse_windows(args.windows)
            rep = slice_wav_segments(args.wav, args.out_dir, windows=windows)
        else:
            rep = slice_wav_segments(
                args.wav,
                args.out_dir,
                auto_profile=True,
                bpm=args.bpm,
                loop_seam_s=args.loop_seam,
            )
    except (ValueError, FileNotFoundError, OSError, wave.Error) as exc:
        p.error(str(exc))

    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
