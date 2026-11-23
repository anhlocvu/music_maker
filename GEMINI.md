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

---

## Phiên làm việc: 2026-11-21 — Chiến lược Bản đồ MIDI (`tools/` → `midi_map.md`) & Tối ưu Quy tắc bằng `llm-prompt-optimizer`

### Mục tiêu
Tránh tràn ngữ cảnh khi kho `midi/` có nhiều project bằng cách tạo script sinh bản đồ tĩnh ở `/tools` xuất ra `music_maker_plugin/midi_map.md`, đồng thời áp dụng `llm-prompt-optimizer` (RSCIT, positive instructions, prompt compression) để chuyển quy trình sang tra cứu `midi_map.md` rộng, liên tục ở mọi công đoạn, mô phỏng 100% phong cách phối nhưng hoàn toàn **âm thầm & nội tại hóa** (không lộ nguồn kho MIDI với người dùng cộng đồng).

### Những thay đổi đã thực hiện

1. **Công cụ tạo Bản đồ MIDI ngoài plugin (`tools/`)**:
   - `tools/generate_midi_map.py`: Tái sử dụng `analyze_midi.py` / `engine/midi_io.py` (kèm `sys.dont_write_bytecode = True`), tính toán hai lượt (two-pass) để sinh mục lục `1. Project Index` và `2. Instrument & Track Lookup` (ưu tiên phân loại theo tên file/track trước `program_name` mặc định) với dải dòng `L<start>-L<end>` chính xác 100%, theo sau bởi toàn bộ nốt theo bar, velocity, micro-timing, CC64 pedal, pitch bend và `readme.md` của từng project.
   - `tools/generate_midi_map.bat`: Script Windows chạy nhanh bằng `uv` / `py` / `python` (hỗ trợ cờ `--no-pause`).
   - Đã chạy sinh thử `music_maker_plugin/midi_map.md` (374 dòng, gồm `drum fill template1` và `my_ballad_beat`).

2. **Tối ưu bộ Quy tắc, Skills, Agents & Tài liệu theo `llm-prompt-optimizer`**:
   - Cập nhật `music_maker_plugin/rules/AGENTS.md`: Thay bước chạy `analyze_midi.py` bằng giao thức tra `midi_map.md` 2 pha (trước khi làm việc + tra không giới hạn trong mọi công đoạn piano/drum/bass/strings/synth/guitar...), bắt buộc tra rộng nhiều project/nhạc cụ không tự bó hẹp, mô phỏng 100% phong cách và tuyệt đối tra âm thầm không nhắc tới `midi_map.md`/`midi/` với người dùng cuối.
   - Cập nhật đồng bộ `music_maker_plugin/skills/soundfont-music/SKILL.md`, `music_maker_plugin/skills/soundfont-music/references/toolkit.md`, `music_maker_plugin/skills/producer-mindset-workflow/` (`SKILL.md`, `references/song-planner-protocol.md`, `references/style-reference-and-copyright.md`), `music_maker_plugin/skills/music-theory-harmony/SKILL.md`, `music_maker_plugin/skills/groove-rhythm-drums/SKILL.md`.
   - Cập nhật 4 agents trong `music_maker_plugin/agents/` (`executive-producer.md`, `composer-theorist.md`, `groove-arranger.md`, `soundfont-mix-engineer.md`), bỏ công cụ `Bash` khỏi `executive-producer.md` và chỉnh `Return Format` sang `Internalized Performance & Arrangement DNA` để không lộ nguồn cho người dùng cuối.
   - Cập nhật `music_maker_plugin/plugin.json` (`suggestedPrompts` & `description` thân thiện cộng đồng) và `README.md`.

