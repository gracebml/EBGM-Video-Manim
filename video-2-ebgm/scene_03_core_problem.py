"""
EBGM Video — Overview Section
Scene 3: Vấn đề cốt lõi
Thời lượng dự kiến: 55s

 YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts
  - XeLaTeX (thường có sẵn trong TeX Live)

Render command:
  manim -pql scene_03_core_problem.py Scene3_CoreProblem
  manim -pqh scene_03_core_problem.py Scene3_CoreProblem  # high quality
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# PROCEDURAL FACE BUILDERS FOR COMPACT VISUALIZATION
# ============================================================
def make_frontal_neutral(color=ACCENT_BLUE, fill_opacity=0.06):
    """1. Frontal / Neutral Face"""
    head = Ellipse(width=1.3, height=1.7, color=color, stroke_width=2, fill_opacity=fill_opacity)
    left_eye = Dot(point=[-0.22, 0.2, 0], radius=0.045, color=color)
    right_eye = Dot(point=[0.22, 0.2, 0], radius=0.045, color=color)
    nose = Line([0, 0.2, 0], [0, -0.1, 0], color=color, stroke_width=2)
    mouth = Arc(radius=0.18, start_angle=-PI/6, angle=-2*PI/3, color=color, stroke_width=2).shift(DOWN * 0.35)
    return VGroup(head, left_eye, right_eye, nose, mouth)

def make_profile_face(color=ACCENT_BLUE, fill_opacity=0.06):
    """2. Rotated Pose Face"""
    head = Ellipse(width=1.0, height=1.7, color=color, stroke_width=2, fill_opacity=fill_opacity)
    left_eye = Dot(point=[-0.08, 0.2, 0], radius=0.04, color=color)
    right_eye = Dot(point=[0.32, 0.2, 0], radius=0.04, color=color)
    nose = Line([0.12, 0.2, 0], [0.32, -0.1, 0], color=color, stroke_width=2)
    mouth = Arc(radius=0.12, start_angle=-PI/8, angle=-PI/2, color=color, stroke_width=2).shift(RIGHT * 0.08 + DOWN * 0.35)
    return VGroup(head, left_eye, right_eye, nose, mouth)

def make_smiling_face(color=ACCENT_BLUE, fill_opacity=0.06):
    """3. Smiling Expression"""
    head = Ellipse(width=1.3, height=1.7, color=color, stroke_width=2, fill_opacity=fill_opacity)
    left_eye = Dot(point=[-0.22, 0.2, 0], radius=0.045, color=color)
    right_eye = Dot(point=[0.22, 0.2, 0], radius=0.045, color=color)
    nose = Line([0, 0.2, 0], [0, -0.1, 0], color=color, stroke_width=2)
    # Smile: Wide open mouth arc
    mouth = Arc(radius=0.22, start_angle=0, angle=-PI, color=color, stroke_width=2).shift(DOWN * 0.3)
    mouth_line = Line(mouth.get_left(), mouth.get_right(), color=color, stroke_width=1.5)
    return VGroup(head, left_eye, right_eye, nose, mouth, mouth_line)

def make_dark_face(color=ACCENT_BLUE):
    """4. Shadow / Low-light Face"""
    face = make_frontal_neutral(color=color, fill_opacity=0.01)
    # Dark shadow overlay
    shadow = Polygon(
        [-0.8, 1.0, 0], [0.8, -1.0, 0], [0.8, 1.0, 0],
        color=BG_NAVY, stroke_width=0, fill_opacity=0.72
    )
    return VGroup(face, shadow)

def make_glasses_face(color=ACCENT_BLUE, fill_opacity=0.06):
    """5. Wearing Glasses (Occlusion)"""
    face = make_frontal_neutral(color=color, fill_opacity=fill_opacity)
    left_glass = Circle(radius=0.16, color=ACCENT_CYAN, stroke_width=1.5).move_to([-0.22, 0.2, 0])
    right_glass = Circle(radius=0.16, color=ACCENT_CYAN, stroke_width=1.5).move_to([0.22, 0.2, 0])
    bridge = Line([-0.06, 0.2, 0], [0.06, 0.2, 0], color=ACCENT_CYAN, stroke_width=1.5)
    return VGroup(face, left_glass, right_glass, bridge)

# ============================================================
# COMPANION FACES FOR IN-CLASS DISCRIMINATION (DIFFERENT PEOPLE)
# ============================================================
def make_person_A(color=ACCENT_TEAL):
    """Wide face, larger nose"""
    head = Ellipse(width=1.5, height=1.6, color=color, stroke_width=2, fill_opacity=0.08)
    left_eye = Dot(point=[-0.28, 0.15, 0], radius=0.05, color=color)
    right_eye = Dot(point=[0.28, 0.15, 0], radius=0.05, color=color)
    nose = Triangle(color=color, stroke_width=2).scale(0.12).move_to([0, -0.05, 0])
    mouth = Line([-0.2, -0.4, 0], [0.2, -0.4, 0], color=color, stroke_width=2)
    return VGroup(head, left_eye, right_eye, nose, mouth)

def make_person_B(color=ACCENT_LAVENDER):
    """Long face, narrow eyes, small mouth"""
    head = Ellipse(width=1.1, height=1.9, color=color, stroke_width=2, fill_opacity=0.08)
    left_eye = Line([-0.25, 0.25, 0], [-0.15, 0.25, 0], color=color, stroke_width=3)
    right_eye = Line([0.15, 0.25, 0], [0.25, 0.25, 0], color=color, stroke_width=3)
    nose = Line([0, 0.25, 0], [0, -0.15, 0], color=color, stroke_width=2)
    mouth = Arc(radius=0.1, start_angle=-PI/4, angle=-PI/2, color=color, stroke_width=2).shift(DOWN * 0.45)
    return VGroup(head, left_eye, right_eye, nose, mouth)

# ============================================================
# MAIN SCENE CLASS
# ============================================================
class Scene3_CoreProblem(Scene):
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

        # === Phase A: Tiêu đề & dẫn dắt (0s - 8s) ===
        sec_title = section_title("Vấn đề cốt lõi của Face Recognition")
        sec_title.to_edge(UP, buff=0.5)

        self.play(FadeIn(sec_title, shift=DOWN * 0.2), run_time=1.0)

        # "Tại sao nhận diện khuôn mặt lại khó?"
        question = vn_tex_bold("Tại sao nhận diện khuôn mặt lại khó?", color=TEXT_PRIMARY, scale=0.75)
        question.move_to(ORIGIN)

        new_sub = make_subtitle("Tại sao nhận diện khuôn mặt lại khó?")
        self.play(FadeIn(new_sub, shift=UP * 0.15), run_time=0.4)
        self.current_sub = new_sub

        self.play(Write(question), run_time=2.6)
        self.wait(1.0)

        update_sub("Một người có thể trông rất khác nhau giữa các bức ảnh", 3.0)
        self.play(FadeOut(question), run_time=0.8)

        # === Phase B: Variance — cùng một người, rất nhiều biến đổi (8s - 28s) ===
        # Create 5 stylized faces representing the same person under different conditions
        face_neutral = make_frontal_neutral().scale(0.85)
        face_pose = make_profile_face().scale(0.85)
        face_expression = make_smiling_face().scale(0.85)
        face_lighting = make_dark_face().scale(0.85)
        face_accessory = make_glasses_face().scale(0.85)

        faces_group = VGroup(
            face_neutral,
            face_pose,
            face_expression,
            face_lighting,
            face_accessory
        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.3)

        # Labels for each variation
        labels = VGroup(
            vn_tex("Chính diện", color=TEXT_MUTED, scale=0.45),
            vn_tex("Tư thế", color=TEXT_MUTED, scale=0.45),
            vn_tex("Biểu cảm", color=TEXT_MUTED, scale=0.45),
            vn_tex("Ánh sáng", color=TEXT_MUTED, scale=0.45),
            vn_tex("Vật cản", color=TEXT_MUTED, scale=0.45)
        )

        for i, face in enumerate(faces_group):
            labels[i].next_to(face, DOWN, buff=0.25)

        # Subtitle 12s - 20s
        update_sub("Biểu cảm, tư thế, ánh sáng, vị trí, kích thước --- tất cả đều thay đổi", 8.0)

        # Lagged show faces and labels
        self.play(
            LaggedStart(
                *[
                    VGroup(faces_group[i], labels[i]).animate.shift(UP * 0.15).set_opacity(1.0)
                    for i in range(5)
                ],
                lag_ratio=0.2,
                run_time=2.5
            )
        )
        self.wait(1.5)

        # Surrounding container showing "SAME PERSON"
        big_box = SurroundingRectangle(faces_group, color=ACCENT_MINT, buff=0.4, stroke_width=1.5)
        same_person_lbl = vn_tex_bold("CÙNG MỘT NGƯỜI", color=ACCENT_MINT, scale=0.6)
        same_person_lbl.next_to(big_box, UP, buff=0.15)

        # Subtitle 20s - 28s
        update_sub("Đây là bài toán: phân biệt trong môi trường có nhiều biến đổi", 8.0)

        # Add double-ended curved arrows to indicate mapping
        arrows = VGroup()
        for i in range(4):
            arrow = CurvedArrow(
                faces_group[i].get_top() + UP * 0.15 + RIGHT * 0.1,
                faces_group[i+1].get_top() + UP * 0.15 + LEFT * 0.1,
                angle=-PI/4,
                color=ACCENT_MINT,
                stroke_width=1.2
            )
            arrows.add(arrow)

        # Scientific Terminology
        term_1 = vn_tex_mono("discrimination in the presence of variance", color=ACCENT_CYAN, scale=0.48)
        term_1.to_edge(DOWN, buff=1.2)

        self.play(
            Create(big_box),
            FadeIn(same_person_lbl, shift=DOWN*0.1),
            Create(arrows),
            FadeIn(term_1, shift=UP*0.1),
            run_time=2.0
        )
        self.wait(3.0)

        # Clear Phase B elements
        self.play(
            FadeOut(faces_group),
            FadeOut(labels),
            FadeOut(big_box),
            FadeOut(same_person_lbl),
            FadeOut(arrows),
            FadeOut(term_1),
            run_time=0.8
        )

        # === Phase C: In-class discrimination — cấu trúc chung (28s - 44s) ===
        # Subtitle 28s - 36s
        update_sub("Nhưng mọi khuôn mặt đều có cấu trúc chung --- hai mắt, một mũi, một miệng", 8.0)

        # Master face template (cyan line art)
        template_label = vn_tex_bold("MẪU CẤU TRÚC CHUNG (FACE TEMPLATE)", color=ACCENT_CYAN, scale=0.55)
        template_label.to_edge(UP, buff=1.3)

        face_template = make_frontal_neutral(color=ACCENT_CYAN, fill_opacity=0.0).scale(1.2).move_to(LEFT * 2.5 + DOWN * 0.2)
        
        self.play(
            FadeIn(template_label),
            Create(face_template),
            run_time=1.5
        )
        self.wait(1.0)

        # Overlay 3 different people showing they fit the same base structure
        person_neutral = make_frontal_neutral(color=ACCENT_BLUE).scale(1.2).move_to(RIGHT * 2.5 + DOWN * 0.2)
        person_A = make_person_A(color=ACCENT_TEAL).scale(1.2).move_to(RIGHT * 2.5 + DOWN * 0.2)
        person_B = make_person_B(color=ACCENT_LAVENDER).scale(1.2).move_to(RIGHT * 2.5 + DOWN * 0.2)

        person_label = vn_tex_bold("CÁC CÁ NHÂN KHÁC NHAU", color=ACCENT_BLUE, scale=0.55)
        person_label.next_to(person_neutral, UP, buff=0.45)

        # Subtitle 36s - 44s
        update_sub("Máy phải biết cấu trúc chung trước, rồi mới tìm chi tiết phân biệt từng người", 8.0)

        self.play(
            FadeIn(person_neutral),
            FadeIn(person_label),
            run_time=1.0
        )
        self.wait(0.5)

        # Transform neutral face to person A then B
        self.play(
            ReplacementTransform(person_neutral, person_A),
            person_label.animate.set_color(ACCENT_TEAL),
            run_time=1.2
        )
        self.wait(0.8)

        self.play(
            ReplacementTransform(person_A, person_B),
            person_label.animate.set_color(ACCENT_LAVENDER),
            run_time=1.2
        )
        self.wait(0.8)

        # Zoom-in overlay simulation to highlight details: scale up and shift
        zoom_lbl = vn_tex_bold("Tập trung vào chi tiết tinh tế để phân biệt", color=ACCENT_MINT, scale=0.55)
        zoom_lbl.to_edge(UP, buff=1.3)

        # Shift templates to center and scale up
        highlight_group = VGroup(face_template, person_B)
        
        # Highlight circles on eyes and mouth
        eye_highlight = Circle(radius=0.4, color=ACCENT_MINT, stroke_width=2).move_to(face_template[1].get_center() + RIGHT * 0.2)
        mouth_highlight = Circle(radius=0.4, color=ACCENT_MINT, stroke_width=2).move_to(face_template[4].get_center())

        term_2 = vn_tex_mono("in-class discrimination", color=ACCENT_CYAN, scale=0.48)
        term_2.to_edge(DOWN, buff=1.2)

        self.play(
            ReplacementTransform(template_label, zoom_lbl),
            FadeOut(person_label),
            highlight_group.animate.scale(1.8).move_to(ORIGIN + DOWN * 0.2),
            run_time=1.5
        )
        
        # Reposition and show highlights
        eye_highlight.move_to(person_B[1].get_center() + RIGHT * 0.2)
        mouth_highlight.move_to(person_B[4].get_center())

        self.play(
            Create(eye_highlight),
            Create(mouth_highlight),
            FadeIn(term_2, shift=UP*0.1),
            run_time=1.2
        )
        self.wait(2.5)

        # Clean up Phase C
        self.play(
            FadeOut(highlight_group),
            FadeOut(zoom_lbl),
            FadeOut(eye_highlight),
            FadeOut(mouth_highlight),
            FadeOut(term_2),
            run_time=0.8
        )

        # === Phase D: Kết luận (44s - 55s) ===
        # Subtitle 44s - 55s
        update_sub("Mục tiêu: triệt tiêu biến đổi và làm nổi bật đặc trưng nhận dạng", 11.0)

        promise_lbl = vn_tex_bold("HỨA HẸN CỦA PHƯƠNG PHÁP EBGM", color=ACCENT_CYAN, scale=0.65)
        promise_lbl.to_edge(UP, buff=1.5)

        conc_1 = vn_tex_bold("1. Triệt tiêu các biến dạng (Collapse the variance)", color=ACCENT_MINT, scale=0.65)
        conc_2 = vn_tex_bold("2. Làm nổi bật đặc trưng (Emphasize discriminating features)", color=ACCENT_LAVENDER, scale=0.65)

        conclusions = VGroup(conc_1, conc_2).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(ORIGIN)

        self.play(
            FadeIn(promise_lbl, shift=DOWN*0.2),
            Write(conc_1),
            run_time=2.0
        )
        self.wait(1.5)
        self.play(
            Write(conc_2),
            run_time=2.0
        )
        self.wait(4.5)

        # Final cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)
