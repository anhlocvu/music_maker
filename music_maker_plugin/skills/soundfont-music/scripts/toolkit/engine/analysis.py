"""Quantitative NumPy audio/stem QA: K-weighted loudness, 6-band balance, spectral slope & mono check."""
import json
import math
from pathlib import Path
import wave

import numpy as np

BANDS = [
    ("sub_20_60", 20.0, 60.0),
    ("bass_60_250", 60.0, 250.0),
    ("low_mid_250_800", 250.0, 800.0),
    ("mid_800_2500", 800.0, 2500.0),
    ("presence_2500_6000", 2500.0, 6000.0),
    ("air_6000_16000", 6000.0, 16000.0),
]


def _read_wav(path):
    with wave.open(str(path), "rb") as wf:
        sr = wf.getframerate()
        ch = wf.getnchannels()
        sw = wf.getsampwidth()
        raw = wf.readframes(wf.getnframes())
    if sw == 2:
        arr = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    elif sw == 4:
        arr = np.frombuffer(raw, dtype="<i4").astype(np.float64) / 2147483648.0
    else:
        raise ValueError(f"Unsupported sample width {sw} in {path}")
    arr = arr.reshape(-1, ch)
    if ch == 1:
        arr = np.repeat(arr, 2, axis=1)
    return arr, sr


def _k_weight_response(n, sr):
    """BS.1770-style K-weighting magnitude-squared approximation valid at `sr`."""
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    # High-shelf (+4 dB above ~1.5 kHz) + 2nd-order RLB high-pass (~38 Hz)
    f_shelf = 1500.0
    f_hp = 38.0
    shelf = 1.0 + 0.5849 * (freqs / f_shelf) ** 2 / (1.0 + (freqs / f_shelf) ** 2)
    hp = (freqs / f_hp) ** 2 / np.sqrt((1.0 - (freqs / f_hp) ** 2) ** 2 + (math.sqrt(2) * freqs / f_hp) ** 2 + 1e-12)
    return shelf * hp


def _k_weighted_lufs(arr, sr):
    if len(arr) < 2:
        return -120.0
    n = 1 << (len(arr) - 1).bit_length()
    h = _k_weight_response(n, sr)[:, None]
    spec = np.fft.rfft(arr, n=n, axis=0) * h
    y = np.fft.irfft(spec, n=n, axis=0)[: len(arr)]
    power = float(np.mean(y ** 2, axis=0).sum())
    return round(-0.691 + 10.0 * math.log10(max(power, 1e-20)), 2)


def _find_tonal_references():
    here = Path(__file__).resolve()
    for p in (
        here.parents[1] / "assets" / "tonal-references.json",
        here.parents[4] / "mixing-timbre-mastering" / "assets" / "tonal-references.json",
    ):
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8")).get("references", {})
    return {}