3. **Kiểm thử sau cùng**:
   - `uv run --with mido python -m py_compile tools/generate_midi_map.py`: **OK**.
   - `cmd /c "tools\generate_midi_map.bat --no-pause"`: Sinh thành công `music_maker_plugin/midi_map.md` (374 dòng), phân loại chuẩn xác `Drums / Percussion`, `Bass`, `Guitar / Plucked`, `Strings / Pad`, `Piano / Keys`.
   - `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 7 · agents 4 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).

---

## Phiên làm việc: 2026-11-21 — Mở xích `midi_map.md`, Nâng cấp Engine Multi-Point Pitch Bend & Tải Tài liệu `tai lieu/`

### Mục tiêu
1. Gỡ bỏ hoàn toàn các rào cản quy tắc (`No House Style`, `wildcard` bắt buộc, `Originality` gây dè chừng) đối với `music_maker_plugin/midi_map.md` để AI tự do tái sử dụng và mô phỏng 100% phong cách hòa âm, bass, trống, rải phím, CC64 pedal và kỹ thuật ben (pitch bend) của tác giả.
2. Nâng cấp Python toolkit (`sf2.py`, `song.py`, `midi_io.py`, `expression.py`) để thực sự biết "ben" đa điểm như tay người chơi thật (bend-and-release, delayed bend, pre-bend, dive/scoop, vibrato-by-bend, RPN 0,0, import pitch bend từ MIDI).
3. Giữ nguyên `analyze_midi.py`, `tools/generate_midi_map.py` và `music_maker_plugin/midi_map.md` (bỏ qua bước gom/tóm tắt pitchwheel theo yêu cầu người dùng).
4. Tải các tài liệu chuyên sâu về biểu cảm guitar/bass/MIDI/SoundFont vào `tai lieu/` và ghi chú lại để xây dựng skill riêng sau này.

### Những thay đổi đã thực hiện

1. **Mở xích 100% phong cách `midi_map.md` (Signature House Style)**:
   - `music_maker_plugin/rules/AGENTS.md`: Xác định `midi_map.md` là **Unchained Signature House Style**; cho phép tái sử dụng trực tiếp 100% vòng hợp âm, voicing, bassline, fill trống, strum/arpeggio, CC64 pedal và các đường cong pitch bend / vibrato-by-bend; đồng thời bắt buộc sử dụng bộ API bend đa điểm mới cho lead guitar, bass, strings, solo.
   - `music_maker_plugin/skills/soundfont-music/SKILL.md`: Đổi mục *Originality* thành *Signature House Style (`midi_map.md`) & External Copyright*, giới hạn luật chống sao chép chỉ cho bài hát thương mại bên ngoài.
   - `music_maker_plugin/skills/producer-mindset-workflow/` (`SKILL.md`, `references/song-planner-protocol.md`, `references/style-reference-and-copyright.md`, `references/reference-track-digging.md`, `assets/diagnostic-checklists.md`): Chuyển `No House Style` → `Signature Style First (No Generic AI Defaults)`, biến `[wildcard]` và `12-word seed` thành tùy chọn, ghi rõ ngoại lệ `midi_map.md` ở mọi checklist chống copy.
   - `music_maker_plugin/agents/` (`executive-producer.md`, `composer-theorist.md`, `groove-arranger.md`, `soundfont-mix-engineer.md`): Đồng bộ quyền tái sử dụng trực tiếp `midi_map.md` và chỉ thị thiết kế/code multi-stage pitch bend.

2. **Nâng cấp Engine Pitch Bend (`music_maker_plugin/skills/soundfont-music/scripts/toolkit/`)**:
   - `engine/sf2.py`: Thêm `build_bend_curve(...)` (8 preset: `bend_release`, `bend_hold`, `delayed_bend`, `pre_bend`, `scoop`, `dive`, `bend_vibrato`, `glide`), `_eval_bend_points(...)`, và nâng cấp `pitch_curve(...)` hỗ trợ `("norm", smooth, points)` và `("points", smooth, points)` (tương thích ngược hoàn toàn với `(semis, "bend"/"glide")`).
   - `engine/song.py`:
     - Mở rộng step-string trong `Track.seq(...)` với `D5^E5^D5` / `D5^+2^0` (bend & release) và `D5~E5` (delayed bend-release), dùng `re.split(r"\+(?=[A-Za-z])", tok)` để không cắt nhầm dấu `+` trong bán cung tương đối.
     - Thêm `Track.note(...)`, `Track.bend(...)`, `Track.bend_last(...)`, và tham số `Track(..., bend_range=2.0)`.
     - Nâng cấp `Song.export_midi(...)` & `_pitchwheel(...)`: tự tính `bend_range` hiệu dụng và phát **RPN `0, 0`** (`CC101=0, CC100=0, CC6=range, CC38=0`) khi biên độ bend vượt `±2` semitones.
   - `engine/midi_io.py`: Thêm `_attach_pitch_bends_to_notes(...)` và cập nhật `load_midi_into_track(...)` để nạp cả `pitch_bends` và `bend_range_semitones` khi import MIDI.
   - `engine/expression.py`: Xuất `make_bend_curve` và thêm `expressive_bends(track, role=..., seed=..., max_semi=..., min_dur=..., intensity=...)` tự động bổ sung bend/vibrato cho các nốt ngân dài hoặc đỉnh câu nhạc (không ghi đè nốt đã có `bend`).
   - `references/toolkit.md`: Bổ sung tài liệu API cho multi-stage pitch bend & `expressive_bends`.
   - `tools/tests/test_toolkit_bends.py`: Bộ 7 unit tests bao phủ tương thích ngược, multi-point norm/sec, step-string `^` / `~`, render WAV + export MIDI kèm RPN `0,0`, round-trip `load_midi_into_track`, và `expressive_bends`.

3. **Kho tài liệu đã tải về `tai lieu/` (để làm Skill sau)**:
   - `tai lieu/dadagp/`:
     - `DadaGP_ISMIR2021.pdf` (3.110.022 bytes) — Bài báo *DadaGP: A Dataset of Tokenized GuitarPro Songs for Sequence Models* (Sarmento et al., ISMIR 2021, arXiv:2107.14653).
     - `dadagp.py` (91.943 bytes) & `README.md` (2.022 bytes) — Mã nguồn encoder/decoder GuitarPro (`.gp3/.gp4/.gp5`) sang token, chứa chuẩn hóa chi tiết các hiệu ứng `bend`, `pre-bend`, `bend-release`, `vibrato`, `slide`, `hammer-on/pull-off`, `palm mute`.
     - `GTR_CTRL_ShredGP_2302.05393.pdf` (1.805.580 bytes) — Bài báo *ShredGP / Controllable Guitar Tablature Generation* (arXiv:2302.05393) về điều khiển phong cách & kỹ thuật chơi guitar.
     - `Fretting_Transformer_2506.14223.pdf` (1.081.775 bytes) — Bài báo *Fretting-Transformer* (arXiv:2506.14223) về chuyển đổi MIDI sang tablature và thế bấm dây.
   - `tai lieu/synthtab/`:
     - `SynthTab_2309.09085.pdf` (605.921 bytes) — Bài báo *SynthTab: Leveraging Synthesized Data for Guitar Tablature Transcription* (arXiv:2309.09085), hướng dẫn map các kỹ thuật guitar (bends, vibrato, slides) sang MIDI CC / pitch bend / keyswitch khi tổng hợp âm thanh.
   - `tai lieu/soundfont/`:
     - `sfspec24.pdf` (530.464 bytes) — Đặc tả chính thức **SoundFont 2.04 Technical Specification** (RIFF chunks, modulators, pitch wheel → pitch generator, LFO vibrato, envelope).
   - `tai lieu/midi_specs/`:
     - `MPE-final-spec-notes.md` (7.775 bytes) — Ghi chú kiến trúc đặc tả **MIDI Polyphonic Expression (MPE)** (per-note pitch bend, RPN, channel allocation).
     - `fluidsynth_devdoc.txt` (4.694 bytes) — Tài liệu lập trình kiến trúc SoundFont synth **FluidSynth v2.0**.
   - *Ghi chú nguồn bị chặn mạng khi tải*: `KTH_rule_system_2006.pdf` (Friberg, Bresin & Sundberg, *Overview of the KTH rule system for musical performance*) không tải trực tiếp được do lỗi timeout/SSL từ `diva-portal.org` và `ac-psych.org`; khi làm skill sau có thể tải tay từ ResearchGate/KTH nếu cần bổ sung quy tắc *Melodic Charge* / *Phrase Arch*.

### Kiểm thử sau cùng
- `uv run python -B -m unittest discover -s tools/tests -v`: **7/7 tests OK**.
- `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 7 · agents 4 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).

---

## Phiên làm việc: 2026-11-22 — Chưng cất `tai lieu/` vào Skill `guitar-bass-expression` & Nâng cấp Toolkit v1.3.0 (SF2 2.04, MPE 1.0, GTR-CTRL)

