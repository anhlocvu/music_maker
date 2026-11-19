# Quy tắc vận hành Plugin `music_maker_plugin`

Plugin này chuyên sáng tác **nhạc hòa tấu không lời (instrumental)** và **nhạc beat** bằng SoundFont (`.sf2`) và Python toolkit.

## 1. Kích hoạt Skill & Agent đồng bộ

- **Skill chính**: `soundfont-music`.
- Khi người dùng yêu cầu kích hoạt plugin hoặc giao nhiệm vụ làm nhạc cho plugin này:
  1. **LUÔN kích hoạt `soundfont-music` làm skill chính** điều phối toàn bộ quy trình.
  2. **Đồng thời quét và kích hoạt toàn bộ các skill chuyên gia / skill khác** đang có trong `music_maker_plugin/skills/` (và nạp hướng dẫn của các agent chuyên môn trong `music_maker_plugin/agents/` nếu có file `.md` agent).

## 2. Học toàn bộ kho MIDI trước khi vào việc (`midi/`)

- Trước khi lên bố cục hay sáng tác bài nhạc mới, **BẮT BUỘC** kiểm tra và chạy script phân tích MIDI (`python analyze_midi.py` trỏ tới thư mục `music_maker_plugin/midi/`) để học toàn bộ dữ liệu MIDI hiện có.
- Kho `midi/` có thể chứa:
  - Các file `.mid` / `.midi` đơn lẻ (1 track hoặc multi-track).
  - Các **thư mục project MIDI** chứa nhiều file `.mid` tách riêng theo nhạc cụ (ví dụ: `drum.mid`, `bass.mid`, `piano.mid`, `lead.mid`...).
- **Nhận diện nhạc cụ qua tên file**: Luôn đọc chính xác **tên file (`filename`)** và **tên thư mục project** do `analyze_midi.py` xuất ra, vì tác giả đặt tên file theo đúng tên nhạc cụ.
- **Tư duy học từ MIDI**: Những file MIDI trong `midi/` là do chính tác giả (người dùng) tự đánh và tự phối. Hãy lấy đó làm tư liệu tham khảo cốt lõi để học **cách đánh, cách rải, cách fill chuyển đoạn, cách đánh trống (kick/snare/hat/ghost notes/fills), cách đi bass, cách xếp voicing, dynamics và tư duy phối khí** của tác giả. Nếu tác giả yêu cầu phối tiếp từ một bản phác thảo MIDI có sẵn, hãy nạp trực tiếp dữ liệu MIDI đó vào bài.

## 3. Kỹ thuật Pedal (Vang) & Rải nhạc cụ

- Với các nhạc cụ cần độ vang tự nhiên như **piano, e-piano, harp, guitar, strings, bell/celesta...**, không để hợp âm khô cứng ở các đoạn cần cảm xúc hoặc không gian rộng:
  - **Chủ động bật chế độ Pedal (`track.pedal(...)`)** cho các đoạn muốn giữ độ vang (vừa kéo dài âm thanh mượt khi render WAV, vừa ghi chuẩn MIDI CC 64 `Sustain Pedal`). Nhớ nhả/đạp lại pedal khi đổi hợp âm để tránh đục tiếng.
  - **Chủ động rải nhạc cụ (`track.strum(...)` / `track.arpeggio(...)`)** hoặc tách nốt hợp âm lệch thời gian tự nhiên ở các đoạn piano đệm, harp, guitar.

## 4. Quy tắc xuất Multi-Track Audio (`multi_track/`)

- Sau khi hoàn thiện bài nhạc, bên cạnh file MIDI và file WAV mix tổng, **BẮT BUỘC** tạo thư mục `multi_track/` (trong thư mục output của bài, ví dụ `out/<song>/multi_track/`) và xuất **toàn bộ các track thành từng file audio `.wav` riêng biệt** để người dùng có thể đưa vào DAW mix hoặc chỉnh sửa.
- **Quy tắc xử lý hiệu ứng & Pan khi xuất multi-track**:
  - **Giữ nguyên toàn bộ hiệu ứng của nhạc cụ** (reverb, vibrato, release, bend/glide, âm sắc, tỷ lệ âm lượng tương đối...).
  - **KHÔNG giữ `pan` của track** khi xuất multi-track (mọi track stem được đưa về giữa / center `pan=0` để người dùng tự do pan lại trong DAW).
  - Mọi file stem đều phải đồng bộ điểm bắt đầu tại `beat 0` (cùng mốc thời gian) để thả vào DAW là khớp nhịp ngay.
