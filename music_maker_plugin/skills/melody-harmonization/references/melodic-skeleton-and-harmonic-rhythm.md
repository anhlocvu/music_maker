# Melodic Skeletons, Key/Mode Diagnosis, Harmonic Rhythm & Divorce Layers

Distilled strictly from Trevor de Clercq (*Some Reharmonization Techniques for Popular Music*, 2018; *The Harmonic-Bass Divorce in Rock*, 2019; *Tempo versus Average Rates of Harmonic Rhythm*, 2023), David Temperley & Trevor de Clercq (*Statistical Analysis of Harmony and Melody in Rock Music*, 2013), Wu et al. (*AutoHarmonizer*), and *Open Music Theory v2* (Modal Schemas & Pentatonic Harmony).

---

## 1. Beat Strength & Melodic Skeleton Extraction (No Naive Note-Chasing)

Traditional classical chorale exercises harmonize almost every melodic note on every beat. In popular, ballad, R&B, and contemporary songwriting, melodies are rhythmically syncopated and decorated with non-chord tones—chasing every note with a new chord produces frantic, unnatural harmony.

### 1.1 Beat-Strength Weighting (AutoHarmonizer)
Tag every melodic frame by its metrical position (`0–3`):
- **`3` — Strong beat** (downbeat / beat 1 of bar): Highest priority for harmonic anchoring. Most human chord onsets occur here.
- **`2` — Medium-weak beat** (e.g., beat 3 in `4/4`): Second priority for chord changes (`0.5`-bar harmonic rhythm or pre-cadence acceleration).
- **`1` — Weak beat** (beats 2 and 4 in `4/4`): Fewer chord onsets; often melodic passing/neighbor motion.
- **`0` — Non-beat** (off-beat / syncopated 8th or 16th): Rarely initiates a chord unless used for a deliberate syncopated anticipation (push).

### 1.2 Melodic Skeleton Reduction (de Clercq 2018)
Streamline any complex/syncopated melody into **1–2 structural scale degrees per measure** (its **Melodic Skeleton**) before choosing chords:
1. Keep notes that are **held for longer duration** (duration modeled in Temperley & de Clercq 2013 as inter-onset interval capped at 1 bar), **occur on strong beats (`2–3`)**, or sit at **phrase beginnings/endings** or original chord tones.
2. Treat short stepwise notes between skeleton tones as **proper non-chord tones** (specifically notes within 1–2 semitones of the immediately following tone, per *AutoHarmonizer* `CTnCTR` logic) rather than forcing chord changes beneath them.
3. **Bidirectional Context**: Select each chord considering both the **current skeleton tones** and the **upcoming melodic phrase goal** (look-behind + look-ahead), avoiding greedy one-note-at-a-time choices that overuse `I` triads.

---

## 2. Key/Mode Diagnosis & Scale-Degree Reality in Popular Music

From Temperley & de Clercq (2013, 200-song corpus; 97% key-finding accuracy):
1. **Duration-Weighted Melodic Profile**: Weight each melodic pitch by its sounding duration (until the next onset, or 1 bar max). Phrase-final long notes carry high tonal weight.
2. **Metrical Weighting of Odd vs. Even Bars**: In 4-bar hypermeters, **odd-numbered bars (bars 1 and 3)** are metrically stronger and favor tonic chords more strongly than even-numbered bars.
3. **Popular Music Scale Realities**:
   - **The Supermode**: Both melodic and harmonic pop/rock corpora freely draw on all 12 chromatic scale degrees **except `b2` and `#4`** (though `b6` is relatively rare melodically).
   - **`b7` vs. `7`**: Unlike classical music where leading-tone `7` dominates, **melodic `b7` (`te`) is more common than `7` (`ti`) overall** in popular melodies.
   - **Pentatonic Union (`1–2–b3–3–4–5–6–b7`)**: Second most common melodic scale vector after major Ionian (`1–2–3–4–5–6–7`). Major pentatonic (`1–2–3–5–6`) dominates major melodies; minor-melody songs frequently mix `b3`, `3`, `nat-6`, and `b7`.
   - **Minor/Major Cross-Relation (`me` over major `I`)**: Very common in blues-rooted rock, soul, and R&B—a melody highlighting `b3` (`me`) can validly sit over a major tonic triad (`I` or `I7`).

### Modal Color-Note Identification (OMTv2)
Identify modal flavor by tonic third quality (`mi` major vs. `me` minor) plus **characteristic color notes**:
- **Mixolydian**: Major tonic + lowered `b^7` (`te`) → `bVII` (dominant-substitute function), schemas `bVII–IV–I` (Double Plagal), `I–bVII` (Subtonic Shuttle).
- **Aeolian**: Minor tonic + `le` (`b^6`) & `te` (`b^7`) → `bVI` (subdominant) and `bVII` (dominant), avoiding leading-tone `ti`; schemas `i–bVII`, `i–bVII–bVI–bVII`, `bVI–bVII–i` (or Picardy `bVI–bVII–I`).
- **Dorian**: Minor tonic + raised `^6` (`la`) → **major `IV` chord** (primary marker in funk, disco, soul); schema `i–IV`.
- **Lydian**: Major tonic + raised `#^4` (`fi`) → **major `II#` chord** (not resolving to `V`); schemas `I–II#`, `II#–IV–I` (where `IV` neutralizes `fi -> fa`).
- **Pentatonic Harmony**: Roots drawn from pentatonic rotations (`1, b3, 4, 5, b7` or `1, 2, 3, 5, 6`) supporting parallel major triads or power chords, producing `mi/me`, `la/le`, `ti/te` cross-relations (e.g., *Higher Ground*, *Hey Joe* quintuple plagal `bVI–bIII–bVII–IV–I`).

---

