# Post-Tonal Pitch-Class Set Theory, Total Voice Leading & 12-Tone Serialism

## 1. Pitch-Class Sets, Normal Order, Prime Form & Interval Vectors

Using integer pitch-class notation (`C=0, C#=1, D=2, Eb=3, E=4, F=5, F#=6, G=7, Ab=8, A=9, Bb=10 (t), B=11 (e)`):

### Computing Prime Form (Open Music Theory / Rahn Algorithm)
1. **Extract** unique pitch classes modulo 12 (remove duplicates & octave registers).
2. **Normal Order**: Arrange in ascending chromatic order inside `< 12` semitones by choosing the rotation with the **smallest outer span** (`last - first`); break ties by minimizing span from left (`2nd - 1st`, `3rd - 1st`, ...).
3. **Transpose** so first pc = `0` (`T_{-first}`).
4. **Invert** the result (`(12 - x) mod 12` or `(-x) mod 12`), put into Normal Order, and transpose first pc = `0`.
5. **Compare**: Choose whichever is more compactly packed (`Rahn (1980)` compares from the **right** so intervals pack smallest-to-the-left, e.g. `5-20 = [0,1,5,6,8]`, whereas `Forte (1973)` compares from the **left**, e.g. `[0,1,3,7,8]`; OMT / Rahn is standard in modern computation).
- **Visual Disc Diagram ("Tone Clock" / *de Toonklok*, Absil & Schat)**: Plot pitch classes on a 12-hour dial (`0` at 12 o'clock). **Transposition ($T_n$)** rotates the polygon clockwise by $n$ steps; **Inversion ($I_n$)** flips the dial across a diameter; overlapping two rotated dials reveals exact **common-tone preservation** instantly.

### Interval Class Vector (ICV) & Combinatorial Enumeration (Hook)
- Each pc-set has a 6-digit **Interval Class Vector `[n1 n2 n3 n4 n5 n6]`** counting occurrences of interval classes `ic1` (m2/M7) through `ic6` (tritone). Pairs of sets with **different prime forms** yet **identical ICVs** are **Z-related** (e.g., All-Interval Tetrachords `4-Z15 [0,1,4,6]` and `4-Z29 [0,1,3,7]`, both `[1,1,1,1,1,1]`).
- **Julian Hook / Pólya Enumeration Counts (mod-12)**:

| Cardinality $k$ | Raw PC-Sets $\binom{12}{k}$ | $T_n / T_n I$ Set Classes (24 ops) | $T_n$-Only Classes (SG1, 12 ops) |
|---|---|---|---|
| `0` / `12` | `1` / `1` | `1` / `1` | `1` / `1` |
| `1` / `11` | `12` / `12` | `1` / `1` | `1` / `1` |
| `2` / `10` | `66` / `66` | `6` / `6` | `6` / `6` |
| `3` / `9` | `220` / `220` | **`12`** / `12` | `19` / `19` |
| `4` / `8` | `495` / `495` | **`29`** / `29` | **`43`** / `43` |
| `5` / `7` | `792` / `792` | **`38`** / `38` | `66` / `66` |
| `6` | `924` | **`50`** | `80` |
| **Total ($0..12$)** | `4096` | **`224`** *(non-trivial 3..9: `208`)* | **`352`** |

### Cohn's Tetrahedral Tetrachordal Voice-Leading Space
- All **29 $T_n/T_nI$ tetrachords** organize into a 3D **Tetrahedron** where edges connect sets differing by **one single semitone displacement** (`P`-relation, e.g., `[0123] <-> [0124] <-> [0235]`).
- The **4 Tetrahedron Vertices** hold the four all-combinatorial tetrachord sites: **`A = [0123]`** (chromatic cluster), **`B = [0167]`** & **`C = *0167*`** (Berg/Bartók double-tritone-fifth redundancy pair), and **`D = [0127]`** (`4-6`), while symmetrical **`[0268]`** and **`[0369]`** sit along Edge `BC`.

## 2. Joseph Straus's Total Voice Leading (`IFUNC` & `imultiset`)

Instead of tracking only 1-to-1 linear voices, **Total Voice Leading** captures the complete $x \cdot y$ ordered pc-interval envelope between Set $X$ and Set $Y$ via David Lewin's **`IFUNC(X, Y)(i)`** ("in how many ways ordered pc interval $i \in \{0..11\}$ spans from $X$ to $Y$"):

1. **`imultiset`**: Write all $x \cdot y$ ordered differences `(y - x) mod 12` as a multiset (e.g., two trichords -> 9-interval envelope; two tetrachords -> 16-interval envelope). Put into normal form by eliminating doublings, finding standard normal order, and reinstating doublings.
2. **Hyper-Transposition (`<Tn>`)**: Transposing $Y$ by $T_n$ (while holding $X$) shifts **every interval** in the `imultiset` up by $+n \pmod{12}$ (`<Tn>`). Thus two progressions sharing `<T0>` or related by `<Tn>` project the **exact same voice-leading contour/shape** at different intervallic heights!
3. **Hyper-Inversion (`<In>`) & Order Reversal**: Reversing $X \to Y$ into $Y \to X$ (or inverting both $X$ and $Y$ around the same axis) inverts the `imultiset` at `<I0>` (`(12 - i) mod 12`); more generally, `<In>` pairs corresponding intervals summing to $n$.
4. **Inversional Symmetry Laws**:
   - If $X = Y$ (`T0`), the `imultiset` matches the traditional interval vector symmetric around `<I0>` (`0` & `6`).
   - If $Y = T_n(X)$, the `imultiset` is self-inversional at **`<I_{2n}>`** (symmetric around `n` & `n+6`).
   - If both $X$ and $Y$ are independently inversionally symmetrical, their Total Voice Leading is always inversionally symmetrical.
5. **Transpositional Combination (`TC`) & Multiple Parentage**: Every `imultiset(X -> Y)` automatically satisfies **Transpositional Combination** equivalent to $I(X) * Y$: columns embed $Y$-type sets transposed by $I(X)$, and rows embed $I(X)$-type sets transposed by $Y$. Crucially, **disparate chord pairs can share identical Total Voice Leading** (**Multiple Parentage**, e.g., `[06] -> [048]`, `[06] -> [024]`, and `[02] -> [048]` all generate `i(02468t)`, and Bartók switches `[01] <-> [06]` with `[05] <-> [06]` to project identical `i(0167)`).

## 3. Twelve-Tone Serialism (`P, R, I, RI`) & Invariance

- **48 Row Forms**: Built from an ordered 12-pc permutation **Prime $P_n$** (indexed by starting pitch class `n = 0..11`):
  - **$I_n$** (Inversion starting on pc `n`): Replace every ordered interval $i$ in $P$ with its complement **`12 - i`**.
  - **$R_n$** (Retrograde **ending** on pc `n` of $P_n$): Exact reverse of $P_n$; its ordered intervals equal the **reverse of $I$'s intervals**.
  - **$RI_n$** (Retrograde Inversion **ending** on pc `n` of $I_n$): Exact reverse of $I_n$; its ordered intervals equal the **reverse of $P$'s intervals**.
- **Segmental Invariance Theorem (Open Music Theory / Webern Op. 28)**:
  - **How to hold a segment pitch-class invariant across row changes**:
    1. Locate two segments (dyads, trichords, tetrachords) in $P_0$ belonging to the **same set class**.
    2. Compute the $T_n$ or $I_n$ operation mapping Segment A -> Segment B.
    3. Transforming the entire row by that exact $T_n$ or $I_n$ holds those pitch-class segments invariant (e.g., if discrete tetrachord 1 `[6,7,8,9]` maps via $T_8$ to discrete tetrachord 3 `[2,3,4,5]`, then transforming the row by $T_8$ maps the last tetrachord right onto the first!).
- **Combinatoriality & Derived Rows**:
  - **Hexachordal Combinatoriality** (Schoenberg/Babbitt): Pair $P_x$ with an inverted/transposed form (often $I_{x+5}$) whose first 6 pcs are the exact **complement** of $P_x$'s first 6 pcs, forming complete 12-pc aggregates both horizontally and vertically without octave doubling.
  - **Derived Rows** (Webern Op. 24 `[0,1,4]`): Construct the full 12-tone row out of 4 disjoint transformations (`P, RI, R, I`) of a single generative trichord or 3 statements of a generative tetrachord.
