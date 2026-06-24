"""
EBGM Video — Part 3: Experiments
Scene 26: Tổng kết phần 3 & Teaser Discussion
Thời lượng dự kiến: 25s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)

Render command:
  manim -pql scene_26_summary.py Scene26_Summary
  manim -pqh scene_26_summary.py Scene26_Summary  # high quality
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
# CIRCLED NUMBER HELPER (Tránh dùng unicode ②③ để dvisvgm không crash)
# ============================================================
def make_circled_num(num_str, color=ACCENT_CYAN, scale=0.35):
    """Tự vẽ vòng tròn lồng chữ số ở giữa."""
    bg = Circle(radius=0.18, color=color, stroke_width=1.2)
    txt = vn_tex_bold(num_str, color=color, scale=scale)
    txt.move_to(bg.get_center())
    return VGroup(bg, txt)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene26_Summary(Scene):
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
        # PHASE A: Recap 4 câu hỏi với 4 câu trả lời (0s - 15s)
        # ============================================================
        # Phụ đề sub_1 (0s - 8s)
        sub_1 = make_subtitle("EBGM đã chứng minh cả bốn khía cạnh của cuộc thử nghiệm")
        self.current_sub = sub_1
        self.play(FadeIn(sub_1, shift=UP * 0.15), run_time=0.4)

        # Trình bày tiêu đề chính
        title = section_title("Tổng kết hiệu năng EBGM", color=ACCENT_CYAN)
        title.to_edge(UP, buff=0.55)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # Xây dựng 4 thẻ 2x2
        card_w, card_h = 5.2, 1.8
        card_coords = [
            [-2.8, 1.0, 0],   # Top-left (Card 1)
            [2.8, 1.0, 0],    # Top-right (Card 2)
            [-2.8, -1.1, 0],  # Bottom-left (Card 3)
            [2.8, -1.1, 0]    # Bottom-right (Card 4)
        ]
        
        cards_data = [
            ("1", "ACCURACY (Độ chính xác)", "98\\% (Frontal) / 84\\% (Profile)", EBGM_BRAND),
            ("2", "MATCHING (Định vị mốc)", "Sai số cực nhỏ: 1.6 px", ACCENT_MINT),
            ("3", "SPEED (Tốc độ so khớp)", "< 1s / ~300 models", ACCENT_CYAN),
            ("4", "BENCHMARKS (Đối thủ)", "Top-tier (Vượt trội cross-pose)", ACCENT_LAVENDER)
        ]

        cards_group = VGroup()
        for idx, (num, label, value, col) in enumerate(cards_data):
            pos = card_coords[idx]
            # Vỏ card bo tròn nhẹ
            bg = RoundedRectangle(
                corner_radius=0.06, width=card_w, height=card_h, color=col, stroke_width=0.8,
                fill_color=BG_NAVY_SOFT, fill_opacity=0.85
            ).move_to(pos)
            
            # Nhãn số tròn tự vẽ
            num_circle = make_circled_num(num, color=col, scale=0.35).move_to(bg.get_top() + DOWN * 0.28 + LEFT * (card_w/2 - 0.4))
            
            # Nhãn tiêu chí
            lbl_text = vn_tex_bold(label, color=TEXT_PRIMARY, scale=0.3).next_to(num_circle, RIGHT, buff=0.15).align_to(num_circle, UP).shift(DOWN * 0.04)
            
            # Con số kết quả nổi bật ở giữa card
            val_text = vn_tex_mono(value, color=col, scale=0.38).move_to(bg.get_center() + DOWN * 0.22)
            
            cards_group.add(VGroup(bg, num_circle, lbl_text, val_text))

        # Hiện 4 thẻ đồng loạt
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in cards_group], lag_ratio=0.15),
            run_time=1.8
        )
        self.wait(1.5) # Đợi sub_1 hoàn thành nốt 8s

        # Phụ đề sub_2 (8s - 16s)
        sub_2 = make_subtitle("Độ chính xác cao, định vị tinh, tốc độ nhanh, benchmark top")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # Lần lượt nhấp nháy (Flash) và scale up nhẹ từng card khi vinh danh số liệu
        for idx in range(4):
            self.play(
                Indicate(cards_group[idx][3], color=cards_group[idx][0].get_color(), scale_factor=1.12),
                Flash(cards_group[idx][3].get_center(), color=cards_group[idx][0].get_color(), flash_radius=0.4),
                run_time=0.9
            )
            self.wait(0.3)
        self.wait(2.0) # Đợi nốt 16s

        # Dọn dẹp Phase A
        self.play(
            FadeOut(cards_group),
            FadeOut(title),
            run_time=0.8
        )

        # ============================================================
        # PHASE B: Teaser cho phần Discussion (16s - 25s)
        # ============================================================
        # Phụ đề sub_3 (16s - 25s)
        sub_3 = make_subtitle("Tiếp theo: so sánh sâu hơn và hướng phát triển tương lai")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3

        # Tiêu đề teaser
        teaser_title = section_title("TIẾP THEO TRONG LOẠT VIDEO", color=ACCENT_CYAN).move_to(UP * 1.5)
        
        # Câu dẫn chính
        teaser_text = vn_tex("EBGM so với các hệ thống khác — và hướng phát triển tương lai", color=TEXT_PRIMARY, scale=0.45).move_to(UP * 0.7)

        # 3 Keywords xếp ngang bên dưới
        kw_y = -0.5
        kw_x = [-4.0, 0.0, 4.0]
        keywords_data = [
            ("vs PCA / Eigenfaces", PCA_COLOR),
            ("vs Neural Networks", NN_COLOR),
            ("Future Improvements", EBGM_BRAND)
        ]

        keywords = VGroup()
        for idx, (text, col) in enumerate(keywords_data):
            # Box nhỏ cho keyword
            box = RoundedRectangle(
                corner_radius=0.04, width=3.4, height=0.9, color=col, stroke_width=0.6,
                fill_color=BG_NAVY_SOFT, fill_opacity=0.9
            ).move_to(np.array([kw_x[idx], kw_y, 0]))
            
            txt = vn_tex_bold(text, color=col, scale=0.34).move_to(box.get_center())
            keywords.add(VGroup(box, txt))

        # Mũi tên chỉ tương lai ở dưới cùng
        arrow = DoubleArrow(LEFT * 1.2 + DOWN * 1.8, RIGHT * 1.2 + DOWN * 1.8, color=ACCENT_CYAN, stroke_width=2.5)

        self.play(
            FadeIn(teaser_title, shift=DOWN * 0.15),
            FadeIn(teaser_text, shift=DOWN * 0.15),
            run_time=1.2
        )
        self.play(
            LaggedStart(*[FadeIn(kw, shift=UP * 0.25) for kw in keywords], lag_ratio=0.25),
            Create(arrow),
            run_time=1.8
        )
        
        # Flash cúp/mũi tên hướng đi
        self.play(Flash(arrow.get_end(), color=ACCENT_CYAN, flash_radius=0.45), run_time=0.8)
        self.wait(3.8) # Đợi nốt 25s

        # Cleanup toàn màn hình kết thúc video
        self.play(
            FadeOut(teaser_title),
            FadeOut(teaser_text),
            FadeOut(keywords),
            FadeOut(arrow),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
