# Melody Harmonization & Reharmonization Pre-Render Checklists

Use this operational checklist whenever harmonizing a melody, designing chord changes from scratch, or reharmonizing an existing progression.

---

## 1. Pre-Composition & Pre-Arrangement Audit (5-Gate Check)

- [ ] **Gate 1 — Melodic Skeleton & Beat Strength (No Naive Note-Chasing)**
  - Separated syncopated/ornamental notes (`beat_strength = 0–1`) from structural anchor pitches (`beat_strength = 2–3`, sustained notes, phrase goals)?
  - Identified whether any phrase uses **Melodic-Harmonic Divorce** (e.g., static pentatonic vocal riff over a 4-chord loop, or "Loose Verse, Tight Chorus")?
- [ ] **Gate 2 — Key/Mode & Harmonic Rhythm (`~2s` Ideal)**
  - Diagnosed tonal center using both pitch duration and metrical weight (strong odd-bar downbeats), checking modal color tones (`te` = Mixolydian, `le+te` = Aeolian, `la` in minor = Dorian, `fi` = Lydian)?
  - Verified chord duration sits near the **1.0s–4.0s (~2.0s midpoint)** perceptual window (`chord_bars ≈ BPM / 120` in `4/4`; slow 50–90.5 BPM / median 94.5–108.3 ≈ half-bar; medium 108.8–122.7 BPM / median 112–120 ≈ 1 bar; fast 138.3–240 BPM / median 130–139 ≈ 2 bars), accelerating only at pre-choruses/cadences?
- [ ] **Gate 3 — Cadence-First & 3-Level Scoring**
  - Locked phrase endings (`HC`, `IAC`, `PAC`, `Aeolian bVI–bVII–i/I`, `Double Plagal bVII–IV–I`, `Minor Plagal IV–iv–I`) and strong predominants (`ii6`, `IV`, `iiø7`) before filling phrase middles?
  - Checked **Micro** (strong-beat melody notes sit on chord tones or valid 9/11/13/altered extensions—no unintentional avoid-note clashes), **Meso** (chord phrase aligns with 4/8-bar melodic phrases), and **Macro** (smooth cross-section pivots)?
  - Evaluated **Fragile / Emergent / Absent Tonic** options for Verse vs. Chorus emotional lift?
- [ ] **Gate 4 — Bass-Line Meta-Schema & Divorce Hygiene**
  - Does the bass trace a purposeful line (stepwise/chromatic descent `1–7–6–5` or `1–b7–6–b6–5–#4–4`, ascending `1–3–4–#4–5–#5–6–7–1`, contrary motion against melody, or intentional pedal/hybrid chord)?
  - If using **Harmonic-Bass Loop Divorce**, is it kept clear of dense competing vocal counterlines or resolved via cadential **Syntax Divorce**?
- [ ] **Gate 5 — Restraint & Voice-Leading Verification**
  - Did every applied `b5` tritone sub, `ii–V` back-cycle, `1/2-step` approach, or `CT°7` avoid clashing with the top melody note?
  - Are upper voices spaced cleanly (wide low, close high), omitting unneeded 5ths, keeping extensions (9, 13) above the 7th, and connecting `3 -> 7` / `9 -> 13` smoothly?
  - Is restraint honored ("less is more"—targeted color at pre-choruses, bridges, second As, and final choruses rather than busy chord-swapping everywhere)?

---

## 2. Diagnostic Troubleshooting Matrix

| Symptom | Root Cause | Grounded Fix |
|---|---|---|
| Chords jump frantically every beat over a vocal line | Harmonizing non-chord tones instead of the Melodic Skeleton | Filter to `beat_strength 2–3` & sustained notes; slow Harmonic Rhythm toward `~2s` per chord (de Clercq 2018/2023, AutoHarmonizer). |
| Progression sounds flat, generic, or `I`-heavy | Overuse of root-position `I–IV–V–vi` triads; uniform harmonic rhythm | Shift weight toward `ii` and `vi`; apply **Fragile/Emergent Tonic** (Spicer/OMTv2), **Modal Mixture** (`iv`, `iiø7`, `bVI`, `bVII` via `le`), or a bass **Meta-Schema** (de Clercq 2018, AutoHarmonizer). |
| Vocal pentatonic melody clashes with chord-by-chord triads | Ignoring **Melodic-Harmonic Divorce** | Allow pentatonic topline to float in Verse (*Loose Verse, Tight Chorus*), then lock tightly into chord tones at Chorus cadences (Temperley 2007, Nobile 2015, de Clercq 2018/2019). |
| Reharm feels "forced" or hurts the singable melody | Blind `b5` tritone sub or altered extensions under a fixed melody note | Check top-note interval first: swap to **Companion `m7`/`dom7sus`**, **3rd Substitution**, or **Scalewise/Contrary Bass** instead of forced `b5` (Ted Greene 1973–1976). |
| Turnaround or phrase ending feels static | Direct `V7 -> I` or overly long static `I` chord | Insert **Applied `V7`/`ii7`**, **Back-Cycle `III7–VI7–II7–V7`**, **`CT°7`**, or **Pre-Destination Approach** (`Abm7–Db7 -> C`, `D7–Dbmaj7 -> C`) (OMTv2, Ted Greene 1977). |
| Arrangement sounds muddy or boxy in low mids | Close intervals in bass register or 13th voiced below 7th | Space via **Harmonic Series** (wide low, close high), omit 5th, voice `3–7` in lower-mid and `9–13` on top (OMTv2 Jazz Voicings). |
