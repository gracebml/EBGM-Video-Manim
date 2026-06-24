"""
EBGM Video — Part 3: Experiments
Scene 21: Results trên FERET
Thời lượng dự kiến: 75s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)

Render command:
  manim -pql scene_21_feret_results.py Scene21_FeretResults
  manim -pqh scene_21_feret_results.py Scene21_FeretResults  # high quality
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# PART 3 COLOR PALETTE
# ============================================================
BAR_PRIMARY   = "#48CAE4"
BAR_SECONDARY = "#778DA9"
BAR_SUCCESS   = "#95D5B2"
BAR_WARNING   = "#E29578"
TROPHY_GOLD   = "#FCBF49"

EBGM_BRAND    = "#B8B5FF"
PCA_COLOR     = "#76C5BF"
NN_COLOR      = "#E29578"
PREV_COLOR    = "#778DA9"

# ============================================================
# PART 3 ADDITIONAL HELPERS (Sử dụng LaTeX thuần)
# ============================================================
def make_bar_chart(values, labels, max_val=100, bar_color=BAR_PRIMARY,
                   highlight_idx=None, scale=1.0):
    """
    Tạo bar chart ngang bằng LaTeX thuần.
    """
    bars = VGroup()
    for i, (val, lbl) in enumerate(zip(values, labels)):
        color = EBGM_BRAND if i == highlight_idx else bar_color
        # Bar
        bar = Rectangle(
            width=val/max_val * 4.0,
            height=0.35,
            fill_color=color,
            fill_opacity=0.85,
            stroke_color=color,
            stroke_width=1
        )
        bar.shift(DOWN * i * 0.55 + RIGHT * (val/max_val * 2.0))
        
        # Label trái bằng vn_tex
        lbl_text = vn_tex(lbl, color=TEXT_PRIMARY, scale=0.45)
        lbl_text.next_to(bar, LEFT, buff=0.3).align_to(bar, LEFT).shift(LEFT * 0.5)
        
        # Value phải bằng vn_tex_mono (escape % trong LaTeX thành \%)
        val_text = vn_tex_mono(f"{val:.0f}\%", color=color, scale=0.45)
        val_text.next_to(bar, RIGHT, buff=0.2)
        
        bars.add(VGroup(bar, lbl_text, val_text))
    return bars.scale(scale)


def make_percentage_circle(value, color=BAR_PRIMARY, radius=1.0):
    """
    Donut chart: 1 con số phần trăm ở giữa (LaTeX thuần), vòng tròn lấp đầy theo %.
    """
    bg_ring = Circle(radius=radius, color=GRID_LINE, stroke_width=8).set_opacity(0.3)
    progress_ring = Arc(
        radius=radius,
        start_angle=PI/2,
        angle=-2*PI * (value/100),
        stroke_width=10,
        color=color
    )
    text = vn_tex_bold(f"{value:.0f}\%", color=color, scale=1.1 * radius)
    text.move_to(bg_ring.get_center())
    return VGroup(bg_ring, progress_ring, text)


def trophy_icon(color=TROPHY_GOLD, scale=0.6):
    """Icon trophy vẽ bằng VMobject (không dùng emoji)."""
    cup = VGroup(
        # Cup body
        ArcPolygon([-0.4,0.5,0], [0.4,0.5,0], [0.3,-0.3,0], [-0.3,-0.3,0],
                   color=color, fill_opacity=0.8, stroke_width=2),
        # Handles
        Arc(radius=0.2, start_angle=PI/2, angle=-PI, color=color, 
            stroke_width=3).shift(LEFT*0.4),
        Arc(radius=0.2, start_angle=PI/2, angle=PI, color=color,
            stroke_width=3).shift(RIGHT*0.4),
        # Base
        Rectangle(width=0.5, height=0.1, color=color, fill_opacity=0.8
                  ).shift(DOWN*0.4),
        Rectangle(width=0.8, height=0.08, color=color, fill_opacity=0.8
                  ).shift(DOWN*0.5),
    )
    return cup.scale(scale)


# ============================================================
# VECTOR SILHOUETTE GENERATORS FOR INSIGHT PHASES
# ============================================================
def make_frontal_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt chính diện (Frontal)."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    eye_l = Dot(head.get_center() + LEFT * 0.18 + UP * 0.1, radius=0.04, color=color)
    eye_r = Dot(head.get_center() + RIGHT * 0.18 + UP * 0.1, radius=0.04, color=color)
    mouth = Arc(radius=0.12, start_angle=-5*PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.18)
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, mouth, shoulders).scale(scale)


def make_half_profile_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt nghiêng vừa (Half-Profile)."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    eye_l = Dot(head.get_center() + LEFT * 0.28 + UP * 0.1, radius=0.035, color=color)
    eye_r = Dot(head.get_center() + LEFT * 0.02 + UP * 0.1, radius=0.045, color=color)
    nose = Line(head.get_center() + LEFT * 0.15 + UP * 0.05, head.get_center() + LEFT * 0.35 - DOWN * 0.05, color=color, stroke_width=1.2)
    mouth = Arc(radius=0.1, start_angle=-5*PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + LEFT * 0.15 + DOWN * 0.18)
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, nose, mouth, shoulders).scale(scale)


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
# MAIN SCENE
# ============================================================
class Scene21_FeretResults(Scene):
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
        # PHASE A: Setup tiêu đề (0s - 10s)
        # ============================================================
        title = section_title("FERET — Kết quả Rank-1 Recognition", color=ACCENT_CYAN)
        title.to_edge(UP, buff=0.6)
        
        intro_lbl = vn_tex("Mỗi gallery 250 người — bao nhiêu lần nhận diện đúng?", color=ACCENT_CYAN, scale=0.42)
        intro_lbl.next_to(title, DOWN, buff=0.18)

        # Phụ đề 1
        sub_1 = make_subtitle("Trên FERET — kết quả nhận diện rank-1")
        self.current_sub = sub_1

        self.play(
            FadeIn(title, shift=DOWN * 0.25),
            FadeIn(intro_lbl, shift=UP * 0.15),
            FadeIn(sub_1, shift=UP * 0.15),
            run_time=1.5
        )
        self.wait(8.5)

        # ============================================================
        # PHASE B: Bar chart chính & Spotlight (10s - 35s)
        # ============================================================
        # 1. Chuyển phụ đề sang sub_2
        sub_2 = make_subtitle("Chính diện vs chính diện: 98\% — gần như hoàn hảo")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # 2. Xây dựng Bar Chart
        values = [98, 84, 57, 18, 12]
        labels = [
            "Frontal (fa vs fb)",
            "Profile R vs Profile L",
            "Half-Profile R vs L",
            "Half-Profile vs Frontal",
            "Half-Profile vs Profile"
        ]
        
        chart = make_bar_chart(values, labels, max_val=100, bar_color=BAR_PRIMARY, highlight_idx=0, scale=0.95)
        # Căn chỉnh để chart nằm cân đối hơi lệch xuống và sang trái
        chart.shift(LEFT * 1.4 + DOWN * 0.4)

        chart_elements = []
        for group in chart:
            bar, lbl, val = group
            chart_elements.append((bar, lbl, val))

        # Animation hiện nhãn trước
        self.play(
            LaggedStart(*[FadeIn(lbl, shift=RIGHT * 0.2) for bar, lbl, val in chart_elements], lag_ratio=0.12),
            run_time=1.0
        )

        # Animation grow bar từ 0 và hiện số
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    GrowFromEdge(bar, LEFT),
                    FadeIn(val, shift=LEFT * 0.15)
                )
                for bar, lbl, val in chart_elements
            ], lag_ratio=0.25),
            run_time=2.2
        )
        self.wait(1.5)

        # 3. Spotlight cho 98% (Frontal) - Hiện cúp vàng (20s)
        bar_0, lbl_0, val_0 = chart_elements[0]
        trophy = trophy_icon(color=TROPHY_GOLD, scale=0.4).next_to(val_0, RIGHT, buff=0.25)

        self.play(
            Flash(val_0.get_center(), color=ACCENT_CYAN, flash_radius=0.5),
            Indicate(val_0, color=EBGM_BRAND, scale_factor=1.15),
            FadeIn(trophy, shift=LEFT * 0.2),
            run_time=1.0
        )
        self.wait(1.5)

        # 4. Phụ đề sub_3 & Spotlight cho 84% (Profile) (24s)
        sub_3 = make_subtitle("Profile vs profile (sau khi lật): 84\% — rất ấn tượng")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        bar_1, lbl_1, val_1 = chart_elements[1]
        spotlight_lbl = vn_tex("Xuất sắc cho Profile lật!", color=ACCENT_LAVENDER, scale=0.3).next_to(val_1, RIGHT, buff=0.2)

        self.play(
            Indicate(val_1, color=ACCENT_LAVENDER, scale_factor=1.1),
            FadeIn(spotlight_lbl, shift=LEFT * 0.15),
            run_time=1.0
        )
        self.wait(6.0)

        # ============================================================
        # PHASE C: Insight — Tại sao kết quả thay đổi? (35s - 55s)
        # ============================================================
        # 1. Thu nhỏ biểu đồ cột dịch sang trái
        chart_group = VGroup(chart, trophy, spotlight_lbl)
        self.play(
            chart_group.animate.scale(0.6).shift(LEFT * 2.8 + UP * 0.25),
            run_time=1.2
        )

        # 2. Xây dựng 3 cụm mô tả mốc giải thích
        # Cụm 1: Frontal vs Frontal (DỄ)
        frontal_l = make_frontal_silhouette(color=ACCENT_CYAN, scale=0.42).move_to(np.array([1.2, 1.2, 0]))
        frontal_r = make_frontal_silhouette(color=ACCENT_CYAN, scale=0.42).move_to(np.array([2.8, 1.2, 0]))
        connectors = VGroup(
            Line(frontal_l.get_center(), frontal_r.get_center(), color=ACCENT_CYAN, stroke_width=0.8).set_opacity(0.4),
            Line(frontal_l.get_center() + UP * 0.1, frontal_r.get_center() + UP * 0.1, color=ACCENT_CYAN, stroke_width=0.8).set_opacity(0.4)
        )
        lbl_1 = vn_tex("Chính diện: Chỉ khác biểu cảm nhỏ (DỄ)", color=ACCENT_CYAN, scale=0.34).move_to(np.array([4.0, 1.2, 0]), aligned_edge=LEFT)
        group_1 = VGroup(frontal_l, frontal_r, connectors, lbl_1)

        # Cụm 2: Profile lật đối xứng (ỔN)
        profile_l = make_profile_silhouette(color=ACCENT_LAVENDER, scale=0.42).move_to(np.array([1.2, -0.3, 0]))
        profile_r = make_profile_silhouette(color=ACCENT_LAVENDER, scale=0.42).move_to(np.array([2.8, -0.3, 0]))
        profile_r.stretch(-1, 0) # Lật ngược profile
        flip_arrow = DoubleArrow(profile_l.get_right() + RIGHT * 0.05, profile_r.get_left() + LEFT * 0.05, color=ACCENT_LAVENDER, stroke_width=1.2, buff=0).scale(0.5)
        lbl_2 = vn_tex("Lật profile: Tận dụng tính đối xứng (ỔN)", color=ACCENT_LAVENDER, scale=0.34).move_to(np.array([4.0, -0.3, 0]), aligned_edge=LEFT)
        group_2 = VGroup(profile_l, profile_r, flip_arrow, lbl_2)

        # Cụm 3: Half-profile vs Frontal (KHÓ)
        half_profile = make_half_profile_silhouette(color=ACCENT_CORAL, scale=0.42).move_to(np.array([1.2, -1.8, 0]))
        frontal_target = make_frontal_silhouette(color=ACCENT_BLUE, scale=0.42).move_to(np.array([2.8, -1.8, 0]))
        neq_sign = vn_tex(r"\neq", color=ACCENT_CORAL, scale=0.7).move_to(np.array([2.0, -1.8, 0]))
        lbl_3 = vn_tex("Góc xoay quá lớn 40-70$^\circ$ (KHÓ)", color=ACCENT_CORAL, scale=0.34).move_to(np.array([4.0, -1.8, 0]), aligned_edge=LEFT)
        group_3 = VGroup(half_profile, frontal_target, neq_sign, lbl_3)

        # Hiện cụm 1 (Chính diện)
        sub_5 = make_subtitle("Frontal vs frontal dễ — chỉ khác biểu cảm nhỏ")
        self.play(
            ReplacementTransform(sub_3, sub_5),
            FadeIn(group_1),
            run_time=1.0
        )
        self.current_sub = sub_5
        self.wait(4.0)

        # Hiện cụm 2 (Profile)
        sub_6 = make_subtitle("Profile lật ngược tận dụng được tính đối xứng của khuôn mặt")
        self.play(
            ReplacementTransform(self.current_sub, sub_6),
            FadeIn(group_2),
            run_time=1.0
        )
        self.current_sub = sub_6
        self.wait(4.0)

        # Hiện cụm 3 (Half-profile)
        sub_7 = make_subtitle("Half-profile có góc xoay rất lớn — đây là giới hạn thật của EBGM")
        self.play(
            ReplacementTransform(self.current_sub, sub_7),
            FadeIn(group_3),
            run_time=1.0
        )
        self.current_sub = sub_7
        self.wait(5.0)

        # Dọn dẹp Phase C
        self.play(
            FadeOut(chart_group),
            FadeOut(group_1),
            FadeOut(group_2),
            FadeOut(group_3),
            run_time=0.8
        )
        self.wait(0.2)

        # ============================================================
        # PHASE D: Take-away & Percentage Circle (55s - 75s)
        # ============================================================
        sub_8 = make_subtitle("Kết luận: EBGM xuất sắc trong cùng pose, vẫn cần cải thiện cross-pose")
        self.current_sub = sub_8

        # 1. Dòng kết luận trung tâm
        conclusion = vn_tex("Hiệu năng tối đa khi tư thế tương đồng. Hiệu năng suy giảm khi góc xoay sâu tăng.", color=TEXT_PRIMARY, scale=0.45).move_to(UP * 1.6)
        
        # 2. Hai vòng tròn tiêu biểu
        circle_98 = make_percentage_circle(98, color=EBGM_BRAND, radius=1.1).move_to(LEFT * 2.2 + DOWN * 0.8)
        circle_84 = make_percentage_circle(84, color=BAR_PRIMARY, radius=0.9).move_to(RIGHT * 2.2 + DOWN * 0.8)
        
        lbl_circle_98 = vn_tex("Frontal Recognition", color=EBGM_BRAND, scale=0.35).next_to(circle_98, DOWN, buff=0.25)
        lbl_circle_84 = vn_tex("Profile (Lật đối xứng)", color=BAR_PRIMARY, scale=0.35).next_to(circle_84, DOWN, buff=0.25)

        self.play(
            FadeIn(conclusion, shift=DOWN * 0.15),
            FadeIn(circle_98[0]), FadeIn(circle_98[2]), FadeIn(lbl_circle_98),
            FadeIn(circle_84[0]), FadeIn(circle_84[2]), FadeIn(lbl_circle_84),
            ReplacementTransform(self.current_sub, sub_8),
            run_time=1.2
        )
        self.current_sub = sub_8

        # Chạy sweep đầy vòng phần trăm
        self.play(
            Create(circle_98[1]),
            Create(circle_84[1]),
            run_time=1.8
        )
        self.wait(6.0)

        # Cleanup toàn màn hình kết thúc scene
        self.play(
            FadeOut(conclusion),
            FadeOut(circle_98),
            FadeOut(lbl_circle_98),
            FadeOut(circle_84),
            FadeOut(lbl_circle_84),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
