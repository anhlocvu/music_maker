"""Analyze all MIDI project folders (and any MIDI files) in the plugin's midi/ directory.

Usage:
    python analyze_midi.py                  # scans plugin's midi/ folder automatically
    python analyze_midi.py path/to/midi     # scans a custom MIDI library or project folder
    python analyze_midi.py --json           # outputs JSON instead of Markdown
"""
from collections import defaultdict
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from engine.midi_io import (
    discover_midi_sources,
    parse_midi_file,
    read_project_readme,
    summarize_track,
)


def _markdown_fence(text):
    """Return a backtick fence longer than any backtick run in text."""
    longest = max((len(m.group(0)) for m in re.finditer(r"`+", text)), default=2)
    return "`" * max(3, longest + 1)


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
    """Analyze every discovered MIDI project folder (and any fallback MIDI files) under target_path."""
    groups = discover_midi_sources(target_path)
    results = []
    for group in groups:
        file_reports = []
        for fpath in group["files"]:
            parsed = parse_midi_file(fpath)
            rel_path = os.path.relpath(fpath, target_path) if os.path.isdir(target_path) else os.path.basename(fpath)
            track_summaries = [
                summarize_track(
                    tr,
                    beats_per_bar=parsed["beats_per_bar"],
                    file_name=parsed["file_name"],
                    bpm=parsed["bpm"],
                )
                for tr in parsed["tracks"]
            ]
            file_reports.append({
                "file_name": parsed["file_name"],
                "relative_path": rel_path.replace("\\", "/"),
                "bpm": parsed["bpm"],
                "time_signature": parsed["time_signature"],
                "beats_per_bar": parsed["beats_per_bar"],
                "total_beats": parsed["total_beats"],
                "total_bars": parsed["total_bars"],
                "tracks": track_summaries,
            })

        readme_abs = group.get("readme_path")
        readme_rel = None
        if readme_abs:
            readme_rel = (
                os.path.relpath(readme_abs, target_path).replace("\\", "/")
                if os.path.isdir(target_path)
                else os.path.basename(readme_abs)
            )
        readme_text = read_project_readme(readme_abs)

        results.append({
            "project": group["project"],
            "is_folder": group["is_folder"],
            "readme_file": os.path.basename(readme_abs) if readme_abs else None,
            "readme_path": readme_rel,
            "readme": readme_text,
            "files": file_reports,
        })
    return results


def _format_note_token(n):
    """Format one note with duration, velocity, and optional inline pedal/bend tags."""
    attrs = [f"d={n['dur_beats']}", f"v={n['vel']}"]
    if n.get("ped"):
        attrs.append("ped")
    if n.get("bend"):
        attrs.append(f"bend={n['bend']}")
    return f"@{n['start_beat']} {n['note']}({','.join(attrs)})"


def format_markdown(target_path, report):
    """Format analysis report as Markdown with Project README first and inline note bends."""
    lines = [f"# MIDI Reference Library Analysis (`{target_path}`)", ""]
    if not report:
        lines.append("_Chưa có project MIDI hoặc file `.mid` / `.midi` nào trong thư mục này._")
        return "\n".join(lines)

    for group in report:
        kind = "MIDI Project" if group["is_folder"] else "MIDI File"
        lines.append(f"## [{kind}] `{group['project']}`")
        lines.append("")
        if group["is_folder"]:
            readme_label = group.get("readme_path") or "readme.md"
            readme_body = group.get("readme")
            lines.append(f"### Project README (`{readme_label}`)")
            if readme_body is None:
                lines.append("_No readme.md found in this project folder._")
            elif not readme_body:
                lines.append("_(Empty readme.md)_")
            else:
                fence = _markdown_fence(readme_body)
                lines.append(f"{fence}markdown")
                lines.append(readme_body)
                lines.append(fence)
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
                    f"notes={tr['note_count']}, vel={vel_lo}..{vel_hi} avg {tr['velocity_avg']} std {tr.get('velocity_std', 0)}, "
                    f"ghost<60={round(tr.get('ghost_note_ratio', 0) * 100, 1)}%, "
                    f"micro_offset={tr.get('micro_timing_avg_abs_offset_beats', 0)}b, "
                    f"avg_notes/bar={tr['avg_notes_per_bar']})"
                )
                if tr["pedal_count"]:
                    lines.append(
                        f"  - Pedal CC64: {tr['pedal_count']} lần (giữ TB {tr['pedal_avg_beats']} beats; đánh dấu `ped` trên nốt)"
                    )
                if tr.get("bent_note_count") or tr["pitchwheel_count"]:
                    lines.append(
                        f"  - Pitch Bend: {tr.get('bent_note_count', 0)} nốt có bend "
                        f"(range ±{tr.get('bend_range_semitones', 2.0)} st; gắn trực tiếp `bend=...` trên từng nốt)"
                    )
                if tr["high_activity_bars"]:
                    lines.append(f"  - Bars nhiều hoạt động / Fill gợi ý: {tr['high_activity_bars']}")
                if tr.get("is_drum_hint"):
                    pieces = ", ".join(f"{name}({cnt})" for name, cnt in tr.get("drum_pieces", []))
                    lines.append(f"  - Drum pieces: {pieces or 'N/A'}")
                else:
                    pr = tr.get("pitch_range")
                    pr_text = f"{pr[0]}..{pr[1]}" if pr else "N/A"
                    lines.append(
                        f"  - Range: {pr_text} | Key ước lượng: {tr.get('estimated_key')} | "
                        f"Chords: rolled={tr.get('rolled_chords', 0)}, block={tr.get('block_chords', 0)}"
                    )

                all_notes = tr.get("notes", [])
                if all_notes:
                    bpb = f.get("beats_per_bar", 4.0)
                    by_bar = defaultdict(list)
                    for n in all_notes:
                        by_bar[n["bar"]].append(n)
                    lines.append(f"  - **All Notes ({len(all_notes)})**:")
                    for bar_num in sorted(by_bar):
                        bar_start = round((bar_num - 1) * bpb, 3)
                        bar_end = round(bar_num * bpb, 3)
                        tokens = " | ".join(_format_note_token(n) for n in by_bar[bar_num])
                        lines.append(f"    - Bar {bar_num} ({bar_start}..{bar_end}): {tokens}")
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
