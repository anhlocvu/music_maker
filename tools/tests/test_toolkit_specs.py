"""TDD tests for GTR-CTRL symbolic metrics, SF2 spec features (sampleModes=3, exclusiveClass), and MPE MIDI export."""
import os
import struct
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

from engine import sf2, song as song_mod, review  # noqa: E402


def _chunk(tag: bytes, data: bytes) -> bytes:
    pad = b"\x00" if (len(data) & 1) else b""
    return tag + struct.pack("<I", len(data)) + data + pad


def _list(kind: bytes, payload: bytes) -> bytes:
    return _chunk(b"LIST", kind + payload)


def _build_minimal_sf2(path: str) -> str:
    """Build a valid minimal SF2 with:
    - Preset 0:0 'LoopMode3' (sampleModes=3: loop [100..500], then release tail [500..1500])
    - Preset 128:0 'ChokeKit' (keys 42 & 46 share exclusiveClass=1)
    """
    sr = 44100
    n_smpl = 2000
    t = np.arange(n_smpl, dtype=np.float64)
    pcm = (0.5 * np.sin(2.0 * np.pi * 440.0 * t / sr) * 32767.0).astype("<i2")
    smpl_bytes = pcm.tobytes()

    info = _list(b"INFO", _chunk(b"ifil", struct.pack("<HH", 2, 4)) + _chunk(b"INAM", b"TestSF2\x00"))
    sdta = _list(b"sdta", _chunk(b"smpl", smpl_bytes))

    def name20(s: str) -> bytes:
        return s.encode("ascii")[:20].ljust(20, b"\x00")

    # Samples: 0='tone', 1='EOS'
    shdr = b"".join([
        struct.pack("<20sIIIIIBbHH", name20("tone"), 0, n_smpl, 100, 500, sr, 69, 0, 0, 1),
        struct.pack("<20sIIIIIBbHH", name20("EOS"), 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ])

    # Instruments: 0='InstLoop3' (1 zone), 1='InstChoke' (2 zones), 2='EOI'
    inst = b"".join([
        struct.pack("<20sH", name20("InstLoop3"), 0),
        struct.pack("<20sH", name20("InstChoke"), 1),
        struct.pack("<20sH", name20("EOI"), 3),
    ])

    # igen items for 3 instrument zones + terminal
    # Zone 0 (InstLoop3): sampleModes=3, releaseVolEnv=-1200 (0.5s), sampleID=0
    # Zone 1 (InstChoke key 42): keyRange=(42,42), exclusiveClass=1, releaseVolEnv=0 (1.0s), sampleID=0
    # Zone 2 (InstChoke key 46): keyRange=(46,46), exclusiveClass=1, releaseVolEnv=0 (1.0s), sampleID=0
    igen_list = [
        (sf2.SAMPLE_MODES, struct.pack("<H", 3)),
        (sf2.RELEASE_VOL, struct.pack("<h", -1200)),
        (sf2.SAMPLE_ID, struct.pack("<H", 0)),

        (sf2.KEY_RANGE, bytes([42, 42])),
        (sf2.EXCLUSIVE_CLASS, struct.pack("<H", 1)),
        (sf2.RELEASE_VOL, struct.pack("<h", 0)),
        (sf2.SAMPLE_ID, struct.pack("<H", 0)),

        (sf2.KEY_RANGE, bytes([46, 46])),
        (sf2.EXCLUSIVE_CLASS, struct.pack("<H", 1)),
        (sf2.RELEASE_VOL, struct.pack("<h", 0)),
        (sf2.SAMPLE_ID, struct.pack("<H", 0)),

        (0, b"\x00\x00"),
    ]
    igen = b"".join(struct.pack("<H2s", op, val) for op, val in igen_list)
    ibag = b"".join([
        struct.pack("<HH", 0, 0),
        struct.pack("<HH", 3, 0),
        struct.pack("<HH", 7, 0),
        struct.pack("<HH", 11, 0),
    ])
    imod = struct.pack("<HHhHH", 0, 0, 0, 0, 0)

    # Presets: 0=(0,0,'LoopMode3'), 1=(128,0,'ChokeKit'), 2='EOP'
    phdr = b"".join([
        struct.pack("<20sHHHIII", name20("LoopMode3"), 0, 0, 0, 0, 0, 0),
        struct.pack("<20sHHHIII", name20("ChokeKit"), 0, 128, 1, 0, 0, 0),
        struct.pack("<20sHHHIII", name20("EOP"), 0, 0, 2, 0, 0, 0),
    ])
    pbag = b"".join([
        struct.pack("<HH", 0, 0),
        struct.pack("<HH", 1, 0),
        struct.pack("<HH", 2, 0),
    ])
    pgen = b"".join([
        struct.pack("<HH", sf2.INSTRUMENT, 0),
        struct.pack("<HH", sf2.INSTRUMENT, 1),
        struct.pack("<HH", 0, 0),
    ])
    pmod = struct.pack("<HHhHH", 0, 0, 0, 0, 0)

    pdta = _list(
        b"pdta",
        _chunk(b"phdr", phdr)
        + _chunk(b"pbag", pbag)
        + _chunk(b"pmod", pmod)
        + _chunk(b"pgen", pgen)
        + _chunk(b"inst", inst)
        + _chunk(b"ibag", ibag)
        + _chunk(b"imod", imod)
        + _chunk(b"igen", igen)
        + _chunk(b"shdr", shdr),
    )
    riff = _chunk(b"RIFF", b"sfbk" + info + sdta + pdta)
    with open(path, "wb") as f:
        f.write(riff)
    return path


class TestSymbolicMetricsGtrCtrl(unittest.TestCase):
    def test_pce_gc_pip_uip_calculations(self):
        s = song_mod.Song("MetricsTest", bpm=120)
        lead = s.track("lead", "osc_sine")
        # 4 bars of consistent rhythm on single pitch C5 -> PCE = 0, GC = 1.0
        lead.seq("C5 . C5 . | C5 . C5 . | C5 . C5 . | C5 . C5 . |", step=1.0)
        # Unprompted pad plays in 2 of 4 bars
        pad = s.track("pad", "osc_sine")
        pad.seq("E4 - - - | . . . . | G4 - - - | . . . . |", step=1.0)

        rep = review.review_song(s, prompted_tracks=["lead"])
        self.assertIn("metrics", rep)
        m = rep["metrics"]
        # Lead has 3 pairs at 1.0; pad alternates active/rest (15/16 = 0.9375) -> mean 0.9688
        self.assertAlmostEqual(m["groove_consistency"], 0.9688, places=3)
        self.assertGreater(m["pitch_class_entropy"], 0.0)
        # Prompted 'lead' active 4/4 bars, total bars across 2 tracks = 8 -> PIP = 4/8 = 0.5
        self.assertAlmostEqual(m["pip"], 0.5, places=3)
        # Unprompted 'pad' active 2 bars out of 6 active track-bars -> UIP = 2/6 = 0.333
        self.assertAlmostEqual(m["uip"], 1.0 / 3.0, places=3)

    def test_pce_zero_for_single_pitch_class(self):
        s = song_mod.Song("SinglePitch", bpm=120)
        tr = s.track("lead", "osc_sine")
        tr.seq("C4 C5 C4 C5", step=1.0)
        m = review.symbolic_metrics(s)
        self.assertAlmostEqual(m["pitch_class_entropy"], 0.0, places=5)
        self.assertAlmostEqual(m["pip"], 1.0, places=5)
        self.assertAlmostEqual(m["uip"], 0.0, places=5)


class TestSF2SpecFeatures(unittest.TestCase):
    def test_sample_mode_3_plays_loop_then_remainder(self):
        with tempfile.TemporaryDirectory() as tmp:
            sf2_path = _build_minimal_sf2(os.path.join(tmp, "test.sf2"))
            font = sf2.SoundFont(sf2_path)
            try:
                preset = font.preset(0, 0)
                # Sample length = 2000 (~45ms). Loop [100..500] (~9ms).
                # Hold for 0.10s (4410 samples > 2000, so it MUST loop while held),
                # then release plays the remaining tail to sample end (~1500/44100 = 0.034s), NOT 0.5s!
                wav = preset.render(69, 100, dur=0.10, sr=44100)
                self.assertGreater(len(wav), 4410)
                self.assertLess(len(wav), int(0.16 * 44100))
            finally:
                font.close()

    def test_exclusive_class_chokes_open_hihat(self):
        from engine import instruments

        with tempfile.TemporaryDirectory() as tmp:
            sf2_path = _build_minimal_sf2(os.path.join(tmp, "choke.sf2"))
            instruments.register_font("testchoke", sf2_path)
            try:
                s = song_mod.Song("ChokeTest", bpm=120, room=0.0)
                d = s.track("drums", ("testchoke", 128, 0), reverb=0.0)
                # Open hat (46) at beat 0 with dur=0.25 (release=1.0s would ring past 1.1s),
                # closed hat (42) hits at beat 0.5 (0.25s) and MUST choke key 46.
                d.events.append((0.0, 0.25, 46, 100, None))
                d.events.append((0.5, 0.1, 42, 100, None))
                preset = instruments.load(("testchoke", 128, 0))
                self.assertEqual(preset.exclusive_class(46, 100), 1)
                self.assertEqual(preset.exclusive_class(42, 100), 1)
                buf, _ = s._render_track(d, int(1.5 * 44100), keep_pan=False)
                # After key 42 one-shot finishes (~0.47s at key 42 pitch), choked key 46 must be silent
                # rather than ringing out to ~1.125s.
                tail_rms = float(np.sqrt(np.mean(buf[int(0.55 * 44100):] ** 2)))
                self.assertLess(tail_rms, 1e-4)
            finally:
                f_obj = instruments._fonts.pop("testchoke", None)
                if f_obj is not None:
                    f_obj.close()
                instruments.FONTS.pop("testchoke", None)


class TestMpeMidiExport(unittest.TestCase):
    def test_mpe_export_allocates_member_channels_and_emits_rpn_00_06(self):
        import mido

        s = song_mod.Song("MPETest", bpm=120)
        gtr = s.track("guitar", "odguitar")
        # Simultaneous stationary E4 and bent D4->E4 on the same track
        gtr.note("E4", beats=2.0, at=0.0, vel=90)
        gtr.bend("D4", beats=2.0, at=0.0, style="bend_release", semis=2.0, vel=95)
        bass = s.track("bass", "fingerbass")
        bass.bend("E2", beats=2.0, at=0.0, style="scoop", semis=1.0, vel=92)
        drm = s.track("drums", "drums")
        drm.seq("kick . snare .", step=0.5)
        gtr.pedal(0.0, 1.9)

        with tempfile.TemporaryDirectory() as tmp:
            mid_path = os.path.join(tmp, "mpe.mid")
            s.export_midi(mid_path, mpe=True, mpe_bend_range=24)
            mid = mido.MidiFile(mid_path)
            all_msgs = [m for tr in mid.tracks for m in tr]

            # RPN 00 06 on Master Channel 0 with Data Entry CC6 > 0
            ch0_cc = [(m.control, m.value) for m in all_msgs if m.type == "control_change" and m.channel == 0]
            self.assertIn((101, 0), ch0_cc)
            self.assertIn((100, 6), ch0_cc)
            self.assertTrue(any(c == 6 and v == 8 for c, v in ch0_cc), f"Expected Lower Zone N=8 with drums, got {ch0_cc}")
            # Pedal CC64 must go to Master Channel 0
            self.assertIn((64, 127), ch0_cc)

            # The two simultaneous guitar notes must be on two distinct Member Channels (1..8)
            gtr_tr = next(tr for tr in mid.tracks if getattr(tr, "name", "").startswith("guitar"))
            bass_tr = next(tr for tr in mid.tracks if getattr(tr, "name", "").startswith("bass"))
            gtr_note_ons = [m for m in gtr_tr if m.type == "note_on" and m.velocity > 0]
            bass_note_ons = [m for m in bass_tr if m.type == "note_on" and m.velocity > 0]
            self.assertEqual(len(gtr_note_ons), 2)
            self.assertEqual(len({m.channel for m in gtr_note_ons}), 2)
            self.assertTrue(all(1 <= m.channel <= 8 for m in gtr_note_ons))
            # Bass must not collide with guitar's active member channels at t=0
            self.assertNotIn(bass_note_ons[0].channel, {m.channel for m in gtr_note_ons})

            # Pitchwheel messages only on the bent note's member channel, never on the stationary note's channel
            bent_ch = next(m.channel for m in gtr_note_ons if m.note == 62)  # D4
            hold_ch = next(m.channel for m in gtr_note_ons if m.note == 64)  # E4
            pw_channels = {m.channel for m in gtr_tr if m.type == "pitchwheel" and m.pitch != 0}
            self.assertEqual(pw_channels, {bent_ch})
            self.assertNotIn(hold_ch, pw_channels)


if __name__ == "__main__":
    unittest.main()
