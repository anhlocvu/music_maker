"""Copy this file (without the leading underscore) to start a new song,
then run:  python render.py <your_file_name>

Step strings, one token per step:
    C5        play a note (octave number required; C4 = middle C; sharps #, flats b)
    C4+E4+G4  chord
    -         hold the previous note one more step
    .         rest
    |         bar line (ignored, just for readability)
    C5@60     note with velocity 60 (default 100)
Drum tracks use names: kick snare hat ohat crash ride tom1..tom4 clap rim tamb cowbell ...

Track options: volume, pan (-1 left .. 1 right), reverb (send amount), transpose (semitones)
seq options:   step (beats per token, 0.5 = 8ths, 0.25 = 16ths), vel, repeat, at (start beat)
Instruments: a GM name ("piano", "strings", "drums_power" ...) from engine/instruments.py,
a (font key, bank, program) tuple, or a built-in synth ("nes_pulse25", "osc_sine" ...).
"""
from engine.song import Song
from engine import instruments

# the user's soundfonts - ask them which files to use
instruments.register_font("main", r"C:/path/to/your/GeneralMIDI.sf2")

song = Song("My Song", bpm=120, room=1.5)   # swing=0.3 for shuffle feel

song.track("lead", "piano").seq("C5 - E5 G5 | C6 - - - |", step=0.5)
song.track("bass", "fingerbass").seq("C2 - - - | C2 - - - |", step=0.5)
song.track("drums", "drums").seq("kick . hat . snare . hat . | " * 2, step=0.25)
