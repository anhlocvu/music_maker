# SoundFont (`SF2 2.04`) & GM/GS Drum Architecture

Understand how SoundFont 2.04 drum banks, choke groups, multi-velocity zones, and built-in modulators translate your MIDI note numbers and velocities into realistic percussion audio. *(For general RIFF `sfbk`, 60 generator IDs, and all 10 modulator math specs, see `soundfont-music/references/sf2-spec-and-modulators.md`.)*

## 1. Bank 128 Convention & Toolkit Drum Kits (`SF2 2.04` & `GeneralUser GS`)

- **SF2 Spec Bank Standard (§7.2)**: Melodic presets occupy MIDI Banks **`0–127`**; percussion kits conventionally reside in **`wBank = 128`** and respond on **MIDI Channel 10** (`0-based ch 9`) in standard GM/GS synthesizers.
- **GS Multi-Channel Workaround**: Banks following *GeneralUser GS* optionally duplicate percussion presets onto melodic **Bank 120** so non-Ch.10 channels can trigger distinct drum kits concurrently (useful for layered percussion or isolated kit routing).
- **Bank 128 Kits (`Bank 128` / Toolkit `instruments.KITS`)**: *(Note: MIDI integer `27..88` is invariant; GeneralUser GS labels use `C3=60` notation so `36 = C1`, whereas `soundfont-music` Python step strings use `C4=60` so `36 = C2` / `"kick"`.)*

| Program # | GS Kit Name | Toolkit Key (`instruments.py`) | Key Characteristics & Mapping Caveats |
|---|---|---|---|
| **0 / 1 / 2** | **Standard 1 / 2 / 3** | `"drums"` (`0`) | General-purpose acoustic kits (`27 D#0`..`87 D#5`) |
| **8** | **Room Kit** | `"drums_room"` | Wet ambient studio kit (`RoomKick`, `RoomSnare`, `RoomToms`, `RoomHats`) |
| **16** | **Power Kit** | `"drums_power"` | Heavy arena rock punch (`PowerKick1/2`, `PowerSnare1/2`, gated/tight punch) |
| **24** | **Electronic Kit** | `"drums_electronic"` | `ElecBD/SD`, **`GatedSD` (`40 E1`)**, **`ReverseCymbal` (`52 E2`)**, `ElecHandClap` |
| **25** | **808 / 909 Kit** | `"drums_808"` | Analog drum-machine staple (`808BassDrum`, `909BassDrum`, `808RimShot`, `808SnareDrum/909SnareDrum`, `808ClosedHat/OpenHat`, **`808Cowbell`**, **`808High/Mid/LowConga`**) |
| **26** | **Dance Kit** | *Use tuple `("main", 128, 26)`* | `DanceKick`, `DanceSnare`, `ElecHandClap`, `909SnareDrum` |
| **32** | **Jazz Kit** | `"drums_jazz"` | Tight **`JazzKick`**, crisp **`JazzSnare`**, **`BrushedSnare` (`40 E1`)** |
| **40** | **Brush Kit** | `"drums_brush"` | **`BrushTap` (`38 D1`), `BrushSlap` (`39 D#1`), `BrushSwirl` (`40 E1`)**, brushed toms—**caution**: hats/cymbals still use stick samples in many SF2 brush kits, so balance cymbal velocities softly! |
| **48** | **Orchestral Kit** | `"drums_orch"` | **Non-standard layout**: moves **Hi-Hat/Ride** down to `27–30 (D#0–F#0)`, places **`Castanets` (`39`)**, fills **`41–53 (F1–F2)` with chromatic `Timpani F..f`**, **`57/59` = `ConcertCymbal2/1`** |
| **56** | **SFX Kit** | *Use tuple `("main", 128, 56)`* | Sound effects across `39–84` (`Laughing`, `Explosion`, `Thunder`, `HeartBeat`, `MachineGun`, `Applause`) |

*(Full 62-note note-by-note layout across all 10 kit columns: `assets/gm-gs-percussion-map.md`.)*

---

## 2. SF2 Generators & Modulators Driving Drum Realism

