"""
EBGM Video — Algorithm Detail Section
Scene 16: Two-Stage Schedule (Chuẩn hóa viền mặt vs Nhận diện chi tiết)
Thời lượng dự kiến: 50s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)
  - Hoạt động trong conda env "vid"

Render command:
  manim -pql scene_16_two_stage_schedule.py Scene16_TwoStageSchedule
  manim -pqh scene_16_two_stage_schedule.py Scene16_TwoStageSchedule  # high quality
"""

from manim import *
import numpy as np
from _common import *

def make_sparse_outline_grid(pos, color, scale=1.0):
    """Outline-heavy sparse grid (Stage 1: Face Finding). Focuses on jawline and hairline."""
    g = VGroup()
    # 5 nodes concentrated around the border outline
    n_pos = {
        0: np.array([-0.9, 0.7, 0]),   # Hairline L
        1: np.array([0.9, 0.7, 0]),    # Hairline R
        2: np.array([-0.7, -0.6, 0]),  # Jaw L
        3: np.array([0.7, -0.6, 0]),   # Jaw R
        4: np.array([0, -1.1, 0]),     # Chin
    }
    
    # Draw simple pentagram-like border edges
    pairs = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]
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
            radius=0.075, color=color
        )
        g.add(dot)
    return g

def make_dense_interior_grid(pos, color, scale=1.0):
    """Interior-heavy dense grid (Stage 2: Recognition). Focuses on interior landmarks."""
    g = VGroup()
    # 8 nodes clustered inside face landmarks
    n_pos = {
        0: np.array([-0.55, 0.4, 0]),   # L Eye
        1: np.array([0.55, 0.4, 0]),    # R Eye
        2: np.array([0, 0.4, 0]),       # Bridge
        3: np.array([0, -0.1, 0]),      # Nose Tip
        4: np.array([-0.38, -0.5, 0]),  # Mouth L
        5: np.array([0.38, -0.5, 0]),   # Mouth R
        6: np.array([0, -0.5, 0]),      # Mouth Center
        7: np.array([0, -0.9, 0]),      # Chin Center
    }
    
    # Connect interior structures (triangles)
    pairs = [
        (0, 1), (0, 2), (1, 2), (2, 3), (0, 3), (1, 3),
        (3, 6), (3, 4), (3, 5), (4, 6), (5, 6), (4, 7), (5, 7), (6, 7)
    ]
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
            radius=0.065, color=color
        )
        g.add(dot)
    return g

