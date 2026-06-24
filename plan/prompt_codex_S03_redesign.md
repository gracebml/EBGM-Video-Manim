# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 3 (S03 "Pre-Deep-Learning")

> File: `release/scene_S03_pre_deeplearning.py` (class `S03_PreDL`). Thiết kế lại **toàn bộ** phần hình. Giữ: `add_sound`, khung `beat_to`, English/LaTeX (`en_label`), palette, tổng = audio (**57.21s**, |Δ|≤0.3s). Render `-qh`.

## LỖI HIỆN TẠI (phải fix hết)
1. **Sơ đồ CNN sơ sài & chưa hoàn chỉnh:** các "khối" chỉ là grid phẳng mờ, không ra hình tích chập; **mũi tên backprop xấu** (cong lệch, đè chữ).
2. **Các khối không pop theo lời thoại** — hiện hết một lúc, rối, đè cả tiêu đề.
3. **Đoạn rewind 1997 quá đơn giản** — chỉ đồng hồ + 2 thẻ chữ.
4. **GPU/dataset không có minh họa** — chỉ chữ "No powerful GPUs".
5. **Các đoạn sau (paper, vỏ não, tên thuật toán, FERET) quá sơ sài** — chỉ chữ + hình vẽ thô.

## NGUYÊN TẮC
- **KHÔNG dùng `ThreeDScene` + camera rotation.** Dùng `Scene` (hoặc `MovingCameraScene`). Vẽ "3D" bằng **khối isometric** (polygon 3 mặt sáng-tối) — vừa đẹp vừa dễ ghép ảnh, KHÔNG xoay liên tục.
- **Mỗi khối/element POP theo đúng từ khóa** đang đọc (dùng `word_start(T, "...")`), `GrowFromCenter`/`FadeIn(scale=0.7→1)` + `Indicate` nhẹ. Mỗi lúc 1 tiêu điểm, cái cũ mờ/đẩy đi.
- Mũi tên: dùng `Arrow`/`CurvedArrow` **gọn, đều, KHÔNG đè chữ** (đặt dưới/khỏi khối).

## HELPER cần viết (gợi ý)
```python
def iso_box(w=1.0, h=1.4, d=0.5, color=ACCENT_CYAN, fill=0.18):
    """Khối tích chập kiểu isometric: mặt trước + mặt trên + mặt phải (3 độ sáng khác nhau)."""
    front = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2,
                      fill_color=color, fill_opacity=fill)
    top = Polygon(front.get_corner(UL), front.get_corner(UL)+np.array([d*0.7,d*0.5,0]),
                  front.get_corner(UR)+np.array([d*0.7,d*0.5,0]), front.get_corner(UR),
                  stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill*1.8)
    side = Polygon(front.get_corner(UR), front.get_corner(UR)+np.array([d*0.7,d*0.5,0]),
                   front.get_corner(DR)+np.array([d*0.7,d*0.5,0]), front.get_corner(DR),
                   stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill*0.6)
    return VGroup(front, top, side)

def conv_stack(n=3, color=ACCENT_CYAN):
    """Chồng vài khối isometric mô phỏng feature maps (conv volume)."""
    g = VGroup()
    for i in range(n):
        b = iso_box(0.18, 1.3-i*0.12, 0.4, color).shift(RIGHT*i*0.12+UP*i*0.0+OUT*0)
        g.add(b)
    return g

def gpu_3d(color=ACCENT_TEAL):
    """GPU card isometric: thân hộp dài + 2 quạt (vòng tròn + cánh) + cổng PCIe. KHÔNG xoay."""
    body = iso_box(2.4, 1.0, 0.5, color, fill=0.14)
    fan1 = VGroup(Circle(radius=0.28, color=color, stroke_width=2),
                  *[Line(ORIGIN, 0.26*np.array([np.cos(a),np.sin(a),0]), color=color, stroke_width=1.5)
                    for a in np.linspace(0,TAU,7)[:-1]]).move_to(body[0].get_center()+LEFT*0.55)
    fan2 = fan1.copy().shift(RIGHT*1.1)
    pcie = Rectangle(width=0.9, height=0.12, color=color, fill_opacity=0.4, stroke_width=1).next_to(body, DOWN, buff=0.02)
    return VGroup(body, fan1, fan2, pcie)
```
> (Có thể tinh chỉnh, miễn ra đúng tinh thần: khối 3D rõ ràng, GPU nhận ra được.)

## STORYBOARD MỚI (map 13 segment Jessica)

