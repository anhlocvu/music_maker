# Fretboard Playability, Tunings, Capo & Symbolic Metrics

*Grounded strictly in `Fretting-Transformer` (Hamberger et al., 2025), `dadagp.py`, and `GTR-CTRL / ShredGP` (Sarmento et al., 2023).*

---

## 1. Why Playability Matters (String–Fret Ambiguity)

On a fretted instrument, the same MIDI pitch can be played on multiple `(string, fret)` pairs (e.g., `E4 = 64` is open string 1, fret 5 on string 2, fret 9 on string 3, or fret 14 on string 4). Writing from a piano-roll mindset without fretboard geometry produces:
- Unplayable chord stretches (>4–5 frets wide without an open string).
- Impossible simultaneous note assignments on the same string.
- Unnatural position jumps instead of idiomatic box patterns or open-string resonance.

---

## 2. Quantitative Fretboard Transition Difficulty (`Fretting-Transformer`, Eq. 1–6)

When evaluating a transition from fretboard position $p = (\text{string}_p, \text{fret}_p)$ to $q = (\text{string}_q, \text{fret}_q)$ on a 24-fret guitar:

$$\text{difficulty}(p, q) = \text{along}(p, q) + \text{across}(p, q)$$

1. **Horizontal movement along the neck** ($\text{along}(p, q) = \text{fret\_stretch}(p, q) + \text{locality}(p, q)$):
   - Let $\Delta\text{fret} = \text{fret}_q - \text{fret}_p$:
     $$\text{fret\_stretch}(p, q) = \begin{cases} 0.50 \cdot |\Delta\text{fret}| & \text{if } \Delta\text{fret} > 0 \text{ (moving up toward narrower frets)} \\ 0.75 \cdot |\Delta\text{fret}| & \text{if } \Delta\text{fret} \le 0 \text{ (moving down toward wider frets)} \end{cases}$$
   - **Locality penalty** (higher frets require greater string tension/reach, while open strings `0` cost zero):
     $$\text{locality}(p, q) = \alpha \cdot (\text{fret}_p + \text{fret}_q), \quad \alpha = 0.25$$
2. **Vertical movement across strings** ($\text{across}(p, q) = \text{vertical\_stretch}(p, q)$):
   - Let $\Delta\text{string} = |\text{string}_q - \text{string}_p|$:
     $$\text{vertical\_stretch}(p, q) = \begin{cases} 0.25 & \text{if } \Delta\text{string} \le 1 \text{ (same or adjacent string)} \\ 0.50 & \text{if } \Delta\text{string} > 1 \text{ (string skip)} \end{cases}$$
3. **Reference scale**: `[0 .. 18.5]` for a 24-fret neck (`0` = repeating the same open string). Empirical dataset difficulty averages from *Fretting-Transformer* (Table 3):
   - Easy fingerstyle (*GuitarToday*): `~1.95`
   - Rock/Metal (*DadaGP*): `~2.41`
   - Complex Jazz (*Leduc*): `~4.24`

### Practical Arrangement Rules Derived from This Model

- **Stay inside a 4-fret hand box** (plus 1-fret index/pinky extension) for single-note melodies and arpeggios unless deliberately executing a slide or position shift.
- **Prefer open strings** (`E2, A2, D3, G3, B3, E4` in standard tuning) as chord anchors or pedal tones in folk, pop, and rock riffs (just as *Fretting-Transformer* Fig. 3 demonstrates for *Smoke on the Water*-style riffs).
- **Avoid rapid downward fret leaps** (`0.75` penalty vs `0.50` upward); if jumping down >4 frets, place a rest, open string, or slide breath between phrases.
- **Check chord polyphony**: A 6-string guitar sounds at most 6 notes simultaneously—and only when each pitch maps to a distinct string within a 4-fret span (or open strings). Never assign piano-style stacked 2nds/close triads in the low register (`E2–D3`).
- **Context window consistency**: Choose positions using at least a `±5` note lookahead/lookbehind window (not greedy note-by-note minimum fret) so phrases stay coherent in one neck region.

---

## 3. Supported Guitar & Bass Tunings (`dadagp.py` & `Fretting-Transformer`)

