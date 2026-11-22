# Spectral Melody & Schillinger Periodic Rhythm Techniques

## 1. Spectral & Post-Spectral Melody (Donaldson / Grisey / Vivier / Haas)

Spectral and post-spectral music derives pitch, harmonic tension, and melodic continuity directly from **acoustical harmonic overtone spectra** ($f_k = k \cdot f_0$) rather than abstract 12-TET scales.

### Three Spectral Melodic Archetypes

| Type | Structural Role | Acoustic / Compositional Mechanism | Repertoire Benchmark |
|---|---|---|---|
| **1. Differential** | Gradual unfolding & timbral transformation | Horizontal melody articulates/projects the overtones of a fundamental bass, moving smoothly across harmonic vs. inharmonic spectra | **Gérard Grisey, *Prologue*** (viola solo unfolding harmonic spectra & spectral compression over time) |
| **2. Liminal** | Perceptual threshold between **timbre, chord & melody** | High odd partials (**7, 9, 11, 13**) and combination tones/ring modulation are voiced as monophonic/homophonic "melody-as-timbre" ("jeux de timbres") | **Claude Vivier, *Zipangu*** (partials `7–13` stacked as shimmering harmonic colors glued beneath melodic contour) |
| **3. Transitory** | Continuous pitch/spectrum gliding & microtonal morphing | Eliminates discrete note steps in favor of continuous glissandi, quarter-tone/sixth-tone partial approximations, and morphing beat frequencies | **Georg Friedrich Haas, *de terrae fine*** |

### Microtonal Partial-to-Cents Guide (from Fundamental `C`, `k = 1..16`)

When programming spectral melodies or just-intonation partials in `soundfont-music` (using per-track `cents=` or `Track.bend()` / MPE):

| Harmonic Partial $k$ | Closest 12-TET Interval above `C` | Exact Cents Deviation from 12-TET | Sonic Character |
|---|---|---|---|
| `1, 2, 4, 8, 16` | Unison / Octaves (`C`) | `0` cents | Acoustic bedrock |
| `3, 6, 12` | `P5 + 8ve` (`G`) | **`+2`** cents | Pure fifth |
| `5, 10` | `M3 + 2/3 8ve` (`E`) | **`-14`** cents | Sweet just-intonation third |
| **`7, 14`** | Natural minor 7th (`Bb`) | **`-31`** cents | "Harmonic seventh" (warm blue/spectral glow) |
| `9` | Major 9th (`D`) | **`+4`** cents | Bright pythagorean step |
| **`11`** | Half-sharp 4th (`F / F#` midpoint) | **`-49`** cents (`F#` down / `+51` from `F`) | Iconic **Alpha-Alphorn** spectral fourth! |
| **`13`** | Neutral 6th (`Ab / A`) | **`+41`** cents from `Ab` (`-59` from `A`) | Vivier / spectral bittersweet minor-major 6th |
| `15` | Major 7th (`B`) | **`-12`** cents | Pure harmonic leading tone |

---

## 2. Schillinger System of Musical Composition — Rhythmic Interference (Absil)

Joseph Schillinger generates non-repeating, organically balanced asymmetric rhythms by colliding two (or more) regular periodic clocks (**monomial periodicities**) called **Interference of Periodicities**.

### Core Equation: Binary Synchronization (`a ÷ b`)
Let **Major Generator $a$** and **Minor Generator $b$** ($a > b$, coprime integers, time grid step $\Delta t$):
- Attack series $\vec{t}_r = \vec{t}_A \cup \vec{t}_B$ combines every tick from both periodicities starting together at $t = 0$.
- The full rhythmic cycle repeats cleanly every **$T_r = a \cdot b \cdot \Delta t$** time units!
- Resultant duration sequence $r_{a \div b}$ records intervals $r_i = t_{r, i+1} - t_{r, i}$ (always palindromic/symmetric!).

### Exact Verified Schillinger Resultant Patterns (`r_{a÷b}`)

| Generator Pair `a ÷ b` | Cycle Length $a \cdot b$ (grid units) | Resulting Duration Pattern $r_{a \div b}$ (symmetric palindrome!) | Musical Meter Mapping |
|---|---|---|---|
| **`3 ÷ 2`** | `6` eighths (`3/4` or `6/8`) | **`[2, 1, 1, 2]`** | Classic Afro-Cuban/rock hemiola pulse |
| **`4 ÷ 3`** | `12` sixteenths (`3/4` or `12/8`) | **`[3, 1, 2, 2, 1, 3]`** | Rolling modernist/prog ostinato (total = 12) |
| **`5 ÷ 2`** | `10` steps (`5/4` or `10/8`) | **`[2, 2, 1, 1, 2, 2]`** | Tight asymmetric 5/4 groove |
| **`5 ÷ 3`** | `15` steps (`15/8`) | **`[3, 2, 1, 3, 1, 2, 3]`** | Extended 15-step polymetric cycle |
| **`5 ÷ 4`** | `20` steps (`5/4` in 16ths) | **`[4, 1, 3, 2, 2, 3, 1, 4]`** | Dense shifting accents inside 5/4 |
| **`6 ÷ 5`** | `30` steps | **`[5, 1, 4, 2, 3, 3, 2, 4, 1, 5]`** | Long-form developmental phrase |
| **`7 ÷ 4`** | `28` steps (`7/4` in 16ths) | **`[4, 3, 1, 4, 2, 2, 4, 1, 3, 4]`** | High-energy asymmetric 7-beat cycle |

### Advanced Schillinger Rhythm Operations
1. **Fractioning (`r'_{a÷b}`)**: When $a \cdot b$ feels too slow or breaks standard $4/4$ barlines, reset/compress the minor generator $b$ into **square symmetry ($a^2$ units)** so interference resolves inside even phrasing (`e.g. 3 ÷ 2` inside `3 × 3 = 9` or binary `2^k` bars).
2. **Three Generators (`a ÷ b ÷ c`)**: Collide 3 clocks (e.g., `5 ÷ 3 ÷ 2`, cycle $a b c = 30$) or assign each generator to a different kit/orchestral voice for locked polyrhythm.
3. **Grouping by Common Product**: Re-bar an interference resultant into regular beats (e.g., regroup 12-unit `r(4:3) = [3,1,2,2,1,3]` over three `4/4` bars of 16ths by tying across barlines -> organic syncopation without randomness).
4. **Distributive Powers & Binomial Evolution**: Multiply rhythmic polynomials $(a + b)^2$ or $(a + b)^3$ to derive self-similar multi-bar rhythmic phrase forms (*homogeneous continuity*).
5. **Variable Velocities (Geometric Accelerando / Ritardando)**: Apply geometric or Fibonacci ratios (`1:2:4:8` or `2:3:5:8`) to step durations to compose structurally measured speed-ups and slow-downs.

### Python Implementation Snippet (`soundfont-music`)
```python
def schillinger_resultant(a: int, b: int) -> list[int]:
    """Compute Schillinger binary synchronization r(a:b) over a*b grid units."""
    attacks = sorted(set(range(0, a * b, a)) | set(range(0, a * b, b))) + [a * b]
    return [attacks[i + 1] - attacks[i] for i in range(len(attacks) - 1)]
# schillinger_resultant(4, 3) -> [3, 1, 2, 2, 1, 3]
```
