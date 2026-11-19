"""Built-in oscillators for sounds that need no soundfont: chip-style pulse waves
(6.25/12.5/25/50% duty), a stepped triangle, noise, and plain sine/triangle.
Same render() interface as sf2.Preset.
"""
import numpy as np


class Synth:
    def __init__(self, name, wave, duty=0.5, attack=0.002, decay=0.0, sustain=1.0,
                 release=0.03, gain=0.35, steps=None):
        self.name, self.wave, self.duty = name, wave, duty
        self.attack, self.decay, self.sustain, self.release = attack, decay, sustain, release
        self.gain, self.steps = gain, steps  # steps: quantize amplitude like NES 4-bit DAC

    def render(self, key, vel, dur, sr=44100, tail=None, cents=0, vibrato=None, bend=None):
        rel = self.release if tail is None else min(self.release, tail)
        n_on, n = int(dur * sr), int((dur + rel) * sr)
        freq = 440.0 * 2 ** ((key - 69 + cents / 100.0) / 12.0)
        t = np.arange(n) / sr
        if vibrato or bend:
            from .sf2 import pitch_curve
            phase = np.cumsum(freq * pitch_curve(n, sr, dur, vibrato, bend) / sr) % 1.0
        else:
            phase = (t * freq) % 1.0
        if self.wave == "pulse":
            w = np.where(phase < self.duty, 1.0, -1.0)
        elif self.wave == "triangle":
            w = 4 * np.abs(phase - 0.5) - 1
            if self.steps:  # NES triangle is a 16-step staircase
                w = np.round((w + 1) / 2 * (self.steps - 1)) / (self.steps - 1) * 2 - 1
        elif self.wave == "saw":
            w = 2 * phase - 1
        elif self.wave == "noise":
            # sample-and-hold noise; higher keys clock faster, like the NES noise channel
            rate = max(200.0, freq * 8)
            idx = (t * rate).astype(np.int64)
            rng = np.random.default_rng(key)
            w = rng.choice([-1.0, 1.0], size=idx[-1] + 1)[idx]
        else:
            w = np.sin(2 * np.pi * phase)
        env = np.full(n, self.sustain)
        a = max(1, int(self.attack * sr))
        env[:a] = np.linspace(0, 1, a)
        if self.decay > 0:
            d = np.arange(n - a) / sr
            env[a:] = self.sustain + (1 - self.sustain) * np.exp(-d / self.decay)
        if n > n_on:
            env[n_on:] = env[max(0, n_on - 1)] * np.linspace(1, 0, n - n_on)
        w = (w * env * self.gain * (vel / 127.0)).astype(np.float32)
        return np.stack([w, w], axis=1)


SYNTHS = {
    "nes_pulse6":    Synth("NES 6% Pulse", "pulse", duty=0.0625),
    "nes_pulse12":   Synth("NES 12.5% Pulse", "pulse", duty=0.125),
    "nes_pulse25":   Synth("NES 25% Pulse", "pulse", duty=0.25),
    "nes_pulse50":   Synth("NES 50% Pulse", "pulse", duty=0.5),
    "nes_triangle":  Synth("NES Triangle", "triangle", steps=16, gain=0.5),
    "nes_noise":     Synth("NES Noise", "noise", decay=0.06, sustain=0.0, gain=0.3),
    "osc_sine":      Synth("3x Osc Sine", "sine", gain=0.6),
    "osc_triangle":  Synth("3x Osc Triangle", "triangle", gain=0.45, release=0.15),
}
