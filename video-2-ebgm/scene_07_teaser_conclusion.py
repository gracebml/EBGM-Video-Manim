"""
EBGM Video — Overview Section
Scene 7: Kết thúc Overview & Teaser
Thời lượng dự kiến: 15s

 YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts
  - XeLaTeX (thường có sẵn trong TeX Live)

Render command:
  manim -pql scene_07_teaser_conclusion.py Scene7_TeaserConclusion
  manim -pqh scene_07_teaser_conclusion.py Scene7_TeaserConclusion  # high quality
"""

from manim import *
import numpy as np
from _common import *

def make_detailed_graph(color=ACCENT_CYAN, scale=1.0):
    """Detailed facial landmark graph with 10 nodes for high visual quality."""
    p_forehead = np.array([0, 1.0, 0])
    p_eyebrow_l = np.array([-0.4, 0.6, 0])
    p_eyebrow_r = np.array([0.4, 0.6, 0])
    p_eye_l = np.array([-0.35, 0.3, 0])
    p_eye_r = np.array([0.35, 0.3, 0])
    p_nose_bridge = np.array([0, 0.2, 0])
    p_nose_tip = np.array([0, -0.2, 0])
    p_mouth_l = np.array([-0.3, -0.6, 0])
    p_mouth_r = np.array([0.3, -0.6, 0])
    p_chin = np.array([0, -1.0, 0])
    
    node_points = [
        p_forehead, p_eyebrow_l, p_eyebrow_r, p_eye_l, p_eye_r,
        p_nose_bridge, p_nose_tip, p_mouth_l, p_mouth_r, p_chin
    ]
    
    nodes = VGroup(*[Dot(point=pt, radius=0.06, color=color) for pt in node_points])
    
    # Connecting edges mathematically
    edge_pairs = [
        (0, 1), (0, 2), (1, 2), (1, 3), (2, 4),
        (3, 4), (3, 5), (4, 5), (5, 6), (3, 6),
        (4, 6), (6, 7), (6, 8), (7, 8), (7, 9), (8, 9)
    ]
    
    edges = VGroup(*[
        Line(node_points[u], node_points[v], color=color, stroke_width=1.5).set_opacity(0.4)
        for u, v in edge_pairs
    ])
    
    return VGroup(edges, nodes).scale(scale)

class Scene7_TeaserConclusion(Scene):
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

        # === Phase A: Promise summary (0s - 8s) ===
        update_sub("EBGM --- nén biến đổi, làm nổi đặc trưng phân biệt", 8.0)

        # Detailed face graph
        detailed_graph = make_detailed_graph(color=ACCENT_CYAN, scale=1.4).move_to(UP * 0.5)
        
        # Add a slow rotation to make it feel alive and professional
        detailed_graph.add_updater(lambda m, dt: m.rotate(dt * 0.12, about_point=m.get_center()))
        
        # Bottom academic text
        promise_lbl = vn_tex_bold(
            "Collapse the variance \\quad \\cdot \\quad Emphasize discriminating features",
            color=ACCENT_CYAN, scale=0.55
        ).move_to(DOWN * 1.8)

        self.play(
            Create(detailed_graph[0]), # edges
            LaggedStart(*[GrowFromCenter(n) for n in detailed_graph[1]], lag_ratio=0.15),
            run_time=2.0
        )
        self.play(FadeIn(promise_lbl, shift=UP * 0.15), run_time=1.0)
        self.wait(4.6)

        # Remove phase A updater and elements
        detailed_graph.remove_updater(detailed_graph.updaters[0])
        self.play(
            FadeOut(detailed_graph),
            FadeOut(promise_lbl),
            run_time=0.8
        )

        # === Phase B: Teaser (8s - 15s) ===
        update_sub("Tiếp theo: đi sâu vào từng thành phần của hệ thống", 7.0)

        teaser_1 = vn_tex_bold("Tiếp theo: Khám phá chi tiết hệ thống EBGM", color=TEXT_PRIMARY, scale=0.68)
        teaser_2 = vn_tex(
            "Gabor Wavelets \\quad \\cdot \\quad Face Representation \\quad \\cdot \\quad Matching \\quad \\cdot \\quad Recognition",
            color=ACCENT_LAVENDER, scale=0.45
        )
        teaser_grp = VGroup(teaser_1, teaser_2).arrange(DOWN, buff=0.35).move_to(UP * 0.2)

        arrow = Arrow(LEFT * 0.6, RIGHT * 0.6, color=ACCENT_LAVENDER, stroke_width=4.0).scale(1.2)
        arrow.next_to(teaser_grp, DOWN, buff=0.7)

        self.play(
            Write(teaser_1),
            run_time=1.8
        )
        self.play(
            FadeIn(teaser_2, shift=UP*0.1),
            run_time=1.2
        )
        self.play(
            GrowArrow(arrow),
            Flash(arrow.get_end(), color=ACCENT_LAVENDER, flash_radius=0.45),
            run_time=1.2
        )
        self.wait(2.4)

        # Final FadeOut of all mobjects in scene
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)
