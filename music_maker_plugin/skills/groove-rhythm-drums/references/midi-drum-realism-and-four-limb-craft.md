# MIDI Drum Realism, 4-Limb Ergonomics & Humanizing Craft

Program acoustic and hybrid MIDI drum tracks that breathe like a four-limbed human drummer instead of a mechanical step grid.

## 1. Four-Limb Polyphony & Physical Constraints (`SOS 20 Tips` & `Get Real`)

- **Strict 4-Voice Ceiling**: A real drummer has two arms and two feet (`<= 4 simultaneous kit voices`). Never trigger two toms + ride + crash + closed hi-hat on the same tick in acoustic tracks.
- **Mute Hats/Rides During Tom Fills**: Hands playing snare/tom fills cannot simultaneously keep steady 8th/16th patterns on the hi-hat or ride. Strip conflicting cymbal hits whenever hands move to toms.
- **Two-Handed Fast Hats**: Above brisk mid-tempos, continuous 16th-note hi-hats require alternating right/left strokes—leaving no free hand to strike a backbeat snare + crash on top without dropping one 16th hi-hat note.
- **Dominant-Hand Asymmetry (`Left / Right / Left / Right`)**: Shift MIDI velocities systematically between alternating strokes on 16th hi-hats and snare rolls (e.g., stronger dominant hand `~92`, softer off-hand `~68`, or 3-note Moeller tapering `acc -> tap -> rebound`).
- **Consecutive-Hit Velocity Roll-Off**: Rapid repeated hits on the same drum or bass pedal lose stroke travel, reducing peak velocity naturally. For quick consecutive bass-drum doubles, contrast a slightly rounder, softer pickup kick against a sharper accented downbeat kick.
- **Implement & Kit Consistency**:
  - Avoid instantaneous switching between **brush snare** and **stick rimshots**, or mixing simultaneous steady **ride cymbal + hi-hat** across opposite kit sides in naturalistic tracks.
  - Constrain kit size to believable studio pieces (**2–3 toms**, avoid arbitrary exotic percussion clutter) and avoid excessive loud crashes on the same cymbal back-to-back (alternate **`CrashCymbal1` [`49 / C#2`]** and **`CrashCymbal2` [`57 / A2`]**).

---

## 2. "Weeding" Busy Loops & "Doubling Up" Section Evolution (`Programming Realistic Drum Parts`)

Stop treating a 1-bar preset loop as a finished drum track:

1. **Weeding Pass (Subtraction First)**:
   - Strip busy preset fills ("Preset Zero syndrome"): pare back redundant kicks to **1–2 essential harmonic/bass-locking hits per bar**.
   - Mute identical cloned snare **ghost notes** that repeat identically every single bar (predictable ghost notes betray MIDI programming immediately).
   - Remove unnecessary crashes/percussion clutter before building section momentum.
2. **"Doubling Up" Pipeline (`1 -> 2 -> 4 -> 8` Bars)**:
   - **1 Bar -> 2 Bars**: Duplicate your weeded 1-bar pocket; in Bar 2, displace a secondary kick by an `8th` or `16th` and vary velocities subtly.
   - **2 Bars -> 4 Bars**: Duplicate to 4 bars; toggle a ghost snare or shift an open hi-hat lift in Bars 3–4 so the phrase breathes as one sentence.
   - **4 Bars -> 8 Bars**: Duplicate to 8 bars; reserve **Bar 8** for a transition fill (dropping hats as toms enter) and land **Crash 1** on the return Beat 1 of the next section.
3. **Asymmetric Variation Chaining**: Build four 1-bar variations around a master groove (`1, 2, 3, 4`) and chain unpredictably (`1/2/3/4` in Verse 1, `2/4/2/3` in Verse 2) instead of repeating bar 1 endlessly.

---

## 3. Micro-Timing, Groove Extraction & Iterative Quantize

- **Replace Rigid `100%` Snap with Iterative Quantize**: Tighten sloppy hits partway (`10%–50%` strength toward grid) so `50%–90%` of organic timing spread remains intact.
- **Voice-Specific Timing Push/Pull**:
  - Push **`Kick` (`1 & 3`) or `Snare`** subtly **ahead** of the beat (`-5..-12 ms`) for disco/pop/country urgency.
  - Lay back the **snare** (`+8..+18 ms` late) for blues, neo-soul, and slow pocket funk feel.
  - Never trigger simultaneous hits (kick + hi-hat + crash) on the **exact same sample tick**—offset companion limbs microscopically (`2–8 ms`) to simulate acoustic physical arrival.
- **Selective Swing & Grid Conversions**: Apply swing selectively to **hi-hats and top percussion** (`1/8`, `1/16`, `1/32`) without dragging downbeat kicks/snares; or convert straight 16th rock/funk grooves into instant **hip-hop pocket** by re-quantizing onto a **`24`-step (`16th-triplet`) grid** (`SOS Effective Drum Programming Part 1`).
- **Organic Tempo Breathing & Global Dynamics**:
  - Nudge song tempo subtly (`+2..+4 BPM` lifting into choruses, gentle easing into bridges, slight rallentando on tags).
  - Automate section-wide **Global Velocity Shift** upward into high-intensity choruses—because real kits change **bright overtone timbre**, not just dB gain, when struck harder.

---

## 4. Realistic Panning & Kit Ambience (`Get Real` & `20 Tips`)

- **Choose One Perspective & Stay Subtle**: Standardize on **Audience View** (right-handed drummer facing listener): **`Kick` & `Snare` dead center**, **`Hi-Hat` slightly right**, **`Toms`** cascading moderately **right-to-left (high -> floor)**, **`Crash` & `Ride`** gently offset—avoid extreme hard-left/hard-right drum pans.
- **Room Cohesion Over Heavy Reverb**: Route kit tracks to a subtle shared short studio room ambience (`~20 ms` pre-delay, low-cut EQ, keep **Kick driest**), glue gently on the drum bus (`~2:1` ratio, **`10–20 ms` attack** to preserve transient punch), and reserve aggressive parallel compression or heavy tails for deliberate style choices.
