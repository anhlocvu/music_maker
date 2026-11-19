"""Read a Reaper project (.RPP) into a Song.

Takes the tempo, each track's name / volume / pan, the inline MIDI items, and -
for tracks using the BassMidi VSTi - which soundfont and preset the plugin has
loaded, so the Python render sounds like the Reaper one. Tracks using other
instruments get the `fallback` preset (GM piano in the "main" font by default).
"""
import base64
import binascii
import math
import os
import re

from .song import Song
from . import instruments

# offsets inside BassMidi VSTi's saved state (found by comparing tracks)
BASSMIDI_BANK_OFS = 2715
BASSMIDI_PROG_OFS = 2719


def _b64(line):
    try:
        return base64.b64decode(line + "=" * (-len(line) % 4))
    except binascii.Error:
        return b""


def _bassmidi(track_text):
    m = re.search(r'<VST "VSTi: BassMidi[^\n]*\n(.*?)\n\s*>', track_text, re.S)
    if not m:
        return None
    raw = b"".join(_b64(l.strip()) for l in m.group(1).splitlines())
    path = re.search(rb"((?:[\x20-\x7e]\x00)+?\.\x00s\x00f\x00[23z]\x00)", raw, re.I)
    if not path or len(raw) <= BASSMIDI_PROG_OFS:
        return None
    sf = os.path.basename(path.group(1).decode("utf-16le"))
    return sf, raw[BASSMIDI_BANK_OFS], raw[BASSMIDI_PROG_OFS]


def _items(track_text):
    """Yield (item_start_beats, [(start, beats, key, vel)]) for each MIDI item."""
    for item in re.split(r"\n\s*<ITEM", track_text)[1:]:
        pos = re.search(r"^\s*POSITION ([\d.]+)", item, re.M)
        src = re.search(r"<SOURCE MIDI(.*?)\n\s*>", item, re.S)
        if not pos or not src:
            continue
        body = src.group(1)
        ppq = int(re.search(r"HASDATA \d+ (\d+)", body).group(1))
        tick, on, notes = 0, {}, []
        for m in re.finditer(r"^\s*[Ee]m? (\d+) ([0-9a-f]{2}) ([0-9a-f]{2}) ([0-9a-f]{2})", body, re.M):
            tick += int(m.group(1))
            st, a, b = int(m.group(2), 16), int(m.group(3), 16), int(m.group(4), 16)
            kind = st & 0xF0
            if kind == 0x90 and b > 0:
                on[a] = (tick, b)
            elif (kind == 0x80 or kind == 0x90) and a in on:
                s, v = on.pop(a)
                notes.append((s / ppq, (tick - s) / ppq, a, v))
        yield float(pos.group(1)), notes


def load_rpp(path, fallback=("main", 0, 0), font_overrides=None):
    """font_overrides: {"file.sf2": "other.sf2"} to swap a font you don't have locally."""
    text = open(path, encoding="utf-8", errors="replace").read()
    tempo = re.search(r"^\s*TEMPO ([\d.]+)", text, re.M)
    bpm = float(tempo.group(1)) if tempo else 120.0
    song = Song(os.path.splitext(os.path.basename(path))[0], bpm=bpm)
    for tr in re.split(r"\n\s*<TRACK ", text)[1:]:
        name = re.search(r"^\s*NAME (.+)$", tr, re.M).group(1).strip().strip('"')
        volpan = re.search(r"^\s*VOLPAN ([\d.e-]+) ([\d.e-]+)", tr, re.M)
        vol, pan = (float(volpan.group(1)), float(volpan.group(2))) if volpan else (1.0, 0.0)
        bm = _bassmidi(tr)
        if bm:
            sf, bank, prog = bm
            sf = (font_overrides or {}).get(sf, sf)
            inst = (instruments.font_key_for_file(sf), bank, prog)
        else:
            inst = fallback
        t = song.track(name, inst, volume=vol, pan=pan, reverb=0.25)
        for item_pos, notes in _items(tr):
            off = item_pos * bpm / 60.0
            t.events.extend((off + s, b, k, v, None) for s, b, k, v in notes)
        t.events.sort()
        t._cursor = t.length()
    return song


def loop_length(song, beats_per_bar=4):
    """Length of the longest track rounded up to whole bars."""
    return math.ceil(max(t.length() for t in song.tracks) / beats_per_bar - 1e-3) * beats_per_bar
