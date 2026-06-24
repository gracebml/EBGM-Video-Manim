"""
EBGM Video — Algorithm Detail Section
Scene 12: Face Representation — Individual Graph
Thời lượng dự kiến: 65s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)
  - Hoạt động trong conda env "vid"

Render command:
  manim -pql scene_12_individual_graph.py Scene12_IndividualGraph
  manim -pqh scene_12_individual_graph.py Scene12_IndividualGraph  # high quality
"""

from manim import *
import numpy as np
from _common import *

def make_mini_jet_compact(pos, color=ACCENT_CYAN):
    jet = VGroup()
    for nu in range(2):  # 2 disks only for extreme compactness
        disk = VGroup()
        for mu in range(8):
            sector = AnnularSector(
                inner_radius=0.1 + nu * 0.04,
                outer_radius=0.2 + nu * 0.04,
                start_angle=mu * PI/4,
                angle=PI/4,
                color=interpolate_color(ManimColor(color), ManimColor(TEXT_MUTED), 0.4),
                fill_opacity=0.5,
                stroke_color=BG_NAVY,
                stroke_width=0.3
            )
            disk.add(sector)
        disk.shift(UP * nu * 0.15)
        jet.add(disk)
    jet.rotate(25 * DEGREES, axis=RIGHT)
    jet.move_to(pos)
    return jet

