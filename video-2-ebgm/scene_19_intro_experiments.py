"""
EBGM Video — Part 3: Experiments
Scene 19: Intro "EBGM tốt đến đâu?"
Thời lượng dự kiến: 20s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)

Render command:
  manim -pql scene_19_intro_experiments.py Scene19_IntroExperiments
  manim -pqh scene_19_intro_experiments.py Scene19_IntroExperiments  # high quality
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# PART 3 COLOR PALETTE
# ============================================================
BAR_PRIMARY   = "#48CAE4"   # cyan
BAR_SECONDARY = "#778DA9"   # blue-grey
BAR_SUCCESS   = "#95D5B2"   # mint
BAR_WARNING   = "#E29578"   # coral
TROPHY_GOLD   = "#FCBF49"   # vàng ấm

EBGM_BRAND    = "#B8B5FF"   # Signature lavender cho EBGM
PCA_COLOR     = "#76C5BF"   # teal cho PCA
NN_COLOR      = "#E29578"   # coral cho Neural Network
PREV_COLOR    = "#778DA9"   # blue-grey cho preceding system

# ============================================================
# PART 3 ADDITIONAL HELPERS (Sử dụng LaTeX thuần)
# ============================================================
def make_bar_chart(values, labels, max_val=100, bar_color=BAR_PRIMARY,
                   highlight_idx=None, scale=1.0):
    """
    Tạo bar chart ngang bằng LaTeX thuần.
    """
    bars = VGroup()
    for i, (val, lbl) in enumerate(zip(values, labels)):
        color = EBGM_BRAND if i == highlight_idx else bar_color
        # Bar
        bar = Rectangle(
            width=val/max_val * 4.0,
            height=0.35,
            fill_color=color,
            fill_opacity=0.85,
            stroke_color=color,
            stroke_width=1
        )
        bar.shift(DOWN * i * 0.55 + RIGHT * (val/max_val * 2.0))
        
        # Label trái bằng vn_tex
        lbl_text = vn_tex(lbl, color=TEXT_PRIMARY, scale=0.45)
        lbl_text.next_to(bar, LEFT, buff=0.3).align_to(bar, LEFT).shift(LEFT * 0.5)
        
        # Value phải bằng vn_tex_mono (escape % trong LaTeX thành \%)
        val_text = vn_tex_mono(f"{val:.0f}\%", color=color, scale=0.45)
        val_text.next_to(bar, RIGHT, buff=0.2)
        
        bars.add(VGroup(bar, lbl_text, val_text))
    return bars.scale(scale)


def make_percentage_circle(value, color=BAR_PRIMARY, radius=1.0):
    """
    Donut chart: 1 con số phần trăm ở giữa (LaTeX thuần), vòng tròn lấp đầy theo %.
    """
    bg_ring = Circle(radius=radius, color=GRID_LINE, stroke_width=8).set_opacity(0.3)
    progress_ring = Arc(
        radius=radius,
        start_angle=PI/2,
        angle=-2*PI * (value/100),
        stroke_width=10,
        color=color
    )
    # Escape % thành \% cho LaTeX
    text = vn_tex_bold(f"{value:.0f}\%", color=color, scale=1.1 * radius)
    text.move_to(bg_ring.get_center())
    return VGroup(bg_ring, progress_ring, text)


def trophy_icon(color=TROPHY_GOLD, scale=0.6):
    """Icon trophy vẽ bằng VMobject (không dùng emoji)."""
    cup = VGroup(
        # Cup body
        ArcPolygon([-0.4,0.5,0], [0.4,0.5,0], [0.3,-0.3,0], [-0.3,-0.3,0],
                   color=color, fill_opacity=0.8, stroke_width=2),
        # Handles
        Arc(radius=0.2, start_angle=PI/2, angle=-PI, color=color, 
            stroke_width=3).shift(LEFT*0.4),
        Arc(radius=0.2, start_angle=PI/2, angle=PI, color=color,
            stroke_width=3).shift(RIGHT*0.4),
        # Base
        Rectangle(width=0.5, height=0.1, color=color, fill_opacity=0.8
                  ).shift(DOWN*0.4),
        Rectangle(width=0.8, height=0.08, color=color, fill_opacity=0.8
                  ).shift(DOWN*0.5),
    )
    return cup.scale(scale)


# ============================================================
# SCENE-SPECIFIC HELPERS FOR SCENE 19
# ============================================================
def make_face_silhouette_thumbnail(pos, scale=0.65):
    """Tạo thumbnail khuôn mặt mờ ảo làm background."""
    bg = RoundedRectangle(
        corner_radius=0.04, width=0.9, height=1.2, color=GRID_LINE, stroke_width=0.6,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.15
    ).set_opacity(0.2).move_to(pos)
    
    # Head outline
    head = Circle(radius=0.18, color=GRID_LINE, stroke_width=0.8).set_opacity(0.2).move_to(pos + UP * 0.15)
    # Shoulders
    shoulders = Arc(radius=0.25, start_angle=0, angle=PI, color=GRID_LINE, stroke_width=0.8).set_opacity(0.2).move_to(pos + DOWN * 0.25)
    
    return VGroup(bg, head, shoulders).scale(scale)


def make_circled_num(num_str, color=ACCENT_LAVENDER, scale=0.45):
    """Vẽ vòng tròn số an toàn cho XeLaTeX."""
    circle = Circle(radius=0.18, color=color, stroke_width=1.0)
    num_text = vn_tex_bold(num_str, color=color, scale=scale)
    num_text.move_to(circle.get_center())
    return VGroup(circle, num_text)


def make_card(num_str, title_str, sub_str, pos):
    """Tạo card tiêu chí cho Phase B."""
    card_bg = RoundedRectangle(
        corner_radius=0.08, width=3.3, height=1.7, color=ACCENT_BLUE, stroke_width=1.0,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.85
    ).move_to(pos)
    
    # Số tròn ở góc trên bên trái
    circled_num = make_circled_num(num_str).move_to(pos + LEFT * 1.25 + UP * 0.55)
    
    # Tiêu đề card
    title = vn_tex_bold(title_str, color=ACCENT_LAVENDER, scale=0.45).move_to(pos + UP * 0.1)
    
    # Subtext nhỏ phía dưới
    sub = vn_tex(sub_str, color=TEXT_PRIMARY, scale=0.35).move_to(pos + DOWN * 0.35)
    
    return VGroup(card_bg, circled_num, title, sub)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene19_IntroExperiments(Scene):
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
        # PHASE A: Câu hỏi lớn & Background Gallery (0s - 8s)
        # ============================================================
        # 1. Tạo lưới 5x5 các khuôn mặt mờ ảo làm nền
        bg_gallery = VGroup()
        for row in range(-2, 3):
            for col in range(-2, 3):
                pos = np.array([col * 2.4, row * 1.4, 0])
                # Không vẽ đè lên vùng trung tâm của câu hỏi
                if abs(row) <= 1 and abs(col) <= 1:
                    thumbnail = make_face_silhouette_thumbnail(pos, scale=0.65).set_opacity(0.12)
                else:
                    thumbnail = make_face_silhouette_thumbnail(pos, scale=0.65).set_opacity(0.25)
                bg_gallery.add(thumbnail)

        # 2. Câu hỏi lớn ở giữa
        question = vn_tex("Lý thuyết đã rõ — nhưng EBGM thực sự hiệu quả đến đâu?", scale=0.65)
        question.move_to(ORIGIN)

        # 3. Phụ đề Phase A
        sub_1_text = "Lý thuyết đã rõ — nhưng EBGM thực sự hiệu quả đến đâu?"
        sub_1 = make_subtitle(sub_1_text)
        self.current_sub = sub_1

        # Chạy song song: Gallery trôi nhẹ, Câu hỏi xuất hiện, Phụ đề xuất hiện
        self.play(
            FadeIn(bg_gallery, run_time=1.5),
            FadeIn(question, shift=UP * 0.25, run_time=1.8),
            FadeIn(sub_1, shift=UP * 0.15, run_time=1.2),
            bg_gallery.animate(run_time=8.0, rate_func=linear).shift(UP * 0.4 + LEFT * 0.2)
        )
        self.wait(0.2)

        # ============================================================
        # PHASE B: 4 Cards tiêu chí (8s - 20s)
        # ============================================================
        # 1. Chuyển phụ đề sang Phase B
        sub_2_text = "Bốn khía cạnh sẽ được kiểm chứng"
        sub_2 = make_subtitle(sub_2_text)

        # 2. Thu nhỏ câu hỏi thành tiêu đề góc trên
        header = section_title("Kiểm chứng hiệu năng của EBGM").to_edge(UP, buff=0.6)

        self.play(
            ReplacementTransform(question, header),
            ReplacementTransform(self.current_sub, sub_2),
            FadeOut(bg_gallery, run_time=1.2),
            run_time=1.2
        )
        self.current_sub = sub_2

        # 3. Tạo 4 cards xếp 2x2
        card_positions = [
            np.array([-1.9, 0.7, 0]),  # Top Left
            np.array([1.9, 0.7, 0]),   # Top Right
            np.array([-1.9, -0.8, 0]), # Bottom Left
            np.array([1.9, -0.8, 0])   # Bottom Right
        ]
        
        cards_data = [
            ("1", "ACCURACY", "Trên DB lớn?"),
            ("2", "PRECISION", "Bao chính xác?"),
            ("3", "SPEED", "Đủ nhanh thực tế?"),
            ("4", "BENCHMARKS", "Hơn các hệ khác?")
        ]

        cards = VGroup()
        for idx, (num, title, desc) in enumerate(cards_data):
            card = make_card(num, title, desc, card_positions[idx])
            cards.add(card)

        # Hiện từng card tuần tự bằng LaggedStart
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.35) for card in cards], lag_ratio=0.35),
            run_time=2.2
        )
        self.wait(0.6)

        # 4. Phụ đề Phase C & Câu kết luận xuất hiện với Flash
        sub_3_text = "Độ chính xác, độ định vị, tốc độ và so sánh với các hệ thống khác"
        sub_3 = make_subtitle(sub_3_text)

        conclusion_text = vn_tex_italic("Bốn câu hỏi — bốn câu trả lời.", color=ACCENT_CYAN, scale=0.5)
        conclusion_text.move_to(DOWN * 2.1)

        self.play(
            ReplacementTransform(self.current_sub, sub_3),
            Flash(ORIGIN, color=ACCENT_CYAN, flash_radius=1.5),
            FadeIn(conclusion_text, shift=UP * 0.15),
            run_time=1.2
        )
        self.current_sub = sub_3
        self.wait(4.8)

        # ============================================================
        # CLEANUP
        # ============================================================
        self.play(
            FadeOut(header),
            FadeOut(cards),
            FadeOut(conclusion_text),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
