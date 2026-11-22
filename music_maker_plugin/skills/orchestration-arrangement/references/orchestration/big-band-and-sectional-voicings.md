# Big Band, Sectional Jazz Voicings & Latin-Swing Arranging

## 1. Standard 17-Piece Big Band Architecture (Evan Rogers & Frans Absil)

| Section | Instrumentation | Standard Doubles & Key Pitfalls |
|---|---|---|
| **Woodwinds (5)** | `Alto Sax 1, Alto Sax 2, Tenor Sax 1, Tenor Sax 2, Bari Sax` | Doubles: Altos -> Flute; Tenors -> Clarinet; Bari -> Bass Clarinet. **Avoid written low `Bb–C#` on all saxes** (honky/loud) and written middle `C#` (thin/out-of-tune); keep background pads inside the staff. |
| **Trumpets (4)** | `Tpt 1 (Lead)` + `Tpt 2, 3, 4` | Lead sits at staff top (`G4–D6`); use **Straight, Cup, or Harmon mutes** to drop brass energy cleanly behind saxes or solos (cup mute blends trumpets seamlessly between saxes & bones). |
| **Trombones (4)** | `Tbn 1, 2, 3` + `Bass Trombone` | Ultra-smooth homogeneous blend up to `G4`; `Ab4` tends flat/weak; avoid writing Bass Bone below bass clef in soft pads (`piano`) so players hold breath control. |
| **Rhythm (4)** | `Piano, Guitar, Upright/Electric Bass, Drum Kit` | **Rhythm Anticipation Rule (Davies)**: Horns anticipate harmonic changes (beat `4+` into beat `1`), while the **walking bass stays firmly on beat `1`** so time momentum never stumbles! |

## 2. Four-Way Close, Thickened Line & Chord-Tone Substitutions

To harmonize a jazz melody as a tight horn *soli* (**Thickened Line**, Tim Davies / Glenn Miller / Sammy Nestico style):

1. **Four-Way Close**: Place the melody on top and "peel downward" the next 3 chord tones directly beneath within a single octave.
2. **Avoid Top-Voice Minor 2nds (`m2`)**: Having `root` in melody over `maj7` directly beneath creates a harsh `m2` (or worse `m9` if dropped!) that sounds like a clam in bright horns. Fix immediately via **Chord Tone Substitution**:
   - **`Root` -> replace with `9` (or `b9` / `#9`)**: Solving `C over B` on `Cmaj7` -> voice `D (9)` underneath or convert **`maj7 -> 6`** (`A` instead of `B`) for classic smooth swing blend!
   - **`7` <-> `6`** (interchangeable for tonic warmth; avoids top-voice grind).
   - **`5` -> replace with `11`, `#11`, `13`, or `b13`** (when substituting `#11` on a major chord, **always also swap `Root -> 9`** so the inner voice pairs `9 + #11` cleanly as a `M3` instead of clashing `Root + #11`!).
   - **`3` -> `4`** (for `sus4` colors).

## 3. Five Methods for Harmonizing Non-Chord Approach Notes (Evan Rogers)

First harmonize all target chord tones cleanly, then harmonize each melodic **approach note** between them using one of 5 verified techniques (work **backwards** from the resolution chord!):

| Approach Technique | When to Use | Exact Voice-Leading Mechanism |
|---|---|---|
| **1. Chromatic Approach** | Approach note steps chromatically (`1 st`) into target chord tone | Slide ALL inner voices strictly by `1 st` in parallel into their target chord notes (`D#->E` takes entire block up/down 1 st) |
| **2. Diatonic Approach** | Approach note is inside active key/chord scale | Shift inner voices to adjacent diatonic steps inside the current scale (`key-of-the-moment` fidelity) |
| **3. Dominant Approach** | Approach note fits a `V7` or `V7alt` resolving to target | Harmonize approach note as `V7` (or `V7b9` / `ii-V7`) of the target chord; only needs rhythm section/horns to treat target briefly as temporary tonic |
| **4. Diminished Approach** | Root-less crisp `vii°7` passing motion (`V7b9` without root) | Build symmetric `dim7` chord (`minor 3rd` stack) resolving inward by half-step to target chord (Tim Davies default for fast sax runs!) |
| **5. Parallel Planing / Side-Slip** | Catch-all for any approach interval (step, 3rd, etc.) | Lock the exact intervallic shape of the target chord and **shift every voice uniformly** by the melody's interval (*thinking backwards from the resolution*) |

