# Implementation Plan: `piano-comping-and-voicing` & `bass-arranging-and-line-craft` Skills

**Branch**: `007-piano-bass-arranging-skills` | **Date**: 2026-11-27 | **Spec**: [spec.md](file:///C:/Users/LCBoy/Desktop/data/github%20repository/music_maker/specs/007-piano-bass-arranging-skills/spec.md)

## Summary
1. **New Skill 1 (`music_maker_plugin/skills/piano-comping-and-voicing/`)**:
   - `SKILL.md`: Engineered with `llm-prompt-optimizer` (RSCIT, Anti-Hallucination & Uncertainty Guardrail, Positive Coordination Rules, 6-step CoT, 2 Few-Shot examples matching Output Format, Token-compressed Navigation Map, Output Format placed at end, Dual Priority `References ‖ midi_map.md`, Zero-Code User Persona).
   - `references/00-navigation.md`: Minimal-loading router (1–3 files per call) + explicit boundaries (`pop-ballad-arranging`, `orchestration-arrangement`, `music-theory-harmony`).
   - `references/voicing-systems-and-voice-leading.md`: Distills `JB-Dyas-Jazz-Piano-Voicings-Mnemonics.txt`, `Dan-Haerle-Jazz-Piano-Voicing-Skills.txt`, `OMT-Jazz-Voicings.txt`, `Pease-Pullig-Modern-Jazz-Voicings.txt`, `Aebersold-Jazz-Handbook-RedBook.txt`, `Hutchinson-Music-Theory-21st-Century.txt`.
   - `references/jazz-comping-and-rhythm-section-interplay.md`: Distills `UC-Piano-Comping-Thesis.txt`, `Autumn-Leaves-Comping-Voicings-Annotated.txt`, `Frans-Absil-Arranging-by-Examples.txt`, `Contemporary-Jazz-Arranging-Techniques-DocDrop.txt`, `UOML-Jazz-Arranging-Techniques.txt`, `Ithaca-Arranging-School-Jazz-Ensembles.txt`, `MidwestClinic-{Dunscomb,Finding-The-Groove,Tolson,Widner-Houghton-Kehner}.txt`.
   - `references/pop-rock-and-contemporary-accompaniment.md`: Distills `Migu-Pop-Piano-Method-Preview.txt`, `Ron-Drotos-Pop-Ballad-Accompaniment-Complete.txt`, `Stevens-Contemporary-Accompaniment-Patterns.txt`, `OMT-Pop-Rock-Texture.txt`, `OMT-Pop-Rhythm-Section-Texture.txt`, `HandsUpForTrad-Dave-Milligan-Rhythm-Section.txt`, `Hutchinson-Music-Theory-21st-Century.txt`, `SOS-Arranging-Start-With-Rhythm.txt`.
   - `references/afro-cuban-latin-piano-and-independence.md`: Distills `UMiami-AfroCuban-Jazz-Piano-Comping-Thesis.txt`, `Frans-Absil-Arranging-by-Examples.txt`, `Contemporary-Jazz-Arranging-Techniques-DocDrop.txt`.

2. **New Skill 2 (`music_maker_plugin/skills/bass-arranging-and-line-craft/`)**:
   - `SKILL.md`: Engineered with `llm-prompt-optimizer` (RSCIT, 6-step CoT, 2 Few-Shot examples matching Output Format, Anti-Hallucination Guardrails, Dual Priority `References ‖ midi_map.md`, Zero-Code User Persona).
   - `references/00-navigation.md`: Minimal-loading router + boundaries (`groove-rhythm-drums`, `guitar-bass-expression`, `pop-ballad-arranging`, `mixing-timbre-mastering`).
   - `references/linear-and-walking-bass-construction.md`: Distills `JB-Dyas-Linear-Bass-Line-Construction.txt`, `MrBlancq-Walking-Bass-Lines.txt`, `Walking-Bass-Fundamentals-Parts-1-3.txt`, `Ithaca-Arranging-School-Jazz-Ensembles.txt`, `MidwestClinic-{Tolson,Dunscomb,Finding-The-Groove,Widner-Houghton-Kehner}.txt`, `Aebersold-Jazz-Handbook-RedBook.txt`, `Hutchinson-Music-Theory-21st-Century.txt`, `UOML-Jazz-Arranging-Techniques.txt`, `Frans-Absil-Arranging-by-Examples.txt`.
   - `references/african-rhythm-tumbao-funk-and-motown-grooves.md`: Distills `Rubim-de-Toledo-African-Rhythm-Contemporary-Bass-Thesis.txt`, `Berklee-Online-Bass-Handbook.txt`, `OnlineBass-100-Funk-Grooves-Sample.txt`, `Aebersold-Latin-Bass-Tumbao-Sample.txt`, `Contemporary-Jazz-Arranging-Techniques-DocDrop.txt`.
   - `references/kick-bass-lock-and-low-end-clarity.md`: Distills `SOS-Bass-And-Kick-Arrangement-1.txt`, `SOS-Bass-Arrangement-Clarity.txt`, `SOS-Arranging-Start-With-Rhythm.txt`, `OMT-Pop-Rock-Texture.txt`, `HandsUpForTrad-Dave-Milligan-Rhythm-Section.txt`, `Frans-Absil-Arranging-by-Examples.txt`.

3. **Existing Skill Upgrades & Plugin Wiring (`v1.10.0`)**:
   - Update `skills/orchestration-arrangement/{SKILL.md,references/instrument-idiom/piano-keyboards.md}` and `skills/groove-rhythm-drums/{SKILL.md,references/bass.md}` to route deep piano comping/voicing and bassline/groove construction to the two new skills.
   - Cross-link in `skills/soundfont-music/SKILL.md`, `rules/AGENTS.md`, `agents/{executive-producer,composer-theorist,groove-arranger,orchestral-bigband-arranger,soundfont-mix-engineer}.md`, `THIRD_PARTY.md`, `plugin.json` (`1.10.0`), and `README.md`.

4. **Verification & Logging (ECC)**:
   - Deep-read relevant sections of all 33 `.txt` files before drafting each reference file (zero guessing).
   - Run source-accuracy cross-audit & check zero `tai lieu` leaks inside `music_maker_plugin/`.
   - Run `agy plugin validate --strict music_maker_plugin`.
   - Run `code-reviewer` subagent and fix any CRITICAL/HIGH/MEDIUM findings.
   - Log completed work in `GEMINI.md`.

## Technical Context
- **Language/Format**: Markdown skill prompts & reference guides (`music_maker_plugin/`)
- **Target Platform**: Antigravity plugin (`agy plugin validate --strict`)
- **Constraints**: Zero Python `engine/` edits; English inside `music_maker_plugin/`; preserve `tai lieu/` on disk; strictly 0 fabricated rules or citations (`Bill-Dobbins-Jazz-Arranging-and-Composing.pdf` 0-char image scan excluded from claim synthesis).

## Constitution Check
- Self-contained plugin skills, independent testability via strict validation + source cross-audit, minimal file duplication, explicit boundary routing. Pass.

## Project Structure
```text
specs/007-piano-bass-arranging-skills/
├── spec.md
├── plan.md
├── tasks.md
└── checklists/requirements.md

music_maker_plugin/
├── plugin.json                                     # bump 1.9.0 -> 1.10.0
├── README.md & THIRD_PARTY.md
├── rules/AGENTS.md
├── agents/{executive-producer,composer-theorist,groove-arranger,orchestral-bigband-arranger,soundfont-mix-engineer}.md
└── skills/
    ├── piano-comping-and-voicing/                  # NEW
    │   ├── SKILL.md
    │   └── references/
    │       ├── 00-navigation.md
    │       ├── voicing-systems-and-voice-leading.md
    │       ├── jazz-comping-and-rhythm-section-interplay.md
    │       ├── pop-rock-and-contemporary-accompaniment.md
    │       └── afro-cuban-latin-piano-and-independence.md
    ├── bass-arranging-and-line-craft/              # NEW
    │   ├── SKILL.md
    │   └── references/
    │       ├── 00-navigation.md
    │       ├── linear-and-walking-bass-construction.md
    │       ├── african-rhythm-tumbao-funk-and-motown-grooves.md
    │       └── kick-bass-lock-and-low-end-clarity.md
    ├── orchestration-arrangement/{SKILL.md,references/instrument-idiom/piano-keyboards.md}
    ├── groove-rhythm-drums/{SKILL.md,references/bass.md}
    └── soundfont-music/SKILL.md
```
