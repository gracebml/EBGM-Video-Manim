# 🤖 PROMPT cho CODEX — Storyboard S05 / S07 / S11

> Đọc kèm `prompt_codex.md` (luật chung: skeleton `beat_to`, `load_scene_timing`, English-only, palette `_common.py`, đo ffprobe) và `prompt_codex_S01.md` (mẫu cách bám thoại). File này ghi đè storyboard cho **S05, S07, S11** — làm đúng nội dung thoại, hiệu ứng CÓ Ý NGHĨA, KHÔNG dày đặc/chồng lấp.

## NGUYÊN TẮC CHUNG (áp cho cả 3)
- Mỗi beat **một tiêu điểm**; cái cũ mờ/đẩy đi trước khi cái mới vào. Không hiệu ứng trang trí vô nghĩa.
- Khớp audio tuyệt đối: `self.add_sound(...)`, canh beat theo mốc câu dưới đây, chốt `self.wait(duration - elapsed)`.
- Nhãn ngắn = `en_label(...)` (English). KHÔNG phụ đề. Công thức = `MathTex` (giữ ký hiệu quốc tế).
- 3D nặng trên CPU: `Surface` để `resolution=(16,16)` khi `-pql`, `(32,32)` khi `-pqh`.

---

# 🎬 S05 — GABOR WAVELETS (scene_05 · 34.04s · ThreeDScene)
**Ý nghĩa cốt lõi:** từ 1 điểm trên mặt → giải thích Gabor = sine × Gaussian → là bộ lọc theo hướng/tần số → DC-free → giống filter lớp đầu CNN / vỏ não.

| Beat | Mốc (s) | Thoại | Hình (ý nghĩa) |
|---|---|---|---|
| B0 | 0.00–4.00 | "How does the AI see a single point on a face?" | Mặt (ảnh/silhouette) thu nhỏ góc; **zoom vào MỘT điểm** (khóe mắt) → 1 chấm sáng + ô patch nhỏ quanh nó. |
| B1 | 4.22–9.16 | "Instead of pixels... borrowed from biology." | Cạnh patch: lưới pixel thô **nhấp nháy/đổi giá trị** (coral, "nhạy sáng") → gạch chéo bỏ. Gợi ý chuyển sang sinh học (icon mắt/vỏ não mờ). |
| B2 | 9.50–15.16 | "GABOR wavelets... sine wave trapped inside a Gaussian envelope." | **Dựng Gabor:** vẽ `sine wave` (cyan) **×** `Gaussian envelope` (đường chuông, teal) **=** Gabor kernel. Có thể nâng kernel thành `Surface` 3D nhô lên. Hiện `MathTex` rút gọn của ψ. |
| B3 | 15.48–21.14 | "a filter, capturing only wrinkles and edges at one orientation and frequency." | Kernel **xoay** qua vài hướng + đổi tần số (ValueTracker) để minh họa "orientation & frequency". Áp kernel lên patch → highlight cạnh cùng hướng. |
| B4 | 21.68–26.22 | "it cancels out the background light component. It's DC-free." | Tăng/giảm độ sáng nền của patch → đáp ứng Gabor **không đổi** (ổn định). Nhãn `DC-free` (mint). |
| B5 | 26.22–33.64 | "Just like the first layers of a CNN... mirrors how the visual cortex works." | Bên cạnh kernel: **3 ô filter CNN lớp đầu** (edge detectors) hiện song song; caption `≈ CNN first-layer filter`; icon vỏ não glow. Kết. |

**Chống chồng lấp:** lưới pixel (B1) tan trước khi dựng kernel (B2). CNN filters (B5) chỉ xuất hiện ở cuối, không đè lên phần dựng kernel.

---

# 🎬 S07 — TWO SIMILARITY FUNCTIONS (scene_07 · 35.34s · ThreeDScene)
**Ý nghĩa cốt lõi:** so 2 jet bằng 2 hàm: (1) chỉ biên độ → **basin trơn rộng** (coarse); (2) có pha → **đỉnh nhọn subpixel** (fine) + chỉ hướng dịch. Đây là scene "wow" với Surface 3D.

| Beat | Mốc (s) | Thoại | Hình (ý nghĩa) |
|---|---|---|---|
| B0 | 0.00–2.50 | "With two jets, how does the machine know they match?" | Hai jet (stack-of-discs) cạnh nhau + dấu `?`. |
| B1 | 2.80–6.76 | "pairs two similarity functions in beautiful harmony." | Tách màn 2 panel: trái `Sₐ (amplitude)`, phải `S_φ (phase)` — mới chỉ tiêu đề, chưa vẽ surface. |
| B2 | 7.04–10.46 | "The first compares only amplitude, ignoring phase." | Panel trái sáng; `MathTex` Sₐ; pha bị "gạch bỏ". |
| B3 | 11.06–14.26 | "forming a smooth basin, a wide attractor," | **Surface 3D**: lòng chảo trơn rộng (1 cực tiểu), camera nghiêng để thấy chiều sâu. |
| B4 | 14.54–18.74 | "catch a signal from afar and slide toward the eye." | Thả `Sphere` ở rìa basin → **lăn mượt** xuống đáy (= hội tụ từ xa). |
| B5 | 19.18–20.68 | "This is the coarse step." | Nhãn `Coarse` (cyan) trên panel trái. |
| B6 | 20.88–24.00 | "the second function with phase kicks in." | Chuyển tiêu điểm sang panel phải; `MathTex` S_φ. |
| B7 | 24.20–30.32 | "razor sharp... pinning exact position with sub-pixel accuracy." | **Surface 3D thứ 2:** gồ ghề nhiều đỉnh nhọn, 1 đỉnh trung tâm cực sắc. Zoom vào đỉnh → nhãn `sub-pixel`. |
| B8 | 30.72–34.94 | "Better still, it points the way... how far to move the jet." | **Mũi tên displacement** (lavender) từ jet lệch → đúng vị trí; thanh `focus 1→5`. Kết. |

