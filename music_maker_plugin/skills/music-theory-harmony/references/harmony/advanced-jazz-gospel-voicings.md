# Advanced Jazz, Gospel Polychords, Barry Harris & Coltrane Systems

## 1. Upper Structure Triads (Jason Lyon / Opus 28 & Gospel Intersection)

An **Upper Structure (US)** voices a rich dominant or tonic chord by placing the essential **shell** (`root` in bass + `3` and `7` tritone in middle-low range) underneath a **major or minor triad** in close or spread position in the upper register. The upper triad creates audible triadic clarity inside dense altered harmonies while avoiding awkward low-register clashes.

*Notation rule*: Upper Structure Roman numerals (`II`, `bIII`, `#IV`, `bVI`, `VI`, `#Im`, `bIIIm`, `#IVm`) name the **triad root relative to the chord's root**, regardless of key signature.

### Complete Verified Upper Structure Table for Dominant Chords (`C7` Examples)

| US Degree & Quality | Notes over `C7` (`E–Bb` shell) | Resulting Tensions Added | Parent Scale | Best Harmonic Function / Affect |
|---|---|---|---|---|
| **US II** (major) | `D F# A` over `C7` | `9, #11, 13` (`C13#11`) | Mixolydian `#11` (Lydian `b7`) | The "YEAH" / Gospel–Jazz bright dominant (`IV` Lydian/backdoor) |
| **US bIII** (major) | `Eb G Bb` over `C7` | `#9, 5, 7` (`C7#9`) | Altered / Half-Whole Dim | Bluesy, gritty soul/funk `7#9` |
| **US #IV** (major) | `F# A# C#` over `C7` | `#11, b7, b9` (`C7b9#11`) | Half-Whole Dim / Altered | **Works on BOTH `7b9` and `7alt`**; biting upper clarity |
| **US bVI** (major) | `Ab C Eb` over `C7` | `b13, 1, #9` (`C7#9b13` / `C7alt`) | **Altered (7th mode Melodic Minor)** | Classic fiery jazz-altered turnaround dominant |
| **US VI** (major) | `A C# E` over `C7` | `13, b9, 3` (`C13b9`) | **Half-Whole Diminished** | Gospel climax dominant (e.g., `C#/E7`), radiant major triad against `b9` |
| **US #Im** (minor) | `C# E G#` over `C7` | `b9, 3, b13` (`C7b9b13`) | **Altered / Phrygian Dominant** | Smooth descending minor-tonic approach (`V7alt -> i` or `I`) |
| **US bIIIm** (minor) | `Eb Gb Bb` over `C7` | `#9, #11, b7` (`C7#9#11`) | **Half-Whole Dim & Altered** | Dual-family bridge US (shared by both `7b9` & `7alt`) |
| **US #IVm** (minor) | `F# A C#` over `C7` | `#11, 13, b9` (`C13b9#11`) | **Half-Whole Diminished** | Rich extended diminished dominant (`13b9#11`) |

**Upper Structure Selection Rule by Target Resolution**:
- Use **`7b9` US shapes** (`VI`, `#IVm`, `bIII`) when the chord contains a natural `13` (`A` over `C7`), especially resolving to **major** (`I`) or functioning as `V7/V` / Gospel `I13`.
- Use **`7alt` US shapes** (`bVI`, `#Im`) when `b13` (`Ab`) + `b9/#9` dominate, especially resolving into **minor (`i`)** or heavy chromatic `ii-V`.
- Use **shared US shapes** (`#IV`, `bIIIm`) to pivot seamlessly between Half-Whole Diminished and Altered scales mid-phrase.

```python
from engine.harmony import upper_structure_triad
from engine.voicing import upper_structure_voicing

us = upper_structure_triad("E", "VI", "maj")   # C# triad over E7 (G# D) -> E13b9!
v = upper_structure_voicing("C", "bVI", "maj", bass_octave=3, upper_octave=4)
```

---

## 2. Gospel Polychords, Diminished Passing & Walk-Ups

