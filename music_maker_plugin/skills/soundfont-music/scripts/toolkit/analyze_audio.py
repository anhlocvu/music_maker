"""CLI to run quantitative NumPy acoustic & stem QA on a rendered WAV (and multi_track/).

Usage: python analyze_audio.py out/<song>.wav [--stems out/<song>/multi_track] [--lead lead] [--ref pop]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from engine.analysis import analyze_song_mix


def main(argv):
    p = argparse.ArgumentParser(description="Quantitative WAV and multi_track stem QA")
    p.add_argument("wav", help="Path to rendered mix WAV")
    p.add_argument("--stems", default=None, help="Path to multi_track/ stems folder")
    p.add_argument("--lead", default=None, help="Substring matching lead stem filename")
    p.add_argument("--ref", default=None, help="Reference genre key in tonal-references.json")
    args = p.parse_args(argv)
    rep = analyze_song_mix(args.wav, stems_dir=args.stems, lead_stem=args.lead, reference_genre=args.ref)
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
