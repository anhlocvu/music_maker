"""TDD tests for ultra-advanced harmony, voicing, and orchestration review helpers."""
import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLKIT_DIR = os.path.join(
    REPO_ROOT, "music_maker_plugin", "skills", "soundfont-music", "scripts", "toolkit"
)
if TOOLKIT_DIR not in sys.path:
    sys.path.insert(0, TOOLKIT_DIR)

from engine import harmony, voicing, song as song_mod, review  # noqa: E402


class TestAdvancedHarmony(unittest.TestCase):
    def test_extended_qualities_and_polychord_parsing(self):
        c_alt = harmony.parse("G7alt")
        self.assertIsNotNone(c_alt)
        self.assertIn(8, c_alt["pcs"])   # Ab (b9)
        self.assertIn(3, c_alt["pcs"])   # Eb (b13)

        c_lyd = harmony.parse("Fmaj9#11")
        self.assertIsNotNone(c_lyd)
        self.assertEqual(c_lyd["pcs"], {5, 9, 0, 4, 7, 11})

        poly = harmony.parse("D|C7")
        self.assertIsNotNone(poly)
        self.assertEqual(poly["root"], 0)
        self.assertEqual(poly["upper_pcs"], {2, 6, 9})
        self.assertEqual(poly["lower_pcs"], {0, 4, 7, 10})
        self.assertEqual(poly["pcs"], {0, 2, 4, 6, 7, 9, 10})

    def test_neo_riemannian_plr_transformations_are_involutions(self):
        # C major (0, 'maj')
        self.assertEqual(harmony.plr_transform(0, "maj", "P"), (0, "min"))
        self.assertEqual(harmony.plr_transform(0, "maj", "L"), (4, "min"))   # E minor
        self.assertEqual(harmony.plr_transform(0, "maj", "R"), (9, "min"))   # A minor
        self.assertEqual(harmony.plr_transform(0, "maj", "S"), (1, "min"))   # C# minor (Slide)
        self.assertEqual(harmony.plr_transform(0, "maj", "N"), (5, "min"))   # F minor (Nebenverwandt)
        self.assertEqual(harmony.plr_transform(0, "maj", "H"), (8, "min"))   # Ab minor (Hexatonic pole)

        # Involution check: applying any single PLR/S/N/H twice returns original triad
        for op in ("P", "L", "R", "S", "N", "H"):
            r1, q1 = harmony.plr_transform(0, "maj", op)
            r2, q2 = harmony.plr_transform(r1, q1, op)
            self.assertEqual((r2, q2), (0, "maj"), f"Failed involution for {op}")

        # Case-aware & long-name quality guards ("major", "M" vs "min", "m")
        self.assertEqual(harmony.plr_transform(0, "major", "L"), (4, "min"))
        self.assertEqual(harmony.plr_transform(0, "M", "L"), (4, "min"))
        self.assertEqual(harmony.plr_transform(0, "m", "L"), (8, "maj"))

        # Chained operations: PL on C major -> P(C)=Cm -> L(Cm)=Ab major
        self.assertEqual(harmony.plr_transform(0, "maj", "PL"), (8, "maj"))

    def test_negative_harmony_axis_mapping(self):
        # In C, axis maps C(0)<->G(7), E(4)<->Eb(3) => C major {0,4,7} <-> C minor {0,3,7}
        c_maj = {0, 4, 7}
        neg_c = harmony.negative_harmony_pcs(c_maj, tonic="C")
        self.assertEqual(neg_c, {0, 3, 7})

        # G7 {7, 11, 2, 5} -> Fm6 / Dm7b5 {0, 8, 5, 2}
        g7 = harmony.parse("G7")["pcs"]
        neg_g7 = harmony.negative_harmony_pcs(g7, tonic="C")
        self.assertEqual(neg_g7, {0, 2, 5, 8})

    def test_coltrane_cycle_and_barry_harris_and_upper_structures(self):
        centers = harmony.coltrane_cycle("B", direction=-1, include_dominants=False)
        self.assertEqual(centers, ["B", "G", "Eb"])

        chain = harmony.coltrane_cycle("B", direction=-1, include_dominants=True)
        self.assertEqual(chain, ["Bmaj7", "D7", "Gmaj7", "Bb7", "Ebmaj7", "F#7"])

        bh_maj = harmony.barry_harris_scale("C", mode="major")
        self.assertEqual(bh_maj["scale_pcs"], [0, 2, 4, 5, 7, 8, 9, 11])
        self.assertEqual(bh_maj["tonic_sixth_pcs"], {0, 4, 7, 9})
        self.assertEqual(bh_maj["diminished_pcs"], {11, 2, 5, 8})
        self.assertEqual(harmony.barry_harris_scale("C", mode="maj")["scale_pcs"], [0, 2, 4, 5, 7, 8, 9, 11])
        self.assertEqual(harmony.barry_harris_scale("C", mode="m")["scale_pcs"], [0, 2, 3, 5, 7, 8, 9, 11])

        # US VI (A major triad) over C7 -> A(9), C#(1), E(4) + shell E(4), Bb(10)
        us_vi = harmony.upper_structure_triad("C", us_degree="VI", triad_quality="maj")
        self.assertEqual(us_vi["upper_pcs"], {9, 1, 4})
        self.assertEqual(us_vi["shell_pcs"], {4, 10})
        self.assertEqual(us_vi["all_pcs"], {1, 4, 9, 10})


