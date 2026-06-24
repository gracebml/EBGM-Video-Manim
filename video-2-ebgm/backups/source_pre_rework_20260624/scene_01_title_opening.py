"""
EBGM Video — Overview Section
Scene 1: Title Opening
Thời lượng dự kiến: 12s

 YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts
  - XeLaTeX (thường có sẵn trong TeX Live)

Render command:
  manim -pql scene_01_title_opening.py Scene1_TitleOpening
  manim -pqh scene_01_title_opening.py Scene1_TitleOpening  # high quality
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# MAIN SCENE
# ============================================================
class Scene1_TitleOpening(Scene):
    def construct(self):
        # Set dark navy background
        self.camera.background_color = BG_NAVY

        # Seed for reproducible random layout
        np.random.seed(42)

        # === Phase A: Grow abstract dots & graph (0s - 3s) ===
        dots = VGroup(*[
            Dot(
                point=np.array([
                    np.random.uniform(-3.5, 3.5),
                    np.random.uniform(-2.0, 2.0),
                    0
                ]),
                color=ACCENT_CYAN if i % 2 == 0 else ACCENT_LAVENDER,
                radius=0.06
            )
            for i in range(12)
        ])

        abstract_edges_indices = [
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
            (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
            (0, 5), (1, 6), (2, 7), (3, 9), (4, 10), (8, 11)
        ]

        edges = VGroup(*[
            Line(
                dots[start].get_center(),
                dots[end].get_center(),
                color=ACCENT_BLUE,
                stroke_width=1.5,
                stroke_opacity=0.6
            )
            for start, end in abstract_edges_indices
        ])

        self.play(
            LaggedStart(
                *[GrowFromCenter(dot) for dot in dots],
                lag_ratio=0.08,
                run_time=1.0
            )
        )
        self.play(Create(edges, run_time=1.2))
        self.wait(0.8)

        # === Phase B: Morph into structured facial grid (3s - 6s) ===
        try:
            face_outline = SVGMobject("assets/face_silhouette.svg").set_color(ACCENT_BLUE).set_opacity(0.4)
        except (FileNotFoundError, OSError):
            face_outline = VGroup(
                Ellipse(width=3.2, height=4.2, color=ACCENT_BLUE, stroke_width=2.5, fill_opacity=0.12),
                Dot(point=[-0.6, 0.5, 0], radius=0.12, color=ACCENT_BLUE),
                Dot(point=[0.6, 0.5, 0], radius=0.12, color=ACCENT_BLUE),
                Line([0.0, 0.5, 0], [0.0, -0.2, 0], color=ACCENT_BLUE, stroke_width=2.5),
                Line([0.0, -0.2, 0], [0.25, -0.2, 0], color=ACCENT_BLUE, stroke_width=2.5),
                Arc(radius=0.5, start_angle=-PI/6, angle=-2*PI/3, color=ACCENT_BLUE, stroke_width=2.5).shift(DOWN * 0.8),
            ).set_opacity(0.4)

        landmark_positions = [
            [-0.8, 1.4, 0], [0.0, 1.6, 0], [0.8, 1.4, 0],
            [-0.9, 0.5, 0], [-0.6, 0.5, 0], [0.6, 0.5, 0],
            [0.9, 0.5, 0], [0.0, 0.5, 0], [0.2, -0.2, 0],
            [-0.4, -0.8, 0], [0.0, -1.0, 0], [0.4, -0.8, 0]
        ]

        facial_edges_indices = [
            (0, 1), (1, 2),
            (0, 3), (3, 4), (1, 4), (1, 5), (5, 6), (2, 6),
            (4, 7), (5, 7), (7, 8),
            (8, 9), (8, 10), (8, 11),
            (9, 10), (10, 11),
            (3, 9), (6, 11)
        ]

        target_dots = VGroup(*[
            Dot(point=np.array(pos), color=ACCENT_LAVENDER, radius=0.07)
            for pos in landmark_positions
        ])

        target_edges = VGroup(*[
            Line(
                target_dots[start].get_center(),
                target_dots[end].get_center(),
                color=ACCENT_LAVENDER,
                stroke_width=2.0
            )
            for start, end in facial_edges_indices
        ])

        self.play(FadeIn(face_outline, run_time=0.8))
        self.play(
            Transform(dots, target_dots),
            Transform(edges, target_edges),
            run_time=1.8
        )
        self.wait(0.4)

        # === Phase C: Title Reveal & Citation (6s - 12s) ===
        # All text via LaTeX (Latin Modern Roman)
        title_1 = vn_tex("FACE RECOGNITION", color=TEXT_PRIMARY, scale=0.9)
        title_2 = vn_tex("BY", color=TEXT_PRIMARY, scale=0.65)

        # Signature title in lavender
        el_text = vn_tex("ELASTIC", color=ACCENT_LAVENDER)
        bg_text = vn_tex("BUNCH GRAPH", color=ACCENT_LAVENDER)
        ma_text = vn_tex("MATCHING", color=ACCENT_LAVENDER)

        title_main = VGroup(el_text, bg_text, ma_text).arrange(RIGHT, buff=0.25).scale(1.05)

        # Underlines under ELASTIC and BUNCH GRAPH
        line_el = Line(
            el_text.get_corner(DL) + DOWN * 0.08,
            el_text.get_corner(DR) + DOWN * 0.08,
            color=ACCENT_CYAN, stroke_width=1.5
        )
        line_bg = Line(
            bg_text.get_corner(DL) + DOWN * 0.08,
            bg_text.get_corner(DR) + DOWN * 0.08,
            color=ACCENT_CYAN, stroke_width=1.5
        )

        title_group = VGroup(title_1, title_2, title_main).arrange(DOWN, buff=0.35)
        title_group.move_to(ORIGIN + UP * 0.4)

        line_el.move_to(el_text.get_bottom() + DOWN * 0.08)
        line_bg.move_to(bg_text.get_bottom() + DOWN * 0.08)

        # Citation — italic Latin Modern
        citation = vn_tex_italic(
            r"Wiskott $\cdot$ Fellous $\cdot$ Kr{\"u}ger $\cdot$ von der Malsburg\quad---\quad 1999",
            color=TEXT_MUTED, scale=0.55
        )
        citation.next_to(title_group, DOWN, buff=0.8)

        # Fade out face elements, reveal title
        self.play(
            FadeOut(face_outline, run_time=0.6),
            FadeOut(dots, run_time=0.6),
            FadeOut(edges, run_time=0.6)
        )

        self.play(
            Write(title_1),
            Write(title_2),
            Write(title_main),
            Create(line_el),
            Create(line_bg),
            run_time=2.2
        )

        self.play(FadeIn(citation, shift=UP * 0.2), run_time=0.8)
        self.wait(3.5)

        # End Scene Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)
