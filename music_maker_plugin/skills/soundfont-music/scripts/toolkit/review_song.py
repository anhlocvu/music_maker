"""CLI to run score review diagnostics on a song module in songs/.

Usage: python review_song.py <song_name>
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from engine.review import format_review, review_song


def main(argv):
    if not argv:
        print("Usage: python review_song.py <song_name>")
        sys.exit(1)
    name = argv[0]
    mod = importlib.import_module(f"songs.{name}")
    harmony = getattr(mod, "harmony", None)
    rep = review_song(mod.song, harmony=harmony)
    print(format_review(rep))


if __name__ == "__main__":
    main(sys.argv[1:])
