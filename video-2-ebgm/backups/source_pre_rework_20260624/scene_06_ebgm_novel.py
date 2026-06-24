"""
EBGM Video — Overview Section
Scene 6: Cách tiếp cận novel của EBGM
Thời lượng dự kiến: 75s

 YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts
  - XeLaTeX (thường có sẵn trong TeX Live)

Render command:
  manim -pql scene_06_ebgm_novel.py Scene6_EBGM_Novel
  manim -pqh scene_06_ebgm_novel.py Scene6_EBGM_Novel  # high quality
"""

from manim import *
import numpy as np
from _common import *

# ============================================================
# LOCAL STYLIZED PROCEDURAL BUILDERS
# ============================================================
def make_jet_icon(scale=1.0):
    """Generates a mathematical Gabor wavelet packet radiating in 8 directions."""
    wedges = VGroup()
    # 3 frequencies, 8 directions
    for nu in range(3):
        for mu in range(8):
            freq = 1.2 + nu * 0.9
            angle = mu * PI / 8
            u_ray = np.array([np.cos(angle), np.sin(angle), 0])
            u_perp = np.array([-np.sin(angle), np.cos(angle), 0])
            
            # Parametric wave with Gaussian decay envelope
            curve = ParametricFunction(
                lambda t: t * u_ray + 0.12 * np.exp(-((t - 0.32)**2) / 0.04) * np.sin(freq * t * 15) * u_perp,
                t_range=[0.0, 0.65], 
                color=ACCENT_CYAN, 
                stroke_width=0.6
            )
            wedges.add(curve)
    return wedges.scale(scale)

def make_mini_graph(color=ACCENT_BLUE, scale=0.75):
    """Stylized face landmark graph with 6 nodes and connecting edges."""
    p_forehead = np.array([0, 0.55, 0])
    p_eye_l = np.array([-0.3, 0.15, 0])
    p_eye_r = np.array([0.3, 0.15, 0])
    p_nose = np.array([0, -0.15, 0])
    p_mouth_l = np.array([-0.25, -0.45, 0])
    p_mouth_r = np.array([0.25, -0.45, 0])
    
    nodes = VGroup(
        Dot(point=p_forehead, radius=0.05, color=color),
        Dot(point=p_eye_l, radius=0.05, color=color),
        Dot(point=p_eye_r, radius=0.05, color=color),
        Dot(point=p_nose, radius=0.05, color=color),
        Dot(point=p_mouth_l, radius=0.05, color=color),
        Dot(point=p_mouth_r, radius=0.05, color=color)
    )
    
    edges = VGroup(
        Line(p_forehead, p_eye_l, color=color, stroke_width=0.8).set_opacity(0.35),
        Line(p_forehead, p_eye_r, color=color, stroke_width=0.8).set_opacity(0.35),
        Line(p_eye_l, p_eye_r, color=color, stroke_width=0.8).set_opacity(0.35),
        Line(p_eye_l, p_nose, color=color, stroke_width=0.8).set_opacity(0.35),
        Line(p_eye_r, p_nose, color=color, stroke_width=0.8).set_opacity(0.35),
        Line(p_nose, p_mouth_l, color=color, stroke_width=0.8).set_opacity(0.35),
        Line(p_nose, p_mouth_r, color=color, stroke_width=0.8).set_opacity(0.35),
        Line(p_mouth_l, p_mouth_r, color=color, stroke_width=0.8).set_opacity(0.35),
    )
    
    return VGroup(edges, nodes).scale(scale)