class TestAdvancedVoicingAndReview(unittest.TestCase):
    def test_drop2_drop3_drop24_transforms(self):
        cmaj7_close = [60, 64, 67, 71]  # C4 E4 G4 B4
        self.assertEqual(voicing.drop2(cmaj7_close), [55, 60, 64, 71])
        self.assertEqual(voicing.drop3(cmaj7_close), [52, 60, 67, 71])
        self.assertEqual(voicing.drop24(cmaj7_close), [48, 55, 64, 71])

    def test_so_what_quartal_and_upper_structure_voicings(self):
        sw = voicing.so_what_voicing("D", low=50)
        self.assertEqual(sw, [50, 55, 60, 65, 69])  # D3 G3 C4 F4 A4

        q4 = voicing.quartal_stack("D", voices=4, low=50)
        self.assertEqual(q4, [50, 55, 60, 65])
        self.assertEqual(voicing.quartal_stack("D", voices=0, low=50), [])

        # Polychord support in chord_tones & voice_lead
        poly_tones = voicing.chord_tones("D|C7", voices=5)
        self.assertEqual(len(poly_tones), 5)
        vl_poly = voicing.voice_lead(["D|C7", "Gmaj7"], voices=4, low=48, high=76)
        self.assertEqual(len(vl_poly), 2)

        us_voicing = voicing.upper_structure_voicing("C", us_degree="II", triad_quality="maj", bass_octave=3, upper_octave=4)
        # C3(48) + shell E3(52)/Bb3(58) + D major triad above
        self.assertEqual(us_voicing["shell"][0], 48)
        self.assertEqual(len(us_voicing["upper"]), 3)
        self.assertTrue(min(us_voicing["upper"]) > max(us_voicing["shell"]))

    def test_review_detects_same_family_register_clumping(self):
        s = song_mod.Song("ClumpTest", bpm=100)
        h1 = s.track("horn_1", "french_horn")
        h2 = s.track("horn_2", "french_horn")
        # Timpani (GM 47) playing low 2nd against Contrabass (GM 43) must NOT clump as same family
        cb = s.track("contrabass_part", "contrabass")
        tp = s.track("timp", "timpani")
        # Both horns clumped a minor 2nd apart in low-mid register (< C4=60)
        h1.note("F3", beats=2.0, vel=90)
        h2.note("F#3", beats=2.0, vel=90)
        cb.note("C3", beats=2.0, vel=90)
        tp.note("Db3", beats=2.0, vel=90)

        rep = review.review_song(s)
        self.assertIn("register_clumps", rep)
        self.assertEqual(len(rep["register_clumps"]), 1)
        self.assertEqual(rep["register_clumps"][0]["family"], "brass")


if __name__ == "__main__":
    unittest.main()
