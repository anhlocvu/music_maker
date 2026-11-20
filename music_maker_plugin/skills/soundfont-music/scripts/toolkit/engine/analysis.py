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
