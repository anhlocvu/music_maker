"""TDD tests for upgraded multi-point pitch bend, MIDI import/export, and expression helpers."""
import os
import sys
import tempfile
import unittest

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLKIT_DIR = os.path.join(
    REPO_ROOT, "music_maker_plugin", "skills", "soundfont-music", "scripts", "toolkit"
)
if TOOLKIT_DIR not in sys.path:
    sys.path.insert(0, TOOLKIT_DIR)

from engine import sf2, song as song_mod, midi_io, expression  # noqa: E402


class TestPitchCurveAndBends(unittest.TestCase):
    def test_legacy_bend_and_glide_remain_compatible(self):
        n = 4410
        bend_curve = sf2.pitch_curve(n, 44100, 0.1, bend=(2.0, "bend"))
        glide_curve = sf2.pitch_curve(n, 44100, 0.1, bend=(-2.0, "glide"))
        self.assertAlmostEqual(float(bend_curve[0]), 1.0, places=4)
        self.assertAlmostEqual(float(bend_curve[-1]), 2.0 ** (2.0 / 12.0), places=3)
        self.assertAlmostEqual(float(glide_curve[0]), 1.0, places=4)
        self.assertAlmostEqual(float(glide_curve[-1]), 2.0 ** (-2.0 / 12.0), places=3)

    def test_multipoint_norm_bend_release_and_pre_bend(self):
        sr = 1000
        dur = 1.0
        n = 1000
        # Bend up +2st at 25%, hold until 50%, release back to 0st at 75%
        br = ("norm", True, ((0.0, 0.0), (0.25, 2.0), (0.5, 2.0), (0.75, 0.0), (1.0, 0.0)))
        curve = sf2.pitch_curve(n, sr, dur, bend=br)
        self.assertAlmostEqual(float(curve[0]), 1.0, places=4)
        self.assertAlmostEqual(float(curve[350]), 2.0 ** (2.0 / 12.0), places=3)
        self.assertAlmostEqual(float(curve[900]), 1.0, places=4)

        # Pre-bend: starts at +2st at t=0, releases to 0st
        pb = ("norm", True, ((0.0, 2.0), (0.2, 2.0), (0.7, 0.0), (1.0, 0.0)))
        pb_curve = sf2.pitch_curve(n, sr, dur, bend=pb)
        self.assertAlmostEqual(float(pb_curve[0]), 2.0 ** (2.0 / 12.0), places=3)
        self.assertAlmostEqual(float(pb_curve[850]), 1.0, places=4)

    def test_multipoint_seconds_curve_clamps_endpoints(self):
        sr = 1000
        dur = 1.0
        n = 1000
        pts = ("points", False, ((0.2, 0.0), (0.5, -3.0), (0.8, 0.0)))
        curve = sf2.pitch_curve(n, sr, dur, bend=pts)
        self.assertAlmostEqual(float(curve[100]), 1.0, places=4)
        self.assertAlmostEqual(float(curve[500]), 2.0 ** (-3.0 / 12.0), places=4)
        self.assertAlmostEqual(float(curve[900]), 1.0, places=4)

    def test_step_string_three_part_bend_release_and_tilde(self):
        s = song_mod.Song("BendTest", bpm=120)
        tr = s.track("lead", "osc_sine")
        tr.seq("D5^E5^D5 - | D5~E5 - | D5^+2^0 - |", step=0.5)
        self.assertEqual(len(tr.events), 3)
        for ev in tr.events:
            bend = ev[4]
            self.assertIsNotNone(bend)
            self.assertEqual(bend[0], "norm")
            # Peak should be +2.0 semitones and end should return to 0.0
            semis_vals = [pt[1] for pt in bend[2]]
            self.assertAlmostEqual(max(semis_vals), 2.0, places=3)
            self.assertAlmostEqual(semis_vals[-1], 0.0, places=3)

    def test_track_bend_presets_render_and_export_wide_rpn(self):
        import mido

        s = song_mod.Song("WideBend", bpm=120)
        tr = s.track("guitar", "osc_sine")
        tr.bend("A4", beats=2.0, style="bend_release", semis=2.0)
        tr.bend("C5", beats=2.0, style="dive", semis=4.0)
        tr.bend("E5", beats=2.0, style="bend_vibrato", semis=1.0, vibrato_waves=3)
        self.assertEqual(len(tr.events), 3)

        # Render audio should succeed without clipping or NaNs
        mix = s.render()
        self.assertTrue(np.isfinite(mix).all())
        self.assertGreater(float(np.abs(mix).max()), 0.01)

        with tempfile.TemporaryDirectory() as tmp:
            mid_path = os.path.join(tmp, "wide_bend.mid")
            s.export_midi(mid_path)
            mid = mido.MidiFile(mid_path)
            msgs = [m for t in mid.tracks for m in t]
            # Check RPN 0,0 Data Entry MSB >= 4 for the 4-semitone dive
            rpn_msb = [m.value for m in msgs if m.type == "control_change" and m.control == 6]
            self.assertTrue(any(v >= 4 for v in rpn_msb), f"Expected RPN data entry >= 4, got {rpn_msb}")
            pw_vals = [m.pitch for m in msgs if m.type == "pitchwheel"]
            self.assertGreater(len(pw_vals), 10)
            self.assertTrue(any(p < -4000 for p in pw_vals))

    def test_load_midi_into_track_preserves_pitch_bends(self):
        s = song_mod.Song("RoundTrip", bpm=100)
        tr = s.track("lead", "osc_sine")
        tr.bend("G4", beats=2.0, style="delayed_bend", semis=2.0)

        with tempfile.TemporaryDirectory() as tmp:
            mid_path = os.path.join(tmp, "rt.mid")
            s.export_midi(mid_path)
            s2 = song_mod.Song("Imported", bpm=100)
            tr2 = midi_io.load_midi_into_track(s2, "lead", mid_path, "osc_sine", track_index=0)
            self.assertEqual(len(tr2.events), 1)
            imported_bend = tr2.events[0][4]
            self.assertIsNotNone(imported_bend)
            self.assertEqual(imported_bend[0], "points")
            semis_list = [pt[1] for pt in imported_bend[2]]
            self.assertGreater(max(semis_list), 1.5)

    def test_expressive_bends_enriches_sustained_notes_without_clobbering(self):
        s = song_mod.Song("AutoBend", bpm=80)
        tr = s.track("guitar_lead", "osc_sine")
        tr.seq("C5 - - - | D5 . E5 - | G5 - - - |", step=0.5)
        # Pre-set bend on first note; expressive_bends must preserve it
        first_custom = ("norm", True, ((0.0, 0.0), (0.5, 1.0), (1.0, 0.0)))
        s0, d0, k0, v0, _ = tr.events[0]
        tr.events[0] = (s0, d0, k0, v0, first_custom)

        res = expression.expressive_bends(tr, role="guitar", seed=7, min_dur=1.0)
        self.assertGreater(res["bends_added"], 0)
        self.assertEqual(tr.events[0][4], first_custom)
        # Sustained G5 (dur=2.0) should receive a bend curve
        self.assertIsNotNone(tr.events[-1][4])


if __name__ == "__main__":
    unittest.main()
