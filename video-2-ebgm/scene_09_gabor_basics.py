"""
EBGM Video — Algorithm Detail Section
Scene 9: Gabor Wavelets — Khái niệm cơ bản
Thời lượng dự kiến: 80s

YÊU CẦU:
  - TeX Live 2022+ với Latin Modern fonts (để chạy _common.py helpers)
  - XeLaTeX (để render tiếng Việt qua vn_tex)
  - Hoạt động trong conda env "vid"

Render command:
  manim -pql scene_09_gabor_basics.py Scene9_GaborBasics
  manim -pqh scene_09_gabor_basics.py Scene9_GaborBasics  # high quality
"""

from manim import *
import numpy as np
from _common import *

# Function to generate 2D Gabor kernel array dynamically
def generate_gabor_mobject(orientation, freq=2.0, sigma=0.35, size=60):
    arr = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            x = (i - size/2) / size * 2
            y = (j - size/2) / size * 2
            # rotate
            xr = x * np.cos(orientation) + y * np.sin(orientation)
            yr = -x * np.sin(orientation) + y * np.cos(orientation)
            gauss = np.exp(-(xr**2 + yr**2) / (2 * sigma**2))
            wave = np.cos(2 * np.pi * freq * xr)
            arr[i, j] = gauss * wave
            
    # Normalize to [0, 255] grayscale
    gray = ((arr + 1.0) / 2.0 * 255.0).clip(0, 255).astype(np.uint8)
    # Stack to RGB
    rgb = np.stack([gray, gray, gray], axis=-1)
    
    img = ImageMobject(rgb)
    img.scale(0.025 * size) # scale to reasonable display size
    return img

