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


---

## Phiên làm việc: 2026-11-20 — Cập nhật `analyze_midi.py` cho MIDI Project Folders & `readme.md`

### Mục tiêu
Chuyển kho `music_maker_plugin/midi/` sang mô hình **project MIDI** (mỗi project là một thư mục con như `ballad beat/` gồm các track `.mid` và file `readme.md` tiếng Anh mô tả phong cách/BPM/ý đồ phối khí), xóa `music_maker_plugin/midi/README.md`, và cập nhật script phân tích MIDI để quét toàn bộ các project kèm xuất nguyên văn nội dung `readme.md` của từng project đó.

### Những thay đổi đã thực hiện

1. **Dọn thư mục `music_maker_plugin/midi/`**:
   - Xóa `music_maker_plugin/midi/README.md` và thêm `.gitkeep` để giữ thư mục `midi/` trong repository.

2. **Nâng cấp `engine/midi_io.py` & `analyze_midi.py`**:
   - `music_maker_plugin/skills/soundfont-music/scripts/toolkit/engine/midi_io.py`:
     - Thêm `_find_project_readme()` (tìm `readme.md` không phân biệt hoa/thường trong từng thư mục project) và `read_project_readme()` (đọc toàn bộ văn bản UTF-8/UTF-8-SIG).
     - Cập nhật `discover_midi_sources()` để quét toàn bộ các project folder trong `midi/`, hỗ trợ cả trường hợp trỏ thẳng vào một thư mục project cụ thể.
   - `music_maker_plugin/skills/soundfont-music/scripts/toolkit/analyze_midi.py`:
     - `analyze_directory()` trả về thêm `readme_file`, `readme_path`, và toàn bộ nội dung `readme` cho từng project (có sẵn cả khi chạy `--json`).
     - `format_markdown()` hiển thị mục `### Project README (...)` ngay sau phần phân tích các file `.mid` của từng project và in toàn bộ văn bản `readme.md` bên trong code fence an toàn (`_markdown_fence()`).

3. **Đồng bộ Rules, Skills, Agent & README**:
   - Cập nhật `music_maker_plugin/rules/AGENTS.md`, `music_maker_plugin/skills/soundfont-music/SKILL.md`, `music_maker_plugin/skills/soundfont-music/references/toolkit.md`, `music_maker_plugin/agents/executive-producer.md`, và `README.md` để AI luôn chạy `analyze_midi.py` trước khi sáng tác/phối khí và đọc cả phần `readme.md` tiếng Anh của từng project MIDI.

