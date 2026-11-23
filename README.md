# music_maker

Plugin Antigravity chuyên sáng tác **nhạc hòa tấu không lời (instrumental)** và **nhạc beat** sử dụng SoundFont (`.sf2`) và Python toolkit.

## Cấu trúc Plugin (`music_maker_plugin/` — v1.7.0)

```text
music_maker_plugin/
├── plugin.json                        # Manifest Antigravity plugin (v1.7.0)
├── THIRD_PARTY.md                     # Ghi nhận giấy phép & bản quyền bên thứ ba
├── assets/logo.svg                    # Logo plugin
├── rules/
│   └── AGENTS.md                      # Quy tắc kích hoạt đồng bộ, học MIDI, pedal, xuất multi_track
├── skills/
│   ├── soundfont-music/               # Skill chính (SoundFont 2.04 engine, MPE export, engine.harmony NRT/Negative/Coltrane/BarryHarris/US, engine.voicing Drop/Quartal/SoWhat, review register_clumps, multi_track)
│   ├── melody-harmonization/          # Dựng hòa âm từ giai điệu có sẵn & thiết kế vòng hợp âm (Melodic Skeletons, Beat Strength, ~2s Harmonic Rhythm, Harmonic-Bass Divorce, Fragile/Emergent Tonics, AccoMontage2 3-level scoring, hệ thống Ted Greene & OMT2 Jazz/Pop voice leading)
│   ├── guitar-bass-expression/        # Biểu cảm guitar/bass (12 BendTypes, nfx/bfx, fretboard playability, tunings/capo, per-string MIDI/MPE)
│   ├── producer-mindset-workflow/     # Executive producer, Making Music, PWYM, Song Planner protocol, 12-word seed, moods
│   ├── genre-style-encyclopedia/      # Blueprint 23+ thể loại, 7-Axis Style Maps & 10 craft playbooks
│   ├── music-theory-harmony/          # Hòa âm cơ bản đến cực kỳ nâng cao: Neo-Riemannian PLR/SLIDE/Hexatonic, Negative Harmony (CRT Z3xZ4), Lendvai Axis, Film CMCR, LCC, Upper Structures, Gospel polychords, Barry Harris 6th-Dim, Coltrane cycles & climax craft
│   ├── counterpoint-fugue-and-post-tonal/ # Đối âm Species 1-5 & đối âm khả đảo (8ve/10th/12th), Canon, Fugue, PC-Set (29/224), Total Voice Leading (IFUNC), 12-Tone Serialism, Spectral melody & nhịp Schillinger r(a:b)
│   ├── instrumental-soloing-improvisation/ # Solo nâng cao & ứng tác (guide tones, Harmonic Bricks, enclosures, 4-note cells, bebop, nhịp điệu Parker & Golden Mean 0.618)
│   ├── groove-rhythm-drums/           # Trống nâng cao (4-limb MIDI realism, Doubling Up, Afro-Cuban, SF2 Bank 128 velRange/choke, 10-kit GM/GS map, 729 mẫu trống & Groove MIDI stats)
│   ├── orchestration-arrangement/     # Phối khí cổ điển (Piston 7 Textures, Rimsky-Korsakov, Berlioz/Strauss/Forsyth/Widor), ACTOR perceptual timbre grouping, Davies studio scoring, Big Band (4-Way Close, 5 approach, Drop-2/2+4, Cascades, Spread Pads) & 5 lớp chức năng
│   └── mixing-timbre-mastering/       # Timbre oppositions, Sound-Box 3D, spectral slope baselines & NumPy/GTR-CTRL QA
├── agents/                            # 5 specialist agents: executive-producer, composer-theorist, orchestral-bigband-arranger, groove-arranger, soundfont-mix-engineer
├── midi_map.md                        # Bản đồ MIDI tĩnh (sinh bởi tools/generate_midi_map.py) để AI tra âm thầm
└── midi/                              # Kho MIDI tham khảo & project multi-track MIDI của tác giả
```

## Tính năng chính

1. **Điều phối đồng bộ**: `soundfont-music` là skill chính; khi kích hoạt plugin sẽ tự động nạp cùng toàn bộ 11 skill và 5 agent chuyên môn khác trong plugin.
2. **Song hành Ưu tiên Hàng đầu (`Docs ‖ midi_map.md`)**: Script `tools/generate_midi_map.py` quét kho `music_maker_plugin/midi/` và xuất ra file tĩnh `music_maker_plugin/midi_map.md` (có mục lục + dải dòng + toàn bộ nốt, velocity, Pedal CC64, Pitch Bend và `readme.md` của từng project). AI luôn đọc **song song** tài liệu chuyên gia trong các skills/agents cùng với `midi_map.md` (cả hai cùng là ưu tiên #1) như kiến thức âm nhạc nội tại, kế thừa 100% phong cách một cách âm thầm.
3. **Giao tiếp Thuần Âm nhạc & Chủ động Chuyển đoạn / Báo trống**: AI giao tiếp hoàn toàn bằng ngôn ngữ nhà sản xuất âm nhạc (không nhắc đến mã nguồn/Python với người dùng cuối), đồng thời chủ động sáng tạo chuyển đoạn, báo trống (fills/pickups) và độ gối mượt mà nối kết cấu trúc bài nhạc.
4. **Toolkit Hòa âm & Phối khí Nâng cao (`v1.5.0+`)**: Tích hợp sẵn đa hợp âm (`D|C7`), biến đổi `plr_transform`, `negative_harmony_pcs`, `coltrane_cycle`, `barry_harris_scale`, `upper_structure_triad`, các thế xếp `drop2`/`drop3`/`drop24`/`quartal_stack`/`so_what_voicing`, và chẩn đoán `register_clumps` trong `review_song.py`.
5. **Pedal (Sustain CC 64) & Rải nhạc cụ**: Hỗ trợ `track.pedal()`, `track.pedal_steps()`, `track.strum()` và `track.arpeggio()` cho âm thanh piano/guitar/harp giàu độ vang và tự nhiên.
6. **Xuất Multi-track Audio (`multi_track/`)**: `render.py` tự động xuất bản mix tổng, file `.mid` và thư mục `out/<song>/multi_track/` chứa từng track `.wav` căn chuẩn beat 0 — giữ nguyên hiệu ứng nhạc cụ (reverb, vibrato, release, bends) và đưa pan về giữa (`pan=0`) để tiện mix trong DAW.

## Cài đặt / Sử dụng

- **Cài đặt toàn cục cho mọi dự án (khuyến nghị)**: Chạy file [install.bat](install.bat) (sử dụng Antigravity CLI `agy plugin install` để cài plugin toàn cục và cài đặt các thư viện Python trong [requirements.txt](requirements.txt)).
- **Cập nhật Bản đồ MIDI sau khi thêm project vào `midi/`**: Chạy `tools/generate_midi_map.bat` (hoặc `python tools/generate_midi_map.py`) để tái tạo `music_maker_plugin/midi_map.md`.
- **Dùng riêng theo workspace**: Workspace này đã khai báo plugin qua [.agents/plugins.json](.agents/plugins.json).
- **Thư viện Python cần thiết** (`requirements.txt`): `numpy`, `scipy`, `mido` (`pip install -r requirements.txt`).
