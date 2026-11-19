"""Soundfont registry and instrument names.

No fonts are built in - register the user's own:
    from engine import instruments
    instruments.register_font("main", r"C:/path/to/GeneralMIDI.sf2")   # default for GM names
    instruments.register_font("chip", r"C:/path/to/chiptune.sf2")

Instruments can then be given as
  - a GM name ("piano", "strings", "drums_power" ...) -> that program in the "main" font
  - a tuple (font key, bank, program), e.g. ("chip", 0, 80)
  - a built-in synth name from engine/synth.py ("nes_pulse25", "osc_sine" ...)
Browse any font with:  python list_presets.py <font key> [search]

Fonts can also be registered from the environment:
  SOUNDFONT_MAIN=C:/fonts/gm.sf2           -> key "main"
  SOUNDFONT_DIR=C:/fonts                   -> relative file names resolve against it
"""
import os
from .sf2 import SoundFont
from .synth import SYNTHS

SOUNDFONT_DIR = os.environ.get("SOUNDFONT_DIR", "")

FONTS = {}          # key -> .sf2 path (absolute, or relative to SOUNDFONT_DIR)
if os.environ.get("SOUNDFONT_MAIN"):
    FONTS["main"] = os.environ["SOUNDFONT_MAIN"]

_fonts = {}


def register_font(key, path):
    """Make a soundfont available under `key`. The key "main" is used by GM names."""
    FONTS[key] = path
    _fonts.pop(key, None)
    return key


# General MIDI program numbers (0-based) - valid for any GM-layout soundfont
GM = {
    "piano": 0, "brightpiano": 1, "epiano": 4, "epiano2": 5, "harpsichord": 6, "clavinet": 7,
    "celesta": 8, "glockenspiel": 9, "musicbox": 10, "vibraphone": 11, "marimba": 12,
    "xylophone": 13, "tubularbells": 14, "dulcimer": 15,
    "organ": 16, "percorgan": 17, "rockorgan": 18, "churchorgan": 19, "accordion": 21,
    "harmonica": 22,
    "nylonguitar": 24, "steelguitar": 25, "jazzguitar": 26, "cleanguitar": 27, "mutedguitar": 28,
    "odguitar": 29, "distguitar": 30, "harmonics": 31,
    "acousticbass": 32, "fingerbass": 33, "pickbass": 34, "fretless": 35, "slapbass": 36,
    "slapbass2": 37, "synthbass": 38, "synthbass2": 39,
    "violin": 40, "viola": 41, "cello": 42, "contrabass": 43, "tremolostrings": 44,
    "pizzicato": 45, "harp": 46, "timpani": 47,
    "strings": 48, "slowstrings": 49, "synthstrings": 50, "choir": 52, "voiceoohs": 53,
    "synthvoice": 54, "orchhit": 55,
    "trumpet": 56, "trombone": 57, "tuba": 58, "mutedtrumpet": 59, "frenchhorn": 60,
    "brass": 61, "synthbrass": 62,
    "sopranosax": 64, "sax": 65, "tenorsax": 66, "barisax": 67, "oboe": 68, "englishhorn": 69,
    "bassoon": 70, "clarinet": 71, "piccolo": 72, "flute": 73, "recorder": 74, "panflute": 75,
    "bottle": 76, "shakuhachi": 77, "whistle": 78, "ocarina": 79,
    "squarelead": 80, "sawlead": 81, "calliope": 82, "chifflead": 83, "charang": 84,
    "voicelead": 85, "fifthslead": 86, "basslead": 87,
    "pad": 88, "warmpad": 89, "polysynth": 90, "choirpad": 91, "bowedpad": 92,
    "metalpad": 93, "halopad": 94, "sweeppad": 95,
    "sitar": 104, "banjo": 105, "shamisen": 106, "koto": 107, "kalimba": 108, "bagpipe": 109,
    "fiddle": 110, "shanai": 111,
    "tinklebell": 112, "agogo": 113, "steeldrums": 114, "woodblock": 115, "taiko": 116,
    "melodictom": 117, "synthdrum": 118, "reversecymbal": 119,
}
# GM/GS drum kits live in bank 128 (these program numbers are the GS standard)
KITS = {"drums": 0, "drums_room": 8, "drums_power": 16, "drums_electronic": 24,
        "drums_808": 25, "drums_jazz": 32, "drums_brush": 40, "drums_orch": 48}

INSTRUMENTS = {name: ("main", 0, p) for name, p in GM.items()}
INSTRUMENTS.update({name: ("main", 128, p) for name, p in KITS.items()})


def font(key):
    if key not in _fonts:
        if key not in FONTS:
            raise KeyError(
                f"no soundfont registered as {key!r}. Ask the user which .sf2 files to use, "
                f"then call instruments.register_font({key!r}, path).")
        path = FONTS[key]
        if not os.path.isabs(path):
            path = os.path.join(SOUNDFONT_DIR, path)
        print(f"  loading {os.path.basename(path)} ...")
        _fonts[key] = SoundFont(path)
    return _fonts[key]


def font_key_for_file(filename):
    """Register a soundfont by file name (e.g. from a Reaper project) and return its key."""
    for k, f in FONTS.items():
        if os.path.basename(f).lower() == os.path.basename(filename).lower():
            return k
    key = os.path.splitext(os.path.basename(filename))[0]
    FONTS[key] = filename
    return key


def resolve(name):
    """Instrument name or (font key, bank, program) tuple -> (font key, bank, program)."""
    if isinstance(name, tuple):
        return name
    return INSTRUMENTS.get(name, ("synth", 0, 80))


def load(name):
    if isinstance(name, str) and name in SYNTHS:
        return SYNTHS[name]
    fkey, bank, prog = resolve(name)
    return font(fkey).preset(bank, prog)
