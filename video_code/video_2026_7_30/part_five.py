from manim import *

config.background_color = "#000012"  # 设置Scene背景颜色

# 中文文字模板
CHINESE_TEMPLATE = TexTemplate()
CHINESE_TEMPLATE.tex_compiler = "xelatex"
CHINESE_TEMPLATE.output_format = ".xdv"
CHINESE_TEMPLATE.add_to_preamble(r"\usepackage[UTF8]{ctex}")

# 展示一些无处稠密集
class NowhereDenseSet(Scene):
    def construct(self):
        # 可调参数
        NUMBER_LINE_RANGE, NUMBER_LINE_LENGTH = [-4, 4, 1], 16
        NUMBER_LINE_COLOR, NUMBER_LINE_WIDTH, NUMBER_FONT_SIZE = GREY_B, 3.2, 36

        SET_POINT_X, SET_POINT_RADIUS, SET_POINT_COLOR = 0.45, 0.08, YELLOW
        SET_LABEL, SET_LABEL_SCALE, SET_LABEL_BUFF = r"S", 0.8, 0.18

        INITIAL_INTERVAL = (-3.2, 3.2)
        SHRINK_INTERVALS = [(-1.4, 2.1), (-0.3, 1.25)]
        AVOIDING_INTERVALS = [(0.8, 2.6), (-1.0, 0.1), (0.65, 1.05)]

        MAIN_SEGMENT_COLOR, MAIN_SEGMENT_WIDTH = TEAL, 8
        AVOIDING_SEGMENT_COLOR, AVOIDING_SEGMENT_WIDTH = GREEN, 11

        INTEGER_COLOR, INTEGER_DOT_RADIUS = YELLOW, 0.08
        FLASH_COLOR, FLASH_RADIUS, FLASH_LINE_LENGTH, FLASH_NUM_LINES = YELLOW_A, 0.36, 0.18, 12

        NUMBER_LINE_TIME, SET_POINT_TIME, INITIAL_SEGMENT_TIME = 1.5, 0.7, 1.0
        AVOIDING_SEGMENT_TIME, SHRINK_TIME, STEP_WAIT_TIME = 0.7, 0.8, 0.9
        SET_FLASH_TIME, INTEGER_CREATE_TIME, INTEGER_CREATE_LAG = 0.7, 1.0, 0.08
        INTEGER_FLASH_TIME, WAIT_BEFORE_INTEGERS, FINAL_WAIT_TIME = 1.6, 0.8, 2.0

        numberline = NumberLine(
            x_range = NUMBER_LINE_RANGE, length = NUMBER_LINE_LENGTH, include_ticks = True, include_numbers = True, include_tip = False,
            tick_size = 0.1, color = NUMBER_LINE_COLOR, stroke_width = NUMBER_LINE_WIDTH, font_size = NUMBER_FONT_SIZE,
            label_direction = DOWN, line_to_number_buff = 0.24
        ).set_z_index(0)

        self.play(Create(numberline), run_time = NUMBER_LINE_TIME)

        # 黄色点 S
        set_point = Dot(point = numberline.n2p(SET_POINT_X), radius = SET_POINT_RADIUS, color = SET_POINT_COLOR).set_z_index(6)

        set_label = MathTex(
            SET_LABEL, color = YELLOW_A
        ).scale(SET_LABEL_SCALE).next_to(set_point, UP, buff = SET_LABEL_BUFF).set_z_index(6)
        self.play(GrowFromCenter(set_point), Write(set_label), run_time = SET_POINT_TIME)

        # TEAL 线段的两个端点
        left_tracker = ValueTracker(INITIAL_INTERVAL[0])
        right_tracker = ValueTracker(INITIAL_INTERVAL[1])

        main_segment = always_redraw(
            lambda: Line(
                start = numberline.n2p(left_tracker.get_value()), end = numberline.n2p(right_tracker.get_value()),
                color = MAIN_SEGMENT_COLOR, stroke_width = MAIN_SEGMENT_WIDTH
            ).set_z_index(2)
        )
        self.play(Create(main_segment),run_time = INITIAL_SEGMENT_TIME)
        self.wait(STEP_WAIT_TIME)

        # 第一次生成不含 S 的线段
        first_avoiding_segment = Line(
            start = numberline.n2p(AVOIDING_INTERVALS[0][0]), end = numberline.n2p(AVOIDING_INTERVALS[0][1]),
            color = AVOIDING_SEGMENT_COLOR, stroke_width = AVOIDING_SEGMENT_WIDTH
        ).set_z_index(3)

        self.play(Create(first_avoiding_segment), run_time = AVOIDING_SEGMENT_TIME)
        self.wait(STEP_WAIT_TIME)

        # TEAL 线段缩小，但仍然包含 S
        self.play(
            left_tracker.animate.set_value(SHRINK_INTERVALS[0][0]), right_tracker.animate.set_value(SHRINK_INTERVALS[0][1]),
            FadeOut(first_avoiding_segment), run_time = SHRINK_TIME, rate_func = smooth
        )
        self.wait(STEP_WAIT_TIME)

        # 在缩小后的 TEAL 线段内重新生成不含 S 的线段
        second_avoiding_segment = Line(
            start = numberline.n2p(AVOIDING_INTERVALS[1][0]), end = numberline.n2p(AVOIDING_INTERVALS[1][1]),
            color = AVOIDING_SEGMENT_COLOR, stroke_width = AVOIDING_SEGMENT_WIDTH
        ).set_z_index(3)

        self.play(Create(second_avoiding_segment), run_time = AVOIDING_SEGMENT_TIME)
        self.wait(STEP_WAIT_TIME)

        # 再次缩小，TEAL 线段仍然包含 S
        self.play(
            left_tracker.animate.set_value(SHRINK_INTERVALS[1][0]), right_tracker.animate.set_value(SHRINK_INTERVALS[1][1]),
            FadeOut(second_avoiding_segment), run_time = SHRINK_TIME, rate_func = smooth
        )
        self.wait(STEP_WAIT_TIME)

        # 再次生成一条不含 S 的线段
        third_avoiding_segment = Line(
            start = numberline.n2p(AVOIDING_INTERVALS[2][0]), end = numberline.n2p(AVOIDING_INTERVALS[2][1]),
            color = AVOIDING_SEGMENT_COLOR, stroke_width = AVOIDING_SEGMENT_WIDTH
        ).set_z_index(3)

        self.play(Create(third_avoiding_segment), run_time = AVOIDING_SEGMENT_TIME)
        self.wait(STEP_WAIT_TIME)

        # S 点闪烁
        self.play(
            Flash(
                set_point.get_center(), color = FLASH_COLOR, flash_radius = FLASH_RADIUS,
                line_length = FLASH_LINE_LENGTH, num_lines = FLASH_NUM_LINES
            ), run_time = SET_FLASH_TIME
        )

        self.wait(WAIT_BEFORE_INTEGERS)

        # 同时标出所有整数点
        integer_values = range(NUMBER_LINE_RANGE[0], NUMBER_LINE_RANGE[1] + 1)

        integer_dots = VGroup(
            *[
                Dot(
                    point = numberline.n2p(integer), radius = INTEGER_DOT_RADIUS, color = INTEGER_COLOR
                ).set_z_index(7)
                for integer in integer_values
            ]
        )
        self.play(
            LaggedStart(
                *[GrowFromCenter(dot) for dot in integer_dots], lag_ratio = INTEGER_CREATE_LAG
            ), run_time = INTEGER_CREATE_TIME
        )
        self.wait(STEP_WAIT_TIME)
        self.play(
            LaggedStart(
                *[
                    Flash(
                        dot.get_center(), color = FLASH_COLOR, flash_radius = FLASH_RADIUS,
                        line_length = FLASH_LINE_LENGTH, num_lines = FLASH_NUM_LINES
                    )
                    for dot in integer_dots
                ], lag_ratio = 0.35
            ), run_time = INTEGER_FLASH_TIME
        )
        self.wait(FINAL_WAIT_TIME)

