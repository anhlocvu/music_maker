# music_maker

Plugin Antigravity chuyên sáng tác **nhạc hòa tấu không lời (instrumental)** và **nhạc beat** sử dụng SoundFont (`.sf2`) và Python toolkit.

## Cấu trúc Plugin (`music_maker_plugin/`)

```text
music_maker_plugin/
├── plugin.json                        # Manifest Antigravity plugin (v1.2.0)
├── THIRD_PARTY.md                     # Ghi nhận giấy phép & bản quyền bên thứ ba
├── assets/logo.svg                    # Logo plugin
├── rules/
│   └── AGENTS.md                      # Quy tắc kích hoạt, học MIDI, pedal, xuất multi_track
├── skills/
│   ├── soundfont-music/               # Skill chính (SoundFont engine, voicing, expression, patterns, review, analysis, render, stems)
│   ├── producer-mindset-workflow/     # Executive producer, Making Music, PWYM, Song Planner protocol, 12-word seed, moods
│   ├── genre-style-encyclopedia/      # Blueprint 23+ thể loại, 7-Axis Style Maps & 10 craft playbooks
│   ├── music-theory-harmony/          # Hòa âm, thang âm, Pop/Jazz schemas, climax/melody, 12-TET YAML
│   ├── groove-rhythm-drums/           # Trống, pocket, 729 mẫu trống 16-step, Groove MIDI stats, khóa Kick-Bass
│   ├── orchestration-arrangement/     # Dàn nhạc (Rimsky-Korsakov), 5 layers, low-interval hygiene, piano/organ idioms
│   └── mixing-timbre-mastering/       # Timbre oppositions, Sound-Box 3D, spectral slope baselines & NumPy WAV QA
├── agents/                            # 4 specialist agents: executive-producer, composer-theorist, groove-arranger, soundfont-mix-engineer
└── midi/                              # Kho MIDI tham khảo & project multi-track MIDI của tác giả
```

## Tính năng chính

1. **Điều phối đồng bộ**: `soundfont-music` là skill chính; khi kích hoạt plugin sẽ tự động nạp cùng toàn bộ các skill và agent chuyên môn khác trong plugin.
2. **Học kho project MIDI (`analyze_midi.py`)**: Trước khi sáng tác/phối khí, script quét toàn bộ các **thư mục project MIDI** trong `music_maker_plugin/midi/` (ví dụ `ballad beat/`), phân tích từng file track (`drum.mid`, `bass.mid`, `piano.mid`...) và xuất kèm **toàn bộ nội dung `readme.md`** của từng project để AI nắm đúng phong cách, BPM và ý đồ phối khí.
3. **Pedal (Sustain CC 64) & Rải nhạc cụ**: Hỗ trợ `track.pedal()`, `track.pedal_steps()`, `track.strum()` và `track.arpeggio()` cho âm thanh piano/guitar/harp giàu độ vang và tự nhiên.
4. **Xuất Multi-track Audio (`multi_track/`)**: `render.py` tự động xuất bản mix tổng, file `.mid` và thư mục `out/<song>/multi_track/` chứa từng track `.wav` căn chuẩn beat 0 — giữ nguyên hiệu ứng nhạc cụ (reverb, vibrato, release, bends) và đưa pan về giữa (`pan=0`) để tiện mix trong DAW.

## Cài đặt / Sử dụng

- **Cài đặt toàn cục cho mọi dự án (khuyến nghị)**: Chạy file [install.bat](install.bat) (sử dụng Antigravity CLI `agy plugin install` để cài plugin toàn cục và cài đặt các thư viện Python trong [requirements.txt](requirements.txt)).
- **Dùng riêng theo workspace**: Workspace này đã khai báo plugin qua [.agents/plugins.json](.agents/plugins.json).
- **Thư viện Python cần thiết** (`requirements.txt`): `numpy`, `scipy`, `mido` (`pip install -r requirements.txt`).
