# Kho MIDI tham khảo (`midi/`)

Thư mục này chứa các file MIDI hoặc các project multi-track MIDI do tác giả (người dùng) tự đánh và tự phối.

## Cách tổ chức gợi ý

1. **File MIDI đơn (Single `.mid` / `.midi`)**:
   - Đặt trực tiếp vào `music_maker_plugin/midi/`, ví dụ: `piano_idea.mid`, `lofi_sketch.mid`.
2. **Project MIDI tách nhiều track (Multi-track MIDI project)**:
   - Tạo một thư mục con cho mỗi project và đặt từng file MIDI theo tên nhạc cụ bên trong, ví dụ:
     ```text
     music_maker_plugin/midi/
     ├── my_ballad_project/
     │   ├── drum.mid
     │   ├── bass.mid
     │   ├── piano.mid
     │   └── strings.mid
     └── chill_beat_01/
         ├── kick_snare.mid
         ├── hihat.mid
         ├── 808_bass.mid
         └── rhodes.mid
     ```
   - **Đặt tên file rõ theo nhạc cụ** (`drum.mid`, `bass.mid`, `piano.mid`, `lead.mid`, `guitar.mid`...) giúp AI nhận diện ngay vai trò từng track (ngay cả khi bên trong file MIDI chưa đổi Program Change khỏi mặc định Piano).

## Quy tắc AI đối với thư mục này
Trước khi bắt tay vào sáng tác hoặc phối khí, AI sẽ chạy `analyze_midi.py` trên toàn bộ thư mục này (hiển thị rõ tên thư mục project và tên file `.mid` gốc) để học cách đánh, cách fill, cách đi trống, hòa âm, dynamics và cách dùng pedal của tác giả.
