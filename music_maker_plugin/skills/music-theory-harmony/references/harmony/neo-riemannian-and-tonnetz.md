# Neo-Riemannian Theory, Tonnetz, Axis System & Film Cadences

## 1. The PLR Group & Generalized Tonnetz

Neo-Riemannian theory replaces diatonic root-function labels with **parsimonious voice-leading operations** between consonant major and minor triads (all 24 triads in 12-TET). Viewed geometrically on the infinite Tonnetz (horizontal = fifths `P5`, diagonal NE/SW = major thirds `M3`, diagonal NW/SE = minor thirds `m3`), each operation acts as a reflection across an edge of a triadic triangle—generating the affine Coxeter group $\tilde{S}_3$ on the infinite Tonnetz and dihedral symmetry modulo 12 on the toroidal Tonnetz.

### Primary Involutions (1-Semitone or Whole-Tone Parsimony)

| Op | Name | Voice-Leading Motion | Major -> Minor (from C maj) | Minor -> Major (from C min) |
|---|---|---|---|---|
| **P** | Parallel | Move 3rd by 1 semitone (retain root & 5th) | `C -> Cm` (`E -> Eb`) | `Cm -> C` (`Eb -> E`) |
| **L** | Leading-tone exchange | Move root of major down 1 st / 5th of minor up 1 st | `C -> Em` (`C -> B`) | `Cm -> Ab` (`G -> Ab`) |
| **R** | Relative | Move 5th of major up 2 st / root of minor down 2 st | `C -> Am` (`G -> A`) | `Cm -> Eb` (`C -> Bb`) |

Because $P^2 = L^2 = R^2 = I$, each primary transformation is an **involution** (self-inverse). Unlike continuous shifts on the pitch-class plane, applying a fixed sequence $s$ of PLR moves to an adjacent major/minor pair causes them to drift in opposite directions unless dualistic chirality is preserved.

### Secondary Compound Operations

| Op | Formula | Common Tones | Effect on C maj | Effect on C min | Expressive / Dramatic Affect |
|---|---|---|---|---|---|
| **S** (SLIDE) | `LPR` | 1 (the 3rd stays!) | `C -> C#m` (`C,G -> C#,G#`; `E` held) | `Cm -> B` (`C,G -> B,F#`; `Eb = D#` held) | Shadow progression; uncanny enharmonic shift (`D#`/`Eb` pivot) |
| **N** (Nebenverwandt) | `RLP` | 1 | `C -> Fm` (5th relation minor subdominant) | `Cm -> G` (major dominant) | Dark plagal shadow / classical turn |
| **H** (Hexatonic Pole) | `PLP` (or `LPL`) | 0 (max smoothness, 3 semitones total) | `C -> Abm` (`C->B, E->Eb, G->Ab`) | `Cm -> E` (`C->B, Eb->E, G->G#`) | Maximum uncanniness (Cohn paradox): consonant triads with zero common tones and maximally opposite tonal polarity |

## 2. Cyclic Subgroups & Regions

Applying two primary operations alternately closes symmetric cycles in 12-TET:

