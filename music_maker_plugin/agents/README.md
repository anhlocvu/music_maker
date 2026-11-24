# Thư mục Agents chuyên môn (`agents/`)

Đây là nơi đặt 6 specialist agents phối hợp trong `music_maker_plugin`:

| Agent | Chuyên môn cốt lõi |
|---|---|
| `executive-producer.md` | Học ngầm `midi_map.md`, Song Planner, Production Brief, phân định thể loại / hệ hòa âm / biên chế dàn nhạc |
| `composer-theorist.md` | Hòa âm nâng cao (NRT `PLR`/`H`, Negative Harmony `Z3xZ4`, Axis, CMCR, LCC, Upper Structure, Gospel, Barry Harris, Coltrane), Đối âm / Fuga / PC-Set / 12-Tone / Spectral / Schillinger & giai điệu cao trào |
| `orchestral-bigband-arranger.md` | Dàn nhạc giao hưởng & phim/pops (`Piston` 7 Textures, `Rimsky` Overlaying/Crossing/Enclosure, `ACTOR` TOGE blending, `Davies` studio scoring) & Big Band (`4-Way Close`, 5 approach harmonizations, `Drop-2/2+4`, `Cascades`, `Impact Spreads`, kiểm soát `D3` low intervals) |
| `groove-arranger.md` | Trống 4-limb, Afro-Cuban/Latin clave & tumbao, Big Band Swing pocket, nhịp Schillinger `r(a:b)`, kick-bass composite, pedal/strum/arpeggio & 5 lớp chức năng |
| `soundfont-mix-engineer.md` | Tra preset `.sf2`, lập trình `soundfont-music` (gồm `engine.harmony`/`voicing`), kiểm tra `review_song.py` (`register_clumps`, `out_of_scale_bends`), mixing & xuất `multi_track/*.wav` (`pan=0`) + kiểm định NumPy |
| `audio-listening-critic.md` | Đạo diễn âm thanh / Mastering Ear: nghe trực tiếp file `.wav` mix tổng và `multi_track/` stems ở nhiều cấp thời lượng (Macro, Meso 15–30s, Micro 3–10s qua `slice_audio.py`) để thẩm định thực chiến 5 trục trước khi bàn giao |

Khi plugin được kích hoạt:
- `soundfont-music` luôn là skill điều phối chính.
- Tất cả các skill trong `skills/` và 6 agent chuyên môn trong `agents/` được kích hoạt đồng bộ theo quy tắc tại `rules/AGENTS.md`.
