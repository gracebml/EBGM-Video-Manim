# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 7 (S07 "Two similarity functions")

> File: `release/scene_S07_similarity.py` (class `S07_Similarity`).
> Thiết kế lại **toàn bộ** phần hình. **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX (`en_label`, `MathTex`/`Tex` + `EN_TEX_TEMPLATE`), palette `_common.py`, tổng thời lượng khớp audio.
> **Audio = `scene_07`, duration = 36.55s** → render xong `ffprobe` phải cho `|Δ| ≤ 0.3s`.
> Chạy trong env `vid`, render kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa)

Bản hiện tại đã đúng ý nghĩa nhưng **xấu và rối** ở phần 3D:

1. **Mặt cong 3D dùng `checkerboard_colors`** (ô vuông cyan/teal xen kẽ) + `stroke` lưới → trông lốm đốm, không "sang", đọc không ra hình lòng chảo / đỉnh nhọn.
2. **`Arrow3D(... height, base_radius)`** ở beat "points the way" = **mũi tên hình nón/tam giác cục mịch** đâm vào lòng chảo → đúng cái user phàn nàn. **BỎ.**
3. `Sphere` bi lăn + `eye_marker` là vòng tròn trơ → không gợi được "trượt về phía con mắt".
4. Hai mặt cong (basin ↔ sharp) hiện lên rời rạc, người xem **không thấy được tương phản "rộng & nông" vs "hẹp & nhọn"** một cách trực tiếp.

**Mục tiêu:** đường nét sạch – sắc – sang như **Scene 02**; hình 3D rõ ràng có chủ đích; tuyệt đối không mũi tên nón 3D.

---

## 2. Ý NGHĨA SCENE (phải truyền tải thật rõ)

Hai jet (model jet `J` và image jet `J'`) — **làm sao máy biết chúng khớp?** EBGM dùng **2 hàm tương đồng phối hợp nhịp nhàng**:

| Hàm | Công thức | Hình dạng "địa hình" tương đồng | Vai trò |
|---|---|---|---|
| `S_a` — **amplitude only** (bỏ phase) | `S_a = Σ aⱼa'ⱼ / √(Σaⱼ² · Σa'ⱼ²)` | **Lòng chảo rộng, nông, trơn** (wide attractor) | **COARSE**: bắt tín hiệu từ xa, trượt dần về đáy (con mắt) — *capture range lớn* |
| `S_φ` — **with phase** | `S_φ = Σ aⱼa'ⱼ cos(φⱼ − φ'ⱼ − d·kⱼ) / √(…)` | **Đỉnh nhọn, hẹp, dốc** (razor peak) | **FINE**: cực nhạy với dịch chuyển nhỏ → định vị **sub-pixel**; hơn nữa **chỉ hướng** — ước lượng vector dịch `d` (đi bao xa, hướng nào) |

Thông điệp 1 câu: *amplitude lo phần "đến gần", phase lo phần "đặt đúng chỗ chính xác và chỉ đường".*

---

## 3. NGUYÊN TẮC HÌNH (sửa đúng phàn nàn của user)

### 3.1 Hình 3D phải "sắc và sang"
- **BỎ `checkerboard_colors`.** Mặt cong tô **một màu gradient mượt** + `fill_opacity` thấp (≈0.5–0.6), `stroke_width` rất mảnh hoặc 0.
  - `S_a` basin: gradient theo độ cao (đáy `ACCENT_CYAN` → vành `ACCENT_TEAL`), dùng `set_fill_by_value`/`set_color_by_gradient` hoặc tự nội suy theo `z`.
  - `S_φ` peak: tông `ACCENT_LAVENDER`.
- **Thêm contour rings** (đường đồng mức): vài `ParametricFunction`/`Circle` ở các mức `z` cố định, stroke mảnh (~1.0), màu sáng hơn nền — đây là thứ làm địa hình **đọc ra ngay** (rộng-nông vs hẹp-nhọn) mà không cần xoay camera.
- **Tăng `resolution`** (≥ (28,28)) cho mặt mượt. **Camera đứng yên** (không `begin_ambient_camera_rotation`), một góc nghiêng nhẹ cố định.
- **2.5D, không 3D rối:** mặt cong vẽ trong không gian 3D, nhưng **mọi nhãn / chip / mũi tên / crosshair = `add_fixed_in_frame_mobjects` (2D phẳng, nét StealthTip)** — không bao giờ chữ 3D nghiêng méo.

