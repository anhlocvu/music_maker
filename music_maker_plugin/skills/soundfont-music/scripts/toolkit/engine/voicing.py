"""Dynamic-programming voice leading and Track voicing helpers."""
import itertools
import warnings

import numpy as np

from . import harmony as harm
from .harmony import QUALITIES, parse

# Robin Hoffmann low interval limits (lowest MIDI pitch per semitone span).
LOW_INTERVAL_LIMITS = {
    1: 52, 2: 51, 3: 48, 4: 46, 5: 46, 6: 46, 7: 34, 8: 43,
    9: 41, 10: 41, 11: 41, 13: 40, 14: 39, 15: 36, 16: 34,
}
TOP_WEIGHT, LEAP_COST, DRIFT_COST = 1.5, 1.0, 0.3
PARALLEL_COST = 1e6


class GivenUp(UserWarning):
    """Raised when no voicing in range satisfies all spacing/low-interval limits."""


def _rubs(a, b):
    """True when two pitches form a minor second or minor ninth."""
    return abs(a - b) in (1, 13)


def _chord_intervals(parsed):
    """Return chord intervals relative to root, supporting both QUALITIES keys and polychords."""
    if parsed["quality"] in QUALITIES:
        return QUALITIES[parsed["quality"]]
    return [0] + sorted((p - parsed["root"]) % 12 for p in parsed["pcs"] if (p - parsed["root"]) % 12 != 0)


def chord_tones(symbol, voices, rotation=0, omit=0, exclude=(), keep_root=False):
    """Select `voices` pitch classes for `symbol` following standard arranging omission order."""
    c = parse(symbol)
    if c is None:
        raise ValueError(f"Unknown chord symbol: {symbol}")
    iv = [i for i in dict.fromkeys(_chord_intervals(c)) if (c["root"] + i) % 12 not in exclude]
    third = any(i in iv for i in (3, 4))
    colour = any(i in iv for i in (9, 10, 11))
    major_seventh = 11 in iv

    def rank(i):
        if i == 7:
            return 0.5 if major_seventh else 0
        if i == 0:
            return 9 if keep_root else 0 if major_seventh else 1
        if i == 5 and third:
            return 2
        if i == 2 and third and colour:
            return 3
        return 9

    keep = sorted(iv, key=rank)
    while len(keep) > voices and rank(keep[0]) < 9:
        keep.pop(0)
    if len(keep) > voices:
        raise ValueError(f"{symbol} needs at least {len(keep)} voices")
    for _ in range(omit):
        if len(keep) > 1 and rank(keep[0]) < 9:
            keep.pop(0)
    order = (
        [i for i in (0, 7) if i in keep]
        + [i for i in keep if i not in (0, 7, 3, 4)]
        + [i for i in keep if i in (3, 4)]
    )
    clear = [i for i in order if not any((i - j) % 12 in (1, 11) for j in keep if j != i)]
    doubling = clear or order
    out, k = list(keep), rotation
    while len(out) < voices:
        out.append(doubling[k % len(doubling)])
        k += 1
    return [(c["root"] + i) % 12 for i in out]


def candidates(pcs, low, high, max_gap=12, limits=True, against=(), unisons=True):
    """Return sorted valid MIDI voicings of `pcs` inside [low, high]."""
    options = [[p for p in range(low, high + 1) if p % 12 == pc] for pc in pcs]
    found = set()
    for combo in itertools.product(*options):
        v = tuple(sorted(combo))
        if len(set(v)) < len(v) or any(b - a > max_gap for a, b in zip(v, v[1:])):
            continue
        if limits and (
            any(a < LOW_INTERVAL_LIMITS.get(b - a, 0) for a, b in zip(v, v[1:]))
            or any(_rubs(a, b) for a, b in itertools.combinations(v, 2))
            or any(_rubs(a, b) or (a == b and not unisons) for a in v for b in against)
        ):
            continue
        found.add(v)
    return sorted(found)


def _parallels(a, b, d):
    count = np.zeros(d.shape[:2])
    n = a.shape[1]
    for i in range(n):
        for j in range(i + 1, n):
            ia, ib = (a[:, j] - a[:, i]) % 12, (b[:, j] - b[:, i]) % 12
            same = (ia[:, None] == ib[None, :]) & np.isin(ia, (0, 7))[:, None]
            si, sj = np.sign(d[..., i]), np.sign(d[..., j])
            count += same & (si == sj) & (si != 0)
    return count


