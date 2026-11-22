"""Chord-symbol parsing and pitch-class utilities for voicing and score review."""
import re

PCS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
NOTE_NAMES = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
QUALITIES = {
    "": (0, 4, 7), "maj": (0, 4, 7), "M": (0, 4, 7), "m": (0, 3, 7), "min": (0, 3, 7), "-": (0, 3, 7), "5": (0, 7),
    "6": (0, 4, 7, 9), "m6": (0, 3, 7, 9), "7": (0, 4, 7, 10), "maj7": (0, 4, 7, 11), "M7": (0, 4, 7, 11),
    "m7": (0, 3, 7, 10), "min7": (0, 3, 7, 10), "-7": (0, 3, 7, 10), "mMaj7": (0, 3, 7, 11), "mmaj7": (0, 3, 7, 11),
    "9": (0, 4, 7, 10, 2), "maj9": (0, 4, 7, 11, 2), "M9": (0, 4, 7, 11, 2), "m9": (0, 3, 7, 10, 2),
    "add9": (0, 4, 7, 2), "madd9": (0, 3, 7, 2), "6/9": (0, 4, 7, 9, 2), "69": (0, 4, 7, 9, 2),
    "11": (0, 4, 7, 10, 2, 5), "m11": (0, 3, 7, 10, 2, 5), "13": (0, 4, 7, 10, 2, 9), "maj13": (0, 4, 7, 11, 2, 9),
    "m13": (0, 3, 7, 10, 2, 9), "sus2": (0, 2, 7), "sus4": (0, 5, 7), "sus": (0, 5, 7), "7sus4": (0, 5, 7, 10),
    "7sus": (0, 5, 7, 10), "9sus4": (0, 5, 7, 10, 2), "dim": (0, 3, 6), "o": (0, 3, 6), "dim7": (0, 3, 6, 9),
    "o7": (0, 3, 6, 9), "m7b5": (0, 3, 6, 10), "ø": (0, 3, 6, 10), "ø7": (0, 3, 6, 10), "aug": (0, 4, 8),
    "+": (0, 4, 8), "7#5": (0, 4, 8, 10), "+7": (0, 4, 8, 10), "7b5": (0, 4, 6, 10), "7b9": (0, 4, 7, 10, 1),
    "7#9": (0, 4, 7, 10, 3), "7#11": (0, 4, 7, 10, 6), "maj7#11": (0, 4, 7, 11, 6), "7b13": (0, 4, 7, 10, 8),
    "7alt": (0, 4, 8, 10, 1), "7b9b13": (0, 4, 8, 10, 1), "7#9#11": (0, 4, 6, 10, 3),
    "13#11": (0, 4, 7, 10, 6, 9), "13b9": (0, 4, 7, 10, 1, 9), "7#5#9": (0, 4, 8, 10, 3),
    "maj9#11": (0, 4, 7, 11, 2, 6), "mMaj9": (0, 3, 7, 11, 2), "mmaj9": (0, 3, 7, 11, 2),
    "6/9#11": (0, 4, 7, 9, 2, 6), "m11b5": (0, 3, 6, 10, 5), "sowhat": (0, 5, 10, 3, 7),
}


def pitch_class(name):
    """Return pitch class 0..11 for a note name like 'F#' or 'Bb'."""
    v = PCS[name[0].upper()]
    for ch in name[1:]:
        v += 1 if ch in "#♯" else -1 if ch in "b♭" else 0
    return v % 12


def midi_to_name(midi):
    """Convert MIDI note number (C4=60) to scientific pitch string."""
    return f"{NOTE_NAMES[int(midi) % 12]}{int(midi) // 12 - 1}"


def parse(symbol, transpose=0):
    """Parse a chord symbol like 'F#m7/A' or polychord 'D|C7' into pitch-class sets."""
    text = symbol.strip()
    if "|" in text:
        upper_sym, lower_sym = (part.strip() for part in text.split("|", 1))
        upper = parse(upper_sym, transpose=transpose)
        lower = parse(lower_sym, transpose=transpose)
        if upper is None or lower is None:
            return None
        return {
            "symbol": symbol,
            "root": lower["root"],
            "bass": lower["bass"],
            "quality": f"{upper_sym}|{lower_sym}",
            "pcs": upper["pcs"] | lower["pcs"],
            "upper_pcs": upper["pcs"],
            "lower_pcs": lower["pcs"],
        }
    m = re.fullmatch(r"([A-Ga-g][#b♯♭]?)(.*?)(?:/([A-Ga-g][#b♯♭]?))?", text.replace("Δ", "maj"))
    if not m or m.group(2) not in QUALITIES:
        return None
    root = (pitch_class(m.group(1)) + transpose) % 12
    bass = (pitch_class(m.group(3)) + transpose) % 12 if m.group(3) else root
    return {
        "symbol": symbol,
        "root": root,
        "bass": bass,
        "quality": m.group(2),
        "pcs": {(root + i) % 12 for i in QUALITIES[m.group(2)]} | {bass},
    }