*Double-Neighbor / Enclosure Fix*: Either map the 2-note enclosure onto **`ii – V7(alt) – Target`** OR **chromatic/parallel plane backwards** from target -> approach 2 -> approach 1.

## 4. Expanding to 5 Voices: Octave-Lead, Drop-2, Drop-2+4 & Cascades

Because a big band sax section has **5 players** (`engine.voicing.drop2`, `drop3`, `drop24`):

1. **Octave-Doubled Lead**: Double Voice 1 (Alto 1) down 1 octave in Voice 5 (Bari Sax) with 3 inner close voices — punchy classic Big Band projection.
2. **Drop-2 Voicing**: Build a 4-way (or 5-tone) close block from top down -> **drop Voice 2 down 1 octave**. Throatier blend, spreads outer voices (`9th, 10th, 12th`), and resolves top-voice `2nd` rubs cleanly.
3. **Open / Drop-2+4 Voicing (`drop24`)**: Drop both **Voice 2 AND Voice 4 down 1 octave**. Gives rich orchestral chorale weight; Bari Sax often takes roots/5ths at phrase arrivals without dragging fast swing tempos (note: Bari Sax can play roots with the saxes while Upright Bass keeps walking!).
4. **Quartal & "So What" Voicings**: Reserve `quartal_stack` / `so_what_voicing` (`[0, +5, +10, +15, +19]`) for slow/medium sustained melody hits or modal textures—avoid in fast bebop lines.
5. **Shock Voicings & Cascades**:
   - *Shock*: Pack tight `m2` / tritone clusters framed so top melody and bottom bass resolve cleanly by `1 st` into the target chord.
   - *Cascade*: Start a phrase in crisp unison/octaves, then **split voices one-by-one or symmetrically into full harmony** ONLY at the final phrase punctuation (never split too early on a weak offbeat!).

## 5. Background Spread Pads, Dissonance Arc & Low Interval Guard

- **Build Pads Bottom-Up**: Anchor root (or bass Trombone `10th/5th/octave` above bass) -> secure **Guide Tones (`3` & `7`)** -> layer upper extensions (`9, 11, 13`) smoothly so no inner part leaps erratically, and **leave room for the horns to breathe**.
- **Low Interval Rule (Evan Rogers)**: **Below the middle line of the bass staff (`D3`), keep intervals strictly consonant—ideally `10ths`, `5ths`, or `octaves`!** Close thirds/2nds below `D3` create mud instantly in timbrally matched horn sections (`review_song.py -> register_clumps` + `low_intervals`).
- **Manage the "Dissonance Factor" Tension Arc**: Align inner voicing dissonance (`m2` / `b9` rubs) to peak on dominant/climax chords and **open out** (`quartal` or drop-spread without `m2` rubs) on resolved tonic chords (e.g., omit the `5th` in `Cmaj7#11` if it rubs `m2` against `#11`!).
- **Impact Spreads (Polychordal Shout Climax)**: Assign Upper Structure triad to **Trumpets (Voices 1–3/4)** and Lower `R-3-7` shell/spread to **Saxes & Trombones** (`US / Polychord` family separation).

## 6. Big Band Swing vs. Latin Pocket Integration (Absil)

- **Swing Rhythm & Notation**: Write eighth-note swing lines evenly (interpreting ratio ~`2:1` triplet feel -> softer at faster tempos); ride cymbal carries continuous 4-beat `spang-a-lang` pattern (`sticks` in loud *f*, `wire brushes` in soft *p* ballad/intimate sections).
- **Afro-Cuban / Latin Clave Lock**: Anchor all horn hits, piano *montuno*, and bass *tumbao* cleanly to either **`3-2` or `2-3` Son / Rumba Clave** (never cross the clave side mid-phrase!); bass emphasizes beat `2+` and anticipates the **`1` of the next bar** (`tumbao`) alongside conga low open hits.
