"""
EBGM Video — Overview Section
Scene 2: Bài toán Face Recognition
Thời lượng dự kiến: 50s

 YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts
  - XeLaTeX (thường có sẵn trong TeX Live)

Render command:
  manim -pql scene_02_face_recognition.py Scene2_FaceRecognition
  manim -pqh scene_02_face_recognition.py Scene2_FaceRecognition  # high quality
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# LOCAL HELPERS
# ============================================================
def make_tiny_face(color=ACCENT_BLUE, scale=0.5, opacity=0.2):
    """Creates a stylized simplified facial sketch for illustrations."""
    face = VGroup(
        Ellipse(width=1.6, height=2.1, color=color, stroke_width=1.5, fill_opacity=0.1),
        Dot(point=[-0.3, 0.25, 0], radius=0.06, color=color),
        Dot(point=[0.3, 0.25, 0], radius=0.06, color=color),
        Line([0.0, 0.25, 0], [0.0, -0.1, 0], color=color, stroke_width=1.5),
        Arc(radius=0.25, start_angle=-PI/6, angle=-2*PI/3, color=color, stroke_width=1.5).shift(DOWN * 0.4),
    )
    return face.scale(scale).set_opacity(opacity)

# ============================================================
# MAIN SCENE
# ============================================================
class Scene2_FaceRecognition(Scene):
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

        # === Phase A: Câu hỏi mở & Parallax (0s - 8s) ===
        np.random.seed(10)
        tiny_faces = VGroup()
        for _ in range(5):
            face = make_tiny_face(
                color=ACCENT_BLUE,
                scale=np.random.uniform(0.35, 0.65),
                opacity=np.random.uniform(0.08, 0.18)
            )
            face.move_to(np.array([
                np.random.uniform(4, 8),
                np.random.uniform(-2.5, 2.5),
                0
            ]))
            tiny_faces.add(face)

        self.add(tiny_faces)

        drift_anim = [
            face.animate.shift(LEFT * np.random.uniform(10, 14))
            for face in tiny_faces
        ]

        # Question text — LaTeX
        question = vn_tex(
            "Máy tính nhận diện khuôn mặt như thế nào?",
            color=TEXT_PRIMARY, scale=0.85
        )

        # Subtitle 0s - 4s
        new_sub = make_subtitle("Máy tính nhận diện khuôn mặt như thế nào?")
        self.play(FadeIn(new_sub, shift=UP * 0.15), run_time=0.4)
        self.current_sub = new_sub

        self.play(
            Write(question),
            *drift_anim,
            run_time=3.6,
            rate_func=linear
        )

        # Transform question into Section Title (4s - 8s)
        sec_title = section_title("Face Recognition --- Hai nhánh chính")
        sec_title.to_edge(UP, buff=0.5)

        update_sub("Bài toán có hai nhánh chính", 4.0)

        self.play(
            ReplacementTransform(question, sec_title),
            FadeOut(tiny_faces, run_time=0.8)
        )
        self.wait(0.2)

        # === Phase B: Split-screen 2 nhánh (8s - 50s) ===
        divider = Line(UP * 2.2, DOWN * 2.2, color=ACCENT_BLUE, stroke_width=1.5).set_opacity(0.35)
        self.play(Create(divider), run_time=0.8)

        # --- Left Side: Verification ---
        left_header = vn_tex_bold("VERIFICATION 1:1", color=ACCENT_CYAN, scale=0.7)
        left_sub_label = vn_tex("(Xác thực)", color=TEXT_MUTED, scale=0.5)
        left_title = VGroup(left_header, left_sub_label).arrange(DOWN, buff=0.1)
        left_title.move_to(np.array([-3.5, 2.0, 0]))

        left_q = vn_tex_italic("Đúng là họ không?", color=TEXT_PRIMARY, scale=0.6)
        left_q.move_to(np.array([-3.5, 1.4, 0]))

        # Face box
        face_sample = make_tiny_face(color=ACCENT_BLUE, scale=0.5, opacity=0.7)
        face_box = Rectangle(width=1.3, height=1.6, color=ACCENT_BLUE, stroke_width=1.5,
                             fill_opacity=0.05, fill_color=ACCENT_BLUE)
        face_icon_grp = VGroup(face_box, face_sample).move_to(np.array([-4.6, 0.3, 0]))

        # ID card box
        id_box = Rectangle(width=1.6, height=1.1, color=ACCENT_TEAL, stroke_width=1.5,
                           fill_opacity=0.05, fill_color=ACCENT_TEAL)
        id_label = vn_tex_mono("ID CARD", color=ACCENT_TEAL, scale=0.45)
        id_icon_grp = VGroup(id_box, id_label).move_to(np.array([-2.4, 0.3, 0]))

        # Comparison indicator
        eq_sign = vn_tex_bold("?=", color=TEXT_PRIMARY, scale=0.9)
        eq_sign.move_to(np.array([-3.5, 0.3, 0]))

        left_ex_1 = vn_tex(r"$\bullet$ Ví dụ: Mở khóa FaceID iPhone", color=TEXT_MUTED, scale=0.45)
        left_ex_2 = vn_tex(r"$\bullet$ Ví dụ: Kiểm tra hộ chiếu điện tử", color=TEXT_MUTED, scale=0.45)
        left_examples = VGroup(left_ex_1, left_ex_2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        left_examples.move_to(np.array([-3.5, -1.2, 0]))

        # Subtitle 8s - 14s
        update_sub("Verification --- Xác thực 1:1 --- Người này có đúng là họ không?", 6.0)

        self.play(
            FadeIn(left_title, shift=UP * 0.2),
            FadeIn(left_q, shift=UP * 0.2),
            FadeIn(face_icon_grp, shift=RIGHT * 0.2),
            FadeIn(id_icon_grp, shift=LEFT * 0.2),
            Write(eq_sign),
            run_time=1.5
        )
        self.wait(0.5)

        # Subtitle 14s - 20s
        update_sub(r"So sánh một ảnh với một mẫu duy nhất $\rightarrow$ Đúng / Sai", 6.0)

        # Morph ?= to checkmark (Mint)
        checkmark = vn_tex(r"$\checkmark$", color=ACCENT_MINT, scale=1.2)
        checkmark.move_to(eq_sign)
        self.play(ReplacementTransform(eq_sign, checkmark), run_time=0.8)
        self.play(Indicate(checkmark, color=ACCENT_MINT), run_time=0.8)
        self.wait(0.4)

        # Subtitle 20s - 24s
        update_sub("Ví dụ: mở khóa FaceID, quẹt hộ chiếu điện tử", 4.0)

        self.play(FadeIn(left_examples, shift=UP * 0.2), run_time=1.0)
        self.wait(1.0)

        # --- Right Side: Identification ---
        right_header = vn_tex_bold("IDENTIFICATION 1:N", color=ACCENT_LAVENDER, scale=0.7)
        right_sub_label = vn_tex("(Nhận dạng)", color=TEXT_MUTED, scale=0.5)
        right_title = VGroup(right_header, right_sub_label).arrange(DOWN, buff=0.1)
        right_title.move_to(np.array([3.5, 2.0, 0]))

        right_q = vn_tex_italic("Là ai trong N người?", color=TEXT_PRIMARY, scale=0.6)
        right_q.move_to(np.array([3.5, 1.4, 0]))

        # Probe face box
        probe_sample = make_tiny_face(color=ACCENT_BLUE, scale=0.35, opacity=0.7)
        probe_box = Rectangle(width=0.9, height=1.1, color=ACCENT_BLUE, stroke_width=1.5,
                              fill_opacity=0.05, fill_color=ACCENT_BLUE)
        probe_grp = VGroup(probe_box, probe_sample).move_to(np.array([1.8, 0.3, 0]))

        # Scan Arrow
        scan_arrow = Arrow(LEFT, RIGHT, color=ACCENT_CYAN, buff=0.05, stroke_width=3
                           ).scale(0.4).move_to(np.array([2.7, 0.3, 0]))

        # Grid of N faces in Database
        grid = VGroup()
        for r in range(3):
            row = VGroup()
            for c in range(5):
                db_item = Rectangle(width=0.3, height=0.38, color=TEXT_MUTED,
                                    stroke_width=0.8, fill_opacity=0.05)
                row.add(db_item)
            row.arrange(RIGHT, buff=0.08)
            grid.add(row)
        grid.arrange(DOWN, buff=0.08)
        grid.move_to(np.array([4.4, 0.3, 0]))

        match_item = grid[1][2]

        right_ex_1 = vn_tex(r"$\bullet$ Ví dụ: Tìm đối tượng qua camera", color=TEXT_MUTED, scale=0.45)
        right_ex_2 = vn_tex(r"$\bullet$ Ví dụ: Tự động tag ảnh Facebook", color=TEXT_MUTED, scale=0.45)
        right_examples = VGroup(right_ex_1, right_ex_2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        right_examples.move_to(np.array([3.5, -1.2, 0]))

        # Subtitle 24s - 30s
        update_sub("Identification --- Nhận dạng 1:N --- Người này là ai trong N người?", 6.0)

        self.play(
            FadeIn(right_title, shift=UP * 0.2),
            FadeIn(right_q, shift=UP * 0.2),
            FadeIn(probe_grp, shift=RIGHT * 0.2),
            FadeIn(scan_arrow),
            FadeIn(grid),
            run_time=1.5
        )
        self.wait(0.5)

        # Subtitle 30s - 36s
        update_sub(r"So sánh một ảnh với toàn bộ N mẫu $\rightarrow$ trả về top giống nhất", 6.0)

        # Scanning animation sweep
        scan_line = Line(
            grid.get_left() + UP * 0.1,
            grid.get_right() + UP * 0.1,
            color=ACCENT_CYAN,
            stroke_width=2.0
        ).set_opacity(0.8)
        self.add(scan_line)

        self.play(
            scan_line.animate.move_to(grid.get_bottom() + DOWN * 0.1),
            run_time=1.8,
            rate_func=exponential_decay
        )
        self.play(FadeOut(scan_line), run_time=0.3)

        # Highlight match item
        self.play(
            match_item.animate.set_color(ACCENT_LAVENDER).set_fill(ACCENT_LAVENDER, opacity=0.35).scale(1.2),
            run_time=0.8
        )
        self.play(Indicate(match_item, color=ACCENT_MINT), run_time=1.0)
        self.wait(0.4)

        # Subtitle 36s - 42s
        update_sub("Ví dụ: tìm tội phạm qua camera, auto-tag Facebook", 6.0)
        self.play(FadeIn(right_examples, shift=UP * 0.2), run_time=1.0)
        self.wait(1.0)

        # === Phase C: Kết luận (42s - 50s) ===
        update_sub("EBGM tập trung giải quyết bài toán 1:N", 8.0)

        right_panel_box = SurroundingRectangle(
            VGroup(right_title, right_q, probe_grp, grid, right_examples),
            color=ACCENT_LAVENDER,
            buff=0.25,
            stroke_width=1.5
        )

        self.play(
            Create(right_panel_box),
            VGroup(left_title, left_q, face_icon_grp, id_icon_grp, checkmark, left_examples
                   ).animate.set_opacity(0.25),
            divider.animate.set_opacity(0.1),
            run_time=1.5
        )
        self.wait(3.5)

        # Clean up
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)
