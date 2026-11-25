# String Section Orchestration for Pop Ballads

Grounded strictly in:
- Dave Stewart (& David William Hearn), *Arranging For Strings* Parts 1–4 (*Sound On Sound*, June–Sep 2012)
- Frans Absil, *Arranging by Examples* (§2.3.5, Chapter 8 *String Section Voicing* pp. 145–166), *Size of the String Section in Popular Music Recordings* (2018), *Studio Orchestra Seating* (2008), and *Range of Musical Instruments*
- TaiShun Tse, *Pop Ballad* (HK EDB, pp. 16, 22–23)
- Big George, *Making Arrangements* Parts 1, 2 & 4 (incl. Debbie Wiseman)

---

## 1. Studio Section Sizing & The `2:3` Balance Rule

1. **Real Pop/Studio String Configurations** (*Absil Ch. 8 & String Size Survey; Dave Stewart Pt. 1*):
   - **Small / Regular Studio Recording**: `5-3-2-2` (`Vi1-Vi2-Va-Vc`, **0 Contrabass**) or **Octet** `2-2-2-2` (for exposed, personal, chamber-like ballad intimacy, *Stewart Pt. 1* on Anathema).
   - **Large Studio / Pop Recording**: `7-5-4-4` or `8-6-4-4` (22 players: 14 violins, 4 violas, 4 cellos — *Stewart Pt. 1*), or `8-6-6-6` when heavier lower strings are needed.
   - **Metropole / Chamber Studio Orchestra**: `8-7-5-4-3` (with `3` double basses; Vince Mendoza rule: *always use odd numbers—minimum 3—in double basses* for smooth chorus intermodulation rather than exposed pairs, *Absil p. 147*).
2. **Omit Double Basses by Default in Pop Ballads** (*Absil p. 146; Stewart Pt. 1*):
   - Because electric/synth bass owns the low end in pop/rock tracks, **omit Contrabass from the string pad** (or reserve cellos/basses doubling the bassline only for massive chorus/climax peaks, *Stewart Pt. 4* 'Grey Skies').
3. **`2:3` Acoustic Balancing Rule** (*Absil §8.1, Fig. 8.1*):
   - Anchored around violas, upper strings naturally lack acoustic weight against lower strings; compensate via **unison violins**, **violins doubled an octave below by violas**, or **`divisi a 2` cellos** (splitting cellos in two halves).

---

## 2. Do Not Copy-Paste Piano/Guitar Chords (Stewart Pt. 3 & Absil §8.3)

Keyboard and guitar chords blend homogeneously; copying a dense 6-note piano voicing straight to strings sounds over-thick and artificial (*Stewart Pt. 3*):
1. **Thin Out Redundant Mid-Range Octave Doublings** (*Stewart Pt. 3, Diagrams 1–4*):
   - Strip duplicated octave pitches in the middle register, or replace dense interiors with an open low 5th (`Cello + Viola`) and clean upper intervals (`Vln 2 + Vln 1`).
2. **Half-Open Voicing & Harmonic Series Spacing** (*Absil §8.3, p. 151*):
   - Use **half-open voicing**: wider intervals at the bottom (`Cello -> Viola`), closer in the middle, opening cleanly at the top.
   - **Omit the Root When Bass Plays**: Assign chordal functions **`3rd` and `7th`** to the **cellos** as the lowest string parts when bass guitar covers the root; place upper tensions **`7, 9, 11, 13`** in the higher voices respecting the acoustic harmonic series.
   - **Root Position for Extended Chords**: Keep `S9, S11, S13` in root position (bass holds root); alterable `5ths` (`#11=b5`, `b13=#5`) replace the `5th` and may sit lower.
   - **Doubling Priority** (*Absil p. 151*): Double `1` and `5` preferentially (more `5th` than `3rd`); avoid doubling `7th` and use doubled `9th` sparingly.
3. **Voice Leading & Independence** (*Absil §8.3; Stewart Pt. 1; Wiseman*):
   - Treat every string line as a singable melody moving primarily **by step**, keeping common tones, preparing and resolving dissonant suspensions downward by step, and avoiding parallel 5ths/octaves.
   - Avoid locking cellos and double basses together continuously unless reinforcing a heavy low passage (*Wiseman, Making Arrangements Pt. 4*).

---

## 3. Expressive Ballad Devices & Dynamic Layering

1. **Sustained High-Note Chorus Lift** (*Big George Pt. 1 & 2; Stewart Pt. 3*):
   - Holding a single high tonic/fifth pitch (or luminous high fifth interval like `A–E`, *Stewart Pt. 3* 'Everwake') across a quiet verse/chorus creates immediate emotional lift without harmonic clutter.
2. **Independent Inner Movement Over Pads** (*Stewart Pt. 1*):
   - Instead of changing all string notes strictly on Bar 1, write short 2–4 beat melodic links in the cellos or inner voices while upper strings hold.
3. **Soaring High Descant & Rhythm Contrast** (*Stewart Pt. 4*):
   - When drums, distorted guitars, or dense vocals dominate the chorus, write a **high-register violin descant** (voiced in octaves `Vln 1 + Vln 2` or unison violins) moving in **contrasting rhythm** to the vocal: slow whole/half notes against a busy syncopated vocal (*'Grey Skies'*, *'Untouchable Pt. 2'*), or active quarter notes against a sparse vocal (*'Kingdom'*).
4. **Special Bowing & Timbral Colors** (*Stewart Pt. 2–3; Absil §8.6*):
   - **`staccatissimo` vs. sustained contrasts**: Crisp 16th-length `staccatissimo` stabs vs. long unaccented sustains give rhythmic lift without drowning soloists (*'Truenorth'*).
   - **Harmonics** (airy, chime-like over solo piano), **`divisi tremolo` (`div trem`)** (half the section plays tremolo while half plays straight *arco* for subtle shimmer without horror-cliché, *Stewart Pt. 3*), **`sul tasto`** (over fingerboard = soft, warm, mellow) vs. **`sul ponticello`** (near bridge = eerie, sharp overtones, *Absil §8.6.4*), **scale runs** (exciting upward "whoosh" into climaxes, *Stewart Pt. 4*), and **portamento slides** (*Stewart Pt. 2*).
5. **Bowed MIDI Realism** (*Stewart Pt. 1–3; Hearn*):
   - **Pre-shift bowed attacks**: Because bowed strings speak slowly, hard-quantizing on the beat makes them sound late—nudge MIDI entries slightly early or avoid rigid quantize (*Stewart Pt. 1*).
   - **Continuous `CC#11` / `CC#1` Dynamics & Vibrato Crossfade**: Draw arching volume swells (`CC#11`) and phrase breaths (bow lifts between phrases); optionally crossfade `noVib -> Vib` or fade in a single solo violin subtly on key emotional phrases (*Hearn, Stewart Pt. 3*). Never use the exact same violin-section patch for `Vln 1` and `Vln 2` on unison notes without separate libraries/detune to avoid phasing (*Stewart Pt. 1*).