### Mục tiêu
Kích hoạt `llm-prompt-optimizer`, trích xuất toàn bộ 5 PDF + tài liệu spec/code trong `tai lieu/` sang Markdown để chưng cất chính xác 100% (tiếng Anh) thành skill mới và bổ sung vào các skill/agent/toolkit hiện tại, sau đó dọn sạch nội dung trong `tai lieu/`.

### Những thay đổi đã thực hiện

1. **Trích xuất & chưng cất tài liệu `tai lieu/` (`pymupdf4llm`)**:
   - `DadaGP_ISMIR2021.pdf` (8 trang) + `dadagp.py` (2.078 dòng) + `README.md` → 12 `BendType`, `BendPoint` (quartertones), đầy đủ `nfx:` / `bfx:`, tuning vectors & resolution `960 ticks/quarter`.
   - `Fretting_Transformer_2506.14223.pdf` (8 trang) → công thức độ khó bấm cần đàn (`along`/`across`/`locality`), heuristic dây buông, capo & alternate tunings.
   - `GTR_CTRL_ShredGP_2302.05393.pdf` (16 trang) → tách điều khiển nhạc cụ/genre khỏi nốt đầu & 4 chỉ số đánh giá symbolic (`PCE`, `GC`, `PIP`, `UIP`).
   - `SynthTab_2309.09085.pdf` (5 trang) → per-string MIDI isolation, micro-vibrato & picking/pickup profiles.
   - `sfspec24.pdf` (69 trang) + `fluidsynth_devdoc.txt` + `MPE-final-spec-notes.md` → SoundFont 2.04 generators/modulators/`sampleModes=3`/`exclusiveClass` và MPE 1.0 (RP35) `RPN 00 06`, Lower/Upper Zones, member channel allocation.

2. **Skill mới `music_maker_plugin/skills/guitar-bass-expression/` (Tiếng Anh, chuẩn RSCIT + CoT)**:
   - `SKILL.md`
   - `references/articulation-and-bend-taxonomy.md`
   - `references/fretboard-playability-and-tunings.md`
   - `references/per-string-synthesis-and-human-vibrato.md`

3. **Bổ sung vào các Skills, Agents, Rules & Manifest hiện tại**:
   - `soundfont-music`: thêm `references/sf2-spec-and-modulators.md`, `references/mpe-and-multi-channel.md`; cập nhật `SKILL.md` & `references/toolkit.md`.
   - `orchestration-arrangement`: cập nhật `references/instrument-idiom/guitar.md` (box 4 ngăn, quy tắc tách dây khi polyphonic bend, link sang `guitar-bass-expression`).
   - `groove-rhythm-drums`: cập nhật `references/bass.md` (palm mute, dead/ghost, slap/pop, bends/slides bass, link sang `guitar-bass-expression`).
   - `mixing-timbre-mastering`: cập nhật `references/sound-selection.md` (`Vel -> FilterFc` SF2, picking/pickup contrast) & `references/dsp-and-audio-verification.md` (pre-render symbolic QA `PCE`/`GC`/`PIP`/`UIP`).
   - Đồng bộ `music_maker_plugin/rules/AGENTS.md`, `music_maker_plugin/agents/{composer-theorist,groove-arranger,soundfont-mix-engineer}.md`, `music_maker_plugin/plugin.json` (`1.3.0`), `music_maker_plugin/THIRD_PARTY.md` và `README.md`.

4. **Nâng cấp Python Toolkit (`music_maker_plugin/skills/soundfont-music/scripts/toolkit/`) theo TDD**:
   - `engine/review.py` & `review_song.py`: thêm `symbolic_metrics()` (`PCE`, `GC`, `PIP`, `UIP`) và cờ `--prompted`.
   - `engine/sf2.py`: thêm `EXCLUSIVE_CLASS = 57` (`Preset.exclusive_class()`), `SoundFont.close()`, và hỗ trợ `sampleModes == 3` (loop khi giữ phím, phát tiếp phần đuôi đến `end` khi nhả phím).
   - `engine/song.py`: thêm `exclusiveClass` choke (có tính `swing`) trong `_render_track()` và chế độ `export_midi(..., mpe=True, mpe_bend_range=...)` (Lower Zone `RPN 00 06`, `RPN 00 00` trên member channels, cấp phát kênh động tránh nhiễu bend đa âm và giữ `ch=9` cho GM drums).
   - `tools/tests/test_toolkit_specs.py`: thêm 5 unit tests mới cho GTR-CTRL metrics, SF2 `sampleModes=3` & `exclusiveClass`, và MPE MIDI export.