### Zone Selection & Key/Velocity Splitting
- **`keyRange` (`gen 43`) & `velRange` (`gen 44`)**: Assign individual drums to single MIDI keys (`ScaleTuning = 0`, `gen 56`, disabling chromatic pitch shift across adjacent keys—while `scaleTuning = 100` remains available for melodic toms/timpani).
- **Multi-Velocity Timbral Layers (`velRange`)**: Well-crafted SoundFonts map multiple recordings (`soft tap`, `medium rim`, `hard crack`) onto stacked `velRange` zones per key. Therefore, varying MIDI velocity alters **stick impact timbre and resonance**, not mere loudness.
- **Generator Order Rule**: In SF2 zones, `keyRange` must precede `velRange`, and both must lead the zone generator list.

### Choke Groups (`exclusiveClass`, `gen 57`)
- **Spec Behavior (§8.1.2)**: Instrument-level generator scoped across the **entire preset**. `0` = no choke; any shared non-zero integer causes a new Note-On to **rapidly silence any sounding zone sharing that `exclusiveClass`**.
- **Canonical Choke Pairs in Drum Programming**:
  - **Hi-Hat Family**: **`Closed Hi-Hat (42 F#1)`**, **`Pedal Hi-Hat (44 G#1)`**, **`Open Hi-Hat (46 A#1)`** share an exclusive class—placing a closed or pedal hit after an open splash cleanly chokes the ringing cymbal!
  - **Auxiliary Pairs**: `Short/Long Whistle (71/72)`, `Short/Long Guiro (73/74)`, `Mute/Open Cuica (78/79)`, `Mute/Open Triangle (80/81)`, `Mute/Open Surdo (86/87)`.
  - *Programmer takeaway*: Always follow an **Open Hi-Hat (`46`)** with a **Closed (`42`)** or **Pedal (`44`)** hit at the exact musical cutoff point so `exclusiveClass` naturally clamps the ring.

### Built-In Default Modulators (§8.4)
Even on single-sample zones without `velRange` switches, compliant SF2 synths (such as **FluidSynth 2.3+**, **BASSMIDI 2.4.14.28+**, **Sobanth**, and **SpessaSynth** when rendering your exported `.mid`) automatically apply two crucial velocity dynamics *(note: the toolkit's built-in Python sampler `engine/sf2.py` supports `velRange`, `exclusiveClass`, and `sampleModes` `0/1/3`, plus velocity gain scaling)*:
1. **`Velocity -> Initial Attenuation` (`960 cB = 96 dB`, negative unipolar concave)**: Quiet ghost notes (`vel 25–45`) drop smoothly deep below main accents (`vel 100–120`).
2. **`Velocity -> Initial Filter Cutoff` (`-2400 cents` linear)**: Lower MIDI velocities lower the dynamic low-pass filter cutoff automatically, making ghost notes naturally **warmer and darker** while full accents cut **brightly** through the mix.
- **Synth Engine Requirement & Polyphone Guardrails**: Render exclusively with spec-compliant engines (**FluidSynth 2.3+**, **BASSMIDI 2.4.14.28+**, **Sobanth**, **SpessaSynth**; avoid legacy TinySoundFont/Apple native players that ignore modulators/LPF). When authoring custom `.sf2` kits (e.g., via Polyphone), retain short decay/release floors (`~0.2 s` where sensible) so sample tails end cleanly without clicks.

---

## 3. Velocity & Timing Calibration Reference (`GeneralUser GS`)

Use GeneralUser GS's built-in `MIDI timing test` dynamic tiering as an empirical velocity ladder for crisp multi-subdivision fills & percussion:
- **Quarter-Note Accents**: **`vel 127`** (peak structural hit / downbeat crash)
- **8th-Note Backbone**: **`vel 108`** (main groove pulse)
- **16th-Note Forward Motion**: **`vel 82`** (secondary sticking / off-hand stroke)
- **32nd-Note Ghosts / Rolls**: **`vel 46`** (subtle ghost notes, buzz swells, fast flams)

For optimal GS kit playback under FluidSynth (`v2.4+` / `GeneralUser GS` target): use `reverb.damp=0.3`, `reverb.level=0.7`, `reverb.room-size=0.5`, `reverb.width=0.8` alongside gentle chorus (`depth=3.6`, `level=0.55`, `nr=4`, `speed=0.36`) when dry kits sound disconnected—keeping the **kick drier** in dedicated multi-track stem routing.
