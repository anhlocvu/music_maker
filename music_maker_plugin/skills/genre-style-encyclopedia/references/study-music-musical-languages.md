# Musical Language Families & Chiptune/VGM Constraints (`study-music`)

*Distilled faithfully from `study-music` (Vitaly Pavlenko, `README.md` & `talks/f0/07_nes_composition.md`).*

## 1. Western Music Language Traits vs. Non-Western Families

### Common Traits of Western Music Languages
- 12-tone equal temperament (`12-TET`).
- Major-minor tonality plus select diatonic modes (Dorian, Mixolydian) with harmonic shuttles.
- **Homophony** (melody over chords; chords carry an independent harmonic narrative using functional schemata, cadences, and voice-leading space).
- Tertian harmony (chords built in stacked thirds); any of the 12 pitches can serve as tonic.
- **Phrase contrast rule**: After two repetitions of an idea, introduce a contrasting idea.
- Predominantly `4/4` and `3/4` meters; expressive nuance carried primarily by velocity arcs and micro-pauses rather than heavy microtonal ornamentation.
- **Major Western Sub-Languages**: Rock (pop, soul/R&B, blues-rock, folk-rock, punk, prog, metal), Classical (pre-classical, Bach chorales, common practice), Jazz (harmony, solo, "lego" licks), Groove/Blues (funk, R&B), Barbershop, Film/Movie Scoring (neo-Riemannian progressions), Video Games (VGM), EDM, plus Country, Gospel, Rap, Latin, and Flamenco.

### Non-Western Music Language Families
Non-Western traditions do not share a single structural grammar and should never be reduced to plain Western major/minor triads:
- **Balkan Languages**: Rooted in *maqam* scales (e.g., *hijaz*) and additive meters (`7/8`, `9/8`), intersecting with 12-TET and Western harmonization.
- **Maqam Languages (Arabic / Turkish / Persian)**: Microtonal scales, **monophonic and heterophonic** textures rather than vertical triadic chord changes.
- **Indian Classical & Film Traditions**: *Raga* melodic frameworks and *tala* rhythmic cycles.
- **Gong-Chime Languages (Indonesian Gamelan, Thai Piphat)**: Layered cyclic colotomic structures and interlocking percussive textures, non-12-TET tunings (*sléndro* / *pélog*).
- **East Asian & Regional Traditions**: Chinese, Japanese (*in* / *yo* scales), Kyrgyz *komuz*, Georgian polyphonic singing.

---

## 2. Chiptune / NES Composition Constraint Method
*(From `study-music/talks/f0/07_nes_composition.md`)*
When drafting game or chiptune music cleanly without getting lost in timbre tweaking:
1. **Constrain Palette First**: Compose all melodic/bass voices using raw square/triangle waves first so **expressiveness comes strictly from notes, rhythm, and counterpoint** rather than lush patches.
2. **Start Two-Voice (Root + Melody)**: Draft the bass root line + lead melody in period form (`antecedent → consequent`) first; only add an inner middle voice or counter-bass afterward.
3. **Standard Game Cue Suite**:
   - Title / Main Menu: short 2–4 bar loop
   - Level 1: seamless repeating period (`A` + `A'`)
   - Contrasting Level (`Level 2` / dark stage): contrasting period or minor-mode shift
   - Mission Clear & Game Over: short non-looping stingers