Contemporary Gospel fuses Jazz extensions with tight 3-part SAT/SAB choir upper structures over pedal or walking bass lines:

### Polychordal Gospel Construction (`Upper Chord / Bass Root`)

| Desired Sound | Polychord Shortcut (RH over Bass) | Intervals Realized | Classic Gospel Application |
|---|---|---|---|
| **Dom13sus4 (`C13sus4`)** | `Bbmaj7 / C` (`bVIImaj7 / R`) | `b7, 9, 11, 13` (no 3rd clash!) | The quintessential warm Gospel dominant; delays `3` cleanly before `C13b9` |
| **Dom13add9 (`C13`)** | `Bbmaj7b5 / C` (`bVIImaj7b5 / R`) | `b7, 9, 3 (E), 13` | `E` replaces `F`, instantly opening `sus4` into full `13` |
| **Dom7#9#5 (`C7#9#5`)** | `Emaj7b5 / C` (`IIImaj7b5 / R`) | `3, #5 (G#), b7 (Bb), #9 (D#)` | Crunchy Gospel turnaround `V7alt -> I` or `V7/vi` |
| **Half-Dim7 (`Cm7b5`)** | `Ebm / C` (`bIIIm / R`) | `1, b3, b5, b7` | `iiø7` in minor keys or `iiø7/I` |
| **Min11 (`Cm11`)** | `Bbmaj7 / C` or `Eb6 / C` | `1, b3, 5, b7, 9, 11` | Warm minor tonic / `ii11` pad |

### Signature Gospel Harmonic Moves
1. **`I13` Tonic Dominant**: Like blues, `I` frequently carries a `b7` + `13` (`I7` / `I13`) rather than a pure `maj7`.
2. **`b5` Diminished Passing Chords**: Insert a `dim7` chord a semitone below target roots (`#iv°7 -> V` or `#i°7 -> ii`, and chromatic walk-ups `#1°7 -> ii`, `#2°7 -> iii`, `#5°7 -> vi`) and symmetric `dim7` ascents moving in **minor 3rds** (`+3` st).
3. **`iiø7 -> I6/4` Walk-Up**: Bass walks chromatically/diatonically up through `iiø7` (`ii - iii - IV - #iv°7 -> I/V -> V13sus4 -> I`).
4. **3-Part Gospel Choir Structures**: Voice SAB/SSA upper blocks purely as **Major triads, Minor triads, Diminished triads (`3-5-b7` of dominant), or Sus2/Sus4 triads (`1-2-5`, `1-4-5`)** over LH `R-3-7`.
5. **Neo-Soul Parallel `maj9` / `min9` Inversions**: Maintain crisp open 9th/5th voicings (`R–5–7–9–3` or rootless `3–5–7–9` / `7–9–3–5`) and glide chromatically or diatonically via parallel planing (`Em9 -> Fmaj9 -> Gm9 -> Ebm9`).

---

## 3. Barry Harris 6th-Diminished System (Major & Minor)

Barry Harris unifies harmony and horizontal scale motion into **one 8-note scale** per tonic by inserting the **`b6` passing tone** between `5` and `6`, pairing exactly two interlocking four-note chord families: **Tonic `6` (`1 3 5 6`)** and **Leading-Tone `vii°7` (`7 2 4 b6`)**:

- **Major 6th Diminished Scale**: `1 – 2 – 3 – 4 – 5 – b6 – 6 – 7` (`C D E F G Ab A B` -> alternates `C6` and `B°7`).
- **Minor 6th Diminished Scale**: `1 – 2 – b3 – 4 – 5 – b6 – 6 – 7` (`C D Eb F G Ab A B` -> alternates `Cm6` and `B°7`).
- **Functional Rule (Borrowing / Movement inside a Static Chord)**:
  - On *any* sustained tonic chord (`C6` or `Cm6`), harmonize scalar melodies note-for-note by alternating `C6` inversions on chord tones (`C E G A`) and `B°7` inversions on passing tones (`D F Ab B`).
  - **1-Note Borrowing**: Borrow a single note from the opposite family into `C6` (`B°7`'s `Ab` over `C6` = `C6/b6` Gospel plagal turn) or move 2 notes in contrary motion for luminous multi-voice counterpoint without ever leaving tonic space!

```python
from engine.harmony import barry_harris_scale
bh = barry_harris_scale("C", mode="major")
# {'scale_pcs': [0,2,4,5,7,8,9,11], 'tonic_sixth_pcs': [0,4,7,9], 'diminished_pcs': [11,2,5,8]}
```

---

## 4. Coltrane Multi-Tonic Cycles (Symmetric Divisions of the Octave)

John Coltrane partitioned the 12-tone octave symmetrically into major-3rd (`T_4` / `T_{-4}`, 3 key centers) and minor-3rd / tritone axes (`T_3` / `T_6`, 4 key centers), bridging remote tonics rapidly via `V7` or `ii-V7`:

1. **Major-3rd Cycle (*Giant Steps* / *Countdown*)**:
   - **Giant Steps (8-bar A, `I - V7 -> I` descending by M3)**:
     `Bmaj7 D7 | Gmaj7 Bb7 | Ebmaj7 | Am7 D7 | Gmaj7 Bb7 | Ebmaj7 F#7 | Bmaj7 | Fm7 Bb7` (key centers: `B -> G -> Eb`, then returning via `ii-V` up `+4` st).
   - **Countdown substitution**: Replace a standard `ii7 – V7 – I` (in `C`: `Dm7 – G7 – Cmaj7`) with descending M3 centers (`Dm7 Eb7 | Abmaj7 B7 | Emaj7 G7 | Cmaj7`).
   - **Common-Tone / Axis Coherence**: Across `B – G – Eb`, each tonic relates by Neo-Riemannian `PL` / `LP` and Lendvai's Axis equivalence (where `ii` of one center sits on the `S` axis of the previous center, producing smooth 1-to-2 semitone guide-tone links).
2. **Minor-3rd / Tritone Axis Cycle (*Central Park West*)**:
   - Symmetric m3/tritone pivots (`Bmaj7 -> Dmaj7 -> Abmaj7 -> Fmaj7 -> Bmaj7`) or `ii-V` chains ascending by `+3` st, linked by **common melody notes** sustained across tonic shifts.

```python
from engine.harmony import coltrane_cycle
giant = coltrane_cycle("B", direction=-1, include_dominants=True)
# ['Bmaj7', 'D7', 'Gmaj7', 'Bb7', 'Ebmaj7', 'F#7']
```

---

## 5. Standard Idiom Forms & Drop / Quartal Voicings (`engine.voicing`)

- **12-Bar Blues** (3 stanzas × 4 bars): Basic `I–I–I–I | IV–IV–I–I | V–IV–I–I`; Jazz Blues adds `I7–IV7–I7–v7/V7/IV | IV7–#iv°7–I7–VI7 | ii7–V7–iii7 VI7–ii7 V7`.
- **32-Bar Rhythm Changes (`AABA`, 8+8+8+8)**: `A` = `I vi | ii V | I vi | ii V | I I7 | IV #iv°7 | I V | I`; `B` Bridge = dominant cycle of 5ths `III7 (2 bars) -> VI7 (2) -> II7 (2) -> V7 (2)`.
- **Mechanical & Quartal Voicings** (Dan Haerle / Evan Rogers / Tim Davies):
  - **Drop-2**: Drop the 2nd voice from top of a close 4-note chord down 1 octave — opens minor-2nd top-voice rubs and adds warm tenor richness (`drop2(notes)`).
  - **Drop-3**: Drop the 3rd voice from top down 1 octave (`drop3(notes)`).
  - **Drop-2+4**: Drop both 2nd and 4th voices down 1 octave (`drop24(notes)`) for lush spread pads.
  - **Quartal & "So What" Voicings**: 4ths stacked upward (`quartal_stack(root, 4)`), or `So What` = `[0, +5, +10, +15, +19]` (3 stacked P4s + M3 on top, e.g. `D-G-C-F-A` for `Dm11`).