class Scene16_TwoStageSchedule(Scene):
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
        # PHASE A: Flowchart pipeline setup (0s - 10s)
        # ============================================================
        title = section_title("Hai giai đoạn: Chuẩn hóa \& Nhận diện")
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=0.8)

        # Subtitle 1 (0s - 6s)
        update_sub("Trong thực tế, quá trình so khớp chạy qua hai giai đoạn riêng biệt", 5.0)

        # Define 5 steps in the vertical flowchart pipeline
        flow_coords = [
            UP * 1.0,
            UP * 0.2,
            DOWN * 0.6,
            DOWN * 1.4
        ]
        
        box_texts = [
            ("Ảnh gốc (256x384)", ACCENT_BLUE),
            ("Giai đoạn 1: CHUẨN HÓA (FBG thưa viền mặt)", ACCENT_CYAN),
            ("Ảnh cắt \& co kích thước (128x128)", ACCENT_BLUE),
            ("Giai đoạn 2: NHẬN DIỆN (FBG dày trung tâm)", ACCENT_LAVENDER)
        ]
        
        flow_boxes = VGroup()
        flow_arrows = VGroup()
        
        for idx, (text, color) in enumerate(box_texts):
            box = RoundedRectangle(
                corner_radius=0.06, width=7.2, height=0.55, color=color, stroke_width=1.2,
                fill_color=BG_NAVY_SOFT, fill_opacity=0.8
            ).move_to(flow_coords[idx])
            lbl = vn_tex_bold(text, color=TEXT_PRIMARY, scale=0.38).move_to(box.get_center())
            flow_boxes.add(VGroup(box, lbl))
            
            # Connecting arrow
            if idx > 0:
                arrow = Arrow(flow_coords[idx - 1] + DOWN * 0.28, flow_coords[idx] + UP * 0.28, color=TEXT_MUTED, buff=0, stroke_width=2.5)
                flow_arrows.add(arrow)

        self.play(
            LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in flow_boxes], lag_ratio=0.2),
            LaggedStart(*[Create(a) for a in flow_arrows], lag_ratio=0.2),
            run_time=1.8
        )
        self.wait(1.5)

        # Fade out flowchart
        self.play(
            FadeOut(flow_boxes),
            FadeOut(flow_arrows),
            run_time=0.8
        )

        # ============================================================
        # PHASE B: Stage 1 — Normalization (10s - 30s)
        # ============================================================
        # Subtitle 2 (6s - 14s)
        update_sub("Giai đoạn 1: Chuẩn hóa ảnh dùng FBG thưa, tập trung viền mặt", 6.0)

        # Left: Large Original Image Frame
        img_frame_large = RoundedRectangle(
            corner_radius=0.08, width=3.8, height=4.8, color=ACCENT_BLUE, stroke_width=1.2,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.4
        ).shift(LEFT * 3.2 + DOWN * 0.3)
        lbl_img_l = vn_tex("Ảnh gốc (Tỷ lệ tự do)", color=ACCENT_BLUE, scale=0.4).next_to(img_frame_large, UP, buff=0.18)

        # Vector face contour inside the frame (scaled up)
        face_l = Arc(radius=1.3, start_angle=-PI/2, angle=PI, color=TEXT_MUTED, stroke_width=0.8).move_to(img_frame_large.get_center())
        face_l_lines = VGroup(
            face_l,
            Line(face_l.get_top(), face_l.get_center() + UP * 0.3 + RIGHT * 0.8, color=TEXT_MUTED, stroke_width=0.8),
            Line(face_l.get_center() + UP * 0.3 + RIGHT * 0.8, face_l.get_center() + DOWN * 0.0 + RIGHT * 0.9, color=TEXT_MUTED, stroke_width=0.8),
            Line(face_l.get_center() + DOWN * 0.0 + RIGHT * 0.9, face_l.get_center() + DOWN * 0.4 + RIGHT * 0.3, color=TEXT_MUTED, stroke_width=0.8),
            Arc(radius=0.2, start_angle=PI/2, angle=-PI/2, color=TEXT_MUTED, stroke_width=0.8).move_to(face_l.get_center() + DOWN * 1.0 + RIGHT * 0.25)
        )

        self.play(
            FadeIn(img_frame_large),
            FadeIn(lbl_img_l),
            FadeIn(face_l_lines),
            run_time=1.2
        )

        # Overlay Stage 1 sparse grid (outline focused)
        sparse_g = make_sparse_outline_grid(img_frame_large.get_center(), color=ACCENT_CYAN, scale=1.4)
        lbl_sparse = vn_tex_bold("Stage 1: Outline-focused Grid", color=ACCENT_CYAN, scale=0.4).next_to(img_frame_large, DOWN, buff=0.18)

        self.play(
            FadeIn(sparse_g, shift=RIGHT * 0.2),
            FadeIn(lbl_sparse, shift=UP * 0.1),
            run_time=1.2
        )
        self.wait(1.0)

        # Right: Normalization bullet points
        note_bg = RoundedRectangle(
            corner_radius=0.08, width=5.6, height=3.8, color=TEXT_MUTED, stroke_width=0.8,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.8
        ).shift(RIGHT * 3.2 + DOWN * 0.3)
        note_title = vn_tex_bold("GIAI ĐOẠN 1: CHUẨN HÓA", color=ACCENT_CYAN, scale=0.45).shift(RIGHT * 3.2 + UP * 1.1)

        bullets_1 = VGroup(
            vn_tex("- Số lượng: M = 30 models mẫu", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("- Vị trí nút: Tập trung ở đường viền mặt", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("- Mục tiêu: Định vị và cắt cúp mặt", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("- Hiệu suất: ~99\% chính xác trong tìm mặt", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("- Tốc độ: ~20s trên SPARCstation 10-512", color=TEXT_MUTED, scale=0.35)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(note_title, DOWN, buff=0.35).align_to(note_title, LEFT)

        self.play(
            FadeIn(note_bg),
            FadeIn(note_title, shift=UP * 0.15),
            LaggedStart(*[FadeIn(bullet, shift=RIGHT * 0.15) for bullet in bullets_1], lag_ratio=0.15),
            run_time=1.5
        )
        self.wait(1.5)

        # Subtitle 3 (14s - 22s)
        update_sub("Mục tiêu: định vị và crop khuôn mặt về kích thước chuẩn 128x128 pixel", 6.0)

        # Show Cropping / Bounding Box box and Shrink
        crop_box = Rectangle(width=3.2, height=3.8, color=HIGHLIGHT_HOT, stroke_width=2.2).move_to(img_frame_large.get_center())
        self.play(Create(crop_box), run_time=0.8)
        self.play(
            Flash(crop_box.get_center(), color=HIGHLIGHT_HOT, flash_radius=1.2),
            run_time=0.6
        )

        # Shrink large image to a small 128x128 normalized frame
        img_frame_small = RoundedRectangle(
            corner_radius=0.08, width=2.4, height=2.4, color=ACCENT_CYAN, stroke_width=1.5,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.6
        ).shift(LEFT * 3.2 + DOWN * 0.3)
        lbl_img_s = vn_tex("Cắt chuẩn (128x128 px)", color=ACCENT_CYAN, scale=0.38).next_to(img_frame_small, UP, buff=0.18)

        small_face = Arc(radius=0.6, start_angle=-PI/2, angle=PI, color=TEXT_MUTED, stroke_width=0.6).move_to(img_frame_small.get_center())
        small_face_lines = VGroup(
            small_face,
            Line(small_face.get_top(), small_face.get_center() + UP * 0.15 + RIGHT * 0.35, color=TEXT_MUTED, stroke_width=0.6),
            Line(small_face.get_center() + UP * 0.15 + RIGHT * 0.35, small_face.get_center() + DOWN * 0.0 + RIGHT * 0.4, color=TEXT_MUTED, stroke_width=0.6),
            Line(small_face.get_center() + DOWN * 0.0 + RIGHT * 0.4, small_face.get_center() + DOWN * 0.2 + RIGHT * 0.12, color=TEXT_MUTED, stroke_width=0.6),
            Arc(radius=0.1, start_angle=PI/2, angle=-PI/2, color=TEXT_MUTED, stroke_width=0.6).move_to(small_face.get_center() + DOWN * 0.45 + RIGHT * 0.1)
        )

        self.play(
            FadeOut(face_l_lines),
            FadeOut(sparse_g),
            FadeOut(lbl_sparse),
            FadeOut(lbl_img_l),
            ReplacementTransform(img_frame_large, img_frame_small),
            ReplacementTransform(crop_box, img_frame_small),
            FadeIn(lbl_img_s, shift=UP * 0.1),
            FadeIn(small_face_lines),
            run_time=1.5
        )
        self.wait(1.5)

        # ============================================================
        # PHASE C: Stage 2 — Recognition (30s - 50s)
        # ============================================================
        # Subtitle 4 (22s - 30s)
        update_sub("Giai đoạn 2: Nhận diện khuôn mặt đã chuẩn hóa sử dụng FBG dày đặc", 6.0)

        # Transition notes on the right to Stage 2
        note_title_2 = vn_tex_bold("GIAI ĐOẠN 2: NHẬN DIỆN CHI TIẾT", color=ACCENT_LAVENDER, scale=0.45).shift(RIGHT * 3.2 + UP * 1.1)

        bullets_2 = VGroup(
            vn_tex("- Số lượng: M = 70 models đầy đủ", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("- Vị trí nút: Phân bố dày đặc trong mặt", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("- Mục tiêu: Trích xuất đặc trưng chi tiết", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("- Chức năng: So khớp biểu cảm \& cấu trúc mắt/mũi", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("- Tốc độ: Chỉ ~10s cho việc trích xuất sạch", color=TEXT_MUTED, scale=0.35)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(note_title_2, DOWN, buff=0.35).align_to(note_title_2, LEFT)

        self.play(
            ReplacementTransform(note_title, note_title_2),
            ReplacementTransform(bullets_1, bullets_2),
            run_time=1.2
        )

        # Subtitle 5 (30s - 38s)
        update_sub("Hệ thống áp dụng đồ thị 8 nút mốc nội thất dày đặc lên ảnh 128x128", 5.0)

        # Overlay Stage 2 interior-heavy dense grid
        dense_g = make_dense_interior_grid(img_frame_small.get_center(), color=ACCENT_LAVENDER, scale=0.7)
        lbl_dense = vn_tex_bold("Stage 2: Interior-focused Grid", color=ACCENT_LAVENDER, scale=0.38).next_to(img_frame_small, DOWN, buff=0.22)

        self.play(
            FadeIn(dense_g, shift=RIGHT * 0.25),
            FadeIn(lbl_dense, shift=UP * 0.1),
            run_time=1.5
        )
        self.wait(1.5)

        # Subtitle 6 (38s - 50s)
        update_sub("Đầu ra là Image Graph cuối cùng cực kỳ chi tiết, sẵn sàng cho việc so sánh!", 6.0)
        
        self.play(
            Flash(dense_g.get_center(), color=ACCENT_LAVENDER, flash_radius=0.8),
            Indicate(dense_g, scale_factor=1.05, color=ACCENT_LAVENDER),
            run_time=1.2
        )
        self.wait(2.5)

        # Cleanup everything
        self.play(
            FadeOut(title),
            FadeOut(img_frame_small),
            FadeOut(lbl_img_s),
            FadeOut(small_face_lines),
            FadeOut(dense_g),
            FadeOut(lbl_dense),
            FadeOut(note_bg),
            FadeOut(note_title_2),
            FadeOut(bullets_2),
            run_time=0.8
        )
        self.wait(0.3)
