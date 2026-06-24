"""
EBGM Video — Algorithm Detail Section
Scene 15: Matching Procedure (Elastic Bunch Graph Matching — 4 BƯỚC)
Thời lượng dự kiến: 110s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)
  - Hoạt động trong conda env "vid"

Render command:
  manim -pql scene_15_matching_procedure.py Scene15_MatchingProcedure
  manim -pqh scene_15_matching_procedure.py Scene15_MatchingProcedure  # high quality
"""

from manim import *
import numpy as np
from _common import *

def make_elastic_wireframe(pos, color, scale=1.0, stretch_x=1.0, stretch_y=1.0, node_offsets=None):
    g = VGroup()
    # 6 baseline nodes
    n_pos = {
        0: np.array([-0.6 * stretch_x, 0.5 * stretch_y, 0]),
        1: np.array([0.6 * stretch_x, 0.5 * stretch_y, 0]),
        2: np.array([0, 0.0, 0]),
        3: np.array([-0.4 * stretch_x, -0.4 * stretch_y, 0]),
        4: np.array([0.4 * stretch_x, -0.4 * stretch_y, 0]),
        5: np.array([0, -0.8 * stretch_y, 0]),
    }
    
    # Apply local per-node displacement offsets
    if node_offsets is not None:
        for k, offset in node_offsets.items():
            if k in n_pos:
                n_pos[k] = n_pos[k] + offset
                
    # Draw edges
    pairs = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
    for p1, p2 in pairs:
        line = Line(
            (n_pos[p1] * scale) + pos,
            (n_pos[p2] * scale) + pos,
            color=color, stroke_width=1.8
        )
        g.add(line)
        
    # Draw nodes
    for k, p in n_pos.items():
        dot = Dot(
            (p * scale) + pos,
            radius=0.07, color=color
        )
        g.add(dot)
    return g

