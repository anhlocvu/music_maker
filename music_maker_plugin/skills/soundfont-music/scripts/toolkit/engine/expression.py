"""Human player-like timing and velocity shaping for soundfont-music Tracks.

Implements linear phase correction (Vorberg/Wing/Repp), 1/f^beta long-range
correlated velocity wander (Raesanen et al.), KTH phrase arches, high-loud,
chord top-note lead/spread, and 2-bar cymbal accent cycles.
"""
import hashlib
import math

import numpy as np

from .sf2 import build_bend_curve as make_bend_curve

ROLE_DEFAULTS = {
    "melody": {"timing_sd": 6.0, "short_sd": 2.0, "vel_pct": 3.0, "high_loud": 0.3, "arch": 6.0, "spread": 0.0, "lead": 0.0, "gate_sd": 0.02},
    "countermelody": {"timing_sd": 6.0, "short_sd": 2.0, "vel_pct": 3.0, "high_loud": 0.2, "arch": 4.0, "spread": 8.0, "lead": 0.0, "gate_sd": 0.0},
    "harmony": {"timing_sd": 5.0, "short_sd": 2.0, "vel_pct": 3.0, "high_loud": 0.0, "arch": 4.0, "spread": 10.0, "lead": 10.0, "gate_sd": 0.0},
    "texture": {"timing_sd": 5.0, "short_sd": 2.0, "vel_pct": 4.0, "high_loud": 0.0, "arch": 3.0, "spread": 6.0, "lead": 6.0, "gate_sd": 0.03},
    "rhythm": {"timing_sd": 4.0, "short_sd": 1.5, "vel_pct": 3.0, "high_loud": 0.0, "arch": 3.0, "spread": 0.0, "lead": 0.0, "gate_sd": 0.03},
    "bass": {"timing_sd": 3.5, "short_sd": 1.5, "feel": 4.0, "vel_pct": 3.0, "high_loud": 0.0, "arch": 3.0, "spread": 0.0, "lead": 0.0, "gate_sd": 0.02},
    "drums": {"timing_sd": 2.5, "short_sd": 1.5, "vel_pct": 3.0, "high_loud": 0.0, "arch": 0.0, "spread": 0.0, "lead": 0.0, "gate_sd": 0.0, "cymbal_cycle": 4.0},
}
BASE = {"timing_sd": 0.0, "short_sd": 0.0, "feel": 0.0, "vel_pct": 0.0, "high_loud": 0.0, "arch": 0.0, "spread": 0.0, "lead": 0.0, "gate_sd": 0.0, "cymbal_cycle": 0.0, "beta": 0.8, "correction": 0.4}
CYMBALS = {42, 44, 46, 51, 53, 59}
GRID = 4


def _rng(seed, name):
    digest = hashlib.sha256(f"{seed}:{name}".encode("utf-8")).hexdigest()[:12]
    return np.random.default_rng(int(digest, 16))


def kept_to_the_beat(n, rng, share=0.4, per_beat=1):
    """Linear phase-correction timing curve centered at 0 with unit std."""
    if not 0 < share <= 1:
        raise ValueError(f"correction must be in (0, 1], got {share!r}")
    if n < 2:
        return np.zeros(n)
    e = rng.standard_normal(n)
    x = np.empty(n)
    x[0] = e[0]
    kept = (1.0 - share) ** (1.0 / per_beat)
    scale = math.sqrt(max(0.0, 1.0 - kept * kept))
    for i in range(1, n):
        x[i] = kept * x[i - 1] + scale * e[i]
    x -= x.mean()
    std = x.std()
    return x / std if std > 0 else x