| Beat | Mốc (s) | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–4.96 | "facing face recognition, what's our first instinct?" | Ảnh mặt thật `face.png` nhỏ bên trái = **input**; nhãn lớn `Modern instinct?`. |
| B1 | 4.96–12.66 | "Build a **CNN**, gather **millions of images**, define a **loss**, **backpropagation**" | **Dựng CNN tử tế, pop từng phần theo từ:** tại "CNN" → khối conv `iso_box`/`conv_stack` đầu pop; tiếp các khối conv (2–3 volume) pop dần với **mũi tên forward** rõ giữa chúng → tới node `face ID` bên phải. Tại "millions of images" → nhãn + chồng ảnh nhỏ ở input. Tại "loss" → node `Loss ↓` góc phải. Tại "backpropagation" → **một `CurvedArrow` gọn chạy ngược** từ Loss về input (coral), nhãn `backpropagation` đặt **dưới** mũi tên (không đè khối). |
| B2 | 12.66–15.18 | "But rewind to 1997." | **Rewind thật:** mũi tên forward đảo chiều, khối CNN **co/mờ dần theo thứ tự ngược**; **đồng hồ quay ngược ~1 vòng** (chỉ 1 lần, KHÔNG liên tục); số `1997` lớn hiện giữa. |
| B3 | 15.18–17.24 | "No powerful GPUs." | **GPU 3D** (`gpu_3d`) pop lên giữa → **gạch chéo ✗ coral** + nhãn `No powerful GPUs`. |
| B4 | 17.24–19.38 | "No massive data sets." | **Khối dataset 3D** (chồng ảnh nhỏ / hình trụ database) pop → **✗ coral** + nhãn `No massive datasets`. GPU lùi ra trái cho gọn. |
| B5 | 19.38–25.34 | "Recognizing a face under changing light or expression… impossible if you only compared pixels." | Ảnh mặt thật (`face.png` ↔ `s2_same_lowlight`) **đổi sáng/biểu cảm**; phủ **lưới pixel**; phép so pixel bật **diff coral bùng** → nhãn `pixel compare ✗`. |
| B6 | 25.34–29.16 | "how did scientists solve this **geometric variance** problem?" | Trên mặt: các **điểm mốc + lưới dịch/biến dạng** (gợi geometric variance); nhãn câu hỏi `Geometric variance?`. |
| B7 | 29.16–34.70 | "Not with deep learning, but with **pure mathematics and signal processing**." | Icon mạng nơ-ron nhỏ **mờ + ✗**; thay bằng **ký hiệu toán** ($\int,\Sigma$, sóng Gabor) + nhãn `Pure math · signal processing` (thanh lịch). |
| B8 | 34.70–43.26 | "In **1997**, published in **IEEE PAMI**… an unusual idea" | **Ảnh paper thật `ebgm_paper_p1.png`** trượt vào (khung bo góc) + **con dấu `IEEE PAMI · 1997`** (lavender) đóng lên; highlight tiêu đề paper. |
| B9 | 43.26–47.06 | "teach the computer to see a face the way our **visual cortex** does." | **Minh họa vỏ não thị giác** (đường viền não + vùng V1 + tia) **glow**; tia nối não → ảnh mặt (báo trước Gabor). |
| B10 | 47.06–50.46 | "That algorithm is **Elastic Bunch Graph Matching**." | Reveal tên `ELASTIC BUNCH GRAPH MATCHING` lớn (lavender glow) + icon nhỏ lưới-đồ-thị-trên-mặt. |
| B11 | 50.46–55.26 | "ranked among the **very best** in **FERET** blind tests of the 1990s." | Badge `FERET · top-ranked` + **bảng xếp hạng nhỏ** (vài thanh, EBGM thanh cao nhất, vàng) hoặc bục huy chương. |
| B12 | 55.26–56.86 | "Today, we dissect it." | Mặt + lưới đồ thị **zoom nhẹ vào** dẫn sang scene sau; fade gọn. |

## ASSETS
✅ **Đã có sẵn, dùng trực tiếp:**
- `assets/ebgm_paper_p1.png` — **trang 1 paper EBGM thật** (cho B8).
- `assets/face.png`, `assets/s2_same_lowlight.jpg` — mặt + mặt thiếu sáng (B0, B5).

🟡 **TÙY CHỌN (👉 NOTE người dùng — chỉ nếu muốn đẹp hơn):**
- GPU: prompt yêu cầu **VẼ** `gpu_3d` (không cần ảnh). Nếu muốn ảnh GPU thật, người dùng có thể bỏ `assets/gpu.png` (ảnh card đồ họa nền trong), code ưu tiên ảnh nếu có, không thì vẽ.
- Vỏ não: vẽ bằng VMobject; nếu muốn ảnh, `assets/brain.png` (tùy chọn).

> Dùng helper `load_face`/thử nhiều đuôi như S02 cho ảnh tùy chọn, có fallback vẽ tay để luôn render được.

## RÀNG BUỘC
- Không ThreeDScene/xoay camera. Khối 3D = isometric polygon. Mỗi element pop theo từ khóa; không đè chữ; mỗi lúc 1 tiêu điểm.
- English-only, `en_label` (LaTeX Latin Modern), KHÔNG phụ đề. Palette `_common.py`.
- Tổng = 57.21s (|Δ|≤0.3s, đo ffprobe). STT lưu ý: "IEE PAMI"→**IEEE PAMI**, "ferret"→**FERET**.

## LÀM
Viết lại `release/scene_S03_pre_deeplearning.py`, render `manim -qh --disable_caching release/scene_S03_pre_deeplearning.py S03_PreDL`, đo ffprobe, mô tả ngắn + Δ rồi dừng chờ duyệt.
