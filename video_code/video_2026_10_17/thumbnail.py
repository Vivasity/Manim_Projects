from manim import *

config.background_color = "#000012"  # 设置Scene背景颜色
config.frame_rate = 1
config.save_last_frame = True

# 生成视频封面
class Thumbnail(Scene):
    def construct(self):
        radius = 1.8
        left_center = LEFT * 3
        right_center = RIGHT * 3

        # 左侧：连续的渐变圆环
        arc_count = 240
        continuous_circle = VGroup()

        for i in range(arc_count):
            theta = TAU * i / arc_count
            alpha = (np.cos(theta) + 1) / 2
            color = interpolate_color(BLUE_B, GREEN_B, alpha)
            arc = Arc(
                radius = radius, start_angle = theta, angle = TAU / arc_count + 0.002,
                stroke_color = color, stroke_width = 14
            ).shift(left_center)
            continuous_circle.add(arc)
        
        continuous_circle.shift(DOWN * 0.72)

        # 右侧：由散点组成的渐变圆
        dot_count = 24
        dotted_circle = VGroup()

        for i in range(dot_count):
            theta = TAU * i / dot_count
            alpha = (np.cos(theta) + 1) / 2
            color = interpolate_color(BLUE_B, GREEN_B, alpha)
            position = right_center + radius * np.array([np.cos(theta), np.sin(theta), 0])
            dot = Dot(point = position, radius = 0.11, color = color)
            dotted_circle.add(dot)

        dotted_circle.shift(DOWN * 0.72)

        # 向上的白色箭头
        left_arrow = Arrow(
            start = left_center + UP * 1.5, end = left_center + UP * 2.1,
            buff = 0, color = WHITE, stroke_width = 12, tip_length = 0.25
        )
        right_arrow = Arrow(
            start = right_center + UP * 1.5, end = right_center + UP * 2.1,
            buff = 0, color = WHITE, stroke_width = 12, tip_length = 0.25
        )

        self.add(continuous_circle, dotted_circle, left_arrow, right_arrow)
