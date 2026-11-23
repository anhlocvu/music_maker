# Feature Specification: Dual Top-Priority Knowledge (`skills` ‖ `midi_map.md`), Zero-Code Producer Persona & Proactive Transitions/Fills

**Feature Branch**: `003-dual-knowledge-and-producer-persona`
**Created**: 2026-11-23
**Status**: Approved (Implementing)
**Input**: Apply `llm-prompt-optimizer` to refine and expand `music_maker_plugin` rules, skills, and agents with three core directives: (1) Treat `music_maker_plugin/midi_map.md` as an internalized, first-class knowledge base read in **parallel** with specialist skill/agent documentation—both holding top priority, with 100% style adoption/emulation authorized; (2) Enforce a pure Music Producer persona in all user-facing communication (no code/Python/function/source terminology unless explicitly asked); (3) Proactively compose musical transitions, turnarounds, drum fills, and fuzzy boundaries beyond the user's skeleton prompt.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Parallel Top-Priority Study of Specialist Docs & `midi_map.md` (Priority: P1)
As a music producer using `music_maker_plugin`, I want the AI to read **both** specialist skill/agent documentation and `music_maker_plugin/midi_map.md` in parallel as co-equal top-priority knowledge—because written docs capture theory/engineering principles while `midi_map.md` captures lived performance nuance—and to freely reuse/emulate 100% of `midi_map.md`'s style silently.

**Independent Test**:
- Inspect `music_maker_plugin/rules/AGENTS.md`, `skills/soundfont-music/SKILL.md`, specialist `SKILL.md` files, and all 5 `agents/*.md` files to verify explicit dual-parallel top-priority instructions (`Specialist Docs ‖ midi_map.md`) and 100% style emulation permission without exposing `midi_map.md` / `midi/` to users.

### User Story 2 - Zero-Code Music Producer Persona in User Communication (Priority: P1)
As a non-programmer musician/producer, I want the AI to speak strictly in musical and production terms (e.g., *"Tôi đã soạn xong bản phối cho project này"*, *"thêm kỹ thuật đạp pedal và rải phím"*) rather than programming terms (*"code mã nguồn"*, *"chạy script Python"*, *"gọi hàm"*) when talking to me—unless I explicitly ask about code.

**Independent Test**:
- Inspect `rules/AGENTS.md`, `soundfont-music/SKILL.md`, `producer-mindset-workflow/`, and `agents/*.md` for explicit RSCIT constraints + positive Few-Shot terminology replacements distinguishing internal execution from user-facing musical communication.

### User Story 3 - Proactive Musical Transitions, Drum Fills & Fuzzy Boundaries (Priority: P1)
As a creator who gives a high-level structural prompt (e.g., Verse → Chorus → Outro), I want the AI to treat my prompt as a structural core and proactively compose smooth connecting transitions, turnarounds, pre-chorus lifts, drum fills, pickups, cymbal swells, and fuzzy boundaries so the arrangement flows naturally without abrupt block cuts.

**Independent Test**:
- Inspect `rules/AGENTS.md`, `soundfont-music/SKILL.md`, `producer-mindset-workflow/`, `groove-rhythm-drums/SKILL.md`, `orchestration-arrangement/SKILL.md`, and `agents/{executive-producer,composer-theorist,groove-arranger,orchestral-bigband-arranger,soundfont-mix-engineer}.md` for explicit proactive transition & drum-fill directives.

## Functional Requirements
- **FR-001**: Optimize `music_maker_plugin/rules/AGENTS.md` using `llm-prompt-optimizer` (RSCIT structure, positive alternatives, few-shot examples, prompt compression) covering all three directives while preserving existing pedal, strumming, `multi_track/`, and `/project` directory rules.
- **FR-002**: Establish **Dual Top-Priority Knowledge** across `rules/AGENTS.md`, `soundfont-music/SKILL.md`, specialist skills, and all 5 agents: specialist documentation (`skills/` & `agents/`) AND `music_maker_plugin/midi_map.md` MUST both be read in parallel as co-equal #1 sources of truth, with 100% silent style emulation from `midi_map.md`.
- **FR-003**: Enforce **Zero-Code User Communication** across `rules/AGENTS.md`, `soundfont-music/SKILL.md`, `producer-mindset-workflow/`, and all 5 agents using positive musical phrasing examples (while keeping internal Python toolkit invocation instructions intact for execution).
- **FR-004**: Enforce **Proactive Transitions & Drum Fills** across `rules/AGENTS.md`, `soundfont-music/SKILL.md`, `producer-mindset-workflow/`, `groove-rhythm-drums/SKILL.md`, `orchestration-arrangement/SKILL.md`, and all 5 agents.
- **FR-005**: Update `music_maker_plugin/plugin.json` (`1.6.0`), `README.md`, and `GEMINI.md`, and verify with `agy plugin validate --strict music_maker_plugin` and `code-reviewer`.

## Success Criteria
- **SC-001**: `agy plugin validate --strict music_maker_plugin` passes with 0 errors and 0 warnings.
- **SC-002**: All updated prompt files follow `llm-prompt-optimizer` (RSCIT, positive alternatives, concise framing) with zero contradictions across rules, skills, and agents.
- **SC-003**: `code-reviewer` finds 0 CRITICAL or HIGH issues.