class Scene15_MatchingProcedure(Scene):
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
        # PHASE A: Setup Title & Roadmap Progress Bar (0s - 15s)
        # ============================================================
        title = section_title("Elastic Bunch Graph Matching --- 4 Bước")
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # Create Roadmap Progress Bar at UP * 2.2
        roadmap_bg = RoundedRectangle(
            corner_radius=0.08, width=12.2, height=0.75, color=TEXT_MUTED, stroke_width=1.0,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.9
        ).shift(UP * 2.1)
        self.play(FadeIn(roadmap_bg), run_time=0.6)

        # Draw 4 boxes inside progress bar
        step_titles = [
            "1. Vị trí thô",
            "2. Vị trí + Size",
            "3. Tỷ lệ x/y",
            "4. Biến dạng cục bộ"
        ]
        
        step_boxes = VGroup()
        step_labels = VGroup()
        box_width = 2.85
        for idx, text in enumerate(step_titles):
            pos_x = (idx - 1.5) * 3.0
            box = RoundedRectangle(
                corner_radius=0.06, width=box_width, height=0.55, color=TEXT_MUTED, stroke_width=0.8,
                fill_color=BG_NAVY, fill_opacity=1.0
            ).move_to(np.array([pos_x, 2.1, 0]))
            lbl = vn_tex_bold(text, color=TEXT_MUTED, scale=0.38).move_to(box.get_center())
            step_boxes.add(box)
            step_labels.add(lbl)

        self.play(
            LaggedStart(*[FadeIn(b) for b in step_boxes], lag_ratio=0.15),
            LaggedStart(*[FadeIn(l) for l in step_labels], lag_ratio=0.15),
            run_time=1.2
        )

        def highlight_step(step_idx):
            anims = []
            for idx in range(4):
                if idx == step_idx:
                    anims.append(step_boxes[idx].animate.set_stroke(HIGHLIGHT_HOT, width=1.5).set_fill(HIGHLIGHT_HOT, opacity=0.25))
                    anims.append(step_labels[idx].animate.set_color(HIGHLIGHT_HOT))
                else:
                    anims.append(step_boxes[idx].animate.set_stroke(TEXT_MUTED, width=0.8).set_fill(BG_NAVY, opacity=1.0))
                    anims.append(step_labels[idx].animate.set_color(TEXT_MUTED))
            self.play(*anims, run_time=0.6)

        # Draw a beautiful vector face silhouette on the left to act as probe image
        face_contour = Arc(radius=1.8, start_angle=-PI/2, angle=PI, color=ACCENT_BLUE, stroke_width=1.0).shift(LEFT * 2.8 + DOWN * 0.4)
        face_profile = VGroup(
            face_contour,
            # Nose profile bulge
            Line(face_contour.get_top(), LEFT * 1.8 + UP * 0.3, color=ACCENT_BLUE, stroke_width=1.0),
            Line(LEFT * 1.8 + UP * 0.3, LEFT * 1.6 + DOWN * 0.0, color=ACCENT_BLUE, stroke_width=1.0),
            Line(LEFT * 1.6 + DOWN * 0.0, LEFT * 2.5 + DOWN * 0.4, color=ACCENT_BLUE, stroke_width=1.0),
            # Chin bulge
            Arc(radius=0.3, start_angle=PI/2, angle=-PI/2, color=ACCENT_BLUE, stroke_width=1.0).move_to(LEFT * 2.7 + DOWN * 1.6)
        )
        # 6 reference target landmark dots in green
        landmarks_pos = {
            0: LEFT * 3.5 + UP * 0.2,   # L Eye
            1: LEFT * 2.6 + UP * 0.2,   # R Eye
            2: LEFT * 2.9 + DOWN * 0.3,  # Nose
            3: LEFT * 3.3 + DOWN * 0.8,  # L Mouth
            4: LEFT * 2.7 + DOWN * 0.8,  # R Mouth
            5: LEFT * 2.9 + DOWN * 1.4,  # Chin
        }
        landmark_dots = VGroup(*[Dot(p, radius=0.08, color=ACCENT_MINT) for k, p in landmarks_pos.items()])
        landmark_label = vn_tex("Landmarks ảnh mới", color=ACCENT_MINT, scale=0.38).next_to(face_contour, DOWN, buff=0.2)

        update_sub("Bốn bước Elastic Bunch Graph Matching: từ thô đến tinh", 5.0)

        self.play(
            FadeIn(face_profile, shift=RIGHT * 0.2),
            FadeIn(landmark_dots, shift=RIGHT * 0.2),
            FadeIn(landmark_label, shift=RIGHT * 0.2),
            run_time=1.5
        )
        self.wait(1.5)

        # ============================================================
        # PHASE B: STEP 1 — Approximate Position (15s - 35s)
        # ============================================================
        highlight_step(0)
        update_sub("Bước 1: Tìm vị trí xấp xỉ --- quét toàn ảnh bằng mô hình cứng", 6.0)

        # Rigid Model: FBG average
        rigid_g = make_elastic_wireframe(RIGHT * 2.5 + DOWN * 0.4, color=ACCENT_BLUE, scale=1.4)
        lbl_rigid = vn_tex_bold("Rigid Graph (Đồ thị trung bình)", color=ACCENT_BLUE, scale=0.45).next_to(rigid_g, UP, buff=0.25)
        
        self.play(
            FadeIn(rigid_g, shift=LEFT * 0.2),
            FadeIn(lbl_rigid, shift=LEFT * 0.15),
            run_time=1.2
        )
        self.wait(1.5)

        update_sub("Mô hình cứng được sinh bằng cách trung bình hóa FBG, chưa dùng phase", 6.0)
        self.play(FadeOut(lbl_rigid), run_time=0.6)

        # Slide rigid model across scan grid (4 positions)
        scan_coords = [
            LEFT * 3.8 + UP * 0.5,
            LEFT * 2.0 + UP * 0.5,
            LEFT * 3.8 + DOWN * 1.2,
            LEFT * 2.9 + DOWN * 0.4  # Best fit
        ]
        
        # Mini score bar on the right
        score_bg = RoundedRectangle(
            corner_radius=0.08, width=3.5, height=0.28, color=TEXT_MUTED, stroke_width=0.8,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.7
        ).shift(RIGHT * 3.5 + DOWN * 0.4)
        score_lbl = vn_tex_bold("Độ tương đồng Sa", color=TEXT_PRIMARY, scale=0.38).next_to(score_bg, UP, buff=0.15)
        
        def get_score_fill(percentage):
            if percentage <= 0.01:
                return VMobject()
            width_fill = percentage * 3.42
            return RoundedRectangle(
                corner_radius=0.06, width=width_fill, height=0.22, color=ACCENT_CYAN, stroke_width=0.0,
                fill_color=ACCENT_CYAN, fill_opacity=0.9
            ).move_to(score_bg.get_left() + RIGHT * (width_fill / 2 + 0.04))

        self.play(
            FadeIn(score_bg),
            FadeIn(score_lbl),
            run_time=0.8
        )

        fill_score = get_score_fill(0.12)
        self.play(FadeIn(fill_score), run_time=0.3)

        # Scanning loop
        scan_scores = [0.15, 0.30, 0.22, 0.85]
        for step_idx, pos in enumerate(scan_coords):
            lbl_scan_pos = vn_tex_italic(f"Thử quét vị trí {step_idx + 1}...", color=TEXT_MUTED, scale=0.38).next_to(score_bg, DOWN, buff=0.25)
            self.play(FadeIn(lbl_scan_pos), run_time=0.3)
            
            new_rigid = make_elastic_wireframe(pos, color=ACCENT_CYAN, scale=1.4)
            new_fill = get_score_fill(scan_scores[step_idx])
            
            self.play(
                ReplacementTransform(rigid_g, new_rigid),
                ReplacementTransform(fill_score, new_fill),
                run_time=0.8
            )
            rigid_g = new_rigid
            fill_score = new_fill
            self.play(FadeOut(lbl_scan_pos), run_time=0.2)

        # Highlight optimal global position with Flash
        opt_lbl = vn_tex_bold("VỊ TRÍ TỐT NHẤT!", color=ACCENT_MINT, scale=0.45).next_to(score_bg, DOWN, buff=0.25)
        self.play(
            Flash(rigid_g.get_center(), color=ACCENT_MINT, flash_radius=0.8),
            Indicate(rigid_g, scale_factor=1.05, color=ACCENT_MINT),
            FadeIn(opt_lbl, shift=UP * 0.1),
            run_time=1.2
        )
        self.wait(2.0)
        self.play(FadeOut(opt_lbl), run_time=0.6)

        # ============================================================
        # PHASE C: STEP 2 — Position + Size (35s - 55s)
        # ============================================================
        highlight_step(1)
        update_sub("Bước 2: Tinh chỉnh vị trí và kích thước đồng thời", 5.0)

        # Thử 8 cấu hình: 4 dịch chuyển (±3, ±3) × 2 kích thước (1.0x, 1.15x)
        # We will wiggle the graph sequentially representing these tests and display high score
        update_sub("Thử 8 cấu hình khác nhau, bắt đầu sử dụng phase ở tần số thấp (Focus 1)", 6.0)

        config_scales = [1.0, 1.15, 1.0, 1.15, 1.0, 1.15, 1.05]
        config_offsets = [
            UP * 0.2 + RIGHT * 0.2,
            DOWN * 0.2 + LEFT * 0.2,
            UP * 0.2 + LEFT * 0.2,
            DOWN * 0.2 + RIGHT * 0.2,
            UP * 0.1,
            DOWN * 0.1,
            ORIGIN  # Optimal size 1.08x
        ]
        config_scores = [0.80, 0.72, 0.78, 0.82, 0.88, 0.74, 0.94]

        for c_idx in range(len(config_scales)):
            new_rigid = make_elastic_wireframe(
                LEFT * 2.9 + DOWN * 0.4 + config_offsets[c_idx],
                color=HIGHLIGHT_HOT if c_idx == 6 else ACCENT_CYAN,
                scale=1.4 * config_scales[c_idx]
            )
            new_fill = get_score_fill(config_scores[c_idx])
            self.play(
                ReplacementTransform(rigid_g, new_rigid),
                ReplacementTransform(fill_score, new_fill),
                run_time=0.45
            )
            rigid_g = new_rigid
            fill_score = new_fill

        self.play(
            Flash(rigid_g.get_center(), color=HIGHLIGHT_HOT, flash_radius=0.8),
            Indicate(rigid_g, scale_factor=1.05, color=HIGHLIGHT_HOT),
            run_time=1.0
        )
        self.wait(1.5)

        # ============================================================
        # PHASE D: STEP 3 — Aspect Ratio (55s - 75s)
        # ============================================================
        highlight_step(2)
        update_sub("Bước 3: Điều chỉnh tỷ lệ khung hình x và y độc lập", 5.0)

        # Scale x and y independently
        # Configs: stretched along x, stretched along y, optimal balanced stretching
        update_sub("Tăng độ phân giải của sóng Gabor (Focus 1 lên 5) giúp tinh chỉnh subpixel", 6.0)

        # Focus indicator circle around L Eye node
        focus_dot = Dot(landmarks_pos[0], radius=0.18, color=ACCENT_CYAN, fill_opacity=0.0, stroke_width=1.5)
        focus_lbl = vn_tex_bold("Focus: 1", color=ACCENT_CYAN, scale=0.38).next_to(focus_dot, UP, buff=0.15)
        
        self.play(
            Create(focus_dot),
            FadeIn(focus_lbl),
            run_time=0.8
        )

        stretches_x = [1.2, 0.9, 1.05]
        stretches_y = [0.95, 1.2, 1.02]
        stretch_scores = [0.90, 0.88, 0.96]

        for s_idx in range(len(stretches_x)):
            # Update focus label sequentially
            new_focus_lbl = vn_tex_bold(f"Focus: {s_idx * 2 + 1}", color=ACCENT_CYAN, scale=0.38).move_to(focus_lbl.get_center())
            new_rigid = make_elastic_wireframe(
                LEFT * 2.9 + DOWN * 0.4,
                color=ACCENT_LAVENDER if s_idx == 2 else ACCENT_CYAN,
                scale=1.4,
                stretch_x=stretches_x[s_idx],
                stretch_y=stretches_y[s_idx]
            )
            new_fill = get_score_fill(stretch_scores[s_idx])
            
            self.play(
                ReplacementTransform(rigid_g, new_rigid),
                ReplacementTransform(fill_score, new_fill),
                ReplacementTransform(focus_lbl, new_focus_lbl),
                focus_dot.animate.scale(0.72 - s_idx * 0.15),  # expanding lens effect zoom-in
                run_time=0.9
            )
            rigid_g = new_rigid
            fill_score = new_fill
            focus_lbl = new_focus_lbl

        self.play(
            FadeOut(focus_dot),
            FadeOut(focus_lbl),
            run_time=0.6
        )
        self.wait(1.5)

        # ============================================================
        # PHASE E: STEP 4 — Local Distortion (75s - 100s)
        # ============================================================
        highlight_step(3)
        update_sub("Bước 4: Biến dạng cục bộ --- lúc này đồ thị thực sự trở nên đàn hồi!", 6.0)

        # Each node wiggles independently. Draw small arrows at each node.
        # Nodes shift to perfectly match landmark dots.
        # λ=2 so distortion penalty is active. We display distortion penalty bar.
        penalty_bg = RoundedRectangle(
            corner_radius=0.08, width=3.5, height=0.28, color=TEXT_MUTED, stroke_width=0.8,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.7
        ).shift(RIGHT * 3.5 + DOWN * 1.2)
        penalty_lbl = vn_tex_bold("Hình phạt biến dạng (Distortion Penalty)", color=ACCENT_CORAL, scale=0.35).next_to(penalty_bg, UP, buff=0.12)
        
        def get_penalty_fill(percentage):
            if percentage <= 0.01:
                return VMobject()
            width_fill = percentage * 3.42
            return RoundedRectangle(
                corner_radius=0.06, width=width_fill, height=0.22, color=ACCENT_CORAL, stroke_width=0.0,
                fill_color=ACCENT_CORAL, fill_opacity=0.9
            ).move_to(penalty_bg.get_left() + RIGHT * (width_fill / 2 + 0.04))

        self.play(
            FadeIn(penalty_bg),
            FadeIn(penalty_lbl),
            run_time=0.8
        )

        update_sub("Lúc này lambda = 2. Nếu nút dịch chuyển quá xa cấu trúc sẽ bị phạt nặng", 6.0)

        # Individual wiggles (elastic matching)
        # Node offsets to wiggles
        offsets_history = [
            # Wiggle 1: L Eye node wiggles too far → penalty jumps
            ({0: np.array([-0.3, 0.15, 0])}, 0.95, 0.45),
            # Wiggle 2: L Eye node refines to best position → penalty drops, similarity high
            ({0: np.array([-0.05, 0.0, 0])}, 0.97, 0.08),
            # Wiggle 3: Chin node wiggles to best position
            ({0: np.array([-0.05, 0.0, 0]), 5: np.array([0.02, -0.05, 0])}, 0.98, 0.09),
            # Wiggle 4: All nodes adapt perfectly to landmarks pos
            ({
                0: np.array([-0.04, 0.02, 0]),
                1: np.array([0.0, 0.0, 0]),
                2: np.array([0.01, -0.02, 0]),
                3: np.array([-0.02, -0.02, 0]),
                4: np.array([0.02, -0.01, 0]),
                5: np.array([0.02, -0.05, 0])
             }, 0.99, 0.05)
        ]

        fill_penalty = get_penalty_fill(0.0)
        self.play(FadeIn(fill_penalty), run_time=0.3)

        for w_idx, (node_offsets, sim_val, pen_val) in enumerate(offsets_history):
            new_rigid = make_elastic_wireframe(
                LEFT * 2.9 + DOWN * 0.4,
                color=HIGHLIGHT_HOT if w_idx == 3 else ACCENT_LAVENDER,
                scale=1.4,
                stretch_x=1.05,
                stretch_y=1.02,
                node_offsets=node_offsets
            )
            new_sim_fill = get_score_fill(sim_val)
            new_pen_fill = get_penalty_fill(pen_val)

            # Draw wiggling arrows on active wiggling nodes
            active_arrows = VGroup()
            if w_idx == 0:
                # Arrow for L Eye node
                arr = Arrow(LEFT * 3.7 + UP * 0.3, LEFT * 4.0 + UP * 0.45, color=HIGHLIGHT_HOT, buff=0, stroke_width=2)
                active_arrows.add(arr)
            elif w_idx == 2:
                # Arrow for Chin node
                arr = Arrow(LEFT * 2.9 + DOWN * 1.5, LEFT * 2.9 + DOWN * 1.8, color=HIGHLIGHT_HOT, buff=0, stroke_width=2)
                active_arrows.add(arr)

            self.play(
                ReplacementTransform(rigid_g, new_rigid),
                ReplacementTransform(fill_score, new_sim_fill),
                ReplacementTransform(fill_penalty, new_pen_fill),
                FadeIn(active_arrows),
                run_time=1.0
            )
            self.play(FadeOut(active_arrows), run_time=0.2)
            rigid_g = new_rigid
            fill_score = new_sim_fill
            fill_penalty = new_pen_fill

        self.wait(1.5)

        # Clear Phase B-E elements for Phase F
        self.play(
            FadeOut(face_profile),
            FadeOut(landmark_dots),
            FadeOut(landmark_label),
            FadeOut(rigid_g),
            FadeOut(fill_score),
            FadeOut(score_bg),
            FadeOut(score_lbl),
            FadeOut(fill_penalty),
            FadeOut(penalty_bg),
            FadeOut(penalty_lbl),
            run_time=0.8
        )

        # ============================================================
        # PHASE F: Kết quả - Showcase 2 types of grids (100s - 110s)
        # ============================================================
        update_sub("Kết quả: Image Graph khớp hoàn hảo lên ảnh khuôn mặt", 4.0)

        # Draw two grids side by side (recreating paper Figure 4)
        # Left: Face Finding grid (outline-heavy)
        # Right: Face Recognition grid (interior-heavy)
        grid_l_pos = LEFT * 3.0 + DOWN * 0.4
        grid_r_pos = RIGHT * 3.0 + DOWN * 0.4
        
        # Face finding grid outline
        finding_g = make_elastic_wireframe(grid_l_pos, color=ACCENT_CYAN, scale=1.4, stretch_x=1.1, stretch_y=1.05)
        lbl_finding = vn_tex_bold("1. Face Finding Grid (Viền mặt)", color=ACCENT_CYAN, scale=0.45).next_to(finding_g, UP, buff=0.3)
        desc_finding = vn_tex_italic("Mật độ cao ở outline, thưa ở giữa", color=TEXT_MUTED, scale=0.38).next_to(lbl_finding, DOWN, buff=0.12)

        # Face recognition grid
        recognition_g = make_elastic_wireframe(grid_r_pos, color=ACCENT_LAVENDER, scale=1.3, stretch_x=0.95, stretch_y=0.98)
        lbl_rec = vn_tex_bold("2. Face Recognition Grid (Chi tiết)", color=ACCENT_LAVENDER, scale=0.45).next_to(recognition_g, UP, buff=0.3)
        desc_rec = vn_tex_italic("Mật độ dày đặc ở mắt, mũi, miệng, cằm", color=TEXT_MUTED, scale=0.38).next_to(lbl_rec, DOWN, buff=0.12)

        update_sub("Đây là 'Image Graph' --- biểu diễn tối ưu nhất cho khuôn mặt này!", 6.0)

        self.play(
            FadeIn(finding_g, shift=UP * 0.25),
            FadeIn(lbl_finding, shift=UP * 0.15),
            FadeIn(desc_finding, shift=UP * 0.1),
            FadeIn(recognition_g, shift=UP * 0.25),
            FadeIn(lbl_rec, shift=UP * 0.15),
            FadeIn(desc_rec, shift=UP * 0.1),
            run_time=2.0
        )
        self.wait(3.5)

        # Cleanup everything
        self.play(
            FadeOut(title),
            FadeOut(roadmap_bg),
            FadeOut(step_boxes),
            FadeOut(step_labels),
            FadeOut(finding_g),
            FadeOut(lbl_finding),
            FadeOut(desc_finding),
            FadeOut(recognition_g),
            FadeOut(lbl_rec),
            FadeOut(desc_rec),
            run_time=0.8
        )
        self.wait(0.3)
