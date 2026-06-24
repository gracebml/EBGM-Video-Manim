"""
EBGM Video — Algorithm Detail Section
Scene 11: So sánh Jet — Similarity functions
Thời lượng dự kiến: 75s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)
  - Hoạt động trong conda env "vid"

Render command:
  manim -pql scene_11_similarity.py Scene11_Similarity
  manim -pqh scene_11_similarity.py Scene11_Similarity  # high quality
"""

from manim import *
import numpy as np
from _common import *

def make_mini_jet(pos, color=ACCENT_CYAN):
    jet = VGroup()
    for nu in range(3):
        disk = VGroup()
        for mu in range(8):
            sector = AnnularSector(
                inner_radius=0.15 + nu * 0.05,
                outer_radius=0.3 + nu * 0.05,
                start_angle=mu * PI/4,
                angle=PI/4,
                color=interpolate_color(ManimColor(color), ManimColor(TEXT_MUTED), 0.3),
                fill_opacity=0.5,
                stroke_color=BG_NAVY,
                stroke_width=0.4
            )
            disk.add(sector)
        disk.shift(UP * nu * 0.22)
        jet.add(disk)
    jet.rotate(25 * DEGREES, axis=RIGHT)
    jet.move_to(pos)
    return jet

class Scene11_Similarity(Scene):
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
        # PHASE A: Đặt vấn đề (0s - 15s)
        # ============================================================
        # Section Title
        title = section_title("So sánh Jet: Hai hàm Similarity")
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=1.0)

        # Main question
        question = vn_tex("Làm sao so sánh hai đặc trưng Jet?", color=TEXT_PRIMARY, scale=0.7).shift(UP * 1.5)
        self.play(Write(question), run_time=1.8)

        # Subtitle 1 (0s - 8s)
        update_sub("Hai jet --- chúng giống nhau không? Cách nhau bao xa?", 5.0)

        # Draw two Gabor jets J and J'
        jet_l = make_mini_jet(LEFT * 2.8 + DOWN * 0.5, ACCENT_CYAN)
        jet_r = make_mini_jet(RIGHT * 2.8 + DOWN * 0.5, ACCENT_LAVENDER)
        
        lbl_l = MathTex(r"\mathcal{J}", tex_template=VN_TEX_TEMPLATE, color=ACCENT_CYAN).scale(0.85).next_to(jet_l, UP, buff=0.2)
        lbl_r = MathTex(r"\mathcal{J}'", tex_template=VN_TEX_TEMPLATE, color=ACCENT_LAVENDER).scale(0.85).next_to(jet_r, UP, buff=0.2)

        compare_arrow = DoubleArrow(
            start=LEFT * 1.5 + DOWN * 0.2,
            end=RIGHT * 1.5 + DOWN * 0.2,
            color=TEXT_MUTED, stroke_width=2.5
        )
        compare_lbl = vn_tex_italic("So khớp?", color=TEXT_MUTED, scale=0.45).next_to(compare_arrow, UP, buff=0.15)

        self.play(
            FadeIn(Group(jet_l, jet_r)),
            FadeIn(VGroup(lbl_l, lbl_r)),
            Create(compare_arrow),
            FadeIn(compare_lbl),
            run_time=1.5
        )
        self.wait(1.5)

        # Clear Phase A elements
        self.play(
            FadeOut(question),
            FadeOut(Group(jet_l, jet_r)),
            FadeOut(VGroup(lbl_l, lbl_r)),
            FadeOut(compare_arrow),
            FadeOut(compare_lbl),
            run_time=0.8
        )

        # ============================================================
        # PHASE B: Hàm similarity KHÔNG dùng phase - Sa (15s - 35s)
        # ============================================================
        # Subtitle 2 (8s - 16s)
        update_sub("Cách 1: chỉ so sánh magnitude --- bỏ qua phase", 5.0)

        # Left panel: Formula Sa
        formula_sa = MathTex(
            r"\mathcal{S}_a(\mathcal{J}, \mathcal{J}') = \frac{\sum_j a_j a'_j}{\sqrt{\sum_j a_j^2 \sum_j {a'_j}^2}}",
            tex_template=VN_TEX_TEMPLATE,
            color=TEXT_PRIMARY
        ).scale(0.78).shift(LEFT * 3.4 + UP * 0.5)

        sa_title = vn_tex_bold("Chỉ dùng Magnitude (Biên độ)", color=ACCENT_CYAN, scale=0.48).next_to(formula_sa, UP, buff=0.4)
        sa_desc = vn_tex_italic("Không chứa thông tin góc pha", color=TEXT_MUTED, scale=0.45).next_to(formula_sa, DOWN, buff=0.4)

        # Right panel: Plot Sa
        ax_sa = Axes(
            x_range=[-40, 40, 10],
            y_range=[0, 1.2, 0.5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"color": GRID_LINE, "stroke_width": 1.2}
        ).shift(RIGHT * 3.4 + DOWN * 0.6)

        sa_plot_title = vn_tex_bold("Lực hút của Sa", color=TEXT_PRIMARY, scale=0.45).next_to(ax_sa, UP, buff=0.25)
        curve_sa = ax_sa.plot(
            lambda x: 0.9 * np.exp(-(x / 16)**2),
            color=ACCENT_CYAN, stroke_width=2.5
        )
        
        # Highlight broad attractor basin
        basin_rect = SurroundingRectangle(curve_sa, color=ACCENT_CYAN, stroke_width=1.5, fill_color=ACCENT_CYAN, fill_opacity=0.1)
        basin_lbl = vn_tex("Large attractor basin", color=ACCENT_CYAN, scale=0.38).next_to(basin_rect, UP, buff=0.1)

        self.play(
            FadeIn(sa_title),
            Write(formula_sa),
            FadeIn(sa_desc),
            run_time=1.5
        )

        # Subtitle 3 (16s - 24s)
        update_sub("Đường cong mượt, có vùng thu hút lớn --- dễ hội tụ", 5.0)

        self.play(
            FadeIn(ax_sa),
            FadeIn(sa_plot_title),
            Create(curve_sa),
            run_time=1.5
        )
        self.play(
            Create(basin_rect),
            FadeIn(basin_lbl),
            run_time=1.0
        )
        
        # Subtitle 4 (24s - 32s)
        update_sub("Phù hợp cho bước tìm thô vị trí ban đầu", 5.0)
        self.wait(1.8)

        # Clear Phase B elements
        self.play(
            FadeOut(sa_title),
            FadeOut(formula_sa),
            FadeOut(sa_desc),
            FadeOut(ax_sa),
            FadeOut(sa_plot_title),
            FadeOut(curve_sa),
            FadeOut(basin_rect),
            FadeOut(basin_lbl),
            run_time=0.8
        )

        # ============================================================
        # PHASE C: Hàm similarity DÙNG phase - Sphi (35s - 55s)
        # ============================================================
        # Subtitle 5 (32s - 42s)
        update_sub("Cách 2: so sánh có dùng phase --- chính xác hơn nhiều", 5.0)

        # Left panel: Formula Sphi
        formula_sphi = MathTex(
            r"\mathcal{S}_\phi(\mathcal{J}, \mathcal{J}') = \frac{\sum_j a_j a'_j \cos(\phi_j - \phi'_j - \vec{d}\cdot\vec{k}_j)}{\sqrt{\sum_j a_j^2 \sum_j {a'_j}^2}}",
            tex_template=VN_TEX_TEMPLATE,
            color=TEXT_PRIMARY
        ).scale(0.72).shift(LEFT * 3.4 + UP * 0.5)

        sphi_title = vn_tex_bold("Dùng thêm Phase (Góc pha)", color=ACCENT_LAVENDER, scale=0.48).next_to(formula_sphi, UP, buff=0.4)
        sphi_desc = vn_tex_italic("d: Vector dịch chuyển cần ước lượng", color=TEXT_MUTED, scale=0.42).next_to(formula_sphi, DOWN, buff=0.4)

        # Highlight cos(phi_j - phi'_j - d.k_j) inside the formula
        box_cos = SurroundingRectangle(formula_sphi[0][21:40], color=ACCENT_LAVENDER, stroke_width=1.5)

        # Right panel: Plot Sphi
        ax_sphi = Axes(
            x_range=[-40, 40, 10],
            y_range=[-0.5, 1.2, 0.5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"color": GRID_LINE, "stroke_width": 1.2}
        ).shift(RIGHT * 3.4 + DOWN * 0.6)

        sphi_plot_title = vn_tex_bold("Đỉnh nhọn và cực trị của Sphi", color=TEXT_PRIMARY, scale=0.45).next_to(ax_sphi, UP, buff=0.25)
        
        # High frequency oscillating curve with a sharp central peak
        curve_sphi = ax_sphi.plot(
            lambda x: 0.95 * np.exp(-(x / 20)**2) * np.cos(x / 2.2),
            color=ACCENT_LAVENDER, stroke_width=2.5
        )

        # Indicate side peak (false peak / side lobe)
        side_peak_pos = ax_sphi.c2p(-13.8, 0.65)
        side_arrow = Arrow(
            start=side_peak_pos + LEFT * 0.8 + UP * 0.8,
            end=side_peak_pos,
            color=ACCENT_CORAL, stroke_width=2.0, buff=0.05
        )
        side_lbl = vn_tex("Đỉnh giả (Side lobe)", color=ACCENT_CORAL, scale=0.35).next_to(side_arrow.get_start(), UP, buff=0.1)

        self.play(
            FadeIn(sphi_title),
            Write(formula_sphi),
            FadeIn(sphi_desc),
            run_time=1.5
        )
        self.play(Create(box_cos), run_time=0.8)

        # Subtitle 6 (42s - 50s)
        update_sub("Đường cong nhiều đỉnh --- nhưng đỉnh chính rất nhọn", 5.0)

        self.play(
            FadeIn(ax_sphi),
            FadeIn(sphi_plot_title),
            Create(curve_sphi),
            run_time=1.5
        )
        self.play(
            GrowArrow(side_arrow),
            FadeIn(side_lbl),
            run_time=1.0
        )
        self.wait(1.5)

        # Subtitle 7 (50s - 58s)
        update_sub("Phase còn cho phép ước lượng độ dịch chuyển d", 5.0)
        self.wait(1.5)

        # Clear Phase C elements
        self.play(
            FadeOut(sphi_title),
            FadeOut(formula_sphi),
            FadeOut(sphi_desc),
            FadeOut(box_cos),
            FadeOut(ax_sphi),
            FadeOut(sphi_plot_title),
            FadeOut(curve_sphi),
            FadeOut(side_arrow),
            FadeOut(side_lbl),
            run_time=0.8
        )

        # ============================================================
        # PHASE D: Ước lượng dịch chuyển - Estimated d (55s - 70s)
        # ============================================================
        # Subtitle 8 (58s - 66s)
        update_sub("Quanh vị trí đúng, ước lượng chính xác đến subpixel", 5.0)

        # Left panel: Matrix formula for estimated d
        formula_d = MathTex(
            r"\vec{d} = \frac{1}{\Gamma_{xx}\Gamma_{yy} - \Gamma_{xy}\Gamma_{yx}}"
            r"\begin{pmatrix}\Gamma_{yy} & -\Gamma_{yx}\\ -\Gamma_{xy} & \Gamma_{xx}\end{pmatrix}"
            r"\begin{pmatrix}\Phi_x \\ \Phi_y\end{pmatrix}",
            tex_template=VN_TEX_TEMPLATE,
            color=TEXT_PRIMARY
        ).scale(0.68).shift(LEFT * 3.4 + UP * 0.5)

        d_title = vn_tex_bold("Ước lượng độ lệch d", color=HIGHLIGHT_HOT, scale=0.48).next_to(formula_d, UP, buff=0.4)
        d_desc = vn_tex_italic("Giải hệ tuyến tính từ khai triển Taylor", color=TEXT_MUTED, scale=0.42).next_to(formula_d, DOWN, buff=0.4)

        # Right panel: Recreate Fig 2(c) Estimated displacement curve
        ax_d = Axes(
            x_range=[-20, 20, 5],
            y_range=[-10, 10, 5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"color": GRID_LINE, "stroke_width": 1.2}
        ).shift(RIGHT * 3.4 + DOWN * 0.6)

        d_plot_title = vn_tex_bold("Ước lượng d vs Lệch thực tế", color=TEXT_PRIMARY, scale=0.45).next_to(ax_d, UP, buff=0.25)

        # Piecewise sawtooth-like estimation curve
        # Correctly estimates between -6 and 6, then Jumps
        curve_d = ax_d.plot(
            lambda x: x if abs(x) <= 6 else (x - 14 if x > 6 else x + 14),
            discontinuities=[-6, 6],
            color=HIGHLIGHT_HOT, stroke_width=2.5
        )

        d_correct_pos = ax_d.c2p(0, 0)
        d_arrow = Arrow(
            start=d_correct_pos + UP * 1.0 + RIGHT * 0.8,
            end=d_correct_pos + UP * 0.15 + RIGHT * 0.15,
            color=ACCENT_CYAN, stroke_width=2.0, buff=0.05
        )
        d_lbl = vn_tex("Chính xác quanh 0", color=ACCENT_CYAN, scale=0.35).next_to(d_arrow.get_start(), UP, buff=0.1)

        self.play(
            FadeIn(d_title),
            Write(formula_d),
            FadeIn(d_desc),
            run_time=1.5
        )
        self.play(
            FadeIn(ax_d),
            FadeIn(d_plot_title),
            Create(curve_d),
            run_time=1.5
        )
        self.play(
            GrowArrow(d_arrow),
            FadeIn(d_lbl),
            run_time=1.0
        )
        self.wait(3.0)

        # Clear Phase D elements
        self.play(
            FadeOut(d_title),
            FadeOut(formula_d),
            FadeOut(d_desc),
            FadeOut(ax_d),
            FadeOut(d_plot_title),
            FadeOut(curve_d),
            FadeOut(d_arrow),
            FadeOut(d_lbl),
            run_time=0.8
        )

        # ============================================================
        # PHASE E: Trade-off Summary (70s - 75s)
        # ============================================================
        # Subtitle 9 (66s - 75s)
        update_sub("EBGM kết hợp cả hai: thô trước, tinh sau", 5.0)

        # Contrast Table cards layout
        card1 = RoundedRectangle(
            corner_radius=0.1, width=4.8, height=2.4, color=ACCENT_CYAN, stroke_width=1.5,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.9
        ).shift(LEFT * 2.8 + DOWN * 0.5)

        t1_title = vn_tex_bold("Similarity Sa (Biên độ)", color=ACCENT_CYAN, scale=0.5).move_to(card1.get_top() + DOWN * 0.35)
        t1_bullet1 = vn_tex("- Vùng thu hút lớn, trơn tru", color=TEXT_PRIMARY, scale=0.42).next_to(t1_title, DOWN, buff=0.25).align_to(t1_title, LEFT)
        t1_bullet2 = vn_tex("- Mục tiêu: Tìm kiếm THÔ (Coarse)", color=TEXT_PRIMARY, scale=0.42).next_to(t1_bullet1, DOWN, buff=0.18).align_to(t1_bullet1, LEFT)
        t1_bullet3 = vn_tex("- Khởi động hội tụ ban đầu", color=TEXT_PRIMARY, scale=0.42).next_to(t1_bullet2, DOWN, buff=0.18).align_to(t1_bullet2, LEFT)
        t1_grp = VGroup(t1_title, t1_bullet1, t1_bullet2, t1_bullet3)

        card2 = RoundedRectangle(
            corner_radius=0.1, width=4.8, height=2.4, color=ACCENT_LAVENDER, stroke_width=1.5,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.9
        ).shift(RIGHT * 2.8 + DOWN * 0.5)

        t2_title = vn_tex_bold("Similarity Sphi (Góc pha)", color=ACCENT_LAVENDER, scale=0.5).move_to(card2.get_top() + DOWN * 0.35)
        t2_bullet1 = vn_tex("- Cực trị nhọn, nhạy cảm sai lệch", color=TEXT_PRIMARY, scale=0.42).next_to(t2_title, DOWN, buff=0.25).align_to(t2_title, LEFT)
        t2_bullet2 = vn_tex("- Mục tiêu: Khớp TINH (Fine Refine)", color=TEXT_PRIMARY, scale=0.42).next_to(t2_bullet1, DOWN, buff=0.18).align_to(t2_bullet1, LEFT)
        t2_bullet3 = vn_tex("- Định vị cực kỳ chính xác subpixel", color=TEXT_PRIMARY, scale=0.42).next_to(t2_bullet2, DOWN, buff=0.18).align_to(t2_bullet2, LEFT)
        t2_grp = VGroup(t2_title, t2_bullet1, t2_bullet2, t2_bullet3)

        self.play(
            FadeIn(card1, shift=UP * 0.3),
            FadeIn(t1_grp, shift=UP * 0.2),
            run_time=0.8
        )
        self.play(
            FadeIn(card2, shift=UP * 0.3),
            FadeIn(t2_grp, shift=UP * 0.2),
            run_time=0.8
        )
        self.wait(3.5)

        # Cleanup
        self.play(
            FadeOut(title),
            FadeOut(Group(card1, card2)),
            FadeOut(VGroup(t1_grp, t2_grp)),
            run_time=0.8
        )
        self.wait(0.3)