# ============================================================
# MAIN SCENE
# ============================================================
class Scene6_EBGM_Novel(Scene):
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

        # === Part A: Reveal tên EBGM (0s - 10s) ===
        update_sub("EBGM --- Elastic Bunch Graph Matching", 6.0)

        # Large beautiful opening title
        ebgm_title = vn_tex_bold("EBGM", color=ACCENT_CYAN, scale=1.4)
        ebgm_full = vn_tex_bold("Elastic Bunch Graph Matching", color=TEXT_PRIMARY, scale=0.75)
        ebgm_sub = vn_tex_italic("Một cách tiếp cận trung gian đầy mới mẻ", color=TEXT_MUTED, scale=0.52)
        
        ebgm_title.move_to(UP * 1.5)
        ebgm_full.next_to(ebgm_title, DOWN, buff=0.25)
        ebgm_sub.next_to(ebgm_full, DOWN, buff=0.35)

        # Floating node network background
        np.random.seed(42)
        background_nodes = VGroup()
        for _ in range(12):
            x = np.random.uniform(-6.0, 6.0)
            y = np.random.uniform(-3.5, 3.5)
            node = Dot(point=[x, y, 0], radius=np.random.uniform(0.02, 0.05), color=ACCENT_LAVENDER).set_opacity(0.2)
            background_nodes.add(node)
        
        self.play(
            FadeIn(background_nodes),
            FadeIn(ebgm_title, shift=DOWN*0.2),
            Write(ebgm_full),
            run_time=2.0
        )
        self.play(FadeIn(ebgm_sub, shift=UP*0.15), run_time=1.0)
        self.wait(1.0)

        # Drifting animation of background nodes
        drift_anims = [
            node.animate.shift(np.array([np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3), 0]))
            for node in background_nodes
        ]
        self.play(
            *drift_anims,
            run_time=2.0
        )

        update_sub("Một cách tiếp cận trung gian, linh hoạt hơn các phương pháp trước", 4.0)
        
        # Clean up Part A elements
        self.play(
            FadeOut(ebgm_title),
            FadeOut(ebgm_full),
            FadeOut(ebgm_sub),
            FadeOut(background_nodes),
            run_time=0.8
        )

        # === Part B: Tóm tắt 3 khái niệm cốt lõi (10s - 35s) ===
        # 10s - 18s: Image Graph
        update_sub("Image Graph --- biểu diễn khuôn mặt bằng đồ thị các điểm mốc", 8.0)

        sec_title = section_title("Khái niệm cốt lõi của EBGM")
        sec_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(sec_title, shift=DOWN*0.15), run_time=0.8)

        # Three container boxes
        box_width, box_height = 3.4, 4.4
        box1 = RoundedRectangle(corner_radius=0.1, width=box_width, height=box_height, color=ACCENT_BLUE, fill_color=BG_NAVY_SOFT, fill_opacity=0.35)
        box2 = RoundedRectangle(corner_radius=0.1, width=box_width, height=box_height, color=ACCENT_CYAN, fill_color=BG_NAVY_SOFT, fill_opacity=0.35)
        box3 = RoundedRectangle(corner_radius=0.1, width=box_width, height=box_height, color=ACCENT_LAVENDER, fill_color=BG_NAVY_SOFT, fill_opacity=0.35)
        
        concept_boxes = VGroup(box1, box2, box3).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.3)
        
        # Concept Titles
        c_title1 = vn_tex_bold("1. Image Graph", color=ACCENT_BLUE, scale=0.55).next_to(box1.get_top(), DOWN, buff=0.3)
        c_title2 = vn_tex_bold("2. Wavelet Jet", color=ACCENT_CYAN, scale=0.55).next_to(box2.get_top(), DOWN, buff=0.3)
        c_title3 = vn_tex_bold("3. Bunch Graph", color=ACCENT_LAVENDER, scale=0.55).next_to(box3.get_top(), DOWN, buff=0.3)

        self.play(
            FadeIn(concept_boxes, shift=UP*0.25),
            FadeIn(c_title1),
            FadeIn(c_title2),
            FadeIn(c_title3),
            run_time=2.0
        )
        self.wait(0.5)

        # Icon 1: Image Graph
        img_graph = make_mini_graph(color=ACCENT_BLUE, scale=1.35).move_to(box1.get_center() + DOWN * 0.2)
        self.play(
            Create(img_graph[0]), # edges
            LaggedStart(*[GrowFromCenter(n) for n in img_graph[1]], lag_ratio=0.15),
            run_time=2.0
        )
        self.wait(1.0)

        # 18s - 26s: Wavelet Jet
        update_sub("Jet --- tập hợp các đặc trưng tần số và hướng tại mỗi điểm mốc", 8.0)

        # Icon 2: Gabor Jet
        jet_icon = make_jet_icon(scale=1.15).move_to(box2.get_center() + DOWN * 0.25)
        jet_center_dot = Dot(point=box2.get_center() + DOWN * 0.25, radius=0.08, color=ACCENT_CYAN)
        
        self.play(
            Create(jet_icon),
            FadeIn(jet_center_dot),
            run_time=3.0
        )
        self.wait(1.0)

        # 26s - 34s: Bunch Graph
        update_sub("Bunch Graph --- chồng nhiều đồ thị mẫu để bao phủ các biến thể", 8.0)

        # Icon 3: Bunch Graph stacked deck
        bunch_deck = VGroup()
        colors = [ACCENT_BLUE, ACCENT_TEAL, ACCENT_LAVENDER, ACCENT_CYAN]
        for i, color in enumerate(colors):
            g = make_mini_graph(color=color, scale=1.1)
            g.shift(UP * (i * 0.14) + RIGHT * (i * 0.14))
            bunch_deck.add(g)
        bunch_deck.move_to(box3.get_center() + DOWN * 0.4 + LEFT * 0.15)
        
        self.play(
            LaggedStart(
                *[FadeIn(g, shift=UP*0.12 + RIGHT*0.12) for g in bunch_deck],
                lag_ratio=0.25
            ),
            run_time=2.5
        )
        self.wait(1.5)

        # Clean up Part B
        self.play(
            FadeOut(concept_boxes),
            FadeOut(c_title1),
            FadeOut(c_title2),
            FadeOut(c_title3),
            FadeOut(img_graph),
            FadeOut(jet_icon),
            FadeOut(jet_center_dot),
            FadeOut(bunch_deck),
            FadeOut(sec_title),
            run_time=0.8
        )

        # === Part C: 4 ưu điểm chính của EBGM (34s - 70s) ===
        # 34s - 42s: Advantage 1
        update_sub("Trơ lì tuyệt vời trước ánh sáng nhờ đặc tính vật lý của Gabor wavelets", 8.0)

        adv_title = section_title("Ưu điểm vượt trội của EBGM")
        adv_title.to_edge(UP, buff=0.45)
        self.play(FadeIn(adv_title, shift=DOWN*0.15), run_time=0.8)

        # Define 4 cards in 2x2 grid layout
        card_w, card_h = 5.2, 1.8
        card1 = RoundedRectangle(corner_radius=0.08, width=card_w, height=card_h, color=ACCENT_BLUE, fill_color=BG_NAVY_SOFT, fill_opacity=0.35)
        card2 = RoundedRectangle(corner_radius=0.08, width=card_w, height=card_h, color=ACCENT_CYAN, fill_color=BG_NAVY_SOFT, fill_opacity=0.35)
        card3 = RoundedRectangle(corner_radius=0.08, width=card_w, height=card_h, color=ACCENT_TEAL, fill_color=BG_NAVY_SOFT, fill_opacity=0.35)
        card4 = RoundedRectangle(corner_radius=0.08, width=card_w, height=card_h, color=ACCENT_LAVENDER, fill_color=BG_NAVY_SOFT, fill_opacity=0.35)

        card1.move_to([-2.9, 1.0, 0])
        card2.move_to([2.9, 1.0, 0])
        card3.move_to([-2.9, -1.1, 0])
        card4.move_to([2.9, -1.1, 0])

        # Content for Card 1
        icon1 = make_jet_icon(scale=0.35).move_to(card1.get_left() + RIGHT * 0.5)
        t_card1 = vn_tex_bold("1. Trơ lì trước biến động", color=ACCENT_BLUE, scale=0.48).next_to(icon1, RIGHT, buff=0.35).shift(UP * 0.3)
        d_card1 = vn_tex("Bất biến trước sự thay đổi của ánh sáng\nvà độ dịch chuyển nhỏ.", color=TEXT_MUTED, scale=0.36).next_to(t_card1, DOWN, buff=0.08).align_to(t_card1, LEFT)
        c1_grp = VGroup(card1, icon1, t_card1, d_card1)

        # Content for Card 2
        icon2 = make_mini_graph(color=ACCENT_CYAN, scale=0.4).move_to(card2.get_left() + RIGHT * 0.5)
        t_card2 = vn_tex_bold("2. Tổ hợp linh hoạt", color=ACCENT_CYAN, scale=0.48).next_to(icon2, RIGHT, buff=0.35).shift(UP * 0.3)
        d_card2 = vn_tex("Tự động khớp và bù trừ linh hoạt giữa\ncác tư thế và biểu cảm khác nhau.", color=TEXT_MUTED, scale=0.36).next_to(t_card2, DOWN, buff=0.08).align_to(t_card2, LEFT)
        c2_grp = VGroup(card2, icon2, t_card2, d_card2)

        # Content for Card 3
        # Small stacked deck representation for Icon 3
        icon3 = VGroup(
            RoundedRectangle(corner_radius=0.02, width=0.4, height=0.5, color=ACCENT_TEAL, fill_color=BG_NAVY, fill_opacity=0.7),
            RoundedRectangle(corner_radius=0.02, width=0.4, height=0.5, color=ACCENT_TEAL, fill_color=BG_NAVY, fill_opacity=0.7).shift(RIGHT*0.06 + UP*0.06),
            RoundedRectangle(corner_radius=0.02, width=0.4, height=0.5, color=ACCENT_TEAL, fill_color=BG_NAVY, fill_opacity=0.7).shift(RIGHT*0.12 + UP*0.12),
        ).move_to(card3.get_left() + RIGHT * 0.45)
        t_card3 = vn_tex_bold("3. Yêu cầu ít dữ liệu", color=ACCENT_TEAL, scale=0.48).next_to(icon3, RIGHT, buff=0.35).shift(UP * 0.3)
        d_card3 = vn_tex("Chỉ cần khoảng 70 ảnh khuôn mặt gốc\nlàm mẫu là đủ nhận dạng xuất sắc.", color=TEXT_MUTED, scale=0.36).next_to(t_card3, DOWN, buff=0.08).align_to(t_card3, LEFT)
        c3_grp = VGroup(card3, icon3, t_card3, d_card3)

        # Content for Card 4
        icon4 = VGroup(
            Line([-0.18, 0, 0], [0.18, 0, 0], color=ACCENT_MINT, stroke_width=3),
            Line([0, -0.18, 0], [0, 0.18, 0], color=ACCENT_MINT, stroke_width=3)
        ).move_to(card4.get_left() + RIGHT * 0.5)
        t_card4 = vn_tex_bold("4. Dễ dàng mở rộng", color=ACCENT_LAVENDER, scale=0.48).next_to(icon4, RIGHT, buff=0.35).shift(UP * 0.3)
        d_card4 = vn_tex("Gặp ngoại lệ chỉ cần nạp thêm ảnh vào\nbunch graph mà không phải lập trình lại.", color=TEXT_MUTED, scale=0.36).next_to(t_card4, DOWN, buff=0.08).align_to(t_card4, LEFT)
        c4_grp = VGroup(card4, icon4, t_card4, d_card4)

        # Display Card 1
        self.play(
            FadeIn(card1),
            Create(icon1),
            Write(t_card1),
            FadeIn(d_card1, shift=UP*0.08),
            run_time=1.8
        )
        self.wait(0.5)

        # 42s - 50s: Advantage 2
        update_sub("Linh hoạt: mỗi điểm trên graph tự chọn 'expert' khớp tốt nhất trong bunch", 8.0)
        self.play(
            FadeIn(card2),
            Create(icon2),
            Write(t_card2),
            FadeIn(d_card2, shift=UP*0.08),
            run_time=1.8
        )
        self.wait(0.5)

        # 50s - 58s: Advantage 3
        update_sub("Hiệu quả dữ liệu cực cao: chỉ khoảng 70 mẫu cho toàn bộ hệ thống", 8.0)
        self.play(
            FadeIn(card3),
            Create(icon3),
            Write(t_card3),
            FadeIn(d_card3, shift=UP*0.08),
            run_time=1.8
        )
        self.wait(0.5)

        # 58s - 66s: Advantage 4
        update_sub("Khi gặp góc mặt mới, chỉ cần thêm ảnh vào bunch mà không cần học lại từ đầu", 8.0)
        self.play(
            FadeIn(card4),
            Create(icon4),
            Write(t_card4),
            FadeIn(d_card4, shift=UP*0.08),
            run_time=1.8
        )
        self.wait(1.0)

        # 66s - 70s: Synthesis circular wrap
        update_sub("Cân bằng hoàn hảo giữa thiết kế đặc trưng và khả năng tự tổ hợp cấu trúc", 4.0)

        # Glowing container surrounding all cards
        synthesis_box = RoundedRectangle(
            corner_radius=0.15,
            width=11.6,
            height=4.6,
            color=ACCENT_CYAN,
            stroke_width=2.0,
            fill_color=BG_NAVY,
            fill_opacity=0.0
        ).move_to(DOWN * 0.05)
        
        synthesis_lbl = vn_tex_bold("CÂN BẰNG GIỮA THIẾT KẾ THỦ CÔNG VÀ HỌC MÁY", color=ACCENT_CYAN, scale=0.55)
        synthesis_lbl.move_to(adv_title)

        self.play(
            Create(synthesis_box),
            ReplacementTransform(adv_title, synthesis_lbl),
            # Dim all cards slightly to pop the circular wrap
            c1_grp.animate.set_opacity(0.4),
            c2_grp.animate.set_opacity(0.4),
            c3_grp.animate.set_opacity(0.4),
            c4_grp.animate.set_opacity(0.4),
            run_time=2.0
        )
        self.wait(1.5)

        # Clean up Part C
        self.play(
            FadeOut(synthesis_box),
            FadeOut(synthesis_lbl),
            FadeOut(c1_grp),
            FadeOut(c2_grp),
            FadeOut(c3_grp),
            FadeOut(c4_grp),
            run_time=0.8
        )

        # === Part D: Câu chốt (70s - 75s) ===
        update_sub("EBGM hoạt động gần giống cách nhận thức tự nhiên ở con người", 5.0)

        conc_q1 = vn_tex("EBGM gần với cách hệ thống nhận thức tự nhiên hoạt động,", color=TEXT_PRIMARY, scale=0.55)
        conc_q2 = vn_tex("nơi bộ não chỉ cần vài chục mẫu đại diện là đủ.", color=TEXT_PRIMARY, scale=0.55)
        conclusion_grp = VGroup(conc_q1, conc_q2).arrange(DOWN, buff=0.15).move_to(ORIGIN)

        self.play(
            Write(conclusion_grp),
            run_time=2.5
        )
        self.wait(1.5)

        # Final cleanup
        self.play(FadeOut(conclusion_grp), run_time=0.8)
        self.wait(0.2)