def analyze_wav(path_or_array, sr=44100, reference_genre=None):
    """Return quantitative acoustic metrics for a stereo WAV path or array."""
    if isinstance(path_or_array, (str, Path)):
        arr, sr = _read_wav(path_or_array)
    else:
        arr = np.asarray(path_or_array, dtype=np.float64)
        if arr.ndim == 1:
            arr = np.stack([arr, arr], axis=1)

    peak = float(np.abs(arr).max()) if len(arr) else 0.0
    rms = float(np.sqrt(np.mean(arr ** 2))) if len(arr) else 0.0
    crest_db = round(20.0 * math.log10(max(peak, 1e-12) / max(rms, 1e-12)), 2) if rms > 0 else 0.0
    dc = float(np.abs(np.mean(arr, axis=0)).max()) if len(arr) else 0.0

    l, r = arr[:, 0], arr[:, 1]
    denom = float(np.sqrt(np.sum(l ** 2) * np.sum(r ** 2)))
    lr_corr = round(float(np.sum(l * r) / denom), 4) if denom > 1e-12 else 1.0
    mono = 0.5 * (l + r)
    mono_rms = float(np.sqrt(np.mean(mono ** 2)))
    mono_delta_db = round(20.0 * math.log10(max(mono_rms, 1e-12) / max(rms, 1e-12)), 2) if rms > 0 else 0.0

    # Spectral power across 6 bands + slope 100 Hz - 4 kHz
    mono_win = mono * np.hanning(len(mono)) if len(mono) > 16 else mono
    spec = np.abs(np.fft.rfft(mono_win)) ** 2
    freqs = np.fft.rfftfreq(len(mono_win), 1.0 / sr) if len(mono_win) else np.array([0.0])

    total_p = float(spec[(freqs >= 20.0) & (freqs <= 16000.0)].sum()) or 1e-20
    bands_pct = {
        name: round(float(spec[(freqs >= lo) & (freqs < hi)].sum()) / total_p * 100.0, 2)
        for name, lo, hi in BANDS
    }

    slope_mask = (freqs >= 100.0) & (freqs <= 4000.0) & (spec > 0)
    slope = 0.0
    if int(slope_mask.sum()) >= 4:
        x_oct = np.log2(freqs[slope_mask])
        y_db = 10.0 * np.log10(spec[slope_mask])
        slope = round(float(np.polyfit(x_oct, y_db, 1)[0]), 2)

    out = {
        "duration_s": round(len(arr) / float(sr), 3),
        "sample_rate": int(sr),
        "peak": round(peak, 5),
        "peak_db": round(20.0 * math.log10(max(peak, 1e-12)), 2),
        "rms_db": round(20.0 * math.log10(max(rms, 1e-12)), 2),
        "crest_db": crest_db,
        "dc_offset": round(dc, 6),
        "lr_correlation": lr_corr,
        "mono_fold_delta_db": mono_delta_db,
        "k_weighted_lufs": _k_weighted_lufs(arr, sr),
        "bands_pct": bands_pct,
        "spectral_slope_db_per_oct": slope,
    }
    if reference_genre:
        refs = _find_tonal_references()
        if reference_genre in refs:
            ref_slope = refs[reference_genre]["tonal_balance"]["slope_db_per_octave_100hz_4khz"]
            out["reference_genre"] = reference_genre
            out["reference_slope_db_per_oct"] = ref_slope
            out["slope_diff_db_per_oct"] = round(slope - ref_slope, 2)
    return out


def analyze_song_mix(mix_wav, stems_dir=None, lead_stem=None, reference_genre=None):
    """Measure a rendered mix WAV and optionally verify multi_track/ centered stems + lead presence."""
    result = analyze_wav(mix_wav, reference_genre=reference_genre)
    if not stems_dir:
        return result
    stem_files = sorted(Path(stems_dir).glob("*.wav"))
    stems = {}
    all_centered = True
    lead_arrs, other_arrs = [], []
    sr = result["sample_rate"]
    for sf in stem_files:
        arr, sf_sr = _read_wav(sf)
        sr = sf_sr
        rms_l = float(np.sqrt(np.mean(arr[:, 0] ** 2))) if len(arr) else 0.0
        rms_r = float(np.sqrt(np.mean(arr[:, 1] ** 2))) if len(arr) else 0.0
        lr_balance_db = round(20.0 * math.log10(max(rms_l, 1e-12) / max(rms_r, 1e-12)), 2) if (rms_l > 0 or rms_r > 0) else 0.0
        centered = abs(lr_balance_db) < 2.0
        if not centered:
            all_centered = False
        lufs = _k_weighted_lufs(arr, sf_sr)
        stems[sf.stem] = {
            "k_weighted_lufs": lufs,
            "lr_balance_db": lr_balance_db,
            "centered": centered,
            "peak": round(float(np.abs(arr).max()), 5),
        }
        if lead_stem and lead_stem.lower() in sf.stem.lower():
            lead_arrs.append(arr)
        else:
            other_arrs.append(arr)

    result["stems"] = stems
    result["all_stems_centered"] = all_centered
    if lead_arrs and other_arrs:
        n = min(min(len(a) for a in lead_arrs), min(len(a) for a in other_arrs))
        lead_sum = sum(a[:n] for a in lead_arrs)
        other_sum = sum(a[:n] for a in other_arrs)
        result["lead_minus_accompaniment_db"] = round(_k_weighted_lufs(lead_sum, sr) - _k_weighted_lufs(other_sum, sr), 2)
    return result


