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