Interval vectors show semitone differences from highest string down to lowest string:

| Tuning ID | Instrument | Open Strings (High → Low) | Interval Vector (`strdiff`) | Typical Use |
|---|---|---|---|---|
| `g6_standard` | 6-string Guitar | `E4 B3 G3 D3 A2 E2` | `[-5, -4, -5, -5, -5]` | General pop, rock, jazz, blues, fingerstyle |
| `g6_drop` | 6-string Drop D | `E4 B3 G3 D3 A2 D2` | `[-5, -4, -5, -5, -7]` | Rock/metal chugs, one-finger fifth power chords (`D2+A2+D3`) |
| `g7_standard` | 7-string Guitar | `E4 B3 G3 D3 A2 E2 B1` | `[-5, -4, -5, -5, -5, -5]` | Extended-range metal, prog, low riffing |
| `g7_drop` | 7-string Drop A | `E4 B3 G3 D3 A2 D2 A1` | `[-5, -4, -5, -5, -7, -5]` | Modern metal / djent |
| `b4_standard` | 4-string Bass | `G2 D2 A1 E1` | `[-5, -5, -5]` | Standard electric/upright bass |
| `b4_drop` | 4-string Drop D Bass | `G2 D2 A1 D1` | `[-5, -5, -7]` | Matches `g6_drop` guitar low `D` pedal |
| `b5_standard` | 5-string Bass | `G2 D2 A1 E1 B0` | `[-5, -5, -5, -5]` | Pop/gospel/modern R&B/metal low `B0–D1` sub weight |
| `b6_standard` | 6-string Bass | `C3 G2 D2 A1 E1 B0` | `[-5, -5, -5, -5, -5]` | Solo bass, jazz fusion chordal/upper-register fills |

- **Uniform Downtuning** (*Fretting-Transformer* Sec 3.3 & `dadagp.py`):
  - **Half-step down (`-1` st)**: `Eb4 Bb3 Gb3 Db3 Ab2 Eb2` (`transpose=-1` on open-shape tabs).
  - **Full-step down (`-2` st)**: `D4 A3 F3 C3 G2 D2` (or Drop C: `D4 A3 F3 C3 G2 C2`).
- **Capo Conditioning (`CAPO<0..7>`)**:
  - A capo at fret $k$ shifts every sounding pitch up by $+k$ semitones while preserving open-string fingerings (`soundfont-music`: write comfortable open-key shapes in `C/G/D/Am/Em`, then set `Track(..., transpose=k)`).

---

## 4. Conditioning & Symbolic Quality Metrics (`GTR-CTRL`, Sarmento et al. 2023)

Use these principles when structuring arrangements and auditing symbolic scores (`engine/review.py`):

1. **Decouple Instrument/Genre Setup from Opening Notes**:
   - Specifying an initial low open-string note (e.g., `E2`) to establish guitar presence inadvertently locks the song's key to E minor/major. Lock instrumentation and genre frame *first*, then choose the target key independently.
2. **Four Quantitative Symbolic Metrics**:
   - **PCE (Pitch Class Histogram Entropy)**: Measures tonal concentration across melodic/harmonic tracks (excluding drums). Very low PCE indicates repetitive/static harmony; moderate PCE reflects healthy tonal center with harmonic motion; excessive PCE warns of aimless chromaticism or tonal instability.
   - **GC (Groove Consistency)**: Measures bar-to-bar rhythmic similarity across the piece (`0..1`). High GC confirms steady rhythmic pocket; very low GC flags disjointed rhythms (unless intentionally free-form).
   - **PIP (Prompted Instrument Presence)**: Fraction of measures where requested instruments actually play notes (`sum(M_i - E_i) / sum(M_i)` for prompted instruments `i in P`, where `E_i` = empty rest-only measures). Target high PIP so featured tracks do not disappear for large stretches unintentionally.
   - **UIP (Unprompted Instrument Presence)**: Fraction of active measures belonging to unrequested instruments (`sum_{i in A\P}(M_i - E_i) / sum_{i in A}(M_i - E_i)`). Keep UIP near `0%`—do not leave accidental stray/ghost tracks active.
