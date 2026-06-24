"""
EBGM Video — Algorithm Detail Section
Scene 13: Face Bunch Graph (FBG)
Thời lượng dự kiến: 70s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)
  - Hoạt động trong conda env "vid"

Render command:
  manim -pql scene_13_bunch_graph.py Scene13_BunchGraph
  manim -pqh scene_13_bunch_graph.py Scene13_BunchGraph  # high quality
"""

from manim import *
import numpy as np
from _common import *

def make_mini_jet_super_compact(pos, color=ACCENT_CYAN):
    jet = VGroup()
    for nu in range(2):
        disk = VGroup()
        for mu in range(8):
            sector = AnnularSector(
                inner_radius=0.08 + nu * 0.03,
                outer_radius=0.16 + nu * 0.03,
                start_angle=mu * PI/4,
                angle=PI/4,
                color=interpolate_color(ManimColor(color), ManimColor(TEXT_MUTED), 0.4),
                fill_opacity=0.5,
                stroke_color=BG_NAVY,
                stroke_width=0.25
            )
            disk.add(sector)
        disk.shift(UP * nu * 0.12)
        jet.add(disk)
    jet.rotate(25 * DEGREES, axis=RIGHT)
    jet.move_to(pos)
    return jet

def make_wireframe_graph(pos, color, opacity=0.6, scale=1.0):
    g = VGroup()
    # 6 landmark nodes
    n_pos = {
        0: np.array([-0.6, 0.5, 0]),   # L Eye
        1: np.array([0.6, 0.5, 0]),    # R Eye
        2: np.array([0.0, 0.0, 0]),    # Nose
        3: np.array([-0.4, -0.4, 0]),  # L Mouth
        4: np.array([0.4, -0.4, 0]),   # R Mouth
        5: np.array([0.0, -0.8, 0]),   # Chin
    }
    
    # Draw edges
    pairs = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
    for p1, p2 in pairs:
        line = Line(
            (n_pos[p1] * scale) + pos,
            (n_pos[p2] * scale) + pos,
            color=color, stroke_width=1.0, stroke_opacity=opacity
        )
        g.add(line)
        
    # Draw nodes
    for k, p in n_pos.items():
        dot = Dot(
            (p * scale) + pos,
            radius=0.04, color=color, fill_opacity=opacity
        )
        g.add(dot)
    return g

