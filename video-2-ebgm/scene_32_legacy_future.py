"""
EBGM Video — Part 4: Discussion (FINAL PART)
Scene 32: Legacy & Future
Thời lượng dự kiến: 55s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - Be Vietnam Pro:  https://fonts.google.com/specimen/Be+Vietnam+Pro
  - EB Garamond:     https://fonts.google.com/specimen/EB+Garamond
  - JetBrains Mono:  https://fonts.google.com/specimen/JetBrains+Mono

Render command:
  manim -pql scene_32_legacy_future.py Scene32_LegacyFuture
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
FUTURE_GLOW     = "#B8B5FF"

SUBTITLE_FONT = "Be Vietnam Pro"
TITLE_FONT    = "EB Garamond"
MONO_FONT     = "JetBrains Mono"

# ============================================================
# HELPERS (Bổ sung đầy đủ cho phần 4)
# ============================================================
def future_node(text_str, icon_mob, color=FUTURE_GLOW, scale=1.0):
    """Node cho roadmap: icon + text trong rounded box."""
    box = RoundedRectangle(
        width=3.4, height=1.4, corner_radius=0.12,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.8,
        stroke_color=color, stroke_width=1.8
    )
    # Convert newlines to LaTeX line breaks inside a tabular to maintain pure LaTeX font
    tex_str = r"\begin{tabular}{l} " + text_str.replace("\n", r" \\ ") + r" \end{tabular}"
    txt = vn_tex(tex_str, color=TEXT_PRIMARY, scale=0.38)
    icon_mob.scale(0.85).move_to(box.get_left() + RIGHT * 0.5)
    txt.next_to(icon_mob, RIGHT, buff=0.2)
    return VGroup(box, icon_mob, txt).scale(scale)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene32_LegacyFuture(Scene):
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
        # PHASE A: Setup tiêu đề & roadmap structure (0s - 10s)
        # ============================================================
        sub_1 = make_subtitle("EBGM để lại di sản sâu sắc và mở đường cho công nghệ tương lai")
        self.current_sub = sub_1
        self.play(FadeIn(sub_1, shift=UP * 0.15), run_time=0.4)

        # Tiêu đề chính
        title = vn_tex_bold("Legacy \\& Future --- Bước Đệm Tương Lai", color=ACCENT_LAVENDER, scale=0.8)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.wait(8.8) # Wait out 10s total

        # ============================================================
        # PHASE B: 3 Nodes Roadmap (10s - 45s)
        # ============================================================
        
        # 1. Node 1: Landmark Detection
        sub_2 = make_subtitle("Đầu tiên: EBGM là phương pháp tiên phong đặt nền móng cho Landmark Detection")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # Icon 1: Silhouette khuôn mặt nhỏ với 4 mốc mắt, mũi, miệng phát sáng
        face_head = Circle(radius=0.22, color=TEXT_MUTED, stroke_width=1.2)
        dots = VGroup(
            Dot(face_head.get_center() + LEFT*0.07 + UP*0.05, radius=0.024, color=ACCENT_MINT),
            Dot(face_head.get_center() + RIGHT*0.07 + UP*0.05, radius=0.024, color=ACCENT_MINT),
            Dot(face_head.get_center() + DOWN*0.02, radius=0.018, color=ACCENT_MINT),
            Dot(face_head.get_center() + DOWN*0.09, radius=0.018, color=ACCENT_MINT),
        )
        icon_1 = VGroup(face_head, dots)
        node_1 = future_node("Pioneering\nLandmarks", icon_1, color=ACCENT_CYAN, scale=1.0)
        node_1.move_to(LEFT * 4.4 + UP * 0.2)

        self.play(FadeIn(node_1, shift=RIGHT * 0.3), run_time=1.0)
        self.play(Flash(dots.get_center(), color=ACCENT_MINT, flash_radius=0.4), run_time=0.6)
        self.wait(10.0) # Wait out 22s total

        # 2. Node 2: Khái niệm "Bunch"
        sub_3 = make_subtitle("Thứ hai: khái niệm 'Bunch' mở đường cho việc lưu trữ đa dạng đặc trưng")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        # Icon 2: Một 'bó' gồm 3 grids nhỏ xếp chồng đè nhẹ lên nhau
        icon_2 = VGroup()
        for idx in range(3):
            rect = RoundedRectangle(width=0.35, height=0.45, corner_radius=0.03, stroke_color=ACCENT_LAVENDER, stroke_width=1.0, fill_color=BG_NAVY_SOFT, fill_opacity=0.8)
            rect.shift(UP * 0.05 * idx + RIGHT * 0.05 * idx)
            icon_2.add(rect)
        icon_2.move_to(ORIGIN)

        node_2 = future_node("Bunch Concept\n(Multi-features)", icon_2, color=ACCENT_LAVENDER, scale=1.0)
        node_2.move_to(UP * 0.2)

        # Nối node 1 và node 2
        arrow_1_2 = DashedLine(node_1.get_right(), node_2.get_left(), color=ACCENT_BLUE, stroke_width=1.8)

        self.play(Create(arrow_1_2), run_time=0.8)
        self.play(FadeIn(node_2, shift=RIGHT * 0.3), run_time=1.0)
        self.play(Indicate(icon_2, color=ACCENT_LAVENDER), run_time=0.8)
        self.wait(9.4) # Wait out 34s total

        # 3. Node 3: Bước đệm Neural Networks
        sub_4 = make_subtitle("Cuối cùng: EBGM là bước đệm tư duy trực tiếp cho mạng nơ-ron học sâu ngày nay")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4

        # Icon 3: Biểu tượng mạng nơ-ron nhỏ (3 input nối 2 output)
        in1 = Dot([-0.18, 0.14, 0], radius=0.035, color=ACCENT_CORAL)
        in2 = Dot([-0.18, -0.14, 0], radius=0.035, color=ACCENT_CORAL)
        out1 = Dot([0.18, 0.0, 0], radius=0.035, color=ACCENT_MINT)
        l1 = Line(in1.get_center(), out1.get_center(), color=TEXT_MUTED, stroke_width=1.0)
        l2 = Line(in2.get_center(), out1.get_center(), color=TEXT_MUTED, stroke_width=1.0)
        icon_3 = VGroup(l1, l2, in1, in2, out1)

        node_3 = future_node("Stepping Stone\nto Deep Learning", icon_3, color=ACCENT_TEAL, scale=1.0)
        node_3.move_to(RIGHT * 4.4 + UP * 0.2)

        # Nối node 2 và node 3
        arrow_2_3 = DashedLine(node_2.get_right(), node_3.get_left(), color=ACCENT_BLUE, stroke_width=1.8)

        self.play(Create(arrow_2_3), run_time=0.8)
        self.play(FadeIn(node_3, shift=RIGHT * 0.3), run_time=1.0)
        self.play(Indicate(icon_3, color=ACCENT_MINT), run_time=0.8)
        self.wait(8.4) # Wait out 45s total

        # ============================================================
        # PHASE C: Tổng kết di sản - Honest Note (45s - 55s)
        # ============================================================
        sub_5 = make_subtitle("EBGM vẫn giữ nguyên vẹn giá trị học thuật như một minh chứng rực rỡ")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5

        honest_note = vn_tex_italic(
            "(Dù đã bị thay thế bởi các mạng học sâu hiện đại, EBGM vẫn giữ nguyên vẹn giá trị học thuật là minh chứng rực rỡ nhất cho tư duy hình học chặt chẽ và logic toán học thuần túy)",
            color=TEXT_MUTED, scale=0.34
        ).move_to(DOWN * 2.2)

        self.play(FadeIn(honest_note, shift=UP * 0.15), run_time=0.8)
        self.wait(8.8) # Wait out 55s total

        # ============================================================
        # CLEANUP
        # ============================================================
        self.play(
            FadeOut(title),
            FadeOut(node_1), FadeOut(node_2), FadeOut(node_3),
            FadeOut(arrow_1_2), FadeOut(arrow_2_3),
            FadeOut(honest_note),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
