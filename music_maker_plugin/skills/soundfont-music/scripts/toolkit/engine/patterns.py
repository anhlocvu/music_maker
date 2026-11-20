"""Drum-pattern lookup (Bardet 200+260 + Pocket Operations) and empirical Groove MIDI stats."""
import functools
import json
from pathlib import Path
import random

# Map external drum-pattern track names to soundfont-music DRUMS token names.
PIECE_TO_TOKEN = {
    "BassDrum": "kick", "BD": "kick", "kick": "kick",
    "SnareDrum": "snare", "SN": "snare", "SD": "snare", "snare": "snare",
    "RimShot": "rim", "RS": "rim", "cross_stick": "rim",
    "Claps": "clap", "HandClap": "clap", "CL": "clap", "CP": "clap",
    "ClosedHiHat": "hat", "CH": "hat", "hat_closed": "hat",
    "OpenHiHat": "ohat", "OH": "ohat", "hat_open": "ohat",
    "PedalHiHat": "phat", "hat_pedal": "phat",
    "RideCymbal": "ride", "CY": "crash", "Cymbal": "crash", "ride": "ride", "crash": "crash",
    "LowTom": "tom3", "LT": "tom3", "tom_low": "tom3",
    "MediumTom": "tom2", "MT": "tom2", "tom_mid": "tom2",
    "HighTom": "tom1", "HT": "tom1", "tom_high": "tom1",
    "Tambourine": "tamb", "TM": "tamb",
    "Cowbell": "cowbell", "CB": "cowbell",
    "Shaker": "shaker", "SH": "shaker",
    "HighConga": "conga", "HC": "conga",
}


def _find_skill_asset(rel_path):
    """Locate an asset under toolkit/assets or sibling groove-rhythm-drums/assets."""
    here = Path(__file__).resolve()
    candidates = [
        here.parents[1] / "assets" / rel_path,
        here.parents[4] / "groove-rhythm-drums" / "assets" / rel_path,
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


@functools.lru_cache(maxsize=1)
def _load_all_patterns():
    out = []
    for fname, src in (("Patterns_200.json", "bardet_200"), ("Patterns_260.json", "bardet_260")):
        p = _find_skill_asset(f"drum-patterns/{fname}")
        if not p:
            continue
        for item in json.loads(p.read_text(encoding="utf-8")):
            steps = int(item.get("length", 16))
            tracks = {}
            for raw_k, seq in (item.get("tracks") or {}).items():
                tok = PIECE_TO_TOKEN.get(raw_k)
                if tok:
                    tracks[tok] = [1 if str(v).lower() == "note" else 0 for v in seq[:steps]]
            out.append({"name": item.get("title", "unnamed"), "source": src, "steps": steps, "tracks": tracks})

    po = _find_skill_asset("drum-patterns/pocket_operations_patterns.json")
    if po:
        data = json.loads(po.read_text(encoding="utf-8"))
        for item in data.get("patterns", []):
            tracks = {}
            steps = 16
            for raw_k, seq in (item.get("rows") or {}).items():
                tok = PIECE_TO_TOKEN.get(raw_k)
                if tok:
                    steps = max(steps, len(seq))
                    tracks[tok] = [1 if int(v) else 0 for v in seq]
            out.append({"name": item.get("name", "unnamed"), "source": "pocket_operations", "steps": steps, "tracks": tracks})
    return out


def list_patterns(source="all", query=None):
    """Return matching drum patterns from 'bardet_200', 'bardet_260', 'pocket_operations', or 'all'."""
    pats = _load_all_patterns()
    if source != "all":
        pats = [p for p in pats if p["source"] == source]
    if query:
        q = query.lower()
        pats = [p for p in pats if q in p["name"].lower()]
    return pats


def pattern_to_steps(pattern_or_name, bars=1, combine=False, vel=100):
    """Convert a pattern dict or name into `soundfont-music` step string(s)."""
    if isinstance(pattern_or_name, str):
        matches = list_patterns(query=pattern_or_name)
        if not matches:
            raise ValueError(f"Drum pattern not found: {pattern_or_name}")
        pat = next((m for m in matches if m["name"].lower() == pattern_or_name.lower()), matches[0])
    else:
        pat = pattern_or_name

    n_steps = int(pat.get("steps", 16))
    tracks = pat.get("tracks", {})
    if not combine:
        per_voice = {}
        for tok, grid in tracks.items():
            bar_str = " ".join(f"{tok}@{vel}" if (i < len(grid) and grid[i]) else "." for i in range(n_steps))
            per_voice[tok] = " | ".join([bar_str] * max(1, int(bars)))
        return per_voice

    bar_tokens = []
    for i in range(n_steps):
        hits = [tok for tok, grid in tracks.items() if i < len(grid) and grid[i]]
        bar_tokens.append("+".join(hits) if hits else ".")
    bar_str = " ".join(bar_tokens)
    return " | ".join([bar_str] * max(1, int(bars)))


def drum_stats_suggest(feel="funk", bars=4, seed=1):
    """Generate a multi-bar 16th-step drum string sampled from Groove MIDI Dataset statistics."""
    p = _find_skill_asset("drum-statistics.json")
    if not p:
        raise FileNotFoundError("drum-statistics.json not found in skill assets")
    data = json.loads(p.read_text(encoding="utf-8"))
    feels = data.get("feels", {})
    if feel not in feels:
        raise ValueError(f"Unknown feel {feel!r}; choose from {sorted(feels)}")
    onset = feels[feel]["onset"]
    rng = random.Random(seed)

    bar_strings = []
    for b in range(max(1, int(bars))):
        tokens = []
        is_last = (b == bars - 1) and bars >= 2
        for step in range(16):
            hits = []
            for raw_piece in ("kick", "snare", "hat_closed", "hat_open", "ride"):
                probs = onset.get(raw_piece)
                if not probs or step >= len(probs):
                    continue
                if rng.random() < probs[step]:
                    hits.append(PIECE_TO_TOKEN[raw_piece])
            if b == 0 and step == 0 and "kick" not in hits:
                hits.insert(0, "kick")
            if is_last and step >= 12 and rng.random() < 0.45:
                hits = [PIECE_TO_TOKEN["tom_mid"] if step % 2 == 0 else "snare"]
            tokens.append("+".join(dict.fromkeys(hits)) if hits else ".")
        bar_strings.append(" ".join(tokens))
    return " | ".join(bar_strings)
