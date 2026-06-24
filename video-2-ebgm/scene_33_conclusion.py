"""
EBGM Video — Part 4: Discussion (FINAL PART)
Scene 33: Conclusion
Thời lượng dự kiến: 30s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - Be Vietnam Pro:  https://fonts.google.com/specimen/Be+Vietnam+Pro
  - EB Garamond:     https://fonts.google.com/specimen/EB+Garamond
  - JetBrains Mono:  https://fonts.google.com/specimen/JetBrains+Mono

Render command:
  manim -pql scene_33_conclusion.py Scene33_Conclusion
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
# MAIN SCENE
# ============================================================
class Scene33_Conclusion(Scene):
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
        # PHASE A: Setup logo grid hữu cơ ở tâm (0s - 10s)
        # ============================================================
        sub_1 = make_subtitle("Chúng ta đã đi qua toàn bộ hành trình khám phá thuật toán EBGM")
        self.current_sub = sub_1
        self.play(FadeIn(sub_1, shift=UP * 0.15), run_time=0.4)

        # Tiêu đề chính
        title = vn_tex_bold("Conclusion --- Tổng Kết Hành Trình", color=ACCENT_LAVENDER, scale=0.8)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # Vẽ một Lưới Elastic Grid 3x3 hữu cơ tự thiết kế đẹp mắt
        # Sử dụng tọa độ hơi lệch ngẫu nhiên nhẹ để thể hiện tính chất "đàn hồi"
        nodes_pos = [
            [-0.55,  0.58, 0], [ 0.05,  0.62, 0], [ 0.58,  0.55, 0],
            [-0.62, -0.05, 0], [ 0.00,  0.00, 0], [ 0.65,  0.05, 0],
            [-0.58, -0.62, 0], [-0.05, -0.58, 0], [ 0.55, -0.58, 0]
        ]
        nodes_pos = [np.array(pos) * 1.5 for pos in nodes_pos]
        
        dots = VGroup(*[Dot(pos, radius=0.08, color=ACCENT_LAVENDER) for pos in nodes_pos])
        
        # Vẽ các đường kết nối lưới ngang và dọc
        lines = VGroup()
        connections = [
            (0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8),  # ngang
            (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8)   # dọc
        ]
        for start, end in connections:
            lines.add(Line(nodes_pos[start], nodes_pos[end], color=ACCENT_LAVENDER, stroke_width=1.8).set_opacity(0.6))

        logo_grid = VGroup(lines, dots)
        self.play(Create(lines), FadeIn(dots, scale=0.5), run_time=2.0)
        self.play(Indicate(logo_grid, color=ACCENT_LAVENDER), run_time=1.0)
        self.wait(5.8) # Wait out 10s total

        # ============================================================
        # PHASE B: 3 Dòng tóm tắt chuyển dịch logo sang trái (10s - 25s)
        # ============================================================
        sub_2 = make_subtitle("Tóm lại, EBGM kết hợp xuất sắc giữa Wavelet Jets toàn cục và cấu trúc lưới đàn hồi")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # Dịch logo_grid sang bên trái
        self.play(logo_grid.animate.scale(0.85).shift(LEFT * 3.8 + DOWN * 0.2), run_time=1.2)

        # 3 bullets bên phải
        bullets_y = [0.8, -0.1, -1.0]
        bullet_x = -0.5

        # Bullet 1
        b1_dot = Dot([bullet_x, bullets_y[0], 0], radius=0.06, color=ACCENT_CYAN)
        b1_txt = vn_tex("Kết hợp Wavelet Jets \\& Elastic Graph Matching", color=TEXT_PRIMARY, scale=0.4).next_to(b1_dot, RIGHT, buff=0.25)
        bullet_1 = VGroup(b1_dot, b1_txt)

        # Bullet 2
        b2_dot = Dot([bullet_x, bullets_y[1], 0], radius=0.06, color=ACCENT_MINT)
        b2_txt = vn_tex("Nhận diện đa tư thế hiệu quả không cần training", color=TEXT_PRIMARY, scale=0.4).next_to(b2_dot, RIGHT, buff=0.25)
        bullet_2 = VGroup(b2_dot, b2_txt)

        # Bullet 3
        b3_dot = Dot([bullet_x, bullets_y[2], 0], radius=0.06, color=ACCENT_LAVENDER)
        b3_txt = vn_tex("Mở ra kỷ nguyên nhận diện hình học có cấu trúc", color=TEXT_PRIMARY, scale=0.4).next_to(b3_dot, RIGHT, buff=0.25)
        bullet_3 = VGroup(b3_dot, b3_txt)

        self.play(FadeIn(bullet_1, shift=RIGHT * 0.25), run_time=0.8)
        self.wait(2.5)

        sub_3 = make_subtitle("Giúp giải quyết trọn vẹn bài toán nhận diện cùng lớp đối tượng với góc xoay nhỏ")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        self.play(FadeIn(bullet_2, shift=RIGHT * 0.25), run_time=0.8)
        self.wait(2.5)

        sub_4 = make_subtitle("Và để lại những tri thức nền tảng vô giá cho các hệ thống hiện đại")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4

        self.play(FadeIn(bullet_3, shift=RIGHT * 0.25), run_time=0.8)
        self.wait(3.3) # Wait out 25s total

        # ============================================================
        # PHASE C: Lời chào kết thúc (25s - 30s)
        # ============================================================
        sub_5 = make_subtitle("Cảm ơn các bạn đã đồng hành cùng hành trình khám phá này")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5

        # Thu nhỏ và dập tắt các chi tiết cũ
        self.play(
            FadeOut(logo_grid),
            FadeOut(bullet_1), FadeOut(bullet_2), FadeOut(bullet_3),
            run_time=0.8
        )

        # Text Cảm ơn chính giữa
        thank_you = vn_tex_bold("CẢM ƠN BẠN ĐÃ THEO DÕI!", color=EBGM_BRAND, scale=0.85).move_to(ORIGIN)

        self.play(FadeIn(thank_you, shift=UP*0.25), run_time=0.8)
        self.wait(2.5) # Wait out 30s total

        # ============================================================
        # CLEANUP
        # ============================================================
        self.play(
            FadeOut(title),
            FadeOut(thank_you),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