### 3.2 Thêm "lát cắt 2D" làm mỏ neo đọc hiểu (giống Scene 02)
Song song với mặt 3D, vẽ **cross-section profile 2D** (trục `x = displacement` ngang, `y = similarity` dọc) đặt cố định 1 góc khung:
- `S_a`: đường cong **bướu rộng, thoải** (Gaussian bè).
- `S_φ`: đường cong **gai cao, hẹp**.
- Đây là nơi cho **viên bi trượt** và cho **mũi tên dịch chuyển** chạy → sạch, không cần nón 3D. Lát cắt 2D chính là phần "đường nét sang như scene 02".

> Gợi ý bố cục: mặt 3D lớn bên trái/giữa làm "wow", lát cắt 2D nhỏ-rõ bên phải làm "đọc hiểu". Hoặc dùng lát cắt 2D làm chủ đạo, 3D chỉ là establishing shot ngắn — chọn cách nào sạch hơn khi render.

### 3.3 Mũi tên & chống chồng lấp (theo CLAUDE.md)
- **"points the way" / "how far to move":** dùng **`thin_arrow(...)` (StealthTip)** trên lát cắt 2D hoặc fixed-in-frame, hoặc `thin_curved_arrow` men theo mặt — **TUYỆT ĐỐI không `Arrow3D`/nón**.
- Nhãn `match?` (B0): hai mũi tên hội tụ phải **dừng cách chữ một khoảng rõ** (canh `get_left()/get_right()` + margin), đầu mũi không chạm chữ.
- Mỗi beat **một tiêu điểm**; fade/dim cái cũ trước khi đưa cái mới vào. Chip nhãn (`COARSE`, `sub-pixel`) đặt góc, không đè lên địa hình.

---

## 4. STORYBOARD — map đúng segment của `transcript.json` (scene_07)

Lấy mốc bằng `seg_end(T, k)`. (Các mốc dưới là `end` mỗi segment, để tra cứu — **đừng hardcode, đọc từ `T`**.)

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →2.52 | "With two jets, how does the machine know they match?" | 2 jet bundle (style `mini_jet`/S06): trái `J` cyan, phải `J'` lavender. Hai `thin_arrow` hội tụ vào giữa, nhãn lớn **`match?`** (cách mũi tên rõ). 2D thuần. |
| **B1** | 1 | →6.54 | "pairs two similarity functions in beautiful harmony" | Hai **card công thức** trượt vào: `S_a` (amplitude only, cyan) & `S_φ` (with phase, lavender). Caption nhỏ `coarse first · precise second`. |
| **B2** | 2 | →10.12 | "The first compares only amplitude, ignoring phase" | Focus card `S_a`: hiện đầy công thức `S_a = Σaⱼa'ⱼ/√(…)`. Icon nhỏ: **các thanh amplitude giữ lại**, **đồng hồ phase bị gạch chéo** (`ignoring phase`). Dim card `S_φ`. |
| **B3** | 3 | →14.42 | "Picture it forming a smooth basin, a wide attractor" | Chuyển sang địa hình. Hiện **LÒNG CHẢO rộng-nông** (3D gradient mượt + contour rings) **và** lát cắt 2D bướu rộng. Nhãn `smooth basin · wide attractor`. |
| **B4** | 4 | →18.44 | "catch a signal from afar and slide toward the eye" | Marker bắt đầu **ở xa trên vành**, **trượt mượt xuống đáy**. Đáy = **con mắt** (crop `assets/s7_eye.png` hoặc eye-marker sạch). Trượt chạy đồng thời trên cả mặt 3D lẫn lát cắt 2D. |
| **B5** | 5 | →20.38 | "This is the coarse step" | Chip **`COARSE`** (mint). Marker dừng **gần đáy nhưng chưa chính xác**. Vẽ **bracket "capture range"** rộng để nhấn "bắt được từ xa". |
| **B6** | 6 | →24.34 | "Once very close, the second function with phase kicks in" | Zoom/đổi sang `S_φ`. Công thức phase hiện. Địa hình **morph lòng chảo → đỉnh nhọn** (lavender). |
| **B7** | 7 | →28.02 | "razor sharp, sensitive to the tiniest shift" | **ĐỈNH NHỌN hẹp-dốc** rõ (3D + lát cắt gai cao). Minh hoạ **dịch nhỏ → tụt similarity mạnh** (marker nhích ngang một chút, y rớt sâu). Nhãn `razor sharp`. |
| **B8** | 8 | →31.22 | "pinning the exact position with sub-pixel accuracy" | **Crosshair (Stealth/`Cross` mảnh)** ghim đúng đỉnh. Chip `sub-pixel accuracy`. Có thể chèn lưới nhỏ với target nằm **giữa 2 ô** (sub-pixel). |
| **B9** | 9 | →33.74 | "Better still, it points the way" | Phase cho **hướng dịch**: `thin_arrow` 2D từ vị trí jet hiện tại → đỉnh thật (KHÔNG nón 3D). Nhãn `points the way` + ký hiệu vector `d`. |
| **B10** | 10 | →36.12 | "It tells you how far to move the jet" | Hiện **độ lớn**: nhãn chiều dài trên mũi tên + jet **nhảy** từ vị trí cũ sang đúng vị trí (focus snap vào con mắt). Nhãn `move the jet · d = (Δx, Δy)`. Kết sạch. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 36.55s.

