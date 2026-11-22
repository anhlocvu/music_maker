# Solo Rhythm Vocabulary, Phrasing & Climax Architecture

Pitches alone sound robotic if rhythm stays locked to downbeat starts and square 8th-note chains. Apply empirical phrasing distributions and macro compositional arcs to make solos breathe like a live master soloist.

## 1. Empirical Phrase Statistics (Mark Watkins Ch. 3 — Charlie Parker 12-Solo Study)

Use these observed distributions as stylistic targets rather than uniform beat-1 phrasing:

### A. Phrase Beginnings (~70% Launch BEFORE the Downbeat!)
| Phrase Launch Position | Empirical Share | MIDI Implementation Rule |
|---|---|---|
| **Upbeat Start (`and` of beat)** | **56%** | Start majority of phrases on `&` of beat 1, 2, 3, or 4 |
| **Drag / Multi-Note Pickup** | **~13–15%** | Launch 2–4 rapid pickup notes before beat 1 |
| **Direct Downbeat Start** | **~25%** | Reserve direct beat-1 entries (~1/4 of phrases) for high-impact thematic statements |

### B. Phrase Endings (4 Canonical Archetypes + Other)
| Ending Archetype | Empirical Share | Articulation & Duration Shape |
|---|---|---|
| **Long Upbeat (`Do-dah` / `Do-wah`)** | **30%** | Phrase terminates on an accented upbeat held over/into the bar |
| **Short Upbeat (`Bebop`)** | **24%** | Crisp, clipped final upbeat cutoff |
| **Short Downbeat (`Bop`)** | **10%** | Signature downbeat punch lasting roughly **`2/3` of a beat** (`The Bop`) |
| **Long Downbeat (`Dah`)** | **7%** | Sustained final downbeat (paired with subtle terminal vibrato) |
| **Other + Basie-ism** | **29%** | Syncopated tags, rests, or delayed 3-note Basie-style sign-offs |

---

## 2. Articulation, Ghost Notes & Swing Feel Nuances

- **Foundational Swing Articulation**: **Tongue the upbeat, slur into the downbeat** (appears purely in **~28–32%** of Charlie Parker lines, interwoven with alternating tongued and slurred accents).
- **Ghosted / Half-Tongued Upbeats**: Lower MIDI velocity (`~45–65%` of accent velocity) on upbeats leading into crisp, high-velocity (`~95–115`) downbeats—creates instant horn/vocal bounce instead of flat machine-gun 8ths.
- **Terminal Vibrato**: Avoid constant vibrato from note onset; hold sustained phrase endings steady first, then apply **subtle below-pitch vibrato (`2–3` pulses)** across the final third of the note (using delayed `Track(..., vibrato=(freq, cents, delay_sec, onset_sec))` or a custom below-pitch terminal `t.bend(..., curve=[(0.0,0.0), (0.65,0.0), (0.72,-0.35), (0.80,0.0), (0.88,-0.35), (0.95,0.0), (1.0,0.0)])`).
- **Contour-Accent Coupling**: Place dynamic velocity peaks on ascending contour turns and structural upbeat targets rather than every beat evenly.
- **Triplets & Swing-Grid Turns**: Use ascending, descending, horizontal, and paired 8th-note triplets alongside **turns** (`16th-note triplet + 8th note` aligned to swing triplets).

---

## 3. Rhythm Blocks & Four Target Landing Positions

Break solo rhythm away from predictable barline grids by assembling half-bar **Rhythm Blocks** (**1-, 2-, 3-, and 4-note cells**):
- Transform blocks via: **internal rests, ties across the barline, triplets, rhythmic displacement (shifting a motif by an 8th or beat), and pickups**.
- Aim phrase tails deliberately at four target rhythmic positions relative to the bar/chord change:
  1. **On**: Exact downbeat arrival
  2. **Half-way**: Mid-beat / upbeat (`and`)
  3. **Ricochet**: Short off-beat bounce kicking into the next bar
  4. **Almost**: Anticipated arrival (`&` of 4) stealing forward into the coming harmony.

---

## 4. Improvisation as Composition: Climax, Space & Form (Mark Watkins Ch. 11 & 13)

### Golden Mean Climax Arc (`0.618` / `~2/3` Mark)
Plan the entire solo as one dramatic sentence peaking around **61.8%–67% (`~2/3`)** through its total chorus count via **four coupled levers**:
1. **Note Density**: Sparse lyrical motifs -> denser 8th/16th/triplet bursts -> relaxing tail
2. **Rhythmic Complexity**: On-beat anchors -> syncopated displacements & tuplets -> settled cadences
3. **Pitch Range**: Comfortable mid-register opening -> upper-register peak near Golden Mean -> warm return
4. **Dynamics / Velocity**: Mezzopiano/mezzoforte breath -> fortissimo climax -> composed tag resolution.

### Space Discipline & Section Delineation
- **Avoid Run-On Sentences**: Leave deliberate **1–4 beat rests (breathing space)** between early phrases; **gradually diminish space** as the solo builds toward its `0.618` peak.
- **Boundary Activity Surge**: Signal upcoming 4-bar and 8-bar structural landmarks—especially **bar 4 leading into bar 5** and the **end of an A-section chorus launching into the bridge**—with increased rhythmic/harmonic momentum.
- **Prune Over-Busy Starts**: Use learned cell patterns as *departure points*, and intentionally **edit out clutter at phrase beginnings** so motifs feel conversational rather than front-loaded exercises.

### Standard Forms & Live Arrangement Slots
- **Core Forms**: `AAB` (12-bar blues), `AAA`, through-composed blues, `AABA` (32-bar rhythm changes / standards), `ABAB`, `AABC`, `ABA (14+8+14)`.
- **Four-Bar Question / Answer**: Frame bars `1–4` as an open antecedent (`question`, ending on unstable `3, 5, 7, 9`) answered by bars `5–8` (`answer`, resolving onto stable `1, 3, 5` or leading into the next harmonic brick).
- **Arrangement Slots**: Coordinate solo entries and exits across **Intro -> Head -> Lead-in / Kick -> Solo Chorus (with optional Backgrounds behind 2nd+ chorus) -> Interlude -> Solo Break (unaccompanied 2–4 bar launch) -> Head Out -> Tag / Coda**.
