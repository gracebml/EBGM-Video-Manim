"""
EBGM Video — Overview Section
Scene 4: Các cách tiếp cận trước đây
Thời lượng dự kiến: 90s

 YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts
  - XeLaTeX (thường có sẵn trong TeX Live)

Render command:
  manim -pql scene_04_prior_approaches.py Scene4_PriorApproaches
  manim -pqh scene_04_prior_approaches.py Scene4_PriorApproaches  # high quality
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# LOCAL STYLIZED PROCEDURAL BUILDERS
# ============================================================
def make_eye_model(color=ACCENT_CYAN, scale=1.0):
    """Procedural almond-shaped eye with iris and radius markup."""
    # Outer almond shape
    left_arc = Arc(radius=1.0, start_angle=5*PI/6, angle=-2*PI/3, color=color, stroke_width=2.5)
    right_arc = Arc(radius=1.0, start_angle=-PI/6, angle=-2*PI/3, color=color, stroke_width=2.5)
    # Combine and close into eye shape
    eye_outline = VGroup(left_arc, right_arc).arrange(RIGHT, buff=-0.3).scale(0.85)
    
    # Iris
    iris = Circle(radius=0.28, color=color, stroke_width=2.0)
    pupil = Dot(color=color, radius=0.09)
    
    # Annotation lines
    radius_line = Line([0, 0, 0], [0.28 * np.cos(30*DEGREES), 0.28 * np.sin(30*DEGREES), 0],
                       color=ACCENT_LAVENDER, stroke_width=1.5)
    
    eye = VGroup(eye_outline, iris, pupil, radius_line).scale(scale)
    return eye

def make_simple_nose(color=ACCENT_BLUE, scale=0.5):
    """Simple line nose."""
    return Line([0, 0.4, 0], [0, -0.2, 0], color=color, stroke_width=2).add(
           Line([0, -0.2, 0], [0.2, -0.2, 0], color=color, stroke_width=2)
    ).scale(scale)

def make_simple_mouth(color=ACCENT_BLUE, scale=0.5):
    """Simple mouth arc."""
    return Arc(radius=0.4, start_angle=-PI/6, angle=-2*PI/3, color=color, stroke_width=2).scale(scale)

def make_simple_eyebrow(color=ACCENT_BLUE, scale=0.5):
    """Curved eyebrow line."""
    return Arc(radius=0.5, start_angle=PI/6, angle=2*PI/3, color=color, stroke_width=2).scale(scale)

def make_neural_net(scale=1.0):
    """Creates a 4-layer fully connected network illustration."""
    layer_sizes = [4, 5, 5, 2]
    nodes = VGroup()
    connections = VGroup()
    
    layer_x = [-1.6, -0.5, 0.5, 1.6]
    layer_nodes = []
    
    for l_idx, size in enumerate(layer_sizes):
        layer = VGroup()
        y_positions = np.linspace(-1.0, 1.0, size)
        for y in y_positions:
            node = Circle(
                radius=0.1, 
                color=ACCENT_CYAN if l_idx < 3 else ACCENT_LAVENDER, 
                fill_color=BG_NAVY, 
                fill_opacity=1.0, 
                stroke_width=1.5
            )
            node.move_to([layer_x[l_idx], y, 0])
            layer.add(node)
        nodes.add(layer)
        layer_nodes.append(layer)
        
    for l_idx in range(len(layer_sizes) - 1):
        for node_a in layer_nodes[l_idx]:
            for node_b in layer_nodes[l_idx+1]:
                conn = Line(
                    node_a.get_center(), 
                    node_b.get_center(), 
                    color=ACCENT_BLUE, 
                    stroke_width=0.8
                ).set_opacity(0.25)
                connections.add(conn)
                
    return VGroup(connections, nodes).scale(scale)

def make_eigenface(color=ACCENT_BLUE, width=0.6, height=0.8, opacity=0.3):
    """Ghostly abstract outline mask representing an eigenface."""
    head = Ellipse(width=width, height=height, color=color, stroke_width=1.5, fill_opacity=opacity)
    eye_l = Ellipse(width=0.15, height=0.06, color=color, stroke_width=0.8).move_to([-0.12, 0.1, 0])
    eye_r = Ellipse(width=0.15, height=0.06, color=color, stroke_width=0.8).move_to([0.12, 0.1, 0])
    mouth = Ellipse(width=0.22, height=0.08, color=color, stroke_width=0.8).move_to([0, -0.18, 0])
    return VGroup(head, eye_l, eye_r, mouth)

def make_frontal_neutral(color=ACCENT_BLUE, fill_opacity=0.06):
    """Frontal / Neutral Face for PCA demo."""
    head = Ellipse(width=1.3, height=1.7, color=color, stroke_width=2, fill_opacity=fill_opacity)
    left_eye = Dot(point=[-0.22, 0.2, 0], radius=0.045, color=color)
    right_eye = Dot(point=[0.22, 0.2, 0], radius=0.045, color=color)
    nose = Line([0, 0.2, 0], [0, -0.1, 0], color=color, stroke_width=2)
    mouth = Arc(radius=0.18, start_angle=-PI/6, angle=-2*PI/3, color=color, stroke_width=2).shift(DOWN * 0.35)
    return VGroup(head, left_eye, right_eye, nose, mouth)

# ============================================================
# MAIN SCENE
# ============================================================
class Scene4_PriorApproaches(Scene):
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
        sec_title = section_title("Các hướng tiếp cận nhận diện trước đây")
        sec_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(sec_title, shift=DOWN * 0.2), run_time=1.0)

        # Base Panel Frame in which all 3 approaches will sit
        panel_frame = RoundedRectangle(
            corner_radius=0.15,
            width=11.5,
            height=4.8,
            color=ACCENT_BLUE,
            stroke_width=1.2,
            fill_color=BG_NAVY_SOFT,
            fill_opacity=0.35
        ).move_to(DOWN * 0.2)
        
        self.play(Create(panel_frame), run_time=1.0)
        self.wait(0.5)

        # 0s - 6s: Intro Subtitle
        update_sub("Trước EBGM, có ba hướng tiếp cận phổ biến", 6.0)

        # ============================================================
        # PANEL 1: DESIGNER-PROVIDED STRUCTURES (0s - 28s)
        # ============================================================
        p1_grp = VGroup()
        
        # Header number and title
        p1_num = vn_tex_bold("01", color=ACCENT_CYAN, scale=1.3)
        p1_num.move_to(panel_frame.get_corner(UL) + RIGHT * 0.6 + DOWN * 0.5)
        p1_title = vn_tex_bold("DESIGNER-PROVIDED STRUCTURES", color=TEXT_PRIMARY, scale=0.6)
        p1_title.next_to(p1_num, RIGHT, buff=0.25).align_to(p1_num, DOWN).shift(UP * 0.15)
        
        p1_grp.add(p1_num, p1_title)

        # Eye model visual (left part of inside)
        eye_model = make_eye_model(color=ACCENT_CYAN, scale=1.3).move_to(LEFT * 2.8 + DOWN * 0.1)
        r_lbl = vn_math("r = 15\\text{ px}", color=ACCENT_LAVENDER, scale=0.45).next_to(eye_model, UR, buff=-0.2)
        alpha_lbl = vn_math("\\alpha = 40^\\circ", color=ACCENT_LAVENDER, scale=0.45).next_to(eye_model, DR, buff=-0.35)
        eye_model_grp = VGroup(eye_model, r_lbl, alpha_lbl)

        # Companion shapes
        nose_shape = make_simple_nose(color=ACCENT_BLUE, scale=0.65).next_to(eye_model, RIGHT, buff=0.8).shift(UP * 0.3)
        mouth_shape = make_simple_mouth(color=ACCENT_BLUE, scale=0.65).next_to(nose_shape, DOWN, buff=0.3)
        eyebrow_shape = make_simple_eyebrow(color=ACCENT_BLUE, scale=0.65).next_to(eye_model, LEFT, buff=0.6)
        shapes_grp = VGroup(eye_model_grp, nose_shape, mouth_shape, eyebrow_shape)
        
        p1_grp.add(shapes_grp)

        # Monospace code block mock on the right (Escaped underscores for LaTeX)
        code_bg = RoundedRectangle(
            corner_radius=0.08, width=4.5, height=2.2,
            color=ACCENT_BLUE, stroke_width=0.8, fill_color=BG_NAVY, fill_opacity=0.6
        ).move_to(RIGHT * 2.8 + DOWN * 0.1)
        
        c_1 = vn_tex_mono(r"if eye\_open():", color=TEXT_PRIMARY, scale=0.42)
        c_2 = vn_tex_mono(r"    detect\_iris()", color=TEXT_PRIMARY, scale=0.42)
        c_3 = vn_tex_mono(r"elif sunglasses\_detected():", color=TEXT_PRIMARY, scale=0.42)
        c_4 = vn_tex_mono("    ???", color=ACCENT_CORAL, scale=0.42)
        code_lines = VGroup(c_1, c_2, c_3, c_4).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(code_bg.get_center() + LEFT * 0.1)
        code_block = VGroup(code_bg, code_lines)
        
        p1_grp.add(code_block)

        # Pros and cons (Replaced \bm{\times} with standard \times)
        p1_pro = vn_tex(r"$\checkmark$ Ưu điểm: Mô hình hình học rõ ràng, trực quan, dễ hiểu", color=ACCENT_MINT, scale=0.45)
        p1_con = vn_tex(r"$\times$ Hạn chế: Rất đắt đỏ và thiếu linh hoạt --- ngoại lệ yêu cầu code lại", color=ACCENT_CORAL, scale=0.45)
        p1_bullets = VGroup(p1_pro, p1_con).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        p1_bullets.move_to(panel_frame.get_bottom() + UP * 0.6)
        
        p1_grp.add(p1_bullets)

        # 6s - 14s: First sub phase
        update_sub("Một: thiết kế thủ công các đặc trưng khuôn mặt", 8.0)

        # Reveal panel 1 elements
        self.play(
            FadeIn(p1_num, shift=UP * 0.15),
            FadeIn(p1_title, shift=UP * 0.15),
            Create(eye_model),
            FadeIn(r_lbl),
            FadeIn(alpha_lbl),
            run_time=2.0
        )
        self.wait(1.0)

        # 14s - 22s: Explain eye & eyebrows
        update_sub("Ví dụ: định nghĩa mắt là hình quả hạnh, kèm các thông số góc, bán kính", 8.0)
        
        self.play(
            Create(nose_shape),
            Create(mouth_shape),
            Create(eyebrow_shape),
            FadeIn(code_bg),
            Write(code_lines),
            run_time=2.5
        )
        self.wait(1.5)

        # Glitch / warning failure animation on "???"
        warning_box = SurroundingRectangle(c_4, color=ACCENT_CORAL, buff=0.08, stroke_width=1.5)
        warning_dot = Dot(color=ACCENT_CORAL, radius=0.15).next_to(warning_box, RIGHT, buff=0.15)
        
        # 22s - 28s: Drawbacks
        update_sub("Hạn chế: gặp ngoại lệ như đeo kính râm là hệ thống bị phá vỡ", 6.0)
        
        # Shake effect on eye model to represent match error
        shake_anim = [
            eye_model_grp.animate.shift(LEFT*0.1),
            eye_model_grp.animate.shift(RIGHT*0.2),
            eye_model_grp.animate.shift(LEFT*0.1)
        ]
        
        self.play(
            Create(warning_box),
            FadeIn(warning_dot),
            Flash(warning_dot, color=ACCENT_CORAL),
            *shake_anim,
            run_time=1.5
        )
        self.play(FadeIn(p1_bullets, shift=UP * 0.15), run_time=1.2)
        self.wait(1.8)

        # Clean up Panel 1 elements
        self.play(
            FadeOut(p1_grp),
            FadeOut(warning_box),
            FadeOut(warning_dot),
            run_time=0.8
        )

        # ============================================================
        # PANEL 2: NEURAL NETWORKS (28s - 56s)
        # ============================================================
        p2_grp = VGroup()

        # Header and title
        p2_num = vn_tex_bold("02", color=ACCENT_LAVENDER, scale=1.3)
        p2_num.move_to(panel_frame.get_corner(UL) + RIGHT * 0.6 + DOWN * 0.5)
        p2_title = vn_tex_bold("NEURAL NETWORKS", color=TEXT_PRIMARY, scale=0.6)
        p2_title.next_to(p2_num, RIGHT, buff=0.25).align_to(p2_num, DOWN).shift(UP * 0.15)

        p2_grp.add(p2_num, p2_title)

        # Neural Net visual
        nn_model = make_neural_net(scale=1.15).move_to(LEFT * 2.2 + DOWN * 0.1)
        p2_grp.add(nn_model)

        # Training statistics mock on the right
        stats_bg = RoundedRectangle(
            corner_radius=0.08, width=4.5, height=2.2,
            color=ACCENT_BLUE, stroke_width=0.8, fill_color=BG_NAVY, fill_opacity=0.6
        ).move_to(RIGHT * 2.8 + DOWN * 0.1)
        
        epoch_tracker = ValueTracker(1)
        epoch_text = always_redraw(lambda: vn_tex_mono(
            f"EPOCH: {int(epoch_tracker.get_value())}", 
            color=ACCENT_CYAN, scale=0.55
        ).move_to(stats_bg.get_center() + UP * 0.5))
        
        cost_tracker = ValueTracker(25.0)
        # Escaped dollar sign to avoid LaTeX math mode error
        cost_text = always_redraw(lambda: vn_tex_mono(
            f"COMPUTE COST: \\${cost_tracker.get_value():.2f}", 
            color=ACCENT_LAVENDER, scale=0.45
        ).move_to(stats_bg.get_center() + DOWN * 0.15))
        
        status_text = vn_tex_mono("TRAINING STATUS: RUNNING...", color=ACCENT_MINT, scale=0.35
                                 ).move_to(stats_bg.get_center() + DOWN * 0.65)
        
        stats_grp = VGroup(stats_bg, epoch_text, cost_text, status_text)
        p2_grp.add(stats_grp)

        # Pros and cons
        p2_pro = vn_tex(r"$\checkmark$ Ưu điểm: Tự động học và hấp thụ cấu trúc khuôn mặt từ dữ liệu", color=ACCENT_MINT, scale=0.45)
        p2_con = vn_tex(r"$\times$ Hạn chế: Đòi hỏi tài nguyên tính toán khổng lồ và tập dữ liệu huấn luyện lớn", color=ACCENT_CORAL, scale=0.45)
        p2_bullets = VGroup(p2_pro, p2_con).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        p2_bullets.move_to(panel_frame.get_bottom() + UP * 0.6)

        p2_grp.add(p2_bullets)

        # 28s - 36s: Neural Networks intro
        update_sub("Hai: sử dụng mạng nơ-ron học trực tiếp từ dữ liệu", 8.0)

        self.play(
            FadeIn(p2_num, shift=UP * 0.15),
            FadeIn(p2_title, shift=UP * 0.15),
            Create(nn_model[0]),  # Create connections
            LaggedStart(*[GrowFromCenter(node) for layer in nn_model[1] for node in layer], lag_ratio=0.05),
            run_time=2.2
        )

        # 36s - 44s: Training mock
        update_sub("Mạng tự phát hiện các cấu trúc ẩn qua hàng triệu lượt học thử sai", 8.0)
        
        self.play(
            FadeIn(stats_bg),
            FadeIn(epoch_text),
            FadeIn(cost_text),
            FadeIn(status_text),
            run_time=1.0
        )
        
        # Pulse connection animation & value tracking
        pulse_line = nn_model[0].copy().set_color(ACCENT_CYAN).set_stroke(width=2.5, opacity=0.8)
        self.play(
            epoch_tracker.animate.set_value(1250),
            cost_tracker.animate.set_value(8420.50),
            ShowPassingFlash(pulse_line, time_width=0.5),
            run_time=4.5,
            rate_func=linear
        )
        self.wait(1.0)

        # 44s - 56s: Drawbacks
        update_sub("Hạn chế: chi phí huấn luyện vô cùng đắt đỏ, cần khối lượng dữ liệu khổng lồ", 12.0)
        
        status_done = vn_tex_mono("TRAINING STATUS: HEAVY LOAD", color=ACCENT_CORAL, scale=0.35).move_to(status_text)
        self.play(
            ReplacementTransform(status_text, status_done),
            FadeIn(p2_bullets, shift=UP * 0.15),
            run_time=1.5
        )
        self.wait(6.0)

        # Clean up Panel 2
        self.play(FadeOut(p2_grp), FadeOut(status_done), run_time=0.8)

        # ============================================================
        # PANEL 3: PCA / EIGENFACES (56s - 90s)
        # ============================================================
        p3_grp = VGroup()

        # Header and title
        p3_num = vn_tex_bold("03", color=ACCENT_CYAN, scale=1.3)
        p3_num.move_to(panel_frame.get_corner(UL) + RIGHT * 0.6 + DOWN * 0.5)
        p3_title = vn_tex_bold("PCA / EIGENFACES", color=TEXT_PRIMARY, scale=0.6)
        p3_title.next_to(p3_num, RIGHT, buff=0.25).align_to(p3_num, DOWN).shift(UP * 0.15)

        p3_grp.add(p3_num, p3_title)

        # Math formula in Eigenspace
        formula = vn_math(
            r"\mathbf{f} \approx \bar{\mathbf{f}} + \alpha_1 \mathbf{u}_1 + \alpha_2 \mathbf{u}_2 + \alpha_3 \mathbf{u}_3",
            color=TEXT_PRIMARY, scale=0.75
        ).move_to(UP * 0.7 + RIGHT * 0.3)
        p3_grp.add(formula)

        # Row of Eigenfaces below formula
        eigen_1 = make_eigenface(color=ACCENT_TEAL, opacity=0.15).move_to(LEFT * 4.5 + DOWN * 0.7)
        eigen_2 = make_eigenface(color=ACCENT_BLUE, opacity=0.12).move_to(LEFT * 2.8 + DOWN * 0.7)
        eigen_3 = make_eigenface(color=ACCENT_LAVENDER, opacity=0.18).move_to(LEFT * 1.1 + DOWN * 0.7)
        eigenfaces = VGroup(eigen_1, eigen_2, eigen_3)
        
        lbl_1 = vn_math(r"\mathbf{u}_1", color=ACCENT_TEAL, scale=0.45).next_to(eigen_1, DOWN, buff=0.1)
        lbl_2 = vn_math(r"\mathbf{u}_2", color=ACCENT_BLUE, scale=0.45).next_to(eigen_2, DOWN, buff=0.1)
        lbl_3 = vn_math(r"\mathbf{u}_3", color=ACCENT_LAVENDER, scale=0.45).next_to(eigen_3, DOWN, buff=0.1)
        eigen_labels = VGroup(lbl_1, lbl_2, lbl_3)
        
        p3_grp.add(eigenfaces, eigen_labels)

        # Limitation demo illustration (Right side of panel)
        lim_bg = RoundedRectangle(
            corner_radius=0.08, width=4.5, height=2.2,
            color=ACCENT_BLUE, stroke_width=0.8, fill_color=BG_NAVY, fill_opacity=0.6
        ).move_to(RIGHT * 2.8 + DOWN * 0.1)
        
        # Draw two faces overlaid with opacity to simulate PCA linear mix blur
        face_mouth_high = make_frontal_neutral(color=ACCENT_CYAN).scale(0.85)
        # Shift mouth up
        face_mouth_high[4].shift(UP * 0.12)
        
        face_mouth_low = make_frontal_neutral(color=ACCENT_TEAL).scale(0.85)
        # Shift mouth down
        face_mouth_low[4].shift(DOWN * 0.12)
        
        # Mix them: overlay with half opacity
        face_mouth_high.set_opacity(0.48).move_to(lim_bg)
        face_mouth_low.set_opacity(0.48).move_to(lim_bg)
        
        mixed_face = VGroup(face_mouth_high, face_mouth_low)
        p3_grp.add(lim_bg, mixed_face)

        # Pros and cons
        p3_pro = vn_tex(r"$\checkmark$ Ưu điểm: Biểu diễn nén, gọn gàng, giảm chiều dữ liệu hiệu quả", color=ACCENT_MINT, scale=0.45)
        p3_con = vn_tex(r"$\times$ Hạn chế: Tuyến tính --- không xử lý được các biến dạng phi tuyến và che khuất", color=ACCENT_CORAL, scale=0.45)
        p3_bullets = VGroup(p3_pro, p3_con).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        p3_bullets.move_to(panel_frame.get_bottom() + UP * 0.6)

        p3_grp.add(p3_bullets)

        # 56s - 64s: PCA Eigenfaces intro
        update_sub("Ba: phương pháp PCA phân tách khuôn mặt thành các vector riêng biệt", 8.0)

        self.play(
            FadeIn(p3_num, shift=UP * 0.15),
            FadeIn(p3_title, shift=UP * 0.15),
            Write(formula),
            run_time=2.0
        )
        self.wait(0.5)

        # 64s - 72s: Show eigenfaces
        update_sub("Mỗi bức ảnh mới được nén biểu diễn bằng tổng tuyến tính các hệ số", 8.0)
        self.play(
            LaggedStart(
                *[FadeIn(ef, shift=UP*0.1) for ef in eigenfaces],
                lag_ratio=0.25
            ),
            Write(eigen_labels),
            run_time=2.0
        )
        self.wait(1.5)

        # 72s - 82s: Linear Interpolation Limit
        update_sub("Nhưng PCA là tuyến tính --- trộn hai khuôn mặt sẽ tạo ra ảnh mờ chồng chéo", 10.0)
        self.play(
            FadeIn(lim_bg),
            FadeIn(mixed_face, shift=UP*0.1),
            run_time=1.5
        )
        
        red_arrow = Arrow(
            lim_bg.get_right() + RIGHT * 0.1, 
            lim_bg.get_center() + DOWN * 0.35, 
            color=ACCENT_CORAL, stroke_width=2.5
        ).scale(0.7)
        limit_lbl = vn_tex_bold("Lỗi nội suy mờ!", color=ACCENT_CORAL, scale=0.45).next_to(red_arrow, RIGHT, buff=0.1)
        
        self.play(
            Create(red_arrow),
            FadeIn(limit_lbl, shift=LEFT*0.1),
            run_time=1.2
        )
        self.wait(1.5)

        # 82s - 90s: Eigenspace sensitivity
        update_sub("Rất nhạy cảm với các biến đổi hình học phi tuyến và che khuất cục bộ", 8.0)
        self.play(FadeIn(p3_bullets, shift=UP * 0.15), run_time=1.5)
        self.wait(4.0)

        # Final Cleanup
        self.play(
            FadeOut(p3_grp),
            FadeOut(red_arrow),
            FadeOut(limit_lbl),
            FadeOut(panel_frame),
            FadeOut(sec_title),
            run_time=1.0
        )
        self.wait(0.3)