class Scene9_GaborBasics(Scene):
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
        # PHASE A: Câu hỏi & Motivation (0s - 15s)
        # ============================================================
        # Section Title at the top
        title = section_title("Gabor Wavelets --- Mắt của EBGM")
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=1.0)

        # Main question
        question = vn_tex("Làm sao trích xuất đặc trưng tại MỘT điểm ảnh?", color=TEXT_PRIMARY, scale=0.7)
        self.play(Write(question), run_time=2.0)
        
        # Subtitle 1 (0s - 6s)
        update_sub("Bước 1: Trích xuất đặc trưng bằng Gabor Wavelets", 5.0)

        # Draw stylized face fallback using vector graphics
        face_outline = Ellipse(width=2.5, height=3.5, color=ACCENT_BLUE, stroke_width=2.0, fill_opacity=0.1)
        eye_l = Circle(radius=0.15, color=ACCENT_BLUE, stroke_width=2.0).shift(LEFT * 0.45 + UP * 0.3)
        eye_r = Circle(radius=0.15, color=ACCENT_BLUE, stroke_width=2.0).shift(RIGHT * 0.45 + UP * 0.3)
        nose = Line(UP * 0.1 + LEFT * 0.05, DOWN * 0.2 + RIGHT * 0.1, color=ACCENT_BLUE, stroke_width=2.0)
        mouth = Arc(radius=0.4, start_angle=-PI/6, angle=-2*PI/3, color=ACCENT_BLUE, stroke_width=2.0).shift(DOWN * 0.7)
        face_grp = VGroup(face_outline, eye_l, eye_r, nose, mouth).scale(0.95).shift(LEFT * 3.5 + DOWN * 0.5)

        # Animate face outline entry
        self.play(
            FadeOut(question),
            FadeIn(face_grp),
            run_time=1.2
        )

        # Subtitle 2 (6s - 12s)
        update_sub("Câu hỏi: làm sao mô tả 'cái gì' xảy ra tại MỘT điểm ảnh?", 6.0)

        # Highlight point (e.g. left eye pupil corner)
        highlight_pos = eye_l.get_left() + RIGHT * 0.08
        highlight_circle = Circle(radius=0.18, color=ACCENT_CYAN, stroke_width=2.0).move_to(highlight_pos)
        
        # Arrow pointing to the highlighted spot
        arrow = Arrow(
            start=highlight_pos + RIGHT * 1.5 + UP * 0.8,
            end=highlight_pos + RIGHT * 0.25 + UP * 0.1,
            color=ACCENT_CYAN, stroke_width=3.5, buff=0.05
        )
        
        # Point label
        point_lbl = vn_tex_italic("Điểm này nói lên điều gì?", color=ACCENT_CYAN, scale=0.45)
        point_lbl.next_to(arrow.get_start(), UP, buff=0.15)

        self.play(
            Create(highlight_circle),
            GrowArrow(arrow),
            Write(point_lbl),
            run_time=1.2
        )
        self.wait(1.6)

        # ============================================================
        # PHASE B: Convolution với Gabor Kernels (15s - 35s)
        # ============================================================
        # Subtitle 3 (12s - 20s)
        update_sub("Câu trả lời: convolve điểm đó với một bộ lọc đặc biệt", 3.0)

        # 3 Gabor kernels (0 deg, 45 deg, 90 deg)
        kernel0 = generate_gabor_mobject(0, size=50)
        kernel45 = generate_gabor_mobject(PI/4, size=50)
        kernel90 = generate_gabor_mobject(PI/2, size=50)
        
        # Draw background Soft Panels for Gabor kernels
        panels = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=1.1, height=1.1, color=GRID_LINE, stroke_width=1.0, fill_color=BG_NAVY_SOFT, fill_opacity=0.9)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.25).shift(LEFT * 0.8 + DOWN * 0.5)

        # Put kernels inside panels
        kernel0.move_to(panels[0].get_center())
        kernel45.move_to(panels[1].get_center())
        kernel90.move_to(panels[2].get_center())

        lbl0 = vn_tex_mono(r"\mu = 0", color=ACCENT_CYAN, scale=0.45).next_to(panels[0], RIGHT, buff=0.2)
        lbl45 = vn_tex_mono(r"\mu = 2", color=ACCENT_LAVENDER, scale=0.45).next_to(panels[1], RIGHT, buff=0.2)
        lbl90 = vn_tex_mono(r"\mu = 5", color=ACCENT_TEAL, scale=0.45).next_to(panels[2], RIGHT, buff=0.2)

        # Clean old Phase A pointer elements
        self.play(
            FadeOut(arrow),
            FadeOut(point_lbl),
            FadeOut(highlight_circle),
            FadeIn(panels),
            FadeIn(Group(kernel0, kernel45, kernel90)),
            FadeIn(VGroup(lbl0, lbl45, lbl90)),
            run_time=1.5
        )

        # Subtitle 4 (20s - 28s)
        update_sub("Gabor wavelet --- sóng phẳng bị giới hạn bởi envelope Gaussian", 8.0)

        # Mimic convolution / sliding window on the face
        scan_square = Square(side_length=0.4, color=ACCENT_CYAN, stroke_width=1.5).move_to(face_outline.get_corner(UL) + RIGHT * 0.5 + DOWN * 0.5)
        
        # Add output panel (Magnitude and Imaginary results placeholder)
        out_panel = RoundedRectangle(
            corner_radius=0.1, width=2.4, height=3.8,
            color=GRID_LINE, stroke_width=1.2, fill_color=BG_NAVY_SOFT, fill_opacity=0.9
        ).shift(RIGHT * 4.2 + DOWN * 0.5)
        
        out_title = vn_tex_bold("Kết quả chập", color=TEXT_PRIMARY, scale=0.48).move_to(out_panel.get_top() + DOWN * 0.3)
        
        # Stylized convolution results inside the output panel
        conv_imag = ImageMobject(np.random.randint(50, 200, size=(40, 40), dtype=np.uint8)).scale(0.8).move_to(out_panel.get_center() + UP * 0.3)
        conv_mag = ImageMobject(np.random.randint(80, 220, size=(40, 40), dtype=np.uint8)).scale(0.8).move_to(out_panel.get_center() + DOWN * 0.9)
        
        lbl_imag = vn_tex("Imaginary", color=ACCENT_LAVENDER, scale=0.35).next_to(conv_imag, DOWN, buff=0.15)
        lbl_mag = vn_tex("Magnitude", color=ACCENT_MINT, scale=0.35).next_to(conv_mag, DOWN, buff=0.15)

        self.play(
            FadeIn(scan_square),
            FadeIn(out_panel),
            FadeIn(out_title),
            run_time=1.0
        )

        # sliding animation
        self.play(
            scan_square.animate.move_to(face_outline.get_corner(DR) - RIGHT * 0.5 - UP * 0.5),
            FadeIn(Group(conv_imag, conv_mag, lbl_imag, lbl_mag)),
            run_time=3.5,
            rate_func=linear
        )
        self.wait(1.5)

        # Subtitle 5 (28s - 36s)
        update_sub("Mỗi điểm được mô tả bởi 5 tần số x 8 hướng = 40 hệ số", 8.0)

        # Display text below Gabor kernels
        desc_conv = vn_tex_italic("Mỗi kernel = sóng phẳng giới hạn bởi envelope Gaussian", color=ACCENT_BLUE, scale=0.5)
        desc_conv.next_to(panels, DOWN, buff=0.35)
        self.play(Write(desc_conv), run_time=1.5)
        self.wait(2.5)

        # Clear Phase B elements for formula
        self.play(
            FadeOut(face_grp),
            FadeOut(scan_square),
            FadeOut(panels),
            FadeOut(Group(kernel0, kernel45, kernel90)),
            FadeOut(VGroup(lbl0, lbl45, lbl90)),
            FadeOut(out_panel),
            FadeOut(out_title),
            FadeOut(Group(conv_imag, conv_mag, lbl_imag, lbl_mag)),
            FadeOut(desc_conv),
            run_time=1.0
        )

        # ============================================================
        # PHASE C: Công thức Toán (35s - 55s)
        # ============================================================
        # Subtitle 6 (36s - 46s)
        update_sub("Thành phần DC-free giúp trơ lì với thay đổi độ sáng nền", 5.0)

        # Math formula with split components for precise highlighting
        formula = MathTex(
            r"\psi_j(\vec{x}) = ",                                                 # Index 0
            r"\frac{k_j^2}{\sigma^2}\exp\!\left(-\frac{k_j^2 x^2}{2\sigma^2}\right)", # Index 1: Envelope Gaussian
            r"\left[",                                                            # Index 2
            r"\exp(i\vec{k}_j\vec{x})",                                           # Index 3: Plane wave
            r"-",                                                                 # Index 4
            r"\exp\!\left(-\frac{\sigma^2}{2}\right)",                            # Index 5: DC-free
            r"\right]",                                                           # Index 6
            tex_template=VN_TEX_TEMPLATE,
            color=TEXT_PRIMARY
        ).scale(0.85).move_to(UP * 0.2)
        
        self.play(Write(formula), run_time=2.5)
        self.wait(0.5)

        # Highlight part 1: Envelope Gaussian (Index 1)
        box_gauss = SurroundingRectangle(formula[1], color=ACCENT_CYAN, stroke_width=2.0)
        lbl_gauss = vn_tex("Envelope Gaussian", color=ACCENT_CYAN, scale=0.45)
        lbl_gauss.next_to(box_gauss, UP, buff=0.4)
        arrow_gauss = Arrow(lbl_gauss.get_bottom(), box_gauss.get_top(), color=ACCENT_CYAN, stroke_width=2.0, buff=0.08)

        self.play(
            Create(box_gauss),
            FadeIn(lbl_gauss, shift=UP * 0.15),
            GrowArrow(arrow_gauss),
            run_time=1.0
        )
        self.wait(2.0)

        # Subtitle 7 (46s - 56s)
        update_sub("Envelope Gaussian khoanh vùng cục bộ, chống dịch chuyển nhỏ", 3.0)

        # Highlight part 2 & 3: Plane wave (Index 3) & DC-free (Index 5)
        box_plane = SurroundingRectangle(formula[3], color=ACCENT_LAVENDER, stroke_width=2.0)
        lbl_plane = vn_tex("Sóng phẳng (Plane wave)", color=ACCENT_LAVENDER, scale=0.45)
        lbl_plane.next_to(box_plane, DOWN, buff=0.4)
        arrow_plane = Arrow(lbl_plane.get_top(), box_plane.get_bottom(), color=ACCENT_LAVENDER, stroke_width=2.0, buff=0.08)

        box_dc = SurroundingRectangle(formula[5], color=ACCENT_CORAL, stroke_width=2.0)
        lbl_dc = vn_tex("Khử thành phần một chiều (DC-free)", color=ACCENT_CORAL, scale=0.45)
        lbl_dc.next_to(box_dc, UP, buff=0.55)
        arrow_dc = Arrow(lbl_dc.get_bottom(), box_dc.get_top(), color=ACCENT_CORAL, stroke_width=2.0, buff=0.08)

        self.play(
            FadeOut(box_gauss), FadeOut(lbl_gauss), FadeOut(arrow_gauss),
            Create(box_plane), FadeIn(lbl_plane, shift=DOWN * 0.15), GrowArrow(arrow_plane),
            Create(box_dc), FadeIn(lbl_dc, shift=RIGHT * 0.15), GrowArrow(arrow_dc),
            run_time=1.2
        )
        
        # Informational small text
        info_tex = vn_tex(
            r"5 tần số \times 8 hướng = 40 hệ số tại mỗi điểm",
            color=TEXT_MUTED, scale=0.55
        ).to_edge(DOWN, buff=1.35)
        self.play(FadeIn(info_tex, shift=UP * 0.2), run_time=1.0)
        self.wait(3.8)

        # Clear mathematical elements
        self.play(
            FadeOut(formula),
            FadeOut(box_plane), FadeOut(lbl_plane), FadeOut(arrow_plane),
            FadeOut(box_dc), FadeOut(lbl_dc), FadeOut(arrow_dc),
            FadeOut(info_tex),
            run_time=0.8
        )

        # ============================================================
        # PHASE D: Vì sao Gabor? (55s - 80s)
        # ============================================================
        # Subtitle 8 (56s - 66s)
        update_sub("Gabor wavelet có hình dạng giống tế bào thần kinh thị giác", 4.0)

        # 4 cards (2x2 grid layout) explaining Gabor features
        card_recs = VGroup(*[
            RoundedRectangle(corner_radius=0.1, width=4.8, height=1.6, color=GRID_LINE, stroke_width=1.0, fill_color=BG_NAVY_SOFT, fill_opacity=0.9)
            for _ in range(4)
        ])
        
        # Position cards in 2x2 grid
        card_recs[0].move_to([-2.8, 0.8, 0])
        card_recs[1].move_to([2.8, 0.8, 0])
        card_recs[2].move_to([-2.8, -1.0, 0])
        card_recs[3].move_to([2.8, -1.0, 0])

        card_glows = []
        for i, card_rec in enumerate(card_recs):
            accent = [ACCENT_CYAN, ACCENT_LAVENDER, ACCENT_TEAL, ACCENT_MINT][i]
            glow = card_rec.copy().set_stroke(accent, width=6, opacity=0.3)
            glow.set_fill(opacity=0)
            card_glows.append(glow)

        # Add text & hand-drawn simple visual features for each card
        card_contents = VGroup()

        # Card 1: Khử DC (DC-free)
        c1_title = vn_tex_bold("1. Khử DC (DC-free)", color=ACCENT_CYAN, scale=0.48).move_to(card_recs[0].get_top() + DOWN * 0.35)
        c1_desc = vn_tex("Trơ lì trước sự thay đổi ánh sáng nền", color=TEXT_MUTED, scale=0.4).move_to(card_recs[0].get_bottom() + UP * 0.4)
        c1_visual = Circle(radius=0.1, color=ACCENT_CYAN, stroke_width=1.5).next_to(c1_title, RIGHT, buff=0.15)
        card_contents.add(VGroup(c1_title, c1_desc, c1_visual))

        # Card 2: Độ bền (Robust)
        c2_title = vn_tex_bold("2. Bền bỉ (Robust)", color=ACCENT_LAVENDER, scale=0.48).move_to(card_recs[1].get_top() + DOWN * 0.35)
        c2_desc = vn_tex("Chống chịu biến dạng nhỏ và xoay ảnh", color=TEXT_MUTED, scale=0.4).move_to(card_recs[1].get_bottom() + UP * 0.4)
        c2_visual = Triangle(color=ACCENT_LAVENDER).scale(0.1).next_to(c2_title, RIGHT, buff=0.15)
        card_contents.add(VGroup(c2_title, c2_desc, c2_visual))

        # Card 3: Sinh học (Biological)
        c3_title = vn_tex_bold("3. Tính sinh học", color=ACCENT_TEAL, scale=0.48).move_to(card_recs[2].get_top() + DOWN * 0.35)
        c3_desc = vn_tex("Mô phỏng receptive field vỏ não thị giác", color=TEXT_MUTED, scale=0.4).move_to(card_recs[2].get_bottom() + UP * 0.4)
        c3_visual = Rectangle(width=0.25, height=0.15, color=ACCENT_TEAL, stroke_width=1.5).next_to(c3_title, RIGHT, buff=0.15)
        card_contents.add(VGroup(c3_title, c3_desc, c3_visual))

        # Card 4: Tự nhiên (Natural)
        c4_title = vn_tex_bold("4. Thống kê tự nhiên", color=ACCENT_MINT, scale=0.48).move_to(card_recs[3].get_top() + DOWN * 0.35)
        c4_desc = vn_tex("Tối ưu trích xuất thông tin ảnh tự nhiên", color=TEXT_MUTED, scale=0.4).move_to(card_recs[3].get_bottom() + UP * 0.4)
        c4_visual = Star(color=ACCENT_MINT).scale(0.1).next_to(c4_title, RIGHT, buff=0.15)
        card_contents.add(VGroup(c4_title, c4_desc, c4_visual))

        # Animate grid appearance sequentially with delays (LaggedStart equivalent)
        for i in range(4):
            self.play(
                FadeIn(card_recs[i], shift=UP * 0.25),
                FadeIn(card_contents[i], shift=UP * 0.2),
                FadeIn(card_glows[i]),
                run_time=0.7
            )
            self.wait(0.2)

        # Subtitle 9 (66s - 80s)
        update_sub("Đây là lý do EBGM 'nhìn' giống cách bộ não chúng ta nhìn", 10.0)
        self.wait(2.2)

        # Cleanup at the end
        self.play(
            FadeOut(title),
            FadeOut(card_recs),
            FadeOut(card_contents),
            FadeOut(VGroup(*card_glows)),
            run_time=1.0
        )
        self.wait(0.3)
