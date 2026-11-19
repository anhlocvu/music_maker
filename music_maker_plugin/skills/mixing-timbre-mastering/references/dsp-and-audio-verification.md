# DSP Quality & Post-Render Audio Verification

*Grounded in `audio-artifacts-debug`, `audio-dsp`, and `soundfont-music` NumPy/WAV verification practices.*

## 1. Mandatory Integrity Rule
You cannot physically listen to rendered audio files. Never claim a mix "sounds warm," "hits hard," or "has no mud" by ear—instead, **verify structure, levels, dynamic range, phase, and artifact absence quantitatively via Python/NumPy** after every render, and report exactly what was measured.

---

## 2. Audio Artifact Prevention & Diagnostic Checklist

| Artifact | Root Cause in Synthesis / SoundFont Code | Prevention / Fix |
|---|---|---|
| **Clipping / Crackling** | Summed peak exceeds `±1.0` (`>= 0.999` float or `32767` int16) | Target `-3 dBFS` to `-1 dBFS` headroom (`peak <= 0.89`) on final mix; leave `-6 dBFS` on stems before summing |
| **Clicks / Pops at Note Cuts** | Instant zero-crossing discontinuity from zero-time release or abrupt loop splice | Keep `release >= 0.015–0.02 s` on `release_cut` stabs; wrap loops with `render_loop()` so reverb tails cross the seam smoothly |
| **DC Offset** | Asymmetric synth waveform or uncentered sample shifting mean away from `0.0` | Check `abs(mean(audio)) < 1e-4`; apply DC-blocking high-pass if nonzero |
| **Aliasing** | Non-bandlimited oscillators or extreme upward pitch shifts crossing Nyquist (`sr/2`) | Prefer clean `.sf2` multisamples in natural octave spans; inspect extreme high synth notes |
| **Phase Cancellation / Mono Collapse** | Inverted L/R polarity or heavy stereo delay/autopan collapsing in mono | Verify `(L + R) / 2` RMS does not drop sharply relative to stereo RMS |
| **Mud / Low-End Masking** | Overlapping bass notes, long 808 kick tails, or un-released `pedal()` blurring chord roots | Enforce kick-bass composite non-overlap and release/re-press `pedal()` on every chord change |

---

## 3. Standard NumPy Post-Render Verification Snippet
Run a short check like this on `out/<song>.wav` and `out/<song>/multi_track/*.wav`:

```python
import glob, wave, numpy as np

def inspect_wav(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        frames = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    if ch == 2:
        frames = frames.reshape(-1, 2)
        mono = frames.mean(axis=1)
        lr_corr = float(np.corrcoef(frames[:, 0], frames[:, 1])[0, 1]) if frames[:, 0].std() > 0 and frames[:, 1].std() > 0 else 1.0
    else:
        mono = frames
        lr_corr = 1.0
    peak = float(np.max(np.abs(frames))) if frames.size else 0.0
    rms = float(np.sqrt(np.mean(frames ** 2))) if frames.size else 0.0
    dc = float(np.mean(frames)) if frames.size else 0.0
    crest_db = 20.0 * np.log10((peak + 1e-9) / (rms + 1e-9)) if rms > 0 else 0.0
    dur = len(mono) / sr
    print(f"{path}: dur={dur:.2f}s peak={peak:.4f} rms={rms:.4f} crest={crest_db:.1f}dB dc={dc:.2e} corr={lr_corr:.3f}")
```

**Healthy Targets**:
- `peak`: `0.50 – 0.95` (never `>= 0.999` clipped).
- `dc`: `< 1e-3`.
- `crest_db`: typically `8–18 dB` depending on genre (compressed/dense electronic vs. dynamic acoustic/orchestral).
- `lr_corr`: `> 0.0` overall on mixes (avoid near `-1.0` phase inversion); **for `multi_track/` stems exported with `keep_pan=False`, check that L and R balance matches centered `pan=0`**.
- **Duration & Alignment**: Confirm mix WAV matches expected bar count at project BPM and all `multi_track/` stems start from beat 0 without trailing past the song end.
