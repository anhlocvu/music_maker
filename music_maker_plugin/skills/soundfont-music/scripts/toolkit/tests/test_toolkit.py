"""Unit tests for music_maker_plugin soundfont-music toolkit upgrades."""
import os
import shutil
import sys
import tempfile
import unittest
import wave

import mido
import numpy as np

TOOLKIT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if TOOLKIT_DIR not in sys.path:
    sys.path.insert(0, TOOLKIT_DIR)

from analyze_midi import analyze_directory, format_markdown
from engine.midi_io import load_midi_into_track, parse_midi_file
from engine.song import Song


def _read_wav_stereo(path):
    with wave.open(path, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        arr = np.frombuffer(frames, dtype="<i2").astype(np.float32) / 32767.0
        return arr.reshape(-1, wf.getnchannels()), wf.getframerate()


def _write_test_midi(path, notes, pedals=None, channel=0, program=0, bpm=120):
    mid = mido.MidiFile(ticks_per_beat=480)
    tr = mido.MidiTrack()
    tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    tr.append(mido.Message("program_change", channel=channel, program=program, time=0))
    events = []
    for start_beat, dur_beat, note, vel in notes:
        events.append((int(start_beat * 480), 2, dict(type="note_on", note=note, velocity=vel)))
        events.append((int((start_beat + dur_beat) * 480), 0, dict(type="note_off", note=note, velocity=0)))
    for p_start, p_end in (pedals or []):
        events.append((int(p_start * 480), 1, dict(type="control_change", control=64, value=127)))
        events.append((int(p_end * 480), 0, dict(type="control_change", control=64, value=0)))
    events.sort(key=lambda x: (x[0], x[1]))
    last = 0
    for tick, _, kw in events:
        tr.append(mido.Message(channel=channel, time=tick - last, **kw))
        last = tick
    mid.tracks.append(tr)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mid.save(path)


class ToolkitUpgradeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="music_maker_test_")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_pedal_extends_audio_and_writes_cc64_midi(self):
        song_dry = Song("NoPedal", bpm=120, room=0.0)
        t_dry = song_dry.track("lead", "osc_sine", reverb=0.0)
        t_dry.seq("C4 . . .", step=0.5)
        mix_dry = song_dry.render(trim=True)

        song_ped = Song("WithPedal", bpm=120, room=0.0)
        t_ped = song_ped.track("lead", "osc_sine", reverb=0.0)
        t_ped.seq("C4 . . .", step=0.5)
        t_ped.pedal(0.0, 4.0)
        mix_ped = song_ped.render(trim=True)

        self.assertGreater(len(mix_ped), len(mix_dry) * 2)

        midi_path = os.path.join(self.tmp, "pedal.mid")
        song_ped.export_midi(midi_path)
        parsed = parse_midi_file(midi_path)
        self.assertEqual(len(parsed["tracks"][0]["pedals"]), 1)
        s_p, e_p = parsed["tracks"][0]["pedals"][0]
        self.assertAlmostEqual(s_p, 0.0, places=2)
        self.assertAlmostEqual(e_p, 4.0, places=2)

    def test_strum_and_arpeggio_generate_expected_notes(self):
        song = Song("Phrasing", bpm=120, room=0.0)
        t = song.track("piano", "osc_sine")
        t.strum("C4+E4+G4", beats=2.0, spread=0.05, vel=90)
        self.assertEqual(len(t.events), 3)
        self.assertLess(t.events[0][0], t.events[1][0])
        self.assertLess(t.events[1][0], t.events[2][0])
        self.assertAlmostEqual(t.length(), 2.0, places=3)

        t.arpeggio("C4+E4+G4", step=0.25, beats=1.0, pattern="updown", hold=False)
        self.assertEqual(len(t.events), 7)
        self.assertAlmostEqual(t._cursor, 3.0, places=3)

    def test_export_stems_centers_pan_and_keeps_effects(self):
        song = Song("StemTest", bpm=120, room=0.8)
        t_left = song.track("bass", "osc_sine", pan=-1.0, reverb=0.4, volume=0.9)
        t_left.seq("C3 - - -", step=0.5)
        t_right = song.track("lead", "osc_sine", pan=1.0, reverb=0.2, volume=0.8)
        t_right.seq("G4 - - -", step=0.5)

        # Full mix keeps stereo pan
        full_mix = song.render(trim=True)
        left_energy_bass_region = float(np.mean(np.abs(full_mix[:8000, 0])))
        self.assertGreater(left_energy_bass_region, 0.0)

        # Multi-track stems must center pan (L == R for centered mono synth + stereo reverb check)
        song_no_rev = Song("StemCenter", bpm=120, room=0.0)
        song_no_rev.track("hard_left", "osc_sine", pan=-1.0, reverb=0.0).seq("C4 -", step=0.5)
        song_no_rev.track("hard_right", "osc_sine", pan=1.0, reverb=0.0).seq("E4 -", step=0.5)
        stems_dir = os.path.join(self.tmp, "multi_track")
        paths = song_no_rev.export_stems(stems_dir, keep_pan=False)

        self.assertEqual(len(paths), 2)
        arr0, _ = _read_wav_stereo(paths[0])
        arr1, _ = _read_wav_stereo(paths[1])
        self.assertEqual(arr0.shape, arr1.shape)
        self.assertTrue(np.allclose(arr0[:, 0], arr0[:, 1], atol=1e-4))
        self.assertTrue(np.allclose(arr1[:, 0], arr1[:, 1], atol=1e-4))

        # Reverb effect is preserved when room > 0
        stems_fx_dir = os.path.join(self.tmp, "multi_track_fx")
        fx_paths = song.export_stems(stems_fx_dir, keep_pan=False)
        arr_fx, sr = _read_wav_stereo(fx_paths[0])
        # Tail after 1s (2 beats at 120 BPM) should still carry reverb energy
        tail_rms = float(np.sqrt(np.mean(arr_fx[sr : sr + sr // 2] ** 2)))
        self.assertGreater(tail_rms, 1e-4)

    def test_analyze_midi_reports_project_folders_and_full_readme(self):
        midi_root = os.path.join(self.tmp, "midi")
        ballad_proj = os.path.join(midi_root, "ballad beat")
        _write_test_midi(
            os.path.join(ballad_proj, "drum.mid"),
            [(0.0, 0.25, 36, 110), (1.0, 0.25, 38, 105), (2.0, 0.25, 36, 110), (3.0, 0.25, 38, 108)],
            channel=9,
            bpm=72,
        )
        _write_test_midi(
            os.path.join(ballad_proj, "piano.mid"),
            [(0.0, 1.0, 60, 80), (0.04, 1.0, 64, 78), (0.08, 1.0, 67, 75)],
            pedals=[(0.0, 3.9)],
            channel=0,
            bpm=72,
        )
        readme_text = (
            "# Ballad Beat\n"
            "Style: Acoustic Pop Ballad\n"
            "BPM: 72\n"
            "Notes: Soft rolled piano chords with sustain pedal, minimal kick and snare pocket."
        )
        with open(os.path.join(ballad_proj, "readme.md"), "w", encoding="utf-8") as fh:
            fh.write(readme_text + "\n")

        lofi_proj = os.path.join(midi_root, "lofi_sketch")
        _write_test_midi(
            os.path.join(lofi_proj, "bass.mid"),
            [(0.0, 0.5, 36, 95), (1.5, 0.5, 39, 90)],
            channel=0,
            bpm=85,
        )

        report = analyze_directory(midi_root)
        self.assertEqual(len(report), 2)
        md = format_markdown(midi_root, report)

        self.assertIn("ballad beat", md)
        self.assertIn("drum.mid", md)
        self.assertIn("piano.mid", md)
        self.assertIn("Pedal CC64: 1", md)
        self.assertIn("rolled=1", md)
        self.assertIn("lofi_sketch", md)
        self.assertIn("bass.mid", md)
        self.assertIn(readme_text, md)
        # Ensure README appears after the MIDI file analysis for ballad beat
        self.assertGreater(md.index(readme_text), md.index("piano.mid"))
        self.assertIn("No readme.md found in this project folder.", md)

        # Pointing directly at a single project folder also returns its tracks and full readme
        single_proj_report = analyze_directory(ballad_proj)
        self.assertEqual(len(single_proj_report), 1)
        self.assertEqual(single_proj_report[0]["project"], "ballad beat")
        self.assertEqual(single_proj_report[0]["readme"], readme_text)
        self.assertEqual(single_proj_report[0]["readme_file"], "readme.md")

        # Verify load_midi_into_track preserves notes + CC64 pedals
        song = Song("Imported", bpm=72)
        tr = load_midi_into_track(song, "piano", os.path.join(ballad_proj, "piano.mid"), "osc_sine")
        self.assertEqual(len(tr.events), 3)
        self.assertEqual(len(tr.pedals), 1)

    def test_voicing_voice_lead_minimizes_motion_and_avoids_low_mud(self):
        from engine.voicing import apply_voicings, voice_lead

        chords = ["Cmaj7", "Am7", "Dm9", "G7"]
        voicings = voice_lead(chords, voices=4, low=48, high=76, against=[[36], [45], [38], [43]])
        self.assertEqual(len(voicings), 4)
        for v in voicings:
            self.assertEqual(len(v), 4)
            self.assertTrue(all(48 <= p <= 76 for p in v))
            self.assertEqual(v, sorted(v))
            # No minor second or minor ninth inside voicing
            for i in range(len(v)):
                for j in range(i + 1, len(v)):
                    self.assertNotIn(abs(v[j] - v[i]), (1, 13))

        song = Song("Voiced", bpm=100)
        tr = song.track("epiano", "osc_sine")
        apply_voicings(tr, voicings, beats=4.0, vel=82, strum=0.02)
        self.assertEqual(len(tr.events), 16)
        self.assertAlmostEqual(tr.length(), 16.0, places=2)

    def test_expression_humanize_is_deterministic_and_preserves_bounds(self):
        from engine.expression import humanize_song, humanize_track

        def _make_song():
            s = Song("Human", bpm=110)
            drums = s.track("drums", "osc_sine")
            drums.seq("kick . snare . kick . snare .", step=0.5, repeat=4)
            lead = s.track("lead", "osc_sine")
            lead.seq("C5 D5 E5 G5 A5 G5 E5 D5", step=0.5, repeat=2)
            return s

        s1 = _make_song()
        s2 = _make_song()
        r1 = humanize_song(s1, roles={"drums": "drums", "lead": "melody"}, seed=42)
        r2 = humanize_song(s2, roles={"drums": "drums", "lead": "melody"}, seed=42)
        self.assertEqual(s1.tracks[1].events, s2.tracks[1].events)
        self.assertIn("lead", r1)
        self.assertGreater(r1["lead"]["timing_sd_ms"], 0.0)
        for start, dur, key, vel, _ in s1.tracks[1].events:
            self.assertGreaterEqual(start, 0.0)
            self.assertGreater(dur, 0.0)
            self.assertTrue(1 <= vel <= 127)

        # Standalone single-track humanize also works
        s3 = _make_song()
        humanize_track(s3.tracks[1], role="melody", seed=99, bpm=110)
        self.assertNotEqual(s3.tracks[1].events, _make_song().tracks[1].events)

    def test_patterns_lookup_and_conversion_to_steps(self):
        from engine.patterns import drum_stats_suggest, list_patterns, pattern_to_steps

        all_pats = list_patterns(source="all")
        self.assertGreaterEqual(len(all_pats), 700)

        afro = list_patterns(query="AfroCub")
        self.assertTrue(any("AfroCub" in p["name"] for p in afro))

        steps = pattern_to_steps(afro[0])
        self.assertIsInstance(steps, dict)
        self.assertTrue(len(steps) > 0)
        combined = pattern_to_steps(afro[0], combine=True)
        self.assertEqual(len(combined.replace("|", "").split()), 16)

        # Renderable on a Song track
        song = Song("DrumPat", bpm=115)
        tr = song.track("drums", "osc_sine")
        tr.seq(combined, step=0.25)
        self.assertGreater(len(tr.events), 0)
        self.assertAlmostEqual(tr._cursor, 4.0, places=2)

        # Empirical Groove MIDI Dataset suggestion
        stat_seq = drum_stats_suggest("funk", bars=2, seed=7)
        self.assertEqual(len(stat_seq.replace("|", "").split()), 32)

    def test_review_detects_low_interval_mud_and_vertical_rubs(self):
        from engine.review import format_review, review_song

        song = Song("Muddy", bpm=120)
        # Low interval mud: C2 + E2 (major third at MIDI 36, 40 -> below limit 46)
        # Plus vertical rub: C4 vs Db4 sustained together
        bass = song.track("bass", "osc_sine")
        bass.seq("C2 - - -", step=0.5)
        pad1 = song.track("pad1", "osc_sine")
        pad1.seq("E2+C4 - - -", step=0.5)
        pad2 = song.track("pad2", "osc_sine")
        pad2.seq("Db4 - - -", step=0.5)

        rep = review_song(song, harmony=[(0.0, "Cmaj7")])
        self.assertGreater(len(rep["low_intervals"]), 0)
        self.assertGreater(len(rep["vertical_rubs"]), 0)
        self.assertGreater(len(rep["outside_chord"]), 0)
        text = format_review(rep)
        self.assertIn("low_intervals", text)

    def test_analysis_measures_k_lufs_bands_slope_and_stems(self):
        from engine.analysis import analyze_song_mix, analyze_wav

        song = Song("MixQA", bpm=120, room=0.2)
        bass = song.track("bass", "osc_sine", volume=0.7, pan=-0.2)
        bass.seq("C2 - G2 -", step=0.5)
        lead = song.track("lead", "osc_sine", volume=0.9, pan=0.2)
        lead.seq("C5 E5 G5 E5", step=0.5)

        wav_path = os.path.join(self.tmp, "mix.wav")
        stems_dir = os.path.join(self.tmp, "multi_track")
        song.render(wav_path)
        song.export_stems(stems_dir, keep_pan=False)

        qa = analyze_wav(wav_path, reference_genre="pop")
        self.assertIn("k_weighted_lufs", qa)
        self.assertIn("bands_pct", qa)
        self.assertAlmostEqual(sum(qa["bands_pct"].values()), 100.0, delta=1.5)
        self.assertIn("spectral_slope_db_per_oct", qa)
        self.assertIn("mono_fold_delta_db", qa)
        self.assertLess(qa["peak"], 1.0)

        full_qa = analyze_song_mix(wav_path, stems_dir=stems_dir, lead_stem="lead")
        self.assertIn("lead_minus_accompaniment_db", full_qa)
        self.assertTrue(full_qa["all_stems_centered"])


if __name__ == "__main__":
    unittest.main()
