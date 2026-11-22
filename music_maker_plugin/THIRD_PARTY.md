# Third-Party Licenses & Attributions (`music_maker_plugin`)

Original plugin code, skill prompts, and documentation in `music_maker_plugin` are licensed under the **MIT License**. Third-party reference guides, datasets, and ported modules retain their respective licenses and attributions:

## 1. `music-skill` (`owoevan-dev/music-skill`, MIT License)
- **Used in**:
  - Reference guides across `producer-mindset-workflow`, `genre-style-encyclopedia` (7-Axis Style Maps + 10 playbooks), `music-theory-harmony`, `groove-rhythm-drums`, `orchestration-arrangement`, and `mixing-timbre-mastering`.
  - JSON/TSV data: `association-words.tsv`, `style-maps.json`, `tonal-references.json`, and `drum-statistics.json` (see CC BY 4.0 note below).
  - Pure-Python MIT toolkit modules adapted in `soundfont-music/scripts/toolkit/engine/` (`harmony.py`, `voicing.py`, `expression.py`, `review.py`, `analysis.py`).
- **Note**: GPL-3.0 components from `music-skill` (such as `surge_host.py`) are **not** included.

## 2. Groove MIDI Dataset Aggregate Statistics (`drum-statistics.json`, CC BY 4.0)
- Computed from [Groove MIDI Dataset v1.0.0](https://magenta.tensorflow.org/datasets/groove) (Jon Gillick, Adam Roberts, Jesse Engel, Douglas Eck, David Bamman; Google LLC — *Learning to Groove with Inverse Sequence Transformations*, ICML 2019), licensed under **CC BY 4.0**.
- Contains aggregate per-style statistical tables only; no raw MIDI performances are included.

## 3. Drum Pattern Collections (`groove-rhythm-drums/assets/drum-patterns/`)
- **`Patterns_200.json` & `Patterns_260.json`** (MIT License, Copyright © 2018 aarón montoya-moraga / `dmp_midi` & `DrumMachinePatterns`).
- **`pocket_operations_patterns.json`** (© 2024 Paul Wenzel, *Pocket Operations — A Collection of Drum Machine Patterns*, Second Edition Rev. 3.1, https://shittyrecording.studio — **Some Rights Reserved**, educational use, redistributed with author permission; **not** relicensed under MIT). See `skills/groove-rhythm-drums/assets/drum-patterns/ATTRIBUTION.md`.

## 4. `song-planner` Workflow Discipline
- Pre-composition Song Sheet, No House Style, one-batch clarifying questions, mandatory wildcard idea, and user-riff preservation protocol distilled into `skills/producer-mindset-workflow/references/song-planner-protocol.md`.

## 5. Guitar/Bass Expression, Playability & Technical Specs
- **DadaGP & `dadagp.py`** (Pedro Sarmento et al., ISMIR 2021, CC BY 4.0 / MIT-style open research code): 12 `BendType` taxonomy, `nfx:`/`bfx:` articulations, and tuning vectors distilled into `skills/guitar-bass-expression/references/articulation-and-bend-taxonomy.md`.
- **GTR-CTRL / ShredGP** (Pedro Sarmento et al., EvoMUSART 2023): symbolic evaluation metrics (`PCE`, `GC`, `PIP`, `UIP`) distilled into `skills/guitar-bass-expression/` and implemented in `engine/review.py`.
- **Fretting-Transformer** (Anna Hamberger et al., 2025, CC BY 3.0): fretboard transition difficulty (`along`/`across`/`locality`), open-string heuristics, and capo/tuning conditioning distilled into `skills/guitar-bass-expression/references/fretboard-playability-and-tunings.md`.
- **SynthTab** (Yongyi Zang et al., 2023): per-string MIDI isolation, picking/pickup timbre profiles, and human vibrato perturbations distilled into `skills/guitar-bass-expression/references/per-string-synthesis-and-human-vibrato.md`.
- **SoundFont 2.04 Specification** (E-mu Systems / Creative Technology, 2006), **FluidSynth 2.6 Docs** (CC BY-SA 3.0 / LGPL-2.1), and **MPE 1.0 (RP35 / AMEI-MMA CA-034, 2018)**: synthesis model, modulators, `sampleModes=3`, `exclusiveClass`, and MPE zone/channel allocation distilled into `skills/soundfont-music/references/` (`sf2-spec-and-modulators.md`, `mpe-and-multi-channel.md`) and implemented in `engine/sf2.py` & `engine/song.py`.

## 6. Instrumental Soloing & Improvisation Pedagogical References (`instrumental-soloing-improvisation`)
- **Mark Watkins (BYU-Idaho *Fundamentals of Jazz Improvisation*)**: Chapters 3 (*Rhythm Vocabulary* & Charlie Parker 12-solo empirical distributions), 5 (*Theory 2* modal borrowing, melodic/harmonic minor modes, pentatonic blanketing & triad pairs), 10 (*Rhythm Changes* substitutions & change-running vs blanketing), 11 (*Improvisation Composition* Golden Mean `0.618` arc & harmonic delineation), 12 (*Cells and Digital Patterns*), and 13 (*Form and Structure*).
- **Bob Keller (Harvey Mudd College)**: *How To Improvise Jazz Melodies* (approach tones, enclosures, avoid-note constraints, error recovery, quartal lines) and *Harmonic Lego Bricks Field Guide* (John Elliott modular progression/cadence/turnaround taxonomy).
- **Jamey Aebersold, Bob Reynolds, Hal Crook, Alisdair MacRae Birch, Simon Purcell & Keating/Casey**: *Jazz Handbook (Red Book)* (Bebop scales & Dominant Tree), *Chord-Scale Syllabus*, *Chord-Tone vs Chord-Scale Soloing*, *Making Lines Sound Like Jazz*, *Guide Tones & Enclosures*, and *Chord-Tone Soloing Graph Engine* (ArXiv 2510.19666, shortest-path voice-leading DAG).

## 7. Drum Programming, Afro-Cuban Coordination & GeneralUser GS References (`groove-rhythm-drums`)
- **Sound On Sound Drum Programming Series**: *20 Tips On Creating Realistic Sequenced Drum Parts* (Sam Inglis), *Adding Feel To Your Rhythm Parts*, *Get Real*, *Programming Realistic Drum Parts*, and *Effective Drum Programming Parts 1–4* (Nicholas Rowland).
- **Mauro Battisti / ProJazzLab**: *Drumgenius 3.0 Afro-Cuban* drumset coordination & clave repertoire.
- **S. Christian Collins (*GeneralUser GS v2.0.3*, MIT-style free SoundFont documentation) & Polyphone Manual**: 62-note 10-kit GM/GS percussion map (`skills/groove-rhythm-drums/assets/gm-gs-percussion-map.md`), GS Bank 120/128 layout, FluidSynth/BASSMIDI recommended FX settings, and SoundFont 2.04 `velRange`/`exclusiveClass`/modulator percussion mechanics.
