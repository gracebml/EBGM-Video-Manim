"""
EBGM Video — Part 4: Discussion (FINAL PART)
Scene 31: Pros / Cons & Limits
Thời lượng dự kiến: 60s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - Be Vietnam Pro:  https://fonts.google.com/specimen/Be+Vietnam+Pro
  - EB Garamond:     https://fonts.google.com/specimen/EB+Garamond
  - JetBrains Mono:  https://fonts.google.com/specimen/JetBrains+Mono

Render command:
  manim -pql scene_31_pros_cons.py Scene31_ProsCons
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# COLOR PALETTE & FONTS (redeclare để standalone)
# ============================================================
BG_NAVY         = "#0D1B2A"
BG_NAVY_SOFT    = "#1B263B"
TEXT_PRIMARY    = "#E0E1DD"
TEXT_MUTED      = "#A9B4C2"
ACCENT_CYAN     = "#48CAE4"
ACCENT_TEAL     = "#76C5BF"
ACCENT_BLUE     = "#778DA9"
ACCENT_MINT     = "#95D5B2"
ACCENT_LAVENDER = "#B8B5FF"
ACCENT_CORAL    = "#E29578"
GRID_LINE       = "#778DA9"

EBGM_BRAND      = "#B8B5FF"
PREV_COLOR      = "#778DA9"
PRO_COLOR       = "#95D5B2"
CON_COLOR       = "#E29578"

SUBTITLE_FONT = "Be Vietnam Pro"
TITLE_FONT    = "EB Garamond"
MONO_FONT     = "JetBrains Mono"

# ============================================================
# HELPERS (Bổ sung đầy đủ cho phần 4)
# ============================================================
def pro_item(text_str, scale=0.45):
    """Dòng điểm mạnh với check icon mint (vẽ tay, KHÔNG emoji)."""
    check = VGroup(
        Line([-0.1, -0.02, 0], [-0.02, -0.1, 0], color=PRO_COLOR, stroke_width=3.5),
        Line([-0.02, -0.1, 0], [0.1, 0.08, 0], color=PRO_COLOR, stroke_width=3.5),
    )
    txt = vn_tex(text_str, color=TEXT_PRIMARY, scale=scale)
    return VGroup(check, txt).arrange(RIGHT, buff=0.25)


def con_item(text_str, scale=0.45):
    """Dòng điểm yếu với cross icon coral (vẽ tay, KHÔNG emoji)."""
    cross = VGroup(
        Line([-0.08, 0.08, 0], [0.08, -0.08, 0], color=CON_COLOR, stroke_width=3.5),
        Line([-0.08, -0.08, 0], [0.08, 0.08, 0], color=CON_COLOR, stroke_width=3.5),
    )
    txt = vn_tex(text_str, color=TEXT_PRIMARY, scale=scale)
    return VGroup(cross, txt).arrange(RIGHT, buff=0.25)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene31_ProsCons(Scene):
    def construct(self):
        self.camera.background_color = BG_NAVY

        # Setup subtitle tracking
        self.current_sub = None

        def update_sub(text_str, duration):
            new_sub = make_subtitle(text_str)
            if self.current_sub is None:
                self.play(FadeIn(new_sub, shift=UP * 0.15), run_time=0.4)
            else:
                self.play(ReplacementTransform(self.current_sub, new_sub), run_time=0.4)
            self.current_sub = new_sub
            self.wait(duration - 0.4)

        # ============================================================
        # PHASE A: Setup tiêu đề & khung chứa (0s - 10s)
        # ============================================================
        sub_1 = make_subtitle("Cái nhìn khách quan và đa chiều về thuật toán EBGM")
        self.current_sub = sub_1
        self.play(FadeIn(sub_1, shift=UP * 0.15), run_time=0.4)

        # Tiêu đề chính
        title = vn_tex_bold("Pros, Cons \\& Limits --- Nhìn Nhận Đa Chiều", color=ACCENT_LAVENDER, scale=0.8)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # Setup 2 panel bên cạnh nhau
        panel_l = RoundedRectangle(
            width=6.0, height=4.2, corner_radius=0.15,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.6,
            stroke_color=PRO_COLOR, stroke_width=1.8
        ).shift(LEFT * 3.3 + DOWN * 0.2)

        panel_r = RoundedRectangle(
            width=6.0, height=4.2, corner_radius=0.15,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.6,
            stroke_color=CON_COLOR, stroke_width=1.8
        ).shift(RIGHT * 3.3 + DOWN * 0.2)

        lbl_l = vn_tex_bold("ƯU THẾ (PROS)", color=PRO_COLOR, scale=0.55).move_to(panel_l.get_top() + DOWN * 0.4)
        lbl_r = vn_tex_bold("GIỚI HẠN (CONS)", color=CON_COLOR, scale=0.55).move_to(panel_r.get_top() + DOWN * 0.4)

        self.play(
            FadeIn(panel_l), FadeIn(panel_r),
            FadeIn(lbl_l), FadeIn(lbl_r),
            run_time=1.2
        )
        self.wait(7.6) # Wait out 10s total

        # ============================================================
        # PHASE B: Pros & Cons xuất hiện lần lượt (10s - 50s)
        # ============================================================
        sub_2 = make_subtitle("Ưu thế thứ nhất: không cần tập dữ liệu huấn luyện khổng lồ")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # 3 Pros items
        pro1 = pro_item("Không cần training dữ liệu lớn").move_to(panel_l.get_center() + UP * 0.6)
        pro2 = pro_item("Cực kỳ tiết kiệm bộ nhớ").move_to(panel_l.get_center())
        pro3 = pro_item("Robust với biến đổi local ngoài mốc").move_to(panel_l.get_center() + DOWN * 0.6)

        # Align text left inside VGroup for clean look
        for p in [pro1, pro2, pro3]:
            p.align_to(panel_l.get_left() + RIGHT * 0.4, LEFT)

        self.play(FadeIn(pro1, shift=RIGHT * 0.25), run_time=0.8)
        self.wait(1.5)

        sub_3 = make_subtitle("Ưu thế thứ hai: lưu trữ cực kỳ gọn nhẹ, chỉ giữ các vector điểm mốc")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        self.play(FadeIn(pro2, shift=RIGHT * 0.25), run_time=0.8)
        self.wait(1.5)

        sub_4 = make_subtitle("Ưu thế thứ ba: robust với thay đổi như đeo kính, râu hoặc biểu cảm")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4

        self.play(FadeIn(pro3, shift=RIGHT * 0.25), run_time=0.8)
        self.wait(1.5)

        # 3 Cons items
        sub_5 = make_subtitle("Giới hạn đầu tiên: độ chính xác giảm sút khi góc xoay đầu lớn hơn 22 độ")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5

        con1 = con_item("Độ chính xác giảm sâu khi xoay > $22^\\circ$").move_to(panel_r.get_center() + UP * 0.6)
        con2 = con_item("Dễ lỗi khi bị che khuất điểm mốc").move_to(panel_r.get_center())
        con3 = con_item("Độ phức tạp tăng khi có quá nhiều pose").move_to(panel_r.get_center() + DOWN * 0.6)

        # Align text left inside VGroup
        for c in [con1, con2, con3]:
            c.align_to(panel_r.get_left() + RIGHT * 0.4, LEFT)

        self.play(FadeIn(con1, shift=RIGHT * 0.25), run_time=0.8)
        self.wait(1.5)

        sub_6 = make_subtitle("Giới hạn thứ hai: dễ bị lỗi nếu các điểm mốc chính như mắt, mũi bị che khuất")
        self.play(ReplacementTransform(self.current_sub, sub_6), run_time=0.4)
        self.current_sub = sub_6

        self.play(FadeIn(con2, shift=RIGHT * 0.25), run_time=0.8)
        self.wait(1.5)

        sub_7 = make_subtitle("Giới hạn thứ ba: độ phức tạp tăng nhanh khi số lượng góc pose trong FBG tăng lên")
        self.play(ReplacementTransform(self.current_sub, sub_7), run_time=0.4)
        self.current_sub = sub_7

        self.play(FadeIn(con3, shift=RIGHT * 0.25), run_time=0.8)
        self.wait(2.2) # Wait out 50s total

        # ============================================================
        # PHASE C: Honest Note về kỷ nguyên Deep Learning (50s - 60s)
        # ============================================================
        sub_8 = make_subtitle("EBGM đại diện cho đỉnh cao của phương pháp trích xuất đặc trưng thủ công")
        self.play(ReplacementTransform(self.current_sub, sub_8), run_time=0.4)
        self.current_sub = sub_8

        honest_note = vn_tex_italic(
            "(Note: EBGM đại diện cho đỉnh cao của phương pháp thiết kế đặc trưng thủ công (Hand-crafted features) trước kỷ nguyên Deep Learning)",
            color=TEXT_MUTED, scale=0.34
        ).move_to(DOWN * 2.8)

        self.play(FadeIn(honest_note, shift=UP * 0.15), run_time=0.8)
        self.wait(8.8) # Wait out 60s total

        # ============================================================
        # CLEANUP
        # ============================================================
        self.play(
            FadeOut(title),
            FadeOut(panel_l), FadeOut(panel_r),
            FadeOut(lbl_l), FadeOut(lbl_r),
            FadeOut(pro1), FadeOut(pro2), FadeOut(pro3),
            FadeOut(con1), FadeOut(con2), FadeOut(con3),
            FadeOut(honest_note),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
