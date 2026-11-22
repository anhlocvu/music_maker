# General MIDI & Roland GS Percussion Map (MIDI Notes 27-88)

Complete 62-note drum/percussion mapping across Bank 128 (Channel 10, or Bank 120 GS layers) for all 10 GS drum kit archetypes.
> **Octave Naming Convention Note**: The note names in column 2 follow GeneralUser GS / Yamaha **`C3 = 60`** notation (so `KickDrum1` = MIDI `36` displays as `C1`). In `soundfont-music`'s Python toolkit (`engine/song.py`, Scientific Pitch Notation **`C4 = 60`**), add `+1` octave to spelled note names (`C2` = MIDI `36`), use direct numeric MIDI keys `27..88`, or use drum tokens (`"kick"`, `"snare"`, `"hat"`, `"ohat"`, `"phat"`, etc.).
Verify target kit capabilities (e.g., Brush kit swaps snare notes 38/39/40 while keeping stick cymbals; Orchestral kit moves hi-hats to 27-30 and maps Timpani across 41-53) before writing drum steps.

| MIDI # | Note & Standard 1-3 | Room (PC 8) | Power (PC 16) | Electronic (PC 24) | 808/909 (PC 25) | Dance (PC 26) | Jazz (PC 32) | Brush (PC 40) | Orchestra (PC 48) | SFX (PC 56) |
|---:|---|---|---|---|---|---|---|---|---|---|
| 27 | D#0 HighQ | HighQ | HighQ | HighQ | HighQ | HighQ | HighQ | HighQ | Closed Hi-Hat | - |
| 28 | E0 Slap | Slap | Slap | Slap | Slap | Slap | Slap | Slap | Pedal Hi-Hat | - |
| 29 | F0 ScratchPush | ScratchPush | ScratchPush | ScratchPush | ScratchPush | ScratchPush | ScratchPush | ScratchPush | Open Hi-Hat | - |
| 30 | F#0 ScratchPull | ScratchPull | ScratchPull | ScratchPull | ScratchPull | ScratchPull | ScratchPull | ScratchPull | RideCymbal | - |
| 31 | G0 Sticks | Sticks | Sticks | Sticks | Sticks | Sticks | Sticks | Sticks | Sticks | - |
| 32 | G#0 SquareClick | SquareClick | SquareClick | SquareClick | SquareClick | SquareClick | SquareClick | SquareClick | SquareClick | - |
| 33 | A0 MetronomeClick | MetronomeClick | MetronomeClick | MetronomeClick | MetronomeClick | MetronomeClick | MetronomeClick | MetronomeClick | MetronomeClick | - |
| 34 | A#0 MetronomeBell | MetronomeBell | MetronomeBell | MetronomeBell | MetronomeBell | MetronomeBell | MetronomeBell | MetronomeBell | MetronomeBell | - |
| 35 | B0 KickDrum2 | KickDrum2 | PowerKick2 | KickDrum2 | 808BassDrum | KickDrum2 | KickDrum2 | KickDrum2 | KickDrum2 | - |
| 36 | C1 KickDrum1 | RoomKick | PowerKick1 | ElecBD | 909BassDrum | DanceKick | JazzKick | JazzKick | ConcertBD1 | - |
| 37 | C#1 SideStick | SideStick | SideStick | SideStick | 808RimShot | SideStick | SideStick | SideStick | SideStick | - |
| 38 | D1 SnareDrum1 | RoomSnare1 | PowerSnare1 | ElecSD | 808SnareDrum | DanceSnare | JazzSnare | BrushTap | ConcertSD | - |
| 39 | D#1 HandClap | HandClap | HandClap | ElecHandClap | 909HandClap | ElecHandClap | HandClap | BrushSlap | Castanets | HighQ |
| 40 | E1 SnareDrum2 | RoomSnare2 | PowerSnare2 | GatedSD | 909SnareDrum | 909SnareDrum | BrushedSnare | BrushSwirl | ConcertSD | Slap |
| 41 | F1 LowTom2 | RoomLowTom2 | RoomLowTom2 | ElecLowTom2 | 808LowTom2 | ElecLowTom2 | LowTom2 | BrushLowTom2 | TimpaniF | ScratchPush |
| 42 | F#1 Closed Hi-Hat | RoomClosedHat | PowerClosedHat | ElecClosedHat | 808ClosedHat | ElecClosedHat | Closed Hi-Hat | Closed Hi-Hat | TimpaniF# | ScratchPull |
| 43 | G1 LowTom1 | RoomLowTom1 | RoomLowTom1 | ElecLowTom1 | 808LowTom1 | ElecLowTom1 | LowTom1 | BrushLowTom1 | TimpaniG | Sticks |
| 44 | G#1 Pedal Hi-Hat | RoomPedalHat | PowerPedalHat | ElecPedalHat | 808ClosedHat | ElecPedalHat | Pedal Hi-Hat | Pedal Hi-Hat | TimpaniG# | SquareClick |
| 45 | A1 MidTom2 | RoomMidTom2 | RoomMidTom2 | ElecMidTom2 | 808MidTom2 | ElecMidTom2 | MidTom2 | BrushMidTom2 | TimpaniA | MetronomeClick |
| 46 | A#1 Open Hi-Hat | RoomOpenHat | PowerOpenHat | ElecOpenHat | 808OpenHat | ElecOpenHat | Open Hi-Hat | Open Hi-Hat | TimpaniA# | MetronomeBell |
| 47 | B1 MidTom1 | RoomMidTom1 | RoomMidTom1 | ElecMidTom1 | 808MidTom1 | ElecMidTom1 | MidTom1 | BrushMidTom1 | TimpaniB | GuitarSlidingFinger |
| 48 | C2 HighTom2 | RoomHiTom2 | RoomHiTom2 | ElecHiTom2 | 808HiTom2 | ElecHiTom2 | HighTom2 | BrushHighTom2 | Timpanic | GuitarCutNoiseDown |
| 49 | C#2 CrashCymbal1 | CrashCymbal1 | CrashCymbal1 | CrashCymbal1 | 808Crash1 | CrashCymbal1 | CrashCymbal1 | CrashCymbal1 | Timpanic# | GuitarCutNoiseUp |
| 50 | D2 HighTom1 | RoomHiTom1 | RoomHiTom1 | ElecHiTom1 | 808HiTom1 | ElecHighTom1 | HighTom1 | BrushHighTom1 | Timpanid | DoubleBassStringSlap |
| 51 | D#2 RideCymbal1 | RideCymbal1 | RideCymbal1 | RideCymbal1 | 808RideCymbal | RideCymbal1 | RideCymbal1 | RideCymbal1 | Timpanid# | FluteKeyclick |
| 52 | E2 ChineseCymbal | ChineseCymbal | ChineseCymbal | ReverseCymbal | ChineseCymbal | ChineseCymbal | ChineseCymbal | ChineseCymbal | Timpanie | Laughing |
| 53 | F2 RideBell | RideBell | RideBell | RideBell | RideBell | RideBell | RideBell | RideBell | Timpanif | Screaming |
| 54 | F#2 Tambourine | Tambourine | Tambourine | Tambourine | Tambourine | Tambourine | Tambourine | Tambourine | Tambourine | Punch |
| 55 | G2 SplashCymbal | SplashCymbal | SplashCymbal | SplashCymbal | SplashCymbal | SplashCymbal | SplashCymbal | SplashCymbal | SplashCymbal | HeartBeat |
| 56 | G#2 Cowbell | Cowbell | Cowbell | Cowbell | 808Cowbell | Cowbell | Cowbell | Cowbell | Cowbell | Footsteps1 |
| 57 | A2 CrashCymbal2 | CrashCymbal2 | CrashCymbal2 | CrashCymbal2 | 808Crash2 | CrashCymbal2 | CrashCymbal2 | CrashCymbal2 | ConcertCymbal2 | Footsteps2 |
| 58 | A#2 Vibra-slap | Vibra-slap | Vibra-slap | Vibra-slap | Vibra-slap | Vibra-slap | Vibra-slap | Vibra-slap | Vibra-slap | Applause |
| 59 | B2 RideCymbal2 | RideCymbal2 | RideCymbal2 | RideCymbal2 | RideCymbal2 | RideCymbal2 | RideCymbal2 | RideCymbal2 | ConcertCymbal1 | DoorCreaking |
| 60 | C3 HighBongo | HighBongo | HighBongo | HighBongo | HighBongo | HighBongo | HighBongo | HighBongo | HighBongo | Door |
| 61 | C#3 LowBongo | LowBongo | LowBongo | LowBongo | LowBongo | LowBongo | LowBongo | LowBongo | LowBongo | Scratch |
| 62 | D3 MuteHighConga | MuteHighConga | MuteHighConga | MuteHighConga | 808HighConga | MuteHighConga | MuteHighConga | MuteHighConga | MuteHighConga | Windchime |
| 63 | D#3 OpenHighConga | OpenHighConga | OpenHighConga | OpenHighConga | 808MidConga | OpenHighConga | OpenHighConga | OpenHighConga | OpenHighConga | Car-Engine |
| 64 | E3 LowConga | LowConga | LowConga | LowConga | 808LowConga | LowConga | LowConga | LowConga | LowConga | Car-Stop |
| 65 | F3 HighTimbale | HighTimbale | HighTimbale | HighTimbale | HighTimbale | HighTimbale | HighTimbale | HighTimbale | HighTimbale | Car-Pass |
| 66 | F#3 LowTimbale | LowTimbale | LowTimbale | LowTimbale | LowTimbale | LowTimbale | LowTimbale | LowTimbale | LowTimbale | Car-Crash |
| 67 | G3 HighAgogo | HighAgogo | HighAgogo | HighAgogo | HighAgogo | HighAgogo | HighAgogo | HighAgogo | HighAgogo | Siren |
| 68 | G#3 LowAgogo | LowAgogo | LowAgogo | LowAgogo | LowAgogo | LowAgogo | LowAgogo | LowAgogo | LowAgogo | Train |
| 69 | A3 Cabasa | Cabasa | Cabasa | Cabasa | Cabasa | Cabasa | Cabasa | Cabasa | Cabasa | Jetplane |
| 70 | A#3 Maracas | Maracas | Maracas | Maracas | Maracas | Maracas | Maracas | Maracas | Maracas | Helicopter |
| 71 | B3 ShortHiWhistle | ShortHiWhistle | ShortHiWhistle | ShortHiWhistle | ShortHiWhistle | ShortHiWhistle | ShortHiWhistle | ShortHiWhistle | ShortHiWhistle | Starship |
| 72 | C4 LongLowWhistle | LongLowWhistle | LongLowWhistle | LongLowWhistle | LongLowWhistle | LongLowWhistle | LongLowWhistle | LongLowWhistle | LongLowWhistle | GunShot |
| 73 | C#4 ShortGuiro | ShortGuiro | ShortGuiro | ShortGuiro | ShortGuiro | ShortGuiro | ShortGuiro | ShortGuiro | ShortGuiro | MachineGun |
| 74 | D4 LongGuiro | LongGuiro | LongGuiro | LongGuiro | LongGuiro | LongGuiro | LongGuiro | LongGuiro | LongGuiro | Lasergun |
| 75 | D#4 Claves | Claves | Claves | Claves | Claves | Claves | Claves | Claves | Claves | Explosion |
| 76 | E4 HighWoodBlock | HighWoodBlock | HighWoodBlock | HighWoodBlock | HighWoodBlock | HighWoodBlock | HighWoodBlock | HighWoodBlock | HighWoodBlock | Dog |
| 77 | F4 LowWoodBlock | LowWoodBlock | LowWoodBlock | LowWoodBlock | LowWoodBlock | LowWoodBlock | LowWoodBlock | LowWoodBlock | LowWoodBlock | Horse-Gallop |
| 78 | F#4 MuteCuica | MuteCuica | MuteCuica | MuteCuica | MuteCuica | MuteCuica | MuteCuica | MuteCuica | MuteCuica | Birds |
| 79 | G4 OpenCuica | OpenCuica | OpenCuica | OpenCuica | OpenCuica | OpenCuica | OpenCuica | OpenCuica | OpenCuica | Rain |
| 80 | G#4 MuteTriangle | MuteTriangle | MuteTriangle | MuteTriangle | MuteTriangle | MuteTriangle | MuteTriangle | MuteTriangle | MuteTriangle | Thunder |
| 81 | A4 OpenTriangle | OpenTriangle | OpenTriangle | OpenTriangle | OpenTriangle | OpenTriangle | OpenTriangle | OpenTriangle | OpenTriangle | Wind |
| 82 | A#4 Shaker | Shaker | Shaker | Shaker | Shaker | Shaker | Shaker | Shaker | Shaker | Seashore |
| 83 | B4 JingleBell | JingleBell | JingleBell | JingleBell | JingleBell | JingleBell | JingleBell | JingleBell | JingleBell | Stream |
| 84 | C5 Belltree | Belltree | Belltree | Belltree | Belltree | Belltree | Belltree | Belltree | Belltree | Bubble |
| 85 | C#5 Castanets | Castanets | Castanets | Castanets | Castanets | Castanets | Castanets | Castanets | Castanets | - |
| 86 | D5 MuteSurdo | MuteSurdo | MuteSurdo | MuteSurdo | MuteSurdo | MuteSurdo | MuteSurdo | MuteSurdo | MuteSurdo | - |
| 87 | D#5 OpenSurdo | OpenSurdo | OpenSurdo | OpenSurdo | OpenSurdo | OpenSurdo | OpenSurdo | OpenSurdo | OpenSurdo | - |
| 88 | E5 - | - | - | - | - | - | - | - | Applause | - |
