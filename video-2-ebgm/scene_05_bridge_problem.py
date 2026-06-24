"""
EBGM Video — Overview Section
Scene 5: Chuyển tiếp: Vấn đề còn bỏ ngỏ
Thời lượng dự kiến: 15s

 YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts
  - XeLaTeX (thường có sẵn trong TeX Live)

Render command:
  manim -pql scene_05_bridge_problem.py Scene5_BridgeProblem
  manim -pqh scene_05_bridge_problem.py Scene5_BridgeProblem  # high quality
"""

from manim import *
from _common import *

def make_coral_cross(size=0.3):
    """Procedural vector cross."""
    l1 = Line([-size, size, 0], [size, -size, 0], color=ACCENT_CORAL, stroke_width=3.0)
    l2 = Line([-size, -size, 0], [size, size, 0], color=ACCENT_CORAL, stroke_width=3.0)
    return VGroup(l1, l2)

class Scene5_BridgeProblem(Scene):
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

        # === General Header ===
        sec_title = section_title("Hạn chế của các phương pháp cũ")
        sec_title.to_edge(UP, buff=0.5)
        self.play(FadeIn(sec_title, shift=DOWN * 0.2), run_time=0.8)

        # 3 boxes representing prior approaches
        box1 = RoundedRectangle(corner_radius=0.08, width=3.3, height=1.5, color=ACCENT_BLUE, fill_color=BG_NAVY_SOFT, fill_opacity=0.3)
        box2 = RoundedRectangle(corner_radius=0.08, width=3.3, height=1.5, color=ACCENT_LAVENDER, fill_color=BG_NAVY_SOFT, fill_opacity=0.3)
        box3 = RoundedRectangle(corner_radius=0.08, width=3.3, height=1.5, color=ACCENT_CYAN, fill_color=BG_NAVY_SOFT, fill_opacity=0.3)
        boxes = VGroup(box1, box2, box3).arrange(RIGHT, buff=0.4).move_to(UP * 0.8)

        t1 = vn_tex_bold("Hình học thủ công", color=TEXT_MUTED, scale=0.45).move_to(box1)
        t2 = vn_tex_bold("Mạng Nơ-ron", color=TEXT_MUTED, scale=0.45).move_to(box2)
        t3 = vn_tex_bold("PCA / Eigenfaces", color=TEXT_MUTED, scale=0.45).move_to(box3)
        titles = VGroup(t1, t2, t3)

        self.play(
            Create(boxes),
            FadeIn(titles),
            run_time=1.5
        )
        self.wait(0.5)

        # 0s - 8s: Bridge subtitle
        update_sub("Cả ba cách tiếp cận đều có điểm nghẽn riêng", 8.0)

        # Show red crosses over the boxes
        cross1 = make_coral_cross(size=0.35).move_to(box1)
        cross2 = make_coral_cross(size=0.35).move_to(box2)
        cross3 = make_coral_cross(size=0.35).move_to(box3)

        self.play(
            Create(cross1),
            Create(cross2),
            Create(cross3),
            run_time=1.2
        )
        self.wait(1.5)

        # Dim out the boxes and crosses
        self.play(
            boxes.animate.set_opacity(0.18),
            titles.animate.set_opacity(0.18),
            cross1.animate.set_opacity(0.25),
            cross2.animate.set_opacity(0.25),
            cross3.animate.set_opacity(0.25),
            run_time=1.0
        )

        # 8s - 15s: Next phase sub
        update_sub("Liệu có giải pháp nào trung gian, gần với cách con người nhận thức?", 7.0)

        # Big core question
        q1 = vn_tex("Liệu có cách nào tích hợp được thông tin cấu trúc khuôn mặt,", color=TEXT_PRIMARY, scale=0.48)
        q2 = vn_tex("mà không cần huấn luyện khổng lồ, không cần lập trình thủ công,", color=TEXT_PRIMARY, scale=0.48)
        q3 = vn_tex("và vượt qua được giới hạn tuyến tính?", color=TEXT_PRIMARY, scale=0.48)
        question = VGroup(q1, q2, q3).arrange(DOWN, buff=0.12).move_to(DOWN * 1.3)

        self.play(
            Write(question),
            run_time=2.5
        )
        self.wait(2.0)

        # Final transition: fade out elements and transform question to small heading sliding UP
        question_small = vn_tex_bold("Giải pháp trung gian tối ưu?", color=ACCENT_CYAN, scale=0.6).to_edge(UP, buff=0.5)
        
        self.play(
            FadeOut(boxes),
            FadeOut(titles),
            FadeOut(cross1),
            FadeOut(cross2),
            FadeOut(cross3),
            FadeOut(sec_title),
            ReplacementTransform(question, question_small),
            run_time=1.2
        )
        self.wait(0.8)

        # Fade out general small question to prepare for Scene 6
        self.play(FadeOut(question_small), run_time=0.5)
        self.wait(0.2)
