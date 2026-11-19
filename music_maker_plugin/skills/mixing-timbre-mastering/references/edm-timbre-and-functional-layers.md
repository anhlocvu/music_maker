# Timbre Vocabulary & Functional Layering (Lavengood / Moore)

*Distilled faithfully from `edm-timbre-ped-handout.pdf` (Megan Lavengood, "EDM as Timbre Learning Lab", SMT 2025; referencing Lavengood 2020 and Moore 2012).*

## 1. Standardized Timbre Oppositions (Lavengood 2020)
Because metaphorical words like "warm" mean different things to different players, evaluate any SoundFont preset or synth timbre against **binary oppositional pairs** (`−` vs. `+`), anchored by spectrogram partial energy:

### Spectral Components — Sustain
| Opposition (`−` / `+`) | Practical Meaning for Sound Selection & Layering |
|---|---|
| **bright / dark** | High-frequency partial energy vs. rolled-off upper harmonics |
| **pure / noisy** | Clean tonal partials (sine/flute) vs. broadband air/breath/snare/distortion noise |
| **full / hollow** | All harmonics strongly present vs. missing even harmonics / scooped mids (e.g., clarinet low register, square wave) |
| **rich / sparse** | Dense stack of many partials (sawtooth, bowed strings) vs. few partials |
| **beatless / beating** | Rock-steady pitch/phase vs. chorus/detuned shimmering beats |
| **harmonic / inharmonic** | Integer overtone series (strings, brass, piano) vs. metallic/bell-like non-integer partials |

### Spectral Components — Attack
| Opposition (`−` / `+`) | Practical Meaning |
|---|---|
| **percussive / legato** | Sharp transient spike vs. soft/slow envelope bloom |
| **bright / dark** (attack) | Crisp upper-mid/high transient click vs. muted/soft onset |

### Pitch Components
| Opposition (`−` / `+`) | Practical Meaning |
|---|---|
| **low / high** | Fundamental register placement |
| **steady / wavering** | Fixed pitch vs. vibrato, pitch bend, or LFO drift |

### Custom Percussion-Focused Oppositions (e.g., TR-909 / Drum Kits)
For unpitched percussion, narrow the table relative to the kit's overall palette:
- **bright / dark**
- **rich / sparse**
- **pure / noisy**
- **[attack] bright / dark**

---

## 2. Five Functional Layers in Arrangement & Mix (Moore 2012)
Assign every active track to one functional role and verify timbral contrast *between* layers sharing the same frequency region:
1. **Explicit Beat Layer** — rhythmic timekeepers (kick, snare/clap, hats, percussion).
2. **Functional Bass Layer** — low-frequency harmonic anchor.
3. **Harmonic Filler Layer** — sustained or comped chords filling mid-range space.
4. **Melodic Layer** — foreground lead/theme.
5. **Novelty Layer** — ear-catching fills, chimes, FX, counter-lines, and unpitched rhythmic motifs.

**Layering Rule of Thumb**: Never stack two **Harmonic Filler** or **Melodic** instruments that share the *exact same* timbre oppositions (e.g., both `bright + rich + legato` in the same octave). Pair contrasting profiles—such as a `percussive + bright` attack layer (pluck/harp) with a `legato + dark/warm` sustain layer (pad/strings)—so each remains intelligible without fighting on faders.
