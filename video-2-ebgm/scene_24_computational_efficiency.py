"""
EBGM Video — Part 3: Experiments
Scene 24: Computational Efficiency
Thời lượng dự kiến: 55s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)

Render command:
  manim -pql scene_24_computational_efficiency.py Scene24_ComputationalEfficiency
  manim -pqh scene_24_computational_efficiency.py Scene24_ComputationalEfficiency  # high quality
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
# ADDITIONAL HELPERS
# ============================================================
def make_clock(radius=1.0, color=TEXT_PRIMARY):
    """Vẽ chiếc đồng hồ vector gồm vỏ, vạch giờ và kim quay."""
    circle = Circle(radius=radius, color=color, stroke_width=2.5)
    ticks = VGroup()
    for i in range(12):
        angle = i * 2 * PI / 12
        tick = Line(
            circle.get_center() + np.array([np.cos(angle)*radius*0.85, np.sin(angle)*radius*0.85, 0]),
            circle.get_center() + np.array([np.cos(angle)*radius*0.96, np.sin(angle)*radius*0.96, 0]),
            color=color, stroke_width=0.8
        ).set_opacity(0.6)
        ticks.add(tick)
    # Kim phút và kim giờ
    hand_hour = Line(circle.get_center(), circle.get_center() + UP * radius * 0.5, color=color, stroke_width=3.0)
    hand_min = Line(circle.get_center(), circle.get_center() + UP * radius * 0.8, color=color, stroke_width=1.8)
    return VGroup(circle, ticks, hand_hour, hand_min)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene24_ComputationalEfficiency(Scene):
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
        # PHASE A: Setup tiêu đề (0s - 10s)
        # ============================================================
        title = section_title("EBGM có nhanh không?", color=ACCENT_CYAN)
        title.to_edge(UP, buff=0.6)
        
        intro_lbl = vn_tex("Ứng dụng thời gian thực — Khả thi hay không?", color=ACCENT_CYAN, scale=0.42)
        intro_lbl.next_to(title, DOWN, buff=0.18)

        # Phụ đề 1
        sub_1 = make_subtitle("EBGM có đủ nhanh cho ứng dụng thực tế không?")
        self.current_sub = sub_1

        self.play(
            FadeIn(title, shift=DOWN * 0.25),
            FadeIn(intro_lbl, shift=UP * 0.15),
            FadeIn(sub_1, shift=UP * 0.15),
            run_time=1.5
        )
        self.wait(8.5)

        # ============================================================
        # PHASE B: Timeline visualization (10s - 30s)
        # ============================================================
        # 1. Phụ đề sub_2 (10s)
        sub_2 = make_subtitle("Hệ thống tiền nhiệm: 25 giây để so sánh với 87 models")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # 2. Xây dựng trục timeline Preceding System (y = 1.2)
        tl_l_y = 1.2
        line_old_axis = Line(LEFT * 4.0, RIGHT * 4.0, color=TEXT_MUTED, stroke_width=0.8).shift(UP * tl_l_y)
        # Vạch trục
        vach_old = VGroup()
        for x_val, label in zip([-4.0, -2.4, -0.8, 0.8, 2.4, 4.0], ["0s", "5s", "10s", "15s", "20s", "25s"]):
            v = Line(np.array([x_val, tl_l_y-0.1, 0]), np.array([x_val, tl_l_y+0.1, 0]), color=TEXT_MUTED, stroke_width=0.8)
            lbl = vn_tex_mono(label, color=TEXT_MUTED, scale=0.28).next_to(v, UP, buff=0.08)
            vach_old.add(VGroup(v, lbl))
            
        bar_old = Rectangle(
            width=8.0, height=0.26, fill_color=PREV_COLOR, fill_opacity=0.85,
            stroke_color=PREV_COLOR, stroke_width=1
        ).move_to(np.array([0, tl_l_y, 0]))
        
        info_old = vn_tex("So khớp 87 models mất 25 giây", color=PREV_COLOR, scale=0.35).next_to(line_old_axis, DOWN, buff=0.15)
        timeline_old_group = VGroup(line_old_axis, vach_old, bar_old, info_old)

        # 3. Xây dựng trục timeline EBGM (y = -0.6)
        tl_r_y = -0.6
        line_new_axis = Line(LEFT * 4.0, RIGHT * 4.0, color=TEXT_MUTED, stroke_width=0.8).shift(UP * tl_r_y)
        vach_new = VGroup()
        for x_val, label in zip([-4.0, -2.4, -0.8, 0.8, 2.4, 4.0], ["0s", "5s", "10s", "15s", "20s", "25s"]):
            v = Line(np.array([x_val, tl_r_y-0.1, 0]), np.array([x_val, tl_r_y+0.1, 0]), color=TEXT_MUTED, stroke_width=0.8)
            lbl = vn_tex_mono(label, color=TEXT_MUTED, scale=0.28).next_to(v, UP, buff=0.08)
            vach_new.add(VGroup(v, lbl))
            
        # EBGM chỉ mất < 1 giây nên thanh bar siêu ngắn (8.0 * 1/25 = 0.32)
        bar_new = Rectangle(
            width=0.32, height=0.26, fill_color=EBGM_BRAND, fill_opacity=0.85,
            stroke_color=EBGM_BRAND, stroke_width=1
        ).move_to(np.array([-4.0 + 0.16, tl_r_y, 0]))
        
        info_new = vn_tex("So khớp $\\sim$300 models chỉ dưới 1 giây!", color=EBGM_BRAND, scale=0.35).next_to(line_new_axis, DOWN, buff=0.15)
        timeline_new_group = VGroup(line_new_axis, vach_new, bar_new, info_new)

        # Trình diễn Timeline 1 (Hệ cũ) chạy trong 4 giây
        self.play(
            FadeIn(line_old_axis), FadeIn(vach_old),
            GrowFromEdge(bar_old, LEFT),
            run_time=4.0
        )
        self.play(FadeIn(info_old, shift=UP * 0.1), run_time=0.8)
        self.wait(1.2)

        # Phụ đề sub_3 (15s)
        sub_3 = make_subtitle("EBGM: chỉ 1 giây để so sánh với 300 models")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        # Trình diễn Timeline 2 (EBGM) chạy siêu nhanh trong 0.5s
        self.play(
            FadeIn(line_new_axis), FadeIn(vach_new),
            GrowFromEdge(bar_new, LEFT),
            run_time=0.5
        )
        self.play(FadeIn(info_new, shift=UP * 0.1), run_time=0.6)
        self.wait(1.9)

        # 4. Phụ đề sub_4 & Đồng hồ kim quay vù vù (22s)
        sub_4 = make_subtitle("Tốc độ tăng khoảng 1000 lần")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4

        # Dọn dẹp timeline nhanh
        self.play(
            FadeOut(timeline_old_group),
            FadeOut(timeline_new_group),
            run_time=0.6
        )

        clock = make_clock(radius=1.1, color=TEXT_PRIMARY).move_to(ORIGIN)
        lbl_old = vn_tex_bold("Hệ thống cũ: 0.29 models/s", color=PREV_COLOR, scale=0.42).move_to(LEFT * 4.2)
        lbl_new = vn_tex_bold("Hệ EBGM: 300 models/s", color=EBGM_BRAND, scale=0.42).move_to(RIGHT * 4.2)
        lbl_speedup = vn_tex_bold("Nhanh hơn ~1000 lần!", color=ACCENT_MINT, scale=0.5).move_to(DOWN * 1.8)

        # Hiện đồng hồ + 2 nhãn bên cạnh
        self.play(
            FadeIn(clock),
            FadeIn(lbl_old, shift=RIGHT * 0.2),
            FadeIn(lbl_new, shift=LEFT * 0.2),
            run_time=1.0
        )
        # Quay kim đồng hồ
        self.play(
            Rotate(clock[3], angle=-6*2*PI, about_point=clock[0].get_center(), rate_func=linear),
            Rotate(clock[2], angle=-2*PI/2, about_point=clock[0].get_center(), rate_func=linear),
            FadeIn(lbl_speedup, shift=UP * 0.2),
            run_time=3.5
        )
        self.wait(2.5)

        # Dọn dẹp Phase B
        self.play(
            FadeOut(clock),
            FadeOut(lbl_old),
            FadeOut(lbl_new),
            FadeOut(lbl_speedup),
            run_time=0.8
        )

        # ============================================================
        # PHASE C: Pipeline breakdown (30s - 50s)
        # ============================================================
        # 1. Phụ đề sub_5 (32s)
        sub_5 = make_subtitle("Bí quyết: tách bạch extraction (chậm, 1 lần) khỏi comparison (siêu nhanh)")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5

        # 2. Xây dựng Sơ đồ Pipeline
        box_w, box_h = 3.2, 1.4
        
        box1_bg = RoundedRectangle(corner_radius=0.06, width=box_w, height=box_h, color=TEXT_MUTED, stroke_width=0.8, fill_color=BG_NAVY_SOFT, fill_opacity=0.8).move_to(np.array([-4.2, 0.4, 0]))
        box1_txt = vn_tex_bold("ẢNH ĐẦU VÀO", color=TEXT_PRIMARY, scale=0.35).move_to(box1_bg.get_center())
        box1 = VGroup(box1_bg, box1_txt)

        box2_bg = RoundedRectangle(corner_radius=0.06, width=box_w, height=box_h, color=ACCENT_CYAN, stroke_width=1.0, fill_color=BG_NAVY_SOFT, fill_opacity=0.8).move_to(np.array([0.0, 0.4, 0]))
        box2_txt1 = vn_tex_bold("TRÍCH XUẤT ĐỒ THỊ", color=ACCENT_CYAN, scale=0.32).move_to(box2_bg.get_center() + UP * 0.2)
        box2_txt2 = vn_tex("(Chỉ làm 1 lần duy nhất)", color=TEXT_MUTED, scale=0.26).move_to(box2_bg.get_center() + DOWN * 0.22)
        box2 = VGroup(box2_bg, box2_txt1, box2_txt2)

        box3_bg = RoundedRectangle(corner_radius=0.06, width=box_w, height=box_h, color=EBGM_BRAND, stroke_width=1.0, fill_color=BG_NAVY_SOFT, fill_opacity=0.8).move_to(np.array([4.2, 0.4, 0]))
        box3_txt1 = vn_tex_bold("SO KHỚP GALLERY", color=EBGM_BRAND, scale=0.32).move_to(box3_bg.get_center() + UP * 0.2)
        box3_txt2 = vn_tex("(Nhanh chớp mắt với mồi)", color=ACCENT_MINT, scale=0.26).move_to(box3_bg.get_center() + DOWN * 0.22)
        box3 = VGroup(box3_bg, box3_txt1, box3_txt2)

        # Mũi tên kết nối
        arrow1 = Arrow(box1_bg.get_right(), box2_bg.get_left(), color=TEXT_MUTED, buff=0.1, stroke_width=2.5)
        arrow2 = Arrow(box2_bg.get_right(), box3_bg.get_left(), color=TEXT_MUTED, buff=0.1, stroke_width=2.5)
        
        lbl_arrow1 = vn_tex_mono("~30s", color=ACCENT_CORAL, scale=0.32).next_to(arrow1, UP, buff=0.08)
        lbl_arrow2 = vn_tex_mono("<1s", color=ACCENT_MINT, scale=0.32).next_to(arrow2, UP, buff=0.08)

        # Insight box ở dưới
        insight_box = vn_tex("Bí quyết: Tách bạch trích xuất đồ thị (1 lần) khỏi so khớp (nhiều lần)", color=ACCENT_LAVENDER, scale=0.38).move_to(DOWN * 1.6)

        # Hiện sơ đồ
        self.play(
            FadeIn(box1), FadeIn(box2), FadeIn(box3),
            Create(arrow1), Create(arrow2),
            FadeIn(lbl_arrow1), FadeIn(lbl_arrow2),
            run_time=1.5
        )
        self.wait(1.0)

        # 3. Hoạt động "ảnh nhỏ" di chuyển kèm Timer
        timer_tracker = ValueTracker(0.0)
        timer_lbl = always_redraw(
            lambda: vn_tex_mono(f"Thời gian trôi: {timer_tracker.get_value():.1f} s", color=ACCENT_CYAN, scale=0.35).move_to(np.array([0, -0.6, 0]))
        )
        
        # Ảnh mẫu trôi
        probe_icon = RoundedRectangle(
            corner_radius=0.03, width=0.5, height=0.7, color=ACCENT_CYAN, stroke_width=0.8,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.9
        ).move_to(box1_bg.get_center())

        self.play(FadeIn(probe_icon), FadeIn(timer_lbl), run_time=0.6)

        # Bước 1: ẢNH ĐẦU VÀO -> TRÍCH XUẤT ĐỒ THỊ (30s)
        self.play(
            probe_icon.animate.move_to(box2_bg.get_center()),
            timer_tracker.animate.set_value(30.0),
            run_time=3.5,
            rate_func=bezier([0, 0, 1, 1])
        )
        self.wait(0.5)

        # Bước 2: Reset timer và chạy siêu nhanh TRÍCH XUẤT -> SO KHỚP (< 0.8s)
        timer_tracker.set_value(0.0)
        self.play(
            probe_icon.animate.move_to(box3_bg.get_center()),
            timer_tracker.animate.set_value(0.8),
            run_time=0.8,
            rate_func=linear
        )
        self.wait(0.6)

        # Hiện insight box
        self.play(FadeIn(insight_box, shift=UP * 0.15), run_time=0.8)
        self.wait(5.2)

        # Dọn dẹp Phase C
        self.play(
            FadeOut(box1), FadeOut(box2), FadeOut(box3),
            FadeOut(arrow1), FadeOut(arrow2),
            FadeOut(lbl_arrow1), FadeOut(lbl_arrow2),
            FadeOut(probe_icon), FadeOut(timer_lbl),
            FadeOut(insight_box),
            run_time=0.8
        )
        self.wait(0.2)

        # ============================================================
        # PHASE D: Real-world implication (50s - 55s)
        # ============================================================
        # Phụ đề sub_6 (42s)
        sub_6 = make_subtitle("Đủ nhanh cho database lớn — và đã được thương mại hóa thành công")
        self.play(ReplacementTransform(self.current_sub, sub_6), run_time=0.4)
        self.current_sub = sub_6

        conclusion = vn_tex("Đủ nhanh cho ứng dụng thực tế — kể cả với database lớn", color=TEXT_PRIMARY, scale=0.45).move_to(UP * 0.8)
        comm_note = vn_tex_italic("(Cùng nhóm nghiên cứu sau này đã thương mại hóa thành công hệ thống ZN-Face)", color=ACCENT_LAVENDER, scale=0.34).move_to(DOWN * 0.4)

        self.play(
            FadeIn(conclusion, shift=DOWN * 0.15),
            FadeIn(comm_note, shift=UP * 0.15),
            run_time=1.2
        )
        self.wait(3.1)

        # Cleanup kết thúc scene
        self.play(
            FadeOut(conclusion),
            FadeOut(comm_note),
            FadeOut(title),
            FadeOut(intro_lbl),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
