# Feature Specification: Pop Ballad Arranging Skill (`pop-ballad-arranging`)

**Feature Branch**: `006-pop-ballad-arranging-skill`  
**Created**: 2026-11-25  
**Status**: Approved (Implementing)  
**Input**: User request: Build a dedicated `pop-ballad-arranging` skill (and cross-link existing plugin skills/agents/rules) engineered with `llm-prompt-optimizer` and 100% faithfully grounded in the 26 extracted source documents in `tai lieu/` covering Pop Ballad form/tension curves, Bass, Piano, Guitar, Strings, Drums, and Ballad Tutti/Kicks/Setups/Transitions—with zero fabrication.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Full-Band Pop Ballad Arrangement Architecture (Priority: P1)
As a producer arranging a Pop Ballad (Western Pop Ballad, Power Ballad, or Asian/Cantopop/Mandopop/K-Pop/V-Pop Ballad), I want the AI to plan the section-by-section energy arc (`0.618` Golden Ratio climax, `T1/T2/T3` timescale separation, ~30s attention-span variation, delayed Bass/Drums entry) alongside silent `midi_map.md` study so verses stay intimate and choruses/final choruses lift powerfully.

**Independent Test**:
- Verify `music_maker_plugin/skills/pop-ballad-arranging/SKILL.md` and `references/form-tension-and-ballad-case-studies.md` trace every structural rule and case-study fact (`What Was I Made For?`, `K歌之王`, `Frans Absil` Ch. 10–11, `Sound On Sound` *Making Arrangements* 1–4 & *Mix Rescue*) directly to the extracted files in `tai lieu/`.

### User Story 2 - Instrument-Specific Ballad Idioms: Bass, Piano, Guitar, Strings, Drums (Priority: P1)
As a producer, I want exact, non-colliding arranging rules for all 5 ballad core groups:
- **Bass**: Slow legato phrasing, kick-drum/hi-hat sync, descending scalar/slash-chord bass (`1-7-6-5-4-3-2-5`), chromatic/half-step approaches, pedal points, and delayed entry.
- **Piano**: `C3–C6` comp range (staying out of bass register), 3rd & 7th core + 6th/9th/sus4 tensions, no LH/RH voicing doubling, re-voicing static chords, sustain pedal (CC64) dedicated to ballads, non-collision with guitar.
- **Guitar**: Upper-4-string 3–4 note voicings, sharp-key open-string awareness (`G, D, A, E`), substitute chord readability (`Em7` for `Cmaj9`), Acoustic/Clean Electric/FX specs, never comping simultaneously with piano.
- **Strings**: Studio section sizes (`5-3-2-2`, `7-5-4-4`, `8-7-5-4-3`), `2:3` balancing rule, omitting contrabass when rhythm-section bass plays, placing `3rd/7th` in cellos, half-open voicing & harmonic series spacing, stepwise voice leading without parallel 5ths/8ths, `CC11` swells, and high unison/octave violin descants.
- **Drums**: Form-delineating playing, `bass drum` accents, `ride/hi-hat` time, `4-limb` ergonomics, ghost notes, velocity ramps, tuning/bleed realism, and parallel vs. contrapuntal phrasing.

**Independent Test**:
- Cross-check all 5 instrument reference files in `music_maker_plugin/skills/pop-ballad-arranging/references/` line-by-line against `tai lieu/*.txt` to confirm 0 invented numbers, rules, or citations.

### User Story 3 - Ballad Tutti Hits, Kicks, Setups & Ecosystem Wiring (Priority: P1)
As a producer, I want explicit, source-grounded rules for **Ballad Tutti, Ensemble Kicks, Setups, and Transitions** (`<= quarter note` snare kicks vs. `> quarter note` bass drum + crash kicks, setups vs. kicks, on-the-beat kicks for off-beat entrances, unison/octave tutti, bell chords, variable density, and Start & Stop pre-tutti drops), and I want `pop-ballad-arranging` wired cleanly across `music_maker_plugin` and validated strictly.

**Independent Test**:
- Verify `references/tutti-kicks-setups-and-transitions.md` against `midwest_all_about_rhythm_section_2235.txt`, `us_navy_musician_vol2_navedtra_15026c.txt`, `frans_absil_arranging_by_examples_demo.txt`, and `midwest_compositional_drumming_steve_fidyk.txt`; run `agy plugin validate --strict music_maker_plugin` and verify 0 errors/warnings.

## Functional Requirements
- **FR-001**: Create `music_maker_plugin/skills/pop-ballad-arranging/SKILL.md` engineered with `llm-prompt-optimizer` (RSCIT, 6-step CoT, source-grounded Few-Shot examples, anti-hallucination guardrails, prompt compression, Navigation Map, Output Template).
- **FR-002**: Distill 100% of the 26 extracted source files in `tai lieu/*.txt` accurately with zero fabrication into `music_maker_plugin/skills/pop-ballad-arranging/references/` (7 cohesive reference files + `00-navigation.md`).
- **FR-003**: Preserve `tai lieu/` untouched on disk as requested by the user, while keeping `music_maker_plugin/` self-contained in English with zero references to `tai lieu/` inside plugin files.
- **FR-004**: Cross-link `pop-ballad-arranging` into `genre-style-encyclopedia/references/playbooks/pop-and-ballad.md`, `soundfont-music/SKILL.md`, `orchestration-arrangement/SKILL.md`, `groove-rhythm-drums/SKILL.md`, `rules/AGENTS.md`, `agents/{executive-producer,composer-theorist,groove-arranger,orchestral-bigband-arranger,soundfont-mix-engineer}.md`, `THIRD_PARTY.md`, `plugin.json` (`1.9.0`), and `README.md`.
- **FR-005**: Run source-accuracy cross-audit, `agy plugin validate --strict music_maker_plugin`, and `code-reviewer` check, then log work in `GEMINI.md`.

## Success Criteria
- **SC-001**: 100% of facts, ratios, ranges, and rules in `skills/pop-ballad-arranging/` trace accurately to the 26 source `.txt` files in `tai lieu/` with 0 fabricated claims.
- **SC-002**: `agy plugin validate --strict music_maker_plugin` passes with 0 errors and 0 warnings (`skills 12`).
- **SC-003**: `code-reviewer` finds 0 CRITICAL or HIGH issues.
