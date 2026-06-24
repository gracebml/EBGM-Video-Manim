"""
EBGM Video — Part 4: Discussion (FINAL PART)
Scene 29: Feature-based (EBGM) vs Template-based (PCA/Eigenfaces)
Thời lượng dự kiến: 45s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - Be Vietnam Pro:  https://fonts.google.com/specimen/Be+Vietnam+Pro
  - EB Garamond:     https://fonts.google.com/specimen/EB+Garamond
  - JetBrains Mono:  https://fonts.google.com/specimen/JetBrains+Mono

Render command:
  manim -pql scene_29_vs_template.py Scene29_VsTemplate
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
# FRONT SILHOUETTE GENERATOR
# ============================================================
def make_frontal_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt chính diện (Frontal)."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    eye_l = Dot(head.get_center() + LEFT * 0.18 + UP * 0.1, radius=0.04, color=color)
    eye_r = Dot(head.get_center() + RIGHT * 0.18 + UP * 0.1, radius=0.04, color=color)
    mouth = Arc(radius=0.12, start_angle=-5*PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.18)
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, mouth, shoulders).scale(scale)


def make_vs_card(title_left, title_right, color_left, color_right, scale=1.0):
    """Card so sánh 'X vs Y': 2 panel cạnh nhau với divider 'VS' ở giữa."""
    panel_l = RoundedRectangle(
        width=5.0, height=4.2, corner_radius=0.15,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.6,
        stroke_color=color_left, stroke_width=1.8
    ).shift(LEFT * 3.3 + DOWN * 0.2)
    
    panel_r = RoundedRectangle(
        width=5.0, height=4.2, corner_radius=0.15,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.6,
        stroke_color=color_right, stroke_width=1.8
    ).shift(RIGHT * 3.3 + DOWN * 0.2)
    
    lbl_l = vn_tex_bold(title_left, color=color_left, scale=0.44).move_to(panel_l.get_top() + DOWN * 0.4)
    lbl_r = vn_tex_bold(title_right, color=color_right, scale=0.44).move_to(panel_r.get_top() + DOWN * 0.4)
    
    vs = vn_tex_bold("VS", color=TEXT_MUTED, scale=0.7).move_to(DOWN * 0.2)
    return VGroup(panel_l, panel_r, lbl_l, lbl_r, vs).scale(scale)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene29_VsTemplate(Scene):
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
        # PHASE A: Setup tiêu đề & vs-card (0s - 10s)
        # ============================================================
        sub_1 = make_subtitle("So sánh hai triết lý thiết kế đối nghịch trong nhận diện khuôn mặt")
        self.current_sub = sub_1
        self.play(FadeIn(sub_1, shift=UP * 0.15), run_time=0.4)

        # Tiêu đề
        title = vn_tex_bold("Feature-Based vs Template-Based", color=ACCENT_LAVENDER, scale=0.8)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # vs-card
        vs_card = make_vs_card("TEMPLATE-BASED (PCA)", "FEATURE-BASED (EBGM)", PREV_COLOR, EBGM_BRAND, scale=0.95)
        self.play(FadeIn(vs_card), run_time=1.2)
        self.wait(7.6) # Wait out 10s total

        # ============================================================
        # PHASE B: So sánh động (10s - 35s)
        # ============================================================
        sub_2 = make_subtitle("Template-based xem khuôn mặt là một vector pixel lớn toàn cục")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # 1. Panel Trái (PCA / Template-based)
        center_l = vs_card[0].get_center() + DOWN * 0.2
        face_l = make_frontal_silhouette(color=TEXT_MUTED, scale=0.75).move_to(center_l)
        
        # Dense pixel grid covering the face
        pixel_grid_l = NumberPlane(
            x_range=[-0.6, 0.6, 0.15], y_range=[-0.7, 0.7, 0.15],
            background_line_style={"stroke_color": PREV_COLOR, "stroke_width": 0.8, "stroke_opacity": 0.4}
        ).scale(0.8).move_to(center_l)

        lbl_desc_l = vn_tex("Lưu toàn bộ Vector Pixel", color=TEXT_MUTED, scale=0.3).next_to(vs_card[0], DOWN, buff=-0.7)

        self.play(FadeIn(face_l), Create(pixel_grid_l), run_time=1.2)
        self.play(FadeIn(lbl_desc_l, shift=UP*0.1), run_time=0.6)
        self.wait(1.5)

        # 2. Panel Phải (EBGM / Feature-based)
        sub_3 = make_subtitle("Feature-based chỉ trích xuất thông tin tại các điểm mốc chính")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        center_r = vs_card[1].get_center() + DOWN * 0.2
        face_r = make_frontal_silhouette(color=TEXT_MUTED, scale=0.75).move_to(center_r)
        
        # Landmark points
        node_positions = [
            center_r + LEFT * 0.14 + UP * 0.08,  # mắt trái
            center_r + RIGHT * 0.14 + UP * 0.08, # mắt phải
            center_r + DOWN * 0.05,              # mũi
            center_r + DOWN * 0.16               # miệng
        ]
        dots_r = VGroup(*[Dot(pos, radius=0.08, color=ACCENT_MINT) for pos in node_positions])
        lbl_desc_r = vn_tex("Chỉ lưu tại các điểm mốc", color=ACCENT_MINT, scale=0.3).next_to(vs_card[1], DOWN, buff=-0.7)

        self.play(FadeIn(face_r), FadeIn(dots_r, shift=DOWN*0.15), run_time=1.2)
        self.play(FadeIn(lbl_desc_r, shift=UP*0.1), run_time=0.6)
        self.wait(1.5)

        # 3. Thử thách thay đổi local (Kính mắt xuất hiện)
        sub_4 = make_subtitle("Khi có kính hoặc râu xuất hiện, toàn bộ vector của PCA bị thay đổi màu đỏ")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4

        # Kính mắt Panel Trái
        glasses_l = VGroup(
            Circle(radius=0.14, color=ACCENT_CORAL, stroke_width=2.5).move_to(center_l + LEFT * 0.15 + UP * 0.06),
            Circle(radius=0.14, color=ACCENT_CORAL, stroke_width=2.5).move_to(center_l + RIGHT * 0.15 + UP * 0.06),
            Line(center_l + LEFT * 0.01 + UP * 0.06, center_l + RIGHT * 0.01 + UP * 0.06, color=ACCENT_CORAL, stroke_width=2.5)
        )
        # Kính mắt Panel Phải
        glasses_r = VGroup(
            Circle(radius=0.14, color=ACCENT_CYAN, stroke_width=2.5).move_to(center_r + LEFT * 0.15 + UP * 0.06),
            Circle(radius=0.14, color=ACCENT_CYAN, stroke_width=2.5).move_to(center_r + RIGHT * 0.15 + UP * 0.06),
            Line(center_r + LEFT * 0.01 + UP * 0.06, center_r + RIGHT * 0.01 + UP * 0.06, color=ACCENT_CYAN, stroke_width=2.5)
        )

        # Trực quan hóa Lades/PCA lỗi toàn cục
        red_flash_grid = NumberPlane(
            x_range=[-0.6, 0.6, 0.15], y_range=[-0.7, 0.7, 0.15],
            background_line_style={"stroke_color": ACCENT_CORAL, "stroke_width": 1.2, "stroke_opacity": 0.8}
        ).scale(0.8).move_to(center_l)
        
        lbl_err_l = vn_tex("Mismatch toàn bộ Vector!", color=ACCENT_CORAL, scale=0.28).next_to(lbl_desc_l, DOWN, buff=0.1)

        self.play(FadeIn(glasses_l), run_time=0.6)
        self.play(
            ReplacementTransform(pixel_grid_l, red_flash_grid),
            FadeIn(lbl_err_l, shift=UP*0.1),
            run_time=1.0
        )
        self.play(Flash(center_l, color=ACCENT_CORAL, flash_radius=0.8), run_time=0.6)
        self.wait(1.0)

        # Trực quan hóa EBGM bám trụ vững vàng
        sub_5 = make_subtitle("Trong khi EBGM chỉ quan tâm đến các điểm mốc, bỏ qua vùng khác")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5

        lbl_ok_r = vn_tex("Vẫn match tốt tại các điểm mốc!", color=ACCENT_MINT, scale=0.28).next_to(lbl_desc_r, DOWN, buff=0.1)

        self.play(FadeIn(glasses_r), run_time=0.6)
        self.play(Indicate(dots_r, color=ACCENT_MINT), FadeIn(lbl_ok_r, shift=UP*0.1), run_time=1.0)
        self.play(Flash(center_r, color=ACCENT_MINT, flash_radius=0.8), run_time=0.6)
        self.wait(2.2) # Wait out 35s total

        # Clean Phase B for Phase C
        self.play(
            FadeOut(face_l), FadeOut(red_flash_grid), FadeOut(glasses_l), FadeOut(lbl_desc_l), FadeOut(lbl_err_l),
            FadeOut(face_r), FadeOut(dots_r), FadeOut(glasses_r), FadeOut(lbl_desc_r), FadeOut(lbl_ok_r),
            run_time=0.6
        )

        # ============================================================
        # PHASE C: Tổng kết (35s - 45s)
        # ============================================================
        sub_6 = make_subtitle("Bảng so sánh triết lý Feature-based vs Template-based")
        self.play(ReplacementTransform(self.current_sub, sub_6), run_time=0.4)
        self.current_sub = sub_6

        # Summary Table in center
        table_y = [0.8, 0.2, -0.4, -1.0]
        table_x = [-3.8, -0.6, 2.8]

        th_crit = vn_tex_bold("Tiêu chí so sánh", color=ACCENT_CYAN, scale=0.38).move_to(np.array([table_x[0], table_y[0], 0]))
        th_template = vn_tex_bold("Template-based (PCA)", color=PREV_COLOR, scale=0.38).move_to(np.array([table_x[1], table_y[0], 0]))
        th_feature = vn_tex_bold("Feature-based (EBGM)", color=ACCENT_LAVENDER, scale=0.38).move_to(np.array([table_x[2], table_y[0], 0]))
        
        row1_crit = vn_tex("Dữ liệu lưu trữ", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([table_x[0], table_y[1], 0]))
        row1_temp = vn_tex("Toàn bộ ảnh (Pixel)", color=TEXT_MUTED, scale=0.32).move_to(np.array([table_x[1], table_y[1], 0]))
        row1_feat = vn_tex("Chỉ các điểm mốc", color=ACCENT_MINT, scale=0.32).move_to(np.array([table_x[2], table_y[1], 0]))

        row2_crit = vn_tex("Độ nhạy local (kính/râu)", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([table_x[0], table_y[2], 0]))
        row2_temp = vn_tex("Rất cao (Dễ sai lệch)", color=TEXT_MUTED, scale=0.32).move_to(np.array([table_x[1], table_y[2], 0]))
        row2_feat = vn_tex("Thấp (Bỏ qua nhiễu)", color=ACCENT_MINT, scale=0.32).move_to(np.array([table_x[2], table_y[2], 0]))

        row3_crit = vn_tex("Yêu cầu căn chỉnh", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([table_x[0], table_y[3], 0]))
        row3_temp = vn_tex("Cực kỳ khắt khe", color=TEXT_MUTED, scale=0.32).move_to(np.array([table_x[1], table_y[3], 0]))
        row3_feat = vn_tex("Tự động thích nghi lưới", color=ACCENT_MINT, scale=0.32).move_to(np.array([table_x[2], table_y[3], 0]))

        table_lines = VGroup(
            Line(np.array([-5.2, 0.5, 0]), np.array([4.2, 0.5, 0]), color=TEXT_MUTED, stroke_width=0.8).set_opacity(0.4),
            Line(np.array([-5.2, -0.1, 0]), np.array([4.2, -0.1, 0]), color=TEXT_MUTED, stroke_width=0.8).set_opacity(0.4),
            Line(np.array([-5.2, -0.7, 0]), np.array([4.2, -0.7, 0]), color=TEXT_MUTED, stroke_width=0.8).set_opacity(0.4)
        )

        table_group = VGroup(
            th_crit, th_template, th_feature,
            row1_crit, row1_temp, row1_feat,
            row2_crit, row2_temp, row2_feat,
            row3_crit, row3_temp, row3_feat,
            table_lines
        )

        self.play(FadeOut(vs_card), FadeIn(table_group, shift=UP*0.2), run_time=1.2)
        self.wait(5.0) # Wait out 45s total

        # ============================================================
        # CLEANUP
        # ============================================================
        self.play(
            FadeOut(title),
            FadeOut(table_group),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