def _inspect_wav_header(wav_path):
    with wave.open(str(wav_path), "rb") as wf:
        sr = wf.getframerate()
        ch = wf.getnchannels()
        sw = wf.getsampwidth()
        nframes = wf.getnframes()
    total_duration_s = (nframes / float(sr)) if sr > 0 else 0.0
    return sr, ch, sw, nframes, total_duration_s


def _require_finite(name, value):
    val = float(value)
    if not math.isfinite(val):
        raise ValueError(f"{name} must be a finite number, got {value!r}")
    return val


def slice_wav(wav_path, out_path, start_s=0.0, duration_s=None, end_s=None):
    """Extract a PCM WAV segment [start_s, end_s] cleanly, preserving format."""
    src = Path(wav_path)
    dst = Path(out_path)
    if not src.is_file():
        raise FileNotFoundError(f"WAV file not found: {src}")

    sr, ch, sw, nframes, total_duration_s = _inspect_wav_header(src)
    if nframes <= 0 or sr <= 0:
        raise ValueError(f"WAV file has no audio frames: {src}")

    start_val = _require_finite("start_s", start_s)
    if start_val < 0.0 or start_val >= total_duration_s:
        raise ValueError(
            f"start_s ({start_val:.3f}s) must be in [0, {total_duration_s:.3f}s) for {src.name}"
        )

    if duration_s is not None and end_s is not None:
        raise ValueError("Specify either duration_s or end_s, not both")

    if duration_s is not None:
        dur_val = _require_finite("duration_s", duration_s)
        if dur_val <= 0.0:
            raise ValueError(f"duration_s ({dur_val}) must be > 0")
        raw_end = start_val + dur_val
    elif end_s is not None:
        raw_end = _require_finite("end_s", end_s)
        if raw_end <= start_val:
            raise ValueError(f"end_s ({raw_end}) must be greater than start_s ({start_val})")
    else:
        raw_end = total_duration_s

    clamped = raw_end > total_duration_s
    actual_end = min(raw_end, total_duration_s)
    start_frame = int(round(start_val * sr))
    end_frame = min(nframes, int(round(actual_end * sr)))
    if end_frame <= start_frame:
        raise ValueError("Requested slice resolves to 0 audio frames")

    with wave.open(str(src), "rb") as rf:
        rf.setpos(start_frame)
        frames_bytes = rf.readframes(end_frame - start_frame)

    dst.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(dst), "wb") as wf:
        wf.setnchannels(ch)
        wf.setsampwidth(sw)
        wf.setframerate(sr)
        wf.writeframes(frames_bytes)

    actual_start_s = start_frame / float(sr)
    actual_end_s = end_frame / float(sr)
    return {
        "path": str(dst),
        "source": str(src),
        "start_s": round(actual_start_s, 3),
        "end_s": round(actual_end_s, 3),
        "duration_s": round(actual_end_s - actual_start_s, 3),
        "total_duration_s": round(total_duration_s, 3),
        "sample_rate": int(sr),
        "channels": int(ch),
        "clamped": bool(clamped),
    }


