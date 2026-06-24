"""
EBGM Video — Algorithm Detail Section
Scene 17: Recognition Stage (So sánh & Xếp hạng probe vs gallery)
Thời lượng dự kiến: 60s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)
  - Hoạt động trong conda env "vid"

Render command:
  manim -pql scene_17_recognition_stage.py Scene17_RecognitionStage
  manim -pqh scene_17_recognition_stage.py Scene17_RecognitionStage  # high quality
"""

from manim import *
import numpy as np
from _common import *

def make_tiny_model_graph(pos, color, scale=0.5):
    """A very simplified mini graph representation for gallery cards."""
    g = VGroup()
    n_pos = {
        0: np.array([-0.4, 0.4, 0]),
        1: np.array([0.4, 0.4, 0]),
        2: np.array([-0.3, -0.4, 0]),
        3: np.array([0.3, -0.4, 0]),
    }
    pairs = [(0, 1), (0, 2), (1, 3), (2, 3), (0, 3)]
    for p1, p2 in pairs:
        line = Line(
            (n_pos[p1] * scale) + pos,
            (n_pos[p2] * scale) + pos,
            color=color, stroke_width=1.0
        )
        g.add(line)
    for k, p in n_pos.items():
        dot = Dot(
            (p * scale) + pos,
            radius=0.04, color=color
        )
        g.add(dot)
    return g

