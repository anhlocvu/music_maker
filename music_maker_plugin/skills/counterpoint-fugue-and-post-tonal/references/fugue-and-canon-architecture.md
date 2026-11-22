# Fugue, Canon Architecture & Large Contrapuntal Forms

## 1. Fugue Anatomy & Terminology (Prout & Saunders)

A **fugue** is not a fixed external mold (like Sonata form) but a **continuous contrapuntal process** with a constant number of voices (commonly 3 or 4: Soprano, Alto, Tenor, Bass).

### Core Building Blocks

1. **Subject**: Short, memorable opening melody in a single unaccompanied voice defining the tonic key, rhythmic character, and contrapuntal opportunities (head motive = distinctive opening 3–5 notes exploitable in episodes/stretto).
   - **Harmonic design**: *Open* (ends on dominant/V for continuous momentum) or *closed* (cadences on I). Design internal rhythmic and intervallic shapes ahead of time so the subject can overlap in **stretto** and invert in **countersubject**.
2. **Answer (Entry 2, at the 5th above / 4th below — Dominant level)**:
   - **Real Answer**: Exact diatonic/chromatic transposition up a `P5` (or down a `P4`) when the subject begins on `1̂`, stays solidly in tonic without leaping `1̂ <-> 5̂` prominently or modulating to `V`.
   - **Tonal Answer (Prout's Law of Tonal Mutation)**: Slightly alters 1–2 intervals near the head (and/or modulation seam) to preserve tonic-dominant harmonic gravity across the authentic vs. plagal half of the scale:
     - When Subject starts on **`5̂`** or leaps immediately **`1̂ -> 5̂`** (or `1̂ -> 3̂ -> 5̂`), Answer responds **`1̂`** or **`5̂ -> 1̂`** (a `P4` answers a `P5`, keeping tonic pitch space centered!).
     - When Subject **modulates to the dominant (`V`)** before ending, Answer modulates back from `V` to **tonic (`I`)**, adjusting at the earliest musical seam.
     - Always answer minor-mode subjects in the **dominant minor** (never dominant major).
3. **Countersubject (CS)**: Consistent contrapuntal accompaniment sung by Voice 1 against Voice 2's Answer, and subsequently passed to each voice after finishing its Subject/Answer.
   - **Mandatory Design Test**: Because CS must appear both **above** and **below** Subject/Answer entries, it MUST be written in **Double Counterpoint at the Octave** (and ideally also the 12th). Give it rhythmic contrast against the subject (e.g., running 16ths/8ths where the subject sustains, or syncopations where the subject steps evenly).
4. **Exposition & Counter-Exposition**:
   - **Order of entries**: Alternate Subject (`I`) and Answer (`V`) across all $N$ voices (e.g., 4-voice: `S(Tonic) -> A(Dom) -> T(Tonic) -> B(Dom)` or inner-to-outer `A -> S -> B -> T`).
   - **Codetta**: Brief 1–3 bar transition inserted between Answer and Entry 3 whenever needed to modulate cleanly back from `V` to `I` or raise melodic tension.
   - **Counter-Exposition** (optional second exposition in `I`/`V`): Swaps voice order or brings in stretto/inverted entries.
5. **Episodes**: Modulatory bridges free of complete Subject/Answer statements (built via **sequential fragmentation** of the head motive or countersubject motifs over invertible counterpoint). Episodes supply tonal travel (`vi`, `IV`, `ii`, `III`) and textural breathing room (`20–35%` of total fugal length).
6. **Middle Entries, Transformational Techniques & Final Climax**:
   - **Stretto**: Overlapping entries of the Subject where Voice $n+1$ enters *before* Voice $n$ finishes. Reserve the tightest overlap (*stretto maestrale*) for the final climax!
   - **Inversion (`Melodic Inversion`)**: Flip intervals upside down (`up M3 -> down M3`, either diatonic/tonal or strict real) for middle/contrary-motion expositions.
   - **Augmentation & Diminution**: Double (`2x`) or halve (`0.5x`) note durations (often pitting augmented cantus bass against normal-speed upper stretto). *Retrograde* is rare in tonal fugue due to low aural recognizability.
   - **Pedal Point**: Extended **Dominant Pedal** sustains harmonic tension into climactic stretto, followed by a brief **Tonic Pedal** closing plagal/authentic resolution.
7. **Double & Triple Fugue**:
   - **Type 1 (Simultaneous)**: Subject 1 & Subject 2 (or 3) enter together from bar 1 in invertible double/triple counterpoint.
   - **Type 2 (Additive Expositions)**: Subject 1 has a complete fugue exposition -> Subject 2 receives its own separate exposition -> final synthesis combines Subject 1 + Subject 2 simultaneously!

## 2. Canon Architecture (Prout)

- **Canon (`Strict Imitation`)**: One leader (*Dux*) followed at a fixed pitch interval (`unison`, `octave`, `5th`, `4th`, `2nd`, etc.) and rhythmic delay (`1 beat`, `1 bar`, `2 bars`) by follower(s) (*Comes*).
- **Workflow (Measure-by-Measure Lockstep)**: Write Bar 1 of *Dux* -> copy exact pitch/interval contour into *Comes* at the target delay/transposition -> immediately compose Bar 2 of *Dux* as playable, consonant counterpoint **against** Bar 2 of *Comes* -> repeat!
- **Types**:
  - **Finite Canon**: Exits strict imitation near the final cadence for a clean polyphonic close.
  - **Perpetual / Infinite Canon (`Round / Rota`)**: Final measure loops smoothly back into Bar 1.
  - **Accompanied Canon**: Two upper canonic voices supported by a free harmonic bass or Cantus Firmus.
  - **Structural Canons**: **Contrary Motion** (mirror inversion), **Augmentation/Diminution** (mensuration canon, where the faster voice completes and switches to free counterpoint until the augmented voice catches up), **Crab Canon** (*cancrizans* — retrograde).

## 3. Goetschius Homophonic & Larger Form Taxonomy

Percy Goetschius situates polyphonic textures alongside large classical architectural forms:
- **Motives & Sentences**: Build from a 1-bar **Ground-Motive** -> 2-bar Semi-Phrase -> 4-bar Phrase -> 8-bar Period (`antecedent + consequent`).
- **Song-Forms**: One-Part, Two-Part (`AB`), Three-Part (`ABA'` Song-Form with Trio/Minuet).
- **Theme & Variations**: Maintain harmonic/bass frame or phrase length while shifting rhythm, counterpoint (canon/fugato variation), mode, and register.
- **Rondo Forms**: **1st Rondo** (`A – B – A`); **2nd Rondo** (`A – B – A – C – A`, contrasted Subordinate Themes in `V` and `vi`/`IV`); **3rd Rondo** (`A – B – A – C – A – B' – A`, symmetrical Sonata-Rondo hybrid).
- **Sonata-Allegro**: Exposition (Principal Theme in `I` -> Transition modulating -> Subordinate Theme in `V` or `III` -> Codetta) -> **Development** (fragmentation, sequence, fugato episodes, distant keys -> retransition on `V` pedal) -> **Recapitulation** (Principal Theme in `I` -> Subordinate Theme transposed to **`I`**) -> Coda.