def voice_lead(
    symbols,
    voices=4,
    low=48,
    high=79,
    start=None,
    ceilings=None,
    avoid_parallels=False,
    max_gap=12,
    against=None,
    keep_root=False,
):
    """Voice a chord progression with minimal voice motion and low-interval hygiene."""
    if not symbols:
        return []
    cands = []
    for k, symbol in enumerate(symbols):
        top = min(high, ceilings[k]) if ceilings is not None and ceilings[k] is not None else high
        sets = []
        root = keep_root[k] if isinstance(keep_root, (list, tuple)) else keep_root
        for omit, r in itertools.product((0, 1), range(voices)):
            pcs = chord_tones(symbol, voices, r, omit, keep_root=root)
            if sorted(pcs) not in [sorted(x) for x in sets]:
                sets.append(pcs)
        others = tuple(against[k]) if against is not None and against[k] else ()
        tones = {pc for pcs in sets for pc in pcs}
        places = {pc: [p for p in range(low, top + 1) if p % 12 == pc] for pc in tones}
        blocked = {pc for pc in tones if places[pc] and all(any(_rubs(p, a) for a in others) for p in places[pc])}
        c0 = parse(symbol)
        c0_ivs = _chord_intervals(c0)
        thirds = {(c0["root"] + i) % 12 for i in (3, 4, 5) if i in c0_ivs}
        if blocked and not blocked & thirds and len(tones - blocked) >= 2:
            for r in range(voices):
                pcs = chord_tones(symbol, voices, r, 0, exclude=blocked - ({c0["root"]} if root else set()), keep_root=root)
                if sorted(pcs) not in [sorted(x) for x in sets]:
                    sets.append(pcs)
        c, used_rules = None, {}
        for rules in ({"against": others, "unisons": False}, {"against": others}, {}, {"limits": False}):
            c = next((found for pcs in sets if (found := candidates(pcs, low, top, max_gap, **rules))), None)
            if c:
                used_rules = rules
                break
        if not c:
            raise ValueError(f"No voicing of {symbol} in {voices} voices between {low} and {top}; widen range")
        if used_rules.get("limits") is False:
            warnings.warn(
                f"voice_lead: {symbol} (chord {k + 1}) fell back to unconstrained spacing between {low} and {top}.",
                GivenUp,
                stacklevel=2,
            )
        cands.append(np.array(c, dtype=float))

    centre = (low + high) / 2 if start is None else float(np.mean(start))
    drift = lambda c: DRIFT_COST * np.abs(c.mean(axis=1) - centre)
    cost = drift(cands[0])
    if start is not None:
        if len(start) != voices:
            raise ValueError(f"start has {len(start)} pitches for {voices} voices")
        cost = cost + np.abs(cands[0] - np.array(sorted(start), dtype=float)).sum(axis=1)

    back = []
    for a, b in zip(cands, cands[1:]):
        d = b[None, :, :] - a[:, None, :]
        step = np.abs(d)
        motion = step.sum(-1) + (TOP_WEIGHT - 1) * step[..., -1] + LEAP_COST * np.maximum(step - 7, 0).sum(-1)
        if avoid_parallels:
            motion = motion + PARALLEL_COST * _parallels(a, b, d)
        total = cost[:, None] + motion
        back.append(total.argmin(axis=0))
        cost = total.min(axis=0) + drift(b)

    idx = int(cost.argmin())
    path = [idx]
    for pointers in reversed(back):
        idx = int(pointers[idx])
        path.append(idx)
    path.reverse()
    return [[int(x) for x in cands[i][j]] for i, j in enumerate(path)]


def apply_voicings(track, voicings, beats=4.0, at=None, vel=85, strum=0.0, pedal=False, lift=0.05):
    """Write a sequence of MIDI pitch voicings onto a soundfont-music Track."""
    pos = track._end() if at is None else float(at)
    durations = [float(beats)] * len(voicings) if isinstance(beats, (int, float)) else [float(b) for b in beats]
    if len(durations) != len(voicings):
        raise ValueError("beats list length must match voicings length")
    for pitches, dur in zip(voicings, durations):
        if strum > 0 and len(pitches) > 1:
            track.strum(pitches, beats=dur, spread=strum, at=pos, vel=vel)
        else:
            for p in pitches:
                track.events.append((pos, dur, int(p) + track.transpose, int(vel), None))
            track._cursor = pos + dur
        if pedal and dur > lift * 2:
            track.pedal(pos, pos + dur - lift)
        pos += dur
    return track


def _drop_voices(notes, indices_from_top):
    """Drop specified 1-based positions from top down one octave and return sorted MIDI notes."""
    ordered = sorted(int(n) for n in notes)
    n = len(ordered)
    for k in indices_from_top:
        if 1 <= k <= n:
            ordered[n - k] -= 12
    return sorted(ordered)


def drop2(notes):
    """Drop the 2nd highest voice of a close-position chord down an octave."""
    return _drop_voices(notes, (2,))


def drop3(notes):
    """Drop the 3rd highest voice of a close-position chord down an octave."""
    return _drop_voices(notes, (3,))


def drop24(notes):
    """Drop the 2nd and 4th highest voices of a close-position chord down an octave."""
    return _drop_voices(notes, (2, 4))


def quartal_stack(root, voices=4, step_intervals=None, low=48):
    """Build a stack of fourths (or custom intervals) starting at or above `low`."""
    if step_intervals is None and voices <= 0:
        return []
    pc = harm._to_pc(root)
    start = low + ((pc - low) % 12)
    ivs = step_intervals if step_intervals is not None else (5,) * max(0, voices - 1)
    out = [start]
    for iv in ivs:
        out.append(out[-1] + int(iv))
    return out


def so_what_voicing(root, low=48):
    """Build a 5-note 'So What' chord (three P4s + top M3)."""
    return quartal_stack(root, voices=5, step_intervals=(5, 5, 5, 4), low=low)


def upper_structure_voicing(
    root="C", us_degree="II", triad_quality="maj", shell="37", bass_octave=3, upper_octave=4, include_root=True
):
    """Arrange an upper-structure triad cleanly above a root + 3rd/7th guide-tone shell."""
    us = harm.upper_structure_triad(root, us_degree=us_degree, triad_quality=triad_quality, shell=shell)
    r = us["root"]
    bass_midi = (bass_octave + 1) * 12 + r
    shell_notes = [bass_midi] if include_root else []
    for spc in sorted(us["shell_pcs"], key=lambda p: (p - r) % 12):
        shell_notes.append(bass_midi + ((spc - r) % 12))
    shell_notes.sort()
    min_upper = max(max(shell_notes) + 3, (upper_octave + 1) * 12)
    u_root = us["upper_root"]
    u_base = min_upper + ((u_root - min_upper) % 12)
    triad_ivs = harm._TRIAD_IVS[triad_quality]
    upper_notes = [u_base + iv for iv in triad_ivs]
    return {"shell": shell_notes, "upper": upper_notes, "all": shell_notes + upper_notes}
