# Guitar & Bass Articulation and Pitch-Bend Taxonomy

*Grounded strictly in `DadaGP` (Sarmento et al., ISMIR 2021) and `dadagp.py` (v1.1 encoder/decoder), mapped directly to `soundfont-music` APIs.*

---

## 1. Timing Resolution & Pitch-Bend Coordinate System

- **Symbolic tick grid (`DadaGP`)**: `960 ticks per quarter note` (`wait:480` = 8th note, `wait:240` = 16th note, `wait:120` = 32nd note).
- **GuitarPro `BendPoint` representation (`dadagp.py`)**:
  - Up to 4 control points per bend or tremolo-bar gesture: `(position, value, vibrato)`.
  - **`value` units are quartertones** (`0–6+`):
    - `1` quartertone = `0.5` semitones (microtonal / blues curl)
    - `2` quartertones = `1.0` semitone (half-step bend)
    - `3` quartertones = `1.5` semitones
    - `4` quartertones = `2.0` semitones (full-step bend)
    - `6` quartertones = `3.0` semitones (minor-3rd / big rock bend)
  - Convert to `soundfont-music` semitones: `semis = quartertones * 0.5`.
  - Normalized time `frac` in `soundfont-music`: divide GuitarPro `position` by its full span (typically `0..12` in GP5, i.e., `frac = pos / 12.0`).

---

## 2. The 12 `BendType` Gestures (`dadagp.py` → `soundfont-music`)

Both note-level string bends (`nfx:bend`) and whammy/tremolo bar gestures (`bfx:tremolo_bar`) use the same 12-type taxonomy in `dadagp.py`:

| ID | DadaGP `BendType` | Pitch Contour | `soundfont-music` Equivalent |
|---|---|---|---|
| `0` | `none` | Flat pitch (`0.0 st`) | Plain note (`bend=None`) |
| `1` | `simple bend` | Pick at `0`, bend smoothly to `+semis`, hold to note end | `t.bend(note, style="bend_hold", semis=S)` or `D5^E5` |
| `2` | `bendRelease` | Pick at `0`, bend to `+semis`, hold briefly, release back to `0` | `t.bend(note, style="bend_release", semis=S)` or `D5^E5^D5` / `D5^+2^0` |
| `3` | `bendReleaseBend` | `0 → +S → 0 → +S` (double peak within one sustained note) | Custom curve: `t.bend(note, curve=[(0,0),(0.2,S),(0.45,0),(0.7,S),(1.0,S)])` |
| `4` | `preBend` | Start already bent at `+S` before picking; hold at `+S` | Custom curve: `t.bend(note, curve=[(0.0, S), (1.0, S)])` |
| `5` | `prebendRelease` | Pick already bent at `+S`, release down to `0` | `t.bend(note, style="pre_bend", semis=S)` |
| `6` | `tremoloDip` | Hold `0`, dip down (`-S`) sharply mid-note, return to `0` | `t.bend(note, style="dive", semis=S)` |
| `7` | `diveBar` | Start at `0`, dive deep downward (`-S`, often `2–7+ st`) and stay down | Custom curve: `t.bend(note, curve=[(0.0,0.0),(0.25,0.0),(0.85,-S),(1.0,-S)])` |
| `8` | `releaseUp` | Start dipped (`-S`) on bar, release upward back to `0` | `t.bend(note, style="scoop", semis=S)` |
| `9` | `invertedDip` | Hold `0`, pull bar upward (`+S`), return to `0` | `t.bend(note, style="delayed_bend", semis=S)` or `D5~E5` |
| `10` | `returnBar` | Dive (`-S`) then smoothly return to `0` (`0 → -S → 0`) | `t.bend(note, style="dive", semis=S)` |
| `11` | `releaseBar` | Release bar pressure cleanly back to `0` from prior offset | Custom curve ending at `(1.0, 0.0)` |

*Tip for `bend_range`*: Whenever a dive bar or wide bend exceeds `±2` semitones, set `Track(..., bend_range=max_semis)` (or let `Song.export_midi()` auto-emit **RPN `0, 0`**).

---

## 3. Complete Note-Level Articulation Mapping (`nfx:`)

