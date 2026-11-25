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
- **Mark Watkins (BYU-Idaho *Fundamentals of Jazz Improvisation*)**: Chapters 3, 5, 10, 11, 12, and 13.
- **Bob Keller (Harvey Mudd College)**: *How To Improvise Jazz Melodies* and *Harmonic Lego Bricks Field Guide* (John Elliott taxonomy).
- **Jamey Aebersold, Bob Reynolds, Hal Crook, Alisdair MacRae Birch, Simon Purcell & Keating/Casey**: *Jazz Handbook (Red Book)*, *Chord-Scale Syllabus*, *Chord-Tone vs Chord-Scale Soloing*, *Guide Tones & Enclosures*, and *Chord-Tone Soloing Graph Engine* (ArXiv 2510.19666).

## 7. Drum Programming, Afro-Cuban Coordination & GeneralUser GS References (`groove-rhythm-drums`)
- **Sound On Sound Drum Programming Series** (Sam Inglis, Nicholas Rowland), **Mauro Battisti / ProJazzLab (*Drumgenius 3.0 Afro-Cuban*)**, and **S. Christian Collins (*GeneralUser GS v2.0.3*)**.

## 8. Advanced Harmony, Transformational Theory, Jazz & Gospel (`music-theory-harmony`)
- **Open Music Theory (v1 / Gotham, Shaffer et al., CC BY-SA 4.0)**: *Neo-Riemannian Triadic Progressions*, prolonged functional harmony, chromatic alterations, and modulation.
- **Music Theory Online (MTO, Society for Music Theory)**: Frank Lehman (*Hollywood Cadences & CMCR Types I–VI*, MTO 19.4), Nathaniel Forrest (*PL Voice Leading & Uncanny Ids/Tarnhelms*), Richard Cohn (*Tetrahedral Graph of Tetrachordal Voice-Leading Space*, MTO 9.4).
- **arXiv Mathematical Music Papers (CC BY / arXiv)**: Markus Schmidmeier (*From Schritte und Wechsel to Coxeter Groups*, `1901.05106`), Yusuke Imai (*Golden Tonnetz*, `2509.21428`), *Chinese Remainder Theorem, Tonnetz & Negative Harmony* (`2605.25649`), Boland & Hughston (`2604.19960`), Popoff (`1111.4451`), Nurowski (`2606.11246`).
- **Lendvai / Bartók Axis System**, **George Russell (*Lydian Chromatic Concept*, Michael McClimon & Colorado summaries)**, **Jason Lyon (*Opus 28: Using Upper Structure Triads*)**, **Dan Haerle (*Jazz Piano Voicing Skills*)**, **Barry Harris 6th-Diminished System**, **Matt Falker (*Intersection of Jazz & Gospel Harmonies*)**, **Gospel Substitution Guides**, **John Coltrane Cycles** (*ThinkingMusic*, *HarmonicWheel*, Jamie Howell *26-2*, Mark Feezell *LearnMusicTheory.net*), and **Stijn Wauters (*Neo-Soul Progressions*)**.

## 9. Counterpoint, Fugue, Post-Tonal, Spectral & Schillinger (`counterpoint-fugue-and-post-tonal`)
- **Public-Domain Historical Treatises & Pedagogical Guides**: Ebenezer Prout (*Counterpoint Strict and Free*, *Double Counterpoint and Canon*, *Fugue*), Percy Goetschius (*Homophonic Forms*, *Larger Forms of Musical Composition*), Alan Belkin (*Principles of Counterpoint*, *General Principles of Harmony*), Matthew C. Saunders (*Fugue: Concepts and Analysis*, CC/pedagogical), **Open Music Theory (CC BY-SA 4.0)** (Species 1–4, Pitch-Class Sets, Prime Form, 12-Tone Serialism, Derivation, Invariance).
- **Post-Tonal & Contemporary Theory**: Julian Hook (*Why Are There Twenty-Nine Tetrachords?*, MTO 13.4), Joseph N. Straus (*Total Voice Leading*, MTO 20.2), James Donaldson (*Melody in Spectral and Post-Spectral Music*, MTO), Frans Absil (*Pitch-Class Set Diagrams / Tone Clock*, *Jeppesen vs. Schoenberg Counterpoint*, *Schillinger Rhythm Theory: Interference of Periodicities & Fractioning*).

## 10. Advanced Symphonic, Timbre Grouping & Big Band Orchestration (`orchestration-arrangement`)
- **Classical Orchestration Masters (Public Domain / Classic Treatises)**: Walter Piston (*Orchestration*, Texture Types I–VII & Chord Scoring), Nikolai Rimsky-Korsakov (*Principles of Orchestration*), Hector Berlioz & Richard Strauss (*Treatise on Instrumentation*), Cecil Forsyth (*Orchestration*), Charles-Marie Widor (*Technique of the Modern Orchestra*), Ebenezer Prout (*The Orchestra Vol 1–2*, *Instrumentation*), Alan Belkin (*Artistic Orchestration*).
- **ACTOR Project & Perceptual Grouping**: Stephen McAdams, Meghan Goodchild & Kit Soden (*Taxonomy of Orchestral Grouping Effects [TOGE]*, MTO & Timbre and Orchestration Resource).
- **Modern Studio, Jazz & Big Band Arranging**: Tim Davies (*deBreved*: *How to Score*, *Orchestral Arranging Tips*, *Jazz Part 1 & Thickened Line Part 2*, *The Orchestral Default*), Evan Rogers (*Big Band Arranging*: *Voicings Pt 1–2*, *Soli Writing*, *Open Voicings*), Frans Absil (*Arranging by Examples*, *Instrument Ranges*, *String Sizing*, *Big Band Swing & Latin Arranging*).