class Scene13_BunchGraph(Scene):
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
        # PHASE A: Đặt vấn đề & Đồ thị đơn lẻ (0s - 12s)
        # ============================================================
        # Section Title
        title = section_title("Face Bunch Graph --- Trí tuệ tổ hợp")
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=1.0)

        # Subtitle 1 (0s - 6s)
        update_sub("Một graph mẫu không thể đại diện cho mọi khuôn mặt", 5.5)

        # Draw a single baseline graph
        single_g = make_wireframe_graph(LEFT * 2.8 + DOWN * 0.3, color=ACCENT_BLUE, opacity=0.9, scale=1.4)
        single_lbl = vn_tex("Đồ thị đơn lẻ", color=ACCENT_BLUE, scale=0.45).next_to(single_g, UP, buff=0.3)
        
        insufficient_lbl = vn_tex_bold("❌ Chưa đủ đại diện sự đa dạng!", color=ACCENT_CORAL, scale=0.55).shift(RIGHT * 2.0 + DOWN * 0.3)

        self.play(
            FadeIn(single_g, shift=RIGHT * 0.25),
            FadeIn(single_lbl, shift=RIGHT * 0.25),
            run_time=1.5
        )
        self.play(
            FadeIn(insufficient_lbl, shift=LEFT * 0.2),
            run_time=1.0
        )
        self.wait(2.2)

        # Clear Phase A elements
        self.play(
            FadeOut(single_g),
            FadeOut(single_lbl),
            FadeOut(insufficient_lbl),
            run_time=0.8
        )

        # ============================================================
        # PHASE B: Xây dựng FBG - Stacked Graphs (12s - 35s)
        # ============================================================
        # Subtitle 2 (6s - 14s)
        update_sub("Giải pháp: chồng ~70 graphs lên thành một thực thể chung", 5.0)

        # Build FBG stack
        fbg_stack = VGroup()
        m_count = 5
        for m in range(m_count):
            g_color = interpolate_color(ManimColor(ACCENT_BLUE), ManimColor(ACCENT_LAVENDER), m / (m_count - 1))
            g_layer = make_wireframe_graph(
                ORIGIN, color=g_color, opacity=0.55, scale=1.5
            )
            g_layer.shift(UP * m * 0.32 + RIGHT * m * 0.08)
            fbg_stack.add(g_layer)
            
        fbg_stack.rotate(22 * DEGREES, axis=RIGHT)
        fbg_stack.scale(1.1).move_to(ORIGIN + DOWN * 0.4)

        # Subtitle 3 (14s - 22s)
        update_sub("Đó là Face Bunch Graph --- FBG", 5.0)

        # Stack graphs sequentially
        for m in range(m_count):
            self.play(
                FadeIn(fbg_stack[m], shift=UP * 0.15),
                run_time=0.45
            )

        # Add models count label on top right
        models_lbl = vn_tex_bold("M = 70 Models", color=HIGHLIGHT_HOT, scale=0.5).to_edge(RIGHT, buff=1.0).shift(UP * 1.5)

        # Subtitle 4 (22s - 30s)
        update_sub("Tất cả có cùng cấu trúc, các nodes ở cùng vị trí mốc", 5.0)

        self.play(
            FadeIn(models_lbl, shift=LEFT * 0.25),
            run_time=1.0
        )
        self.wait(1.5)

        # Draw a highlighted averaged edge framework
        avg_g = make_wireframe_graph(ORIGIN, color=ACCENT_LAVENDER, opacity=0.9, scale=1.5)
        avg_g.rotate(22 * DEGREES, axis=RIGHT).scale(1.1).move_to(ORIGIN + DOWN * 0.4)
        avg_g_glow = avg_g.copy().set_stroke(ACCENT_LAVENDER, width=3.5, opacity=0.6)

        # Subtitle 5 (30s - 38s)
        update_sub("Tại mỗi node: không phải 1 jet, mà là một CHÙM jets", 5.0)

        self.play(
            FadeIn(avg_g_glow),
            run_time=1.0
        )
        self.wait(2.0)

        # Clear stacked FBG for bunch zoom-in details
        self.play(
            FadeOut(fbg_stack),
            FadeOut(models_lbl),
            FadeOut(avg_g_glow),
            run_time=0.8
        )

        # ============================================================
        # PHASE C: Khái niệm "Bunch" tại 1 Node (35s - 55s)
        # ============================================================
        # Subtitle 6 (38s - 46s)
        update_sub("Mỗi jet trong chùm đến từ một khuôn mặt mẫu khác nhau", 6.0)

        # Build horizontal bunch of jets representing different eye variations
        bunch_grp = VGroup()
        labels_grp = VGroup()
        bunch_labels = [
            "Mắt nam", "Mắt nữ", "Mắt kính", "Mắt nhắm", "Mắt một mí", "Mắt xếch"
        ]
        
        bunch_width = 1.8
        for idx, text in enumerate(bunch_labels):
            pos_x = (idx - 2.5) * bunch_width
            mini_j = make_mini_jet_super_compact(np.array([pos_x, 0.2, 0]), color=ACCENT_CYAN)
            lbl = vn_tex_italic(text, color=TEXT_MUTED, scale=0.35)
            lbl.next_to(mini_j, DOWN, buff=0.25)
            
            bunch_grp.add(mini_j)
            labels_grp.add(lbl)

        # Draw a rounded background card for the Bunch
        bunch_card = RoundedRectangle(
            corner_radius=0.1, width=11.2, height=2.4, color=ACCENT_LAVENDER, stroke_width=1.2,
            fill_color=BG_NAVY_SOFT, fill_opacity=0.8
        ).move_to(DOWN * 0.2)

        card_title = vn_tex_bold("BUNCH (CHÙM) TẠI NÚT MẮT TRÁI", color=ACCENT_LAVENDER, scale=0.48).next_to(bunch_card, UP, buff=0.25)

        self.play(
            FadeIn(bunch_card, shift=UP * 0.2),
            FadeIn(card_title, shift=UP * 0.15),
            LaggedStart(*[FadeIn(j, shift=UP * 0.15) for j in bunch_grp], lag_ratio=0.12),
            LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in labels_grp], lag_ratio=0.12),
            run_time=2.0
        )
        self.wait(1.5)

        # Subtitle 7 (46s - 54s)
        update_sub("Khi quét ảnh mới, mỗi node tự CHỌN jet phù hợp nhất", 6.0)

        # Highlight best fitting jet (Index 2: Mắt kính)
        target_jet = bunch_grp[2]
        target_lbl = labels_grp[2]
        
        glow_box = SurroundingRectangle(target_jet, color=HIGHLIGHT_HOT, stroke_width=2.5, buff=0.15)
        glow_lbl = vn_tex_bold("Local Expert (Chọn tốt nhất!)", color=HIGHLIGHT_HOT, scale=0.36).next_to(glow_box, UP, buff=0.1)

        self.play(
            Create(glow_box),
            FadeIn(glow_lbl, shift=UP * 0.1),
            target_lbl.animate.set_color(HIGHLIGHT_HOT).scale(1.1),
            Indicate(target_jet, scale_factor=1.1, color=HIGHLIGHT_HOT),
            Flash(target_jet.get_center(), color=HIGHLIGHT_HOT, flash_radius=0.5),
            run_time=1.5
        )
        self.wait(2.2)

        # Clear Phase C elements
        self.play(
            FadeOut(bunch_card),
            FadeOut(card_title),
            FadeOut(bunch_grp),
            FadeOut(labels_grp),
            FadeOut(glow_box),
            FadeOut(glow_lbl),
            run_time=0.8
        )

        # ============================================================
        # PHASE D: Sức mạnh tổ hợp - Combinatorial Power (55s - 70s)
        # ============================================================
        # Subtitle 8 (54s - 62s)
        update_sub("Jet được chọn được gọi là 'local expert' --- chuyên gia cục bộ", 5.0)

        # Bring back wireframe face graph in high opacity
        final_g = make_wireframe_graph(ORIGIN + DOWN * 0.3, color=ACCENT_LAVENDER, opacity=0.9, scale=1.8)
        
        self.play(
            FadeIn(final_g),
            run_time=1.2
        )

        # Animate multiple nodes picking their local expert sequentially
        expert_circles = VGroup()
        expert_labels = ["J_1", "J_2", "J_3", "J_4"]
        target_nodes = [0, 1, 2, 5]  # L Eye, R Eye, Nose, Chin
        
        # Get positions of target nodes in scaled wireframe
        n_pos_raw = {
            0: np.array([-0.6, 0.5, 0]),
            1: np.array([0.6, 0.5, 0]),
            2: np.array([0.0, 0.0, 0]),
            5: np.array([0.0, -0.8, 0]),
        }

        # Subtitle 9 (62s - 70s)
        update_sub("FBG tổ hợp ra vô số khuôn mặt mới --- sức mạnh từ tính tổ hợp", 5.0)

        for idx, node_id in enumerate(target_nodes):
            p = n_pos_raw[node_id] * 1.8 + ORIGIN + DOWN * 0.3
            circ = Circle(radius=0.15, color=HIGHLIGHT_HOT, stroke_width=1.5).move_to(p)
            lbl = MathTex(rf"\mathcal{{J}}^{{\text{{exp}}}}_{{{idx}}}", tex_template=VN_TEX_TEMPLATE, color=HIGHLIGHT_HOT).scale(0.5).next_to(circ, RIGHT * 0.5 + UP * 0.5)
            expert_circles.add(VGroup(circ, lbl))
            
            self.play(
                FadeIn(circ),
                Write(lbl),
                Flash(p, color=HIGHLIGHT_HOT, flash_radius=0.4),
                run_time=0.5
            )

        self.wait(1.0)

        # Huge combinatorial math expression
        math_box = RoundedRectangle(
            corner_radius=0.1, width=7.2, height=1.6, color=HIGHLIGHT_HOT, stroke_width=1.5,
            fill_color=BG_NAVY, fill_opacity=0.9
        ).to_edge(UP, buff=1.3)
        
        combo_math = MathTex(
            r"M^N = 6^{16} \approx 2.8 \times 10^{12} \quad \text{tổ hợp cấu trúc}",
            tex_template=VN_TEX_TEMPLATE,
            color=HIGHLIGHT_HOT
        ).scale(0.72).move_to(math_box.get_center())

        combo_lbl = vn_tex_bold(
            "Tổ hợp vô số đặc trưng khuôn mặt mới từ 70 mẫu gốc!",
            color=ACCENT_CYAN, scale=0.48
        ).next_to(math_box, DOWN, buff=0.22)

        self.play(
            FadeIn(math_box, shift=DOWN * 0.25),
            Write(combo_math),
            run_time=1.5
        )
        self.play(
            FadeIn(combo_lbl, shift=DOWN * 0.15),
            run_time=1.0
        )
        self.wait(3.0)

        # Cleanup
        self.play(
            FadeOut(title),
            FadeOut(final_g),
            FadeOut(expert_circles),
            FadeOut(math_box),
            FadeOut(combo_math),
            FadeOut(combo_lbl),
            run_time=0.8
        )
        self.wait(0.3)