| DadaGP Token (`nfx:`) | Physical Guitar/Bass Action | `soundfont-music` Realization |
|---|---|---|
| `nfx:palm_mute` | Right-hand palm damps strings near bridge; tight, percussive, dark decay | Use `mutedguitar` (GM 28) if clean/chug, or cap note gate (`dur * 0.45–0.65`) with `release=0.02–0.04` and lower velocity (`vel 65–85`) |
| `nfx:let_ring` | Allow plucked arpeggio notes to ring across subsequent notes instead of silencing | `t.arpeggio(..., hold=True)` or extend each note's `beats` to the chord boundary; optionally apply `t.pedal(start, chord_end - 0.05)` |
| `nfx:staccato` | Short detached note, immediate left-hand lift | Shorten `dur` (`0.35–0.5 * step`) and set `release=0.015–0.025` (never `0` to avoid clicks) |
| `nfx:dead` | Muted fretting-hand percussive "chuck" (`X` in tab) | Very short duration (`0.05–0.08` beats), muted velocity (`30–50`), optional low release (`0.015`) |
| `nfx:ghost_note` | Soft passing/grace-like inner note in parentheses `(n)` | Low velocity (`25–55`, strictly `< 60`), slightly tucked behind beat or soft duration |
| `nfx:accentuated_note` | `>` strong pick/finger accent | Boost velocity `+12` to `+18` above baseline (e.g., `98–110`) |
| `nfx:heavy_accentuated_note` | `^` marcato / heavy attack | Boost velocity `+22` to `+30` (e.g., `114–125`) |
| `nfx:hammer` | Hammer-on / Pull-off (legato fretting without right-hand re-pick) | Overlap source note slightly (`+0.02` beats) into target; drop target velocity by `10–18` points vs. picked note |
| `nfx:vibrato` | Left-hand finger vibrato | Track `vibrato=(5.5, 25–35, 0.12, 0.18)` or `t.bend(..., style="bend_vibrato", semis=0.35–0.6, vibrato_waves=3)` |
| `nfx:tie` | Sustain pitch seamlessly across beat/barline without re-attack | Merge step duration with `-` in `seq()` or single `note(..., beats=total_dur)` |
| `nfx:slide:1` (`shiftSlideTo`) | Slide finger along string to target fret, re-picking or articulating target | `B4>E5` glide on approach note or short `0.15`-beat `glide` into target |
| `nfx:slide:2` (`legatoSlideTo`) | Slide along string seamlessly without re-picking target | Single combined event with `glide` (`A4>B4`) or smooth `curve` holding target pitch after slide |
| `nfx:slide:-1` / `-2` (`intoFromBelow` / `Above`) | Slide into target note from 1–2 frets below or above | `scoop` (`-1` or `-2` semitones over first `0.15–0.24` of note) |
| `nfx:slide:3` / `4` (`outDownwards` / `Upwards`) | Slide off the end of a note downward or upward | Custom curve holding `0` for `70%` then gliding `-3` to `-5` st (or `+2` to `+4` st) at end |
| `nfx:harmonic:1..5` | `1` Natural, `2` Artificial (`pitch`, `octave`), `3` Tapped (`fret`), `4` Pinch, `5` Semi | Use GM `harmonics` (prog 31) or pitch up (`+12`, `+19`, `+24` st) with bell-like `vel 70–90` and clean sustain; pinch harmonics add upper-octave squeal + wide `bend_vibrato` |
| `nfx:grace` | Quick pre-beat ornament (`fret`, `duration`, `isDead`, `isOnBeat`, `transition`) | `0.125`-beat (`32nd`) pickup note immediately preceding main beat at `-12` to `-18` vel (or `glide` if `transition` is slide/hammer) |
| `nfx:tremoloPicking` | Rapid alternate picking on single note | Subdivide duration into uniform `step=0.125` (32nds) or `0.1667` (16th-triplets) with alternating velocity (`±5`) |
| `nfx:trill` | Rapid alternation between fretted note and `trill.fret` | Alternate main pitch and upper pitch at `step=0.125` with slight velocity taper |

---

## 4. Beat-Level Articulation Mapping (`bfx:`)

| DadaGP Token (`bfx:`) | Musical Meaning | `soundfont-music` Realization |
|---|---|---|
| `bfx:stroke:<dir>:<val>` | Chord strum direction (`1=up`, `2=down`) & speed `val` | `t.strum(chord, beats=..., spread=0.03–0.08, direction="up"\|"down")` |
| `bfx:has_rasgueado` | Rapid flamenco finger-fanning chord roll | Fast `t.strum(chord, spread=0.015–0.025, humanize_vel=8)` + rhythmic accent |
| `bfx:pick_stroke:<1\|2>` | Downstroke (`2`, slightly heavier/brighter) vs. Upstroke (`1`, slightly lighter) | Alternate `vel` by `6–10` points across 8th/16th strums |
| `bfx:slap_effect:<1\|2\|3>` | Bass slap/pop techniques (`1` slap, `2` pop, `3` thumb/double) | Switch/layer GM `slapbass` (36) or `slapbass2` (37); accent thumb slaps on low strings (`vel 105–118`) and sharp short pops on high strings (`vel 110–124`, octave jump) |
| `bfx:fade_in` | Volume-knob or volume-pedal swell | Split held note or shape track expression; soften attack (or stack rising velocity/layer crossfade) |
| `bfx:tempo_change` / `tempo_interpolation` | Step tempo change or gradual ritardando/accelerando | Adjust `beats` slightly or note offsets around cadences when rendering static-BPM `Song` |

---

## 5. `DadaGP` Instrument Groupings & Downtuning Rules

- **DadaGP 9-slot ensemble ceiling** (`dadagp.py`): up to 3 `distorted` guitars (`distorted0..2`), 2 `clean`/acoustic guitars (`clean0..1`), 1 `bass`, 1 `drums`, 1 `leads` (sharp attack e.g. piano), 1 `pads` (ambient e.g. strings/choir).
- **Synchronized downtuning**: In ensemble songs, `downtune` applies uniformly across pitched guitar/bass/lead/pad tracks (`drums` are never downtuned). When transposing a riff in `soundfont-music`, apply `transpose=SHIFT` equally to pitched tracks—and verify open-string suitability before shifting blindly.
