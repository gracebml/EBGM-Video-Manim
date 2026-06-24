"""
Common configuration and helper functions for EBGM Video.
Toàn bộ text dùng LaTeX thuần (Latin Modern Roman) qua XeLaTeX.
"""

from manim import *
import numpy as np

# ============================================================
# COLOR PALETTE — Cool & Premium Tone
# ============================================================
BG_NAVY         = "#0D1B2A"   # Main background
BG_NAVY_SOFT    = "#1B263B"   # Panel/Card background

TEXT_PRIMARY    = "#E0E1DD"   # Main text color
TEXT_MUTED      = "#A9B4C2"   # Dimmed secondary text

# Accent colors (cool tone)
ACCENT_CYAN     = "#48CAE4"   # Main highlight cyan
ACCENT_TEAL     = "#76C5BF"   # Soft teal
ACCENT_BLUE     = "#778DA9"   # Secondary blue-grey
ACCENT_MINT     = "#95D5B2"   # Mint green for "Correct" / "Advantages"
ACCENT_LAVENDER = "#B8B5FF"   # Signature lavender for EBGM, Bunch Graph
ACCENT_CORAL    = "#E29578"   # Coral muted for "Wrong" / "Limitations"

# ============================================================
# LATEX TEMPLATE — XeLaTeX + Latin Modern (hỗ trợ tiếng Việt)
# ============================================================
VN_TEX_TEMPLATE = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    documentclass=r"\documentclass[preview]{standalone}",
    preamble=r"""
\usepackage{fontspec}
\usepackage{polyglossia}
\setdefaultlanguage{vietnamese}
\setmainfont{Latin Modern Roman}
\setsansfont{Latin Modern Sans}
\setmonofont{Latin Modern Mono}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{mathtools}
\usepackage{unicode-math}
\setmathfont{Latin Modern Math}
"""
)

# ============================================================
# TEXT HELPERS — Mọi text đều qua LaTeX (Latin Modern Roman)
# ============================================================
def vn_tex(text_str, color=None, scale=1.0):
    """
    Render chuỗi bất kỳ (tiếng Việt hoặc Anh) qua XeLaTeX,
    font Latin Modern Roman. Trả về Tex mobject.
    """
    color = color or TEXT_PRIMARY
    obj = Tex(text_str, tex_template=VN_TEX_TEMPLATE, color=color)
    if scale != 1.0:
        obj.scale(scale)
    return obj

def vn_tex_bold(text_str, color=None, scale=1.0):
    """Bold variant."""
    color = color or TEXT_PRIMARY
    obj = Tex(r"\textbf{" + text_str + "}", tex_template=VN_TEX_TEMPLATE, color=color)
    if scale != 1.0:
        obj.scale(scale)
    return obj

def vn_tex_italic(text_str, color=None, scale=1.0):
    """Italic variant."""
    color = color or TEXT_PRIMARY
    obj = Tex(r"\textit{" + text_str + "}", tex_template=VN_TEX_TEMPLATE, color=color)
    if scale != 1.0:
        obj.scale(scale)
    return obj

def vn_tex_mono(text_str, color=None, scale=1.0):
    """Monospace variant (Latin Modern Mono)."""
    color = color or TEXT_PRIMARY
    obj = Tex(r"\texttt{" + text_str + "}", tex_template=VN_TEX_TEMPLATE, color=color)
    if scale != 1.0:
        obj.scale(scale)
    return obj

def vn_math(latex_str, color=None, scale=1.0):
    """MathTex with Vietnamese template."""
    color = color or TEXT_PRIMARY
    obj = MathTex(latex_str, tex_template=VN_TEX_TEMPLATE, color=color)
    if scale != 1.0:
        obj.scale(scale)
    return obj

# ============================================================
# SUBTITLE & TITLE HELPERS
# ============================================================
def make_subtitle(text_str, scale=0.55, color=None):
    """
    Phụ đề với viền bo tròn bán trong suốt ở mép dưới màn hình.
    Text bằng LaTeX (Latin Modern Roman).
    """
    # Subtitles are disabled for the release render. Keep returning an invisible
    # mobject so existing FadeIn/ReplacementTransform calls preserve timing.
    return VGroup(Dot(ORIGIN, radius=0.001, fill_opacity=0, stroke_opacity=0))

def section_title(text_str, color=None, scale=0.9):
    """Tiêu đề section — LaTeX bold."""
    color = color or ACCENT_CYAN
    return vn_tex_bold(text_str, color=color, scale=scale)

def cool_glow(mob, color=ACCENT_CYAN):
    """Adds a soft glowing duplicate outline to a mobject."""
    return mob.copy().set_stroke(color, width=8, opacity=0.3)

# ============================================================
# TECHNICAL COLORS & CONSTANTS FOR PART 2 (ALGORITHM DETAIL)
# ============================================================
GABOR_REAL    = "#48CAE4"   # cyan cho phần real của Gabor wavelet
GABOR_IMAG    = "#B8B5FF"   # lavender cho phần imaginary
JET_GLOW      = "#76C5BF"   # teal glow cho jet
GRID_LINE     = "#778DA9"   # blue-grey cho lưới grid mờ
HIGHLIGHT_HOT = "#FCBF49"   # vàng ấm RẤT THƯA THỚT, chỉ dùng nhấn mạnh focus điểm

# Math constants
FONT_MATH_SCALE = 0.8

# Font settings for Text Mobject
SUBTITLE_FONT   = "Be Vietnam Pro"
TITLE_FONT      = "EB Garamond"
MONO_FONT       = "JetBrains Mono"

# ============================================================
# PART 2 HELPERS
# ============================================================
def make_jet_visual(n_freq=5, n_orient=8, scale=1.0, color=GABOR_REAL):
    """
    Visualize jet: 40 wavelets xếp theo lưới (n_freq hàng x n_orient cột).
    Mỗi ô là 1 mini Gabor wavelet pattern.
    """
    grid = VGroup()
    for nu in range(n_freq):
        for mu in range(n_orient):
            kx = np.cos(mu * np.pi / n_orient)
            ky = np.sin(mu * np.pi / n_orient)
            freq = 0.5 + nu * 0.3
            wavelet = ParametricFunction(
                lambda t, kx=kx, freq=freq: np.array([
                    t * 0.3,
                    0.15 * np.sin(freq * t * 8) * np.exp(-(t**2)/0.5),
                    0
                ]),
                t_range=[-0.8, 0.8],
                color=color, stroke_width=1.2
            ).rotate(mu * np.pi / n_orient)
            wavelet.move_to([mu * 0.4 - 1.5, nu * 0.4 - 0.8, 0])
            grid.add(wavelet)
    return grid.scale(scale)

def make_face_graph_node(pos, jet_size=0.15, color=ACCENT_LAVENDER):
    """Một node trên image graph: chấm trung tâm + ring + mini jet."""
    return VGroup(
        Dot(pos, radius=0.06, color=color),
        Circle(radius=jet_size, color=color, stroke_width=1.5).move_to(pos),
    )

def vietnamese_label(text_str, scale=0.45, color=None):
    """Nhãn tiếng Việt nhỏ, dùng cho chú thích."""
    color = color or TEXT_MUTED
    return Text(text_str, font=SUBTITLE_FONT, color=color, weight="LIGHT").scale(scale)
