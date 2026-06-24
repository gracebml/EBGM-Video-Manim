"""
EBGM Video — Part 3: Experiments
Scene 25: Benchmarks — So sánh với các hệ thống khác
Thời lượng dự kiến: 90s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)

Render command:
  manim -pql scene_25_benchmarks.py Scene25_Benchmarks
  manim -pqh scene_25_benchmarks.py Scene25_Benchmarks  # high quality
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
# ADDITIONAL HELPERS (Sử dụng LaTeX thuần)
# ============================================================
def make_bar_chart(values, labels, max_val=100, bar_colors=None, scale=1.0):
    """Tạo grouped bar chart ngang tự định nghĩa."""
    bars = VGroup()
    for i, (val, lbl) in enumerate(zip(values, labels)):
        color = bar_colors[i] if bar_colors is not None else BAR_PRIMARY
        # Bar
        bar = Rectangle(
            width=val/max_val * 4.0,
            height=0.32,
            fill_color=color,
            fill_opacity=0.85,
            stroke_color=color,
            stroke_width=1
        )
        # Sắp xếp các thanh bar lệch dần xuống dưới
        bar.shift(DOWN * i * 0.52 + RIGHT * (val/max_val * 2.0))
        
        # Label trái bằng vn_tex
        lbl_text = vn_tex(lbl, color=TEXT_PRIMARY, scale=0.45)
        lbl_text.next_to(bar, LEFT, buff=0.3).align_to(bar, LEFT).shift(LEFT * 0.5)
        
        # Value phải
        val_text = vn_tex_mono(f"{val:.0f}\%", color=color, scale=0.45)
        val_text.next_to(bar, RIGHT, buff=0.2)
        
        bars.add(VGroup(bar, lbl_text, val_text))
    return bars.scale(scale)


def trophy_icon(color=TROPHY_GOLD, scale=0.6):
    """Icon trophy vẽ bằng VMobject."""
    cup = VGroup(
        ArcPolygon([-0.4,0.5,0], [0.4,0.5,0], [0.3,-0.3,0], [-0.3,-0.3,0],
                   color=color, fill_opacity=0.8, stroke_width=2),
        Arc(radius=0.2, start_angle=PI/2, angle=-PI, color=color, 
            stroke_width=3).shift(LEFT*0.4),
        Arc(radius=0.2, start_angle=PI/2, angle=PI, color=color,
            stroke_width=3).shift(RIGHT*0.4),
        Rectangle(width=0.5, height=0.1, color=color, fill_opacity=0.8
                  ).shift(DOWN*0.4),
        Rectangle(width=0.8, height=0.08, color=color, fill_opacity=0.8
                  ).shift(DOWN*0.5),
    )
    return cup.scale(scale)


# ============================================================
# MAIN SCENE
# ============================================================
class Scene25_Benchmarks(Scene):
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
        # PHASE A: Setup tiêu đề & 4 Cards đối thủ (0s - 10s)
        # ============================================================
        title = section_title("Blind Test — EBGM đối đầu với ai?", color=ACCENT_LAVENDER)
        title.to_edge(UP, buff=0.6)
        
        intro_lbl = vn_tex("Thử nghiệm độc lập FERET, bởi US Army Research Lab", color=ACCENT_LAVENDER, scale=0.4)
        intro_lbl.next_to(title, DOWN, buff=0.15)

        # Phụ đề 1
        sub_1 = make_subtitle("Blind test trên tập FERET — EBGM đối đầu với các đối thủ mạnh")
        self.current_sub = sub_1

        self.play(
            FadeIn(title, shift=DOWN * 0.25),
            FadeIn(intro_lbl, shift=UP * 0.15),
            FadeIn(sub_1, shift=UP * 0.15),
            run_time=1.5
        )
        self.wait(2.5)

        # Vẽ 4 card ngang tượng trưng cho 4 đối thủ
        card_x = [-4.5, -1.5, 1.5, 4.5]
        card_data = [
            ("PCA", PCA_COLOR, "Moghaddam \\& Pentland"),
            ("NN-RBF", NN_COLOR, "Gutta et al."),
            ("Correlation", PREV_COLOR, "Gordon"),
            ("Hệ EBGM", EBGM_BRAND, "Wiskott et al.")
        ]
        
        opponent_cards = VGroup()
        for idx, (name, col, author) in enumerate(card_data):
            # Card
            bg = RoundedRectangle(
                corner_radius=0.06, width=2.6, height=1.0, color=col, stroke_width=0.8,
                fill_color=BG_NAVY_SOFT, fill_opacity=0.85
            ).move_to(np.array([card_x[idx], 0.0, 0]))
            
            lbl_name = vn_tex_bold(name, color=col, scale=0.38).move_to(bg.get_center() + UP * 0.18)
            lbl_auth = vn_tex(author, color=TEXT_MUTED, scale=0.25).move_to(bg.get_center() + DOWN * 0.2)
            
            opponent_cards.add(VGroup(bg, lbl_name, lbl_auth))

        # Hiển thị 4 card lần lượt từ trái sang phải
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in opponent_cards], lag_ratio=0.2),
            run_time=1.6
        )
        self.wait(0.5)

        # Highlight đặc biệt cho EBGM
        self.play(
            Indicate(opponent_cards[3], color=EBGM_BRAND, scale_factor=1.1),
            Flash(opponent_cards[3].get_center(), color=EBGM_BRAND, flash_radius=0.5),
            run_time=1.0
        )
        self.wait(2.5)

        # Dọn dẹp Phase A
        self.play(FadeOut(opponent_cards), run_time=0.6)

        # ============================================================
        # PHASE B: Big Bar Chart Comparison (10s - 40s)
        # ============================================================
        # 1. Phụ đề sub_2 (10s)
        sub_2 = make_subtitle("Trên ảnh chính diện: EBGM đạt 98\% — thuộc nhóm dẫn đầu")
        self.play(ReplacementTransform(self.current_sub, sub_2), run_time=0.4)
        self.current_sub = sub_2

        # 2. Xây dựng Bar Chart
        values_b = [98, 99, 97, 83, 72]
        labels_b = [
            "Hệ EBGM (Wiskott et al.)",
            "PCA (Moghaddam \\& Pentland)",
            "Matching Pursuit (Phillips)",
            "RBF Neural Net (Gutta)",
            "Cross-correlation (Gordon)"
        ]
        colors_b = [EBGM_BRAND, PCA_COLOR, BAR_SECONDARY, NN_COLOR, PREV_COLOR]

        chart = make_bar_chart(values_b, labels_b, max_val=100, bar_colors=colors_b, scale=0.92)
        chart.shift(LEFT * 1.6 + DOWN * 0.45)

        chart_elements = []
        for group in chart:
            bar, lbl, val = group
            chart_elements.append((bar, lbl, val))

        # Hiện nhãn
        self.play(
            LaggedStart(*[FadeIn(lbl, shift=RIGHT * 0.2) for bar, lbl, val in chart_elements], lag_ratio=0.12),
            run_time=1.0
        )
        # Grow bar từ 0 và hiện số
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    GrowFromEdge(bar, LEFT),
                    FadeIn(val, shift=LEFT * 0.15)
                ) for bar, lbl, val in chart_elements
            ], lag_ratio=0.22),
            run_time=2.2
        )
        self.wait(1.0)

        # Spotlight cúp vàng cho EBGM (98%)
        bar_0, lbl_0, val_0 = chart_elements[0]
        trophy = trophy_icon(color=TROPHY_GOLD, scale=0.38).next_to(val_0, RIGHT, buff=0.25)
        self.play(
            Flash(val_0.get_center(), color=ACCENT_CYAN, flash_radius=0.5),
            Indicate(val_0, color=EBGM_BRAND, scale_factor=1.15),
            FadeIn(trophy, shift=LEFT * 0.15),
            run_time=1.0
        )
        self.wait(2.5)

        # Phụ đề sub_3 (18s)
        sub_3 = make_subtitle("PCA đạt 99\%, Matching Pursuit 97\% — các kết quả rất sát nhau")
        self.play(ReplacementTransform(self.current_sub, sub_3), run_time=0.4)
        self.current_sub = sub_3
        self.wait(7.6)

        # Phụ đề sub_4 (26s)
        sub_4 = make_subtitle("Neural Network RBF chỉ đạt 83\% — yếu hơn đáng kể")
        self.play(ReplacementTransform(self.current_sub, sub_4), run_time=0.4)
        self.current_sub = sub_4
        # Highlight RBF bar
        self.play(Indicate(VGroup(*chart_elements[3]), color=NN_COLOR, scale_factor=1.05), run_time=1.0)
        self.wait(4.6)

        # Phụ đề sub_5 (32s)
        sub_5 = make_subtitle("Cross-correlation cổ điển chỉ đạt 72\% — không còn đủ cạnh tranh")
        self.play(ReplacementTransform(self.current_sub, sub_5), run_time=0.4)
        self.current_sub = sub_5
        # Highlight correlation bar
        self.play(Indicate(VGroup(*chart_elements[4]), color=PREV_COLOR, scale_factor=1.05), run_time=1.0)
        self.wait(6.6)

        # ============================================================
        # PHASE C: Insight — EBGM không chỉ nhanh (40s - 60s)
        # ============================================================
        # 1. Thu nhỏ biểu đồ dịch sang bên trái làm context
        chart_group = VGroup(chart, trophy)
        self.play(
            chart_group.animate.scale(0.55).shift(LEFT * 3.2 + UP * 0.25),
            run_time=1.2
        )

        # 2. Xây dựng 2 cards điểm mạnh bên phải
        card_w, card_h = 2.8, 3.6
        # Card 1: Không cần alignment cẩn thận
        box1 = RoundedRectangle(corner_radius=0.06, width=card_w, height=card_h, color=ACCENT_CYAN, stroke_width=0.8, fill_color=BG_NAVY_SOFT, fill_opacity=0.85).move_to(np.array([1.4, -0.4, 0]))
        lbl1 = vn_tex_bold("Không cần Alignment", color=ACCENT_CYAN, scale=0.32).move_to(box1.get_top() + DOWN * 0.4)
        
        mắt1 = Circle(radius=0.1, color=TEXT_MUTED, stroke_width=1.0).move_to(box1.get_center() + LEFT * 0.4 + UP * 0.3)
        mắt2 = Circle(radius=0.1, color=TEXT_MUTED, stroke_width=1.0).move_to(box1.get_center() + RIGHT * 0.4 + UP * 0.5) # lệch trục
        arrows_align = VGroup(
            Arrow(mắt1.get_center(), mắt1.get_center() + DOWN * 0.1, color=ACCENT_CYAN, buff=0, stroke_width=1.5),
            Arrow(mắt2.get_center(), mắt2.get_center() + DOWN * 0.3, color=ACCENT_CYAN, buff=0, stroke_width=1.5)
        )
        txt1 = vn_tex("PCA cần căn chỉnh mắt thẳng trục. EBGM tự co giãn khớp điểm.", color=TEXT_PRIMARY, scale=0.25).move_to(box1.get_center() + DOWN * 0.9)
        group_card1 = VGroup(box1, lbl1, mắt1, mắt2, arrows_align, txt1)

        # Card 2: Học ngoại lệ dễ dàng
        box2 = RoundedRectangle(corner_radius=0.06, width=card_w, height=card_h, color=ACCENT_LAVENDER, stroke_width=0.8, fill_color=BG_NAVY_SOFT, fill_opacity=0.85).move_to(np.array([4.6, -0.4, 0]))
        lbl2 = vn_tex_bold("Học ngoại lệ dễ dàng", color=ACCENT_LAVENDER, scale=0.32).move_to(box2.get_top() + DOWN * 0.4)
        
        bunch_node = Circle(radius=0.25, color=ACCENT_LAVENDER, stroke_width=1.5).move_to(box2.get_center() + UP * 0.3)
        plus_sign = vn_tex("+", color=ACCENT_LAVENDER, scale=0.8).move_to(bunch_node.get_center())
        txt2 = vn_tex("Không cần huấn luyện lại toàn bộ. Chỉ việc thêm ảnh ngoại lệ vào Bunch.", color=TEXT_PRIMARY, scale=0.25).move_to(box2.get_center() + DOWN * 0.9)
        group_card2 = VGroup(box2, lbl2, bunch_node, plus_sign, txt2)

        # Hiện Card 1 (42s)
        sub_6 = make_subtitle("Không cần căn chỉnh ảnh quá cẩn thận như PCA")
        self.play(
            ReplacementTransform(self.current_sub, sub_6),
            FadeIn(group_card1, shift=UP * 0.25),
            run_time=1.0
        )
        self.current_sub = sub_6
        self.wait(5.0)

        # Hiện Card 2 (46s)
        sub_7 = make_subtitle("Học ngoại lệ chỉ cần thêm ảnh vào Bunch — không cần huấn luyện lại")
        self.play(
            ReplacementTransform(self.current_sub, sub_7),
            FadeIn(group_card2, shift=UP * 0.25),
            run_time=1.0
        )
        self.current_sub = sub_7
        self.wait(7.0)

        # Dọn dẹp Phase C
        self.play(
            FadeOut(chart_group),
            FadeOut(group_card1),
            FadeOut(group_card2),
            run_time=0.8
        )
        self.wait(0.2)

        # ============================================================
        # PHASE D: Comparison table chi tiết (60s - 85s)
        # ============================================================
        # Phụ đề sub_8 (52s)
        sub_8 = make_subtitle("Robust với rotation in depth — PCA suy giảm rất mạnh khi lệch góc")
        self.play(ReplacementTransform(self.current_sub, sub_8), run_time=0.4)
        self.current_sub = sub_8

        # Xây dựng bảng so sánh chi tiết
        col_x = [-3.0, -0.8, 1.2, 3.2]
        row_y = [1.6, 1.1, 0.6, 0.1, -0.4, -0.9, -1.4]

        # Tiêu đề cột
        h_tc = vn_tex_bold("Tiêu chí", color=TEXT_PRIMARY, scale=0.34).move_to(np.array([col_x[0], row_y[0], 0]))
        h_pca = vn_tex_bold("Hệ PCA", color=PCA_COLOR, scale=0.34).move_to(np.array([col_x[1], row_y[0], 0]))
        h_nn = vn_tex_bold("NN-RBF", color=NN_COLOR, scale=0.34).move_to(np.array([col_x[2], row_y[0], 0]))
        h_ebgm = vn_tex_bold("Hệ EBGM", color=EBGM_BRAND, scale=0.34).move_to(np.array([col_x[3], row_y[0], 0]))
        headers = VGroup(h_tc, h_pca, h_nn, h_ebgm)

        # Nền mờ cho cột EBGM
        col_ebgm_bg = RoundedRectangle(
            corner_radius=0.06, width=1.8, height=3.6, color=EBGM_BRAND, stroke_width=0.8,
            fill_color=EBGM_BRAND, fill_opacity=0.08
        ).move_to(np.array([col_x[3], 0.1, 0]))

        # Các hàng dữ liệu
        r1_c1 = vn_tex("Chính diện fa/fb", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([col_x[0], row_y[1], 0]), aligned_edge=LEFT)
        r1_c2 = vn_tex_mono("99\%", color=PCA_COLOR, scale=0.34).move_to(np.array([col_x[1], row_y[1], 0]))
        r1_c3 = vn_tex_mono("83\%", color=NN_COLOR, scale=0.34).move_to(np.array([col_x[2], row_y[1], 0]))
        r1_c4 = vn_tex_mono("98\%", color=EBGM_BRAND, scale=0.34).move_to(np.array([col_x[3], row_y[1], 0]))
        row1 = VGroup(r1_c1, r1_c2, r1_c3, r1_c4)

        r2_c1 = vn_tex("Half-profile", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([col_x[0], row_y[2], 0]), aligned_edge=LEFT)
        r2_c2 = vn_tex_mono("38\%", color=TEXT_MUTED, scale=0.34).move_to(np.array([col_x[1], row_y[2], 0]))
        r2_c3 = vn_tex("—", color=TEXT_MUTED, scale=0.34).move_to(np.array([col_x[2], row_y[2], 0]))
        r2_c4 = vn_tex_bold("57\%", color=ACCENT_MINT, scale=0.36).move_to(np.array([col_x[3], row_y[2], 0]))
        row2 = VGroup(r2_c1, r2_c2, r2_c3, r2_c4)

        r3_c1 = vn_tex("Profile", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([col_x[0], row_y[3], 0]), aligned_edge=LEFT)
        r3_c2 = vn_tex_mono("32\%", color=TEXT_MUTED, scale=0.34).move_to(np.array([col_x[1], row_y[3], 0]))
        r3_c3 = vn_tex("—", color=TEXT_MUTED, scale=0.34).move_to(np.array([col_x[2], row_y[3], 0]))
        r3_c4 = vn_tex_bold("84\%", color=ACCENT_MINT, scale=0.36).move_to(np.array([col_x[3], row_y[3], 0]))
        row3 = VGroup(r3_c1, r3_c2, r3_c3, r3_c4)

        r4_c1 = vn_tex("Cần Alignment?", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([col_x[0], row_y[4], 0]), aligned_edge=LEFT)
        r4_c2 = vn_tex("Có (YES)", color=ACCENT_CORAL, scale=0.32).move_to(np.array([col_x[1], row_y[4], 0]))
        r4_c3 = vn_tex("Không (NO)", color=TEXT_MUTED, scale=0.32).move_to(np.array([col_x[2], row_y[4], 0]))
        r4_c4 = vn_tex_bold("Không (NO)", color=ACCENT_MINT, scale=0.34).move_to(np.array([col_x[3], row_y[4], 0]))
        row4 = VGroup(r4_c1, r4_c2, r4_c3, r4_c4)

        r5_c1 = vn_tex("Học ngoại lệ?", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([col_x[0], row_y[5], 0]), aligned_edge=LEFT)
        r5_c2 = vn_tex("Không (NO)", color=TEXT_MUTED, scale=0.32).move_to(np.array([col_x[1], row_y[5], 0]))
        r5_c3 = vn_tex("Retrain", color=TEXT_MUTED, scale=0.32).move_to(np.array([col_x[2], row_y[5], 0]))
        r5_c4 = vn_tex_bold("Thêm (ADD)", color=ACCENT_MINT, scale=0.34).move_to(np.array([col_x[3], row_y[5], 0]))
        row5 = VGroup(r5_c1, r5_c2, r5_c3, r5_c4)

        r6_c1 = vn_tex("Tốc độ", color=TEXT_PRIMARY, scale=0.32).move_to(np.array([col_x[0], row_y[6], 0]), aligned_edge=LEFT)
        r6_c2 = vn_tex("Nhanh", color=TEXT_MUTED, scale=0.32).move_to(np.array([col_x[1], row_y[6], 0]))
        r6_c3 = vn_tex("Trung bình", color=TEXT_MUTED, scale=0.32).move_to(np.array([col_x[2], row_y[6], 0]))
        r6_c4 = vn_tex_bold("Nhanh", color=EBGM_BRAND, scale=0.34).move_to(np.array([col_x[3], row_y[6], 0]))
        row6 = VGroup(r6_c1, r6_c2, r6_c3, r6_c4)

        # Các đường kẻ phân tách ngang mỏng
        divider_y = [1.35, 0.85, 0.35, -0.15, -0.65, -1.15]
        dividers = VGroup()
        for y_val in divider_y:
            div = Line(np.array([-4.5, y_val, 0]), np.array([4.5, y_val, 0]), color=TEXT_MUTED, stroke_width=0.5).set_opacity(0.3)
            dividers.add(div)

        # Hiện nền cột EBGM mờ, headers, dividers trước
        self.play(
            FadeIn(col_ebgm_bg),
            FadeIn(headers),
            FadeIn(dividers),
            run_time=1.2
        )

        # Hiện từng hàng dữ liệu tuần tự (lag 0.3)
        self.play(
            LaggedStart(
                FadeIn(row1), FadeIn(row2), FadeIn(row3),
                FadeIn(row4), FadeIn(row5), FadeIn(row6),
                lag_ratio=0.3
            ),
            run_time=2.2
        )
        self.wait(1.5)

        # Highlight 2 hàng góc nghiêng EBGM thắng áp đảo (Half-profile & Profile)
        self.play(
            Indicate(r2_c4, color=ACCENT_MINT, scale_factor=1.15),
            Indicate(r3_c4, color=ACCENT_MINT, scale_factor=1.15),
            Flash(r2_c4.get_center(), color=ACCENT_MINT, flash_radius=0.4),
            Flash(r3_c4.get_center(), color=ACCENT_MINT, flash_radius=0.4),
            run_time=1.2
        )
        self.wait(8.0)

        # Dọn dẹp Bảng
        self.play(
            FadeOut(col_ebgm_bg), FadeOut(headers), FadeOut(dividers),
            FadeOut(row1), FadeOut(row2), FadeOut(row3),
            FadeOut(row4), FadeOut(row5), FadeOut(row6),
            run_time=0.8
        )
        self.wait(0.2)

        # ============================================================
        # PHASE E: Conclusion (85s - 90s)
        # ============================================================
        # Phụ đề sub_9 (80s)
        sub_9 = make_subtitle("EBGM không vô địch mọi mặt — nhưng linh hoạt và thực tế nhất")
        self.play(ReplacementTransform(self.current_sub, sub_9), run_time=0.4)
        self.current_sub = sub_9

        conclusion = vn_tex("EBGM không phải số 1 mọi mặt — nhưng linh hoạt, robust, và thực tế nhất", color=ACCENT_LAVENDER, scale=0.45).move_to(ORIGIN)
        
        arrow = Arrow(LEFT * 0.5 + DOWN * 0.8, RIGHT * 0.5 + DOWN * 0.8, color=EBGM_BRAND, stroke_width=2.5)

        self.play(
            FadeIn(conclusion, shift=UP * 0.15),
            Create(arrow),
            run_time=1.2
        )
        # Flash mũi tên hướng về tương lai
        self.play(Flash(arrow.get_end(), color=EBGM_BRAND, flash_radius=0.4), run_time=0.8)
        self.wait(2.2)

        # Cleanup toàn màn hình kết thúc scene
        self.play(
            FadeOut(conclusion),
            FadeOut(arrow),
            FadeOut(title),
            FadeOut(intro_lbl),
            FadeOut(self.current_sub),
            run_time=0.8
        )
        self.wait(0.3)
