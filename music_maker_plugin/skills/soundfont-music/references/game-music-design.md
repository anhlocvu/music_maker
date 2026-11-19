# Game music design

## Emotion -> musical choices
Research on music and emotion (valence = pleasant/unpleasant, arousal = calm/excited):
- **Mode** - major reads as positive/serene, minor as negative; minor also raises
  reported arousal. Modes in between colour it (see music-theory.md).
- **Tempo** - faster raises arousal and tension; slow reads as calmer or sadder.
  For non-musicians tempo can outweigh mode (a fast minor tune can still feel fun).
- **Dissonance / roughness** - reads as negative, tense, unsettled; consonance as calm.
- **Texture and register** - more layers and higher density = more intensity; sparse,
  low or dry = intimate or ominous.

| target feeling | starting point |
|---|---|
| cozy town | major, 90-105 BPM, piano + glockenspiel + pizzicato, brushes |
| sad / memory | minor, 60-75 BPM, 3/4, music box, slow strings, lots of reverb |
| battle | minor, 140-190 BPM, driving 8th/16th bass, square/saw or guitar lead, punchy kit, fills every 8 bars |
| boss | battle + chromatic runs, key shifts, diminished and tritone-sub chords, a breakdown section |
| shop / playful | swing, jazzy ii-V-I, electric piano, walking bass, jazz kit |
| graceful / elegant | 80-90 BPM, flutes, strings, light percussion, long vibrato notes |
| mysterious | modal or pentatonic, sparse, pedal tones, dissonant colour notes |
| heroic / adventurous | major with bVII (mixolydian), brass, rising melodies |
| dreamy / magical | lydian, celesta, harp, pads, slow harmonic rhythm |

## Structure for games
- **Loops**: an 8-32 bar loop after a short intro that plays once. The last bar must
  lead back into the first; no final hit. Deliver intro + loop, or one file with loop points.
- **Encounter / alert themes**: a 1-2 bar sting, then a short loop that holds tension
  until the fight starts; variants for different characters can share a motif and differ
  in key, tempo and instrumentation.
- **Adaptive music**: *vertical layering* - stems of identical length that the game
  mutes/unmutes (add percussion when danger rises, strip layers in quiet moments);
  *horizontal resequencing* - switch between sections at musical boundaries.
  Write sections as separate, same-length blocks so both are possible.
- **Fighting fatigue**: players hear loops many times. Vary layers each pass, keep the
  loop long enough, give sections contrast (a B section, a breakdown).

## Leitmotifs
A short, recognizable idea (melody, rhythm, chord move or a distinctive timbre) tied to a
character or place. Keep it flexible: reprise it sad on solo piano, triumphant on full
band, faster in the battle version. Two or three motifs can tie a whole soundtrack
together. A signature can be structural too - e.g. a bass that always slides into each
chord from a half step away makes a family of themes sound related.

## Arranging techniques that worked in practice
- **Guitar bends + delayed vibrato** on held notes make leads expressive; a harmony
  guitar a diatonic third below with a slightly different vibrato rate.
- **Stacked chromatic runs and a whole-band glide** as an intro gesture.
- **bVII** for the "adventure" sound; **i-bVI-bVII-V** for minor battles;
  **line cliché** for motion over a held chord.
- **Anime/J-pop harmony**: royal road IVmaj7-V7-iii7-vi7, IVmaj7-III7-vi7, tritone sub bII7.
- **Release-cut piano** (release ~0.02 s, dry) for punchy breakdowns; syncopated chord
  stabs that jump between low/mid/high registers; stabs that slide in from a half step above.
- **Neoclassical pedal-tone riffs**: a line descends through harmonic minor while a high
  pedal note strikes between every note; end with a chromatic run.
- **Syncopated bass**: 3+3+2 16ths, chromatic approach from a half step below the next
  root, next root anticipated on the last 16th.
- **Tempo-synced autopan** on arps (period 2-4 beats); keep hats static if they clutter.
- **Detuned layers** (a preset shifted by some cents or semitones) add character; write
  the notes the opposite way so they stay in key.
- **Japanese colour**: koto, shakuhachi/flute with slow wide vibrato and bend-ins,
  kotsuzumi/ohkawa hand drums, shakers, hyoshigi clappers with an accelerating roll.

## Sources
- Adaptive music: https://en.wikipedia.org/wiki/Adaptive_music ,
  https://blog.blips.fm/articles/adaptive-music-in-video-games-what-it-is-and-how-it-works
- Mode/tempo/emotion: https://onlinelibrary.wiley.com/doi/full/10.1002/ijop.12922 ,
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7054459/ ,
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4971092/
- Leitmotifs / RPG scoring: https://gamingcomposer.com/music-in-srpgs-the-musical-strategy-behind-tactical-rpg-soundtracks/ ,
  https://www.gamedeveloper.com/audio/getting-making-game-music-that-fits-classic-genre-series-boss-music
