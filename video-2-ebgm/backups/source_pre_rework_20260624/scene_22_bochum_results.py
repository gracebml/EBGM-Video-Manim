"""
EBGM Video — Part 3: Experiments
Scene 22: Results trên Bochum (Cross-pose)
Thời lượng dự kiến: 60s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)

Render command:
  manim -pql scene_22_bochum_results.py Scene22_BochumResults
  manim -pqh scene_22_bochum_results.py Scene22_BochumResults  # high quality
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
# VECTOR SILHOUETTE GENERATORS FOR BOCHUM POSES
# ============================================================
def make_frontal_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt chính diện (0 độ)."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    eye_l = Dot(head.get_center() + LEFT * 0.18 + UP * 0.1, radius=0.04, color=color)
    eye_r = Dot(head.get_center() + RIGHT * 0.18 + UP * 0.1, radius=0.04, color=color)
    mouth = Arc(radius=0.12, start_angle=-5*PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.18)
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, mouth, shoulders).scale(scale)


def make_half_profile_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt nghiêng góc nhỏ (11 hoặc 22 độ)."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    eye_l = Dot(head.get_center() + LEFT * 0.28 + UP * 0.1, radius=0.035, color=color)
    eye_r = Dot(head.get_center() + LEFT * 0.02 + UP * 0.1, radius=0.045, color=color)
    nose = Line(head.get_center() + LEFT * 0.15 + UP * 0.05, head.get_center() + LEFT * 0.35 - DOWN * 0.05, color=color, stroke_width=1.2)
    mouth = Arc(radius=0.1, start_angle=-5*PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + LEFT * 0.15 + DOWN * 0.18)
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, nose, mouth, shoulders).scale(scale)


def make_percentage_circle(value, color=BAR_PRIMARY, radius=1.0):
    """Donut chart cho kết quả phần trăm (LaTeX thuần)."""
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


# ============================================================
# MAIN SCENE
# ============================================================
class Scene22_BochumResults(Scene):
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
        title = section_title("Bochum — Cross-Pose Recognition", color=ACCENT_CYAN)
        title.to_edge(UP, buff=0.6)
        
        intro_lbl = vn_tex("Gallery: 108 người chính diện. Probe: ảnh nghiêng xoay 3D.", color=ACCENT_CYAN, scale=0.42)
        intro_lbl.next_to(title, DOWN, buff=0.18)

        # Phụ đề 1
        sub_1 = make_subtitle("Bài test cross-pose — match ảnh nghiêng với gallery chính diện")
        self.current_sub = sub_1

        self.play(
            FadeIn(title, shift=DOWN * 0.25),
            FadeIn(intro_lbl, shift=UP * 0.15),
            FadeIn(sub_1, shift=UP * 0.15),
            run_time=1.5
        )
        self.wait(8.5)

        # ============================================================
        # PHASE B: 3 Poses & Donut Charts (10s - 35s)
        # ============================================================
        # 1. Chuyển phụ đề sang sub_2 (10s)
        sub_2 = make_subtitle("Xoay 11$^\circ$: 94\% — gần như không bị ảnh hưởng")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # 2. Xây dựng 3 cụm góc xoay
        # Cụm 1: 0 độ
        c1_pos = np.array([-3.6, 0.1, 0])
        c1_lbl = vn_tex("0$^\circ$ (Chính diện)", color=TEXT_PRIMARY, scale=0.35).move_to(c1_pos + UP * 1.5)
        c1_sil = make_frontal_silhouette(color=ACCENT_CYAN, scale=0.55).move_to(c1_pos + UP * 0.55)
        c1_donut = make_percentage_circle(91, color=ACCENT_CYAN, radius=0.65).move_to(c1_pos - UP * 0.8)
        group_0deg = VGroup(c1_lbl, c1_sil, c1_donut)

        # Cụm 2: 11 độ
        c2_pos = np.array([0.0, 0.1, 0])
        c2_lbl = vn_tex("11$^\circ$ (Xoay nhẹ)", color=TEXT_PRIMARY, scale=0.35).move_to(c2_pos + UP * 1.5)
        c2_sil = make_half_profile_silhouette(color=ACCENT_LAVENDER, scale=0.55).move_to(c2_pos + UP * 0.55)
        c2_donut = make_percentage_circle(94, color=ACCENT_MINT, radius=0.65).move_to(c2_pos - UP * 0.8)
        group_11deg = VGroup(c2_lbl, c2_sil, c2_donut)

        # Cụm 3: 22 độ
        c3_pos = np.array([3.6, 0.1, 0])
        c3_lbl = vn_tex("22$^\circ$ (Xoay vừa)", color=TEXT_PRIMARY, scale=0.35).move_to(c3_pos + UP * 1.5)
        c3_sil = make_half_profile_silhouette(color=ACCENT_LAVENDER, scale=0.55).move_to(c3_pos + UP * 0.55)
        # Co hẹp bề ngang để tạo hiệu ứng nghiêng nhiều hơn
        c3_sil.stretch_to_fit_width(0.32)
        c3_donut = make_percentage_circle(88, color=ACCENT_CYAN, radius=0.65).move_to(c3_pos - UP * 0.8)
        group_22deg = VGroup(c3_lbl, c3_sil, c3_donut)

        # Animation hiện silhouettes + nhãn góc
        self.play(
            LaggedStart(
                FadeIn(VGroup(c1_lbl, c1_sil), shift=UP * 0.25),
                FadeIn(VGroup(c2_lbl, c2_sil), shift=UP * 0.25),
                FadeIn(VGroup(c3_lbl, c3_sil), shift=UP * 0.25),
                lag_ratio=0.35
            ),
            run_time=1.8
        )
        self.wait(1.8)

        # 3. Phụ đề sub_3 & Donut sweep (14s)
        sub_3 = make_subtitle("Xoay 22$^\circ$: 88\% — vẫn rất tốt")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        # Hiện nền donut
        self.play(
            FadeIn(c1_donut[0]), FadeIn(c1_donut[2]),
            FadeIn(c2_donut[0]), FadeIn(c2_donut[2]),
            FadeIn(c3_donut[0]), FadeIn(c3_donut[2]),
            run_time=0.8
        )
        # Sweep đầy cung
        self.play(
            Create(c1_donut[1]),
            Create(c2_donut[1]),
            Create(c3_donut[1]),
            run_time=1.6
        )
        self.wait(3.4)

        # 4. Phụ đề sub_4 & Mũi tên nằm ngang (22s)
        sub_4 = make_subtitle("Mức suy giảm rất nhẹ — Gabor wavelet trơ lì với biến đổi nhỏ")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4

        arrow = DoubleArrow(c1_pos + DOWN * 1.6, c3_pos + DOWN * 1.6, color=ACCENT_LAVENDER, stroke_width=1.5, buff=0.2).scale(0.8)
        arrow_lbl = vn_tex("Mức suy giảm rất nhỏ!", color=ACCENT_LAVENDER, scale=0.34).next_to(arrow, DOWN, buff=0.15)

        self.play(
            Create(arrow),
            FadeIn(arrow_lbl, shift=UP * 0.1),
            run_time=1.2
        )
        self.wait(8.8)

        # Dọn dẹp mũi tên trước khi dịch chuyển
        self.play(FadeOut(arrow), FadeOut(arrow_lbl), run_time=0.6)

        # ============================================================
        # PHASE C: Bảng so sánh hệ thống cũ (35s - 55s)
        # ============================================================
        # 1. Thu nhỏ và dịch chuyển 3 cụm sang trái
        all_3_groups = VGroup(group_0deg, group_11deg, group_22deg)
        self.play(
            all_3_groups.animate.scale(0.55).shift(LEFT * 3.4 + UP * 0.2),
            run_time=1.2
        )

        # 2. Xây dựng Bảng so sánh bên phải
        table_bg = RoundedRectangle(
            corner_radius=0.08, width=5.6, height=3.0, color=ACCENT_BLUE, stroke_width=0.8,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.8
        ).move_to(np.array([3.3, 0.4, 0]))

        col_x = [1.2, 3.2, 5.0]
        row_y = [1.4, 0.8, 0.2, -0.4]

        # Hàng tiêu đề cột
        h_goc = vn_tex_bold("Góc xoay", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([col_x[0], row_y[0], 0]))
        h_prev = vn_tex_bold("Tiền nhiệm", color=PREV_COLOR, scale=0.32).move_to(np.array([col_x[1], row_y[0], 0]))
        h_ebgm = vn_tex_bold("Hệ EBGM", color=EBGM_BRAND, scale=0.32).move_to(np.array([col_x[2], row_y[0], 0]))
        headers = VGroup(h_goc, h_prev, h_ebgm)

        # Hàng 1 (0 độ)
        r1_c1 = vn_tex("0$^\circ$ (fb)", color=TEXT_PRIMARY, scale=0.3).move_to(np.array([col_x[0], row_y[1], 0]))
        r1_c2 = vn_tex_mono("92\%", color=PREV_COLOR, scale=0.32).move_to(np.array([col_x[1], row_y[1], 0]))
        r1_c3 = vn_tex_mono("91\%", color=EBGM_BRAND, scale=0.32).move_to(np.array([col_x[2], row_y[1], 0]))
        row1 = VGroup(r1_c1, r1_c2, r1_c3)

        # Hàng 2 (11 độ)
        r2_c1 = vn_tex("11$^\circ$ rotated", color=TEXT_PRIMARY, scale=0.3).move_to(np.array([col_x[0], row_y[2], 0]))
        r2_c2 = vn_tex_mono("97\%", color=PREV_COLOR, scale=0.32).move_to(np.array([col_x[1], row_y[2], 0]))
        r2_c3 = vn_tex_mono("94\%", color=EBGM_BRAND, scale=0.32).move_to(np.array([col_x[2], row_y[2], 0]))
        row2 = VGroup(r2_c1, r2_c2, r2_c3)

        # Hàng 3 (22 độ - EBGM vượt trội)
        r3_c1 = vn_tex("22$^\circ$ rotated", color=TEXT_PRIMARY, scale=0.3).move_to(np.array([col_x[0], row_y[3], 0]))
        r3_c2 = vn_tex_mono("85\%", color=PREV_COLOR, scale=0.32).move_to(np.array([col_x[1], row_y[3], 0]))
        r3_c3 = vn_tex_bold("88\%", color=ACCENT_MINT, scale=0.38).move_to(np.array([col_x[2], row_y[3], 0]))
        row3 = VGroup(r3_c1, r3_c2, r3_c3)

        # Các đường phân tách kẻ ngang mỏng
        divider_y = [1.1, 0.5, -0.1]
        dividers = VGroup()
        for y_val in divider_y:
            div = Line(np.array([0.7, y_val, 0]), np.array([5.9, y_val, 0]), color=TEXT_MUTED, stroke_width=0.5).set_opacity(0.3)
            dividers.add(div)

        # Note box dưới bảng
        note_box_bg = RoundedRectangle(
            corner_radius=0.06, width=5.6, height=0.9, color=ACCENT_LAVENDER, stroke_width=0.6,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.95
        ).move_to(np.array([3.3, -1.3, 0]))
        note_txt_1 = vn_tex("EBGM dùng ít hơn: chỉ 30 nodes (thay vì 70)", color=TEXT_PRIMARY, scale=0.3).move_to(note_box_bg.get_center() + UP * 0.16)
        note_txt_2 = vn_tex("Không cần resize ảnh -> Vẫn hoạt động vượt trội!", color=ACCENT_LAVENDER, scale=0.3).move_to(note_box_bg.get_center() + DOWN * 0.16)
        note_box = VGroup(note_box_bg, note_txt_1, note_txt_2)

        # Hiện nền bảng, header và dividers
        sub_8 = make_subtitle("So với hệ thống tiền nhiệm — EBGM tốt hơn ở case 22$^\circ$")
        self.play(
            ReplacementTransform(self.current_sub, sub_8),
            FadeIn(table_bg),
            FadeIn(headers),
            FadeIn(dividers),
            run_time=1.2
        )
        self.current_sub = sub_8

        # Hiện từng hàng dữ liệu
        self.play(
            LaggedStart(FadeIn(row1), FadeIn(row2), FadeIn(row3), lag_ratio=0.3),
            run_time=1.5
        )
        # Highlight hàng 22 độ EBGM thắng thế
        self.play(
            Indicate(r3_c3, color=ACCENT_MINT, scale_factor=1.15),
            Flash(r3_c3.get_center(), color=ACCENT_MINT, flash_radius=0.5),
            run_time=1.0
        )
        self.wait(1.5)

        # Hiện note_box giải thích (45s)
        sub_9 = make_subtitle("Mà chỉ cần 30 nodes thay vì 70 — ít thông tin, hiệu quả hơn")
        self.play(
            ReplacementTransform(self.current_sub, sub_9),
            FadeIn(note_box, shift=UP * 0.15),
            run_time=1.0
        )
        self.current_sub = sub_9
        self.wait(6.0)

        # ============================================================
        # PHASE D: Insight ngắn (55s - 60s)
        # ============================================================
        sub_10 = make_subtitle("EBGM xử lý xoay 3D nhỏ rất tốt nhờ đặc tính Gabor wavelet")
        
        # Kết luận lớn ở tâm
        conclusion = vn_tex("EBGM xử lý xoay 3D nhỏ xuất sắc nhờ đặc tính Gabor wavelet trơ lì", color=ACCENT_LAVENDER, scale=0.45).move_to(ORIGIN)

        self.play(
            FadeOut(table_bg),
            FadeOut(headers),
            FadeOut(dividers),
            FadeOut(row1),
            FadeOut(row2),
            FadeOut(row3),
            FadeOut(note_box),
            FadeOut(all_3_groups),
            ReplacementTransform(self.current_sub, sub_10),
            FadeIn(conclusion, shift=UP * 0.1),
            run_time=1.2
        )
        self.current_sub = sub_10
        self.wait(5.8)

        # Cleanup kết thúc scene
        self.play(
            FadeOut(conclusion),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
