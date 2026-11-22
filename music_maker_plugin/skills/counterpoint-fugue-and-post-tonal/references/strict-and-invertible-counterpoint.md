# Strict, Free & Invertible Counterpoint

## 1. Two Stylistic Pedagogies: Palestrina (Jeppesen) vs. Baroque (Schoenberg/Fux)

Choosing a contrapuntal idiom determines which dissonances, modes, and ornaments are legal:

| Dimension | Palestrina Style (Jeppesen) | Baroque / Fux Style (Schoenberg) |
|---|---|---|
| **Pitch System** | Modal (Dorian, Phrygian, Mixolydian, Aeolian, Ionian); 2 signatures (`C`, `F` with 1 flat); 1 flat to 3 sharps in leading tones | Tonal (all 24 Major & Minor keys); active "turning points" & neutralization in melodic minor |
| **Strong-Beat Dissonance** | **Forbidden** in Species 1–3; dissonances only on weak beats or via prepared 4th-species suspensions (`7-6, 4-3, 9-8, 2-3`) | **Permitted** even in 3rd species if surrounded by 2 consonances leading stepwise to a 3rd |
| **Cambiata** | **Downward only**: `c ↘ [c, d] ↘ [c, d] ↗ [c, d] ↗ c` | **Both downward and upward** shapes permitted |
| **Harmonic Endings** | Major or open-fifth cadences | Major/minor authentic `ti-do` / `re-do` or Picardy third |

## 2. Species Counterpoint Rules (1 through 5 + Mixed)

1. **First Species (1:1 Note-Against-Note)**:
   - **Openings**: Above Cantus Firmus (CF) start on `do` or `sol` (`P1, P5, P8`); below CF start **strictly on `do`** (`P1, P8` — starting on `sol` gives a dissonant P4 against bass, while `fa` misleads tonal center).
   - **Closings**: End on `P1` or `P8` approached strictly by **contrary stepwise motion**: CF `re -> do` paired with `ti -> do` (`M6 -> P8` or `m3 -> P1/P8`), or CF `ti -> do` with `re -> do`.
   - **Linear Independence**: Each voice gets one distinct melodic climax (never on the same bar as the CF climax). Avoid voice crossing, voice overlap, and intervals wider than `P12` (prefer `<= P10`). Unisons allowed ONLY on first/last bars.
   - **Parallel & Hidden Prohibitions**: Strictly forbid consecutive identical perfect consonances (`P5-P5`, `P8-P8`, `P5-P12`). Forbid approaching a perfect consonance by **similar motion** (hidden/direct fifths or octaves). Cap consecutive identical imperfect consonances (`3rds` or `6ths`) at **3 max**.
2. **Second Species (2:1 Half-Note Counterpoint)**:
   - Downbeats are consonant; weak halves may use stepwise passing tones (or neighbor tones in free/Baroque practice) plus consonant leaps/arpeggiations. Avoid downbeat-to-downbeat and offbeat-to-offbeat parallel `P5`/`P8` separated by skips.
3. **Third Species (4:1 Quarter-Note Counterpoint — *Differencias*)**:
   - Connect chord tones via double passing tones, neighbor tones, double neighbors, and **nota cambiata** (downward 4-note figure stepping down into dissonance, leaping down a 3rd to consonance, then stepping back up).
4. **Fourth Species (Syncopated Suspensions — Out-of-Phase Harmony)**:
   - Preparation (weak beat consonant) -> Suspension (tied over barline onto strong beat dissonance) -> Resolution (weak beat **downward step** into consonance).
   - **Legal Suspensions ABOVE Bass/CF**: **`7–6`**, **`4–3`**, **`9–8`** (treat `9-8` like octave: never two `9-8` in a row!).
   - **Legal Suspensions BELOW Upper Voice**: **`2–3`**, **`5–6`**, **`4–5`** (avoid `7-8` below, which sounds hollow/clumsy). Never use two `4-5` or two consonant `6-5` suspensions in a row; avoid consecutive "after-beat" fifths/octaves on weak beats.
   - **Cadence Rule**: CF must end `re -> do` while counterpoint suspends `do -> ti` (`7-6` above or `2-3` below) resolving onto final `do`. Break species to 2nd species for at most 1–2 bars if trapped.
5. **Fifth Species (Florid Counterpoint) & Mixed Species**:
   - Synthesizes Species 1–4 with ornamental suspension resolutions (dipping down a 3rd to the consonant chord tone before the step resolution, anticipation, or escape tone). Mixed species layers rhythmic rates (e.g., 2:1 against 4:1) to stratify independent polyphonic foregrounds.

