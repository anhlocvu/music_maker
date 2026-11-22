# Per-String Synthesis, Human Vibrato & Timbral Profiles

*Grounded strictly in `SynthTab` (Zang et al., 2023) and `MPE 1.0 Specification Notes` (RP35, 2018).*

---

## 1. The Per-String MIDI Isolation Rule (Avoiding Polyphonic Bend Bleed)

In standard MIDI (and SoundFont channel playback), **Pitch Wheel messages affect the entire channel**, not individual notes:
- If a single track plays `E4` (string 1) and `D4` (string 2) at the same time and `D4` bends up `+2` semitones (`D4^E4`), a single MIDI channel would also bend the stationary `E4` up to `F#4`.
- **Two clean solutions**:
  1. **Per-String / Per-Voice Track Split (*SynthTab* Sec 3.3)**: Split simultaneous stationary and bent strings into separate `soundfont-music` `Track`s (e.g., `gtr_bend` and `gtr_ring`, or up to 6 string tracks for solo fingerstyle). In `soundfont-music` WAV rendering (`sf2.py`), each event evaluates its own `bend` independently, AND splitting tracks ensures standard `.mid` DAW export stays 100% faithful.
  2. **MPE Channel Allocation (`MPE 1.0` / `export_midi(..., mpe=True)`)**: Allocate overlapping bent notes onto separate **Member Channels** (e.g., Lower Zone Master Ch 1, Members Ch 2–15 configured via **RPN `00 06`**), so DAWs and MPE synths render polyphonic per-note bends cleanly without splitting into 6 tracks.

---

## 2. Human Vibrato & Micro-Expression (*SynthTab* Sec 3.3)

Real guitarists and bassists rarely play sustained notes completely dead-flat, nor with mathematically identical vibrato on every bar:
1. **Explicit vibrato perturbation**: Vary vibrato depth/ceiling slightly across phrases (e.g., `depth` `22–38` cents, `rate` `4.8–6.2` Hz, `delay` `0.10–0.22` s) or alternate `Track(..., vibrato=...)` with hand-shaped `t.bend(..., style="bend_vibrato", semis=0.35–0.75)` so peak notes bloom after attack.
2. **Subtle micro-vibrato on sustained plain notes**: Even non-vibrato sustained notes (`dur >= 0.75–1.0` beats) benefit from very light vibrato (`depth 8–15 cents`, `delay 0.18–0.25 s`) or gentle `expression.expressive_bends(track, role="guitar"|"bass", intensity=0.5–0.7)`.
3. **Never let bends bleed past Note-Off**: Per MPE 1.0 Sec 3.3.3, reset pitch wheel cleanly (`0`) at note completion or before the next note on the same channel so release tails and subsequent attacks do not inherit stale bend offsets.

---

## 3. Guitar Timbre, Picking Style & Pickup Profiles (*SynthTab* Table 1 & 2)

Match General MIDI / SoundFont preset choices to physical playing style and pickup color:

| MIDI Program (0-based `instruments.py` / 1-based GM) | Timbral Role | Playing Style & Pickup Guidelines (*SynthTab* Sec 3.5) |
|---|---|---|
| `nylonguitar` (0-based `24` / GM `25`) | Classical, bossa, warm ballads | **Finger (`F`) / Thumb (`Th`)** style; warm mid-lows, `t.strum()` `spread=0.04–0.07`, gentle velocities (`65–95`). |
| `steelguitar` (0-based `25` / GM `26`) | Folk, pop, country, indie | **Pick (`P`)** for crisp rhythmic strumming; **Finger (`F`)** for arpeggiated picking (`let_ring` / `t.arpeggio(hold=True)`). |
| `jazzguitar` (0-based `26` / GM `27`) | Jazz, neo-soul, R&B chords | **Neck (`N`)** pickup character (warm, dark, round); hollow-body attack, subtle `release` (`0.08–0.15`), rich 3rds/7ths/extensions. |
| `cleanguitar` (0-based `27` / GM `28`) | Pop, funk, indie arpeggios, ambient | **Middle (`Mi`) / Neck (`N`)** or `B/Mi` quack for funk; tight `staccato` on muted funk 16ths vs. `pedal()`/`let_ring` on shimmer arpeggios. |
| `mutedguitar` (0-based `28` / GM `29`) | Funk skanks, palm-muted chugs, rhythmic ostinatos | Short percussive envelope; pair with `release=0.02–0.04` and alternating down/upstroke velocity (`±8`). |
| `odguitar` (0-based `29` / GM `30`) | Blues-rock, classic rock, expressive solo leads | **Bridge (`B`)** or **Neck (`N`)** pickup; ideal carrier for `bend_release`, `delayed_bend`, `scoop`, and `bend_vibrato`. |
| `distguitar` (0-based `30` / GM `31`) | Hard rock, metal, punk rhythm & shred leads | **Bridge (`B`)** pickup bite; use power chords (`R+5`, `R+5+8`) and `palm_mute` low chugs for rhythm (`avoid dense low triads`); use `pre_bend`, `dive`, `pinch harmonic`, and `tremoloPicking` for lead. |
| `harmonics` (0-based `31` / GM `32`) | Natural/artificial guitar harmonics | Bell-like transient accents, sparse ornament hits (`vel 75–95`), high register clarity. |

---

## 4. Articulation Routing in SoundFont vs. Sample Libraries

- **Pitch-based techniques** (`bends`, `pre-bends`, `dives`, `scoops`, `vibrato`, `slides`) → Continuous pitch-wheel / `pitch_curve()` modulation.
- **Duration/envelope techniques** (`palm_mute`, `staccato`, `dead`, `let_ring`, `hammer-on/pull-off`) → Gate duration, `release` cap, `t.pedal()`, velocity drop on legato targets, or switching between clean and muted `.sf2` presets (`cleanguitar` vs. `mutedguitar`).
- **Keyswitch caveat**: Commercial virtual instruments (like Ample Sound in *SynthTab*) use out-of-range MIDI keyswitch notes (e.g., `C0–B0`) to toggle slides/palm-mutes/harmonics. Standard GM `.sf2` SoundFonts **do not** respond to VST keyswitches—never send silent keyswitch notes to an `.sf2` preset, because the SoundFont may trigger an unintended low sample or silence. Always translate keyswitch techniques into explicit pitch curves, gate/release shaping, or separate GM presets (`mutedguitar`, `harmonics`, `slapbass`).
