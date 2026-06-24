"""
EBGM Video — Algorithm Detail Section
Scene 8: Intro "How does EBGM work?"
Thời lượng dự kiến: 20s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts
  - XeLaTeX (thường có sẵn trong TeX Live)

Render command:
  manim -pql scene_08_intro.py Scene8_Intro
  manim -pqh scene_08_intro.py Scene8_Intro  # high quality
"""

from manim import *
import numpy as np
from _common import *


class Scene8_Intro(Scene):
    def construct(self):
        self.camera.background_color = BG_NAVY

        # --- Subtitle tracker (reuse pattern from Phase 1) ---
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
        # PHASE A: Câu hỏi lớn & motivation (0s – 8s)
        # ============================================================

        # Câu hỏi chính — LaTeX Latin Modern Roman, nhất quán với phụ đề
        question_text = vn_tex(
            "Vậy EBGM thực sự hoạt động như thế nào?",
            color=TEXT_PRIMARY, scale=0.85
        )

        # Dòng phụ italic dưới câu hỏi
        sub_question = vn_tex_italic(
            "Đi từ pixel thô đến danh tính",
            color=ACCENT_CYAN, scale=0.6
        )
        sub_question.next_to(question_text, DOWN, buff=0.45)

        question_grp = VGroup(question_text, sub_question).move_to(ORIGIN)

        # Subtitle 1 (0s – 6s)
        self.play(Write(question_text), run_time=2.0)
        self.play(FadeIn(sub_question, shift=UP * 0.25), run_time=1.2)
        update_sub("Vậy EBGM thực sự hoạt động như thế nào?", 6.0)

        # Subtitle 2 (6s – 8s)
        update_sub("Bốn bước, đi từ pixel thô đến danh tính người", 2.0)

        # ============================================================
        # PHASE B: Thu nhỏ câu hỏi → header + Pipeline 4 card (8s – 20s)
        # ============================================================

        # Header phía trên
        header_text = vn_tex_bold(
            "Quy trình hoạt động của EBGM",
            color=ACCENT_CYAN, scale=0.7
        )
        header_text.to_edge(UP, buff=0.65)

        header_line = Line(
            start=header_text.get_corner(DL) + DOWN * 0.1,
            end=header_text.get_corner(DR) + DOWN * 0.1,
            color=ACCENT_BLUE, stroke_width=1.5
        )

        self.play(
            ReplacementTransform(question_grp, header_text),
            Create(header_line),
            run_time=1.4
        )
        self.wait(0.2)

        # --- Xây dựng 4 card ---
        card_info = [
            ("1. Gabor Wavelets",   "Tiền xử lý",  "\\S 2.1", ACCENT_CYAN),
            ("2. Face Repres.",      "Biểu diễn",   "\\S 2.2", ACCENT_LAVENDER),
            ("3. Elastic Matching",  "So khớp",      "\\S 2.3", ACCENT_TEAL),
            ("4. Recognition",      "Nhận diện",    "\\S 2.4", ACCENT_MINT),
        ]

        CARD_W, CARD_H = 2.8, 1.9

        cards = []
        for title_str, sub_str, sec_str, accent in card_info:
            # Nền card
            rect = RoundedRectangle(
                corner_radius=0.12,
                width=CARD_W, height=CARD_H,
                color=TEXT_MUTED, stroke_width=1.4,
                fill_color=BG_NAVY_SOFT, fill_opacity=0.88
            )

            # Section badge góc trên phải
            sec_lbl = vn_tex_mono(sec_str, color=accent, scale=0.4)
            sec_lbl.move_to(rect.get_corner(UR) + DL * 0.28)

            # Tiêu đề card — bold LaTeX
            card_title = vn_tex_bold(title_str, color=TEXT_PRIMARY, scale=0.52)
            card_title.move_to(rect.get_center() + UP * 0.15)

            # Label tiếng Việt — italic LaTeX
            card_sub = vn_tex_italic(sub_str, color=TEXT_MUTED, scale=0.45)
            card_sub.move_to(rect.get_center() + DOWN * 0.55)

            card = VGroup(rect, sec_lbl, card_title, card_sub)
            cards.append(card)

        # ⭐ Arrange TRƯỚC, rồi mới tạo glow — sửa bug overlap
        cards_grp = VGroup(*cards).arrange(RIGHT, buff=0.4)
        cards_grp.move_to(DOWN * 0.25)

        # Tạo glow SAU khi card đã ở đúng vị trí
        glows = []
        for i, card in enumerate(cards):
            accent = card_info[i][3]
            glow = card[0].copy().set_stroke(accent, width=6, opacity=0.35)
            glow.set_fill(opacity=0)
            glows.append(glow)

        # Mũi tên kết nối giữa các card
        arrows = []
        for i in range(3):
            arr = Arrow(
                start=cards[i].get_right(),
                end=cards[i + 1].get_left(),
                color=ACCENT_BLUE,
                stroke_width=2.5,
                buff=0.1,
                max_tip_length_to_length_ratio=0.25
            )
            arrows.append(arr)

        # --- Animation tuần tự: card pop in + glow chạy theo ---
        accents = [c[3] for c in card_info]

        # Card 1
        self.play(FadeIn(cards[0], shift=UP * 0.3), run_time=0.6)
        self.play(
            Flash(cards[0].get_center(), color=accents[0], flash_radius=0.9),
            FadeIn(glows[0]),
            run_time=0.4
        )

        # Card 2
        self.play(Create(arrows[0]), FadeIn(cards[1], shift=UP * 0.3), run_time=0.6)
        self.play(
            Flash(cards[1].get_center(), color=accents[1], flash_radius=0.9),
            FadeOut(glows[0]), FadeIn(glows[1]),
            run_time=0.4
        )

        # Card 3
        self.play(Create(arrows[1]), FadeIn(cards[2], shift=UP * 0.3), run_time=0.6)
        self.play(
            Flash(cards[2].get_center(), color=accents[2], flash_radius=0.9),
            FadeOut(glows[1]), FadeIn(glows[2]),
            run_time=0.4
        )

        # Card 4
        self.play(Create(arrows[2]), FadeIn(cards[3], shift=UP * 0.3), run_time=0.6)
        self.play(
            Flash(cards[3].get_center(), color=accents[3], flash_radius=0.9),
            FadeOut(glows[2]), FadeIn(glows[3]),
            run_time=0.4
        )

        # --- Spotlight card 1 + progress bar (12s – 20s) ---
        update_sub(
            "Bắt đầu với bước đầu tiên: trích xuất đặc trưng bằng Gabor Wavelets",
            4.0
        )

        # Progress bar — 4 chấm tròn + đường nối
        progress_dots = VGroup(*[
            Circle(
                radius=0.1,
                color=accents[i] if i == 0 else TEXT_MUTED,
                fill_color=accents[i] if i == 0 else BG_NAVY_SOFT,
                fill_opacity=1.0,
                stroke_width=1.6
            )
            for i in range(4)
        ]).arrange(RIGHT, buff=0.85)
        progress_dots.move_to(DOWN * 1.65)

        progress_lines = VGroup(*[
            Line(
                progress_dots[i].get_right(),
                progress_dots[i + 1].get_left(),
                color=TEXT_MUTED, stroke_width=1.8
            )
            for i in range(3)
        ])

        # Dim các card 2–4 + mũi tên, spotlight card 1
        dim_anims = [
            cards[j].animate.set_opacity(0.35) for j in range(1, 4)
        ] + [
            arrows[j].animate.set_opacity(0.25) for j in range(3)
        ]

        self.play(
            FadeOut(glows[3]),
            FadeIn(glows[0]),
            FadeIn(progress_dots, shift=UP * 0.12),
            Create(progress_lines),
            *dim_anims,
            run_time=1.2
        )

        # Pulse nhẹ glow card 1 để nhấn focus
        self.play(glows[0].animate.scale(1.06).set_opacity(0.5), run_time=0.7)
        self.play(glows[0].animate.scale(1.0 / 1.06).set_opacity(0.35), run_time=0.7)

        self.wait(1.0)

        # --- Cleanup ---
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)
