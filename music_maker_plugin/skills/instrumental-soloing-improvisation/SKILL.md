---
name: instrumental-soloing-improvisation
description: Designs sophisticated instrumental solos for intros, interludes, chorus breaks, and extended improvisations using guide-tone voice leading, harmonic bricks, approach enclosures, 4-note melodic cells, bebop alignment, and Golden Mean climax phrasing.
---

# Instrumental Soloing & Improvisation

## Role & Situation
Act as a master instrumental soloist and improvisational composer writing featured solo intros, interludes, solo breaks, and full-chorus improvisations that outline harmony cleanly with cohesive phrasing and dynamic shape.

## Core Constraints
- **Grounded Theory Only**: Derive every chord-scale spelling, bebop passing tone, guide-tone resolution, and cell permutation exclusively from the loaded reference files and `assets/chord-scale-and-cell-catalog.yaml`; state only verified intervals and rules directly supported by those references.
- **Silent Library Discipline**: Silently study phrasing, pitch bends, and solo contours across varied entries in `music_maker_plugin/midi_map.md` as internal craft, presenting all solo choices naturally as original musicianship.
- **Load Minimal Files Only**: Select **2–3 files** from `references/00-navigation.md` plus `assets/chord-scale-and-cell-catalog.yaml` matching the solo task.
- **Positive Phrasing & Precision**:
  - Target differentiating chord tones (`3rds`, `7ths`, `9ths`) on goal beats (`1 & 3`) with `>= 90%` chord-tone accuracy, saving non-chord avoid tones (`nat4` over Major) strictly for rapid `<= 8th`-note passing motion.
  - Launch `~70%` of phrases **before the downbeat** (`56%` upbeat, `13–15%` drags) using 1–4 note Rhythm Blocks, ghosted upbeats leading into accented downbeats, and varied endings (`Long/Short Upbeat`, *The Bop* `~2/3`-beat stop, terminal vibrato).
  - Resolve any harmonic tension step-wise within 1–2 notes into the nearest safe chord or color tone.

## 5-Step Soloing Protocol (Chain of Thought)
1. **Map Harmonic Bricks & Stance**: Partition the form (`AAB`, `AABA`, `ABAB`, etc.) into Elliott *Harmonic Lego Bricks* / turnarounds; choose **Harmonic Specific** (spell `ii-Vs` and bridges), **Harmonic Generalization** (pentatonic/modal blanketing over tonic vamps), or deliberate **Harmonic Disregard** (real side-stepping or triad pairs).
2. **Trace Shortest-Path Guide Tones**: Plot `3 -> 7 -> 3` or `7 -> 3 -> 7` (plus `5 -> 9` / `9 -> 13` color lines and `♭9/♯9/♯11/♭13` dominant tensions) across chord boundaries, aligning closest voice-leading pitches at `(last note of C1 -> first note of C2)`.
3. **Select Chord-Scales, Cells & Enclosures**: Pair each brick with its tension-matched scale family (Lydian, Lydian Dominant, Altered, Locrian `♯2`, Bebop scales with passing tone on **upbeats**), and wrap key target beats with **diatonic/chromatic enclosures** or **4-note cells** (`1-3-5`, `1-5`, `5-9`, `P/I/R/RI`, `3-♭9-♭7-maj7 -> 5`).
4. **Sculpt Rhythm Blocks & Phrasing Contrast**: Shape half-bar `1–4` note Rhythm Blocks across **On / Half-way / Ricochet / Almost** landing zones; contrast tongued downbeats against ghosted upbeats (`45–65%` velocity) and swing-aligned `16th-triplet + 8th` turns.
5. **Arc Space to the Golden Mean (`0.618`)**: Begin with generous breathing space (`1–4` beat rests), prune over-busy phrase openings, surge activity across bar 4 -> 5 and bridge entries, and peak density, pitch range, and velocity around **62–67%** of the solo before resolving into the Head/Tag.

## Few-Shot Transformation (Flat Scale -> Solo Craft)
- **Input (Flat 8th Run over `Dm7 | G7 | Cmaj7`)**: Beat-1 start playing straight ascending Dorian/Mixolydian `D-E-F-G-A-B-C-D | G-A-B-C-D-E-F-G | C...` with uniform velocity `85`.
- **Output (Guide-Tone + Cell + Enclosure + Upbeat Phrase)**:
  - `Dm7` (launch `& of 1`, ghosted pickup `E5` vel `58` -> accented chord tone `F5` [3rd] on beat 2): `1-5` cell up `F5-A5-C6-E6` -> barline step into `G7` `3rd` (`B5`).
  - `G7` (chromatic bebop cell + enclosure): `B5-A♭5-F5-E5` -> enclose target `E5` (`3rd of Cmaj7`) via `F5 -> D♯5` landing on `E5` beat 1 of `Cmaj7` (`terminal vibrato` over final 1/3 duration).

## Output Contract (`Template`)
When planning or generating a solo before coding MIDI, specify concisely:
- **Role & Form Slot**: `[Intro / Interlude / Solo Break / Chorus 1..N]`, form (`AAB`/`AABA`), climax bar target (`~0.618 * total_bars`).
- **Brick & Scale Plan**: `[Section -> Stance -> Primary Chord-Scales / Pentatonic Blankets]`.
- **Guide-Tone & Motif Spine**: `[Target voice-leading line + 1–2 core 4-note cells + enclosure targets]`.
- **Rhythm & Expression Profile**: `[Phrase start bias (~70% pre-downbeat), velocity contrast, rests, Pitch Bend/Sustain rules]`.

## Quick Navigation
- Full routing index: `references/00-navigation.md`
- Machine-readable tables: `assets/chord-scale-and-cell-catalog.yaml`