# 展示Cantor集
class CantorSet(Scene):
    def construct(self):
        # 可调参数
        LEVELS, SEGMENT_LENGTH, TOP_Y = 7, 12.0, 3.0
        LEVEL_SPACING, SEGMENT_COLOR, STROKE_WIDTH = 0.85, YELLOW, 8
        FIRST_RUN_TIME, LEVEL_RUN_TIME = 1.2, 0.8
        CHILD_LAG_RATIO, FINAL_WAIT_TIME = 0.015, 2.0

        left_x = -SEGMENT_LENGTH / 2
        right_x = SEGMENT_LENGTH / 2
        first_segment = Line(
            start = [left_x, TOP_Y, 0], end = [right_x, TOP_Y, 0], color = SEGMENT_COLOR,
            stroke_width = STROKE_WIDTH
        )
        self.play(Create(first_segment), run_time = FIRST_RUN_TIME)
        self.wait(0.3)
        current_intervals = [(left_x, right_x)]
        current_segments = [first_segment]

        for level in range(1, LEVELS):
            new_y = TOP_Y - level * LEVEL_SPACING
            next_intervals = []
            next_segments = []
            animations = []

            for (start_x, end_x), parent_segment in zip(current_intervals, current_segments):
                third = (end_x - start_x) / 3
                left_interval = (start_x, start_x + third)
                right_interval = (end_x - third, end_x)
                left_segment = Line(
                    start = [left_interval[0], new_y, 0], end = [left_interval[1], new_y, 0], color = SEGMENT_COLOR,
                    stroke_width = STROKE_WIDTH
                )
                right_segment = Line(
                    start = [right_interval[0], new_y, 0], end = [right_interval[1], new_y, 0], color = SEGMENT_COLOR,
                    stroke_width = STROKE_WIDTH
                )
                animations.extend([TransformFromCopy(parent_segment, left_segment), TransformFromCopy(parent_segment, right_segment)])
                next_intervals.extend([left_interval, right_interval])
                next_segments.extend([left_segment, right_segment])

            self.play(LaggedStart(*animations, lag_ratio = CHILD_LAG_RATIO), run_time = LEVEL_RUN_TIME)
            current_intervals = next_intervals
            current_segments = next_segments

        self.wait(0.3)
        self.play(Write(MathTex(r"\cdots", font_size = 54).next_to(VGroup(*current_segments), DOWN, buff = 0.35)))
        self.wait(FINAL_WAIT_TIME)