def lrc_noise(n, rng, beta=0.8):
    """Long-range correlated 1/f^beta loudness drift, zero mean, unit std."""
    if n < 2:
        return np.zeros(n)
    m = 1 << (n - 1).bit_length()
    f = np.arange(m // 2 + 1, dtype=float)
    spec = (rng.standard_normal(len(f)) + 1j * rng.standard_normal(len(f))) / np.maximum(f, 1.0) ** (beta / 2.0)
    spec[0] = 0.0
    x = np.fft.irfft(spec, n=m)[:n]
    x -= x.mean()
    std = x.std()
    return x / std if std > 0 else x


def _arch_shape(pos):
    return math.sin(math.pi * min(1.0, max(0.0, pos)) ** 1.357) - 0.5


def humanize_track(track, role="texture", seed=1, overrides=None, bpm=None):
    """Apply deterministic player-like timing, velocity, and gate variation to a Track."""
    if not track.events:
        return {"notes": 0, "timing_sd_ms": 0.0}
    prof = {**BASE, **ROLE_DEFAULTS.get(role, ROLE_DEFAULTS["texture"]), **(overrides or {})}
    tempo = float(bpm if bpm is not None else getattr(track.song, "bpm", 120.0))
    ms_per_beat = 60000.0 / tempo

    indexed = sorted(enumerate(track.events), key=lambda item: (item[1][0], item[1][2]))
    onsets = sorted({round(ev[0], 6) for _, ev in indexed})
    span = max(1, int(math.floor(onsets[-1] * GRID + 1e-9)) + 1)

    rng = _rng(seed, track.name)
    slow_t = kept_to_the_beat(span, rng, prof["correction"], GRID)
    slow_v = lrc_noise(span, rng, prof["beta"])
    gates = kept_to_the_beat(span, rng, prof["correction"], GRID)
    cycle = rng.uniform(-1.0, 1.0, 16)
    slot = {o: min(span - 1, max(0, int(round(o * GRID)))) for o in onsets}
    fast_t = {o: float(_rng(seed, f"{track.name}:short:{int(round(o * 1_000_000))}").standard_normal()) for o in onsets}

    mean_pitch = sum(ev[2] for _, ev in indexed) / len(indexed)
    by_onset = {}
    for idx, ev in indexed:
        by_onset.setdefault(round(ev[0], 6), []).append((idx, ev))

    new_events = list(track.events)
    moved_ms = []
    for o, group in by_onset.items():
        k = slot[o]
        shared_ms = prof["feel"] + prof["timing_sd"] * slow_t[k] + prof["short_sd"] * fast_t[o]
        group.sort(key=lambda item: item[1][2])
        for j, (orig_idx, (start, dur, key, vel, bend)) in enumerate(group):
            dt_ms = shared_ms
            if len(group) > 1:
                if prof["lead"] and j == len(group) - 1:
                    dt_ms -= prof["lead"]
                elif prof["spread"]:
                    dt_ms += float(_rng(seed, f"{track.name}:spread:{orig_idx}").uniform(-prof["spread"], prof["spread"]))
            dt_ms = max(-80.0, min(80.0, dt_ms))
            moved_ms.append(dt_ms)

            new_start = max(0.0, start + dt_ms / ms_per_beat)
            v = vel * (1.0 + prof["vel_pct"] / 100.0 * slow_v[k])
            if prof["arch"]:
                phrase_pos = (start % 16.0) / 16.0
                v += prof["arch"] * _arch_shape(phrase_pos)
            if prof["high_loud"]:
                v += max(-6.0, min(6.0, prof["high_loud"] * (key - mean_pitch)))
            if prof["cymbal_cycle"] and key in CYMBALS:
                v += prof["cymbal_cycle"] * cycle[int(round(start * 2.0)) % 16]
            new_vel = int(max(1, min(127, round(v))))

            new_dur = dur
            if prof["gate_sd"]:
                new_dur = max(0.05, dur * max(0.3, min(1.4, 1.0 + prof["gate_sd"] * gates[k])))
            new_events[orig_idx] = (new_start, new_dur, key, new_vel, bend)

    track.events = new_events
    return {"notes": len(new_events), "timing_sd_ms": round(float(np.std(moved_ms)), 2)}


def humanize_song(song, roles=None, overrides=None, seed=1):
    """Apply `humanize_track` across a Song using `{track_name: role}` mapping."""
    roles = roles or {}
    overrides = overrides or {}
    report = {}
    for tr in song.tracks:
        if tr.name in overrides and overrides[tr.name] is None:
            continue
        role = roles.get(tr.name, "drums" if "drum" in tr.name.lower() else "bass" if "bass" in tr.name.lower() else "texture")
        report[tr.name] = humanize_track(tr, role=role, seed=seed, overrides=overrides.get(tr.name), bpm=song.bpm)
    return report


_ROLE_BEND_STYLES = {
    "guitar": ("bend_release", "delayed_bend", "bend_vibrato", "scoop", "dive"),
    "lead": ("bend_release", "delayed_bend", "bend_vibrato", "scoop"),
    "bass": ("delayed_bend", "dive", "scoop"),
    "strings": ("scoop", "bend_vibrato", "delayed_bend"),
    "synth": ("scoop", "bend_release", "bend_vibrato"),
}


def expressive_bends(track, role="lead", seed=1, max_semi=2.0, min_dur=0.75, intensity=0.7):
    """Enrich sustained or phrase-peak notes on `track` with natural pitch-bend curves.

    Never overwrites notes that already have an explicit `bend`. Returns a summary dict.
    """
    if not track.events:
        return {"notes": 0, "bends_added": 0}

    rng = _rng(seed, f"{track.name}:bends")
    styles = _ROLE_BEND_STYLES.get(role, _ROLE_BEND_STYLES["lead"])
    cap = max(0.25, float(max_semi))
    prob = max(0.0, min(1.0, float(intensity)))
    indexed = sorted(enumerate(track.events), key=lambda item: (item[1][0], item[1][2]))

    new_events = list(track.events)
    added = 0
    for pos_idx, (orig_idx, (start, dur, key, vel, bend)) in enumerate(indexed):
        if bend is not None:
            continue
        prev_key = indexed[pos_idx - 1][1][2] if pos_idx > 0 else key
        next_key = indexed[pos_idx + 1][1][2] if pos_idx + 1 < len(indexed) else key
        is_peak = key > prev_key and key >= next_key
        effective_min = min_dur * (0.65 if is_peak else 1.0)
        if dur < effective_min:
            continue
        if float(rng.random()) > (0.95 if is_peak and dur >= min_dur else prob):
            continue

        style = styles[int(rng.integers(0, len(styles)))]
        if style == "bend_vibrato":
            semis = round(min(cap, 0.35 + 0.35 * float(rng.random())), 2)
            waves = 3 if dur >= 1.5 else 2
        elif style == "scoop":
            semis = round(min(cap, 0.5 if role == "strings" else 1.0), 2)
            waves = 2
        elif role == "bass":
            semis = round(min(cap, 1.0 if dur < 2.0 else 2.0), 2)
            waves = 2
        else:
            semis = round(min(cap, 2.0 if (dur >= 1.5 and is_peak) else 1.0), 2)
            waves = 3

        curve = make_bend_curve(style=style, semis=semis, smooth=True, vibrato_waves=waves)
        new_events[orig_idx] = (start, dur, key, vel, curve)
        added += 1

    track.events = new_events
    return {"notes": len(new_events), "bends_added": added}
