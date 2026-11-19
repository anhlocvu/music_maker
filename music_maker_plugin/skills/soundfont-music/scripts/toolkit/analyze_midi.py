"""Analyze all MIDI files and multi-track MIDI project folders in the plugin's midi/ directory.

Usage:
    python analyze_midi.py                  # scans plugin's midi/ folder automatically
    python analyze_midi.py path/to/midi     # scans a custom file or folder
    python analyze_midi.py --json           # outputs JSON instead of Markdown
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from engine.midi_io import discover_midi_sources, parse_midi_file, summarize_track


def default_midi_dir():
    """Locate the plugin's midi/ folder, or fallback to local ./midi."""
    env_dir = os.environ.get("MUSIC_MAKER_MIDI_DIR")
    if env_dir and os.path.exists(env_dir):
        return env_dir
    # .../music_maker_plugin/skills/soundfont-music/scripts/toolkit -> .../music_maker_plugin/midi
    plugin_midi = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "midi"))
    if os.path.exists(plugin_midi):
        return plugin_midi
    return os.path.join(HERE, "midi")


def analyze_directory(target_path):
    """Analyze every discovered MIDI file and project folder under target_path."""
    groups = discover_midi_sources(target_path)
    results = []
    for group in groups:
        file_reports = []
        for fpath in group["files"]:
            parsed = parse_midi_file(fpath)
            rel_path = os.path.relpath(fpath, target_path) if os.path.isdir(target_path) else os.path.basename(fpath)
            track_summaries = [
                summarize_track(tr, beats_per_bar=parsed["beats_per_bar"], file_name=parsed["file_name"])
                for tr in parsed["tracks"]
            ]
            file_reports.append({
                "file_name": parsed["file_name"],
                "relative_path": rel_path.replace("\\", "/"),
                "bpm": parsed["bpm"],
                "time_signature": parsed["time_signature"],
                "total_beats": parsed["total_beats"],
                "total_bars": parsed["total_bars"],
                "tracks": track_summaries,
            })
        results.append({
            "project": group["project"],
            "is_folder": group["is_folder"],
            "files": file_reports,
        })
    return results


def format_markdown(target_path, report):
    """Format analysis report as concise Markdown highlighting project and file names."""
    lines = [f"# MIDI Reference Library Analysis (`{target_path}`)", ""]
    if not report:
        lines.append("_Chưa có file `.mid` / `.midi` nào trong thư mục này._")
        return "\n".join(lines)

    for group in report:
        kind = "Multi-track Project Folder" if group["is_folder"] else "Single MIDI File"
        lines.append(f"## [{kind}] `{group['project']}`")
        lines.append("")
        for f in group["files"]:
            lines.append(
                f"### File: `{f['file_name']}` (`{f['relative_path']}`) — "
                f"BPM: **{f['bpm']}** | Time: **{f['time_signature']}** | "
                f"Length: **{f['total_bars']} bars** ({f['total_beats']} beats)"
            )
            if not f["tracks"]:
                lines.append("- _(Không có sự kiện nốt hoặc pedal)_")
            for tr in f["tracks"]:
                vel_lo, vel_hi = tr["velocity_range"]
                lines.append(
                    f"- **Track `{tr['name']}`** (ch={tr['channel']}, prog={tr['program']}:{tr['program_name']}, "
                    f"notes={tr['note_count']}, vel={vel_lo}..{vel_hi} avg {tr['velocity_avg']}, "
                    f"avg_notes/bar={tr['avg_notes_per_bar']})"
                )
                if tr["pedal_count"]:
                    lines.append(
                        f"  - Pedal CC64: {tr['pedal_count']} lần (giữ TB {tr['pedal_avg_beats']} beats)"
                    )
                if tr["pitchwheel_count"]:
                    lines.append(f"  - Pitch Bend events: {tr['pitchwheel_count']}")
                if tr["high_activity_bars"]:
                    lines.append(f"  - Bars nhiều hoạt động / Fill gợi ý: {tr['high_activity_bars']}")
                if tr.get("is_drum_hint"):
                    pieces = ", ".join(f"{name}({cnt})" for name, cnt in tr.get("drum_pieces", []))
                    lines.append(f"  - Drum pieces: {pieces or 'N/A'}")
                else:
                    pr = tr.get("pitch_range")
                    lines.append(
                        f"  - Range: {pr[0]}..{pr[1]} | Key ước lượng: {tr.get('estimated_key')} | "
                        f"Chords: rolled={tr.get('rolled_chords', 0)}, block={tr.get('block_chords', 0)}"
                    )
                    if tr.get("opening_notes"):
                        lines.append(f"  - Opening: {' '.join(tr['opening_notes'])}")
            lines.append("")
    return "\n".join(lines)


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv if not a.startswith("--")]
    target = args[0] if args else default_midi_dir()
    report = analyze_directory(target)
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_markdown(target, report))


if __name__ == "__main__":
    main(sys.argv[1:])
