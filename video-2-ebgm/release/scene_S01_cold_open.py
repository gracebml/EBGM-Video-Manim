import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
import numpy as np
from _common import *


class S01_ColdOpen(MovingCameraScene):
    SCENE_KEY = "scene_01"

    def construct(self):
        T = load_scene_timing(self.SCENE_KEY)
        self.add_sound(T["audio_path"])
        self.camera.background_color = BG_NAVY

        elapsed = 0.0

        def beat_to(t_target, *anims, **kw):
            nonlocal elapsed
            rt = max(0.2, t_target - elapsed)
            if anims:
                self.play(*anims, run_time=rt, **kw)
            else:
                self.wait(rt)
            elapsed = t_target

        def tiny_person(color=ACCENT_BLUE):
            head = Circle(radius=0.18, color=color, stroke_width=2, fill_opacity=0.08)
            body = Line(DOWN * 0.15, DOWN * 0.95, color=color, stroke_width=3)
            legs = VGroup(
                Line(DOWN * 0.95, DOWN * 1.35 + LEFT * 0.18, color=color, stroke_width=2),
                Line(DOWN * 0.95, DOWN * 1.35 + RIGHT * 0.18, color=color, stroke_width=2),
            )
            return VGroup(head, body, legs)

        def mini_face(color=ACCENT_BLUE):
            face = Ellipse(width=1.2, height=1.55, color=color, stroke_width=2, fill_opacity=0.04)
            eyes = VGroup(
                Dot(LEFT * 0.22 + UP * 0.18, radius=0.04, color=color),
                Dot(RIGHT * 0.22 + UP * 0.18, radius=0.04, color=color),
            )
            nose = Line(UP * 0.15, DOWN * 0.12, color=color, stroke_width=2)
            mouth = Arc(radius=0.2, start_angle=210 * DEGREES, angle=120 * DEGREES, color=color, stroke_width=2).shift(DOWN * 0.38)
            return VGroup(face, eyes, nose, mouth)

        horizon = Line(LEFT * 7, RIGHT * 7, color=ACCENT_BLUE, stroke_width=1.2).shift(DOWN * 1.55).set_opacity(0.25)
        buildings = VGroup()
        for i, x in enumerate([-6.0, -4.25, -2.75, 3.95, 5.85]):
            h = 1.15 + 0.25 * ((i * 2) % 4)
            building = Rectangle(
                width=0.95,
                height=h,
                color=ACCENT_BLUE,
                stroke_width=0.8,
                fill_color=BG_NAVY_SOFT,
                fill_opacity=0.16,
            ).move_to([x, -1.55 + h / 2, 0])
            building.set_opacity(0.10)
            buildings.add(building)
        window_glints = VGroup()
        for x, y in [(-5.9, -0.3), (-4.25, 0.25), (4.05, -0.15), (5.85, 0.38)]:
            window_glints.add(Square(side_length=0.11, color=ACCENT_BLUE, stroke_width=0.8).move_to([x, y, 0]).set_opacity(0.10))

        person_a = tiny_person(ACCENT_CYAN).scale(1.15).move_to(LEFT * 3.25 + DOWN * 0.16)
        person_b = tiny_person(ACCENT_LAVENDER).scale(1.15).move_to(RIGHT * 3.25 + DOWN * 0.16)
        face_b = mini_face(ACCENT_LAVENDER).move_to(person_b[0].get_center())
        face_b.scale(0.48)
        person_b[0].become(face_b[0])

        recog_t = word_start(T, "recogn") or 3.5
        self.add(horizon, buildings, window_glints, person_a, person_b)
        beat_to(
            recog_t,
            person_a.animate.move_to(LEFT * 2.05 + DOWN * 0.16),
            person_b.animate.move_to(RIGHT * 2.05 + DOWN * 0.16),
            buildings.animate.shift(LEFT * 0.08).set_opacity(0.10),
            window_glints.animate.set_opacity(0.10),
            rate_func=linear,
        )

        gaze_path = Line(
            person_a[0].get_center() + RIGHT * 0.14,
            person_b[0].get_center() + LEFT * 0.14,
            color=ACCENT_LAVENDER,
            stroke_width=4.0,
        )
        gaze_glow = gaze_path.copy().set_stroke(ACCENT_LAVENDER, width=10, opacity=0.18)
        spark = Dot(gaze_path.get_start(), radius=0.075, color=ACCENT_MINT)
        self.play(Create(gaze_glow), Create(gaze_path), run_time=0.38, rate_func=linear)
        elapsed += 0.38
        self.play(MoveAlongPath(spark, gaze_path), run_time=0.42, rate_func=smooth)
        elapsed += 0.42

        pulse = Circle(radius=0.36, color=ACCENT_MINT, stroke_width=3.2).move_to(person_b[0].get_center())
        recognized = en_label("Recognized!", color=ACCENT_MINT, scale=0.6, bold=True)
        recognized.move_to(UP * 1.25)
        self.play(
            GrowFromCenter(pulse),
            pulse.animate.scale(1.85).set_opacity(0),
            person_b[0].animate.scale(1.18),
            run_time=0.36,
            rate_func=smooth,
        )
        elapsed += 0.36
        self.play(
            FadeIn(recognized, scale=0.8),
            person_b[0].animate.scale(1 / 1.18),
            self.camera.frame.animate.scale(0.92).move_to(person_b.get_center()),
            run_time=max(0.2, seg_end(T, 0) - elapsed),
            rate_func=smooth,
        )
        elapsed = seg_end(T, 0)

        face_image = ImageMobject(FACE_PATH)
        face_image.height = 4.3
        face_image.move_to(ORIGIN)
        image_frame = RoundedRectangle(width=6.6, height=4.55, corner_radius=0.12, color=ACCENT_BLUE, stroke_width=1.5)
        image_frame.set_opacity(0.45)

        beat_to(
            T["segments"][1]["start"],
            FadeOut(gaze_glow),
            FadeOut(gaze_path),
            FadeOut(spark),
            FadeOut(pulse),
            FadeOut(recognized),
            person_a.animate.set_opacity(0.62),
            person_b.animate.set_opacity(0.70),
            rate_func=smooth,
        )
        beat_to(
            seg_end(T, 1),
            FadeOut(person_a),
            FadeOut(person_b),
            FadeOut(buildings),
            FadeOut(window_glints),
            FadeOut(horizon),
            self.camera.frame.animate.move_to(ORIGIN).set(width=config.frame_width),
            FadeIn(face_image),
            Create(image_frame),
        )

        landmark_points = [
            LEFT * 0.85 + UP * 0.55,
            LEFT * 0.35 + UP * 0.6,
            RIGHT * 0.35 + UP * 0.58,
            RIGHT * 0.85 + UP * 0.55,
            UP * 0.1,
            LEFT * 0.42 + DOWN * 0.58,
            RIGHT * 0.42 + DOWN * 0.58,
        ]
        landmarks = VGroup(*[Dot(p, radius=0.045, color=ACCENT_LAVENDER) for p in landmark_points])
        landmark_edges = VGroup(*[
            Line(landmarks[i].get_center(), landmarks[j].get_center(), color=ACCENT_LAVENDER, stroke_width=1.5).set_opacity(0.55)
            for i, j in [(0, 1), (1, 4), (4, 2), (2, 3), (4, 5), (4, 6), (5, 6)]
        ])
        teaser = VGroup(landmark_edges, landmarks)

        beat_to(
            T["segments"][2]["start"],
            LaggedStart(*[GrowFromCenter(d) for d in landmarks], Create(landmark_edges), lag_ratio=0.08),
            face_image.animate.set_opacity(0.86),
        )

        mini = mini_face(ACCENT_BLUE).scale(0.55).move_to(UP * 2.0)
        trunk = Line(UP * 1.22, UP * 0.6, color=ACCENT_BLUE, stroke_width=2)
        left_branch = Line(UP * 0.6, LEFT * 3.25 + UP * 0.6, color=ACCENT_CYAN, stroke_width=2)
        right_branch = Line(UP * 0.6, RIGHT * 3.25 + UP * 0.6, color=ACCENT_LAVENDER, stroke_width=2)
        two_branches = en_label("Two branches", color=TEXT_PRIMARY, scale=0.55, bold=True).move_to(UP * 2.85)

        beat_to(
            seg_end(T, 2),
            FadeOut(teaser),
            FadeOut(face_image),
            FadeOut(image_frame),
            FadeIn(mini, shift=DOWN * 0.08),
            Create(trunk),
            Create(left_branch),
            Create(right_branch),
            FadeIn(two_branches, shift=DOWN * 0.08),
        )

        left_card = RoundedRectangle(width=4.4, height=2.45, corner_radius=0.12, color=ACCENT_CYAN, stroke_width=1.6)
        left_card.move_to(LEFT * 3.2 + DOWN * 0.65)
        left_title = en_label("Verification 1:1", color=ACCENT_CYAN, scale=0.48, bold=True).move_to(left_card.get_top() + DOWN * 0.38)
        phone = VGroup(
            RoundedRectangle(width=0.78, height=1.35, corner_radius=0.11, color=ACCENT_TEAL, stroke_width=2),
            Circle(radius=0.18, color=ACCENT_MINT, stroke_width=2).shift(UP * 0.08),
            MathTex(r"\checkmark", color=ACCENT_MINT).scale(0.55).shift(UP * 0.08),
        ).move_to(left_card.get_center() + DOWN * 0.12)
        owner = en_label("phone owner?", color=TEXT_MUTED, scale=0.34).move_to(left_card.get_bottom() + UP * 0.32)

        beat_to(
            seg_end(T, 3),
            Create(left_card),
            FadeIn(left_title, shift=DOWN * 0.08),
            FadeIn(phone, shift=UP * 0.08),
        )
        beat_to(
            seg_end(T, 4),
            FadeIn(owner, shift=UP * 0.05),
            Indicate(phone[2], color=ACCENT_MINT),
            left_card.animate.set_stroke(ACCENT_CYAN, width=2.4),
        )

        right_card = RoundedRectangle(width=4.4, height=2.45, corner_radius=0.12, color=ACCENT_LAVENDER, stroke_width=1.6)
        right_card.move_to(RIGHT * 3.2 + DOWN * 0.65)
        right_title = en_label("Identification 1:N", color=ACCENT_LAVENDER, scale=0.46, bold=True).move_to(right_card.get_top() + DOWN * 0.38)
        gallery = VGroup()
        for r in range(3):
            for c in range(5):
                item = mini_face(ACCENT_BLUE).scale(0.12)
                item.move_to(right_card.get_center() + LEFT * 1.1 + RIGHT * c * 0.55 + UP * (0.42 - r * 0.42))
                item.set_opacity(0.55)
                gallery.add(item)
        probe = mini_face(ACCENT_CYAN).scale(0.18).move_to(right_card.get_center() + LEFT * 1.65)
        ray = thin_arrow(
            probe.get_right() + RIGHT * 0.05,
            gallery[7].get_left() + LEFT * 0.05,
            color=ACCENT_CYAN,
            buff=0.05,
            stroke_width=2.4,
            max_tip_length_to_length_ratio=0.08,
        )

        beat_to(
            seg_end(T, 5),
            Create(right_card),
            FadeIn(right_title, shift=DOWN * 0.08),
            FadeIn(probe),
            LaggedStart(*[FadeIn(g) for g in gallery], lag_ratio=0.025),
        )

        target_ring = SurroundingRectangle(gallery[7], color=ACCENT_LAVENDER, buff=0.06, stroke_width=2.2)
        among = en_label("among millions", color=TEXT_MUTED, scale=0.33).move_to(right_card.get_bottom() + UP * 0.32)
        beat_to(
            seg_end(T, 6),
            Create(ray),
            Create(target_ring),
            FadeIn(among, shift=UP * 0.05),
            Indicate(gallery[7], color=ACCENT_LAVENDER),
        )

        final_box = RoundedRectangle(width=3.25, height=0.78, corner_radius=0.12, color=ACCENT_LAVENDER, stroke_width=2.2, fill_color=ACCENT_LAVENDER, fill_opacity=0.08)
        final_text = en_label("1:N Identification", color=ACCENT_LAVENDER, scale=0.5, bold=True)
        final_text.move_to(final_box.get_center())
        final_badge = VGroup(final_box, final_text)
        final_badge.move_to(DOWN * 2.55)

        beat_to(
            seg_end(T, 7),
            left_card.animate.set_opacity(0.26),
            left_title.animate.set_opacity(0.35),
            phone.animate.set_opacity(0.25),
            owner.animate.set_opacity(0.25),
            right_card.animate.set_stroke(ACCENT_LAVENDER, width=3.0),
            FadeIn(final_badge, shift=UP * 0.1),
        )
        beat_to(
            seg_end(T, 8),
            Indicate(final_badge, color=ACCENT_LAVENDER),
            right_title.animate.scale(1.04),
            target_ring.animate.set_stroke(ACCENT_LAVENDER, width=3.5),
        )

        tail = max(0.0, T["duration"] - elapsed - 0.33)
        if tail > 0.05:
            self.wait(tail)