class Scene17_RecognitionStage(Scene):
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
        # PHASE A: Probe vs Gallery Setup (0s - 12s)
        # ============================================================
        title = section_title("Nhận diện --- Hạng 1 Chiến thắng")
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=0.8)

        # Subtitle 1 (0s - 6s)
        update_sub("Bước cuối cùng: So sánh Image Graph vừa trích xuất với Gallery dữ liệu", 5.0)

        # Left: Probe Image Graph Card
        probe_card = RoundedRectangle(
            corner_radius=0.08, width=3.4, height=4.2, color=ACCENT_CYAN, stroke_width=1.5,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.7
        ).shift(LEFT * 3.4 + DOWN * 0.3)
        lbl_probe = vn_tex_bold("PROBE (Ảnh cần nhận dạng)", color=ACCENT_CYAN, scale=0.4).next_to(probe_card, UP, buff=0.18)

        # Probe detailed face graph
        probe_graph = make_tiny_model_graph(probe_card.get_center(), color=ACCENT_CYAN, scale=1.8)

        self.play(
            FadeIn(probe_card, shift=RIGHT * 0.2),
            FadeIn(lbl_probe, shift=UP * 0.1),
            FadeIn(probe_graph),
            run_time=1.5
        )

        # Right: Gallery 3x3 Grid
        gallery_card = RoundedRectangle(
            corner_radius=0.08, width=5.6, height=4.2, color=ACCENT_LAVENDER, stroke_width=1.0,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.3
        ).shift(RIGHT * 3.2 + DOWN * 0.3)
        lbl_gallery = vn_tex_bold("GALLERY (Cơ sở dữ liệu mẫu)", color=ACCENT_LAVENDER, scale=0.4).next_to(gallery_card, UP, buff=0.18)
        self.play(FadeIn(gallery_card), FadeIn(lbl_gallery), run_time=0.8)

        # 3x3 Grid of tiny candidate cards inside gallery_card
        candidates = VGroup()
        cand_labels = VGroup()
        for r in range(3):
            for c in range(3):
                idx = r * 3 + c + 1
                pos = gallery_card.get_center() + np.array([(c - 1) * 1.6, (1 - r) * 1.15, 0])
                c_card = RoundedRectangle(
                    corner_radius=0.05, width=1.3, height=0.9, color=ACCENT_LAVENDER, stroke_width=0.6,
                    fill_color=BG_NAVY, fill_opacity=0.9
                ).move_to(pos)
                c_graph = make_tiny_model_graph(pos + DOWN * 0.05, color=ACCENT_LAVENDER, scale=0.65)
                c_lbl = vn_tex(f"M{idx}", color=TEXT_MUTED, scale=0.25).move_to(pos + UP * 0.3)
                candidates.add(VGroup(c_card, c_graph))
                cand_labels.add(c_lbl)

        self.play(
            LaggedStart(*[FadeIn(c) for c in candidates], lag_ratio=0.1),
            LaggedStart(*[FadeIn(l) for l in cand_labels], lag_ratio=0.1),
            run_time=1.5
        )

        # Subtitle 2 (6s - 12s)
        update_sub("So sánh probe với từng mẫu đã lưu để tính điểm tương đồng", 5.0)

        # Draw a scanning arrow from probe to gallery
        scan_arrow = Arrow(probe_card.get_right() + RIGHT * 0.1, gallery_card.get_left() + LEFT * 0.1, color=HIGHLIGHT_HOT, stroke_width=2.5)
        self.play(Create(scan_arrow), run_time=0.8)
        self.wait(1.5)

        # Clear Phase A setup for formula presentation
        self.play(
            FadeOut(probe_card), FadeOut(lbl_probe), FadeOut(probe_graph),
            FadeOut(gallery_card), FadeOut(lbl_gallery),
            FadeOut(candidates), FadeOut(cand_labels),
            FadeOut(scan_arrow),
            run_time=0.8
        )

        # ============================================================
        # PHASE B: Formula & Process (12s - 35s)
        # ============================================================
        # Subtitle 3 (12s - 20s)
        update_sub("Công thức tính độ tương đồng đồ thị tổng thể", 4.0)

        # Recognition Formula
        rec_formula = MathTex(
            r"\mathcal{S}_G(\mathcal{G}^I, \mathcal{G}^M) = ",
            r"\frac{1}{N'}\sum_{n'} \mathcal{S}_a(\mathcal{J}_{n'}^I, \mathcal{J}_{n_{n'}}^M)",
            tex_template=VN_TEX_TEMPLATE,
            color=TEXT_PRIMARY
        ).scale(0.85).move_to(UP * 0.6)

        self.play(Write(rec_formula), run_time=2.0)
        self.wait(0.5)

        # Subtitle 4 (20s - 28s)
        update_sub("Lưu ý: Chỉ sử dụng biên độ Sa, hoàn toàn bỏ qua phần pha phi", 5.0)

        # Highlight note box
        note_box = RoundedRectangle(
            corner_radius=0.08, width=10.5, height=1.6, color=ACCENT_CYAN, stroke_width=1.2,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.8
        ).shift(DOWN * 1.0)
        note_lbl = vn_tex_bold("LÝ DO BỎ QUA PHA (PHASE OMITTED):", color=ACCENT_CYAN, scale=0.4).shift(DOWN * 0.45).align_to(note_box, LEFT).shift(RIGHT * 0.5)
        
        note_bullets = VGroup(
            vn_tex("- Giúp thuật toán trơn tru hơn, tránh các điểm cực tiểu cục bộ", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("- Cực kỳ bền bỉ (robust) trước các thay đổi về biểu cảm khuôn mặt", color=TEXT_PRIMARY, scale=0.38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(note_lbl, DOWN, buff=0.18).align_to(note_lbl, LEFT)

        self.play(
            Create(note_box),
            FadeIn(note_lbl, shift=UP * 0.15),
            FadeIn(note_bullets, shift=UP * 0.1),
            run_time=1.5
        )
        self.wait(2.2)

        # Clear formula & note
        self.play(
            FadeOut(rec_formula),
            FadeOut(note_box),
            FadeOut(note_lbl),
            FadeOut(note_bullets),
            run_time=0.8
        )

        # ============================================================
        # PHASE C: Laser Scan & Live Scores (35s - 50s)
        # ============================================================
        # Bring back grids but smaller/compacted for leaderboard animation
        self.play(
            FadeIn(probe_card), FadeIn(lbl_probe), FadeIn(probe_graph),
            FadeIn(gallery_card), FadeIn(lbl_gallery),
            FadeIn(candidates), FadeIn(cand_labels),
            run_time=1.0
        )

        # Subtitle 5 (28s - 38s)
        update_sub("Quá trình quét và so khớp diễn ra liên tục trên Gallery...", 5.0)

        # Draw a wiggling laser sweeping over candidates
        laser = Line(gallery_card.get_left() + UP * 2.0, gallery_card.get_left() + DOWN * 2.0, color=ACCENT_CYAN, stroke_width=2.5).set_opacity(0.8)
        self.play(FadeIn(laser), run_time=0.3)
        self.play(laser.animate.shift(RIGHT * 5.6), run_time=1.8, rate_func=linear)
        self.play(FadeOut(laser), run_time=0.3)

        # Spawning similarity scores next to candidate labels
        # Score floats
        cand_scores = [0.38, 0.45, 0.89, 0.52, 0.31, 0.64, 0.40, 0.48, 0.35]
        score_labels = VGroup()
        for idx, score in enumerate(cand_scores):
            pos = candidates[idx].get_center() + DOWN * 0.35
            lbl = vn_tex(f"S={score}", color=ACCENT_MINT if score > 0.8 else TEXT_MUTED, scale=0.28).move_to(pos)
            score_labels.add(lbl)

        self.play(
            LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in score_labels], lag_ratio=0.15),
            run_time=1.5
        )
        self.wait(1.5)

        # Subtitle 6 (38s - 48s)
        update_sub("Sắp xếp điểm số: Ứng viên M3 đạt độ tương đồng cao nhất (89\%)", 5.0)

        # We will highlight Candidate 3 (which has index 2 in 0-indexed list)
        win_card = candidates[2][0]
        win_lbl = cand_labels[2]
        win_score = score_labels[2]

        self.play(
            win_card.animate.set_stroke(HIGHLIGHT_HOT, width=2.5).set_fill(HIGHLIGHT_HOT, opacity=0.3),
            win_lbl.animate.set_color(HIGHLIGHT_HOT).scale(1.2),
            win_score.animate.set_color(HIGHLIGHT_HOT).scale(1.2),
            run_time=0.8
        )
        self.play(
            Flash(win_card.get_center(), color=HIGHLIGHT_HOT, flash_radius=0.8),
            Indicate(win_card, scale_factor=1.08, color=HIGHLIGHT_HOT),
            run_time=1.2
        )
        self.wait(1.5)

        # Clear other candidates and transition to final sorting stats
        other_cands = VGroup(*[candidates[idx] for idx in range(9) if idx != 2])
        other_lbls = VGroup(*[cand_labels[idx] for idx in range(9) if idx != 2])
        other_scores = VGroup(*[score_labels[idx] for idx in range(9) if idx != 2])

        self.play(
            FadeOut(other_cands),
            FadeOut(other_lbls),
            FadeOut(other_scores),
            FadeOut(gallery_card),
            FadeOut(lbl_gallery),
            FadeOut(probe_card),
            FadeOut(lbl_probe),
            FadeOut(probe_graph),
            VGroup(win_card, win_lbl, win_score).animate.scale(1.5).move_to(LEFT * 3.4 + DOWN * 0.3),
            run_time=1.2
        )

        # ============================================================
        # PHASE D: Sorting leader board & Rank 1 Success (48s - 60s)
        # ============================================================
        # Leader board on the right
        leader_bg = RoundedRectangle(
            corner_radius=0.08, width=5.6, height=3.8, color=TEXT_MUTED, stroke_width=0.8,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.8
        ).shift(RIGHT * 3.2 + DOWN * 0.3)
        leader_title = vn_tex_bold("BẢNG XẾP HẠNG (LEADERBOARD)", color=ACCENT_CYAN, scale=0.45).shift(RIGHT * 3.2 + UP * 1.1)

        ranks = VGroup(
            vn_tex("Hạng 1: Ứng viên M3 --- Điểm: 0.89 [WINNER]", color=HIGHLIGHT_HOT, scale=0.42),
            vn_tex("Hạng 2: Ứng viên M6 --- Điểm: 0.64", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("Hạng 3: Ứng viên M4 --- Điểm: 0.52", color=TEXT_PRIMARY, scale=0.38),
            vn_tex("Hạng 4: Ứng viên M8 --- Điểm: 0.48", color=TEXT_MUTED, scale=0.35)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(leader_title, DOWN, buff=0.4).align_to(leader_title, LEFT)

        self.play(
            FadeIn(leader_bg),
            FadeIn(leader_title, shift=UP * 0.15),
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ranks], lag_ratio=0.15),
            run_time=1.5
        )
        self.wait(1.5)

        # Subtitle 7 (48s - 60s)
        update_sub("Thử nghiệm FERET: Đạt tỉ lệ chính xác Rank 1 tuyệt hảo trên 95\%!", 6.0)

        # Win Star next to Winner text
        star = Star(color=HIGHLIGHT_HOT, fill_color=HIGHLIGHT_HOT, fill_opacity=0.9).scale(0.18).next_to(ranks[0], RIGHT, buff=0.2)
        self.play(
            FadeIn(star, shift=LEFT * 0.15),
            Flash(star.get_center(), color=HIGHLIGHT_HOT, flash_radius=0.4),
            run_time=1.0
        )
        self.wait(3.0)

        # Final cleanup ending scene
        self.play(
            FadeOut(title),
            FadeOut(win_card),
            FadeOut(win_lbl),
            FadeOut(win_score),
            FadeOut(leader_bg),
            FadeOut(leader_title),
            FadeOut(ranks),
            FadeOut(star),
            run_time=0.8
        )
        self.wait(0.3)
