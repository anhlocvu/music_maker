"""Score diagnostics for soundfont-music Songs (low intervals, vertical rubs, parallels, harmony, static loops)."""
from collections import defaultdict
import itertools

from . import harmony as harm, instruments
from .voicing import LOW_INTERVAL_LIMITS


def _is_drum(track):
    _, bank, _ = instruments.resolve(track.instrument)
    return bank >= 127 or "drum" in track.name.lower()


def _where(beat, bpb=4.0):
    bar = int(beat // bpb) + 1
    b = (beat % bpb) + 1.0
    return f"bar {bar} beat {b:g}"


def _active_events(song):
    pitched = []
    for tr in song.tracks:
        if _is_drum(tr):
            continue
        for start, dur, key, vel, _ in tr.events:
            pitched.append((tr.name, float(start), float(start + dur), int(key), int(vel)))
    return pitched


def review_song(song, harmony=None, allow_parallels=True, bpb=4.0):
    """Audit a Song's written notes and return structured musical review findings."""
    pitched = _active_events(song)
    rubs, low_mud, outside = [], [], []
    by_onset = defaultdict(list)
    for item in pitched:
        by_onset[round(item[1], 3)].append(item)

    # Check simultaneous / overlapping intervals across pitched tracks
    for i in range(len(pitched)):
        t1, s1, e1, k1, _ = pitched[i]
        for j in range(i + 1, len(pitched)):
            t2, s2, e2, k2, _ = pitched[j]
            if s2 >= e1 - 1e-6:
                continue
            overlap = min(e1, e2) - max(s1, s2)
            if overlap <= 1e-4:
                continue
            lo, hi = (k1, k2) if k1 <= k2 else (k2, k1)
            span = hi - lo
            if 1 <= span <= 16 and lo < LOW_INTERVAL_LIMITS.get(span, 0):
                low_mud.append({"at": _where(max(s1, s2), bpb), "tracks": (t1, t2), "pitches": (lo, hi), "semitones": span})
            if t1 != t2 and span in (1, 13) and overlap >= 0.5:
                rubs.append({"at": _where(max(s1, s2), bpb), "tracks": (t1, t2), "pitches": (lo, hi), "semitones": span})

    # Optional chord-timeline check on strong beats
    if harmony:
        sorted_h = sorted(harmony, key=lambda x: x[0])
        by_track = defaultdict(list)
        for tr_name, s, e, k, _ in pitched:
            by_track[tr_name].append((s, k))
        for tr_name, notes in by_track.items():
            notes.sort()
            for idx, (s, k) in enumerate(notes):
                if abs((s % 1.0)) > 1e-4:
                    continue
                ch = harm.chord_at(sorted_h, s)
                if ch is None or (k % 12) in ch["pcs"]:
                    continue
                nxt = notes[idx + 1][1] if idx + 1 < len(notes) else None
                if nxt is None or abs(nxt - k) > 2:
                    outside.append({"at": _where(s, bpb), "track": tr_name, "pitch": k, "chord": ch["symbol"]})

    # Parallel 5ths / 8ves between independent single-line pitched tracks
    parallels = []
    if not allow_parallels:
        lines = defaultdict(list)
        for tr_name, s, _, k, _ in pitched:
            lines[tr_name].append((round(s, 3), k))
        single_tracks = [n for n, evs in lines.items() if len({s for s, _ in evs}) == len(evs)]
        for a_name, b_name in itertools.combinations(single_tracks, 2):
            ma, mb = dict(lines[a_name]), dict(lines[b_name])
            common = sorted(set(ma) & set(mb))
            for t0, t1 in zip(common, common[1:]):
                iv0 = (mb[t0] - ma[t0]) % 12
                iv1 = (mb[t1] - ma[t1]) % 12
                da, db = ma[t1] - ma[t0], mb[t1] - mb[t0]
                if iv0 == iv1 and iv0 in (0, 7) and da != 0 and (da > 0) == (db > 0):
                    parallels.append({"at": _where(t1, bpb), "tracks": (a_name, b_name), "interval": "8ve" if iv0 == 0 else "5th"})

    # Static loop detection (>=16 consecutive identical 1-bar or 2-bar blocks)
    static_loops = []
    for tr in song.tracks:
        if tr.length() < 16 * bpb:
            continue
        bars = defaultdict(list)
        for s, dur, k, vel, _ in tr.events:
            bar_idx = int(s // bpb)
            bars[bar_idx].append((round(s - bar_idx * bpb, 3), round(dur, 3), k))
        max_bar = int(tr.length() // bpb)
        run = 1
        for b in range(1, max_bar):
            if sorted(bars[b]) == sorted(bars[b - 1]) and bars[b]:
                run += 1
                if run == 16:
                    static_loops.append({"track": tr.name, "from_bar": b - 14, "bars": run})
            else:
                run = 1

    lengths = {tr.name: round(tr.length(), 3) for tr in song.tracks}
    return {
        "title": song.title,
        "track_lengths_beats": lengths,
        "low_intervals": low_mud[:30],
        "vertical_rubs": rubs[:30],
        "outside_chord": outside[:30],
        "parallels": parallels[:30],
        "static_loops": static_loops,
    }


def format_review(report):
    """Format a `review_song` dict into a concise human-readable report."""
    lines = [f"# Score Review: {report['title']}"]
    for key in ("low_intervals", "vertical_rubs", "outside_chord", "parallels", "static_loops"):
        items = report.get(key, [])
        lines.append(f"- {key}: {len(items)}")
        for it in items[:8]:
            lines.append(f"    {it}")
    return "\n".join(lines)