**Chống chồng lấp:** chỉ 1 surface hiển thị tại một thời điểm — basin (B3-B5) thu nhỏ/mờ khi surface pha (B7) lên. Hai panel không vẽ đồng thời 2 surface phức tạp.

---

# 🎬 S11 — ELASTIC MATCHING 4 BƯỚC ⭐ (scene_11 · 44.63s · ThreeDScene)
**Ý nghĩa cốt lõi:** lưới đồ thị đáp lên mặt, đi từ **cứng → mềm**: (1) khối cứng trượt tìm mặt; (2) co giãn khớp size+aspect; (3) bước Elastic: từng nút bò về mốc, cạnh = lò xo; (4) 2 pha Normalization → Recognition.

| Beat | Mốc (s) | Thoại | Hình (ý nghĩa) |
|---|---|---|---|
| B0 | 0.00–2.30 | "the heart of the algorithm." | Mặt thật (face.png) + lưới đồ thị lavender hiện mờ phía trên (chưa áp). Nhãn `Elastic Matching`. |
| B1 | 2.80–5.64 | "going from rigid to supple." | Thanh trạng thái `Rigid → Supple` (gợi tiến trình). |
| B2 | 5.98–10.70 | "rigid block sliding across the image to locate the face." | Lưới như **khối CỨNG** (giữ hình) **trượt** quét trên mặt; heatmap nhỏ chấm điểm; dừng tại khuôn mặt. Nhãn `λ = ∞ (rigid)`. |
| B3 | 10.92–16.78 | "scales globally to match size and stretches width and height for aspect ratio." | Lưới **co giãn đồng nhất** khớp size, rồi **kéo x/y độc lập** (aspect). Vẫn cứng. |
| B4 | 17.02–20.80 | "But the magic is the final step. The word elastic." | Dừng nhịp; chữ **`ELASTIC`** sáng lavender, lưới khẽ "thở". |
| B5 | 21.20–22.48 | "The graph is released." | Lưới đổi màu/khoá mở (các nút rời chế độ cứng). |
| B6 | 22.88–28.24 | "Each node crawls freely, nudging toward its true landmark." | **Từng nút bò** về đúng mốc (mắt/mũi/miệng) bằng path ngắn; nút tới đúng chỗ → glow. |
| B7 | 28.24–32.48 | "edges act as springs holding the structure from breaking apart." | Cạnh hiển thị **dạng lò xo** (zig-zag) co giãn giữ lưới; nhãn `λ = 2`. |
| B8 | 32.72–35.14 | "runs in two phases." | Lưới ổn định; tách timeline 2 khối. |
| B9 | 35.72–40.36 | "Normalization, crop the face to a standard 128×128." | Khối `Phase 1: Normalization` — crop khung về `128×128`. |
| B10 | 40.56–44.16 | "Then recognition, extract the final detailed graph." | Khối `Phase 2: Recognition` — lưới chi tiết cuối cùng trên mặt chuẩn hóa. Kết. |

**Chống chồng lấp:** B2→B3 lưới biến đổi tại chỗ (không nhân bản đè). B6 các nút bò **lần lượt/LaggedStart**, không nhảy loạn cùng lúc. B9/B10 hai khối phase nối tiếp, không đè.
**Lưu ý số:** đọc "120x128" trong audio là lỗi STT — đúng là **128×128**, nhãn ghi `128×128`.

---

## CHECKLIST CHUNG (mỗi scene S05/S07/S11)
- [ ] Mỗi beat khớp đúng câu thoại (mốc trên); từ khóa bật đúng lúc.
- [ ] `add_sound` đúng file; |render_dur − target| ≤ 0.3s (ffprobe).
- [ ] Không hiệu ứng vô nghĩa; KHÔNG chồng lấp (chỉ 1 tiêu điểm/lúc; cái cũ mờ trước).
- [ ] Mọi ảnh minh họa gốc còn đủ (chỉ cắt wait chết).
- [ ] English-only, 0 phụ đề; palette `_common.py` giữ nguyên.
- [ ] S07: chỉ 1 Surface hiển thị tại 1 thời điểm. S11: nút bò LaggedStart, nhãn `128×128`.

## LÀM
Làm **một scene một lần** (S05 → S07 → S11). Sửa `release/scene_S0X_*.py`, `manim -pql`, đo ffprobe, báo `render_dur` + Δ rồi dừng chờ duyệt mới sang scene kế.
