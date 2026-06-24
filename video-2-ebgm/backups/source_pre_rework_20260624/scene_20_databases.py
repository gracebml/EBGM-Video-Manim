"""
EBGM Video — Part 3: Experiments
Scene 20: Databases (FERET & Bochum)
Thời lượng dự kiến: 50s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)

Render command:
  manim -pql scene_20_databases.py Scene20_Databases
  manim -pqh scene_20_databases.py Scene20_Databases  # high quality
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# PART 3 COLOR PALETTE
# ============================================================
BAR_PRIMARY   = "#48CAE4"
BAR_SECONDARY = "#778DA9"
BAR_SUCCESS   = "#95D5B2"
BAR_WARNING   = "#E29578"
TROPHY_GOLD   = "#FCBF49"

EBGM_BRAND    = "#B8B5FF"
PCA_COLOR     = "#76C5BF"
NN_COLOR      = "#E29578"
PREV_COLOR    = "#778DA9"

# ============================================================
# VECTOR SILHOUETTE GENERATORS (Tránh dùng file ảnh ngoài)
# ============================================================
def make_frontal_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt chính diện (Frontal)."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    eye_l = Dot(head.get_center() + LEFT * 0.18 + UP * 0.1, radius=0.04, color=color)
    eye_r = Dot(head.get_center() + RIGHT * 0.18 + UP * 0.1, radius=0.04, color=color)
    mouth = Arc(radius=0.12, start_angle=-5*PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.18)
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, mouth, shoulders).scale(scale)


def make_expression_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt có biểu cảm khác biệt (Frontal B)."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    # Mắt cười híp
    eye_l = Arc(radius=0.08, start_angle=PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + LEFT * 0.18 + UP * 0.1)
    eye_r = Arc(radius=0.08, start_angle=PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + RIGHT * 0.18 + UP * 0.1)
    # Miệng cười rộng
    mouth = ArcPolygon(
        head.get_center() + LEFT * 0.18 + DOWN * 0.12,
        head.get_center() + RIGHT * 0.18 + DOWN * 0.12,
        head.get_center() + DOWN * 0.25,
        color=color, fill_opacity=0.4, stroke_width=1.2
    )
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, mouth, shoulders).scale(scale)


def make_half_profile_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt nghiêng vừa (Half-Profile)."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    # Các mốc chi tiết lệch sang bên trái
    eye_l = Dot(head.get_center() + LEFT * 0.28 + UP * 0.1, radius=0.035, color=color)
    eye_r = Dot(head.get_center() + LEFT * 0.02 + UP * 0.1, radius=0.045, color=color)
    nose = Line(head.get_center() + LEFT * 0.15 + UP * 0.05, head.get_center() + LEFT * 0.35 - DOWN * 0.05, color=color, stroke_width=1.2)
    mouth = Arc(radius=0.1, start_angle=-5*PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + LEFT * 0.15 + DOWN * 0.18)
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, nose, mouth, shoulders).scale(scale)


def make_profile_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt nghiêng hẳn 90 độ (Profile)."""
    # Đường cong gáy và đầu
    profile_line = VMobject(color=color, stroke_width=1.5)
    points = [
        np.array([0, 0.5, 0]),
        np.array([0.2, 0.4, 0]),
        np.array([0.3, 0.1, 0]),
        np.array([0.2, -0.3, 0]),
        np.array([-0.05, -0.6, 0]),
    ]
    profile_line.set_points_as_corners(points)
    
    # Mặt trước: Trán, mũi, môi, cằm
    face_line = VMobject(color=color, stroke_width=1.5)
    face_points = [
        np.array([0, 0.5, 0]),
        np.array([-0.18, 0.35, 0]),
        np.array([-0.2, 0.15, 0]),
        np.array([-0.42, 0.05, 0]),
        np.array([-0.22, -0.08, 0]),
        np.array([-0.28, -0.15, 0]),
        np.array([-0.22, -0.22, 0]),
        np.array([-0.28, -0.3, 0]),
        np.array([-0.12, -0.45, 0]),
        np.array([-0.08, -0.6, 0]),
    ]
    face_line.set_points_as_corners(face_points)
    
    # Mắt dạng nghiêng
    eye = Triangle(color=color, stroke_width=1.0).scale(0.06).move_to(np.array([-0.12, 0.18, 0]))
    # Vai nghiêng
    shoulders = Arc(radius=0.7, start_angle=PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(np.array([0.1, -0.9, 0]))
    
    return VGroup(profile_line, face_line, eye, shoulders).scale(scale)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene20_Databases(Scene):
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
        # PHASE A: Setup câu hỏi (0s - 8s)
        # ============================================================
        title = section_title("Thử nghiệm trên cơ sở dữ liệu nào?", color=ACCENT_CYAN)
        title.to_edge(UP, buff=0.6)
        
        hint = vn_tex("Đặc biệt: gallery chỉ chứa đúng MỘT ảnh cho mỗi người", color=ACCENT_CYAN, scale=0.42)
        hint.next_to(title, DOWN, buff=0.18)

        # Phụ đề 1
        sub_1 = make_subtitle("Hai cơ sở dữ liệu lớn được sử dụng để kiểm chứng")
        self.current_sub = sub_1

        self.play(
            FadeIn(title, shift=DOWN * 0.25),
            FadeIn(hint, shift=UP * 0.15),
            FadeIn(sub_1, shift=UP * 0.15),
            run_time=1.5
        )
        self.wait(6.5)

        # ============================================================
        # PHASE B: FERET Database (8s - 32s)
        # ============================================================
        # 1. Chuyển phụ đề sang sub_2
        sub_2 = make_subtitle("FERET — 250 người, do quân đội Mỹ cung cấp")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # 2. Tạo FERET Info Box bên trái
        feret_box_bg = RoundedRectangle(
            corner_radius=0.08, width=5.2, height=3.6, color=ACCENT_CYAN, stroke_width=1.0,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.85
        ).shift(LEFT * 3.4 + DOWN * 0.4)
        
        feret_title = vn_tex_bold("ARPA/ARL FERET DATABASE", color=ACCENT_CYAN, scale=0.43).move_to(feret_box_bg.get_center() + UP * 1.3)
        feret_subtitle = vn_tex("US Army Research Lab", color=TEXT_MUTED, scale=0.35).move_to(feret_box_bg.get_center() + UP * 0.95)
        
        divider = Line(feret_box_bg.get_center() + UP * 0.8 + LEFT * 2.2, feret_box_bg.get_center() + UP * 0.8 + RIGHT * 2.2, color=TEXT_MUTED, stroke_width=0.5).set_opacity(0.5)
        
        feret_bullets = VGroup(
            vn_tex(r"$\bullet$ 250 người (gallery chuẩn)", color=TEXT_PRIMARY, scale=0.36),
            vn_tex(r"$\bullet$ Đúng 1 ảnh / người mẫu", color=TEXT_PRIMARY, scale=0.36),
            vn_tex(r"$\bullet$ Kích thước: 256 $\times$ 384 px", color=TEXT_PRIMARY, scale=0.36),
            vn_tex(r"$\bullet$ Nền ảnh: đồng nhất đơn giản", color=TEXT_PRIMARY, scale=0.36)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(divider, DOWN, buff=0.25).align_to(divider, LEFT).shift(RIGHT * 0.2)
        
        feret_box = VGroup(feret_box_bg, feret_title, feret_subtitle, divider, feret_bullets)

        self.play(FadeIn(feret_box, shift=RIGHT * 0.3), run_time=1.2)
        self.wait(4.0)

        # 3. Phụ đề sub_3 & Grid 4 tư thế xuất hiện bên phải (14s)
        sub_3 = make_subtitle("Bốn tư thế: chính diện, nghiêng 40-70°, profile, biểu cảm khác")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        grid_positions = [
            np.array([1.9, 0.6, 0]),
            np.array([4.9, 0.6, 0]),
            np.array([1.9, -1.2, 0]),
            np.array([4.9, -1.2, 0])
        ]
        
        pose_data = [
            ("frontal", "Frontal (Chính diện)"),
            ("expression", "Expression (Biểu cảm)"),
            ("half_profile", "Half-Profile (Nghiêng vừa)"),
            ("profile", "Profile (Nghiêng hẳn)")
        ]

        pose_boxes = VGroup()
        for idx, (pose_type, lbl) in enumerate(pose_data):
            pos = grid_positions[idx]
            bg_rect = RoundedRectangle(
                corner_radius=0.06, width=2.6, height=1.6, color=TEXT_MUTED, stroke_width=0.6,
                fill_color=BG_NAVY_SOFT, fill_opacity=0.7
            ).move_to(pos)
            
            if pose_type == "frontal":
                sil = make_frontal_silhouette(color=ACCENT_CYAN, scale=0.7).move_to(pos + UP * 0.1)
            elif pose_type == "expression":
                sil = make_expression_silhouette(color=ACCENT_CYAN, scale=0.7).move_to(pos + UP * 0.1)
            elif pose_type == "half_profile":
                sil = make_half_profile_silhouette(color=ACCENT_LAVENDER, scale=0.7).move_to(pos + UP * 0.1)
            else:
                sil = make_profile_silhouette(color=ACCENT_LAVENDER, scale=0.7).move_to(pos + UP * 0.1)
                
            lbl_text = vn_tex(lbl, color=TEXT_PRIMARY, scale=0.3).next_to(bg_rect, DOWN, buff=0.1)
            
            box_group = VGroup(bg_rect, sil, lbl_text)
            pose_boxes.add(box_group)

        self.play(
            LaggedStart(*[FadeIn(box, shift=UP * 0.2) for box in pose_boxes], lag_ratio=0.35),
            run_time=1.8
        )
        self.wait(4.2)

        # 4. Phụ đề sub_4 & Highlight độ khó góc nghiêng (22s)
        sub_4 = make_subtitle("Setup khắc nghiệt: gallery chỉ có MỘT ảnh cho mỗi người")
        difficulty_note = vn_tex("Góc nghiêng 40-70 độ: Cực kỳ thử thách!", color=ACCENT_CORAL, scale=0.35).move_to(DOWN * 2.2)

        self.play(
            ReplacementTransform(self.current_sub, sub_4),
            Indicate(pose_boxes[2], color=ACCENT_CORAL, scale_factor=1.05),
            Indicate(pose_boxes[3], color=ACCENT_CORAL, scale_factor=1.05),
            FadeIn(difficulty_note, shift=UP * 0.1),
            run_time=1.2
        )
        self.current_sub = sub_4
        self.wait(8.8)

        # Dọn dẹp FERET
        self.play(
            FadeOut(feret_box),
            FadeOut(pose_boxes),
            FadeOut(difficulty_note),
            run_time=0.8
        )
        self.wait(0.2)

        # ============================================================
        # PHASE C: Bochum Database (32s - 50s)
        # ============================================================
        # 1. Phụ đề sub_5
        sub_5 = make_subtitle("Bochum — 108 người, tập trung vào kiểm tra xoay nhỏ trong không gian 3D")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5

        # 2. Tạo Bochum Info Box bên trái
        bochum_box_bg = RoundedRectangle(
            corner_radius=0.08, width=5.2, height=3.6, color=ACCENT_LAVENDER, stroke_width=1.0,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.85
        ).shift(LEFT * 3.4 + DOWN * 0.4)
        
        bochum_title = vn_tex_bold("BOCHUM DATABASE", color=ACCENT_LAVENDER, scale=0.45).move_to(bochum_box_bg.get_center() + UP * 1.3)
        bochum_subtitle = vn_tex("Institute for Neural Computation", color=TEXT_MUTED, scale=0.32).move_to(bochum_box_bg.get_center() + UP * 0.95)
        
        divider_b = Line(bochum_box_bg.get_center() + UP * 0.8 + LEFT * 2.2, bochum_box_bg.get_center() + UP * 0.8 + RIGHT * 2.2, color=TEXT_MUTED, stroke_width=0.5).set_opacity(0.5)
        
        bochum_bullets = VGroup(
            vn_tex(r"$\bullet$ 108 người (gallery frontal)", color=TEXT_PRIMARY, scale=0.36),
            vn_tex(r"$\bullet$ Góc xoay nhỏ: 0, 11 và 22 độ", color=TEXT_PRIMARY, scale=0.36),
            vn_tex(r"$\bullet$ Biểu cảm thay đổi linh hoạt", color=TEXT_PRIMARY, scale=0.36),
            vn_tex(r"$\bullet$ Trọng tâm: So khớp đa góc (cross-pose)", color=TEXT_PRIMARY, scale=0.36)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(divider_b, DOWN, buff=0.25).align_to(divider_b, LEFT).shift(RIGHT * 0.2)
        
        bochum_box = VGroup(bochum_box_bg, bochum_title, bochum_subtitle, divider_b, bochum_bullets)

        self.play(FadeIn(bochum_box, shift=RIGHT * 0.3), run_time=1.2)
        self.wait(7.0)

        # 3. Phụ đề sub_6 & 3 ô xoay ngang bên phải (42s)
        sub_6 = make_subtitle("Mục tiêu: matching ảnh xoay 11 và 22 độ với ảnh mẫu chính diện")
        self.play(ReplacementTransform(self.current_sub, sub_6), run_time=0.4)
        self.current_sub = sub_6

        b_positions = [
            np.array([0.7, -0.4, 0]),
            np.array([3.4, -0.4, 0]),
            np.array([6.1, -0.4, 0])
        ]
        
        bochum_poses = VGroup()
        b_data = [
            ("0", "0 độ (Chính diện)"),
            ("11", "11 độ (Xoay nhẹ)"),
            ("22", "22 độ (Xoay vừa)")
        ]
        
        for idx, (angle, lbl) in enumerate(b_data):
            pos = b_positions[idx]
            bg_rect = RoundedRectangle(
                corner_radius=0.06, width=2.1, height=2.0, color=TEXT_MUTED, stroke_width=0.6,
                fill_color=BG_NAVY_SOFT, fill_opacity=0.7
            ).move_to(pos)
            
            if angle == "0":
                sil = make_frontal_silhouette(color=ACCENT_CYAN, scale=0.75).move_to(pos + UP * 0.2)
            elif angle == "11":
                sil = make_half_profile_silhouette(color=ACCENT_LAVENDER, scale=0.75).move_to(pos + UP * 0.2)
            else:
                sil = make_half_profile_silhouette(color=ACCENT_LAVENDER, scale=0.75).move_to(pos + UP * 0.2)
                # Nghiêng hẹp x hơn để tạo cảm giác góc xoay lớn hơn
                sil.stretch_to_fit_width(0.4)
                
            lbl_text = vn_tex(lbl, color=TEXT_PRIMARY, scale=0.28).next_to(bg_rect, DOWN, buff=0.1)
            bochum_poses.add(VGroup(bg_rect, sil, lbl_text))

        self.play(
            LaggedStart(*[FadeIn(b_pose, shift=UP * 0.2) for b_pose in bochum_poses], lag_ratio=0.35),
            run_time=1.5
        )
        self.wait(0.5)

        # 4. Mũi tên kết nối 3 cụm góc xoay
        arrow1 = CurvedArrow(b_positions[0] + UP * 0.7 + RIGHT * 0.8, b_positions[1] + UP * 0.7 + LEFT * 0.8, color=ACCENT_LAVENDER, angle=-PI/4, stroke_width=1.8)
        arrow2 = CurvedArrow(b_positions[1] + UP * 0.7 + RIGHT * 0.8, b_positions[2] + UP * 0.7 + LEFT * 0.8, color=ACCENT_LAVENDER, angle=-PI/4, stroke_width=1.8)
        
        cross_pose_lbl = vn_tex("Thử thách Cross-Pose", color=ACCENT_LAVENDER, scale=0.32).move_to(np.array([3.4, 1.2, 0]))

        self.play(
            Create(arrow1),
            Create(arrow2),
            FadeIn(cross_pose_lbl, shift=DOWN * 0.1),
            run_time=1.2
        )
        self.wait(3.7)

        # ============================================================
        # CLEANUP
        # ============================================================
        self.play(
            FadeOut(title),
            FadeOut(hint),
            FadeOut(bochum_box),
            FadeOut(bochum_poses),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(cross_pose_lbl),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