## 11. Melody Harmonization, Reharmonization & Harmonic Rhythm (`melody-harmonization`)
- **Popular Music Harmony, Divorce & Empirical Corpus Studies**: Trevor de Clercq (*Some Reharmonization Techniques for Popular Music: Melodic Skeletons, the Melodic-Harmonic Divorce, and Meta-Schemas*, CC BY-SA 3.0; *The Harmonic-Bass Divorce in Rock*, Music Theory Spectrum 41.2; *Tempo versus Average Rates of Harmonic Rhythm in Popular Music*, Musicae Scientiae 2023), David Temperley & Trevor de Clercq (*Statistical Analysis of Harmony and Melody in Rock Music*, JNMR 2013).
- **Computational Melody Harmonization Systems**: Li Yi, Haochen Hu, Jingwei Zhao & Gus Xia (*AccoMontage2: A Complete Harmonization and Accompaniment Arrangement System*, ISMIR 2022, CC BY 4.0); Shangda Wu, Yue Yang, Zhaowen Wang, Xiaobing Li & Maosong Sun (*AutoHarmonizer: Generating Chord Progression from Melody with Flexible Harmonic Rhythm and Controllable Harmonic Density*).
- **Ted Greene Pedagogical Harmony Archive (`tedgreene.com`, educational archive)**: *Chord Substitution Parts 1–10* (1973), *Chord Progressions – What to Expect in Popular Music* (1974), *Scale-Chord Relationships in Popular Music* (1974), *Harmonic Improvement Parts 1–5* (1975–1976), *Harmonic Devices for Gospel Feels* (1977), *Summary of Most Common Chord Movements in Modern Jazz Harmony* (1977), *Most Common Harmonic Tendencies in Jazz and Related Music* (1977/1979), *Common Harmonic Improvement Concepts* (1979).
- **Open Music Theory v2 (`viva.pressbooks.pub/openmusictheory`, CC BY-SA 4.0 / CC BY-NC-SA 4.0)**: Mark Gotham, Kyle Gullings, Chelsey Hamm, Bryn Hughes, Brian Jarvis, Megan Lavengood & John Peterson (*Performing Harmonic Analysis Using the Phrase Model*, *Tonicization*, *Extended Tonicization and Modulation to Closely Related Keys*, *Modal Mixture*, *ii–V–I*, *Jazz Voicings*, *Embellishing Chords*, *Substitutions*, *Introduction to Harmonic Schemas in Pop Music*, *Classical Schemas*, *Modal Schemas*, *Pentatonic Harmony*, *Fragile, Absent, and Emergent Tonics* after Mark Spicer 2017).

## 12. Pop Ballad Arranging, Rhythm-Section & Studio String Pedagogical References (`pop-ballad-arranging`)
- **HK Education Bureau (`edb.gov.hk`, Popular Music Teaching Resources Package)**: TaiShun Tse (*Pop Ballad* — Verse-Chorus/AABA structures, *What Was I Made For?* and *K歌之王* instrumentation/harmony breakdowns).
- **Frans Absil (`fransabsil.nl`, educational/demo publications)**: *Arranging by Examples: The Practical Guide to Jazz and Pop Orchestra Arranging* (3rd Ed. Demo), *Size of the String Section in Popular Music Recordings* (2018), *Studio Orchestra Seating* (2008), and *Range of Musical Instruments*.
- **U.S. Navy Center for Service Support (Public Release, Distribution Statement A)**: *Musician Volume 2* (NAVEDTRA 15026C, Sept 2020 — Nonharmonic tones/tensions, Unison & Octave Tutti, Rhythm Section roles, setups, kicks & hits).
- **The Midwest Clinic (`midwestclinic.org`, Clinic Handouts)**: Jerry Tolson (*It's All About the Rhythm (Section)*), Dick Dunscomb (*Keys to a Successful School Rhythm Section*), and Steve Fidyk (*Compositional Jazz Band Drumming*, 2006).
- **Berklee Press / Berklee Online (`online.berklee.edu`, public excerpts & handbook)**: Randy Felts (*Basic Piano Voicing Techniques*, excerpt from *Reharmonization Techniques*), Jack Perricone (*Melody in Songwriting*, Ch. 1 excerpt), and *Berklee Online Piano Digital Handbook* (Paul Schmeling, Dave Limina, Suzanna Sifter).
- **Sound On Sound (`soundonsound.com`, Technical Series)**: Dave Stewart & David William Hearn (*Arranging For Strings* Parts 1–4, 2012), Big George (*Making Arrangements* Parts 1–4, 1997–1998), Mike Senior (*Mix Rescue: Strong Arrangements*, 2024; *Writing Bass Guitar Parts For Rock* excerpt), Dave Gale (*Creating Usable Synth Bass*, 2021), John Walden (*Processing Acoustic Guitars*, 2006), Rory Dow (*Programming Realistic Drum Parts*, 2010), and Sam Inglis (*20 Tips On Creating Realistic Sequenced Drum Parts*, 1999).