## 3. Alan Belkin's Psychological Counterpoint Principles

- Treat every counterpoint study as real architecture with beginning, intensification, and cadence, not static chords trapped in whole-note CF monotony.
- Grade vertical sonorities on a **graduated "scale of harshness"** (spaced M7/m9 vs crunchy close m2/P4) rather than binary right/wrong labels, tuning harshness to tempo and timbre.
- Balance **harmonic momentum** with a mobile contrapuntal bass so harmonic rhythm fluctuates naturally toward cadences.

## 4. Invertible (Double, Triple & Quadruple) Counterpoint (Ebenezer Prout)

Counterpoint is **invertible** when two (or more) voices remain harmonically valid after one is transposed above or below the other by an interval $N$. The exact vertical interval transformation obeys the **Magic Sum Formula**: $\text{Inverted Interval} = (N + 1) - \text{Original Interval}$.

### Double Counterpoint in the Octave (`15th`) — Sum = `9` (or `16`)

| Original Interval | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` |
|---|---|---|---|---|---|---|---|---|
| **Inverts at Octave to** | `8` | `7` | `6` | **`5`** | **`4`** | `3` | `2` | `1` |

- **Critical Rules**:
  1. Note names stay identical (`C` stays `C`).
  2. **`5 <-> 4`**: A harmonic **perfect fifth (`P5`) inverts into a fourth (`P4`)**. Therefore, in 2-part writing, treat **BOTH `P5` and `P4`** carefully—treat any unsupported **fifth as a dissonance** (prepare/resolve or pass it) unless a free third bass voice can later stand underneath in real composition!
  3. **Maximum Spread**: Never let voices exceed an octave (if inverting at `8ve`)—if they cross more than an octave, parts invert onto unintended registers; use **Double Counterpoint at the 15th** (2 octaves, sum = `16` after modulo) when writing wide ranges.

### Double Counterpoint in the Tenth (`3rd` + `8ve`) — Sum = `11`

| Original Interval | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9` | `10` |
|---|---|---|---|---|---|---|---|---|---|---|
| **Inverts at Tenth to** | `10` | `9` | **`8`** | `7` | **`6`** | **`5`** | `4` | **`3`** | `2` | `1` |

- **Critical Rules**:
  1. Note names change and scalar position shifts (`C-D-E -> E-F-G`), changing modal color and minor-2nd half-step placement.
  2. **`3 <-> 8` and `6 <-> 5`**: Parallel/consecutive thirds (`3-3`) invert into **parallel octaves (`8-8`)**; parallel sixths (`6-6`) invert into **parallel fifths (`5-5`)**!
  3. **Absolute Law**: In Double Counterpoint at the Tenth, **forbid consecutive thirds and consecutive sixths** AND forbid **similar motion** into consonances—write almost exclusively in **contrary and oblique motion**! (Bonus: Adding a third voice in parallel 3rds/10ths to one inverted line gives instant 3-voice double-chord counterpoint!).

### Double Counterpoint in the Twelfth (`5th` + `8ve`) — Sum = `13`

| Original Interval | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9` | `10` | `11` | `12` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Inverts at Twelfth to** | `12` | `11` | `10` | `9` | `8` | **`7`** | **`6`** | `5` | `4` | `3` | `2` | `1` |

- **Critical Rules**:
  1. Far more flexible harmonically than the Tenth because fifth transposition preserves scale accidentals (except one degree). Consecutive 3rds (`3 <-> 10`) remain 10ths/3rds!
  2. **`6 <-> 7` (The Cardinal Rule)**: **Every sixth inverts into a dissonant seventh (`6 -> 7`)!** Therefore treat every **6th** in the model as if it were a 7th (prepare/resolve the upper note or treat it as a clear passing/suspension note) so when inverted at the 12th, that 7th resolves properly down by step (or becomes `4-3` / `7-6` / `9-8` via free cadence)!
  3. **Cadences are always free**: The last bar/beat may adjust chromatically to close cleanly in the transposed key.

### Triple & Quadruple Counterpoint (Octave-Invertible Matrices)
- With $k$ voices that can occupy **any** vertical permutation (3 voices = 6 permutations; 4 voices = 24 permutations):
  - Eliminate **all** essential `P5` intervals between any two voices (otherwise when the upper note of a 5th becomes the bass, an illegal root-fourth `6/4` results!).
  - Rely primarily on **complete triads (`1-3-5` minus bare open `1-5`)**, incomplete seventh chords (`1-3-7`, `3-5-7`), and staggered **suspensions** so every voice makes a valid bass on its own.
