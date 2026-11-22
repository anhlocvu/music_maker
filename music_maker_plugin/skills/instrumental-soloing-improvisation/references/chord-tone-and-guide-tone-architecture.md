# Chord-Tone & Guide-Tone Solo Architecture

Great instrumental solos outline the harmony clearly even when heard solo (unaccompanied), rather than meandering up and down scalar steps.

## 1. Chord-Tone vs. Chord-Scale Soloing (Hal Crook)

| Dimension | Chord-Tone Soloing | Chord-Scale Soloing |
|---|---|---|
| Primary Intervals | Arpeggio leaps (`3rds`, `4ths`, `5ths`, `6ths`, `7ths`) | Stepwise scalar motion (`2nds`) |
| Harmonic Clarity | Immediately projects every chord change | Blends chords together under a modal stream |
| Primary Failure Mode | Rigid, mechanical broken-chord "exercise" sound | Directionless 8th-note scalar wandering ("running scales") |
| Accuracy Target | Prove **>= 90% chord-tone accuracy** on target beats before layering dense chromaticism | Reserve continuous scalar streams for transitions connecting strong chord tones |

### Three-Stage Solo Construction Ladder
1. **Stage 1 — Chord Tones Only**: Map `1, 3, 5, 7` (with priority on `3` and `7`) onto strong beats across every chord change.
2. **Stage 2 — Chord Tones + Approach Notes**: Retain chord tones on goal beats while approaching them by diatonic or chromatic step from below or above.
3. **Stage 3 — Synthesized Chord-Scale & Color**: Bridge goal tones with parent scales, enclosures, and color extensions (`6, 9, maj7, ♯11, 13`) while preserving rhythmic variety.

---

## 2. Three Harmonic Approaches & The "Ideal Line" (Alisdair MacRae Birch)

Choose deliberately which harmonic stance governs each phrase or section:

1. **Harmonic Generalization**: Treat a span of chords under a unified scale, mode, or blues/pentatonic umbrella (e.g., blanketing a 4-bar tonic vamp).
2. **Harmonic Specific**: Target each individual chord's defining intervals (`3rds`, `7ths`, `9ths`) and resolve them smoothly across every barline change.
3. **Harmonic Disregard**: Impose an independent melodic idea—sequential pattern, intervallic motif, side-stepping, or superimposed substitute harmony—that intentionally cuts across the written chords before re-converging at a cadence.

### The "Ideal Line" Counterpoint Principle
- Construct the solo line as **linear two-part counterpoint against the bassline**.
- Emphasize **3rds and 7ths** so harmonic function remains unambiguous.
- Drive progressions moving in descending 5ths (`ii -> V -> I`) with smooth **downward step resolution (`7th -> 3rd` of the next chord)**.

---

## 3. Guide-Tone Architecture & "Join the Dots" (Simon Purcell)

Treat guide tones as the invisible harmonic spine beneath rapid solo figuration.

### Core Voice-Leading Paths
- **Primary Spine (`3rd <-> 7th`)**:
  - `3 -> 7 -> 3` across root-movement-by-5th cycles
  - `7 -> 3 -> 7` (invert starting guide tone for complementary register)
- **Upper-Structure Color Lines**:
  - `5 -> 9 -> 5`
  - `9 -> 13 -> 9`
- **Chromaticized Guide-Tone Destinations**:
  - Over dominant or altered harmonies, deflect standard guide tones onto color/altered extensions (`♭9`, `♯9`, `♯11`, `♭13`) to heighten cadential tension before resolving cleanly into a chord tone (`1, 3, 5, 6, 9`) of the target chord.

### Four-Step "Join the Dots" Workflow
1. Write/select sustained guide-tone targets (`3` or `7`) on strong beats (`1` and `3`) per chord.
2. Embellish each static guide tone rhythmically (anticipation, delay, octave jump).
3. Fill intervallic gaps between consecutive guide tones with short chord-scale fragments or arpeggio hops.
4. Wrap selected target dots with diatonic or chromatic **enclosures** (see `references/approach-tones-and-enclosures.md`).

---

## 4. Harmonic Delineation & Metric Weight (Mark Watkins)

- **Differentiating-Pitch Rule**: When two consecutive chords share common tones (e.g., `Dm7` and `G7` sharing `F` and `D` vs moving `C -> B`), prioritize **pitches that change** (`7th of ii -> 3rd of V`, `C -> B`) at chord boundaries rather than camping on shared common tones.
- **Metric Hierarchy (`1 & 3` vs `2 & 4`)**:
  - Use **Beats 1 and 3** as primary melodic/harmonic goal anchors where chord tones, guide-tone resolutions, and phrase targets land.
  - Use **Beats 2 and 4** as groove, rebound, chromatic passing, and timbral accent positions.

---

## 5. Avoid Notes & Priority Hierarchy (Bob Keller)

- **Pitch Priority**: Chord tones (`3, 7, 1, 5`) -> Color tones (`6, 9, maj7`) -> Arpeggios -> Passing/approach tones.
- **On-Beat vs. Off-Beat Rule**: Place chord/color tones on metric downbeats or rhythmic accents; treat non-chord tensions as off-beat appoggiaturas or rapid passing tones.
- **Avoid-Note Constraint**: Avoid resting on a scale tone a **minor 9th (`m9`) above a chord tone** (canonically the **natural 4th over a Major chord**, clashing against the major 3rd). If used melodically, constrain it strictly to a brief passing tone (`<= 8th note`) moving cleanly to `3` or `5`.

---

## 6. Shortest-Path Chord-Tone Graph Engine (Keating & Casey, ArXiv 2510.19666)

When algorithmically voicing solo arpeggio chains or guitar lines across dense changes:

1. **Graph Formulation (Weighted DAG)**:
   - Each chord $C_k$ becomes a layer of candidate `N`-note chord-tone arpeggio realizations (all notes belong to $C_k$'s chord tones).
   - Edge cost between consecutive realizations $C_1$ and $C_2$ minimizes pitch/fret distance across boundary notes:
     $$w(C_1, C_2) = \min_{i \in C_1,\, j \in C_2} |i - j| \quad (+ \text{string-change penalty } 2\times \text{ on fretted instruments})$$
2. **Dijkstra Global Optimization**: Solve shortest path from first chord to cadence rather than choosing chord shapes greedily one bar at a time.
3. **Boundary-Slot Alignment Rule**: Order notes inside each chord window so the **last note of chord $C_1$** and the **first note of chord $C_2$** realize the exact minimal transition pair $(i^*, j^*)$ across the barline.
4. **Guaranteed Smoothness Bound**: Across 12 pitch classes with 4-tone chord realizations on guitar, maximal minimal distance between any two chord-tone sets never exceeds **3 semitones (minor 3rd)**—so smooth half-step or whole-step boundary connections (`7 -> 3`, `5 -> ♭9`, etc.) are almost always available.
