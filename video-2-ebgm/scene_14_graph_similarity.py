"""
EBGM Video — Algorithm Detail Section
Scene 14: Graph Similarity Function
Thời lượng dự kiến: 55s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)
  - Hoạt động trong conda env "vid"

Render command:
  manim -pql scene_14_graph_similarity.py Scene14_GraphSimilarity
  manim -pqh scene_14_graph_similarity.py Scene14_GraphSimilarity  # high quality
"""

from manim import *
import numpy as np
from _common import *

def make_simple_wireframe(pos, color, scale=1.0, stretch_x=1.0, stretch_y=1.0, noise=0.0):
    g = VGroup()
    # 6 baseline nodes
    n_pos = {
        0: np.array([-0.6 * stretch_x, 0.5 * stretch_y, 0]),
        1: np.array([0.6 * stretch_x, 0.5 * stretch_y, 0]),
        2: np.array([0, 0.0, 0]),
        3: np.array([-0.4 * stretch_x, -0.4 * stretch_y, 0]),
        4: np.array([0.4 * stretch_x, -0.4 * stretch_y, 0]),
        5: np.array([0, -0.8 * stretch_y, 0]),
    }
    
    # Add optional random noise to simulate distortion
    if noise > 0.0:
        np.random.seed(42)  # Seed for deterministic distortion
        for k in n_pos:
            n_pos[k] = n_pos[k] + np.random.uniform(-noise, noise, 3)
            n_pos[k][2] = 0.0  # keep on z=0
            
    # Draw edges
    pairs = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
    for p1, p2 in pairs:
        line = Line(
            (n_pos[p1] * scale) + pos,
            (n_pos[p2] * scale) + pos,
            color=color, stroke_width=1.5
        )
        g.add(line)
        
    # Draw nodes
    for k, p in n_pos.items():
        dot = Dot(
            (p * scale) + pos,
            radius=0.06, color=color
        )
        g.add(dot)
    return g

