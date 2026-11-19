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

---

## Phiên làm việc: 2026-11-19 — Trích xuất PDF & Xây dựng 6 Expert Skills + 4 Specialist Agents (Tiếng Anh)

### Mục tiêu
Biến toàn bộ kho tài liệu thu thập trong `tai lieu/` (cả Markdown lẫn 4 file PDF chuyên sâu) cùng kiến thức DSP/audio QA thành hệ thống **6 Expert Skills tiếng Anh** và **4 Specialist Agents** cho `music_maker_plugin`, tuân thủ nghiêm ngặt quy trình `llm-prompt-optimizer` (RSCIT, CoT, anti-hallucination, prompt compression) và bám sát 100% tài liệu gốc.

### Những thay đổi đã thực hiện

1. **Trích xuất & chưng cất tài liệu PDF → Markdown (bằng `uv run --with pymupdf --with pymupdf4llm`)**:
   - `edm-timbre-ped-handout.pdf` (6 trang) → Lavengood 2020 timbre oppositions & Moore 2012 five functional layers.
   - `MakingMusic_DennisDeSantis.pdf` (293 trang, 79 mục lục) → chưng cất đầy đủ 74 chiến lược sáng tạo qua 3 giai đoạn (*Problems of Beginning*, *Problems of Progressing*, *Problems of Finishing*).
   - `principlesoforch00rims.pdf` (516 trang, Rimsky-Korsakov) → chưng cất Chương I–V (tỷ lệ cộng hưởng, pha trộn âm sắc, melody doubling, phân bố woodwind overlaying/crossing/enclosure, economy of colour).
   - `OPEN-MUSIC-THEORY-1688414869.pdf` (1297 trang, v2) → trích xuất bổ sung các chương mới: *Popular Music Schemas*, *Fragile/Absent/Emergent Tonics*, *Texture*, *Orchestration & Piano Transcription*, *Hypermeter*, *Metrical Dissonance*, *Drumbeats*.
   - Chưng cất bổ sung từ `learning-music-production-with-strudel/`, `PWYMCurriculum/`, `study-music/`, `music-theory-data/` (YAML 12-TET), và kiến thức DSP/artifact QA (`audio-dsp`, `audio-artifacts-debug`).

2. **6 Expert Skills mới (Tiếng Anh) trong `music_maker_plugin/skills/`**:
   - `music-theory-harmony/`: `SKILL.md` + 38 file tài liệu & dataset (`references/` + `assets/` gồm `omt-pop-and-neo-riemannian-schemas.md`, `de-santis-melody-and-harmony-strategies.md`, `Chords.yaml`, `Scales.yaml`, `Intervals.yaml`, `Notes.yaml`, v.v.).
   - `groove-rhythm-drums/`: `SKILL.md` + 8 file references (`strudel-beat-foundations.md`, `de-santis-beat-and-groove-strategies.md`, `omt-pop-drumbeats-and-hypermeter.md`, `groove-and-feel.md`, `rhythmic-devices.md`, `odd-meters-polyrhythm.md`, `drums-percussion.md`, `bass.md`).
   - `orchestration-arrangement/`: `SKILL.md` + 17 file references/assets (`rimsky-korsakov-orchestration.md`, `omt-orchestration-and-pop-layers.md`, `orchestration/*`, `instrument-idiom/*`, `form/*`, `assets/form-templates.md`).
   - `producer-mindset-workflow/`: `SKILL.md` + 17 file references/assets (`making-music-beginning.md`, `making-music-progressing.md`, `making-music-finishing.md`, `pwym-producer-listening-and-structure.md`, `creative-workflows/*`, `reference-track-digging.md`, `style-reference-and-copyright.md`, `assets/*`).
   - `mixing-timbre-mastering/`: `SKILL.md` + 6 file references (`edm-timbre-and-functional-layers.md`, `pwym-multitrack-and-mix-balancing.md`, `dsp-and-audio-verification.md`, `arrangement-for-mix.md`, `energy-and-dynamics.md`, `pre-production-decisions.md`).
   - `genre-style-encyclopedia/`: `SKILL.md` + 29 file references/assets (`genres/*`, `study-music-musical-languages.md`, `research/*`, `assets/trend-and-reference-matrices.md`).

3. **4 Specialist Agents & Đồng bộ Manifest/Rules**:
   - Tạo `music_maker_plugin/agents/`: `executive-producer.md`, `composer-theorist.md`, `groove-arranger.md`, `soundfont-mix-engineer.md`.
   - Thêm `music_maker_plugin/assets/logo.svg`, nâng cấp `music_maker_plugin/plugin.json` lên `1.1.0`, cập nhật `music_maker_plugin/rules/AGENTS.md`, `soundfont-music/SKILL.md` và `README.md`.

4. **Kiểm thử sau cùng**:
   - `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 7 · agents 4 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`, 0 errors, 0 warnings).
   - `unittest` (`test_toolkit.py`): **4/4 tests OK**.