4. **Kiểm thử sau cùng**:
   - Cập nhật `test_analyze_midi_reports_project_folders_and_full_readme` trong `music_maker_plugin/skills/soundfont-music/scripts/toolkit/tests/test_toolkit.py` và chạy `unittest`: **4/4 tests OK**.
   - Chạy `python music_maker_plugin/skills/soundfont-music/scripts/toolkit/analyze_midi.py` trên `music_maker_plugin/midi/`: hoạt động bình thường.
   - Chạy `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 7 · agents 4 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).

---

## Phiên làm việc: 2026-11-20 — Tích hợp tài nguyên `tai lieu/` & Nâng cấp Toolkit v1.2.0

### Mục tiêu
Nghiên cứu và tích hợp có chọn lọc các tài liệu, dataset và mã nguồn MIT từ `tai lieu/` (`music-skill`, `dmp_midi` / `DrumMachinePatterns`, `ableton-pocket-operations`, và `SKILL.md` `song-planner`) vào hệ thống 7 skills, 4 agents và Python toolkit của `music_maker_plugin`, đảm bảo an toàn bản quyền và giữ tương thích ngược hoàn toàn.

### Những thay đổi đã thực hiện

1. **Bổ sung tri thức & dataset vào 6 Expert Skills**:
   - `producer-mindset-workflow`: Thêm `references/song-planner-protocol.md` (No House Style, hỏi gom 1 lượt, Song Sheet có duyệt, wildcard, bảo toàn riff người dùng, chỉ mượn form), `references/moods.md`, `references/character-words.md`, và `assets/association-words.tsv` (1.000 từ gợi ý chủ đề chống rập khuôn).
   - `genre-style-encyclopedia`: Thêm hệ thống **7-Axis Style Maps** (`references/style-maps.md`, `assets/style-maps.json`, 12 file `references/style-maps/style-map-*.md`) và 10 playbooks trong `references/playbooks/` (`anime-opening.md`, `baroque.md`, `beats.md`, `electronic.md`, `film-score.md`, `game-music.md`, `jazz-and-funk.md`, `pop-and-ballad.md`, `rock-and-metal.md`, `scene-music.md`).
   - `music-theory-harmony`: Thêm `references/harmony/music-skill-harmony.md` và `references/melody/climax-and-melody.md`.
   - `groove-rhythm-drums`: Thêm `references/development-and-groove.md`, `references/building-blocks.md`, `assets/drum-statistics.json` (Groove MIDI Dataset aggregate stats, CC BY 4.0) và kho 729 mẫu trống 16-step trong `assets/drum-patterns/` (`Patterns_200.json`, `Patterns_260.json` MIT + `pocket_operations_patterns.json` của Paul Wenzel kèm `ATTRIBUTION.md`).
   - `orchestration-arrangement`: Thêm `references/orchestration/arrangement-craft.md`, `orchestral-scoring.md`, `references/instrument-idiom/piano-and-chamber.md`, `organ.md`.
   - `mixing-timbre-mastering`: Thêm `references/performance-and-mix.md`, `measuring.md`, `noise.md`, `sound-selection.md`, `electronic-sounds.md`, và `assets/tonal-references.json`.

2. **Nâng cấp `soundfont-music` Python Toolkit (`scripts/toolkit/`) theo TDD**:
   - `engine/harmony.py`: Phân tích ký hiệu hợp âm (`parse`, `chord_at`, `pitch_class`, `midi_to_name`).
   - `engine/voicing.py`: `voice_lead()` tối ưu dẫn bè bằng Quy hoạch động, `LOW_INTERVAL_LIMITS`, và `apply_voicings()`.
   - `engine/expression.py`: `humanize_track()` / `humanize_song()` (linear phase correction, $1/f^\beta$ velocity drift, phrase arches, cymbal cycles).
   - `engine/patterns.py`: `list_patterns()`, `pattern_to_steps()` (729 mẫu trống 16-step), `drum_stats_suggest()` (Groove MIDI stats).
   - `engine/review.py` & `review_song.py`: Kiểm tra tổng phổ (low-interval mud, quãng 2 thứ/9 thứ, nốt ngoài hợp âm, quãng 5/8 song song, vòng lặp tĩnh $\ge 16$ ô nhịp).
   - `engine/analysis.py` & `analyze_audio.py`: Đo lường WAV & `multi_track/` stems bằng NumPy (K-weighted LUFS, 6 dải tần, spectral slope so với `tonal-references.json`, mono fold-down, lead presence, kiểm tra stem centered pan).

3. **Đồng bộ Plugin, Bản quyền & Agents**:
   - Tạo `music_maker_plugin/THIRD_PARTY.md`, cập nhật `plugin.json` (`1.2.0`), `rules/AGENTS.md`, `agents/{executive-producer,groove-arranger,soundfont-mix-engineer}.md`, `soundfont-music/{SKILL.md,references/toolkit.md}`, và `README.md`.
   - Không đưa thành phần GPL-3.0 (`surge_host.py`) hay dữ liệu nặng không dùng (`surge-catalog.json`) vào plugin.

4. **Kiểm thử sau cùng**:
   - `unittest` (`test_toolkit.py`): **9/9 tests OK**.
   - `analyze_audio.py --help` & `py_compile review_song.py`: **OK**.
   - `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 7 · agents 4 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).
   - Sau đó đã xóa thư mục `music_maker_plugin/skills/soundfont-music/scripts/toolkit/tests/` (gồm `test_toolkit.py`) theo yêu cầu người dùng để tránh bị sao chép theo sang `music_toolkit/` khi làm nhạc; kiểm tra lại `agy plugin validate --strict music_maker_plugin` vẫn **Validation passed**.


