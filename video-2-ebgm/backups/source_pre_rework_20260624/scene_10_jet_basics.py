"""
EBGM Video — Algorithm Detail Section
Scene 10: Jet — 40 hệ số phức tại một điểm
Thời lượng dự kiến: 60s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)
  - Hoạt động trong conda env "vid"

Render command:
  manim -pql scene_10_jet_basics.py Scene10_JetBasics
  manim -pqh scene_10_jet_basics.py Scene10_JetBasics  # high quality
"""

from manim import *
import numpy as np
from _common import *

class Scene10_JetBasics(Scene):
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
        # PHASE A: Định nghĩa Jet (0s - 10s)
        # ============================================================
        # Section Title
        title = section_title("Jet --- 40 hệ số phức tại một điểm")
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=1.0)

        # Formula for Jet
        formula = MathTex(
            r"\mathcal{J}_j = a_j \exp(i\phi_j), \quad j = \mu + 8\nu",
            tex_template=VN_TEX_TEMPLATE,
            color=TEXT_PRIMARY
        ).scale(0.85).move_to(UP * 0.2)

        sub_formula = MathTex(
            r"\nu = 0, \dots, 4 \quad (\text{tần số}), \quad \mu = 0, \dots, 7 \quad (\text{hướng})",
            tex_template=VN_TEX_TEMPLATE,
            color=ACCENT_CYAN
        ).scale(0.65).next_to(formula, DOWN, buff=0.4)

        self.play(Write(formula), run_time=2.0)
        self.play(FadeIn(sub_formula, shift=UP * 0.15), run_time=1.0)
        
        # Subtitle 1 (0s - 6s)
        update_sub("Một jet là gì?", 5.0)

        # Subtitle 2 (6s - 14s)
        update_sub("Jet = bộ 40 hệ số phức tại MỘT điểm ảnh", 6.0)

        # Clear Phase A math elements
        self.play(
            FadeOut(formula),
            FadeOut(sub_formula),
            run_time=0.8
        )

        # ============================================================
        # PHASE B: Stacked Disks Visualization (10s - 30s)
        # ============================================================
        # Face representation on bottom left
        face_outline = Ellipse(width=1.6, height=2.2, color=ACCENT_BLUE, stroke_width=1.5, fill_opacity=0.08)
        eye_l = Circle(radius=0.1, color=ACCENT_BLUE, stroke_width=1.5).shift(LEFT * 0.3 + UP * 0.2)
        eye_r = Circle(radius=0.1, color=ACCENT_BLUE, stroke_width=1.5).shift(RIGHT * 0.3 + UP * 0.2)
        face_grp = VGroup(face_outline, eye_l, eye_r).scale(0.85).shift(LEFT * 4.8 + DOWN * 0.8)
        
        dot = Dot(eye_l.get_left() + RIGHT * 0.05, radius=0.08, color=ACCENT_CYAN)
        zoom_arrow = Arrow(
            start=dot.get_center(),
            end=LEFT * 2.5 + UP * 0.5,
            color=ACCENT_CYAN, stroke_width=2.5, buff=0.05
        )

        self.play(
            FadeIn(face_grp),
            FadeIn(dot),
            GrowArrow(zoom_arrow),
            run_time=1.2
        )

        # Subtitle 3 (14s - 22s)
        update_sub("Cấu trúc: 5 tần số x 8 hướng, xếp như 5 chiếc đĩa chồng lên nhau", 8.0)

        # Generate Stacked Disks with tilt perspective
        jets_disks = VGroup()
        for nu in range(5):
            disk = VGroup()
            for mu in range(8):
                sector = AnnularSector(
                    inner_radius=0.4 + nu * 0.08,
                    outer_radius=0.7 + nu * 0.08,
                    start_angle=mu * PI/4,
                    angle=PI/4,
                    color=interpolate_color(ManimColor(ACCENT_CYAN), ManimColor(ACCENT_LAVENDER), mu/7),
                    fill_opacity=0.6,
                    stroke_color=BG_NAVY,
                    stroke_width=0.8
                )
                disk.add(sector)
            disk.shift(UP * nu * 0.45)
            jets_disks.add(disk)
            
        jets_disks.rotate(30 * DEGREES, axis=RIGHT)
        jets_disks.scale(0.9).move_to(RIGHT * 0.2 + DOWN * 0.6)

        # Show stacked disks sequentially
        for nu in range(5):
            self.play(
                FadeIn(jets_disks[nu], shift=UP * 0.15),
                run_time=0.45
            )

        # Add labels to the right of each disk
        disk_labels = VGroup()
        for nu in range(5):
            lbl = vn_tex_mono(rf"\nu = {nu}", color=TEXT_MUTED, scale=0.42)
            # Position labels relative to each stacked disk's average vertical height
            lbl.move_to(jets_disks[nu].get_right() + RIGHT * 0.5)
            disk_labels.add(lbl)

        # Subtitle 4 (22s - 30s)
        update_sub("Mỗi sector trong đĩa = 1 hướng cụ thể", 8.0)

        self.play(
            FadeIn(disk_labels),
            run_time=1.0
        )
        self.wait(1.5)

        # Highlight single sector (e.g. mu=0, nu=0)
        target_sector = jets_disks[0][0]
        glow_sector = target_sector.copy().set_stroke(HIGHLIGHT_HOT, width=4, opacity=0.9).set_fill(color=HIGHLIGHT_HOT, opacity=0.8)
        
        lbl_sector = vn_tex_mono(r"j = 0 + 8 \times 0 = 0", color=HIGHLIGHT_HOT, scale=0.45)
        lbl_sector.next_to(jets_disks[0], DOWN, buff=0.35)

        self.play(
            FadeIn(glow_sector),
            Write(lbl_sector),
            Flash(target_sector.get_center(), color=HIGHLIGHT_HOT, flash_radius=0.7),
            run_time=1.2
        )
        self.wait(2.0)

        # Clear Phase B elements
        self.play(
            FadeOut(face_grp),
            FadeOut(dot),
            FadeOut(zoom_arrow),
            FadeOut(jets_disks),
            FadeOut(disk_labels),
            FadeOut(glow_sector),
            FadeOut(lbl_sector),
            run_time=1.0
        )

        # ============================================================
        # PHASE C: Phase vs Magnitude Curves (30s - 55s)
        # ============================================================
        # Subtitle 5 (30s - 38s)
        update_sub("Mỗi hệ số phức tách thành hai phần: magnitude và phase", 8.0)

        # Left Axes: Magnitude
        ax_mag = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1.2, 0.5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"color": GRID_LINE, "stroke_width": 1.2}
        ).shift(LEFT * 3.4 + DOWN * 0.8)

        mag_title = vn_tex_bold("Magnitude (Trị tuyệt đối)", color=ACCENT_MINT, scale=0.48).next_to(ax_mag, UP, buff=0.3)
        mag_curve = ax_mag.plot(
            lambda x: np.exp(-x**2 / 1.5),
            color=ACCENT_MINT, stroke_width=2.5
        )
        mag_desc = vn_tex_italic("Biến đổi CHẬM --- Dùng để tìm thô", color=TEXT_MUTED, scale=0.4).next_to(ax_mag, DOWN, buff=0.3)

        # Right Axes: Phase
        ax_phase = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1.2, 1.2, 0.5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"color": GRID_LINE, "stroke_width": 1.2}
        ).shift(RIGHT * 3.4 + DOWN * 0.8)

        phase_title = vn_tex_bold("Phase (Góc pha)", color=ACCENT_LAVENDER, scale=0.48).next_to(ax_phase, UP, buff=0.3)
        phase_curve = ax_phase.plot(
            lambda x: np.cos(3 * x) * np.exp(-x**2 / 5),
            color=ACCENT_LAVENDER, stroke_width=2.5
        )
        phase_desc = vn_tex_italic("Biến đổi NHANH --- Định vị subpixel tinh", color=TEXT_MUTED, scale=0.4).next_to(ax_phase, DOWN, buff=0.3)

        # Subtitle 6 (38s - 46s)
        update_sub("Magnitude biến đổi chậm theo không gian --- dùng để tìm thô", 5.0)

        # Display Left plot
        self.play(
            FadeIn(ax_mag),
            FadeIn(mag_title),
            Create(mag_curve),
            FadeIn(mag_desc),
            run_time=1.5
        )
        self.wait(1.5)

        # Subtitle 7 (46s - 54s)
        update_sub("Phase biến đổi nhanh --- dùng để định vị chính xác đến subpixel", 5.0)

        # Display Right plot
        self.play(
            FadeIn(ax_phase),
            FadeIn(phase_title),
            Create(phase_curve),
            FadeIn(phase_desc),
            run_time=1.5
        )
        self.wait(4.0)

        # Clear plots for concluding formula
        self.play(
            FadeOut(VGroup(ax_mag, mag_title, mag_curve, mag_desc)),
            FadeOut(VGroup(ax_phase, phase_title, phase_curve, phase_desc)),
            run_time=0.8
        )

        # ============================================================
        # PHASE D: Concluding & Merge (55s - 60s)
        # ============================================================
        # Subtitle 8 (54s - 60s)
        update_sub("40 con số --- đủ để mô tả 'cái gì xảy ra tại điểm này'", 6.0)

        # Premium merged formula
        merge_formula = MathTex(
            r"\mathcal{J} = \Big\{ a_j \exp(i\phi_j) \Big\}_{j=0}^{39}",
            tex_template=VN_TEX_TEMPLATE,
            color=TEXT_PRIMARY
        ).scale(1.0).move_to(UP * 0.2)

        desc_conclusion = vn_tex_bold(
            "Mô tả trọn vẹn đặc trưng cấu trúc cục bộ của khuôn mặt",
            color=ACCENT_CYAN, scale=0.55
        ).next_to(merge_formula, DOWN, buff=0.55)

        self.play(
            Write(merge_formula),
            run_time=2.0
        )
        self.play(
            FadeIn(desc_conclusion, shift=UP * 0.25),
            run_time=1.0
        )
        self.wait(2.2)

        # Cleanup
        self.play(
            FadeOut(title),
            FadeOut(merge_formula),
            FadeOut(desc_conclusion),
            run_time=0.8
        )
        self.wait(0.3)
