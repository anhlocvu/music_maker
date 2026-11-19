# music_maker

Plugin Antigravity chuyên sáng tác **nhạc hòa tấu không lời (instrumental)** và **nhạc beat** sử dụng SoundFont (`.sf2`) và Python toolkit.

## Cấu trúc Plugin (`music_maker_plugin/`)

```text
music_maker_plugin/
├── plugin.json                        # Manifest Antigravity plugin (v1.1.0)
├── assets/logo.svg                    # Logo plugin
├── rules/
│   └── AGENTS.md                      # Quy tắc kích hoạt, học MIDI, pedal, xuất multi_track
├── skills/
│   ├── soundfont-music/               # Skill chính (Python SoundFont engine, render, stems, analyze_midi)
│   ├── producer-mindset-workflow/     # Executive producer mindset, 74 chiến lược Making Music, PWYM listening
│   ├── genre-style-encyclopedia/      # Blueprint 23+ thể loại toàn cầu & ngôn ngữ âm nhạc
│   ├── music-theory-harmony/          # Hòa âm, thang âm, Pop/Jazz schemas, voice leading, motif, 12-TET YAML
│   ├── groove-rhythm-drums/           # Trống, pocket, humanize, ghost notes, 3+3+2, khóa Kick-Bass
│   ├── orchestration-arrangement/     # Dàn nhạc (Rimsky-Korsakov), 5 layers, register, pedal/strum, form
│   └── mixing-timbre-mastering/       # Timbre oppositions, Sound-Box 3D, mix balance, DSP & NumPy WAV QA
├── agents/                            # 4 specialist agents: executive-producer, composer-theorist, groove-arranger, soundfont-mix-engineer
└── midi/                              # Kho MIDI tham khảo & project multi-track MIDI của tác giả
```

## Tính năng chính

1. **Điều phối đồng bộ**: `soundfont-music` là skill chính; khi kích hoạt plugin sẽ tự động nạp cùng toàn bộ các skill và agent chuyên môn khác trong plugin.
2. **Học kho MIDI (`analyze_midi.py`)**: Quét toàn bộ file `.mid` đơn lẻ và các thư mục project multi-track MIDI trong `music_maker_plugin/midi/`, giữ nguyên tên file gốc (`drum.mid`, `bass.mid`, `piano.mid`...) để AI hiểu vai trò từng nhạc cụ và học phong cách đánh/phối.
3. **Pedal (Sustain CC 64) & Rải nhạc cụ**: Hỗ trợ `track.pedal()`, `track.pedal_steps()`, `track.strum()` và `track.arpeggio()` cho âm thanh piano/guitar/harp giàu độ vang và tự nhiên.
4. **Xuất Multi-track Audio (`multi_track/`)**: `render.py` tự động xuất bản mix tổng, file `.mid` và thư mục `out/<song>/multi_track/` chứa từng track `.wav` căn chuẩn beat 0 — giữ nguyên hiệu ứng nhạc cụ (reverb, vibrato, release, bends) và đưa pan về giữa (`pan=0`) để tiện mix trong DAW.

## Cài đặt / Sử dụng

- **Cài đặt toàn cục cho mọi dự án (khuyến nghị)**: Chạy file [install.bat](install.bat) (sử dụng Antigravity CLI `agy plugin install` để cài plugin toàn cục và cài đặt các thư viện Python trong [requirements.txt](requirements.txt)).
- **Dùng riêng theo workspace**: Workspace này đã khai báo plugin qua [.agents/plugins.json](.agents/plugins.json).
- **Thư viện Python cần thiết** (`requirements.txt`): `numpy`, `scipy`, `mido` (`pip install -r requirements.txt`).