# 有理数集是可列个单点集的并
class RationalNumberSet(Scene):
    def construct(self):
        q_label = MathTex(r"\mathbb{Q}", font_size = 150, color = YELLOW_A)
        q_formula = MathTex(r"= \bigcup_{n=1}^{\infty } \{q_n\}", font_size = 100, color = YELLOW_A).shift(0.9 * RIGHT)
        self.play(Create(q_label))
        self.wait(0.4)
        self.play(Write(q_formula), q_label.animate.shift(2.5 * LEFT), run_time = 1.6)
        self.wait(2.5)

# 实数集是可列个无处稠密集的并吗？
class RealNumberSet(Scene):
    def construct(self):
        r_label = MathTex(r"\mathbb{R}", font_size = 150, color = YELLOW_A)
        r_formula = MathTex(r"= \bigcup_{n=1}^{\infty } \{A_n\}", font_size = 100, color = YELLOW_A).shift(0.9 * RIGHT)
        self.play(Create(r_label))
        self.wait(0.4)
        self.play(Write(r_formula), r_label.animate.shift(2.5 * LEFT), run_time = 1.6)
        self.wait(0.4)
        question = Tex("?", font_size = 160, color = RED).shift(1.2 * LEFT)
        self.play(FadeIn(question, shift = 0.1 * UP), run_time = 1.2)
        self.wait()
        x_formula = MathTex(r"x\notin \mathbb{R}", font_size = 72, color = YELLOW).shift(1.6 * DOWN)
        r = VGroup(r_label, r_formula, question)
        self.play(r.animate.shift(1 * UP), run_time = 0.8)
        self.play(Write(x_formula))
        self.wait(0.5)
        label = Tex("矛盾！", tex_template = CHINESE_TEMPLATE, color = RED, font_size = 72).shift(1.6 * DOWN + 3 * RIGHT)
        self.play(Write(label))
        self.wait()
        ar_formula = MathTex(r"\neq \bigcup_{n=1}^{\infty } \{A_n\}", font_size = 100, color = YELLOW_A).shift(0.9 * RIGHT + 1 * UP)
        self.play(ReplacementTransform(r_formula, ar_formula), FadeOut(question), run_time = 1.2)
        self.wait(2.5)