1. **Hexatonic Cycle (`PL` / `LP`, length 6)**:
   - Exhausts one co-hexatonic system of 6 triads sharing pitches from a single hexatonic collection (`014589` mod 12).
   - Example: `C -> Cm -> Ab -> Abm -> E -> Em -> C`.
   - **Tarnhelms vs. Ids (Forrest)**: Alternating `PL`/`LP` starting from a minor triad (`Cm -> Abm` via `LP` / `Tarnhelm` = `P+L`, dark, sinister, obsessive, named after Wagner's Tarnhelm leitmotif); starting from a major triad (`C -> E` via `LP` / `Id`, bright, radiant, mystical, euphoric); across the circle is the **Hexatonic Pole** (`H = PLP`).
2. **Octatonic Cycle (`PR` / `RP`, length 8)**:
   - Alternates major and minor triads within one of the 3 octatonic collections (`0134679t`).
   - Example: `C -> Cm -> Eb -> Ebm -> Gb -> Gbm -> A -> Am -> C`.
   - **Subtonic "Cowboy" Half Cadence**: Moving between two major triads a minor 3rd or whole tone apart via `RP` (`bVII -> V` = `Bb -> G`, e.g., in C) or `bVI -> IV` creates sweeping pastoral/Western breadth (Jerome Moross *The Big Country*, Elmer Bernstein).
3. **Full Cycle of Fifths & Relative/Leading Spiral (`RL` / `LR`, length 24)**:
   - Alternates diatonic neighbors: `C -> Am -> F -> Dm -> Bb -> Gm ...`, weaving through all 24 major and minor triads along the fifths-fifths Tonnetz strip.
4. **Weitzmann Regions & Douthett/Steinbach Cube Dance**:
   - The 4 augmented triads (`C+, C#+, D+, Eb+`) act as central hubs connected by single-semitone voice leading to 6 consonant triads each (3 major by lowering a note 1 st; 3 minor by raising a note 1 st), linking hexatonic systems cleanly via 1-semitone voice leading.

## 3. Golden Tonnetz & Symmetry

In geometric generalizations of the Tonnetz using golden triangles and gnomons:
- 7 tones of a diatonic major/minor scale tile inside a base golden triangle such that consecutive scale steps are adjacent and the triads `I, iii, IV, V, vi` form sub-triangles/gnomons.
- Horizontal shifts correspond to fifth transpositions (adding/removing 1 sharp along the circle of fifths); vertical shifts toggle parallel major/minor modes sharing Tonic + Fifth (`C-G`), turning `P`, `L`, `R` into reflections/shears among golden triangles and gnomons.

## 4. Bartók / Lendvai Axis System (`T / S / D`)

Ernő Lendvai partitions the 12 pitch classes modulo a minor-3rd cycle into **three four-pole tonal function axes** (each pole a m3 / 3 semitones apart; tritone pairs are **pole–counterpole**):

| Axis | Roots in C | Functional Role | Pole–Counterpole Tritone Pairs |
|---|---|---|---|
| **T (Tonic)** | `C (I), Eb (bIII), F# (#IV), A (vi)` | Rest / home pole | `C <-> F#`, `Eb <-> A` |
| **D (Dominant)** | `G (V), Bb (bVII), Db (bII), E (III)` | Tension / dominant pole | `G <-> Db`, `Bb <-> E` |
| **S (Subdominant)** | `F (IV), Ab (bVI), B (vii), D (ii)` | Departure / predominant | `F <-> B`, `Ab <-> D` |

**Compositional & Motion Laws**:
- **Normal Axis Progression** (`T -> S -> D -> T` or `S -> D -> T`, e.g., `F -> G -> C`, `D -> Db7 -> C`, `Ab -> G -> C`): **releases tension** cleanly even without textbook `ii-V-I` roots.
- **Axis Retrogression** (`T -> D -> S -> T` or `D -> S`): **builds tension**.
- **Pole–Counterpole Switch** (tritone leap within the same axis, e.g., `G7 <-> Db7`, or `C <-> F#`): **neutral tension change** (neither builds nor releases functional momentum), ideal for color surprise or smooth tritone reharm.
- **Jazz Axis Equivalence**: `ii` (`D`) belongs to `S` and `bVII` (`Bb`) belongs to `D` (`S -> D -> T`), explaining why backdoor `IV -> bVII7 -> I` and Coltrane `ii -> V/M3` progressions retain classic functional gravity across remote keys.

## 5. Film & Cinematic Cadential Taxonomy (Lehman)

Film and modern dramatic harmony codifies chromatic cadences as syntactic phrase endings rather than anomalies:

### Determinate vs. Indeterminate Cadences
- **Determinate Cadence**: Unambiguous arrival onto a root-position goal triad (PAC-like closure).
- **Indeterminate Cadence**: Avoided, suspended, or ambiguous cadence (standing on V, elided dominant, or drifting modal plane) that keeps narrative tension open.

### Mixed Plagal Cadence (M-PC) & Hollywood Fingerprints
- **Paradigm**: `IV -> iv (or iiø7) -> I` featuring the descending chromatic sigh `6 -> b6 -> 5` (`A -> Ab -> G` in C major).
- **Subtonic Half Cadence (S-HC)**: `bVII -> V` (or `bIII -> V`, `bVI -> IV`), creating heroic Western/adventure openness (`RP` transform).
- **Subtonic Authentic Cadence (S-AC)**: `bVII -> I` (or double plagal `bVII -> IV -> I`), warm patriotic/pastoral closure without leading-tone pull.

### Chromatically Modulating Cadential Resolutions (CMCR Types — Lehman *MTO* 19.4)

An abrupt structural key shift right across the cadence boundary from a root-position dominant `V` (prepared as if resolving to `I_old`) onto a fresh root-position tonic triad `I_new` (John Williams *Jurassic Park* "Flyover", *E.T.*, *Harry Potter*, Max Steiner *Key Largo*, Mahler *Durchbruch*). Unlike deceptive cadences, `I_new` requires no "correction"—it establishes the new local key immediately.

| CMCR Type | Cadential Motion (vs. Implied `I_old`) | Repertoire Example (Lehman) | Voice-Leading Mechanism & Affect |
|---|---|---|---|
| **Type 0** | Key-preserving chromatically altered resolution (`VII#3 -> I`) | *Jurassic Park* (`A -> Bb` in Bb) | Retains implied tonic while bypassing expected new key (`D`) |
| **Type I** | `V` discharges down m3 onto `III` of implied key (`+4 st`, `T_4` from `I_old`) | *Harry Potter* "Change of Seasons" (`D -> B` from implied `G`) | Radiant wonderment & expansive narrative lift (`RP` from dominant) |
| **Type III** | `V` shifts to `VII` / `-1 st` below implied `I_old` (`T_11`) | *E.T.* "E.T. Is Alive!" (`D_IV -> C#`); *Jurassic Park* (`F# -> Bb` from implied `B`, `D -> Db`) | Instantaneous otherworldly brilliance & revelation |
| **Type IV** | `V` (or plagal `IV`) moves to `VI` / `-3 st` below implied `I_old` (`T_9`) | *Jurassic Park* (`C -> D` from implied `F`; plagal `Ab -> C` from `Eb`) | Triumphant elevation / dramatic arrival |
| **Type VI** | `V` discharges onto `#IV=I` at the tritone (`T_6` from `I_old`) | Relaxational/displacing (`5̂` focus) | Otherworldly displacement (rarest in Williams) |

*(Subtraction rule: Subtracting attribute 5 replaces `V` with `IV` or `bVII`, yielding a **plagal CMCR** such as `D -> C#` in E.T. or `Ab -> C` in Jurassic Park.)*

## 6. Toolkit Integration (`engine.harmony`)

Use the verified helper directly in composition scripts:

```python
from engine.harmony import plr_transform, parse

root_pc, qual = plr_transform(0, "maj", ops="PLP")  # (8, 'min') -> Abm (Hexatonic Pole from C)
root_pc, qual = plr_transform(0, "maj", ops="S")    # (1, 'min') -> C#m (SLIDE from C)
ch = parse("D|C7")                                  # Polychord: upper_pcs + lower_pcs
```
