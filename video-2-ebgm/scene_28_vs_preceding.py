"""
EBGM Video — Part 4: Discussion (FINAL PART)
Scene 28: EBGM vs Preceding System (Lades, 1993)
Thời lượng dự kiến: 70s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - Be Vietnam Pro:  https://fonts.google.com/specimen/Be+Vietnam+Pro
  - EB Garamond:     https://fonts.google.com/specimen/EB+Garamond
  - JetBrains Mono:  https://fonts.google.com/specimen/JetBrains+Mono

Render command:
  manim -pql scene_28_vs_preceding.py Scene28_VsPreceding
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
# SILHOUETTE GENERATORS (Nhất quán 100% với Scene 20)
# ============================================================
def make_frontal_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt chính diện (Frontal)."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    eye_l = Dot(head.get_center() + LEFT * 0.18 + UP * 0.1, radius=0.04, color=color)
    eye_r = Dot(head.get_center() + RIGHT * 0.18 + UP * 0.1, radius=0.04, color=color)
    mouth = Arc(radius=0.12, start_angle=-5*PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.18)
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, mouth, shoulders).scale(scale)


def make_profile_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt nghiêng hẳn 90 độ (Profile)."""
    profile_line = VMobject(color=color, stroke_width=1.5)
    points = [
        np.array([0, 0.5, 0]),
        np.array([0.2, 0.4, 0]),
        np.array([0.3, 0.1, 0]),
        np.array([0.2, -0.3, 0]),
        np.array([-0.05, -0.6, 0]),
    ]
    profile_line.set_points_as_corners(points)
    
    face_line = VMobject(color=color, stroke_width=1.5)
    face_points = [
        np.array([0, 0.5, 0]),
        np.array([-0.18, 0.35, 0]),
        np.array([-0.2, 0.15, 0]),
        np.array([-0.42, 0.05, 0]),
        np.array([-0.22, -0.08, 0]),
        np.array([-0.28, -0.15, 0]),
        np.array([-0.22, -0.22, 0]),
        np.array([-0.28, -0.3, 0]),
        np.array([-0.12, -0.45, 0]),
        np.array([-0.08, -0.6, 0]),
    ]
    face_line.set_points_as_corners(face_points)
    
    eye = Triangle(color=color, stroke_width=1.0).scale(0.06).move_to(np.array([-0.12, 0.18, 0]))
    shoulders = Arc(radius=0.7, start_angle=PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(np.array([0.1, -0.9, 0]))
    
    return VGroup(profile_line, face_line, eye, shoulders).scale(scale)


# ============================================================
# HELPERS (Bổ sung đầy đủ cho phần 4)
# ============================================================
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
    
    lbl_l = vn_tex_bold(title_left, color=color_left, scale=0.48).move_to(panel_l.get_top() + DOWN * 0.4)
    lbl_r = vn_tex_bold(title_right, color=color_right, scale=0.48).move_to(panel_r.get_top() + DOWN * 0.4)
    
    vs = vn_tex_bold("VS", color=TEXT_MUTED, scale=0.7).move_to(DOWN * 0.2)
    return VGroup(panel_l, panel_r, lbl_l, lbl_r, vs).scale(scale)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene28_VsPreceding(Scene):
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
        sub_1 = make_subtitle("EBGM được xây dựng dựa trên hệ thống Lades 1993, với 3 cải tiến")
        self.current_sub = sub_1
        self.play(FadeIn(sub_1, shift=UP * 0.15), run_time=0.4)

        # Tiêu đề
        title = vn_tex_bold("EBGM vs Hệ Tiền Nhiệm (Lades, 1993)", color=ACCENT_LAVENDER, scale=0.8)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # vs-card
        vs_card = make_vs_card("LADES 1993", "EBGM", PREV_COLOR, EBGM_BRAND, scale=0.95)
        self.play(FadeIn(vs_card), run_time=1.2)
        self.wait(7.6) # Wait out 10s total

        # ============================================================
        # PHASE B: 3 Cải tiến (10s - 60s)
        # ============================================================
        
        # ------------------------------------------------------------
        # Cải tiến 1: Phase Information (10s - 27s)
        # ------------------------------------------------------------
        sub_2 = make_subtitle("Một: dùng thông tin phase để định vị điểm mốc chính xác hơn")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # Label bottom cho Cải tiến 1
        lbl_c1 = vn_tex_bold("1. Dùng Phase Wavelet --- Định vị điểm mốc chính xác hơn", color=ACCENT_CYAN, scale=0.45).move_to(DOWN * 2.8)
        self.play(FadeIn(lbl_c1, shift=UP*0.15), run_time=0.6)

        # Thiết kế visual cho Panel Trái (Lades) - Không dùng phase, lệch
        center_l = vs_card[0].get_center() + DOWN * 0.2
        target_point_l = Dot(center_l, radius=0.06, color=TEXT_PRIMARY)
        target_ring_l = Circle(radius=0.15, color=TEXT_MUTED, stroke_width=1.0).move_to(center_l)
        lbl_eye_l = vn_tex("Khóe mắt", color=TEXT_MUTED, scale=0.28).next_to(target_ring_l, DOWN, buff=0.1)

        # Node matching Lades (lệch hẳn)
        node_l = Dot(center_l + UP * 0.5 + RIGHT * 0.4, radius=0.08, color=ACCENT_CORAL)
        error_line_l = Line(center_l, node_l.get_center(), color=ACCENT_CORAL, stroke_width=2)
        lbl_val_l = vn_tex("Sai số: 5.2 px", color=ACCENT_CORAL, scale=0.3).next_to(node_l, UP, buff=0.15)

        self.play(
            FadeIn(target_point_l), FadeIn(target_ring_l), FadeIn(lbl_eye_l),
            run_time=0.8
        )
        self.play(
            node_l.animate.move_to(center_l + UP * 0.5 + RIGHT * 0.4),
            Create(error_line_l),
            FadeIn(lbl_val_l, shift=DOWN*0.1),
            run_time=1.2
        )
        self.play(Indicate(node_l, color=ACCENT_CORAL), Flash(node_l.get_center(), color=ACCENT_CORAL, flash_radius=0.35), run_time=0.8)

        # Thiết kế visual cho Panel Phải (EBGM) - Dùng phase, cực chính xác
        center_r = vs_card[1].get_center() + DOWN * 0.2
        target_point_r = Dot(center_r, radius=0.06, color=TEXT_PRIMARY)
        target_ring_r = Circle(radius=0.15, color=TEXT_MUTED, stroke_width=1.0).move_to(center_r)
        lbl_eye_r = vn_tex("Khóe mắt", color=TEXT_MUTED, scale=0.28).next_to(target_ring_r, DOWN, buff=0.1)

        # Node matching EBGM (gần như trùng khít)
        node_r = Dot(center_r + UP * 0.12 + RIGHT * 0.08, radius=0.08, color=ACCENT_MINT)
        error_line_r = Line(center_r, node_r.get_center(), color=ACCENT_MINT, stroke_width=2)
        lbl_val_r = vn_tex("Sai số: 1.6 px", color=ACCENT_MINT, scale=0.3).next_to(node_r, UP, buff=0.15)

        self.play(
            FadeIn(target_point_r), FadeIn(target_ring_r), FadeIn(lbl_eye_r),
            run_time=0.8
        )
        
        # Subtitle to sub_3 (18s)
        sub_3 = make_subtitle("Sai số giảm từ 5.2 xuống 1.6 pixel")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        self.play(
            node_r.animate.move_to(center_r + UP * 0.12 + RIGHT * 0.08),
            Create(error_line_r),
            FadeIn(lbl_val_r, shift=DOWN*0.1),
            run_time=1.2
        )
        self.play(Indicate(node_r, color=ACCENT_MINT), Flash(node_r.get_center(), color=ACCENT_MINT, flash_radius=0.35), run_time=0.8)
        self.wait(1.4) # Wait out until 27s total

        # Clean Cải tiến 1
        self.play(
            FadeOut(lbl_c1),
            FadeOut(target_point_l), FadeOut(target_ring_l), FadeOut(lbl_eye_l), FadeOut(node_l), FadeOut(error_line_l), FadeOut(lbl_val_l),
            FadeOut(target_point_r), FadeOut(target_ring_r), FadeOut(lbl_eye_r), FadeOut(node_r), FadeOut(error_line_r), FadeOut(lbl_val_r),
            run_time=0.6
        )

        # ------------------------------------------------------------
        # Cải tiến 2: Object-adapted Grids (27s - 44s)
        # ------------------------------------------------------------
        sub_4 = make_subtitle("Hai: object-adapted grids — mỗi tư thế đầu có một grid riêng")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4

        # Label bottom cho Cải tiến 2
        lbl_c2 = vn_tex_bold("2. Object-Adapted Grids --- Co giãn \\& Xử lý đa tư thế đầu", color=ACCENT_CYAN, scale=0.45).move_to(DOWN * 2.8)
        self.play(FadeIn(lbl_c2, shift=UP*0.15), run_time=0.6)

        # Panel Trái: Lades (Rigid rectangular grid)
        rigid_mesh = NumberPlane(
            x_range=[-1.0, 1.0, 0.4], y_range=[-1.0, 1.0, 0.4],
            background_line_style={"stroke_color": PREV_COLOR, "stroke_width": 1.2, "stroke_opacity": 0.5}
        ).scale(0.8).move_to(center_l)
        
        profile_l = make_profile_silhouette(color=TEXT_MUTED, scale=0.75).move_to(center_l)
        mismatch_lbl = vn_tex("Lệch điểm mốc (Rigid Grid)", color=ACCENT_CORAL, scale=0.3).next_to(vs_card[0], DOWN, buff=-0.7)

        self.play(FadeIn(profile_l), Create(rigid_mesh), run_time=1.2)
        self.play(FadeIn(mismatch_lbl, shift=UP*0.1), run_time=0.6)
        self.wait(1.0)

        # Panel Phải: EBGM (3 pose-adapted grids)
        frontal_r = make_frontal_silhouette(color=TEXT_MUTED, scale=0.75).move_to(center_r)
        
        # Grid cho frontal r (căn chỉnh đẹp mắt)
        frontal_mesh = NumberPlane(
            x_range=[-1.0, 1.0, 0.45], y_range=[-1.0, 1.0, 0.45],
            background_line_style={"stroke_color": ACCENT_LAVENDER, "stroke_width": 1.5, "stroke_opacity": 0.6}
        ).scale(0.85).move_to(center_r)

        self.play(FadeIn(frontal_r), Create(frontal_mesh), run_time=1.2)
        self.wait(1.0)

        # Subtitle to sub_5 (38s)
        sub_5 = make_subtitle("Xử lý được nhiều góc chụp khác nhau")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5

        # Transform Frontal sang Profile và mesh tự động co giãn theo profile!
        profile_r = make_profile_silhouette(color=ACCENT_LAVENDER, scale=0.75).move_to(center_r)
        
        # Warped Profile Mesh (vẽ thủ công để hiển thị sự biến dạng hoàn hảo bám theo profile)
        warped_lines = VGroup()
        profile_nodes = [
            [-0.1, 0.35, 0], [0.15, 0.3, 0], [0.2, 0.08, 0], [0.15, -0.22, 0],
            [-0.14, 0.26, 0], [0.0, 0.08, 0], [0.08, -0.15, 0], [-0.06, -0.34, 0],
            [-0.32, 0.04, 0], [-0.17, -0.06, 0], [-0.21, -0.16, 0], [-0.17, -0.34, 0]
        ]
        # Shift nodes to panel center
        profile_nodes = [np.array(node) * 0.75 + center_r for node in profile_nodes]
        dots_r = VGroup(*[Dot(node, radius=0.04, color=ACCENT_LAVENDER) for node in profile_nodes])
        
        # Connect nodes to form a warped mesh
        connections = [
            (0,1), (1,2), (2,3), (4,5), (5,6), (6,7), (8,9), (9,10), (10,11),
            (0,4), (4,8), (1,5), (5,9), (2,6), (6,10), (3,7), (7,11)
        ]
        for start, end in connections:
            warped_lines.add(Line(profile_nodes[start], profile_nodes[end], color=ACCENT_LAVENDER, stroke_width=1.2).set_opacity(0.7))

        self.play(
            ReplacementTransform(frontal_r, profile_r),
            ReplacementTransform(frontal_mesh, VGroup(warped_lines, dots_r)),
            run_time=1.8
        )
        self.play(Indicate(VGroup(warped_lines, dots_r), color=ACCENT_MINT), run_time=0.8)
        self.wait(1.6) # Wait out until 44s total

        # Clean Cải tiến 2
        self.play(
            FadeOut(lbl_c2),
            FadeOut(rigid_mesh), FadeOut(profile_l), FadeOut(mismatch_lbl),
            FadeOut(profile_r), FadeOut(warped_lines), FadeOut(dots_r),
            run_time=0.6
        )

        # ------------------------------------------------------------
        # Cải tiến 3: Face Bunch Graph (44s - 60s)
        # ------------------------------------------------------------
        sub_6 = make_subtitle("Ba: FBG cho phép tìm điểm mốc của người mới chỉ trong một lần quét")
        self.play(ReplacementTransform(self.current_sub, sub_6), run_time=0.4)
        self.current_sub = sub_6

        # Label bottom cho Cải tiến 3
        lbl_c3 = vn_tex_bold("3. Face Bunch Graph (FBG) --- Trích xuất điểm mốc trong 1 lần quét", color=ACCENT_CYAN, scale=0.45).move_to(DOWN * 2.8)
        self.play(FadeIn(lbl_c3, shift=UP*0.15), run_time=0.6)

        # Panel Trái: Lades (1 Probe phải search lặp đi lặp lại)
        probe_l = make_frontal_silhouette(color=TEXT_MUTED, scale=0.4).move_to(center_l + LEFT * 1.0 + UP * 0.8)
        gal1_l = make_frontal_silhouette(color=PREV_COLOR, scale=0.35).move_to(center_l + RIGHT * 1.0 + UP * 1.2)
        gal2_l = make_frontal_silhouette(color=PREV_COLOR, scale=0.35).move_to(center_l + RIGHT * 1.0)
        gal3_l = make_frontal_silhouette(color=PREV_COLOR, scale=0.35).move_to(center_l + RIGHT * 1.0 + DOWN * 1.2)
        
        lbl_slow = vn_tex("Search lặp lại (Chậm)", color=ACCENT_CORAL, scale=0.28).next_to(vs_card[0], DOWN, buff=-0.7)

        self.play(FadeIn(probe_l), FadeIn(gal1_l), FadeIn(gal2_l), FadeIn(gal3_l), run_time=1.0)
        self.play(FadeIn(lbl_slow), run_time=0.4)

        # Show repeated arrows
        a1 = Arrow(probe_l.get_right(), gal1_l.get_left(), color=ACCENT_CORAL, buff=0.1, stroke_width=2.5)
        a2 = Arrow(probe_l.get_right(), gal2_l.get_left(), color=ACCENT_CORAL, buff=0.1, stroke_width=2.5)
        a3 = Arrow(probe_l.get_right(), gal3_l.get_left(), color=ACCENT_CORAL, buff=0.1, stroke_width=2.5)

        self.play(Create(a1), run_time=0.6)
        self.play(Create(a2), run_time=0.6)
        self.play(Create(a3), run_time=0.6)
        self.wait(0.5)

        # Subtitle to sub_7 (58s)
        sub_7 = make_subtitle("Điều này tăng tốc độ tính toán đáng kể với database lớn")
        self.play(ReplacementTransform(self.current_sub, sub_7), run_time=0.4)
        self.current_sub = sub_7

        # Panel Phải: EBGM (Quét 1 lần qua FBG)
        probe_r = make_frontal_silhouette(color=TEXT_MUTED, scale=0.4).move_to(center_r + LEFT * 1.2)
        
        # Bunch stack visual (3 layers of graphs)
        bunch_g = VGroup()
        for idx in range(3):
            bg_rect = RoundedRectangle(width=0.9, height=1.3, corner_radius=0.05, stroke_color=ACCENT_LAVENDER, stroke_width=1.0, fill_color=BG_NAVY_SOFT, fill_opacity=0.8)
            g_mesh = NumberPlane(x_range=[-0.4, 0.4, 0.25], y_range=[-0.5, 0.5, 0.25], background_line_style={"stroke_color": ACCENT_LAVENDER, "stroke_width": 0.8}).scale(0.5)
            layer = VGroup(bg_rect, g_mesh).shift(UP * 0.12 * idx + RIGHT * 0.12 * idx)
            bunch_g.add(layer)
        
        bunch_g.move_to(center_r + RIGHT * 1.0)
        lbl_fbg = vn_tex("FBG", color=ACCENT_LAVENDER, scale=0.28).next_to(bunch_g, UP, buff=0.1)

        self.play(FadeIn(probe_r), FadeIn(bunch_g), FadeIn(lbl_fbg), run_time=1.0)
        
        # Single arrow Probe -> FBG
        a_fbg = Arrow(probe_r.get_right(), bunch_g.get_left(), color=ACCENT_MINT, buff=0.1, stroke_width=3.0)
        self.play(Create(a_fbg), run_time=0.8)
        self.play(Indicate(bunch_g, color=ACCENT_MINT), run_time=0.8)

        lbl_fast = vn_tex("Quét 1 Lần Duy Nhất!", color=ACCENT_MINT, scale=0.28).next_to(vs_card[1], DOWN, buff=-0.7)
        self.play(FadeIn(lbl_fast, shift=UP*0.1), run_time=0.6)
        self.wait(1.8) # Wait out until 60s total

        # Clean Phase B
        self.play(
            FadeOut(lbl_c3),
            FadeOut(probe_l), FadeOut(gal1_l), FadeOut(gal2_l), FadeOut(gal3_l), FadeOut(a1), FadeOut(a2), FadeOut(a3), FadeOut(lbl_slow),
            FadeOut(probe_r), FadeOut(bunch_g), FadeOut(lbl_fbg), FadeOut(a_fbg), FadeOut(lbl_fast),
            run_time=0.6
        )

        # ============================================================
        # PHASE C: Tổng kết (60s - 70s)
        # ============================================================
        sub_8 = make_subtitle("Cùng độ chính xác — nhưng nhanh hơn và linh hoạt hơn nhiều")
        self.play(ReplacementTransform(self.current_sub, sub_8), run_time=0.4)
        self.current_sub = sub_8

        # Summary Table in center
        table_y = [0.8, 0.2, -0.4, -1.0]
        table_x = [-3.8, -0.6, 2.8]

        th_crit = vn_tex_bold("Cải tiến lớn", color=ACCENT_CYAN, scale=0.38).move_to(np.array([table_x[0], table_y[0], 0]))
        th_lades = vn_tex_bold("Lades 1993", color=PREV_COLOR, scale=0.38).move_to(np.array([table_x[1], table_y[0], 0]))
        th_ebgm = vn_tex_bold("EBGM 1999", color=ACCENT_LAVENDER, scale=0.38).move_to(np.array([table_x[2], table_y[0], 0]))
        
        row1_crit = vn_tex("1. Định vị điểm mốc", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([table_x[0], table_y[1], 0]))
        row1_lades = vn_tex("Thô (~5.2 px)", color=TEXT_MUTED, scale=0.32).move_to(np.array([table_x[1], table_y[1], 0]))
        row1_ebgm = vn_tex("Cực Tinh (~1.6 px)", color=ACCENT_MINT, scale=0.32).move_to(np.array([table_x[2], table_y[1], 0]))

        row2_crit = vn_tex("2. Tư thế xử lý", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([table_x[0], table_y[2], 0]))
        row2_lades = vn_tex("Chỉ 1 Grid cứng", color=TEXT_MUTED, scale=0.32).move_to(np.array([table_x[1], table_y[2], 0]))
        row2_ebgm = vn_tex("Đa lưới co giãn", color=ACCENT_MINT, scale=0.32).move_to(np.array([table_x[2], table_y[2], 0]))

        row3_crit = vn_tex("3. So khớp gallery", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([table_x[0], table_y[3], 0]))
        row3_lades = vn_tex("Lặp lại từng ảnh", color=TEXT_MUTED, scale=0.32).move_to(np.array([table_x[1], table_y[3], 0]))
        row3_ebgm = vn_tex("Quét FBG 1 lần", color=ACCENT_MINT, scale=0.32).move_to(np.array([table_x[2], table_y[3], 0]))

        table_lines = VGroup(
            Line(np.array([-5.2, 0.5, 0]), np.array([4.2, 0.5, 0]), color=TEXT_MUTED, stroke_width=0.8).set_opacity(0.4),
            Line(np.array([-5.2, -0.1, 0]), np.array([4.2, -0.1, 0]), color=TEXT_MUTED, stroke_width=0.8).set_opacity(0.4),
            Line(np.array([-5.2, -0.7, 0]), np.array([4.2, -0.7, 0]), color=TEXT_MUTED, stroke_width=0.8).set_opacity(0.4)
        )

        table_group = VGroup(
            th_crit, th_lades, th_ebgm,
            row1_crit, row1_lades, row1_ebgm,
            row2_crit, row2_lades, row2_ebgm,
            row3_crit, row3_lades, row3_ebgm,
            table_lines
        )

        # Fade out vs_card and fade in summary table
        self.play(FadeOut(vs_card), FadeIn(table_group, shift=UP*0.2), run_time=1.2)
        self.wait(1.5)

        # Honest note at bottom
        honest_note = vn_tex_italic("(Độ chính xác nhận diện frontal ngang nhau --- cải tiến chủ yếu nằm ở tốc độ \\& khả năng mở rộng)", color=TEXT_MUTED, scale=0.34).move_to(DOWN * 2.2)
        self.play(FadeIn(honest_note, shift=UP*0.1), run_time=0.8)
        self.wait(4.1) # Wait until 70s total

        # ============================================================
        # CLEANUP
        # ============================================================
        self.play(
            FadeOut(title),
            FadeOut(table_group),
            FadeOut(honest_note),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
