# Navigation Map — Instrumental Soloing & Improvisation

Load **minimal files** per soloing task (2–3 files max alongside `assets/chord-scale-and-cell-catalog.yaml`). Use this map to pick exact modules instead of guessing harmonic extensions, approach patterns, or rhythmic phrasing.

## Topic-to-Reference Routing

| Soloing Need | File to Load | Core Contents |
|---|---|---|
| Chord-tone targeting, `3 -> 7` guide tones, accompaniment-free clarity, shortest-path voice leading | `references/chord-tone-and-guide-tone-architecture.md` | Crook 90% chord-tone test, Birch 3 harmonic approaches & Ideal Line, Purcell "join the dots" guide tones (`3-7`, `5-9`, `9-13` + chromaticized `♭9/♯9/♯11/♭13`), Watkins `1 & 3` delineation, Keating & Casey weighted DAG shortest-path boundary voice leading |
| Parent chord-scales, Harmonic Lego Bricks, Rhythm Changes subs, triad pairs, pentatonic blanketing | `references/harmonic-bricks-and-advanced-scales.md` | 5 chord-scale families, Melodic/Harmonic Minor modes, Diminished & Whole-Tone symmetry, pentatonic blanketing (`5th of I`, `2nd/4th/♭5`), triad pairs, Elliott *Harmonic Lego Bricks* cadences/turnarounds/joins, Rhythm Changes Sets 1–6 & Bridges 1–5, Haerle 17 blues types |
| Passing tension, single/multiple chromatic approach notes, enclosures, avoid notes, fail-safe recovery | `references/approach-tones-and-enclosures.md` | Keller & Purcell single/chromatic multiple approach tones, diatonic/chromatic enclosures, avoid-note passing constraint (`<=` 8th note for nat4 over Maj), error-recovery rule, skip/zig-zag, quartal (4th) phrasing, swing triplet turns |
| Motivic cells, permutations, bebop lines, circular shapes, side-stepping outside playing | `references/melodic-cells-and-sequences.md` | Watkins 4-note cells (`1-3-5`, `1-5`, `7th`, `5-9` upper-half), Prime/Inversion/Retrograde/RI transforms, circular permutations (`up/up`, `up/down`, `down/down`, `down/up`), real half-step side-stepping, `ii-V` pairing, Bebop cells, 4 Bebop scales & upbeat rule |
| Human solo rhythm, swing phrasing, phrase starts/endings, Golden Mean climax, song forms | `references/rhythm-vocabulary-and-solo-form.md` | Parker quantitative stats (~70% pre-downbeat starts, 4 phrase endings, ghosted upbeats, *The Bop*, terminal vibrato), Rhythm Blocks (1–4 note cells + *On/Half-way/Ricochet/Almost*), Golden Mean (`0.618`) climax arc, space discipline, `AAB`/`AABA`/`ABA` forms & live arrangement slots |
| Machine-readable lookup tables for scales, cells, stats, bricks | `assets/chord-scale-and-cell-catalog.yaml` | Structured YAML tables for programmatic validation and solo planning |

## Cross-Skill Integration

- **Harmony & Song Form**: Load `music-theory-harmony` first to fix the underlying progression, mode, and section keys before planning solo lines over those changes.
- **Instrument Ergonomics & Pitch Bends**: When soloing on **guitar or bass**, also load `guitar-bass-expression` (`Track.bend()`, fret transition geometry, and per-string bend isolation) and align cell/DAG phrasing with string-change costs (`2x` penalty across strings).
- **Arrangement Context & Mixing**: Coordinate with `orchestration-arrangement` (protecting the lead solo lane in Moore's foreground/lyric slot) and `mixing-timbre-mastering` (avoiding frequency clashes between solo instrument and comping keyboards/guitars).