5. **Kiểm thử & Dọn dẹp sau cùng**:
   - `py_compile` (`sf2.py`, `song.py`, `review.py`, `review_song.py`): **OK**.
   - `uv run --with numpy --with scipy --with mido python -B -m unittest discover -s tools/tests -v`: **12/12 tests OK**.
   - `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 8 · agents 4 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).
   - Đã xóa toàn bộ tệp và thư mục con bên trong `tai lieu/` sau khi hoàn tất chưng cất và kiểm thử.

---

## Phiên làm việc: 2026-11-22 (Phần 2) — Chưng cất 28 Tài liệu Soloing & Trống/SoundFont theo Phương án A (v1.4.0)

### Mục tiêu
Áp dụng `llm-prompt-optimizer`, chưng cất chính xác 100% (tiếng Anh, không bịa đặt) toàn bộ **28 tài liệu** đã tải trong `tai lieu/` vào `music_maker_plugin` (Phương án A đã được người dùng duyệt):
1. Tạo mới skill `instrumental-soloing-improvisation` từ **15 tài liệu** trong `tai lieu/01_hoa_am_va_solo/`.
2. Nâng cấp toàn diện skill `groove-rhythm-drums` từ **13 tài liệu** trong `tai lieu/02_soan_trong_va_soundfont/`.
3. Đồng bộ hệ sinh thái plugin (`agents/`, `rules/AGENTS.md`, `soundfont-music/SKILL.md`, `plugin.json` `1.4.0`, `THIRD_PARTY.md`, `README.md`) và rà soát qua `code-reviewer`.

### Những thay đổi đã thực hiện

1. **Skill mới `music_maker_plugin/skills/instrumental-soloing-improvisation/` (Tiếng Anh, chuẩn RSCIT + 5-step CoT + Few-Shot + Grounding)**:
   - `SKILL.md` & `references/00-navigation.md`
   - `references/chord-tone-and-guide-tone-architecture.md`: Hal Crook (90% chord-tone accuracy, 3-stage ladder), Alisdair MacRae Birch (3 harmonic approaches & Ideal Line `7th -> 3rd`), Simon Purcell (`3->7`, `5->9`, `9->13` & chromaticized `b9/#9/#11/b13`), Mark Watkins (`1 & 3` delineation), Bob Keller (avoid-note `nat4`), và Keating & Casey (ArXiv 2510.19666 shortest-path weighted DAG boundary voice leading).
   - `references/harmonic-bricks-and-advanced-scales.md`: 5 chord-scale families (Major, Dominant/Sus4, Minor, Half-Diminished, Diminished), Melodic/Harmonic Minor modes, pentatonic blanketing (`5th of I`, `2nd/4th/b5`), triad pairs (`Cm+Dm`, `Eb+F`, `Dbm+Ebm`), John Elliott *Harmonic Lego Bricks*, Rhythm Changes Sets 1–6 & Bridges 1–5, Change Running vs Blanketing, 17 Dan Haerle Blues progressions.
   - `references/approach-tones-and-enclosures.md`: Single & chromatic multiple approach tones, 2–4 note enclosures, skip/zig-zag, quartal melodies, Parker `16th-triplet + 8th` turns, avoid-note & error-recovery failsafe.
   - `references/melodic-cells-and-sequences.md`: Mark Watkins 4-note cells (`1-3-5`, `1-5`, `7th`, `5-9` upper-half), `P/I/R/RI` permutations, circular `up/up`, `up/down`, `down/down`, `down/up`, real half-step side-stepping, `ii-V` pairing, bebop cells (`3-b9-b7-maj7 -> 5th`, `3-b9-maj7-b7 -> 3rd`), 4 Bebop scales & upbeat alignment rule.
   - `references/rhythm-vocabulary-and-solo-form.md`: Thống kê thực nghiệm Charlie Parker (Watkins Ch. 3: `56%` upbeat + `13–15%` drag starts, 4 phrase endings, *The Bop* `~2/3` beat, ghosted upbeats, below-pitch terminal vibrato), Rhythm Blocks (`1–4` note cells & *On/Half-way/Ricochet/Almost*), Golden Mean (`0.618` / `62–67%`) climax arc, space discipline, song forms & arrangement slots.
   - `assets/chord-scale-and-cell-catalog.yaml`: Bảng tra cứu YAML chuẩn xác đã kiểm tra bằng `pyyaml`.

2. **Nâng cấp `music_maker_plugin/skills/groove-rhythm-drums/`**:
   - `SKILL.md`: Áp dụng `llm-prompt-optimizer` (CoT 5 bước, kiểm soát 4-limb, weeding & `1->2->4->8` Doubling Up, khóa SF2 `velRange`/`exclusiveClass`, Few-Shot Transformation, bảng Navigation mở rộng).
   - `references/midi-drum-realism-and-four-limb-craft.md`: 4-limb polyphony, mute hats/rides khi tom fill, L/R dominant-hand sticking asymmetry, weeding & Doubling Up `1->2->4->8`, iterative quantize `10–50%`, split micro-timing & audience-view panning.
   - `references/advanced-fills-transitions-and-sound-tricks.md`: Dual-snare/timbale fills, flams, partial reversal, Sneaky Snare layer, 3-zone ride, odd poly-loops (`5-beat` conga + `7-beat` hat), 32nd-triplet Big Beat zipper rolls, octave kick layering, tempo-synced pitch-shifting delay & half-speed bouncing.
   - `references/afro-cuban-and-latin-coordination.md`: Quy tắc chọn `2-3`/`3-2` clave theo giai điệu (Ignacio Berroa), Son vs Rumba clave, điều phối 4 chi & 14+ điệu Afro-Cuban (*Afro 6/8, Abaquà, Bembé, Guiro, Cáscara+Clave, Mambo, Son Montuno, Cha-cha, Mozambique, Songo, Timba, Rumba Guaguancó, Ballroom Rumba, Bolero, Danzón, Guajira*) cùng chỉ dẫn `Snare Off`, `Floor Tom Shell`, `Jam Block`, `Large/Small Cowbells`, `Soft Rim-Shot`, `Buzz Roll`.
   - `references/soundfont-gm-gs-drum-architecture.md`: Quy chuẩn `wBank = 128` / GS `Bank 120`, 12 GS kits (`Standard`, `Room`, `Power`, `Electronic`, `808/909`, `Dance`, `Jazz`, `Brush`, `Orchestral`, `SFX`), `keyRange`/`velRange`/`exclusiveClass` chokes (`42/44/46`, triangle, guiro, cuica, whistle, surdo), default modulators & FluidSynth/GeneralUser GS `127/108/82/46` velocity ladder.
   - `assets/gm-gs-percussion-map.md`: Bảng đầy đủ 62 nốt MIDI (`27 D#0` – `88 E5`) qua cả 10 cột kit GS, kèm ghi chú chuyển đổi `C3=60` (GS) sang `C4=60` (toolkit).

3. **Đồng bộ Plugin & Sửa lỗi hậu `code-reviewer`**:
   - Cập nhật `music_maker_plugin/agents/{composer-theorist,groove-arranger,executive-producer,soundfont-mix-engineer}.md`, `music_maker_plugin/skills/soundfont-music/SKILL.md`, `music_maker_plugin/rules/AGENTS.md`, `music_maker_plugin/plugin.json` (`1.4.0`), `music_maker_plugin/THIRD_PARTY.md`, và `README.md`.
   - Xử lý toàn bộ góp ý từ `code-reviewer`: bỏ chú thích đường dẫn `tai lieu/` trong `chord-scale-and-cell-catalog.yaml`, sửa API không tồn tại `BendType.VIBRATO` sang `Track(..., vibrato=...)` / below-pitch terminal `t.bend(...)`, làm rõ quy ước quãng tám `C3=60` vs `C4=60` trong bảng trống, sửa vị trí `[0, 6, 12]` trên lưới 16 bước cho Son Clave, và sửa lỗi chính tả (`udu`, `Bouncing`, `THIRD_PARTY.md` path).

