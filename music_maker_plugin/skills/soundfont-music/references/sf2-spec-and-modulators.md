# SoundFont 2.04 Synthesis Model, Generators, Modulators & FluidSynth Notes

*Grounded strictly in the SoundFont Technical Specification v2.04 (2006) and FluidSynth 2.6 Developer Documentation.*

---

## 1. RIFF `sfbk` Architecture & Hydra (`pdta`)

A SoundFont 2 file is a RIFF container (`RIFF` / `sfbk`) with three `LIST` chunks:
1. **`INFO`**: Metadata (`ifil` version, `isng` target engine, `INAM` bank name, `icrd`, `ieng`, `icop`, `icmt`, `isft`).
2. **`sdta`**: Digital audio waveforms:
   - `smpl`: 16-bit signed PCM sample words.
   - `sm24` (added in SF 2.04): Optional upper/lower 8-bit extension for 24-bit sample playback.
3. **`pdta` (Hydra — 9 sub-chunks)**:
   - Preset tier: `phdr` (preset header: name, program, bank) → `pbag` (preset zones) → `pmod` (preset modulators) → `pgen` (preset generators).
   - Instrument tier: `inst` (instrument header) → `ibag` (instrument zones) → `imod` (instrument modulators) → `igen` (instrument generators).
   - Sample tier: `shdr` (sample header: start/end/loop sample indices, sample rate, `orig_pitch`, `pitch_correction`, sample type).

### Zone Hierarchy & Precedence (Section 8.5 & 9.4)
- **Global zone**: If a preset or instrument has >1 zone and its first zone lacks the terminal generator (`instrument` in `pgen` / `sampleID` in `igen`), it is a **global zone** applying defaults to all local zones in that preset/instrument.
- **Instrument level = Absolute**: Generators in `igen` override default synthesis values (`DEFAULTS`).
- **Preset level = Additive / Relative**: Value generators in `pgen` **add to** the underlying instrument zone values.
- **Range intersection**: `keyRange` (`0..127`) and `velRange` (`0..127`) at preset and instrument levels **intersect** (narrowing active velocity/key splits rather than adding).
- **Instrument-only generators** (ignored if placed in `pgen`): 8 sample address offsets (`0..4, 12, 45, 50`), `keynum` (`46`), `velocity` (`47`), `sampleModes` (`54`), `exclusiveClass` (`57`), `overridingRootKey` (`58`).

---

## 2. Synthesis Model & Parameter Units (Section 9.1 & 9.3)

The SF2 engine follows the EMU8000 wavetable model (also used as the synthesis core of FluidSynth):