---

## Phiên làm việc: 2026-11-20 — Kế thừa phong cách `midi/` & Xuất toàn bộ Notes/Pedal/Pitch Bend trong `analyze_midi.py`

### Mục tiêu
Cho phép và khuyến khích AI kế thừa/mô phỏng sâu phong cách phối khí của tác giả từ kho `music_maker_plugin/midi/` (cách đi hợp âm, rải hợp âm, velocity mạnh-nhẹ, sustain pedal CC64, pitch bend, groove/fill) kết hợp sáng tạo mới, đồng thời nâng cấp `analyze_midi.py` để in ra **toàn bộ nốt, toàn bộ sự kiện pedal CC64 và toàn bộ sự kiện pitch bend** thay vì chỉ tóm tắt.

### Những thay đổi đã thực hiện

1. **Nâng cấp phân tích & xuất đầy đủ sự kiện MIDI (`engine/midi_io.py`, `analyze_midi.py`)**:
   - `parse_midi_file()`: Lưu đầy đủ danh sách `pitch_bends` (`beat`, `pitch`, `semitones`, có phát hiện RPN pitch-bend sensitivity mặc định ±2 st).
   - `summarize_track()`: Bổ sung `velocity_std`, `ghost_note_ratio` (`vel < 60`), `micro_timing_avg_abs_offset_beats`, cùng danh sách đầy đủ `notes` (theo `bar`, `start_beat`, `dur_beats`, `note`, `vel`), `pedals` (`start_beat -> end_beat`), và `pitch_bends`.
   - `format_markdown()` trong `analyze_midi.py`: Xuất toàn bộ `All Pedal CC64 Events`, `All Pitch Bend Events`, và `All Notes` gom theo từng `Bar` (kèm beat 0-based `@start_beat`, thời lượng, velocity) cùng toàn văn `readme.md` của từng project.

2. **Cập nhật Quy tắc, Skills & Agents cho Author Style Adoption**:
   - `music_maker_plugin/rules/AGENTS.md`: Đổi mục 2 thành *Learn & Adopt Style from All MIDI Projects (`midi/`)*, khẳng định không áp dụng luật chống clone lên `midi/` của tác giả và khuyến khích bắt chước 6 trụ cột phong cách (hợp âm/voicing, rải hợp âm, velocity, CC64 pedal, pitch bend, trống/fill) kết hợp sáng tạo giai điệu/cấu trúc mới.
   - `music_maker_plugin/skills/soundfont-music/SKILL.md` & `references/toolkit.md`: Bổ sung ngoại lệ cho `midi/` và quy trình chuyển hóa thói quen từ `midi/` sang `strum`, `arpeggio`, `pedal`, `bends/glides`, `@vel`, `humanize_song`.
   - `music_maker_plugin/skills/producer-mindset-workflow/` (`SKILL.md`, `references/song-planner-protocol.md`, `references/style-reference-and-copyright.md`): Làm rõ luật chống đạo nhạc chỉ áp dụng cho bài hát bên ngoài; kho `midi/` là *Signature Style Anchor* hợp lệ để mô phỏng sâu.
   - `music_maker_plugin/agents/` (`executive-producer.md`, `composer-theorist.md`, `groove-arranger.md`, `soundfont-mix-engineer.md`) & `README.md`: Đồng bộ chỉ thị trích xuất và tái tạo Author Style DNA (cách đi hợp âm, rải, velocity, pedal, pitch bend).

3. **Kiểm thử sau cùng**:
   - `py_compile` (`midi_io.py`, `analyze_midi.py`): **OK**.
   - Smoke test với project MIDI tổng hợp (rolled chord, velocity mạnh/ghost, CC64 pedal, pitchwheel `+4096` / `+1.000st`, `readme.md`): **SMOKE_TEST_OK**.
   - Chạy `python analyze_midi.py` trên `music_maker_plugin/midi/` (`drum fill template1`, `my_ballad_beat`): hiển thị đầy đủ từng nốt, từng bar, thống kê human feel và `readme.md`.
   - `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 7 · agents 4 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).
