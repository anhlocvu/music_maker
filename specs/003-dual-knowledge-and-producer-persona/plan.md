# Implementation Plan: Dual Top-Priority Knowledge, Zero-Code Producer Persona & Proactive Transitions/Fills

**Branch**: `003-dual-knowledge-and-producer-persona` | **Date**: 2026-11-23 | **Spec**: [spec.md](file:///C:/Users/LCBoy/Desktop/data/github%20repository/music_maker/specs/003-dual-knowledge-and-producer-persona/spec.md)

## Summary
1. Refactor `music_maker_plugin/rules/AGENTS.md` using `llm-prompt-optimizer` (RSCIT + Positive Alternatives + Few-Shot + Prompt Compression) to codify:
   - **Dual Top-Priority Parallel Knowledge**: Specialist Skill/Agent Docs **in parallel with** `music_maker_plugin/midi_map.md` (100% silent emulation authorized; `midi_map.md` fills performance nuances docs cannot express).
   - **Zero-Code Music Producer Persona**: User-facing speech uses pure musical/arranging language (e.g., *"Tôi đã soạn project này"*, *"dựng bản phối"*, *"đạp pedal"*) and never mentions code/Python/scripts/functions unless explicitly asked by the user.
   - **Proactive Transitions & Drum Fills**: User prompts provide the core form; the AI proactively invents smooth bridges, turnarounds, pre-chorus lifts, drum fills, pickups, and fuzzy boundaries.
2. Synchronize `soundfont-music/SKILL.md`, specialist skills (`producer-mindset-workflow`, `groove-rhythm-drums`, `orchestration-arrangement`, `music-theory-harmony`, `genre-style-encyclopedia`, `guitar-bass-expression`, `instrumental-soloing-improvisation`, `mixing-timbre-mastering`, `counterpoint-fugue-and-post-tonal`), and all 5 agents (`executive-producer`, `composer-theorist`, `groove-arranger`, `orchestral-bigband-arranger`, `soundfont-mix-engineer`).
3. Bump `music_maker_plugin/plugin.json` to `1.6.0`, sync `README.md`, validate with `agy plugin validate --strict music_maker_plugin`, run `code-reviewer`, and log to `GEMINI.md`.

## Technical Context
**Project Type**: Antigravity AI Music Producer Plugin (`music_maker_plugin`)
**Validation**: `agy plugin validate --strict music_maker_plugin` + `code-reviewer` subagent
**Constraints**:
- Preserve all internal toolkit references (`references/toolkit.md` stays technical for execution, while user-facing communication layers enforce zero-code phrasing).
- Preserve all existing rules in `AGENTS.md` (pedal/strum, `multi_track/` centered pan aligned at beat 0, `/project` directory structure).
- Keep all plugin rules, skills, and agents in clean, idiomatic English (with bilingual/Vietnamese-friendly musical equivalents where helpful in `AGENTS.md` few-shot examples).

## Project Structure
```text
specs/003-dual-knowledge-and-producer-persona/
├── spec.md
├── plan.md
├── tasks.md
└── checklists/
    └── requirements.md
```