---

## 5. ẢNH CẦN CUNG CẤP (user sẽ thả vào `assets/`)

Scene này chủ yếu trừu tượng (toán/địa hình) → **không bắt buộc ảnh mới**. Chỉ **một ảnh tuỳ chọn** giúp beat B4 rõ nghĩa hơn:

- ✅ (tuỳ chọn, khuyến nghị) **`assets/s7_eye.png`** — ảnh **cận cảnh 1 con mắt** (vuông, ~512×512), nền tối/khử nền nhẹ để đặt làm "đáy lòng chảo" cho câu *"slide toward the eye"*. Nếu không có → crop vùng mắt từ `assets/face.png` lúc runtime, hoặc **eye-marker vẽ tay sạch** (ellipse + iris + highlight), KHÔNG hình cầu trơ.
- Đã có sẵn, dùng trực tiếp nếu cần ground "khuôn mặt mục tiêu": `assets/face.png`.

Tham chiếu: `base = Path(__file__).resolve().parents[1] / "assets"`. Có helper kiểm tra tồn tại để **luôn render được** kể cả khi ảnh chưa có.

---

## 6. CÔNG THỨC (LaTeX, đúng theo paper EBGM)

```latex
S_a(\mathcal{J},\mathcal{J}') = \frac{\sum_j a_j a'_j}{\sqrt{\sum_j a_j^2 \,\sum_j a_j'^2}}

S_\phi(\mathcal{J},\mathcal{J}') = \frac{\sum_j a_j a'_j \cos(\phi_j - \phi'_j - \vec{d}\cdot \vec{k}_j)}{\sqrt{\sum_j a_j^2 \,\sum_j a_j'^2}}
```
- `S_a`: cyan; `S_φ`: lavender. Highlight cụm `\cos(\phi_j-\phi'_j-\vec d\cdot\vec k_j)` khi nói "phase kicks in".

---

## 7. KIỂM TRA TRƯỚC KHI RENDER

```bash
python3 -m py_compile video-2-ebgm/release/scene_S07_similarity.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S07_similarity.py   # phải rỗng
rg -n "Arrow3D|checkerboard_colors|begin_ambient_camera_rotation" video-2-ebgm/release/scene_S07_similarity.py  # phải rỗng
```
Sau render:
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S07_Similarity.mp4   # |Δ| ≤ 0.3s so với 36.55
```

## 8. CHECKLIST NGHIỆM THU
- [ ] Không còn `Arrow3D`/nón tam giác; mũi tên đều StealthTip mảnh, dừng cách chữ rõ.
- [ ] Mặt 3D không còn checkerboard; gradient mượt + contour rings, đọc ra "rộng-nông" vs "hẹp-nhọn".
- [ ] Có lát cắt 2D đồng bộ (đường nét sạch như Scene 02).
- [ ] `match?` không bị mũi tên chạm; mỗi beat một tiêu điểm, không chồng lấp.
- [ ] Marker "trượt về con mắt" rõ nghĩa; chip `COARSE`/`sub-pixel` đặt góc gọn.
- [ ] Mọi event hình rơi đúng segment; tổng khớp 36.55s (|Δ|≤0.3s).
- [ ] English-only, palette `_common.py`, render `-qh` ra mp4 thành công.