### Kiểm thử sau cùng
- `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 9 · agents 4 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).
- Kiểm tra `pyyaml` đối với `chord-scale-and-cell-catalog.yaml`: **OK** (7 root keys).
- `uv run --with numpy --with scipy --with mido python -B -m unittest discover -s tools/tests -v`: **12/12 tests OK**.

---

## Phiên làm việc: 2026-11-22 (Phần 3) — Khóa mục tiêu Pitch Bend, Inline `midi_map.md` & Quy tắc Ưu tiên Phong cách

### Mục tiêu
1. Giải quyết lỗi AI bend lung tung thiếu ý đồ nốt đích bằng tài liệu nghiên cứu web đã trích xuất sang text (`tai lieu/pitch_bending/*.md`) và đóng góp vào các skill hiện có + nâng cấp toolkit Python.
2. Nâng cấp định dạng `midi_map.md`: đưa `### Project README` lên đầu mỗi project, khử trùng lặp/rác dump CC64 & Pitch Bend riêng, nhúng trực tiếp `ped` và `bend=...[Target]` inline trên từng nốt (không tự phân loại style vì `readme.md` đã ghi rõ).
3. Gỡ bỏ các rào cản khiến AI bỏ qua phong cách từ `midi_map.md` khi làm project ballad (đặc biệt độ dài dòng cũ >151 KB gây cắt đọc, cộng với việc `genre-style-encyclopedia` / `style-maps.md` / `producer-mindset-workflow` áp đặt mặc định textbook).

### Những thay đổi đã thực hiện

1. **Nghiên cứu & Chưng cất tài liệu Pitch Bend (`tai lieu/pitch_bending/`)**:
   - Tải và trích xuất 4 bài báo arXiv sang Markdown (`arxiv_2308_12307_modeling_bends.md`, `arxiv_2401_13498_expressive_guitar.md`, `arxiv_1910_09021_erhu_techniques.md`, `arxiv_0906_0127_intonation_fretted.md`).
   - Viết `music_maker_plugin/skills/guitar-bass-expression/references/pitch-bend-target-grammar.md` theo chuẩn `llm-prompt-optimizer` (khóa `start -> target`, 4 trạng thái `∅/↑/→/↓` từ mô hình Steve Vai & thống kê 932 track của D'Hooge et al. 2023, bảng bậc âm cho Blues/Pentatonic/Major-Ballad, bend đồng âm/oblique/pre-bend, slide đơn âm cho dây/erhu/bass/synth, ví dụ Few-Shot inline `midi_map.md` và API thực tế của toolkit).

2. **Nâng cấp Toolkit Python & `midi_map.md`**:
   - `engine/harmony.py`: Thêm `SCALE_INTERVALS`, `parse_scale()`, `infer_scale_pcs()`.
   - `engine/song.py`: Thêm `target=` cho `Track.bend()` và `Track.bend_last()` (hỗ trợ cả `int`/`np.integer`/tên nốt và chặn nhầm hướng `scoop`/`dive` có `target` cao hơn nốt gốc).
   - `engine/expression.py`: Nâng cấp `expressive_bends(..., key=None, scale=None, harmony=None)` ràng buộc đích bend theo âm giai/hợp âm (đã xử lý cả `role="strings"` `scoop` và tách `key` + `scale`).
   - `engine/review.py` & `review_song.py`: Thêm `--scale` / `scale=` và báo cáo `out_of_scale_bends` (ngưỡng `>= 0.8 st`).
   - `engine/midi_io.py`, `analyze_midi.py` & `tools/generate_midi_map.py`: Đưa `### Project README` lên đầu block dự án, gỡ hoàn toàn dump `All Pitch Bend Events` và `All Pedal CC64 Events`, thêm `_dedupe_pedals()`, `_summarize_note_bend()` (xử lý chuẩn cả bend khởi trễ sau `0.02s`), `_is_note_pedaled()`, xuất `ped` và `bend=...[Target]` inline ngay trên từng nốt.
   - Tái tạo `music_maker_plugin/midi_map.md`: **830 dòng**, dòng dài nhất chỉ còn **1.540 bytes** (thay vì >151 KB bị cắt đọc trước đây), 0 lỗi `[C3->C3]`.

3. **Cập nhật Skills, Rules & Agents (`llm-prompt-optimizer`)**:
   - Bổ sung giao thức khóa nốt đích và liên kết `pitch-bend-target-grammar.md` vào `guitar-bass-expression/SKILL.md`, `instrumental-soloing-improvisation/SKILL.md`, `music-theory-harmony/SKILL.md`, và `soundfont-music/references/toolkit.md`.
   - Khẳng định quyền ưu tiên tuyệt đối (`midi_map.md` + `readme.md` ghi đè mặc định chung từ `genre-style-encyclopedia`) trong `music_maker_plugin/rules/AGENTS.md`, `soundfont-music/SKILL.md`, `producer-mindset-workflow/SKILL.md` (xóa nhãn `"No House Style"`), `genre-style-encyclopedia/{SKILL.md,references/style-maps.md}`, `orchestration-arrangement/SKILL.md`, `mixing-timbre-mastering/SKILL.md`, và `agents/{executive-producer,soundfont-mix-engineer}.md`.
   - Cập nhật SpecKit: `specs/001-pitch-bend-and-midi-map-style/{spec.md,plan.md,tasks.md}`.

4. **Rà soát & Sửa lỗi từ `code-reviewer`**:
   - Khắc phục các lỗi HIGH/MEDIUM/LOW phát hiện được: sửa ví dụ sai `lead.play()` / `harmony=chord_track` / `review_song.py` trong tài liệu tham chiếu; sửa lỗi `expressive_bends()` ép `1.0 st` ở `role="strings"` gây lệch âm giai; sửa `_summarize_note_bend()` cho bend trễ sau onset; thêm bảo vệ mảng rỗng trong `_dedupe_pedals()`; hỗ trợ `np.integer` và kiểm hướng `scoop`/`dive` trong `Track.bend()`.

### Kiểm thử sau cùng
- `tools/tests/test_toolkit_bends.py` + `tools/tests/test_toolkit_specs.py`: **17/17 tests OK** (0.229s).
- `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 9 · agents 4 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).
- Kiểm tra `Select-String`: **0 tham chiếu** `tai lieu/`, **0 khối** `All Pitch Bend Events`, **0 nhãn** `[C3->C3]` trong `midi_map.md`.

---

## Phiên làm việc: 2026-11-22 (Phần 4) — Chưng cất 107 Tài liệu Hòa âm Cực kỳ Nâng cao, Đối âm/Post-Tonal & Phối khí Dàn nhạc/Big Band (v1.5.0)

### Mục tiêu
Theo kế hoạch SpecKit `002-advanced-harmony-and-orchestration` (Phương án 1 đã được người dùng duyệt) kết hợp `llm-prompt-optimizer`:
1. Chưng cất trung thực 100% (không bịa đặt, không để lộ đường dẫn nội bộ) toàn bộ **107 file `.txt` (trích xuất từ 53 PDF)** trong `tai lieu/` vào 3 trụ cột skill + toolkit Python theo chuẩn TDD.
2. Bổ sung agent chuyên môn thứ 5 (`orchestral-bigband-arranger.md`) và nâng cấp toàn bộ 4 agent hiện có.
3. Sau khi chưng cất đầy đủ, kiểm thử vượt `code-reviewer`, dọn sạch thư mục `tai lieu/`.

### Những thay đổi đã thực hiện

1. **Nâng cấp Python Toolkit (`soundfont-music/scripts/toolkit/engine/`) & TDD (`tools/tests/test_toolkit_advanced.py`)**:
   - `harmony.py`: Bổ sung 12 hợp âm mở rộng/biến đổi (`7alt`, `7b9b13`, `7#9#11`, `13#11`, `13b9`, `7#5#9`, `maj9#11`, `mMaj9`, `mmaj9`, `6/9#11`, `m11b5`, `sowhat`), phân tích đa hợp âm `D|C7` (`upper_pcs` + `lower_pcs`), phép biến đổi Neo-Riemannian `plr_transform()` (`P/L/R/S/N/H`), đối xứng âm tính CRT `negative_harmony_pcs()`, chu kỳ `coltrane_cycle()`, hệ thang âm `barry_harris_scale()`, và `upper_structure_triad()`.
   - `voicing.py`: Hỗ trợ đa hợp âm trong `chord_tones()`/`voice_lead()`, bổ sung `drop2()`, `drop3()`, `drop24()`, `quartal_stack()`, `so_what_voicing()`, và `upper_structure_voicing()`.
   - `review.py`: Thêm chẩn đoán `register_clumps` (phát hiện chen chúc 1–2 nửa cung cùng họ nhạc cụ dưới `C4`, tách đúng GM `46` harp / `47` timpani ra khỏi `"strings"` và bao gồm String Ensemble `48–51`).

2. **Nâng cấp `music-theory-harmony/`**:
   - Thêm `references/harmony/neo-riemannian-and-tonnetz.md` (PLR/Coxeter $\tilde{S}_3$/Golden Tonnetz/Tarnhelms vs Ids, Hệ trục `T/S/D` Lendvai/Bartók, hệ thống kết phim Lehman Mixed Plagal / Subtonic / `CMCR Types 0/I/III/IV/VI`), `negative-harmony-and-polarity.md` (CRT $\mathbb{Z}_3 \times \mathbb{Z}_4$, bản đồ trục cực & Lydian Chromatic Concept 7 thang âm thành viên của George Russell), `advanced-jazz-gospel-voicings.md` (Upper Structure Triads Jason Lyon, Gospel Polychords `bVIImaj7/R` & `IIImaj7b5/R`, Barry Harris 6th-Diminished 12 giọng, Coltrane M3/m3 & Drop/Quartal), và `assets/advanced-harmony-catalog.yaml`.

3. **Tạo Skill mới `counterpoint-fugue-and-post-tonal/`**:
   - `SKILL.md` & `references/00-navigation.md`
   - `references/strict-and-invertible-counterpoint.md` (Species 1–5 Jeppesen vs Schoenberg, đối âm tâm lý Belkin, bảng đảo quãng Đối âm kép quãng 8/10/12 và đối âm 3–4 bè của Prout).
   - `references/fugue-and-canon-architecture.md` (Subject, quy luật biến điệu Real vs Tonal Answer, Countersubject, Exposition, Episode, Stretto/Inversion/Augmentation, Double/Triple Fugue, Canon, Goetschius Homophonic & Larger Forms).
   - `references/post-tonal-set-and-serial-theory.md` (Prime Form Forte vs Rahn, Tone Clock Absil/Schat, đếm tổ hợp Hook Pólya 29 tetrachord / 224 set class, Tứ diện Cohn đỉnh `[0123]/[0167]/*0167*/[0127]`, Straus Total Voice Leading `IFUNC`/`imultiset` `<Tn>`/`<In>` & Multiple Parentage, chu kỳ 48 dạng hàng 12 âm & Segmental Invariance).
   - `references/spectral-and-schillinger-techniques.md` (Giai điệu Spectral Differential/Liminal/Transitory của Grisey/Vivier/Haas & độ lệch cents bồi âm 3–13, nhịp giao thoa chu kỳ Schillinger `a ÷ b -> r(a:b)`, Fractioning, 3 generators & tốc độ biến thiên).
   - `assets/post-tonal-and-fugue-catalog.yaml`.

4. **Nâng cấp `orchestration-arrangement/`**:
   - Thêm `references/orchestration/classical-masters-orchestration.md` (7 Texture Types của Piston, Overlaying/Crossing/Enclosure của Rimsky-Korsakov, cân bằng số lượng, vật lý vĩ & tầm âm/vùng yếu từ Berlioz/Strauss/Forsyth/Widor/Prout/Absil).
   - Thêm `references/orchestration/timbre-grouping-and-modern-scoring.md` (ACTOR/McAdams TOGE Concurrent/Sequential/Segmental, Belkin Planes, thực chiến chấm bài phòng thu & pops của Tim Davies).
   - Thêm `references/orchestration/big-band-and-sectional-voicings.md` (Biên chế 17 cây, 4-Way Close, khử cấn `m2`, 5 phương pháp hòa âm Approach Note, Drop-2/2+4, Cascades, Spread Pads, Dissonance Arc, quy tắc `D3` của Evan Rogers & Swing/Latin Clave).

5. **Đồng bộ Hệ sinh thái, Sửa lỗi `code-reviewer` & Dọn dẹp**:
   - Tạo agent thứ 5 `agents/orchestral-bigband-arranger.md`; nâng cấp `composer-theorist.md`, `groove-arranger.md`, `executive-producer.md`, `soundfont-mix-engineer.md`, `agents/README.md`, `rules/AGENTS.md`, `soundfont-music/{SKILL.md,references/toolkit.md}`, `plugin.json` (`1.5.0`), `THIRD_PARTY.md`, và `README.md`.
   - Khắc phục toàn bộ góp ý HIGH/MEDIUM/LOW từ `code-reviewer`: xử lý polychord trong `voicing.chord_tones()`, sửa kiểm tra mode `"major"`/`"maj"`/`"M"` trong `plr_transform()` & `barry_harris_scale()`, đồng bộ key `usv["shell"]` & 6 hợp âm `coltrane_cycle()` trong tài liệu, sửa map GM `46/47` (harp/timpani) khỏi `"strings"`, xóa 2 dòng ghi chú nháp LLM, chỉnh chính xác bảng CMCR Lehman, phép soi âm tính `Fmaj7 -> Ebmaj7`, quy tắc Forte/Rahn & đỉnh tứ diện Cohn `[0127]`.
   - Xóa toàn bộ tài liệu tạm trong `tai lieu/` sau khi toàn bộ kiến thức đã nạp và kiểm thử đạt chuẩn.

### Kiểm thử sau cùng
- `uv run --with numpy --with scipy --with mido python -B -m unittest discover -s tools/tests -v`: **24/24 tests OK**.
- `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 10 · agents 5 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).
- Kiểm tra rò rỉ `tai lieu/`, `py_compile`, JSON `plugin.json` và YAML (`advanced-harmony-catalog.yaml`, `post-tonal-and-fugue-catalog.yaml`): **OK (0 lỗi, 0 rò rỉ)**.


