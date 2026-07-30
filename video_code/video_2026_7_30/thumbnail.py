from manim import *
import math

config.background_color = "#000012"  # 设置Scene背景颜色
config.frame_rate = 1
config.save_last_frame = True

# 生成视频封面
class Thumbnail(Scene):
    def construct(self):
        axis0 = NumberLine(
            x_range = [-6, 6, 2], length = 12, include_ticks = True, include_numbers = False, include_tip = False,
            tick_size = 0.1, color = GREY_B, stroke_width = 3.2, font_size = 36, label_direction = DOWN, line_to_number_buff = 0.24
        ).shift(2.8 * UP)
        axis1 = NumberLine(
            x_range = [-6, 6, 2], length = 12, include_ticks = True, include_numbers = False, include_tip = False,
            tick_size = 0.1, color = GREY_B, stroke_width = 3.2, font_size = 36, label_direction = DOWN, line_to_number_buff = 0.24
        ).shift(1.8 * UP)
        axis2 = NumberLine(
            x_range = [-6, 6, 2], length = 12, include_ticks = True, include_numbers = False, include_tip = False,
            tick_size = 0.1, color = GREY_B, stroke_width = 3.2, font_size = 36, label_direction = DOWN, line_to_number_buff = 0.24
        ).shift(0.8 * UP)
        axis3 = NumberLine(
            x_range = [-6, 6, 2], length = 12, include_ticks = True, include_numbers = False, include_tip = False,
            tick_size = 0.1, color = GREY_B, stroke_width = 3.2, font_size = 36, label_direction = DOWN, line_to_number_buff = 0.24
        ).shift(0.2 * DOWN)
        cdots = MathTex(r"\cdots", font_size = 96).shift(1.1 * DOWN)
        axis4 = NumberLine(
            x_range = [-6, 6, 2], length = 12, include_ticks = True, include_numbers = False, include_tip = False,
            tick_size = 0.1, color = GREY_B, stroke_width = 3.2, font_size = 36, label_direction = DOWN, line_to_number_buff = 0.24
        ).shift(2 * DOWN)
        axis = VGroup(axis0, axis1, axis2, axis3, axis4)
        interval0 = Line(axis0.n2p(-1.6), axis0.n2p(3.6), color = RED_C, stroke_width = 8)
        interval_label0 = MathTex(r"U_1", color = RED_C, font_size = 48).move_to(axis0.n2p(1) + 0.4 * UP)
        interval1 = Line(axis1.n2p(-0.4), axis1.n2p(3.2), color = BLUE_C, stroke_width = 8)
        interval_label1 = MathTex(r"V_1", color = BLUE_C, font_size = 48).move_to(axis1.n2p(1.4) + 0.4 * UP)
        interval2 = Line(axis2.n2p(1.2), axis2.n2p(3), color = RED_B, stroke_width = 8)
        interval_label2 = MathTex(r"U_2", color = RED_B, font_size = 48).move_to(axis2.n2p(2.1) + 0.4 * UP)
        interval3 = Line(axis3.n2p(1.8), axis3.n2p(2.8), color = BLUE_B, stroke_width = 8)
        interval_label3 = MathTex(r"V_2", color = BLUE_B, font_size = 48).move_to(axis3.n2p(2.3) + 0.4 * UP)
        interval = VGroup(interval0, interval1, interval2, interval3)
        interval_label = VGroup(interval_label0, interval_label1, interval_label2, interval_label3)
        x_dot = Dot(color = YELLOW).move_to(axis4.n2p(math.sqrt(5)))
        x_label = MathTex(r"x \in \overline{\mathbb{Q}}", color = YELLOW, font_size = 64).move_to(axis4.n2p(math.sqrt(5)) + 0.6 * UP)
        dot = VGroup(x_dot, x_label)
        self.add(axis, cdots, interval, interval_label, dot)
        self.wait(0.1)
