# Implementation Plan: `melody-harmonization` Skill & Plugin Wiring

**Branch**: `004-melody-harmonization-skill` | **Date**: 2026-11-23 | **Spec**: [spec.md](file:///C:/Users/LCBoy/Desktop/data/github%20repository/music_maker/specs/004-melody-harmonization-skill/spec.md)

## Summary
1. **New Skill (`music_maker_plugin/skills/melody-harmonization/`)**:
   - `SKILL.md`: Engineered with `llm-prompt-optimizer` (RSCIT + 5-step CoT + 2 source-grounded Few-Shots + Anti-Hallucination Guardrails + Output Template). Broad scope: activates for melody-to-chord harmonization, reharmonization, AND general progression design.
   - `references/00-navigation.md`: Minimal-loading router (1–3 files per call).
   - `references/melodic-skeleton-and-harmonic-rhythm.md`: Distills `00`, `01`, `02`, `03`, `05`, `18`, `19`.
   - `references/phrase-architecture-and-scoring.md`: Distills `04`, `12`, `16`, `17`, `34`.
   - `references/ted-greene-substitution-and-approach-toolkit.md`: Distills `07`, `09`, `10`, `11`, `20`, `21`, `22`, `23`, `26`, `28`, `29`.
   - `references/voice-leading-embellishment-and-modulation.md`: Distills `13`, `14`, `15`, `30`, `31`, `32`, `33`.
   - `assets/harmonic-tendencies-and-approaches.yaml`: Exact lookup tables from `24`, `25`, `26`.
   - `assets/melody-harmonization-checklists.md`: Pre-render checklist & troubleshooting matrix.
2. **Plugin Wiring (No Python Code Changes)**:
   - Update `rules/AGENTS.md`, `skills/soundfont-music/SKILL.md`, `skills/music-theory-harmony/references/00-navigation.md`, `agents/composer-theorist.md`, `agents/executive-producer.md`, `THIRD_PARTY.md`, and `plugin.json` (`1.7.0`).
3. **Verification & Cleanup (ECC)**:
   - Validate YAML syntax (`pyyaml`), verify 100% source accuracy against `tai lieu/txt/`, run `code-reviewer` subagent, run `agy plugin validate --strict music_maker_plugin`, delete all files inside `tai lieu/`, and log to `GEMINI.md`.

## Constraints
- Zero Python code additions (`engine/` untouched).
- English inside `music_maker_plugin/`; zero references to `tai lieu/` inside plugin files; preserve `midi_map.md` parallel study & Zero-Code Persona.
- 100% source fidelity—no invented progressions, percentages, or rules.