def build_auto_profile_windows(total_duration_s, bpm=None, loop_seam_s=None):
    """Generate variable-duration (micro + meso) audit windows tailored to track length."""
    total = _require_finite("total_duration_s", total_duration_s)
    if total <= 0.0:
        raise ValueError("total_duration_s must be > 0")

    if bpm is not None:
        bpm_val = _require_finite("bpm", bpm)
        if bpm_val <= 0.0:
            raise ValueError(f"bpm ({bpm_val}) must be > 0")
        bar_s = 240.0 / bpm_val
    else:
        bar_s = None

    if loop_seam_s is not None:
        seam_val = _require_finite("loop_seam_s", loop_seam_s)
    else:
        seam_val = None

    if total <= 0.2:
        return [{"label": "full_micro", "scale": "micro", "start_s": 0.0, "duration_s": total}]

    def _fit(label, start, dur, scale):
        s = max(0.0, min(start, max(0.0, total - 0.1)))
        s_r = math.floor(s * 1000.0) / 1000.0
        d = min(dur, total - s_r)
        d_r = math.floor(d * 1000.0) / 1000.0
        if d_r <= 0.0:
            d_r = max(0.0, total - s_r)
        return {"label": label, "scale": scale, "start_s": s_r, "duration_s": d_r}

    if total <= 25.0:
        micro_d = min(6.0, max(2.0, total * 0.3))
        meso_d = min(12.0, max(4.0, total * 0.55))
        candidates = [
            _fit("opening_micro", 0.0, micro_d, "micro"),
            _fit("body_meso", max(0.0, total * 0.25), meso_d, "meso"),
            _fit("ending_micro", max(0.0, total - micro_d), micro_d, "micro"),
        ]
    else:
        micro_d = min(10.0, max(6.0, round(bar_s * 2.0, 2) if bar_s else 8.0))
        detail_d = min(12.0, max(6.0, round(bar_s * 3.0, 2) if bar_s else 10.0))
        meso_verse_d = min(24.0, max(14.0, round(bar_s * 6.0, 2) if bar_s else 20.0))
        meso_chorus_d = min(30.0, max(16.0, round(bar_s * 8.0, 2) if bar_s else 28.0))
        candidates = [
            _fit("intro_micro", 0.0, micro_d, "micro"),
            _fit("verse_meso", total * 0.22, meso_verse_d, "meso"),
            _fit("transition_micro", total * 0.44, micro_d, "micro"),
            _fit("climax_meso", total * 0.58, meso_chorus_d, "meso"),
            _fit("detail_micro", total * 0.78, min(detail_d, total * 0.22), "micro"),
            _fit("outro_micro", max(total * 0.85, total - detail_d), detail_d, "micro"),
        ]

    if seam_val is not None and 0.0 < seam_val < total:
        candidates.append(_fit("loop_seam_micro", max(0.0, seam_val - 3.0), 6.0, "micro"))

    candidates.sort(key=lambda item: (item["start_s"], item["duration_s"]))
    deduped = []
    seen = set()
    for w in candidates:
        if w["duration_s"] <= 0.05:
            continue
        key = (round(w["start_s"], 1), round(w["duration_s"], 1))
        if key not in seen:
            seen.add(key)
            deduped.append(w)
    return deduped


def slice_wav_segments(wav_path, out_dir, windows=None, auto_profile=False, bpm=None, loop_seam_s=None):
    """Extract multiple variable-duration audit clips from a WAV file into out_dir."""
    src = Path(wav_path)
    sr, ch, _, nframes, total_duration_s = _inspect_wav_header(src)
    if nframes <= 0 or sr <= 0:
        raise ValueError(f"WAV file has no audio frames: {src}")

    if auto_profile and windows is not None:
        raise ValueError("Specify either explicit windows or auto_profile=True, not both")

    if auto_profile or windows is None:
        plan = build_auto_profile_windows(total_duration_s, bpm=bpm, loop_seam_s=loop_seam_s)
    else:
        plan = list(windows)
        if not plan:
            raise ValueError("windows must not be empty")

    out_root = Path(out_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    stem = src.stem
    segments = []
    for idx, w in enumerate(plan, start=1):
        label = str(w.get("label") or f"seg_{idx:02d}")
        safe_label = "".join(c if (c.isalnum() or c in ("-", "_")) else "_" for c in label)
        start_s = float(w["start_s"])
        dur_s = w.get("duration_s")
        end_s = w.get("end_s")
        clip_path = out_root / f"{stem}_{idx:02d}_{safe_label}.wav"
        meta = slice_wav(src, clip_path, start_s=start_s, duration_s=dur_s, end_s=end_s)
        meta["label"] = label
        if "scale" in w:
            meta["scale"] = w["scale"]
        segments.append(meta)

    return {
        "source": str(src),
        "total_duration_s": round(total_duration_s, 3),
        "sample_rate": int(sr),
        "channels": int(ch),
        "segments": segments,
    }