# R上的Baire纲定理
class BaireTheoremInR(Scene):
    def construct(self):
        theorem = MathTex(r"\mathbb{R}\text{不是可数个无处稠密集的并}", tex_template = CHINESE_TEMPLATE, color = YELLOW_A, font_size = 72)
        self.play(Write(theorem), run_time = 1.2)
        self.wait(2)

# Baire纲定理
class BaireTheorem(Scene):
    def construct(self):
        theorem0 = MathTex(r"X\text{是非空完备度量空间}", tex_template = CHINESE_TEMPLATE, color = YELLOW_A, font_size = 72).shift(1.3 * UP)
        arrow = MathTex(r"\Downarrow ", font_size = 80, color = YELLOW_A)
        theorem1 = MathTex(r"X\text{不是第一纲集}", tex_template = CHINESE_TEMPLATE, color = YELLOW_A, font_size = 72).shift(1.3 * DOWN)
        self.play(Write(theorem0), run_time = 0.9)
        self.play(Create(arrow), run_time = 0.9)
        self.play(Write(theorem1), run_time = 0.9)
        self.wait(2)

# 实数系完备性
class CompletenessOfR(Scene):
    def construct(self):
        # 可调参数
        NUMBER_LINE_RANGE, NUMBER_LINE_LENGTH = [-4, 4, 1], 16
        NUMBER_LINE_COLOR, NUMBER_LINE_WIDTH, NUMBER_FONT_SIZE = GREY_B, 3.2, 36
        REAL_LINE_RANGE, SAMPLE_COUNT = [-4, 4], 600
        REAL_LINE_COLOR, REAL_LINE_WIDTH = YELLOW_A, 7
        WAVE_HEIGHT, WAVE_WIDTH = 0.4, 2.4
        START_POSITION, END_POSITION = -4.8, 4.8
        NUMBER_LINE_TIME, LINE_CREATE_TIME, WAVE_TIME, FINAL_WAIT_TIME = 1.5, 1.0, 1.8, 1.5

        numberline = NumberLine(
            x_range = NUMBER_LINE_RANGE, length = NUMBER_LINE_LENGTH, include_ticks = True, include_numbers = True, include_tip = False,
            tick_size = 0.1, color = NUMBER_LINE_COLOR, stroke_width = NUMBER_LINE_WIDTH, font_size = NUMBER_FONT_SIZE,
            label_direction = DOWN, line_to_number_buff = 0.24
        ).set_z_index(0)
        r_label = MathTex(r"\mathbb{R}", font_size = 180, color = YELLOW_A)
        flat_line = Line(
            start = numberline.n2p(REAL_LINE_RANGE[0]), end = numberline.n2p(REAL_LINE_RANGE[1]),
            color = REAL_LINE_COLOR, stroke_width = REAL_LINE_WIDTH
        ).set_z_index(2)
        self.play(Create(r_label), run_time = 1.1)
        self.play(Create(numberline), ReplacementTransform(r_label, flat_line), run_time = NUMBER_LINE_TIME)
        wave_center = ValueTracker(START_POSITION)

        def create_wave():
            center = wave_center.get_value()
            x_values = np.linspace(REAL_LINE_RANGE[0], REAL_LINE_RANGE[1], SAMPLE_COUNT)
            points = []

            for x in x_values:
                distance = x - center

                if abs(distance) <= WAVE_WIDTH / 2:
                    displacement = WAVE_HEIGHT * np.cos(PI * distance / WAVE_WIDTH) ** 2
                else:
                    displacement = 0

                points.append(numberline.n2p(x) + UP * displacement)

            wave = VMobject(color = REAL_LINE_COLOR, stroke_width = REAL_LINE_WIDTH)
            wave.set_points_as_corners(points)
            wave.set_z_index(2)

            return wave

        traveling_wave = always_redraw(create_wave)
        self.remove(flat_line)
        self.add(traveling_wave)
        self.play(wave_center.animate.set_value(END_POSITION), run_time = WAVE_TIME, rate_func = linear)
        self.wait(FINAL_WAIT_TIME)
