"""
EBGM Video — Part 4: Discussion (FINAL PART)
Scene 27: Intro Discussion & Tính tổng quát
Thời lượng dự kiến: 45s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - Be Vietnam Pro:  https://fonts.google.com/specimen/Be+Vietnam+Pro
  - EB Garamond:     https://fonts.google.com/specimen/EB+Garamond
  - JetBrains Mono:  https://fonts.google.com/specimen/JetBrains+Mono

Render command:
  manim -pql scene_27_intro_generality.py Scene27_IntroGenerality
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# COLOR PALETTE (redeclare để standalone / nhất quán với kịch bản)
# ============================================================
BG_NAVY         = "#0D1B2A"
BG_NAVY_SOFT    = "#1B263B"
TEXT_PRIMARY    = "#E0E1DD"
TEXT_MUTED      = "#A9B4C2"
ACCENT_CYAN     = "#48CAE4"
ACCENT_TEAL     = "#76C5BF"
ACCENT_BLUE     = "#778DA9"
ACCENT_MINT     = "#95D5B2"
ACCENT_LAVENDER = "#B8B5FF"
ACCENT_CORAL    = "#E29578"
GRID_LINE       = "#778DA9"

# === BENCHMARK & SYSTEM COLORS ===
EBGM_BRAND      = "#B8B5FF"   # lavender
PCA_COLOR       = "#76C5BF"   # teal
NN_COLOR        = "#E29578"   # coral nhạt
PREV_COLOR      = "#778DA9"   # blue-grey
YUILLE_COLOR    = "#8896AB"   # xám lạnh
LANITIS_COLOR   = "#5FA8D3"   # blue
WARP_COLOR      = "#A7C5EB"   # light blue

# === PROS / CONS / FUTURE ===
PRO_COLOR       = "#95D5B2"   # mint
CON_COLOR       = "#E29578"   # coral
FUTURE_GLOW     = "#B8B5FF"   # lavender
TROPHY_GOLD     = "#FCBF49"

SUBTITLE_FONT = "Be Vietnam Pro"
TITLE_FONT    = "EB Garamond"
MONO_FONT     = "JetBrains Mono"

# ============================================================
# HELPERS (Bổ sung đầy đủ cho phần 4)
# ============================================================
def make_vs_card(title_left, title_right, color_left, color_right, scale=1.0):
    """
    Card so sánh 'X vs Y': 2 panel cạnh nhau với divider 'VS' ở giữa.
    Trả về VGroup(panel_l, panel_r, lbl_l, lbl_r, vs).
    Panel rỗng để caller tự thêm nội dung vào sau.
    """
    panel_l = RoundedRectangle(
        width=3.0, height=2.0, corner_radius=0.15,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.6,
        stroke_color=color_left, stroke_width=2
    ).shift(LEFT * 2.0)
    panel_r = RoundedRectangle(
        width=3.0, height=2.0, corner_radius=0.15,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.6,
        stroke_color=color_right, stroke_width=2
    ).shift(RIGHT * 2.0)
    lbl_l = vn_tex_bold(title_left, color=color_left, scale=0.4).move_to(panel_l.get_top() + DOWN * 0.3)
    lbl_r = vn_tex_bold(title_right, color=color_right, scale=0.4).move_to(panel_r.get_top() + DOWN * 0.3)
    vs = vn_tex_bold("VS", color=TEXT_MUTED, scale=0.6)
    return VGroup(panel_l, panel_r, lbl_l, lbl_r, vs).scale(scale)


def pro_item(text_str, scale=0.4):
    """Dòng điểm mạnh với check icon mint (vẽ tay, KHÔNG emoji)."""
    check = VGroup(
        Line([-0.08, -0.02, 0], [-0.02, -0.08, 0], color=PRO_COLOR, stroke_width=3),
        Line([-0.02, -0.08, 0], [0.08, 0.06, 0], color=PRO_COLOR, stroke_width=3),
    )
    txt = vn_tex(text_str, color=TEXT_PRIMARY, scale=scale)
    return VGroup(check, txt).arrange(RIGHT, buff=0.2)


def con_item(text_str, scale=0.4):
    """Dòng điểm yếu với cross icon coral (vẽ tay, KHÔNG emoji)."""
    cross = VGroup(
        Line([-0.06, 0.06, 0], [0.06, -0.06, 0], color=CON_COLOR, stroke_width=3),
        Line([-0.06, -0.06, 0], [0.06, 0.06, 0], color=CON_COLOR, stroke_width=3),
    )
    txt = vn_tex(text_str, color=TEXT_PRIMARY, scale=scale)
    return VGroup(cross, txt).arrange(RIGHT, buff=0.2)


def future_node(text_str, icon_mob, color=FUTURE_GLOW, scale=1.0):
    """Node cho roadmap: icon + text trong rounded box."""
    box = RoundedRectangle(
        width=2.8, height=1.2, corner_radius=0.12,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.7,
        stroke_color=color, stroke_width=1.5
    )
    tex_str = r"\begin{tabular}{l} " + text_str.replace("\n", r" \\ ") + r" \end{tabular}"
    txt = vn_tex(tex_str, color=TEXT_PRIMARY, scale=0.38)
    icon_mob.scale(0.5).move_to(box.get_left() + RIGHT * 0.5)
    txt.next_to(icon_mob, RIGHT, buff=0.25)
    return VGroup(box, icon_mob, txt).scale(scale)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene27_IntroGenerality(Scene):
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
        # PHASE A: Tiêu đề & câu hỏi mở (0s - 12s)
        # ============================================================
        sub_1 = make_subtitle("EBGM đã hiệu quả — nhưng nó đứng ở đâu giữa các hệ thống khác?")
        self.current_sub = sub_1
        self.play(FadeIn(sub_1, shift=UP * 0.15), run_time=0.4)

        # Tiêu đề chính
        title = vn_tex_bold("Discussion --- Đặt EBGM Vào Bức Tranh Lớn", color=ACCENT_LAVENDER, scale=0.85)
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=1.0)

        # Soft floating graph nodes in the background
        bg_nodes = VGroup()
        bg_positions = [
            [-5.5, 2.0, 0], [-4.0, 2.8, 0], [-5.0, 0.8, 0],
            [5.5, -2.0, 0], [4.5, -1.2, 0], [5.0, -2.8, 0]
        ]
        for pos in bg_positions:
            node = Dot(pos, color=ACCENT_LAVENDER, radius=0.05).set_opacity(0.3)
            bg_nodes.add(node)
        
        bg_lines = VGroup(
            Line(bg_positions[0], bg_positions[1], color=ACCENT_LAVENDER, stroke_width=0.8).set_opacity(0.2),
            Line(bg_positions[0], bg_positions[2], color=ACCENT_LAVENDER, stroke_width=0.8).set_opacity(0.2),
            Line(bg_positions[3], bg_positions[4], color=ACCENT_LAVENDER, stroke_width=0.8).set_opacity(0.2),
            Line(bg_positions[3], bg_positions[5], color=ACCENT_LAVENDER, stroke_width=0.8).set_opacity(0.2)
        )
        self.play(FadeIn(bg_nodes), FadeIn(bg_lines), run_time=1.0)

        # Lead text
        lead_text = vn_tex("EBGM đã hiệu quả. Nhưng nó đứng ở đâu giữa các hệ thống khác?", color=TEXT_PRIMARY, scale=0.48)
        lead_text.move_to(UP * 0.2)
        self.play(FadeIn(lead_text, shift=UP * 0.15), run_time=1.0)
        self.wait(3.1) # Wait out the remaining duration of 6s total

        # Update subtitle early at 6s
        sub_2 = make_subtitle("Trước hết: EBGM không chỉ dành cho khuôn mặt")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2
        self.wait(5.6) # Wait out until 12s total

        # Clean Phase A for Phase B
        self.play(FadeOut(lead_text), run_time=0.6)

        # ============================================================
        # PHASE B: Tính tổng quát — Không chỉ khuôn mặt (12s - 32s)
        # ============================================================
        sub_3 = make_subtitle("Nó giải quyết bài toán nhận diện trong cùng một lớp đối tượng")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        # Center text: IN-CLASS RECOGNITION
        center_text = vn_tex_bold("IN-CLASS RECOGNITION", color=ACCENT_LAVENDER, scale=0.75)
        center_text.move_to(ORIGIN)
        self.play(Write(center_text), run_time=1.2)

        # Orbit circle path (subtle)
        orbit_path = Circle(radius=2.2, color=ACCENT_LAVENDER, stroke_width=1.0).set_opacity(0.2)
        self.play(FadeIn(orbit_path), run_time=0.8)

        # 4 Vector Icons around the center
        # 1. Face Silhouette
        face_head = Circle(radius=0.35, color=ACCENT_CYAN, stroke_width=1.5)
        face_eye_l = Dot(face_head.get_center() + LEFT * 0.12 + UP * 0.08, radius=0.03, color=ACCENT_CYAN)
        face_eye_r = Dot(face_head.get_center() + RIGHT * 0.12 + UP * 0.08, radius=0.03, color=ACCENT_CYAN)
        face_mouth = Arc(radius=0.08, start_angle=-5*PI/6, angle=2*PI/3, color=ACCENT_CYAN, stroke_width=1.5).move_to(face_head.get_center() + DOWN * 0.1)
        face_icon = VGroup(face_head, face_eye_l, face_eye_r, face_mouth)
        lbl_face = vietnamese_label("Khuôn mặt", scale=0.32, color=TEXT_PRIMARY).next_to(face_icon, UP, buff=0.12)
        group_face = VGroup(face_icon, lbl_face)

        # 2. Paw Print Silhouette
        paw_pad = Ellipse(width=0.32, height=0.24, color=ACCENT_TEAL, fill_color=ACCENT_TEAL, fill_opacity=0.3, stroke_width=1.5)
        paw_toe_1 = Circle(radius=0.05, color=ACCENT_TEAL, fill_color=ACCENT_TEAL, fill_opacity=0.3, stroke_width=1.2).move_to(paw_pad.get_center() + LEFT * 0.16 + UP * 0.12)
        paw_toe_2 = Circle(radius=0.06, color=ACCENT_TEAL, fill_color=ACCENT_TEAL, fill_opacity=0.3, stroke_width=1.2).move_to(paw_pad.get_center() + LEFT * 0.05 + UP * 0.18)
        paw_toe_3 = Circle(radius=0.06, color=ACCENT_TEAL, fill_color=ACCENT_TEAL, fill_opacity=0.3, stroke_width=1.2).move_to(paw_pad.get_center() + RIGHT * 0.05 + UP * 0.18)
        paw_toe_4 = Circle(radius=0.05, color=ACCENT_TEAL, fill_color=ACCENT_TEAL, fill_opacity=0.3, stroke_width=1.2).move_to(paw_pad.get_center() + RIGHT * 0.16 + UP * 0.12)
        paw_icon = VGroup(paw_pad, paw_toe_1, paw_toe_2, paw_toe_3, paw_toe_4)
        lbl_paw = vietnamese_label("Động vật", scale=0.32, color=TEXT_PRIMARY).next_to(paw_icon, UP, buff=0.12)
        group_paw = VGroup(paw_icon, lbl_paw)

        # 3. Car Silhouette
        car_body = RoundedRectangle(width=0.6, height=0.22, corner_radius=0.04, color=ACCENT_BLUE, fill_color=ACCENT_BLUE, fill_opacity=0.3, stroke_width=1.5)
        car_cabin = Polygon(
            [-0.2, 0.11, 0], [0.2, 0.11, 0], [0.12, 0.25, 0], [-0.12, 0.25, 0],
            color=ACCENT_BLUE, fill_color=ACCENT_BLUE, fill_opacity=0.3, stroke_width=1.5
        )
        car_wheel_l = Circle(radius=0.07, color=ACCENT_BLUE, fill_color=BG_NAVY, fill_opacity=1.0, stroke_width=1.5).move_to(car_body.get_center() + LEFT * 0.18 + DOWN * 0.11)
        car_wheel_r = Circle(radius=0.07, color=ACCENT_BLUE, fill_color=BG_NAVY, fill_opacity=1.0, stroke_width=1.5).move_to(car_body.get_center() + RIGHT * 0.18 + DOWN * 0.11)
        car_icon = VGroup(car_body, car_cabin, car_wheel_l, car_wheel_r)
        lbl_car = vietnamese_label("Phương tiện", scale=0.32, color=TEXT_PRIMARY).next_to(car_icon, DOWN, buff=0.12)
        group_car = VGroup(car_icon, lbl_car)

        # 4. Flower Silhouette
        flower_center = Circle(radius=0.08, color=ACCENT_MINT, fill_color=ACCENT_MINT, fill_opacity=0.4, stroke_width=1.5)
        petals = VGroup()
        for angle in np.linspace(0, 2*PI, 6, endpoint=False):
            petal = Circle(radius=0.08, color=ACCENT_MINT, fill_color=ACCENT_MINT, fill_opacity=0.2, stroke_width=1.2)
            petal.move_to(flower_center.get_center() + np.array([0.13 * np.cos(angle), 0.13 * np.sin(angle), 0]))
            petals.add(petal)
        flower_icon = VGroup(flower_center, petals)
        lbl_flower = vietnamese_label("Thực vật", scale=0.32, color=TEXT_PRIMARY).next_to(flower_icon, DOWN, buff=0.12)
        group_flower = VGroup(flower_icon, lbl_flower)

        # Initial placements
        group_face.move_to(UP * 2.2)
        group_paw.move_to(RIGHT * 2.2)
        group_car.move_to(DOWN * 2.2)
        group_flower.move_to(LEFT * 2.2)

        # Dashed connecting lines
        line_face = DashedLine(ORIGIN, UP * 2.2, color=ACCENT_LAVENDER, stroke_width=1.2).set_opacity(0.6)
        line_paw = DashedLine(ORIGIN, RIGHT * 2.2, color=ACCENT_LAVENDER, stroke_width=1.2).set_opacity(0.6)
        line_car = DashedLine(ORIGIN, DOWN * 2.2, color=ACCENT_LAVENDER, stroke_width=1.2).set_opacity(0.6)
        line_flower = DashedLine(ORIGIN, LEFT * 2.2, color=ACCENT_LAVENDER, stroke_width=1.2).set_opacity(0.6)

        # Pop in orbits
        self.play(
            LaggedStart(
                FadeIn(group_face, shift=DOWN*0.2),
                FadeIn(group_paw, shift=LEFT*0.2),
                FadeIn(group_car, shift=UP*0.2),
                FadeIn(group_flower, shift=RIGHT*0.2),
                lag_ratio=0.2
            ),
            Create(line_face), Create(line_paw), Create(line_car), Create(line_flower),
            run_time=2.0
        )
        self.wait(1.5)

        # Update Subtitle to sub_4 (22s)
        sub_4 = make_subtitle("Cùng cấu trúc — có thể áp dụng cho động vật, xe cộ, thực vật")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4

        # Group them to perform Upright Orbit Rotation using ValueTracker
        theta = ValueTracker(0)

        # Updaters to keep icons upright while they orbit!
        def update_face(mob):
            angle = theta.get_value()
            mob.move_to(np.array([2.2 * np.cos(angle + PI/2), 2.2 * np.sin(angle + PI/2), 0]))
        def update_paw(mob):
            angle = theta.get_value()
            mob.move_to(np.array([2.2 * np.cos(angle), 2.2 * np.sin(angle), 0]))
        def update_car(mob):
            angle = theta.get_value()
            mob.move_to(np.array([2.2 * np.cos(angle - PI/2), 2.2 * np.sin(angle - PI/2), 0]))
        def update_flower(mob):
            angle = theta.get_value()
            mob.move_to(np.array([2.2 * np.cos(angle + PI), 2.2 * np.sin(angle + PI), 0]))

        group_face.add_updater(update_face)
        group_paw.add_updater(update_paw)
        group_car.add_updater(update_car)
        group_flower.add_updater(update_flower)

        # Update dashed lines
        line_face.add_updater(lambda m: m.put_start_and_end_on(ORIGIN, group_face[0].get_center()))
        line_paw.add_updater(lambda m: m.put_start_and_end_on(ORIGIN, group_paw[0].get_center()))
        line_car.add_updater(lambda m: m.put_start_and_end_on(ORIGIN, group_car[0].get_center()))
        line_flower.add_updater(lambda m: m.put_start_and_end_on(ORIGIN, group_flower[0].get_center()))

        # Animate orbit rotation
        self.play(theta.animate.set_value(60 * DEGREES), run_time=6.5, rate_func=linear)
        self.wait(1.1)

        # Clean up Phase B updaters & objects
        group_face.clear_updaters()
        group_paw.clear_updaters()
        group_car.clear_updaters()
        group_flower.clear_updaters()
        
        self.play(
            FadeOut(center_text), FadeOut(orbit_path),
            FadeOut(group_face), FadeOut(group_paw), FadeOut(group_car), FadeOut(group_flower),
            FadeOut(line_face), FadeOut(line_paw), FadeOut(line_car), FadeOut(line_flower),
            run_time=0.8
        )
        self.wait(0.2)

        # ============================================================
        # PHASE C: 3 ưu thế cốt lõi & Gauge (32s - 45s)
        # ============================================================
        sub_5 = make_subtitle("Ba ưu thế: không cần huấn luyện, chỉ một ảnh, robust đến 22°")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5

        # 3 Badges setup
        badge_w, badge_h = 3.6, 2.2
        badge_y = 0.5
        badge_x = [-4.3, 0, 4.3]

        # Badge 1: No training
        b1_bg = RoundedRectangle(width=badge_w, height=badge_h, corner_radius=0.12, fill_color=BG_NAVY_SOFT, fill_opacity=0.85, stroke_color=ACCENT_LAVENDER, stroke_width=1.5).move_to(np.array([badge_x[0], badge_y, 0]))
        gear = Circle(radius=0.24, color=TEXT_MUTED, stroke_width=1.5)
        gear_slash = Line([-0.25, 0.25, 0], [0.25, -0.25, 0], color=ACCENT_CORAL, stroke_width=2.5)
        circle_no = Circle(radius=0.3, color=ACCENT_CORAL, stroke_width=2.5)
        gear_icon = VGroup(gear, circle_no, gear_slash).scale(0.85).next_to(b1_bg.get_top(), DOWN, buff=0.25)
        b1_title = vn_tex_bold("Không Cần Training", color=ACCENT_LAVENDER, scale=0.36).next_to(gear_icon, DOWN, buff=0.15)
        b1_desc = vn_tex("Không cần tập dữ liệu lớn", color=TEXT_MUTED, scale=0.28).next_to(b1_title, DOWN, buff=0.08)
        badge_1 = VGroup(b1_bg, gear_icon, b1_title, b1_desc)

        # Badge 2: One image
        b2_bg = RoundedRectangle(width=badge_w, height=badge_h, corner_radius=0.12, fill_color=BG_NAVY_SOFT, fill_opacity=0.85, stroke_color=ACCENT_CYAN, stroke_width=1.5).move_to(np.array([badge_x[1], badge_y, 0]))
        cam_body = RoundedRectangle(width=0.48, height=0.3, corner_radius=0.04, color=ACCENT_CYAN, stroke_width=1.5)
        cam_lens = Circle(radius=0.1, color=ACCENT_CYAN, stroke_width=1.5).move_to(cam_body.get_center())
        cam_flash = Circle(radius=0.025, color=ACCENT_CYAN, stroke_width=1.0).move_to(cam_body.get_corner(UP+RIGHT) + DOWN*0.06 + LEFT*0.06)
        cam_top = Polygon([-0.12, 0.15, 0], [0.12, 0.15, 0], [0.08, 0.22, 0], [-0.08, 0.22, 0], color=ACCENT_CYAN, stroke_width=1.5)
        cam_icon = VGroup(cam_body, cam_lens, cam_flash, cam_top).scale(0.85).next_to(b2_bg.get_top(), DOWN, buff=0.25)
        b2_title = vn_tex_bold("Chỉ 1 Ảnh Mẫu", color=ACCENT_CYAN, scale=0.36).next_to(cam_icon, DOWN, buff=0.15)
        b2_desc = vn_tex("Nhận diện từ 1 ảnh gallery", color=TEXT_MUTED, scale=0.28).next_to(b2_title, DOWN, buff=0.08)
        badge_2 = VGroup(b2_bg, cam_icon, b2_title, b2_desc)

        # Badge 3: Robust 22
        b3_bg = RoundedRectangle(width=badge_w, height=badge_h, corner_radius=0.12, fill_color=BG_NAVY_SOFT, fill_opacity=0.85, stroke_color=ACCENT_MINT, stroke_width=1.5).move_to(np.array([badge_x[2], badge_y, 0]))
        gauge_arc_mini = Arc(radius=0.25, start_angle=0, angle=5*PI/6, color=ACCENT_MINT, stroke_width=2.5)
        gauge_arc_drop = Arc(radius=0.25, start_angle=5*PI/6, angle=PI/6, color=ACCENT_CORAL, stroke_width=2.5)
        gauge_center = Dot(radius=0.03, color=TEXT_PRIMARY)
        gauge_needle = Line(ORIGIN, 0.22 * np.array([np.cos(5*PI/6), np.sin(5*PI/6), 0]), color=TEXT_PRIMARY, stroke_width=2.0)
        mini_gauge_icon = VGroup(gauge_arc_mini, gauge_arc_drop, gauge_center, gauge_needle).scale(0.85).next_to(b3_bg.get_top(), DOWN, buff=0.25)
        b3_title = vn_tex_bold("Robust Đến $22^\\circ$", color=ACCENT_MINT, scale=0.36).next_to(mini_gauge_icon, DOWN, buff=0.15)
        b3_desc = vn_tex("Chịu được góc xoay nhỏ", color=TEXT_MUTED, scale=0.28).next_to(b3_title, DOWN, buff=0.08)
        badge_3 = VGroup(b3_bg, mini_gauge_icon, b3_title, b3_desc)

        # Pop in badges sequentially
        self.play(FadeIn(badge_1, shift=UP*0.25), run_time=0.8)
        self.play(FadeIn(badge_2, shift=UP*0.25), run_time=0.8)
        self.play(FadeIn(badge_3, shift=UP*0.25), run_time=0.8)
        self.wait(1.6) # Wait out sub_5 (until 40s)

        # Subtitle to sub_6 (40s - 45s)
        sub_6 = make_subtitle("Nhưng hiệu năng giảm đáng kể ở các góc xoay lớn hơn")
        self.play(ReplacementTransform(self.current_sub, sub_6), run_time=0.4)
        self.current_sub = sub_6

        # Draw Dynamic Gauge below Badge 3
        gauge_center_pos = np.array([badge_x[2], -1.8, 0])
        gauge_bg = Arc(radius=0.7, start_angle=PI, angle=-PI, color=TEXT_MUTED, stroke_width=2.0).move_to(gauge_center_pos)
        
        # Color areas
        arc_robust = Arc(radius=0.7, start_angle=PI, angle=-PI * 22/90, color=ACCENT_MINT, stroke_width=3.5).move_to(gauge_center_pos)
        arc_drop = Arc(radius=0.7, start_angle=PI * (1 - 22/90), angle=-PI * 68/90, color=ACCENT_CORAL, stroke_width=3.5).move_to(gauge_center_pos)
        
        gauge_dot = Dot(gauge_center_pos, radius=0.04, color=TEXT_PRIMARY)
        needle = Line(gauge_center_pos, gauge_center_pos + np.array([-0.6, 0, 0]), color=TEXT_PRIMARY, stroke_width=2.5) # Points to 0 degree initially (left)

        lbl_0 = vn_tex("$0^\\circ$", color=TEXT_MUTED, scale=0.22).next_to(gauge_bg.get_start(), DOWN * 0.15)
        lbl_22 = vn_tex("$22^\\circ$", color=ACCENT_MINT, scale=0.22).move_to(gauge_center_pos + 0.88 * np.array([np.cos(PI - PI * 22/90), np.sin(PI - PI * 22/90), 0]))
        lbl_90 = vn_tex("$90^\\circ$", color=TEXT_MUTED, scale=0.22).next_to(gauge_bg.get_end(), DOWN * 0.15)

        # Performance text states inside gauge
        perf_0 = vn_tex("98\\%", color=ACCENT_MINT, scale=0.35).move_to(gauge_center_pos + UP * 0.18)
        perf_22 = vn_tex("96\\%", color=ACCENT_MINT, scale=0.35).move_to(gauge_center_pos + UP * 0.18)
        perf_45 = vn_tex("18\\%", color=ACCENT_CORAL, scale=0.35).move_to(gauge_center_pos + UP * 0.18)

        gauge_group = VGroup(gauge_bg, arc_robust, arc_drop, gauge_dot, needle, lbl_0, lbl_22, lbl_90, perf_0)
        self.play(FadeIn(gauge_group, shift=UP*0.2), run_time=0.8)
        self.wait(0.6)

        # Animate needle swing 0 -> 22 degrees
        self.play(
            Rotate(needle, angle=-PI * 22/90, about_point=gauge_center_pos),
            Transform(perf_0, perf_22),
            run_time=1.0
        )
        self.wait(0.4)

        # Animate needle swing 22 -> 45 degrees
        self.play(
            Rotate(needle, angle=-PI * 23/90, about_point=gauge_center_pos),
            Transform(perf_0, perf_45),
            run_time=1.2
        )
        self.wait(1.0) # Wait until 45s total

        # ============================================================
        # CLEANUP
        # ============================================================
        self.play(
            FadeOut(title),
            FadeOut(badge_1), FadeOut(badge_2), FadeOut(badge_3),
            FadeOut(gauge_group), FadeOut(perf_0),
            FadeOut(bg_nodes), FadeOut(bg_lines),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
