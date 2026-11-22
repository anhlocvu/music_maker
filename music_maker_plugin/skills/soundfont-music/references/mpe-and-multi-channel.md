# MIDI Polyphonic Expression (MPE 1.0 / RP35) & Multi-Channel Allocation

*Grounded strictly in the MIDI Polyphonic Expression (MPE) 1.0 Specification Notes (RP35 / AMEI-MMA CA-034, March 2018).*

---

## 1. Why MPE Matters for `soundfont-music` & DAW Export

Standard MIDI Channel Mode 3 (Poly) shares one Pitch Wheel across all notes on a channel. That breaks expressive polyphonic guitar, pedal-steel, and string writing when one note bends (`D4^E4`) while another rings unchanged (`E4`). **MPE solves this by assigning each active note to its own Member Channel** while keeping zone-wide controls on a shared Master Channel.

---

## 2. Zones & Configuration (`RPN 00 06`)

MPE 1.0 restricts splits to **at most two contiguous zones**:

| Zone | Master Channel | Member Channels | Configuration (`RPN 00 06`, Data Entry MSB) |
|---|---|---|---|
| **Lower Zone** | Channel 1 (`ch = 0`) | Channels `2 .. N+1` (`ch = 1..N`) | Sent on `ch = 0`: `CC101=0, CC100=6, CC6=N` (`N=0` disables zone) |
| **Upper Zone** | Channel 16 (`ch = 15`) | Channels `15 .. 16-N` (`ch = 14..15-N`) | Sent on `ch = 15`: `CC101=0, CC100=6, CC6=N` (`N=0` disables zone) |

- **Entering/leaving MPE**: Stop all ongoing notes and reset controllers (`CC121`) on affected channels.
- **GM Drum Coexistence**: When exporting a GM arrangement that uses Percussion on Channel 10 (`ch = 9`) alongside an MPE Lower Zone, cap Lower Zone member channels at `N = 8` (MIDI Channels `2..9`, `ch = 1..8`) so MPE voices never collide with Channel 10 drums.

---

## 3. Note-Level vs. Zone-Level Messages (Section 2.3–2.6)

MPE 1.0 defines three active per-note touch dimensions on **Member Channels**:
1. **Pitch Bend (Glide / X-axis, 14-bit)**:
   - Valid range: `±0` to `±96` semitones (typical MPE default: `±48` semitones; or `±2..±24` for SoundFont compatibility).
   - **Pitch Bend Sensitivity (`RPN 00 00`)**: Must be sent to **every Member Channel** with identical semitone values (`CC101=0, CC100=0, CC6=semis, CC38=0`).
2. **Channel Pressure (Press / Z-axis, 7-bit)**: Per-note aftertouch on Member Channels; Channel Pressure on Master Channel applies globally across sounding notes. (14-bit CC70/102 aftertouch was removed in final MPE 1.0.)
3. **CC 74 (Slide / Timbre / Y-axis, 7-bit)**: Only CC 74 is valid per-note (no 14-bit LSB CC 106 in final MPE 1.0).

**Zone-Scope Messages (Master Channel only)**:
- `CC 64` (Sustain/Damper), `CC 7` (Volume), `CC 10` (Pan), Modulation (`CC 1`), and Program Change (in Mode 4) belong on the Master Channel. They are *not recommended* at the Member Channel level.
- Note-on and note-off messages received on the Master Channel itself are valid and apply globally with zero per-note bend offset.

---

## 4. Channel Allocation & Clean State Rules (Section 3.2 & 3.3)

To preserve musical fidelity when assigning notes to Member Channels (`export_midi(..., mpe=True)`):
1. **Minimize polyphonic collisions**: Prefer an idle channel with zero active notes (or one whose same MIDI key most recently turned off, if no active bend conflict exists).
2. **Isolate simultaneous bends**: Never place two overlapping notes that carry *different* pitch-bend curves onto the same Member Channel.
3. **Protect note release tails (Sec 3.3.3)**: After a `note_off`, subsequent `pitchwheel` resets or bends for a *new* note must not corrupt the releasing tail of the old note—allocate a fresh Member Channel while the prior note decays, or reset `pitchwheel = 0` cleanly *before* the next `note_on`.
4. **Reset per-note pressure/bend before reuse**: Zero out stale `pitchwheel` (`0`) prior to triggering a new unbent note on a recycled Member Channel.
5. **Running-status safety**: Treat `note_on` with `velocity == 0` as `note_off` with release velocity `64` (not `0`).
