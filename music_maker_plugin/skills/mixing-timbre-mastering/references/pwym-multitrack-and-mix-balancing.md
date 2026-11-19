# Mix Balancing, Sound-Box Space & Multitrack Workflow (PWYM Curriculum & Gibson)

*Distilled faithfully from NYU "Play With Your Music" Curriculum (Modules 4–5: Alex Case, Ethan Hein, Kevin Killen) and `study-music/parts/mixing.md` (David Gibson, "The Art of Mixing").*

## 1. Fundamental Mix Priority (Alex Case)
> "Balancing a mix isn't a one time, set-it and leave-it process; it is a constant part of the mix session."

- **The Core Quartet Never Gets Buried**: In any arrangement, keep the core musical pillars—**Lead/Soloist, Snare, Kick, and Bass**—clearly audible and in musical proportion. Never let them sink beneath a wall of guitars, thick pads, distortion, or excessive reverb.
- **Three Primary Mixing Controls** (mastered *before* heavy FX):
  1. **Faders** (relative track gain / volume),
  2. **Pan Pots** (Left–Right stereo placement),
  3. **Mute Buttons** (subtracting redundant clutter).
- **Bracketing Method ("Too Hot vs. Too Cold")**: To dial in a track's relative level (e.g., Lead, Drum Kit, or Bass against the "Mix-Minus" everything else):
  1. Push the level up until it is unmistakably **too loud**.
  2. Pull back until it is unmistakably **too weak**.
  3. Narrow the bracket iteratively, listening across contrasting sections (verse, pre-chorus, chorus) rather than tuning for one isolated bar.
- **Bass Translation Caution**: Headphones and small speakers often distort or under-represent sub-bass (`<80 Hz`), and untreated rooms create bass peaks/nulls. Always verify bass-to-kick balance numerically (RMS/spectral balance) and across multiple playback contexts rather than boosting sub-bass blindly.

---

## 2. The 3D "Sound-Box" Mix Model (Gibson / Dockwray & Moore)
Visualize every instrument inside a 3D stereo box:
- **X-Axis (Left ↔ Right)**: **Panning** (`pan` in `-1.0` to `+1.0`). Keep kick, snare, bass, and primary lead centered (`0.0`); spread rhythmic percussion, doubled guitars/keys, and harmonic fillers asymmetrically left/right for width.
- **Y-Axis (Low ↔ High)**: **Pitch & Frequency Spectrum**. Separate octaves and filter ranges at the arrangement stage (`arrangement-for-mix.md`) so two instruments don't occupy the same X–Y coordinate simultaneously.
- **Z-Axis (Front ↔ Back)**: **Loudness + Dry/Wet Reverb**. Louder, drier, brighter sounds sit in front (foreground); quieter, darker, more reverberant sounds sit behind (background).

---

## 3. Dual Delivery: Full Stereo Mix vs. `multi_track/` DAW Stems
When delivering a finished song in `music_maker_plugin`:
1. **Full Mix WAV (`out/<song>.wav`)**: Uses full intended panning (`pan`), stereo autopan, reverb, and balanced track levels so the standalone render sounds wide and finished.
2. **DAW Multi-Track Stems (`out/<song>/multi_track/*.wav`)**:
   - **Preserve** all musical & expressive effects (`reverb`, `vibrato`, `release` cut, `bends`, `pedal`, timbre, relative gain balance).
   - **Center Pan (`keep_pan=False` → `pan=0.0`)**: Do NOT bake track `pan` into stems, giving the mixing engineer/user clean mono/centered-stereo stems to pan freely in their DAW.
   - **Grid Alignment**: Every stem MUST start cleanly at **beat 0** with identical time origin so dragging the `multi_track/` folder into any DAW snaps every track onto the grid automatically.
