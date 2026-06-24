"""
EBGM Video — Part 3: Experiments
Scene 23: Matching Accuracy — Pha vs Không pha
Thời lượng dự kiến: 70s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)

Render command:
  manim -pql scene_23_phase_importance.py Scene23_PhaseImportance
  manim -pqh scene_23_phase_importance.py Scene23_PhaseImportance  # high quality
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
# ADDITIONAL HELPER FOR VALUE ROUNDED CIRCLE
# ============================================================
def make_value_circle(val_str, color=ACCENT_CYAN, radius=0.6):
    """Vòng tròn bo góc hiển thị số liệu lớn."""
    bg = Circle(radius=radius, color=color, stroke_width=2, fill_color=BG_NAVY_SOFT, fill_opacity=0.85)
    text = vn_tex_bold(val_str, color=color, scale=0.75 * radius)
    text.move_to(bg.get_center())
    return VGroup(bg, text)


# ============================================================
# VECTOR SILHOUETTE GENERATOR (Frontal Face)
# ============================================================
def make_frontal_silhouette(color=TEXT_MUTED, scale=0.6):
    """Vẽ khuôn mặt chính diện chuẩn."""
    head = Circle(radius=0.5, color=color, stroke_width=1.2)
    eye_l = Dot(head.get_center() + LEFT * 0.18 + UP * 0.1, radius=0.04, color=color)
    eye_r = Dot(head.get_center() + RIGHT * 0.18 + UP * 0.1, radius=0.04, color=color)
    mouth = Arc(radius=0.12, start_angle=-5*PI/6, angle=2*PI/3, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.18)
    shoulders = Arc(radius=0.7, start_angle=0, angle=PI, color=color, stroke_width=1.2).move_to(head.get_center() + DOWN * 0.8)
    return VGroup(head, eye_l, eye_r, mouth, shoulders).scale(scale)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene23_PhaseImportance(Scene):
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
        # PHASE A: Setup câu hỏi (0s - 10s)
        # ============================================================
        title = section_title("Tại sao pha quan trọng?", color=ACCENT_CYAN)
        title.to_edge(UP, buff=0.6)
        
        question = vn_tex("Bỏ qua pha thì sao? Đây là thí nghiệm trực quan nhất.", color=TEXT_PRIMARY, scale=0.4)
        question.next_to(title, DOWN, buff=0.18)

        # Phụ đề 1
        sub_1 = make_subtitle("Pha trong Gabor wavelet quan trọng thế nào?")
        self.current_sub = sub_1

        self.play(
            FadeIn(title, shift=DOWN * 0.25),
            FadeIn(question, shift=UP * 0.15),
            FadeIn(sub_1, shift=UP * 0.15),
            run_time=1.5
        )
        self.wait(4.5)

        # ============================================================
        # PHASE B: Visualize matching accuracy (10s - 35s)
        # ============================================================
        # 1. Chuyển phụ đề sang sub_2 (6s)
        sub_2 = make_subtitle("So sánh trực tiếp: matching có phase vs không phase")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2
        self.wait(3.6) # Đợi nốt phase A đến giây thứ 10

        # 2. Xây dựng split-screen
        split_line = Line(UP * 1.8, DOWN * 2.0, color=TEXT_MUTED, stroke_width=0.8).set_opacity(0.3)
        
        # Nhãn tiêu đề 2 bên
        lbl_l = vn_tex_bold("Không dùng pha", color=ACCENT_CORAL, scale=0.4).move_to(LEFT * 3.5 + UP * 1.8)
        lbl_r = vn_tex_bold("Dùng pha (EBGM)", color=ACCENT_MINT, scale=0.4).move_to(RIGHT * 3.5 + UP * 1.8)

        # Silhouettes
        sil_l = make_frontal_silhouette(color=TEXT_MUTED, scale=0.75).move_to(LEFT * 3.5 + UP * 0.15)
        sil_r = make_frontal_silhouette(color=TEXT_MUTED, scale=0.75).move_to(RIGHT * 3.5 + UP * 0.15)

        # Định nghĩa 8 nodes gốc đối xứng trên mặt để so khớp
        ref_offsets = [
            np.array([-0.25, 0.2, 0]),   # mắt trái
            np.array([0.25, 0.2, 0]),    # mắt phải
            np.array([0.0, 0.05, 0]),    # mũi
            np.array([0.0, -0.15, 0]),   # miệng
            np.array([-0.38, -0.05, 0]), # má trái
            np.array([0.38, -0.05, 0]),  # má phải
            np.array([-0.2, -0.35, 0]),  # cằm trái
            np.array([0.2, -0.35, 0])    # cằm phải
        ]

        # --- BÊN TRÁI: KHÔNG DÙNG PHA (Sai lệch ngẫu nhiên lớn trung bình 5.2px) ---
        dots_l_ref = VGroup()
        dots_l_algo = VGroup()
        lines_l = VGroup()

        # Seed random để tạo sự nhất quán và tránh run_time lệch
        np.random.seed(42)
        for i, offset in enumerate(ref_offsets):
            ref_pos = sil_l.get_center() + offset
            # Lệch nhiều (từ 0.15 đến 0.35 đơn vị)
            angle = np.random.uniform(0, 2*PI)
            dist = np.random.uniform(0.18, 0.32)
            # Riêng node má phải bị sai hẳn lệch rất xa ra biên ngoài
            if i == 5:
                algo_pos = ref_pos + np.array([0.48, 0.15, 0])
            else:
                algo_pos = ref_pos + np.array([np.cos(angle)*dist, np.sin(angle)*dist, 0])
                
            dot_ref = Dot(ref_pos, radius=0.05, color=EBGM_BRAND) # Chấm hồng reference
            dot_algo = Dot(algo_pos, radius=0.05, color=ACCENT_CYAN) # Chấm cyan algorithm
            line = Line(ref_pos, algo_pos, color=ACCENT_CORAL, stroke_width=1.0)
            
            dots_l_ref.add(dot_ref)
            dots_l_algo.add(dot_algo)
            lines_l.add(line)
            
        dots_l = VGroup(dots_l_ref, dots_l_algo)
        circle_left = make_value_circle("5.2 px", color=ACCENT_CORAL, radius=0.55).move_to(LEFT * 3.5 + DOWN * 1.3)

        # --- BÊN PHẢI: DÙNG PHA (Trùng khít gần như hoàn hảo trung bình 1.6px) ---
        dots_r_ref = VGroup()
        dots_r_algo = VGroup()
        lines_r = VGroup()

        for i, offset in enumerate(ref_offsets):
            ref_pos = sil_r.get_center() + offset
            # Lệch rất ít (từ 0.02 đến 0.06 đơn vị)
            angle = np.random.uniform(0, 2*PI)
            dist = np.random.uniform(0.02, 0.06)
            algo_pos = ref_pos + np.array([np.cos(angle)*dist, np.sin(angle)*dist, 0])
            
            dot_ref = Dot(ref_pos, radius=0.05, color=EBGM_BRAND)
            dot_algo = Dot(algo_pos, radius=0.05, color=ACCENT_CYAN)
            line = Line(ref_pos, algo_pos, color=ACCENT_MINT, stroke_width=0.8)
            
            dots_r_ref.add(dot_ref)
            dots_r_algo.add(dot_algo)
            lines_r.add(line)
            
        dots_r = VGroup(dots_r_ref, dots_r_algo)
        circle_right = make_value_circle("1.6 px", color=ACCENT_MINT, radius=0.55).move_to(RIGHT * 3.5 + DOWN * 1.3)

        # Hiện 2 silhouettes, 2 nhãn và trục dọc trước
        self.play(
            FadeIn(split_line),
            FadeIn(lbl_l),
            FadeIn(lbl_r),
            FadeIn(sil_l),
            FadeIn(sil_r),
            run_time=1.2
        )

        # 3. Phụ đề sub_3 & Vẽ bên trái (14s)
        sub_3 = make_subtitle("Không pha: trung bình 5.2 pixel sai so với người đánh dấu thủ công")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        self.play(
            FadeIn(dots_l_ref),
            run_time=0.6
        )
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    Create(line),
                    FadeIn(dot_a)
                ) for line, dot_a in zip(lines_l, dots_l_algo)
            ], lag_ratio=0.15),
            FadeIn(circle_left, shift=UP * 0.15),
            run_time=2.2
        )
        self.wait(1.5)

        # 4. Phụ đề sub_4 & Vẽ bên phải (22s)
        sub_4 = make_subtitle("Có pha: chỉ 1.6 pixel — chính xác đến mức subpixel")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4

        self.play(
            FadeIn(dots_r_ref),
            run_time=0.6
        )
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    Create(line),
                    FadeIn(dot_a)
                ) for line, dot_a in zip(lines_r, dots_r_algo)
            ], lag_ratio=0.15),
            FadeIn(circle_right, shift=UP * 0.15),
            run_time=2.2
        )
        self.wait(1.5)

        # 5. Phụ đề sub_5 (30s)
        sub_5 = make_subtitle("Khác biệt 3 lần — nhưng ảnh hưởng đến độ nhận diện thế nào?")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5
        self.wait(4.6)

        # ============================================================
        # PHASE C: Recognition rate khác biệt (35s - 55s)
        # ============================================================
        # 1. Thu nhỏ và gom Phase B lên phía trên làm context
        phase_b_group = VGroup(
            split_line, lbl_l, lbl_r, sil_l, sil_r, 
            dots_l, dots_r, lines_l, lines_r, 
            circle_left, circle_right
        )
        self.play(
            phase_b_group.animate.scale(0.55).shift(UP * 1.55),
            title.animate.scale(0.75).shift(UP * 0.05),
            question.animate.scale(0.75).shift(UP * 0.05),
            run_time=1.2
        )

        # 2. Xây dựng Biểu đồ cột ngang Recognition Rate phía dưới
        values_c = [89, 88, 67]
        labels_c = [
            "Vị trí chuẩn (thủ công)",
            "Có pha (With phase)",
            "Không pha (No phase)"
        ]

        bar_y = [-0.3, -0.9, -1.5]
        c_bars = VGroup()
        
        for i, (val, lbl) in enumerate(zip(values_c, labels_c)):
            color = ACCENT_MINT if i < 2 else ACCENT_CORAL
            # Chiều rộng thanh bar tỉ lệ thực tế
            w = val / 100 * 5.0
            bar = Rectangle(
                width=w, height=0.32, fill_color=color, fill_opacity=0.85,
                stroke_color=color, stroke_width=1
            ).move_to(np.array([-2.4 + w/2, bar_y[i], 0]))
            
            # Nhãn nằm bên trái thanh bar thẳng hàng
            lbl_text = vn_tex(lbl, color=TEXT_PRIMARY, scale=0.35)
            lbl_text.next_to(bar, LEFT, buff=0.25).align_to(bar, LEFT).shift(LEFT * 2.8)
            
            # Chỉ số % nằm bên phải
            val_text = vn_tex_mono(f"{val:.0f}\%", color=color, scale=0.35)
            val_text.next_to(bar, RIGHT, buff=0.15)
            
            c_bars.add(VGroup(bar, lbl_text, val_text))

        # Phụ đề sub_6 (40s)
        sub_6 = make_subtitle("Test trên ảnh xoay 22$^\circ$: dùng phase đạt 88\%")
        self.play(
            ReplacementTransform(self.current_sub, sub_6),
            run_time=0.4
        )
        self.current_sub = sub_6

        # Hiện các cột bar ngang mượt mà từ trái sang
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    GrowFromEdge(b, LEFT),
                    FadeIn(lbl),
                    FadeIn(val)
                ) for b, lbl, val in c_bars
            ], lag_ratio=0.25),
            run_time=2.0
        )

        # Highlight cột "With phase"
        self.play(
            Indicate(c_bars[1][2], color=ACCENT_MINT, scale_factor=1.15),
            Flash(c_bars[1][2].get_center(), color=ACCENT_MINT, flash_radius=0.4),
            run_time=1.0
        )
        self.wait(1.5)

        # Phụ đề sub_7 (50s)
        sub_7 = make_subtitle("Bỏ phase: chỉ còn 67\% — mất đến 21 điểm phần trăm!")
        self.play(
            ReplacementTransform(self.current_sub, sub_7),
            run_time=0.4
        )
        self.current_sub = sub_7

        # Highlight thanh "Without phase" sụt giảm
        self.play(
            Indicate(c_bars[2], color=ACCENT_CORAL, scale_factor=1.05),
            run_time=1.0
        )

        # Vẽ mũi tên so sánh và ghi chú sụt giảm 21%
        arrow_insight = DoubleArrow(c_bars[1][0].get_right() + RIGHT * 0.1, c_bars[2][0].get_right() + RIGHT * 0.8, color=ACCENT_CORAL, stroke_width=1.5)
        arrow_lbl = vn_tex("Mất 21\\% hiệu năng!", color=ACCENT_CORAL, scale=0.32).next_to(arrow_insight, RIGHT, buff=0.1)

        self.play(
            Create(arrow_insight),
            FadeIn(arrow_lbl, shift=LEFT * 0.1),
            run_time=1.0
        )
        self.wait(4.6)

        # ============================================================
        # PHASE D: Take-away (55s - 70s)
        # ============================================================
        # Phụ đề sub_8 (60s)
        sub_8 = make_subtitle("Phase không chỉ chính xác hơn — nó cứu cả hệ thống nhận diện")
        
        # Dọn dẹp sạch Phase C
        self.play(
            FadeOut(phase_b_group),
            FadeOut(c_bars),
            FadeOut(arrow_insight),
            FadeOut(arrow_lbl),
            FadeOut(title),
            FadeOut(question),
            ReplacementTransform(self.current_sub, sub_8),
            run_time=0.8
        )
        self.current_sub = sub_8
        self.wait(0.2)

        # Dòng kết luận trung tâm lớn
        conclusion = vn_tex("Pha không chỉ giúp khớp điểm chính xác — nó cứu sống cả hệ thống nhận diện!", color=ACCENT_MINT, scale=0.45).move_to(UP * 1.5)
        self.play(FadeIn(conclusion, shift=DOWN * 0.15), run_time=1.0)

        # Hai hộp tổng kết
        box_l = RoundedRectangle(corner_radius=0.06, width=4.5, height=1.6, color=ACCENT_CORAL, stroke_width=0.8, fill_color=BG_NAVY_SOFT, fill_opacity=0.9).move_to(LEFT * 2.6 + DOWN * 0.6)
        box_l_txt1 = vn_tex("Sai số Matching", color=TEXT_MUTED, scale=0.32).move_to(box_l.get_center() + UP * 0.35)
        box_l_txt2 = vn_tex_bold("5.2 px vs 1.6 px", color=ACCENT_CORAL, scale=0.42).move_to(box_l.get_center())
        box_l_txt3 = vn_tex("Matching: 3.25$\\times$ chính xác hơn", color=ACCENT_MINT, scale=0.3).move_to(box_l.get_center() + DOWN * 0.38)
        group_box_l = VGroup(box_l, box_l_txt1, box_l_txt2, box_l_txt3)

        box_r = RoundedRectangle(corner_radius=0.06, width=4.5, height=1.6, color=ACCENT_MINT, stroke_width=0.8, fill_color=BG_NAVY_SOFT, fill_opacity=0.9).move_to(RIGHT * 2.6 + DOWN * 0.6)
        box_r_txt1 = vn_tex("Độ nhận diện (Rank-1)", color=TEXT_MUTED, scale=0.32).move_to(box_r.get_center() + UP * 0.35)
        box_r_txt2 = vn_tex_bold("88\\% vs 67\\%", color=ACCENT_MINT, scale=0.42).move_to(box_r.get_center())
        box_r_txt3 = vn_tex("Recognition: +21 điểm \\%", color=ACCENT_MINT, scale=0.3).move_to(box_r.get_center() + DOWN * 0.38)
        group_box_r = VGroup(box_r, box_r_txt1, box_r_txt2, box_r_txt3)

        self.play(
            FadeIn(group_box_l, shift=UP * 0.2),
            FadeIn(group_box_r, shift=UP * 0.2),
            run_time=1.5
        )
        self.wait(5.5)

        # Cleanup toàn màn hình kết thúc scene
        self.play(
            FadeOut(conclusion),
            FadeOut(group_box_l),
            FadeOut(group_box_r),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