class Scene12_IndividualGraph(Scene):
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
        # PHASE A: Khởi đầu & Câu hỏi mở (0s - 10s)
        # ============================================================
        # Title
        title = section_title("Biểu diễn khuôn mặt: Đồ thị đơn lẻ")
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=1.0)

        # Opening question
        question_line1 = vn_tex_bold("Làm sao tổ chức 40 hệ số phức tại nhiều điểm mốc", color=TEXT_PRIMARY, scale=0.6).shift(UP * 1.0)
        question_line2 = vn_tex_bold("thành một biểu diễn nhận diện khuôn mặt mạch lạc?", color=TEXT_PRIMARY, scale=0.6).next_to(question_line1, DOWN, buff=0.25)
        question_grp = VGroup(question_line1, question_line2)

        self.play(FadeIn(question_grp, shift=UP * 0.2), run_time=1.5)

        # Subtitle 1 (0s - 6s)
        update_sub("Bước 2: Biểu diễn khuôn mặt bằng một đồ thị", 4.5)
        self.wait(1.5)

        # Clear opening question
        self.play(FadeOut(question_grp), run_time=0.8)

        # ============================================================
        # PHASE B: Xây dựng Graph từng bước (10s - 35s)
        # ============================================================
        # Subtitle 2 (6s - 14s)
        update_sub("Các nút đặt ở những điểm mốc đặc trưng --- mắt, mũi, miệng", 5.0)

        # Landmark node positions
        nodes_pos = {
            0: np.array([-0.9, 0.8, 0]),   # L Eye
            1: np.array([0.9, 0.8, 0]),    # R Eye
            2: np.array([0.0, 0.1, 0]),     # Nose Tip
            3: np.array([-0.6, -0.5, 0]),  # L Mouth
            4: np.array([0.6, -0.5, 0]),   # R Mouth
            5: np.array([0.0, -1.2, 0]),    # Chin
            6: np.array([0.0, 1.6, 0]),     # Forehead
            7: np.array([-1.3, 0.2, 0]),   # L Cheek
            8: np.array([1.3, 0.2, 0])     # R Cheek
        }

        # Build visual node dots and labels
        nodes_grp = VGroup()
        for idx, pos in nodes_pos.items():
            dot = Dot(pos, radius=0.08, color=ACCENT_LAVENDER)
            nodes_grp.add(dot)

        # Display nodes sequentially
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in nodes_grp], lag_ratio=0.15),
            run_time=2.0
        )
        self.wait(1.0)

        # Subtitle 3 (14s - 22s)
        update_sub("Mỗi nút được gán một jet --- 40 hệ số mô tả đặc trưng cục bộ", 5.0)

        # Highlight Left Eye Node and show Gabor Jet right next to it
        eye_highlight = Circle(radius=0.18, color=HIGHLIGHT_HOT, stroke_width=2.0).move_to(nodes_pos[0])
        mini_jet = make_mini_jet_compact(nodes_pos[0] + LEFT * 0.9 + UP * 0.4, ACCENT_CYAN)
        mini_jet_lbl = MathTex(r"\mathcal{J}_n", tex_template=VN_TEX_TEMPLATE, color=ACCENT_CYAN).scale(0.7).next_to(mini_jet, UP, buff=0.1)

        self.play(
            Create(eye_highlight),
            FadeIn(mini_jet, shift=LEFT * 0.25),
            FadeIn(mini_jet_lbl, shift=LEFT * 0.25),
            run_time=1.2
        )
        self.wait(2.2)

        # Clear highlight and mini jet for edge drawing
        self.play(
            FadeOut(eye_highlight),
            FadeOut(mini_jet),
            FadeOut(mini_jet_lbl),
            run_time=0.8
        )

        # Subtitle 4 (22s - 32s)
        update_sub("Các cạnh nối các nút, mang nhãn là vector khoảng cách giữa chúng", 4.0)

        # Connections (Edges)
        edge_pairs = [
            (0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5),
            (0, 6), (1, 6), (0, 7), (3, 7), (1, 8), (4, 8)
        ]

        edges_grp = VGroup()
        for p1, p2 in edge_pairs:
            line = Line(nodes_pos[p1], nodes_pos[p2], color=GRID_LINE, stroke_width=1.5)
            edges_grp.add(line)

        # Display edges
        self.play(
            Create(edges_grp),
            run_time=2.0
        )
        self.wait(1.5)

        # Highlight single edge (L Eye -> Nose Tip)
        target_edge_idx = 1  # (0, 2)
        edge_highlight_line = Line(nodes_pos[0], nodes_pos[2], color=HIGHLIGHT_HOT, stroke_width=3.5)
        
        edge_arrow = Arrow(
            start=nodes_pos[2],
            end=nodes_pos[0],
            color=HIGHLIGHT_HOT, stroke_width=2.5, buff=0.1
        )
        edge_lbl = MathTex(
            r"\Delta\vec{x}_e = \vec{x}_n - \vec{x}_{n'}",
            tex_template=VN_TEX_TEMPLATE,
            color=HIGHLIGHT_HOT
        ).scale(0.6).next_to(edge_arrow.get_center(), LEFT, buff=0.25).shift(UP * 0.1)

        self.play(
            FadeIn(edge_highlight_line),
            GrowArrow(edge_arrow),
            FadeIn(edge_lbl, shift=LEFT * 0.15),
            run_time=1.2
        )
        self.wait(2.2)

        # Clear edge highlights
        self.play(
            FadeOut(edge_highlight_line),
            FadeOut(edge_arrow),
            FadeOut(edge_lbl),
            run_time=0.8
        )

        # ============================================================
        # PHASE C: Đồ thị hình học cấu trúc - Summary (35s - 55s)
        # ============================================================
        # Subtitle 5 (32s - 42s)
        update_sub("Đây là cấu trúc 'object-adapted graph'", 5.0)

        # Combine nodes and edges to shift left
        full_graph = VGroup(nodes_grp, edges_grp)
        self.play(
            full_graph.animate.scale(0.85).shift(LEFT * 3.4 + DOWN * 0.4),
            run_time=1.2
        )

        # Infographic tree layout on the right
        right_panel_x = 2.4
        
        info_title = vn_tex_bold("ĐỒ THỊ KHUÔN MẶT G = (V, E)", color=ACCENT_CYAN, scale=0.5).move_to(RIGHT * right_panel_x + UP * 1.5)
        
        v_title = vn_tex("- V: Tập hợp N nút mốc", color=TEXT_PRIMARY, scale=0.45).next_to(info_title, DOWN, buff=0.35).align_to(info_title, LEFT)
        v_sub = vn_tex("  Nhãn mỗi nút n = Gabor Jet Jn [40 số phức]", color=TEXT_MUTED, scale=0.4).next_to(v_title, DOWN, buff=0.18).align_to(v_title, LEFT)
        
        e_title = vn_tex("- E: Tập hợp các cạnh kết nối hình học", color=TEXT_PRIMARY, scale=0.45).next_to(v_sub, DOWN, buff=0.35).align_to(info_title, LEFT)
        e_sub = vn_tex("  Nhãn mỗi cạnh e = Vector 2D Δxe = xn - xn'", color=TEXT_MUTED, scale=0.4).next_to(e_title, DOWN, buff=0.18).align_to(e_title, LEFT)

        info_grp = VGroup(info_title, v_title, v_sub, e_title, e_sub)

        # Subtitle 6 (42s - 50s)
        update_sub("Tóm tắt: V = các điểm mốc, E = các kết nối hình học", 6.0)

        self.play(
            FadeIn(info_grp, shift=UP * 0.15),
            run_time=1.8
        )
        self.wait(3.5)

        # Clear Phase C elements
        self.play(
            FadeOut(full_graph),
            FadeOut(info_grp),
            run_time=0.8
        )

        # ============================================================
        # PHASE D: Pose-specific Graphs (55s - 65s)
        # ============================================================
        # Subtitle 7 (50s - 58s)
        update_sub("Mỗi tư thế đầu (frontal, nghiêng, profile) có graph riêng", 5.0)

        # Build 3 small graphs side-by-side
        # Helper to generate custom face graph
        def make_mini_face_graph(pos, scale, type_str="frontal"):
            g_nodes = VGroup()
            g_edges = VGroup()
            
            # frontal pose nodes
            n_pos = {
                0: np.array([-0.6, 0.5, 0]),
                1: np.array([0.6, 0.5, 0]),
                2: np.array([0, 0.0, 0]),
                3: np.array([-0.4, -0.4, 0]),
                4: np.array([0.4, -0.4, 0]),
                5: np.array([0, -0.8, 0]),
            }
            
            if type_str == "half":
                # Shifted and asymmetrical
                n_pos = {
                    0: np.array([-0.5, 0.5, 0]),
                    1: np.array([0.3, 0.5, 0]),
                    2: np.array([-0.1, 0.0, 0]),
                    3: np.array([-0.4, -0.4, 0]),
                    4: np.array([0.2, -0.4, 0]),
                    5: np.array([-0.1, -0.8, 0]),
                }
            elif type_str == "profile":
                # Flat side view, some nodes merged/obscured
                n_pos = {
                    0: np.array([-0.3, 0.5, 0]),
                    2: np.array([0.2, 0.0, 0]),
                    3: np.array([-0.2, -0.4, 0]),
                    5: np.array([-0.1, -0.8, 0]),
                }

            # Draw nodes
            for k, p in n_pos.items():
                dot = Dot(p * scale + pos, radius=0.05, color=ACCENT_LAVENDER)
                g_nodes.add(dot)

            # Draw edges
            pairs = []
            if type_str in ["frontal", "half"]:
                pairs = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
            else:  # profile
                pairs = [(0, 2), (2, 3), (3, 5)]

            for p1, p2 in pairs:
                # profile has 4 nodes but indices mapped differently, let's map safely
                if p1 in n_pos and p2 in n_pos:
                    line = Line(n_pos[p1] * scale + pos, n_pos[p2] * scale + pos, color=GRID_LINE, stroke_width=1.0)
                    g_edges.add(line)

            lbl = vn_tex_bold(type_str.capitalize(), color=TEXT_MUTED, scale=0.45).next_to(g_nodes, DOWN, buff=0.3)
            return VGroup(g_edges, g_nodes, lbl), n_pos[2] * scale + pos # return graph and Nose Tip pos

        g_frontal, nose_frontal = make_mini_face_graph(LEFT * 4.2 + DOWN * 0.4, 0.95, "frontal")
        g_half, nose_half = make_mini_face_graph(ORIGIN + DOWN * 0.4, 0.95, "half")
        g_profile, nose_profile = make_mini_face_graph(RIGHT * 4.2 + DOWN * 0.4, 0.95, "profile")

        self.play(
            FadeIn(g_frontal),
            FadeIn(g_half),
            FadeIn(g_profile),
            run_time=1.8
        )

        # Subtitle 8 (58s - 65s)
        update_sub("Tương ứng giữa các pose được người thiết kế chỉ định", 5.0)

        # Connect nose tip nodes with dotted lavender arrows to show correspondence
        corres_arrow1 = DashedLine(
            start=nose_frontal, end=nose_half,
            color=ACCENT_CYAN, stroke_width=1.2
        )
        corres_arrow2 = DashedLine(
            start=nose_half, end=nose_profile,
            color=ACCENT_CYAN, stroke_width=1.2
        )

        corres_lbl = vn_tex_italic("Correspondences (Đường tương ứng giữa các pose)", color=ACCENT_CYAN, scale=0.38).to_edge(UP, buff=1.6)

        self.play(
            Create(corres_arrow1),
            Create(corres_arrow2),
            FadeIn(corres_lbl, shift=DOWN * 0.1),
            run_time=1.5
        )
        self.wait(2.2)

        # Cleanup
        self.play(
            FadeOut(title),
            FadeOut(g_frontal),
            FadeOut(g_half),
            FadeOut(g_profile),
            FadeOut(corres_arrow1),
            FadeOut(corres_arrow2),
            FadeOut(corres_lbl),
            run_time=0.8
        )
        self.wait(0.3)
