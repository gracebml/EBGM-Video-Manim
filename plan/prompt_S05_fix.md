# 🤖 PROMPT cho CODEX — SỬA TIMING Scene 5 (S05 "Gabor wavelets")

> File: `release/scene_S05_gabor.py` (class `S05_Gabor`).
> **CHỈ sửa timing/đồng bộ** (giữ ý tưởng hình đã làm: mặt thật, build wavelet, filter sweep, DC-free, CNN≈cortex). Không cần vẽ lại từ đầu.
> **Audio = `scene_05`, duration = 36.55s** → render xong `ffprobe` PHẢI cho `|Δ| ≤ 0.3s`.

---

## 1. LỖI HIỆN TẠI (nguyên nhân "thừa quá nhiều ở phần sau")

Đây **không phải lỗi nội dung** mà là **lỗi timing tích luỹ**:

- `beat_to(t)` tính `rt = max(0.2, t − elapsed)` rồi đặt `elapsed = t`. Nó **chỉ đúng nếu MỌI animation đi qua `beat_to`**.
- Nhưng B3–B5 dùng **hàng loạt `self.play(...)` thô** (line ~274–427) + **`self.wait(0.5)` cứng** (line 356) → **không cập nhật `elapsed`**.
- Hệ quả: các `self.play` thô tiêu thời gian thật (vd B3 sweep ≈ 10.6s), **sau đó** `beat_to(seg_end(T,k))` lại **chờ THÊM trọn vẹn `(seg_end − elapsed)`** vì `elapsed` vẫn đứng yên ở mốc segment trước → **nửa sau phình to, lệch hẳn transcript**.

**Tóm lại:** thời gian thật của B3/B4/B5 = (tổng `self.play` thô) **cộng** (cú `beat_to` cuối beat) → gấp đôi/ba ngân sách.

---

## 2. CÁCH SỬA (bắt buộc)

### 2.1 Thêm helper `play_t` cập nhật `elapsed`
Mọi animation tuần tự phải đi qua helper này (hoặc qua `beat_to(target, *anims)`):
```python
def play_t(run_time, *anims, **kw):
    nonlocal elapsed
    self.play(*anims, run_time=run_time, **kw)
    elapsed += run_time
```
- **Thay TẤT CẢ `self.play(...)` thô** trong B3–B5 bằng `play_t(rt, ...)` với `rt` cụ thể.
- **Xoá `self.wait(0.5)` cứng** (line 356) và mọi `self.wait` thô; nếu cần nghỉ thì để `beat_to` cuối beat tự hấp thụ phần dư.
- Cuối mỗi beat vẫn gọi `beat_to(seg_end(T, k))` — giờ nó chỉ chờ **phần dư nhỏ** (đúng như thiết kế).

### 2.2 Tôn trọng NGÂN SÁCH thời gian mỗi beat
Trong mỗi beat, **Σ run_time của các `play_t` ≤ ngân sách**; phần còn lại để `beat_to` hấp thụ. Ngân sách thật (giây) theo transcript:

| Beat | seg | từ → đến (s) | **Ngân sách** | Ghi chú |
|---|---|---|---|---|
| B0 | 0 | 0.00 → 4.22 | **4.22** | |
| B1 | 1 | 4.22 → 9.84 | **5.62** | |
| B2 | 2 | 9.84 → 15.88 | **6.04** | build wavelet |
| B3 | 3 | 15.88 → 22.30 | **6.42** | filter sweep — **PHẢI gọn lại** |
| B4 | 4 | 22.30 → 28.24 | **5.94** | DC-free |
| B5 | 5 | 28.24 → 36.06 | **7.82** | CNN ≈ cortex |

→ **Cắt bớt choreography cho khớp**, đặc biệt B3:
- B3 hiện ~10.6s phải rút về **≤ ~6.0s**: ví dụ chỉ sweep **2 hướng** (0° rồi 90°), mỗi sweep ~1.3s, transform ~0.6s, fade in/out gọn; bỏ bớt reset thừa. Hoặc giảm `run_time` từng sweep.
- B4: fade-in (~0.8) + write `− mean` (~0.6) + hội tụ bar (~1.2) → ~2.6s, còn lại `beat_to` hấp thụ.
- B5: fade-out cũ + LaggedStart filters + cortex + 1 nhịp pulse → tổng `play_t` ≤ ~5.5s, dư để `beat_to`.

### 2.3 always_redraw / updater
- `fg_bar = always_redraw(...)` và `filter_obj.add_updater(...)` ổn, nhưng phải `clear_updaters()` trước khi sang beat sau (đã có ở line 316–317 — giữ). Đảm bảo không để updater chạy nền gây lệch.

---

## 2bis. SỬA "ĐƯỜNG CHÉO" Ở B1 (raw pixels) — cho đẹp & rõ nghĩa

- `slash = Line(...)` (line ~158) là gạch coral cố ý phủ định "raw pixels", **nhưng một đường chéo đơn trông như vệt nhiễu/scribble**.
- Theo CLAUDE.md (Arrow & Overlap Conventions): dấu "rejected approach" phải là **`Cross(...)` slim**, không phải một gạch mơ hồ.
- **Thay `slash` bằng dấu ✗ gọn, sang:**
  ```python
  reject = Cross(raw_grid, color=ACCENT_CORAL, stroke_width=3.0).scale(0.92)
  ```
  - `Cross` ôm theo `raw_grid`, 2 nét đối xứng → đọc ngay là "loại bỏ", không lệch như đường chéo đơn.
  - (tuỳ chọn) thêm badge nhỏ `light-sensitive` (coral, scale 0.22) đặt **dưới** `raw pixels`, không đè lưới.