## 3. Harmonic Rhythm Budgeting (`~2s` Perceptual Ideal)

From de Clercq (2023, empirical study across Rolling Stone, McGill Billboard, and NN corpora):
- **Core Rule**: Chord durations in popular music gravitate toward an **ideal absolute span of ~2.0 seconds** (Table 4 grand medians `1.66–2.43 s`, grand geomeans `1.74–2.50 s`, normally bounded between **`1.0 s` and `4.0 s`**; `< 0.5 s` or `> 8.0 s` is rare), largely **independent of BPM**. Use `chord_bars ≈ BPM / 120` in `4/4` (rounding to `0.5`, `1.0`, or `2.0` bars) for continuous pacing across all tempos, guided by de Clercq's empirical bands:
  - **Slower Tempos (`50 – 90.5 BPM` Study 2 bin; `~94.5–108.3 BPM` Study 1 median)**: Tend toward **half-bar (`0.5` bar)** chord changes so slow ballads do not drag past ~3–4 s.
  - **Medium Tempos (`108.8 – 122.7 BPM` Study 2 bin; `~112–120 BPM` Study 1 median)**: Tend toward **1-bar (`1.0` bar)** chord changes (~2 s per chord).
  - **Faster Tempos (`138.3 – 240 BPM` Study 2 bin; `~130–139 BPM` Study 1 median)**: Tend toward **2-bar (`2.0` bar)** chord changes so harmony does not blur too fast.
  - *(For intermediate transition tempos such as `91–108` or `123–138 BPM`, compute `(chord_bars * 240) / BPM` in `4/4` and pick `0.5`, `1.0`, or `2.0` bars closest to `2.0 s` according to section energy.)*
- **Density Control (*AutoHarmonizer* `Γ` insight)**: Vary chord-change frequency and chord vocabulary across sections—sparser/longer changes in verses or intros, denser changes and non-tonic (`ii`, `vi`, `IV`) substitutions in pre-choruses and cadences. Never output mechanical identical chord-change spacing in every bar of a full song.

---

## 4. Melodic-Harmonic & Harmonic-Bass Divorce (3 Pitch Layers)

Following Allan Moore, David Temperley, Drew Nobile, and Trevor de Clercq (2018, 2019), treat popular/modern harmony as **three potentially independent pitch layers** (plus the explicit drum/beat layer):
1. **Melodic Layer** (vocal / lead topline)
2. **Harmonic Filler Layer** (piano/guitar/pad chords)
3. **Bass Layer** (bass guitar / synth bass / LH root)

### 4.1 Three Types of Divorce (Apply Intentionally, Not Randomly)
- **Hierarchy Divorce**: One layer operates on a deeper structural level while another moves locally:
  - *Melodic-Harmonic Hierarchy*: Melody prolongs the tonic pentatonic scale (`1–2–3–5–6`) while chords shift underneath without forcing every melodic note to match the local triad. Often follows Temperley's **"Loose Verse, Tight Chorus" (LVTC)** model—melody floats freely in the verse, then locks tightly into chord tones at chorus cadences.
  - *Harmonic-Bass Hierarchy (Pedals)*: Traditional **bass pedal** (`I–IV–V` over `^1` bass) OR **upper/inverted pedal** (sustained tonic triad or `^1+^5` power chord in piano/guitar over a moving bass line `I–V–vi–IV`, creating **hybrid / slash chords** such as `D/B` or `D/G`).
- **Syntax Divorce**: Layers diverge on the musical surface yet converge toward a **shared structural cadence**:
  - *Melodic-Harmonic Syntax*: `^3–^2` in melody over `iv` resolving to `^1` over `I`.
  - *Harmonic-Bass Syntax*: `IV` triad in upper voices over `^5` in the bass (`F/G`, `Ab/Bb`, i.e. **`V9sus4` / "pop-soul dominant"**) approaching `I`, or upper voices slipping chromatically by half-step while the bass executes a `ii–V` root motion.
- **Loop Divorce**: A repeating 2-to-4-chord ostinato loops statically in one layer while the melody (or bass) articulates phrase boundaries. In harmonic-bass loop divorce, the standard blueprint is: **Hierarchy Divorce → Loop Divorce → Cadential Syntax Divorce**.
  - *Texture Limit Warning (de Clercq 2019)*: Do **not** overload all three layers in simultaneous divorce while a vocal melody is singing; keep loop/harmonic-bass divorce strongest in intros/interludes or link vocals to the upper triadic layer so the mix stays intelligible.

### 4.2 Bass-Driven Meta-Schemas (de Clercq 2018; Doll 2017)
When classic functional `V–I` syntax is absent or basic progressions feel aimless, design the **bass line first** using linear **Meta-Schemas** (chromatic or stepwise fragments heard clearly in the lowest voice):
- **Descending Bass ("Drooping / Dropping + Slouching / Lament")**: `1–7–6–5` diatonic descent (`I – I42 – vi7 – V`), `1–b7–b6–5` minor tetrachord, or chromatic descent from `b7` down to `4` ("dropping" `[b7–5]` + "slouching" `[5–4]`): `I – bVII – IV6 – bVI – I64 – V65/V – IV – iv – I` (bass `1–b7–6–b6–5–#4–4`).
- **Ascending Bass ("Swelling + Stretching")**: Chromatic ascent from `3` up to `6` ("swelling" `[4–5]` + "stretching" `[5–6]`): `I – iii7 – IV – V65/V – I64 – V65/vi – vi – V6 – I` (bass `1–3–4–#4–5–#5–6–7–1`).
- **Mirrored Contour**: Notice the melodic skeleton's macro-shape (e.g., double-neighbor around `^3`) and mirror or run contrary motion in the bass (`I – bVII – ii – IV – I`).