def chord_at(timeline, beat):
    """Return the active parsed chord at `beat` from a sorted [(start_beat, symbol)] list."""
    current = None
    for start, sym in timeline:
        if start <= beat + 1e-9:
            current = parse(sym) if isinstance(sym, str) else sym
        else:
            break
    return current


SCALE_INTERVALS = {
    "major": (0, 2, 4, 5, 7, 9, 11),
    "ionian": (0, 2, 4, 5, 7, 9, 11),
    "minor": (0, 2, 3, 5, 7, 8, 10),
    "aeolian": (0, 2, 3, 5, 7, 8, 10),
    "natural minor": (0, 2, 3, 5, 7, 8, 10),
    "harmonic minor": (0, 2, 3, 5, 7, 8, 11),
    "melodic minor": (0, 2, 3, 5, 7, 9, 11),
    "dorian": (0, 2, 3, 5, 7, 9, 10),
    "phrygian": (0, 1, 3, 5, 7, 8, 10),
    "lydian": (0, 2, 4, 6, 7, 9, 11),
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    "locrian": (0, 1, 3, 5, 6, 8, 10),
    "major pentatonic": (0, 2, 4, 7, 9),
    "minor pentatonic": (0, 3, 5, 7, 10),
    "blues": (0, 3, 5, 6, 7, 10),
}

_MAJOR_PROF = (6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88)
_MINOR_PROF = (6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17)


def parse_scale(scale_name, transpose=0):
    """Parse a scale name like 'C major' or 'F# minor pentatonic' into a pitch-class set."""
    if not scale_name or not isinstance(scale_name, str):
        return None
    m = re.match(r"^\s*([A-Ga-g][#b♯♭]?)\s*(.*)$", scale_name.strip())
    if not m:
        return None
    root = (pitch_class(m.group(1)) + transpose) % 12
    qual = re.sub(r"\s+", " ", (m.group(2) or "major").strip().lower())
    if qual in ("m", "min"):
        qual = "minor"
    elif qual in ("maj", ""):
        qual = "major"
    elif qual == "pentatonic":
        qual = "major pentatonic"
    ivs = SCALE_INTERVALS.get(qual)
    if ivs is None:
        return None
    return {(root + iv) % 12 for iv in ivs}


def infer_scale_pcs(events, min_distinct=3):
    """Infer best-matching diatonic major/minor pitch-class set from Track events."""
    if not events:
        return None
    weights = [0.0] * 12
    distinct = set()
    for ev in events:
        key = int(ev[2]) % 12
        dur = max(0.05, float(ev[1]))
        vel = max(1, int(ev[3]))
        weights[key] += dur * (vel / 127.0)
        distinct.add(key)
    if len(distinct) < min_distinct:
        return None
    best_score, best_pcs = float("-inf"), None
    for root in range(12):
        rot = weights[root:] + weights[:root]
        maj_s = sum(w * p for w, p in zip(rot, _MAJOR_PROF))
        min_s = sum(w * p for w, p in zip(rot, _MINOR_PROF))
        if maj_s > best_score:
            best_score = maj_s
            best_pcs = {(root + iv) % 12 for iv in SCALE_INTERVALS["major"]}
        if min_s > best_score:
            best_score = min_s
            best_pcs = {(root + iv) % 12 for iv in SCALE_INTERVALS["minor"]}
    return best_pcs


_NR_COMPOSITE = {"S": "LPR", "N": "RLP", "H": "LPL"}
_US_DEGREES = {
    "I": 0, "bII": 1, "II": 2, "bIII": 3, "III": 4, "IV": 5,
    "#IV": 6, "bV": 6, "V": 7, "bVI": 8, "VI": 9, "bVII": 10, "VII": 11,
}
_TRIAD_IVS = {"maj": (0, 4, 7), "min": (0, 3, 7), "aug": (0, 4, 8), "dim": (0, 3, 6)}