1. **Wavetable Oscillator & Sample Looping (`sampleModes` #54)**:
   - `0`: No loop (one-shot to `end`).
   - `1`: Continuous loop (`start → eloop`, wrapping back to `sloop` indefinitely).
   - `3`: Loop while key is depressed; on `note_off`, finish the current loop pass through `eloop` and play the remaining sample tail to `end`.
2. **2nd-Order Resonant Low-Pass Filter**:
   - `initialFilterFc` (#8): Cutoff in **absolute cents** (`Hz = 8.176 * 2^(fc / 1200)`, range `1500` = ~20 Hz to `13500` = ~20 kHz / open).
   - `initialFilterQ` (#9): Resonance peak in **centibels** (`cB`, `0..960` = `0..96 dB`; DC gain drops by `Q / 2` so peak rises `Q / 2` above 0-Q passband).
3. **Two Low-Frequency Oscillators (Triangular after `delay`)**:
   - **Vibrato LFO**: Modulates pitch only (`vibLfoToPitch` #6 in cents, `delayVibLFO` #23 in timecents, `freqVibLFO` #24 in cents relative to `8.176 Hz`).
   - **Modulation LFO**: Can modulate pitch (`modLfoToPitch` #5), filter cutoff (`modLfoToFilterFc` #10), and volume (`modLfoToVolume` #13 in `cB`).
4. **Two 6-Phase Envelope Generators (`Delay → Attack → Hold → Decay → Sustain → Release`)**:
   - **Volume Envelope** (`#33–38`): Attack is convex so gain rises linearly in amplitude; Decay & Release ramp linearly in dB (`cB` attenuation: `sustainVolEnv` #37 `0..1440 cB`, `1000` ≈ `-100 dB` full silence).
   - **Modulation Envelope** (`#25–30`): Modulates pitch (`modEnvToPitch` #7) and/or filter cutoff (`modEnvToFilterFc` #11).
   - **Keyboard Tracking**: `keynumToVolEnvHold/Decay` (#39–40) and `keynumToModEnvHold/Decay` (#31–32) shorten envelopes for higher pitches (`100 timecents/key` halves duration per upward octave relative to `C4 = 60`).
5. **Exclusive Class Choke (`exclusiveClass` #57)**:
   - Any non-zero value (`1..127`) forms a choke group across the preset—triggering a new note rapidly terminates sounding notes with the same `exclusiveClass` (classic use: closed hi-hat choking open hi-hat).

### Unit Conversion Formulas (Section 9.3)
- **Timecents → seconds**: `seconds = 2 ** (timecents / 1200.0)` (`0` = `1.0 s`, `-12000` ≈ `< 1 ms` instantaneous, `-7973` ≈ `10 ms`).
- **Absolute cents → frequency (Hz)**: `hz = 8.176 * (2 ** (cents / 1200.0))` (`0` = `8.176 Hz`, `6900` ≈ `440 Hz`).
- **Centibels (`cB`) → linear amplitude**: `gain = 10 ** (-cB / 200.0)` (`10 cB = 1 dB`). Note: SoundFont/FluidSynth EMU-style `initialAttenuation` (#48) commonly scales attenuation by `0.4` (`att_cb * 0.4`) to prevent overly quiet presets.
- **Pan (#17) & Effects Sends (#15, #16)**: `0.1%` units (`pan` `-500..+500`; `reverbEffectsSend` / `chorusEffectsSend` `0..1000` = `0..100%`).

---

## 3. Modulator Model & the 10 Default Modulators (Section 8.4 & 9.5)

Equation: `destination += Transform(Amount * Map(PrimarySource) * Map(SecondarySource))`

Every SoundFont 2.01+ instrument inherits **10 implicit default modulators** unless overridden by an identical modulator in `imod`:

| # | Primary Source | Secondary Source | Destination | Default Amount & Shape |
|---|---|---|---|---|
| `8.4.1` | Note-On Velocity | None | `initialAttenuation` (#48) | `+960 cB` (Negative Unipolar Concave: soft velocity = heavy attenuation) |
| `8.4.2` | Note-On Velocity | None | `initialFilterFc` (#8) | `-2400 cents` (Negative Unipolar Linear: softer hits sound darker) |
| `8.4.3` | Channel Pressure | None | `vibLfoToPitch` (#6) | `+50 cents` (Positive Unipolar Linear) |
| `8.4.4` | MIDI `CC 1` (Mod Wheel) | None | `vibLfoToPitch` (#6) | `+50 cents` (Positive Unipolar Linear) |
| `8.4.5` | MIDI `CC 7` (Volume) | None | `initialAttenuation` (#48) | `+960 cB` (Negative Unipolar Concave) |
| `8.4.6` | MIDI `CC 10` (Pan) | None | `pan` (#17) | `+1000` (`0.1%`, Positive Bipolar Linear) |
| `8.4.7` | MIDI `CC 11` (Expression) | None | `initialAttenuation` (#48) | `+960 cB` (Negative Unipolar Concave) |
| `8.4.8` | MIDI `CC 91` (Reverb Send) | None | `reverbEffectsSend` (#16) | `+200` (`20%` added send at max) |
| `8.4.9` | MIDI `CC 93` (Chorus Send) | None | `chorusEffectsSend` (#15) | `+200` (`20%` added send at max) |
| `8.4.10` | MIDI Pitch Wheel | `RPN 0` Pitch Wheel Sens. | Initial Pitch | `+12700 cents` (`PitchWheel * RPN0`, Bipolar Linear) |

---

## 4. Standard MIDI & NRPN Behavior (Section 9.2 & 9.6)

- **Channel MIDI controls**: `CC 0/32` Bank Select MSB/LSB; `CC 6/38` Data Entry MSB/LSB; `CC 64` Sustain (`>=64` holds key-on state until `<64`); `CC 66` Soft; `CC 67` Sostenuto; `CC 98/99` NRPN LSB/MSB (`MSB=120` addresses SF2 generator `#` in real time, zero offset at `0x2000`); `CC 100/101` RPN LSB/MSB (`0,0` = Pitch Bend Sensitivity); `CC 120` All Sound Off (immediate cut bypassing release); `CC 121` Reset All Controllers; `CC 123` All Notes Off (enter release).
- **FluidSynth vs. Pure-NumPy `engine/sf2.py`**:
  - `engine/sf2.py` implements memory-mapped `smpl`, `phdr/pbag/pgen/inst/ibag/igen/shdr`, ADSR (`delay/attack/hold/decay/sustain/release`), `sampleModes` `0/1/3`, `exclusiveClass`, `FILTER_FC`, `PAN`, `ATTENUATION`, `pitch_curve` multi-point bends, and `pitch_lfo` vibrato without external C libraries.
  - External FluidSynth (`fluidsynth.org`) adds full `pmod/imod` modulator chaining, `sm24` 24-bit sample extension, chorus DSP, and real-time MIDI CC/NRPN streaming when exporting `.mid` + `.sf2` to a DAW or live host.
