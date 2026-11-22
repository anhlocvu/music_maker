"""CLI to run score review diagnostics on a song module in songs/.

Usage: python review_song.py <song_name> [--prompted track1,track2]
"""
import argparse
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from engine.review import format_review, review_song


def main(argv):
    p = argparse.ArgumentParser(description="Score-level diagnostics and GTR-CTRL symbolic metrics")
    p.add_argument("song_name", help="Song module name inside songs/")
    p.add_argument("--prompted", default=None, help="Comma-separated list of prompted track names for PIP/UIP")
    args = p.parse_args(argv)
    mod = importlib.import_module(f"songs.{args.song_name}")
    harmony = getattr(mod, "harmony", None)
    prompted = [s.strip() for s in args.prompted.split(",") if s.strip()] if args.prompted else None
    rep = review_song(mod.song, harmony=harmony, prompted_tracks=prompted)
    print(format_review(rep))


if __name__ == "__main__":
    main(sys.argv[1:])