def _to_pc(root):
    from numbers import Integral
    if isinstance(root, Integral) and not isinstance(root, bool):
        return int(root) % 12
    return pitch_class(root)


def _normalize_triad_mode(spec, allow_major_triad_aliases=True):
    s = str(spec).strip()
    if s == "M" or s.lower() in ("maj", "major"):
        return "maj"
    if s == "m" or s.lower() in ("min", "minor"):
        return "min"
    if allow_major_triad_aliases and s == "":
        return "maj"
    raise ValueError(f"Expected major or minor mode/quality, got: {spec!r}")


def plr_transform(root_pc, quality="maj", ops="P"):
    """Apply Neo-Riemannian transformations (P, L, R, S, N, H or chains) to a major/minor triad."""
    r = _to_pc(root_pc)
    q = _normalize_triad_mode(quality)
    expanded = "".join(_NR_COMPOSITE.get(ch, ch) for ch in ops.upper())
    for ch in expanded:
        if ch == "P":
            q = "min" if q == "maj" else "maj"
        elif ch == "L":
            r, q = ((r + 4) % 12, "min") if q == "maj" else ((r + 8) % 12, "maj")
        elif ch == "R":
            r, q = ((r + 9) % 12, "min") if q == "maj" else ((r + 3) % 12, "maj")
        else:
            raise ValueError(f"Unknown Neo-Riemannian op: {ch}")
    return (r, q)


def negative_harmony_pcs(pcs, tonic="C"):
    """Reflect pitch classes across the tonic-dominant symmetry axis (2*tonic + 7 mod 12)."""
    axis = (2 * _to_pc(tonic) + 7) % 12
    return {(axis - int(p)) % 12 for p in pcs}


def coltrane_cycle(start_root="B", direction=-1, include_dominants=True):
    """Generate a major-third Coltrane tonal-center cycle (with optional V7 bridges)."""
    r = _to_pc(start_root)
    step = 4 if direction >= 0 else -4
    centers = [(r + k * step) % 12 for k in range(3)]
    if not include_dominants:
        return [NOTE_NAMES[c] for c in centers]
    chain = []
    for idx, c in enumerate(centers):
        chain.append(f"{NOTE_NAMES[c]}maj7")
        nxt = centers[(idx + 1) % 3]
        chain.append(f"{NOTE_NAMES[(nxt + 7) % 12]}7")
    return chain


def barry_harris_scale(tonic="C", mode="major"):
    """Return the Barry Harris 8-note 6th-diminished scale and its two interlocking chord families."""
    r = _to_pc(tonic)
    is_min = _normalize_triad_mode(mode, allow_major_triad_aliases=False) == "min"
    scale_ivs = (0, 2, 3, 5, 7, 8, 9, 11) if is_min else (0, 2, 4, 5, 7, 8, 9, 11)
    sixth_ivs = (0, 3, 7, 9) if is_min else (0, 4, 7, 9)
    dim_ivs = (11, 2, 5, 8)
    return {
        "scale_pcs": [(r + i) % 12 for i in scale_ivs],
        "tonic_sixth_pcs": {(r + i) % 12 for i in sixth_ivs},
        "diminished_pcs": {(r + i) % 12 for i in dim_ivs},
    }


def upper_structure_triad(root="C", us_degree="II", triad_quality="maj", shell="37"):
    """Build an Upper-Structure Triad over a dominant/major/minor guide-tone shell."""
    r = _to_pc(root)
    deg = _US_DEGREES.get(us_degree)
    if deg is None or triad_quality not in _TRIAD_IVS:
        raise ValueError(f"Invalid upper structure spec: {us_degree} {triad_quality}")
    u_root = (r + deg) % 12
    upper_pcs = {(u_root + iv) % 12 for iv in _TRIAD_IVS[triad_quality]}
    shell_map = {"37": (4, 10), "maj37": (4, 11), "min37": (3, 10)}
    if shell not in shell_map:
        raise ValueError(f"Unknown shell type: {shell!r}; expected one of {tuple(shell_map)}")
    shell_ivs = shell_map[shell]
    shell_pcs = {(r + iv) % 12 for iv in shell_ivs}
    return {
        "root": r,
        "upper_root": u_root,
        "upper_pcs": upper_pcs,
        "shell_pcs": shell_pcs,
        "all_pcs": upper_pcs | shell_pcs,
    }
