"""Render songs to WAV + MIDI + multi-track audio stems.

    python render.py                 render every song in songs/
    python render.py cozy_town       render one song (mix WAV, MIDI, and multi_track stems)
    python render.py cozy_town --midi-only
    python render.py cozy_town --stems-only
"""
import importlib
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _render_with_version_fallback(song, out, name):
    wav = os.path.join(out, f"{name}.wav")
    v = 2
    while True:
        try:
            song.render(wav)
            return wav
        except PermissionError:  # file is open in a media player
            wav = os.path.join(out, f"{name}_v{v}.wav")
            v += 1


def main(argv):
    midi_only = "--midi-only" in argv
    stems_only = "--stems-only" in argv
    names = [a for a in argv if not a.startswith("--")]
    if not names:
        names = sorted(f[:-3] for f in os.listdir(os.path.join(HERE, "songs"))
                       if f.endswith(".py") and not f.startswith("_"))
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    for name in names:
        module = importlib.import_module(f"songs.{name}")
        song = module.song
        print(f"{song.title}:")
        t = time.time()
        song.export_midi(os.path.join(out, f"{name}.mid"))
        if not midi_only:
            if not stems_only:
                wav = _render_with_version_fallback(song, out, name)
                print(f"  -> out/{os.path.basename(wav)}")
            stems_dir = os.path.join(out, name, "multi_track")
            song.export_stems(stems_dir, keep_pan=False)
            print(f"  -> out/{name}/multi_track/ ({time.time() - t:.1f}s)")
        if hasattr(module, "after_render"):
            module.after_render(out)
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