- Animate: `Create(reject)` thay cho `Create(slash)`; cập nhật mọi chỗ `FadeOut(slash)` → `FadeOut(reject)`.
- Giữ "pixels flashing erratically" (line 181–182) — đó là minh hoạ "nhạy sáng", hợp lý; chỉ cần để dấu ✗ chồng lên **sau** nhịp nhấp nháy.

---

## 2ter. THIẾT KẾ LẠI B5 — mạng tích chập 3D phóng to RỒI MỚI hiện edge (liền mạch)

> Ý của user: ở chỗ liên hệ với CNN, **trước khi hiện các edge filter**, hãy cho một **mạng tích chập 3D đẹp phóng to ra**, **rồi mới** "mở" ra thành các edge — nối liền mạch, không cắt cứng.

### Phong cách 3D (đồng bộ S03)
- Vẽ "3D" bằng **khối isometric polygon (3 mặt đổ bóng)**, **KHÔNG `Surface` mesh** (theo CLAUDE.md S03). Mỗi conv volume = một khối hộp isometric, gradient nhẹ, viền mảnh, glow nhẹ.
- Mạng: **input block → conv1 → conv2 (→ pool)** xếp theo chiều sâu, mũi tên `thin_arrow` (StealthTip) nối giữa các khối. Khối **pop lần lượt**, sau đó **cả mạng phóng to / đẩy về phía người xem** (`scale` + dịch nhẹ) → cảm giác "zoom in".

### Liền mạch: conv1 → edge filters
- **Không FadeOut rồi FadeIn**. Thay vào đó **zoom vào khối conv1**, rồi **`ReplacementTransform` mặt trước của conv1 → lưới 3×3 Gabor edge filters** (dùng `gabor_array` đã có) → grid "nở ra" từ chính khối conv1 (liền mạch).
- Nhãn `CNN first-layer filters` hiện cùng lúc grid mở ra.

### Sau đó: ≈ visual cortex
- Khi tới "visual cortex": hiện cột cortex/orientation (đã có) + `≈ visual cortex`, liên hệ với grid edge.

### TIMING — neo theo TỪ (seamless + khớp transcript)
B5 chạy từ `elapsed = seg_end(T,4) = 28.24` đến `seg_end(T,5) = 36.06` (**ngân sách 7.82s**). **Dùng `beat_to(word_start(T, "..."))` để tự đồng bộ vào lời** (không tính tay, không overrun):

| Mốc neo | ≈ giây | Hình |
|---|---|---|
| vào B5 (sau DC-free) | 28.24 | clear cụm B4; **build mạng tích chập 3D** (khối pop lần lượt). |
| `beat_to(word_start(T, "CNN"))` | ~30.94 | mạng đã dựng xong, **phóng to ra**; highlight khối **conv1** (first layer). |
| `beat_to(word_start(T, "edges"))` | ~31.66 | **zoom conv1 → ReplacementTransform thành lưới edge filters**; `CNN first-layer filters`. |
| `beat_to(word_start(T, "visual"))` | ~34.92 | hiện cột **visual cortex** + `≈ visual cortex`. |
| `beat_to(seg_end(T, 5))` | 36.06 | hấp thụ phần dư; 1 nhịp pulse nhẹ liên hệ grid↔cortex (nếu còn thời gian). |

- Mỗi `beat_to(...)` chứa luôn animation của nhịp đó → thời lượng tự khít, `elapsed` luôn đúng.
- Nếu một số từ không tách chuẩn (vd "edges" dính dấu phẩy), `word_start` vẫn khớp theo substring; phòng hờ có thể fallback sang mốc giây ở bảng.

---

## 3. NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S05_gabor.py
rg -n "self\.play\(|self\.wait\(" video-2-ebgm/release/scene_S05_gabor.py
#   → trong B3–B5 KHÔNG còn self.play/self.wait thô (chỉ qua play_t/beat_to);
#     self.wait chỉ còn ở cú tail cuối cùng.
```
Render rồi đo:
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S05_Gabor.mp4
```

Checklist:
- [ ] Thêm `play_t` cập nhật `elapsed`; mọi `self.play` thô B3–B5 đổi sang `play_t`.
- [ ] Xoá `self.wait(0.5)` cứng và mọi wait thô; tail cuối vẫn giữ.
- [ ] Mỗi beat: Σ run_time ≤ ngân sách (bảng trên); B3 rút gọn còn ~6s.
- [ ] B1: thay `slash` bằng `Cross` slim (dấu ✗ gọn).
- [ ] B5: có **mạng tích chập 3D isometric phóng to** rồi mới `ReplacementTransform` conv1 → edge filters (liền mạch), neo theo `word_start` ("CNN"/"edges"/"visual").
- [ ] **`|Δ| ≤ 0.3s` so với 36.55s**; mỗi sự kiện vẫn rơi đúng segment; English-only; palette; `-qh` OK.
