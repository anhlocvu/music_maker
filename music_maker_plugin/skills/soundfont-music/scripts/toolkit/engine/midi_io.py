"""MIDI reading, musical analysis, and Track import helpers using mido."""
from collections import Counter, defaultdict
import os

from . import instruments

NOTE_NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
DRUM_LABELS = {
    35: "kick2", 36: "kick", 37: "rim", 38: "snare", 39: "clap", 40: "snare2",
    41: "tom_low2", 42: "hat", 43: "tom4", 44: "phat", 45: "tom3", 46: "ohat",
    47: "tom2", 48: "tom_hi2", 49: "crash", 50: "tom1", 51: "ride", 52: "china",
    53: "ride_bell", 54: "tamb", 55: "splash", 56: "cowbell", 57: "crash2",
    70: "shaker", 81: "triangle",
}
GM_PROGRAM_NAMES = {v: k for k, v in instruments.GM.items()}

MAJOR_PROFILE = (6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88)
MINOR_PROFILE = (6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17)


def key_to_name(key):
    """Convert MIDI note number (0..127) to pitch name like 'C4'."""
    octave = (key // 12) - 1
    return f"{NOTE_NAMES[key % 12]}{octave}"


def _build_tempo_map(mid):
    """Collect sorted (abs_tick, tempo_us) pairs across all tracks."""
    changes = []
    for track in mid.tracks:
        tick = 0
        for msg in track:
            tick += msg.time
            if msg.type == "set_tempo":
                changes.append((tick, msg.tempo))
    changes.sort(key=lambda item: item[0])
    return changes or [(0, 500000)]


def _extract_time_signature(mid):
    """Return first (numerator, denominator) time signature found, defaulting to 4/4."""
    for track in mid.tracks:
        for msg in track:
            if msg.type == "time_signature":
                return msg.numerator, msg.denominator
    return 4, 4


def parse_midi_file(path):
    """Parse a .mid/.midi file into structured per-track musical events and metadata."""
    import mido

    mid = mido.MidiFile(path)
    tpb = mid.ticks_per_beat or 480
    tempo_map = _build_tempo_map(mid)
    bpm = round(mido.tempo2bpm(tempo_map[0][1]), 2)
    ts_num, ts_den = _extract_time_signature(mid)
    beats_per_bar = ts_num * (4.0 / ts_den)

    parsed_tracks = []
    max_beat = 0.0

    for idx, mtrack in enumerate(mid.tracks):
        tick = 0
        track_name = mtrack.name.strip() if getattr(mtrack, "name", "") else ""
        channels = Counter()
        programs = {}
        active = defaultdict(list)  # (channel, note) -> [(start_tick, vel)]
        pedal_down = {}             # channel -> start_tick
        notes = []                  # (start_beat, dur_beats, key, vel, None)
        pedals = []                 # (start_beat, end_beat)
        pitchwheel_count = 0

        for msg in mtrack:
            tick += msg.time
            if msg.type == "track_name" and not track_name:
                track_name = msg.name.strip()
            elif msg.type == "program_change":
                programs[msg.channel] = msg.program
            elif msg.type == "pitchwheel":
                pitchwheel_count += 1
            elif msg.type == "control_change" and msg.control == 64:
                ch = msg.channel
                if msg.value >= 64 and ch not in pedal_down:
                    pedal_down[ch] = tick
                elif msg.value < 64 and ch in pedal_down:
                    s_beat = pedal_down.pop(ch) / tpb
                    e_beat = tick / tpb
                    if e_beat > s_beat:
                        pedals.append((s_beat, e_beat))
            elif msg.type == "note_on" and msg.velocity > 0:
                channels[msg.channel] += 1
                active[(msg.channel, msg.note)].append((tick, msg.velocity))
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                key_id = (msg.channel, msg.note)
                if active[key_id]:
                    s_tick, vel = active[key_id].pop(0)
                    dur = max(1 / tpb, (tick - s_tick) / tpb)
                    notes.append((s_tick / tpb, dur, msg.note, vel, None))

        for (ch, note_num), queue in active.items():
            for s_tick, vel in queue:
                dur = max(0.25, (tick - s_tick) / tpb)
                notes.append((s_tick / tpb, dur, note_num, vel, None))

        for ch, s_tick in pedal_down.items():
            if tick > s_tick:
                pedals.append((s_tick / tpb, tick / tpb))

        if not notes and not pedals:
            continue

        notes.sort(key=lambda e: (e[0], e[2]))
        pedals.sort()
        track_end = max(
            max((s + d for s, d, _, _, _ in notes), default=0.0),
            max((e for _, e in pedals), default=0.0),
        )
        max_beat = max(max_beat, track_end)
        primary_ch = channels.most_common(1)[0][0] if channels else 0
        prog = programs.get(primary_ch, 0)
        is_drum = primary_ch == 9

        parsed_tracks.append({
            "index": idx,
            "name": track_name or f"Track_{idx}",
            "channel": primary_ch,
            "program": prog,
            "program_name": "drums" if is_drum else GM_PROGRAM_NAMES.get(prog, f"program_{prog}"),
            "is_drum": is_drum,
            "notes": notes,
            "pedals": pedals,
            "pitchwheel_count": pitchwheel_count,
        })

    return {
        "path": os.path.abspath(path),
        "file_name": os.path.basename(path),
        "bpm": bpm,
        "time_signature": f"{ts_num}/{ts_den}",
        "beats_per_bar": beats_per_bar,
        "ticks_per_beat": tpb,
        "total_beats": round(max_beat, 3),
        "total_bars": round(max_beat / beats_per_bar, 2) if beats_per_bar else 0.0,
        "tracks": parsed_tracks,
    }


def estimate_key(notes):
    """Estimate musical key (e.g. 'C major' / 'A minor') from note durations."""
    if not notes:
        return None
    weights = [0.0] * 12
    for _, dur, key, vel, _ in notes:
        weights[key % 12] += dur * (vel / 127.0)
    total = sum(weights)
    if total <= 0:
        return None

    best_score, best_name = float("-inf"), None
    for root in range(12):
        rotated = weights[root:] + weights[:root]
        maj = sum(w * p for w, p in zip(rotated, MAJOR_PROFILE))
        min_s = sum(w * p for w, p in zip(rotated, MINOR_PROFILE))
        if maj > best_score:
            best_score, best_name = maj, f"{NOTE_NAMES[root]} major"
        if min_s > best_score:
            best_score, best_name = min_s, f"{NOTE_NAMES[root]} minor"
    return best_name


def _detect_rolled_chords(notes, max_gap=0.15):
    """Count chord clusters whose notes start slightly staggered (arpeggio/strum feel)."""
    if len(notes) < 3:
        return 0, 0
    rolled, block = 0, 0
    i = 0
    while i < len(notes):
        start_0 = notes[i][0]
        group = [notes[i]]
        j = i + 1
        while j < len(notes) and notes[j][0] - notes[j - 1][0] <= max_gap and notes[j][0] - start_0 <= 0.4:
            group.append(notes[j])
            j += 1
        if len(group) >= 3:
            spread = group[-1][0] - group[0][0]
            if spread >= 0.015:
                rolled += 1
            else:
                block += 1
        i = j if j > i + 1 else i + 1
    return rolled, block


def summarize_track(track_data, beats_per_bar=4.0, file_name=""):
    """Build a concise musical summary dict for one parsed MIDI track."""
    notes = track_data["notes"]
    pedals = track_data["pedals"]
    vels = [n[3] for n in notes]
    keys = [n[2] for n in notes]

    bar_counts = Counter()
    for start, _, _, _, _ in notes:
        bar_idx = int(start // beats_per_bar) + 1
        bar_counts[bar_idx] += 1

    avg_density = (sum(bar_counts.values()) / len(bar_counts)) if bar_counts else 0.0
    fill_bars = sorted(b for b, c in bar_counts.items() if avg_density > 0 and c >= max(avg_density * 1.45, avg_density + 4))

    name_hint = f"{file_name} {track_data['name']}".lower()
    looks_like_drum = track_data["is_drum"] or any(
        tok in name_hint for tok in ("drum", "kit", "perc", "kick", "snare", "hat", "beat")
    )

    summary = {
        "name": track_data["name"],
        "channel": track_data["channel"],
        "program": track_data["program"],
        "program_name": track_data["program_name"],
        "is_drum_hint": looks_like_drum,
        "note_count": len(notes),
        "velocity_range": (min(vels), max(vels)) if vels else (0, 0),
        "velocity_avg": round(sum(vels) / len(vels), 1) if vels else 0.0,
        "pedal_count": len(pedals),
        "pedal_avg_beats": round(sum(e - s for s, e in pedals) / len(pedals), 2) if pedals else 0.0,
        "pitchwheel_count": track_data["pitchwheel_count"],
        "avg_notes_per_bar": round(avg_density, 1),
        "high_activity_bars": fill_bars[:12],
    }

    if looks_like_drum:
        pieces = Counter(DRUM_LABELS.get(k, key_to_name(k)) for k in keys)
        summary["drum_pieces"] = pieces.most_common(12)
    else:
        summary["pitch_range"] = (key_to_name(min(keys)), key_to_name(max(keys))) if keys else None
        summary["estimated_key"] = estimate_key(notes)
        rolled, block = _detect_rolled_chords(notes)
        summary["rolled_chords"] = rolled
        summary["block_chords"] = block
        # Sample opening motif (first 12 notes)
        summary["opening_notes"] = [
            f"{key_to_name(k)}@{round(s, 2)}" for s, _, k, _, _ in notes[:12]
        ]

    return summary


def _find_project_readme(project_dir):
    """Find a readme.md file (case-insensitive) inside a MIDI project folder."""
    if not os.path.isdir(project_dir):
        return None
    for entry in sorted(os.listdir(project_dir)):
        full = os.path.join(project_dir, entry)
        if os.path.isfile(full) and entry.lower() == "readme.md":
            return os.path.abspath(full)
    for walk_root, dirs, files in os.walk(project_dir):
        dirs.sort()
        for fname in sorted(files):
            if fname.lower() == "readme.md":
                return os.path.abspath(os.path.join(walk_root, fname))
    return None


def read_project_readme(readme_path):
    """Read the full text content of a project's readme.md safely."""
    if not readme_path or not os.path.isfile(readme_path):
        return None
    for enc in ("utf-8-sig", "utf-8"):
        try:
            with open(readme_path, "r", encoding=enc) as fh:
                return fh.read().strip()
        except UnicodeDecodeError:
            continue
    with open(readme_path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().strip()


def _collect_midi_files(folder):
    """Collect all .mid/.midi files under folder sorted deterministically."""
    midi_files = []
    for walk_root, dirs, files in os.walk(folder):
        dirs.sort()
        for fname in sorted(files):
            if fname.lower().endswith((".mid", ".midi")):
                midi_files.append(os.path.abspath(os.path.join(walk_root, fname)))
    return midi_files


def discover_midi_sources(root_dir):
    """Discover MIDI project folders (and fallback single MIDI files) under root_dir.

    Returns a list of groups:
      [{"project": "<name>", "is_folder": bool, "files": [abs_path, ...], "readme_path": str|None}]
    """
    if not os.path.exists(root_dir):
        return []
    if os.path.isfile(root_dir):
        return [{
            "project": os.path.basename(root_dir),
            "is_folder": False,
            "files": [os.path.abspath(root_dir)],
            "readme_path": None,
        }]

    abs_root = os.path.abspath(root_dir)
    entries = sorted(os.listdir(abs_root))

    # Subfolders representing MIDI projects (e.g. midi/ballad beat/)
    project_groups = []
    for entry in entries:
        full = os.path.join(abs_root, entry)
        if not os.path.isdir(full):
            continue
        midi_files = _collect_midi_files(full)
        if midi_files:
            project_groups.append({
                "project": entry,
                "is_folder": True,
                "files": midi_files,
                "readme_path": _find_project_readme(full),
            })

    # Top-level MIDI files directly inside root_dir
    top_midis = [
        os.path.abspath(os.path.join(abs_root, entry))
        for entry in entries
        if os.path.isfile(os.path.join(abs_root, entry)) and entry.lower().endswith((".mid", ".midi"))
    ]

    # If user pointed directly at a single project folder (no project subfolders)
    if not project_groups and top_midis:
        root_readme = _find_project_readme(abs_root)
        if root_readme is not None or len(top_midis) > 1 or os.path.basename(abs_root).lower() != "midi":
            return [{
                "project": os.path.basename(abs_root),
                "is_folder": True,
                "files": top_midis,
                "readme_path": root_readme,
            }]

    groups = list(project_groups)
    for fpath in top_midis:
        groups.append({
            "project": os.path.basename(fpath),
            "is_folder": False,
            "files": [fpath],
            "readme_path": None,
        })
    return groups


def load_midi_into_track(song, name, midi_path, instrument, track_index=0, **track_kw):
    """Import notes and CC64 sustain pedals from a MIDI file into a new Song Track."""
    parsed = parse_midi_file(midi_path)
    if not parsed["tracks"]:
        raise ValueError(f"No note or pedal events found in {midi_path}")
    src = parsed["tracks"][track_index]
    track = song.track(name, instrument, **track_kw)
    track.events.extend(src["notes"])
    track.pedals.extend(src["pedals"])
    track._cursor = track.length()
    return track