---

## Phiên làm việc: 2026-11-23 — Tối ưu Quy tắc Song hành (`Docs ‖ midi_map.md`), Giao tiếp Thuần Âm nhạc & Chủ động Chuyển đoạn / Báo trống (v1.6.0)

### Mục tiêu
Kích hoạt `llm-prompt-optimizer` (khung RSCIT, Positive Alternatives, Few-Shot, Prompt Compression) kết hợp quy trình SpecKit (`specs/003-dual-knowledge-and-producer-persona/`) và ECC để bổ sung 3 quy tắc cốt lõi cho `music_maker_plugin`:
1. **Song hành Ưu tiên Hàng đầu (`Specialist Docs ‖ midi_map.md`)**: Bắt buộc đọc **song song** tài liệu trong các skills/agents chuyên gia cùng với kho `music_maker_plugin/midi_map.md` (cả hai đều là ưu tiên #1 ngang hàng vì `midi_map.md` chứa sắc thái thực chiến mà văn bản không diễn tả hết), cho phép kế thừa / mô phỏng 100% phong cách từ `midi_map.md` một cách âm thầm.
2. **Giao tiếp Thuần Âm nhạc (Zero-Code User Persona)**: Dù dựng nhạc bằng Python toolkit ở tầng ngầm, AI giao tiếp với người dùng hoàn toàn bằng ngôn ngữ Nhà sản xuất / Chuyên gia Âm nhạc (không nhắc đến mã nguồn, Python, file `.py`, hàm, biến trừ khi người dùng hỏi trực tiếp về code).
3. **Chủ động Sáng tạo Chuyển đoạn, Báo trống & Độ gối Mượt mà**: Coi cấu trúc prompt của người dùng là khung chính; chủ động sáng tạo chuyển đoạn (turnarounds, pre-chorus lifts, bridges/interludes, key-lift modulations), báo trống (drum fills, pickups, cymbal swells, snare rolls) và độ gối chuyển tiếp (fuzzy boundaries).

### Những thay đổi đã thực hiện

1. **SpecKit `003-dual-knowledge-and-producer-persona`**:
   - Tạo `specs/003-dual-knowledge-and-producer-persona/{spec.md,plan.md,tasks.md,checklists/requirements.md}` và cập nhật `.specify/feature.json`.

2. **Tối ưu Quy tắc Trung tâm (`music_maker_plugin/rules/AGENTS.md`)**:
   - Cấu trúc lại theo chuẩn RSCIT (`Role & Situation`, `1. Dual Top-Priority Knowledge: Specialist Docs ‖ midi_map.md`, `2. Pure Music Producer Communication (Zero-Code Persona)` kèm Few-Shot chuyển đổi ngôn ngữ, `3. Proactive Transitions, Drum Fills & Musical Flow`, `4. Sustain Pedal & Instrument Spreading`, `5. Multi-Track Audio Export`, và giữ nguyên `Project directory structure rules`).

3. **Đồng bộ Toàn bộ 10 Skills, 5 Agents, Manifest & README**:
   - `music_maker_plugin/skills/soundfont-music/SKILL.md`, `producer-mindset-workflow/{SKILL.md,references/song-planner-protocol.md}`, `groove-rhythm-drums/SKILL.md`, `orchestration-arrangement/SKILL.md`, `music-theory-harmony/SKILL.md`, `genre-style-encyclopedia/SKILL.md`, `guitar-bass-expression/SKILL.md`, `instrumental-soloing-improvisation/SKILL.md`, `mixing-timbre-mastering/SKILL.md`, `counterpoint-fugue-and-post-tonal/SKILL.md`.
   - `music_maker_plugin/agents/{executive-producer,composer-theorist,groove-arranger,orchestral-bigband-arranger,soundfont-mix-engineer}.md`.
   - Nâng phiên bản `music_maker_plugin/plugin.json` lên `1.6.0` và cập nhật `README.md`.

4. **Xử lý Toàn bộ Góp ý từ `code-reviewer`**:
   - Khắc phục 1 lỗi HIGH (`mixing-timbre-mastering/SKILL.md` loại bỏ tên hàm Python/thuật ngữ script khỏi ví dụ và Output Format, gắn nhãn Internal Handoff).
   - Khắc phục 3 lỗi MEDIUM (`counterpoint-fugue-and-post-tonal/SKILL.md` khôi phục guard ẩn nguồn & ưu tiên #1 song song; đồng bộ CoT Step 1 song hành `Docs ‖ midi_map.md` ở 4 skill lý thuyết/phối khí/guitar/thể loại; đánh dấu Internal Handoff trên Output Format của các specialist skills để tránh rò rỉ hàm nội bộ ra giao tiếp người dùng).
   - Khắc phục 2 lỗi LOW (bổ sung positive alternatives theo `llm-prompt-optimizer` cho các quy tắc stealth/zero-code trong `AGENTS.md` và agents; bổ sung chủ động chuyển đoạn hòa âm vào `music-theory-harmony/SKILL.md`).

### Kiểm thử sau cùng
- `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 10 · agents 5 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`, 0 errors, 0 warnings).
- Kiểm tra JSON `music_maker_plugin/plugin.json` (`1.6.0`) và Markdown formatting: **OK**.


---

## Phiên làm việc: 2026-11-23 — Skill `melody-harmonization` & Tái hòa âm Toàn diện (v1.7.0)

### Mục tiêu
Tìm kiếm, tải và trích xuất sang văn bản thuần bộ tài liệu thực chiến từ cốt lõi đến nâng cao về tư duy soạn hòa âm cho giai điệu có sẵn và thiết kế tiến trình hợp âm nói chung; áp dụng `llm-prompt-optimizer` + SpecKit (`specs/004-melody-harmonization-skill/`) + ECC để đóng gói 100% trung thực (không bịa đặt, không thêm mã Python phân tích giai điệu) thành skill phổ quát mới `melody-harmonization`, kích hoạt mọi lúc khi soạn/tái hòa âm, sau đó xóa toàn bộ tệp trong `tai lieu/`.

### Những thay đổi đã thực hiện

1. **Nghiên cứu & Trích xuất Nguồn (32 tài liệu -> 100% chuẩn hóa trước khi xóa `tai lieu/`)**:
   - Đã thu thập, đối chiếu và trích xuất 32 tài liệu mở/học thuật & sư phạm: Trevor de Clercq (2018 Melodic Skeletons & Bass Meta-Schemas, 2019 Harmonic-Bass Divorce, 2023 ~2s Harmonic Rhythm), Temperley & de Clercq (2013 Corpus Stats), AccoMontage2 (ISMIR 2022 3-Level Scoring), AutoHarmonizer (Beat-Strength & `Γ` Harmonic Rhythm), *Open Music Theory v2* (Phrase Model `Tb–PD–D–Te`, Jazz Voicings `3–7` + `9–13`, Embellishing Chords/`CT°7`, Substitutions/`subV7`/`ii–V` Space, Pop/Classical/Modal/Pentatonic Schemas, Tonicization, Closely Related Modulation, Modal Mixture, Spicer Fragile/Emergent/Absent Tonics), và bộ tài liệu Ted Greene (Chord Substitution Parts 1–10, Harmonic Improvement Concepts, Gospel Feels, What to Expect in Popular Music, Major-Key Harmonic Tendencies, Pre-Destination Chord Movements, Scale-Chord Relationships in Popular Music).
   - Không thêm bất kỳ module Python phân tích giai điệu nào vào `engine/`.

2. **SpecKit `004-melody-harmonization-skill` & Nâng cấp Plugin (`v1.7.0`)**:
   - Tạo `specs/004-melody-harmonization-skill/{spec.md,plan.md,tasks.md,checklists/requirements.md}` và cập nhật `.specify/feature.json`.
   - Tạo trọn bộ 8 tệp trong `music_maker_plugin/skills/melody-harmonization/`:
     - `SKILL.md` (71 dòng): Tối ưu theo chuẩn `llm-prompt-optimizer` (RSCIT, 5-step Chain-of-Thought, Zero-Hallucination Constraints, Dual Priority `Docs ‖ midi_map.md`, Zero-Code User Persona, 2 Few-Shot Examples đã kiểm chứng voice-leading từng nốt, Output Format ở cuối).
     - `references/00-navigation.md` (21 dòng), `references/melodic-skeleton-and-harmonic-rhythm.md` (80 dòng), `references/phrase-architecture-and-scoring.md` (66 dòng), `references/ted-greene-substitution-and-approach-toolkit.md` (113 dòng), `references/voice-leading-embellishment-and-modulation.md` (74 dòng).
     - `assets/harmonic-tendencies-and-approaches.yaml` (213 dòng): Bảng tra cứu YAML đầy đủ 3 Chord Families, 38 mục `major_key_harmonic_tendencies`, bảng Pre-Destination (`to_minor`: 27, `to_dom`: 16, `to_maj`: 14 + 5 `combined_turnaround_examples`), và `scale_chord_relationships_pop`.
     - `assets/melody-harmonization-checklists.md` (38 dòng): 5-Gate Pre-Arrangement Audit + Diagnostic Matrix.
   - Tích hợp phổ quát (universal activation) vào `music_maker_plugin/rules/AGENTS.md`, `skills/soundfont-music/SKILL.md`, `skills/music-theory-harmony/{SKILL.md,references/00-navigation.md,references/harmony/reharmonization.md}`, `agents/{composer-theorist,executive-producer}.md`, `THIRD_PARTY.md`, `plugin.json` (`1.7.0`), và `README.md` (`v1.7.0`, 11 skills).

3. **Kiểm toán `code-reviewer` & Dọn dẹp**:
   - Đã xử lý triệt để toàn bộ 5 lỗi HIGH, 6 lỗi MEDIUM và 4 điểm LOW từ `code-reviewer` (sửa `SKILL.md` Example 1 & 2 voice-leading chính xác 4 giọng không bước nhảy vượt bậc 2, sửa liên kết chéo `../../` từ `references/`, bổ sung `m7+`, `v(7)<->iiiø7`, 3 mục `iv6/v6/vi6`, `Any logical bass progression`, nhãn `(More rare)`, 5 ví dụ kết hợp từ bản tóm tắt 1977, cảnh báo `do not think Lydian Melodic`, công thức liên tục `chord_bars ≈ BPM / 120` bù khoảng trống tempo bins, loại bỏ mô tả suy đoán không có trong AccoMontage2 và bass line không có nguồn ở Concept 9).
   - Xóa sạch 100% nội dung bên trong thư mục `tai lieu/` (`TAI_LIEU_REMAINING: 0`).

### Kiểm thử sau cùng
- Kiểm tra `yaml.safe_load()` trên `harmonic-tendencies-and-approaches.yaml`, `json.loads()` trên `plugin.json` (`1.7.0`), kiểm tra tất cả liên kết chéo tương đối trong `references/`, quét rò rỉ đường dẫn `tai lieu` (`CLEAN_TAI_LIEU_LEAKS: 0`): **OK**.
- `agy plugin validate --strict music_maker_plugin`: **Validation passed** (`skills 11 · agents 5 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0`).
