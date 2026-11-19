# GEMINI.md — Nhật ký phát triển dự án `music_maker`

## Phiên làm việc: 2026-11-19 — Khởi tạo Antigravity Plugin `music_maker_plugin`

### Mục tiêu
Biến `music_maker_plugin/` (hiện có skill `soundfont-music`) thành một Antigravity plugin hoàn chỉnh chuyên sáng tác **nhạc hòa tấu không lời (instrumental)** và **nhạc beat**, tích hợp quy trình học kho MIDI của tác giả, hỗ trợ sustain pedal & rải nhạc cụ, và xuất multi-track audio stems.

### Những thay đổi đã thực hiện

1. **Cấu trúc Antigravity Plugin & Đăng ký**:
   - Tạo `music_maker_plugin/plugin.json` (manifest chuẩn Antigravity).
   - Tạo `.agents/plugins.json` đăng ký `music_maker_plugin` cho workspace.
   - Tạo `music_maker_plugin/midi/README.md` và `music_maker_plugin/agents/README.md`.
   - Cập nhật `.gitattributes` (đánh dấu `*.mid`, `*.midi`, `*.wav`, `*.sf2`, `*.sf3` là `binary`) và `README.md`.

2. **Bộ Quy tắc Plugin (`music_maker_plugin/rules/AGENTS.md`)**:
   - Đặt `soundfont-music` làm skill chính; khi kích hoạt plugin sẽ luôn kích hoạt `soundfont-music` cùng toàn bộ các skill và agent chuyên môn khác trong plugin.
   - Định hướng chuyên làm nhạc hòa tấu không lời hoặc nhạc beat.
   - Bắt buộc chạy `analyze_midi.py` trên `music_maker_plugin/midi/` trước khi vào việc, giữ rõ **tên file** và **tên thư mục project** để nhận diện nhạc cụ và học tư duy đánh/fill/trống/hòa âm từ chính các file MIDI do người dùng tự đánh và phối.
   - Khuyến khích dùng sustain pedal (`t.pedal` / `t.pedal_steps`) và rải nhạc cụ (`t.strum` / `t.arpeggio`) cho các nhạc cụ cần độ vang.
   - Bắt buộc xuất thư mục `multi_track/` chứa từng file `.wav` riêng cho mọi track sau khi hoàn thiện bài nhạc (giữ nguyên hiệu ứng nhạc cụ, không giữ pan khi xuất multi-track).

3. **Nâng cấp Toolkit (`music_maker_plugin/skills/soundfont-music/`)**:
   - `scripts/toolkit/engine/song.py`:
     - Thêm `Track.pedal()`, `Track.pedal_steps()`, hỗ trợ kéo dài ngân vang khi render WAV và xuất MIDI CC 64 (`control=64`) trong `Song.export_midi()`, đồng thời hỗ trợ `render_loop()`.
     - Thêm `Track.strum()` và `Track.arpeggio()` để rải hợp âm tự nhiên.
     - Trích xuất helper `Song._render_track()` dùng chung giữa `render()` và `export_stems()`.
     - Thêm `Song.export_stems(out_dir, keep_pan=False, trim=True)` xuất từng track thành WAV căn đồng bộ từ beat 0, giữ nguyên hiệu ứng (`reverb`, `vibrato`, `release`, `bends`, `pedal`) và đưa `pan` về giữa (`0.0`).
   - `scripts/toolkit/render.py`: Tự động xuất thêm `out/<song>/multi_track/*.wav` (và hỗ trợ cờ `--stems-only`).
   - `scripts/toolkit/engine/midi_io.py` & `scripts/toolkit/analyze_midi.py`: Phân tích toàn bộ file `.mid` đơn lẻ và thư mục project multi-track MIDI trong `music_maker_plugin/midi/`, báo cáo rõ tên file, project, BPM, key ước lượng, drum pieces, bars nhiều hoạt động/fill, CC64 pedal và rolled/block chords; hỗ trợ `load_midi_into_track()`.
   - Cập nhật `SKILL.md` và `references/toolkit.md` đồng bộ với quy trình mới.

4. **Kiểm thử**:
   - Tạo `scripts/toolkit/tests/test_toolkit.py` và chạy `unittest` qua `uv run --with numpy --with scipy --with mido`: 4/4 test cases đạt (pedal + CC64, strum/arpeggio, export_stems center pan & giữ reverb, analyze_midi hiển thị đúng tên file & project folder).

### Cập nhật tiếp theo: Script cài đặt toàn cục & Danh sách thư viện Python

1. **`music_maker_plugin/plugin.json`**: Cập nhật `"name"` sang chuẩn kebab-case `"music-maker-plugin"` để vượt qua `agy plugin validate --strict` không còn cảnh báo.
2. **`requirements.txt`**: Liệt kê đầy đủ các thư viện Python ngoài chuẩn mà `soundfont-music` sử dụng (`numpy>=1.24.0`, `scipy>=1.10.0`, `mido>=1.3.0`).
3. **`install.bat`**: Script cài đặt toàn cục cho mọi dự án bằng Antigravity CLI (`agy plugin validate --strict`, `agy plugin install`, `agy plugin enable`), ưu tiên cài `requirements.txt` bằng `uv add` (tự khởi tạo `pyproject.toml` với `uv init --bare` nếu chưa có) rồi fallback sang `py`/`python` + `pip`, và cập nhật `README.md`.
