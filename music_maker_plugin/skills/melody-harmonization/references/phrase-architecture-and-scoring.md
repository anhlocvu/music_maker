# Phrase Architecture, Fragile/Emergent Tonics & 3-Level Scoring

Distilled strictly from *Open Music Theory v2* (Performing Harmonic Analysis Using the Phrase Model; Classical Schemas; Pop Harmonic Schemas; Mark Spicer's Fragile, Absent, and Emergent Tonics) and Li Yi et al. (*AccoMontage2: A Complete Harmonization and Accompaniment Arrangement System*, ISMIR 2022).

---

## 1. Cadence-First Phrase Architecture (`Tb – PD – D – Te`)

From *Open Music Theory v2* (*Performing Harmonic Analysis Using the Phrase Model*):
**Compose a phrase backwards from its cadence**, just as harmonic analysis reads backwards:
1. **Locate Phrase Endings & Lock the Cadence (`D` / `Te`)**:
   - **Half Cadence (HC)**: Open, inconclusive phrase ending on `V` (`^5` in the bass).
   - **Authentic Cadence (AC)**: Closed ending `V(7) – I` (`^5 – ^1` in the bass). **PAC** when both chords are root-position and `^1` is in the melody over `I`; **IAC** otherwise.
   - **Cadential `6/4` (`cad.6/4`)**: Embellishes `V` over `^5` in the bass (`6–5`, `4–3` motion into `V(7)`).
   - **Pop / Modal Cadences**: **Aeolian** (`bVI–bVII–i` or Picardy `bVI–bVII–I`), **Double Plagal** (`bVII–IV–I`), **Plagal Sigh** (`IV–iv–I` with chromatic `la–le–sol`), **Lydian** (`II#–IV–I` with `fi–fa–mi`).
2. **Place the Strong Predominant (`PD`)**:
   - Back up from the cadence to place a strong predominant: typically `^4` (`fa`) or `^2` (`re`) in the bass (`IV`, `ii6`, `ii7`, or modal-mixture `iiø7` / `iv`).
3. **Establish Opening Tonic (`Tb`) & Prolongation**:
   - Start from `I` (`Tb`) and connect `Tb -> PD` using diatonic prolongation, sequences, or bass meta-schemas—or intentionally delay/weaken `Tb` using Spicer's techniques below.

---

## 2. Fragile, Emergent & Absent Tonics (Spicer 2017 / OMTv2)

Use these three tonal-ambiguity tools to build dramatic arc across Intro, Verse, Pre-Chorus, and Chorus instead of starting every section with a flat root-position `I` chord:

1. **Fragile Tonic** (Vulnerability / Loneliness / Sensitivity):
   - The tonic chord appears, but is **weakened via first inversion (`I6`)** or surrounded by inversions (`vi6`) rather than stable root position (`I`). Ideal for intimate piano/guitar Verses.
2. **Emergent Tonic** (Delayed Arrival / Triumph / Transformation):
   - **Withhold the true tonic chord during Intro, Verse, and Pre-Chorus**—starting on the relative minor (`vi`), modal centers, or `IV–V` tension—and **reveal root-position `I` triumphantly at the Chorus downbeat**.
   - *Verified Blueprint ("Let It Go" form chart in `Ab` major)*:
     - **Intro / Verse**: `Fmi – Db – Eb – Bb(mi)` (sounds like `F` Aeolian `i–VI–VII–iv`, later re-heard as `vi–IV–V–ii`).
     - **Pre-Chorus**: `Eb – Db` (prolonging `V – IV` in `Ab`, delaying resolution).
     - **Chorus**: `Ab – Eb – Fmi – Db` (`I – V – vi – IV` — `Ab` finally emerges as the triumphant tonic).
3. **Absent Tonic** (Restless / Floating / Unresolved Drive):
   - The tonic triad **never appears in the chord progression at all** (e.g., looping `IV – ii – vi – V`), while the **melody explicitly outlines `^3 – ^2 – ^1` (`mi–re–do`)**, letting the ear infer the missing tonic.

---

## 3. AccoMontage2 Three-Level Harmonization Scoring

When selecting or ranking candidate progressions for a multi-phrase melody (or building a progression from scratch across sections), evaluate candidates across **three hierarchical levels**:

1. **Micro-Level (Note-Wise Melody-Chord Fit)**:
   - Measure dissonance/consonance between each sounding melody pitch and the candidate chord root/tones, conditioned on **mode** (major vs. minor) and **harmonic function**:
     - Strong-beat melody notes (`beat_strength 2–3`) prefer unison/octave, 3rd, 5th, 6th, or intentional 7th/9th/11th/13th color; penalize unintended **minor-2nd** or **tritone** clashes (e.g., natural 4th against major 3rd/major 7th on `Imaj7`, unless voiced as `13sus4` or `#11`).
   - Do *not* over-penalize brief weak-beat passing/neighbor notes (`AutoHarmonizer` proper NCTs).
2. **Meso-Level (Phrase-Template Length & Integrity)**:
   - Match harmonic progression templates cleanly to **melodic phrase lengths** (typically **4-bar or 8-bar** phrases).
   - Penalize awkward mid-phrase template stitching unless the transition across the 2-bar seam is idiomatically smooth.
   - Choose explicit style labels from AccoMontage2 (`Pop-standard`, `Pop-complex`, `Dark`, `R&B`) matched to section/song energy:
     - **`Pop-standard`**: Triad chords only (`I, ii, iii, IV, V, vi`) + basic inversions.
     - **`Pop-complex`**: Seventh, ninth (up to ninth chords supported in the curated progression library), and chromatic chord progressions.
     - **`Dark` / `R&B`**: Distinct style-label modes in AccoMontage2's progression library (choose dark minor/modal colors or extended R&B voicings via the companion *Ted Greene* & *OMTv2 Modal Mixture* guides rather than assuming fixed formulas inside AccoMontage2 itself).
3. **Macro-Level (Full-Song Cross-Phrase Coherence)**:
   - Evaluate the **2-bar boundary transition** between adjacent phrases (`last bar of Phrase A -> first bar of Phrase B`) so Verse → Pre-Chorus → Chorus → Bridge flows organically as a unified piece rather than disconnected 4-bar loops.

---

## 4. Classical Schemas in Popular Contexts (OMTv2)

- **Lament Schema (`1 – b7 – b6 – 5` / `i – bVII – bVI – V`)**:
  - Descending minor tetrachord in the bass; variants use minor `v`, major `I`, or passing first-inversion chords (`V6` between `i` and `bVII`, `IV6` between `bVII` and `bVI`). Syncopating the middle two chords leaves rhythmic space for a `V7` turnaround at the end of bar 4.
- **Circle-of-Fifths Schema (`i – iv – VII – III` or `vi – ii – V – I`)**:
  - Roots descend by 5th (`up a 4th`). In minor, `VII – III` naturally pivots like `V – I` into the **relative major** (`III`), making it an effortless bridge between a minor Verse and a relative-major Chorus. Chromatic sequences can turn each fifth-pair into an applied `ii–V`.
- *(For the complete table of 12-Bar Blues, Double/Extended Plagal, Doo-Wop, Singer/Songwriter, Hopscotch, and Puff schemas, consult `../../music-theory-harmony/references/harmony/omt-pop-and-neo-riemannian-schemas.md`.)*
