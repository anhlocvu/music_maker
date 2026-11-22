# Implementation Plan: Ultra-Advanced Harmony, Counterpoint, Post-Tonal & Orchestral/Big-Band Arranging

**Branch**: `002-advanced-harmony-and-orchestration` | **Date**: 2026-11-22 | **Spec**: [spec.md](file:///C:/Users/LCBoy/Desktop/data/github%20repository/music_maker/specs/002-advanced-harmony-and-orchestration/spec.md)
**Input**: Feature specification from `specs/002-advanced-harmony-and-orchestration/spec.md` and 107 extracted plain-text sources in `tai lieu/` (`01_*` through `05_*`).

## Summary
1. **Skill Architecture (1 New Skill + 2 Deep Skill Upgrades + Optional 5th Agent)**:
   - Upgrade `music-theory-harmony` with ultra-advanced harmonic systems (Neo-Riemannian `P/L/R/S/N/H` & Tonnetz, Negative Harmony & Bartók/Lendvai Axis System, Upper-Structure Triads, Lydian Chromatic Concept, Barry Harris 6th-Diminished, Coltrane Cycles, Gospel/Neo-Soul passing harmonies).
   - Create new skill `counterpoint-fugue-and-post-tonal` distilling Prout (*Strict/Free Counterpoint*, *Double Counterpoint & Canon*, *Fugue*), Belkin (*Principles of Counterpoint*), OMTv1/Hook/Straus (Set Theory, 29 Tetrachords, 12-Tone Matrix & Combinatoriality), Absil (*Schillinger Rhythm & Tone Sets*), and MTO Donaldson (Spectral & Post-Spectral music).
   - Upgrade `orchestration-arrangement` with classical master orchestration (Piston, Berlioz/Strauss, Forsyth, Widor, Prout Vol. 1–2, Rimsky-Korsakov complete), psychoacoustic timbre grouping (ACTOR/McAdams, Belkin, Tim Davies), and Big-Band/Jazz sectional arranging (Absil, Rogers, Haerle, Davies: 4-Way Close, Drop-2/3/2+4, Thickened-Line Sax Soli, Open Brass Spreads).
   - Sync agents (`composer-theorist.md`, `groove-arranger.md`, `executive-producer.md`, `soundfont-mix-engineer.md` — plus optional new 5th agent `orchestral-bigband-arranger.md` pending user decision).
2. **Python Toolkit Upgrades via TDD (`soundfont-music/scripts/toolkit/engine/`)**:
   - `harmony.py`: extended `QUALITIES`, polychord parsing (`D|C7`), `plr_transform()`, `negative_harmony_pcs()`, `coltrane_cycle()`, `barry_harris_scale()`, `upper_structure_triad()`.
   - `voicing.py`: `drop2()`, `drop3()`, `drop24()`, `so_what_voicing()`, `quartal_stack()`, `upper_structure_voicing()`.
   - `review.py`: same-family register clumping / timbral masking diagnostic + harmonic variety summary.
3. **Quality Gates (`llm-prompt-optimizer` + ECC)**:
   - All skill/agent prompts engineered in English using RSCIT + 5-Step CoT + Few-Shot + Grounding + Prompt Compression.
   - TDD Red-Green-Refactor, `code-reviewer` subagent review, `agy plugin validate --strict music_maker_plugin`, and `GEMINI.md` project logging.

## Technical Context
**Language/Version**: Python 3.11+ (`uv run`)
**Primary Dependencies**: `numpy`, `scipy`, `mido` (runtime); `pyyaml` (verification)
**Testing**: `unittest` (`tools/tests/test_toolkit_*.py`) + `agy plugin validate --strict music_maker_plugin`
**Target Platform**: Windows / Cross-platform Antigravity CLI plugin (`music_maker_plugin`)
**Project Type**: Antigravity AI Plugin (Skills + Agents + Rules + Pure-Python SoundFont/MIDI Toolkit)
**Constraints**:
- Maintain 100% backwards compatibility in `engine/harmony.py`, `engine/voicing.py`, `engine/review.py`.
- Keep all plugin skills, references, and agents in English; keep `tai lieu/` paths out of `music_maker_plugin/`.
- Preserve `midi_map.md` silent Style Precedence for genres matching `music_maker_plugin/midi/`.

## Constitution Check
- *Library-First & Modularity*: All harmonic/voicing algorithms live cleanly in `engine/harmony.py` & `engine/voicing.py` as pure Python functions with zero side effects.
- *Test-First (TDD)*: Write failing tests in `tools/tests/test_toolkit_advanced.py` before modifying `harmony.py`, `voicing.py`, and `review.py`.
- *Validation Gate*: Run `unittest`, `py_compile`, `pyyaml` validation, and `agy plugin validate --strict` after final edits.

## Project Structure

### Documentation (this feature)
```text
specs/002-advanced-harmony-and-orchestration/
├── spec.md
├── plan.md
├── tasks.md
└── checklists/
    └── requirements.md
```

### Target Files in `music_maker_plugin` & `tools/tests`
```text
music_maker_plugin/
├── plugin.json                                    # Bump to 1.5.0
├── THIRD_PARTY.md                                 # Add newly distilled public-domain/open-access sources
├── rules/AGENTS.md                                # Sync new skill + optional agent + advanced toolkit APIs
├── agents/
│   ├── composer-theorist.md                       # Load new skill + advanced harmony references
│   ├── groove-arranger.md                         # Load upgraded orchestration & big-band references
│   ├── executive-producer.md                      # Align high-level form/genre options
│   ├── soundfont-mix-engineer.md                  # Expose new harmony/voicing/review APIs
│   └── [optional] orchestral-bigband-arranger.md  # Dedicated 5th specialist agent (pending user approval)
└── skills/
    ├── music-theory-harmony/
    │   ├── SKILL.md
    │   ├── references/00-navigation.md
    │   ├── references/harmony/
    │   │   ├── neo-riemannian-and-tonnetz.md
    │   │   ├── negative-harmony-and-polarity.md
    │   │   └── advanced-jazz-gospel-voicings.md
    │   └── assets/advanced-harmony-catalog.yaml
    ├── counterpoint-fugue-and-post-tonal/         # NEW SKILL
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── 00-navigation.md
    │   │   ├── strict-and-invertible-counterpoint.md
    │   │   ├── fugue-and-canon-architecture.md
    │   │   ├── post-tonal-set-and-serial-theory.md
    │   │   └── spectral-and-schillinger-techniques.md
    │   └── assets/post-tonal-and-fugue-catalog.yaml
    ├── orchestration-arrangement/
    │   ├── SKILL.md
    │   └── references/orchestration/
    │       ├── classical-masters-orchestration.md
    │       ├── timbre-grouping-and-modern-scoring.md
    │       └── big-band-and-sectional-voicings.md
    └── soundfont-music/
        ├── SKILL.md
        ├── references/toolkit.md
        └── scripts/toolkit/engine/
            ├── harmony.py
            ├── voicing.py
            └── review.py

tools/tests/
└── test_toolkit_advanced.py                       # NEW TDD test suite
```