class Scene14_GraphSimilarity(Scene):
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
        # PHASE A: Setup so sánh Image Graph & FBG (0s - 10s)
        # ============================================================
        # Title
        title = section_title("Hàm tương đồng đồ thị")
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=1.0)

        # Subtitle 1 (0s - 6s)
        update_sub("Làm sao đo lường: image graph khớp với FBG đến đâu?", 5.0)

        # Setup visual: Image Graph vs FBG
        g_image = make_simple_wireframe(LEFT * 3.4 + DOWN * 0.3, color=ACCENT_CYAN, scale=1.4)
        lbl_g_image = vn_tex("Image Graph GI", color=ACCENT_CYAN, scale=0.45).next_to(g_image, UP, buff=0.3)

        # Stacked FBG representer
        fbg_rep = VGroup()
        for m in range(3):
            g_layer = make_simple_wireframe(
                ORIGIN, color=interpolate_color(ManimColor(ACCENT_BLUE), ManimColor(ACCENT_LAVENDER), m/2),
                scale=1.4
            ).set_opacity(0.6)
            g_layer.shift(UP * m * 0.25 + RIGHT * m * 0.06)
            fbg_rep.add(g_layer)
        fbg_rep.rotate(20 * DEGREES, axis=RIGHT).scale(0.85).move_to(RIGHT * 3.4 + DOWN * 0.5)
        lbl_fbg = vn_tex("Bunch Graph B", color=ACCENT_LAVENDER, scale=0.45).next_to(fbg_rep, UP, buff=0.35)

        vs_arrow = DoubleArrow(LEFT * 1.0 + DOWN * 0.3, RIGHT * 1.0 + DOWN * 0.3, color=TEXT_MUTED, stroke_width=2.0)
        vs_lbl = vn_tex_italic("So khớp?", color=TEXT_MUTED, scale=0.42).next_to(vs_arrow, UP, buff=0.15)

        self.play(
            FadeIn(g_image, shift=RIGHT * 0.25),
            FadeIn(lbl_g_image, shift=RIGHT * 0.25),
            FadeIn(fbg_rep, shift=LEFT * 0.25),
            FadeIn(lbl_fbg, shift=LEFT * 0.25),
            Create(vs_arrow),
            FadeIn(vs_lbl),
            run_time=1.8
        )
        self.wait(1.5)

        # Clear Phase A elements
        self.play(
            FadeOut(g_image), FadeOut(lbl_g_image),
            FadeOut(fbg_rep), FadeOut(lbl_fbg),
            FadeOut(vs_arrow), FadeOut(vs_lbl),
            run_time=0.8
        )

        # ============================================================
        # PHASE B: Công thức Hàm Mục Tiêu (10s - 30s)
        # ============================================================
        # Subtitle 2 (6s - 14s)
        update_sub("Công thức gồm hai phần đối lập nhau", 4.0)

        # Core Formula: Jet Similarity - Distortion Penalty
        formula = MathTex(
            r"\mathcal{S}_B(\mathcal{G}^I, \mathcal{B}) = ",                                                                                                        # Index 0
            r"\frac{1}{N}\sum_n \max_m\left(\mathcal{S}_\phi(\mathcal{J}_n^I, \mathcal{J}_n^{B_m})\right)",                                                          # Index 1: Jet similarity
            r"-",                                                                                                                                                    # Index 2
            r"\frac{\lambda}{E}\sum_e \frac{(\Delta\mathbf{x}_e^I - \Delta\mathbf{x}_e^B)^2}{(\Delta\mathbf{x}_e^B)^2}",                                              # Index 3: Distortion penalty
            tex_template=VN_TEX_TEMPLATE,
            color=TEXT_PRIMARY
        ).scale(0.72).move_to(UP * 0.4)

        self.play(Write(formula), run_time=2.2)
        self.wait(0.5)

        # Subtitle 3 (14s - 22s)
        update_sub("Phần thứ nhất: trung bình độ tương đồng jet --- chọn expert tốt nhất", 5.0)

        # Highlight Part 1: Jet Similarity
        box_jet = SurroundingRectangle(formula[1], color=ACCENT_CYAN, stroke_width=1.8)
        lbl_jet = vn_tex_bold("Jet Similarity (Độ tương đồng đặc trưng)", color=ACCENT_CYAN, scale=0.45)
        lbl_jet.next_to(box_jet, UP, buff=0.45)
        desc_jet = vn_tex_italic("Chọn expert tốt nhất từ chùm tại mỗi nút mốc", color=ACCENT_CYAN, scale=0.38).next_to(lbl_jet, DOWN, buff=0.15)

        self.play(
            Create(box_jet),
            FadeIn(lbl_jet, shift=UP * 0.15),
            FadeIn(desc_jet, shift=UP * 0.1),
            run_time=1.2
        )
        self.wait(2.2)

        # Subtitle 4 (22s - 30s)
        update_sub("Phần thứ hai: hình phạt cho biến dạng cấu trúc", 5.0)

        # Highlight Part 2: Distortion Penalty
        box_dist = SurroundingRectangle(formula[3], color=ACCENT_CORAL, stroke_width=1.8)
        lbl_dist = vn_tex_bold("Distortion Penalty (Phạt biến dạng hình học)", color=ACCENT_CORAL, scale=0.45)
        lbl_dist.next_to(box_dist, DOWN, buff=0.45)
        desc_dist = vn_tex_italic("Độ biến dạng khoảng cách giữa các nút của đồ thị GI so với Bunch Graph", color=ACCENT_CORAL, scale=0.38).next_to(lbl_dist, DOWN, buff=0.15)

        self.play(
            FadeOut(box_jet), FadeOut(lbl_jet), FadeOut(desc_jet),
            Create(box_dist),
            FadeIn(lbl_dist, shift=DOWN * 0.15),
            FadeIn(desc_dist, shift=DOWN * 0.1),
            run_time=1.2
        )
        self.wait(2.5)

        # Clear highlights for Phase C trade-off visuals
        self.play(
            FadeOut(box_dist), FadeOut(lbl_dist), FadeOut(desc_dist),
            formula.animate.scale(0.85).to_edge(UP, buff=1.3),
            run_time=1.0
        )

        # ============================================================
        # PHASE C: Mô phỏng mục tiêu tối ưu - Trade-off configs (30s - 55s)
        # ============================================================
        # Subtitle 5 (30s - 38s)
        update_sub("Quá méo? Score giảm. Quá cứng? Cũng không khớp đặc trưng", 5.0)

        # Layout for Config demonstration
        # Left: Graph configuration
        # Right: Score card & Gauge meter
        gauge_bg = RoundedRectangle(
            corner_radius=0.08, width=4.0, height=0.28, color=TEXT_MUTED, stroke_width=1.0,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.7
        ).shift(RIGHT * 3.2 + DOWN * 0.5)
        gauge_lbl = vn_tex_bold("TỔNG ĐIỂM SCORE (Sa)", color=TEXT_PRIMARY, scale=0.42).next_to(gauge_bg, UP, buff=0.2)

        # Setup dynamic fill
        def get_gauge_fill(percentage, color=ACCENT_CYAN):
            if percentage <= 0.01:
                return VMobject()
            width_fill = percentage * 3.92
            fill = RoundedRectangle(
                corner_radius=0.06, width=width_fill, height=0.22, color=color, stroke_width=0.0,
                fill_color=color, fill_opacity=0.9
            ).move_to(gauge_bg.get_left() + RIGHT * (width_fill / 2 + 0.04))
            return fill

        # Config 1: Distorted
        graph_c1 = make_simple_wireframe(LEFT * 3.2 + DOWN * 0.5, color=ACCENT_CORAL, scale=1.5, noise=0.35)
        lbl_c1 = vn_tex_bold("Cấu hình 1: Quá biến dạng", color=ACCENT_CORAL, scale=0.45).next_to(graph_c1, UP, buff=0.3)
        bullet_c1_1 = vn_tex("+ Feature Match: Cực cao (90\%)", color=ACCENT_CYAN, scale=0.38).shift(RIGHT * 3.2 + DOWN * 1.2).align_to(gauge_lbl, LEFT)
        bullet_c1_2 = vn_tex("- Distortion Penalty: Khổng lồ (85\%)", color=ACCENT_CORAL, scale=0.38).next_to(bullet_c1_1, DOWN, buff=0.15).align_to(bullet_c1_1, LEFT)

        fill_c1 = get_gauge_fill(0.15, ACCENT_CORAL)

        self.play(
            FadeIn(graph_c1),
            FadeIn(lbl_c1, shift=UP * 0.1),
            FadeIn(gauge_bg),
            FadeIn(gauge_lbl),
            FadeIn(fill_c1),
            FadeIn(bullet_c1_1),
            FadeIn(bullet_c1_2),
            run_time=1.5
        )
        self.wait(2.2)

        # Subtitle 6 (38s - 46s)
        update_sub("Tham số lambda điều chỉnh sự cân bằng giữa hai phần", 4.0)

        # Transition to Config 2: Rigid
        graph_c2 = make_simple_wireframe(LEFT * 3.2 + DOWN * 0.5, color=ACCENT_BLUE, scale=1.5, noise=0.0)
        lbl_c2 = vn_tex_bold("Cấu hình 2: Quá cứng nhắc (Rigid)", color=ACCENT_BLUE, scale=0.45).next_to(graph_c2, UP, buff=0.3)
        bullet_c2_1 = vn_tex("- Feature Match: Rất thấp (30\%)", color=ACCENT_CORAL, scale=0.38).shift(RIGHT * 3.2 + DOWN * 1.2).align_to(gauge_lbl, LEFT)
        bullet_c2_2 = vn_tex("+ Distortion Penalty: Bằng 0 (0\%)", color=ACCENT_CYAN, scale=0.38).next_to(bullet_c2_1, DOWN, buff=0.15).align_to(bullet_c2_1, LEFT)
        
        fill_c2 = get_gauge_fill(0.30, ACCENT_BLUE)

        self.play(
            ReplacementTransform(graph_c1, graph_c2),
            ReplacementTransform(lbl_c1, lbl_c2),
            ReplacementTransform(bullet_c1_1, bullet_c2_1),
            ReplacementTransform(bullet_c1_2, bullet_c2_2),
            ReplacementTransform(fill_c1, fill_c2),
            run_time=1.2
        )
        self.wait(2.2)

        # Subtitle 7 (46s - 55s)
        update_sub("Tối đa hóa hàm này = tìm đồ thị khớp ảnh nhất", 5.0)

        # Transition to Config 3: Balanced
        graph_c3 = make_simple_wireframe(LEFT * 3.2 + DOWN * 0.5, color=ACCENT_MINT, scale=1.5, stretch_x=1.05, stretch_y=0.98, noise=0.08)
        lbl_c3 = vn_tex_bold("Cấu hình 3: Cân bằng tối ưu", color=ACCENT_MINT, scale=0.45).next_to(graph_c3, UP, buff=0.3)
        bullet_c3_1 = vn_tex("+ Feature Match: Rất tốt (82\%)", color=ACCENT_CYAN, scale=0.38).shift(RIGHT * 3.2 + DOWN * 1.2).align_to(gauge_lbl, LEFT)
        bullet_c3_2 = vn_tex("+ Distortion Penalty: Rất nhỏ (10\%)", color=ACCENT_CYAN, scale=0.38).next_to(bullet_c3_1, DOWN, buff=0.15).align_to(bullet_c3_1, LEFT)

        fill_c3 = get_gauge_fill(0.72, ACCENT_MINT)
        
        conclusion_lbl = vn_tex_bold(
            "Tối ưu hoá = Vừa khớp đặc trưng cục bộ, vừa giữ cấu trúc hình học!",
            color=ACCENT_CYAN, scale=0.45
        ).to_edge(DOWN, buff=1.3)

        self.play(
            ReplacementTransform(graph_c2, graph_c3),
            ReplacementTransform(lbl_c2, lbl_c3),
            ReplacementTransform(bullet_c2_1, bullet_c3_1),
            ReplacementTransform(bullet_c2_2, bullet_c3_2),
            ReplacementTransform(fill_c2, fill_c3),
            FadeIn(conclusion_lbl, shift=UP * 0.15),
            run_time=1.2
        )
        self.wait(3.5)

        # Cleanup
        self.play(
            FadeOut(title),
            FadeOut(formula),
            FadeOut(graph_c3),
            FadeOut(lbl_c3),
            FadeOut(gauge_bg),
            FadeOut(gauge_lbl),
            FadeOut(fill_c3),
            FadeOut(bullet_c3_1),
            FadeOut(bullet_c3_2),
            FadeOut(conclusion_lbl),
            run_time=0.8
        )
        self.wait(0.3)
