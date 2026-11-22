# Pitch-Bend Target Grammar & Multi-Instrument Execution

Every pitch bend is a **pitch motion from an unbent origin note to an intentional harmonic or melodic destination**—never an arbitrary excursion in cents. Lock the target pitch (`start_note -> target_note`) before computing semitones (`delta = target_midi - start_midi`).

## 1. Arrival-Pitch Model & 4-State Grammar

Represent monophonic bent passages as transitions across four discrete bend states (D'Hooge, Bigo & Déguernel, ISMIR 2023):

| State | Symbol | Definition & Arrival Pitch | Musical Function | Toolkit Representation |
|---|---|---|---|---|
| Unbent | `∅` | Neutral wheel (`8192` / `0 st`); sounding pitch equals written note | Stable anchor, clean chord tone, release floor | Normal note or `0` stage |
| Ascending | `↑` | Starts at written fret (`0 st`) and bends up (`+Δ`) to `target = written + Δ` | Emotive upward approach into a scale/chord tone | `scoop`, `delayed_bend`, `bend_release` (`0 -> +Δ -> 0`) |
| Pre-bent / Held | `→` | Note begins or continues already elevated at `+Δ`; sounding pitch equals `written + Δ` | Held climax tension, pre-bent sigh entry, re-plucked top pitch | `pre_bend`, sustained peak, `dive` (`+Δ -> 0`) |
| Descending | `↓` | Pitch drops from `+Δ` back down to unbent floor (`0 st`), arriving on `written` | Resolution down to chord tone, trailing sigh | `bend_release` release leg, `pre_bend` release |

### Empirical Lead-Guitar Corpus Rules (D'Hooge et al. 2023)
Measured across 932 guitar lead tracks (GPtabs) and random-forest feature importance analysis:
- **Selectivity**: Only **~10%** of notes in lead guitar solos are bent (and **~2.5%** across general tracks). Keep ~90% of notes clean so bends remain focal accents.
- **Single-Note Dominance**: **88%** of bent events occur on single notes (vs. 12% chordal/double-stop). Use dedicated single-voice channels or MPE when bending inside polyphony (Kim, Choi & Nam, 2024 `guitarroll` per-string modeling).
- **Fretboard Window**: Bends concentrate on the **top three treble strings** in middle-neck positions (**frets 5–15**), where string tension allows controlled `+0.5st` to `+2.0st` pulls (Varieschi & Gower, 2009: fretting and stretching elevate wire tension per Mersenne's law, requiring active pitch target compensation).
- **Metric & Duration Placement**:
  - `↑` and `↓` prefer **strong beats** and **longer durations** than the preceding note (top decision predictors: current pitch `0.20`, jump to `n+1` `0.17`, jump from `n-1` `0.16`, duration `0.14`).
  - `→` (re-plucked held bend) tends to fall on **offbeats**, sustaining peak tension.

---

## 2. Scale-Degree Target Tables (Positive Destination Rules)

Before writing a bend, choose `target_note` from the active **chord** first (3rd, 5th, root, 7th, 9th), then **scale tones** or **blue-note curls**. Avoid half-step bends that land on unresolved avoid tones unless explicitly framed as a blue curl (`+0.35` to `+0.5 st`).

### Minor Pentatonic & Blues Targets
| Scale Degree Origin | Destination Degree | Semitones (`+Δ`) | Idiomatic Usage |
|---|---|---|---|
| `♭7` | `1` (Root) | `+2.0 st` | Classic chorus/solo climax arrival on root |
| `4` | `5` | `+2.0 st` | Primary guitar solo peak; pair with vibrato at top or release (`4 -> 5 -> 4`) |
| `4` | `♭5` (Blue note) | `+1.0 st` | Grit tension; release back to `4` or slide down to `♭3` |
| `♭3` | `3` (Major 3rd) | `+1.0 st` | Gospel/blues turnaround lift over Dominant (`I7` / `IV7`) |
| `♭3` | `3♭` micro-curl | `+0.35 to +0.5 st` | Subtle blues inflection before resolving down to `1` |
| `♭3` | `4` | `+2.0 st` | High-register emotional cry (`1 -> ♭3^4`) |

### Major, Mixolydian & Pop-Ballad Targets
| Scale Degree Origin | Destination Degree | Semitones (`+Δ`) | Idiomatic Usage |
|---|---|---|---|
| `2` | `3` (Major 3rd) | `+2.0 st` | Sweet ballad phrase apex (resolving smoothly to chord 3rd) |
| `4` | `5` | `+2.0 st` | Singing climax bend over Tonic or Subdominant |
| `7` (Leading tone) | `1` (Octave) | `+1.0 st` | Half-step vocal-style resolution (`ti -> do`); crisp intonation essential |
| `5` | `6` | `+2.0 st` | Lyric country/pop lift before `5 -> 3` descent |
| `6` | `1` / `♭7` | `+1.0 st` (Mixolydian `6 -> ♭7`) or `+2.0 st` (Minor `♭6 -> ♭7`) | Modal lift into turnaround |

### Pre-Bends & Unison / Oblique Bends
- **Pre-Bend Sigh (`pre_bend` / `→` then `↓`)**: Bend silently up to the upper chord/scale tone (`+1.0` or `+2.0 st`) before plucking, strike at `+Δ`, hold briefly, then release to the written lower scale tone (`e.g., G5 pre-bent +2st -> A5, falling to G5`). Use strictly descending into a strong chord tone (root, 5th, 3rd).
- **Unison Bend**: Play `target_note` stationary on a higher string (Channel/Track A) while bending `target_note - 2st` up `+2.0 st` on a lower string (Channel/Track B) so beating narrows into pure unison.
- **Pedal-Steel Oblique Bend**: Hold a fixed chord top tone on Track A while Track B bends an inner voice (`2 -> 3` or `4 -> 5`) upward underneath.

---

## 3. Cross-Instrument Monophonic Bending (Strings, Erhu, Winds, Bass, Lead Synth)

Non-fretted bowed strings and expressive monophonic leads use rapid, non-overlapping technique contours (Wang et al., 2019 Erhu taxonomy: `slide up`, `slide down`, `slide legato`, `trill`, `trill up short`, typical gesture window `0.15–0.20 s`):
- **Bass (`scoop` / `glide`)**: Keep `95%+` of bass notes centered cleanly on `0 st`. Use quick `+1.0 st` or `+2.0 st` `scoop` (15–20% of note onset) on chromatic leading tones (`7 -> 1`) or fretless octave climbs (`~0.15–0.25 s`). Never widen sustained bass bends across rhythmic kicks.
- **Bowed Strings / Solo Erhu / Violin / Cello**: Use clean diatonic `scoop` entrances (`-1.0 st` or `-2.0 st` from lower scale neighbor into `0 st`) on emotional downbeats, plus `bend_vibrato` with gentle depth (`0.12–0.22 st`) starting only after the initial pitch settles (`~25%` delay). Keep technique windows non-overlapping.
- **Lead Synth**: Match RPN pitch-bend range cleanly (`±2 st` for guitar/vocal expression; `±12 st` strictly for deliberate portamento/octave drops). Always return pitch wheel to `0` (`8192`) before the next articulated step.

---

## 4. Mapping Target-Aware Bends to `soundfont-music`

1. **Inline Shorthand & Explicit `target=`**:
   ```python
   # Target pitch computes exact semitones automatically (G5 -> A5 = +2.0 st):
   lead.bend("G5", beats=2.0, style="bend_release", target="A5", vel=96)

   # Pre-bend descending sigh: silent pre-bend to A5, release back to G5
   lead.bend("G5", beats=1.5, style="pre_bend", target="A5", vel=92)

   # Inline caret/tilde step syntax inside seq() (target pitch is explicit in token):
   lead.seq("E5 G5^A5^G5 - - - E5 - -", step=0.5)   # smooth bend + release on beat 2..4
   lead.seq("B4 D5~E5 - -", step=0.5)                # delayed bend/release targeting E5
   ```
2. **Scale- & Harmony-Constrained Algorithmic Bends**:
   Pass `key` / `scale` and optional `harmony` timeline (`[(beat, symbol), ...]`) into `expressive_bends()` so generated bends never land on non-scale pitches:
   ```python
   from engine import expression
   harmony = [(0.0, "Am"), (4.0, "F"), (8.0, "C"), (12.0, "G")]
   expression.expressive_bends(
       lead,
       role="guitar",
       scale="A minor",          # or key="Am" / "C minor" / "G major"
       harmony=harmony,          # optional [(beat, symbol), ...] chord timeline
       max_semi=2.0,
       min_dur=0.75,
   )
   ```
3. **Audit Bent Targets with `review_song.py`**:
   ```powershell
   uv run --with numpy --with scipy --with mido python music_maker_plugin/skills/soundfont-music/scripts/toolkit/review_song.py <song_name> --scale "C minor"
   ```
   (`song_name` resolves `songs/<song_name>.py`; inside custom project scripts, call `engine.review.review_song(song, harmony=harmony, scale="C minor")` directly.) Verify `out_of_scale_bends` is empty (every peak `start_midi + peak_semis` lands inside the active scale or intentional chord tone).

---

## 5. Inline `midi_map.md` Reading Pattern (Worked Few-Shot Examples)

In `music_maker_plugin/midi_map.md`, bends appear directly inline on their parent notes alongside sustain pedal (`ped`) and velocity (`v=...`):
- `@0.0 G5(d=1.5,v=96,bend=0->+2st[A5])`: Strong-beat `↑` bend starting at `G5` (`0 st`) and reaching target `A5` (`+2 st`).
- `@1.5 G5(d=0.5,v=88,bend=+2st[held->A5])`: Offbeat `→` held/re-plucked note ringing at `A5` (`+2 st`).
- `@2.0 G5(d=1.5,v=90,bend=+2->0st[A5->G5])`: Resolving `↓` release returning from `A5` back down to `G5`.
- `@4.0 C4(d=2.0,v=78,ped)`: Clean sustained chord tone anchored under active CC64 sustain pedal (`ped`).

When composing, preserve that exact separation: **first verify the unbent note + target note**, then apply `bend()` or `^`/`~` on long focal notes while keeping supporting chords clean under `ped`.
