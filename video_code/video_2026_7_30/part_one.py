from manim import *

config.background_color = "#000012"  # 设置Scene背景颜色

# 全局参数：可以在这里统一调整画面、颜色和动画速度
SUPREMUM = 3.114519265

AXIS_LENGTH, AXIS_Y = 16, -0.35
AXIS_COLOR, AXIS_STROKE_WIDTH, AXIS_TICK_SIZE = GREY_B, 3.2, 0.1
DOT_COLOR, DOT_RADIUS, DOT_VERTICAL_OFFSET = YELLOW, 0.07, 0.01
SELECTED_COLOR, REJECTED_COLOR, RESULT_COLOR = TEAL_A, RED_A, WHITE

RESULT_FONT_SIZE, RESULT_Y, LOCAL_LABEL_FONT_SIZE = 66, 2.65, 36
CANDIDATE_LINE_HEIGHT, CANDIDATE_LINE_WIDTH = 0.64, 3
SUPREMUM_LINE_HEIGHT = 1.2

INITIAL_AXIS_TIME, FIRST_DOTS_TIME, LATER_DOTS_TIME = 0.8, 1.0, 1.6
DOT_FLASH_TIME, FAST_SCAN_TIME = 0.8, 1.0
REJECT_GROW_TIME, REJECT_COLOR_TIME, REJECT_FADE_TIME = 0.3, 0.35, 0.2
SELECT_GROW_TIME, SELECT_FLASH_TIME, HIGHLIGHT_TIME = 0.3, 0.4, 0.4
DIGIT_MOVE_TIME, DIGIT_PULSE_TIME, ELLIPSIS_TIME = 0.6, 0.4, 0.7

PAUSE_AFTER_AXIS, PAUSE_AFTER_DOTS = 0.35, 0.45
PAUSE_BETWEEN_CANDIDATES, PAUSE_AFTER_SCAN = 0.30, 0.35
PAUSE_AFTER_HIGHLIGHT, PAUSE_AFTER_DIGIT = 0.35, 0.40
PAUSE_AFTER_ZOOM, PAUSE_BEFORE_FINAL = 0.45, 0.55
FINAL_HOLD_TIME, FINAL_FADE_TIME = 2.0, 1.5

# 解释为什么闭区间套中只有一个实数
class NestedIntervals(Scene):
    def construct(self):
        r_label = MathTex(r"\mathbb{R}", font_size = 180, color = YELLOW_A)
        numberline = NumberLine(
            x_range = [-8, 8, 2], length = 16, include_ticks = True, include_numbers = True, include_tip = False,
            tick_size = 0.1, color = GREY_B, stroke_width = 3.2, font_size = 36, label_direction = DOWN, line_to_number_buff = 0.24
        )
        self.wait(0.5)
        self.play(Write(r_label), run_time = 1.6)
        self.wait(0.5)
        self.play(ReplacementTransform(r_label, numberline), run_time = 1.2)
        self.wait(0.4)
        r_tracker = ValueTracker(0.8)
        r_dot = always_redraw(lambda: Dot(numberline.n2p(r_tracker.get_value()), color = YELLOW, radius = 0.08))
        r_decimal = always_redraw(
            lambda: VGroup(
                DecimalNumber(r_tracker.get_value(), num_decimal_places = 3, font_size = 36, color = YELLOW_A), 
                MathTex(r"\ldots", font_size = 36, color = YELLOW_A)
            ).arrange(RIGHT, buff = 0.08).next_to(numberline.n2p(r_tracker.get_value()), UP, buff = 1.2)
        )
        arrow = always_redraw(
            lambda: Arrow(
                start = r_dot.get_center() + UP * 0.2, end = r_decimal.get_bottom() + DOWN * 0.2, 
                buff = 0, stroke_width = 4, max_tip_length_to_length_ratio = 0.24, color = YELLOW_A
            )
        )
        self.play(FadeIn(r_dot), Write(r_decimal), Create(arrow))
        self.wait(0.5)
        self.play(r_tracker.animate.set_value(3.91137), run_time = 2, rate_func = smooth)
        self.wait()
        self.play(r_tracker.animate.set_value(-1.14514), run_time = 2, rate_func = smooth)
        self.wait()
        self.play(r_tracker.animate.set_value(2.50000), run_time = 2, rate_func = smooth)
        self.wait()
        self.play(FadeOut(r_dot), FadeOut(r_decimal), FadeOut(arrow))
        self.wait()

        interval_groups, interval_heights, creation_animations = [], [], []
        first_center, first_length, shrink_ratio = 0.2, 12, 0.7

        for i in range(8):
            current_length = first_length * shrink_ratio ** i
            left_value = first_center - current_length / 2
            right_value = first_center + current_length / 2
            height = 0.65 + 0.65 * i
            interval_heights.append(height)
            interval_color0 = interpolate_color(TEAL_D, TEAL_A, i / 7)
            interval_color1 = interpolate_color(BLUE_D, BLUE_A, i / 7)
            left_point = numberline.n2p(left_value) + height * UP
            right_point = numberline.n2p(right_value) + height * UP
            segment = Line(left_point, right_point, color = interval_color0, stroke_width = 8)
            left_label = MathTex(f"a_{{{i + 1}}}", color = interval_color1, font_size = 36).next_to(left_point, UP, buff = 0.14)
            right_label = MathTex(f"b_{{{i + 1}}}",color = interval_color1, font_size = 36).next_to(right_point, UP, buff = 0.14)
            interval_group = VGroup(segment, left_label, right_label)
            interval_groups.append(interval_group)
            creation_animations.append(
                AnimationGroup(
                    GrowFromCenter(segment), FadeIn(left_label, shift = 0.14 * UP), FadeIn(right_label, shift = 0.14 * UP),
                    lag_ratio = 0
                )
            )

        self.play(LaggedStart(*creation_animations, lag_ratio = 0.22), run_time = 4, rate_func = smooth)
        self.wait(0.4)

        movement_animations = [
            interval_group.animate.shift(height * DOWN)
            for interval_group, height in zip(interval_groups, interval_heights)
        ]

        flash_animations = [
            AnimationGroup(
                Flash(
                    interval_group[1], color = YELLOW, flash_radius = 0.38, line_length = 0.16, num_lines = 12
                ),
                Flash(
                    interval_group[2], color = YELLOW, flash_radius = 0.38, line_length = 0.16, num_lines = 12
                ), lag_ratio = 0
            )
            for i, interval_group in enumerate(interval_groups)
        ]

        self.play(LaggedStart(*flash_animations, lag_ratio = 0.3), run_time = 4)
        self.wait(0.4)
        self.play(LaggedStart(*movement_animations, lag_ratio = 0.22), run_time = 4.5, rate_func = smooth)
        self.wait(0.4)
        omission = MathTex(r"\cdots", font_size = 36, color = WHITE).next_to(numberline.n2p(0.2), UP, buff = 0.28)
        self.play(GrowFromCenter(omission))
        self.wait()
        inequality = MathTex(
            r"a_1", r"\leq", r"a_2", r"\leq", r"a_3", r"\leq", r"a_4", r"\leq", r"\cdots", r"\leq",
            r"b_4", r"\leq", r"b_3", r"\leq", r"b_2", r"\leq", r"b_1", font_size = 48
        )

        # a_i、b_i 的颜色与第 i 条线段保持一致
        colored_terms = {0: 0, 2: 1, 4: 2, 6: 3, 10: 3, 12: 2, 14: 1, 16: 0}

        for tex_index, interval_index in colored_terms.items():
            inequality[tex_index].set_color(
                interpolate_color(BLUE_D, BLUE_A, interval_index / 7)
            )

        # 所有小于等于号与省略号设为白色
        for tex_index in [1, 3, 5, 7, 8, 9, 11, 13, 15]:
            inequality[tex_index].set_color(WHITE)

        inequality.move_to(numberline.n2p(0) + 2.4 * UP)
        self.play(
            LaggedStart(
                *[
                    FadeIn(part, shift = 0.1 * UP)
                    for part in inequality
                ], lag_ratio = 0.08
            ), run_time = 2
        )
        self.wait()
        b1_box = SurroundingRectangle(inequality[16], color = YELLOW, buff = 0.16, stroke_width = 4)
        self.play(ShowPassingFlash(b1_box), time_width = 0.7, run_time = 2)
        self.wait()
        a1_box = SurroundingRectangle(inequality[0], color = YELLOW, buff = 0.16, stroke_width = 4)
        self.play(ShowPassingFlash(a1_box), time_width = 0.7, run_time = 2)
        self.wait()
        r_dot.clear_updaters()
        r_tracker = ValueTracker(-5.8)
        r_dot = always_redraw(lambda: Dot(numberline.n2p(r_tracker.get_value()), color = YELLOW, radius = 0.08))
        self.play(Create(r_dot))
        self.wait(0.2)
        self.play(r_tracker.animate.set_value(0.2), run_time = 4, rate_func = smooth)
        self.wait()
        self.play(Flash(r_dot, color = YELLOW_A, flash_radius = 0.38, line_length = 0.16, num_lines = 12), run_time = 1.6)
        self.wait(2.5)

        for mob in inequality:
            self.remove(mob)

        self.wait()
        arrow = Arrow(
            start = r_dot.get_center() + UP * 0.2, end = r_dot.get_center() + UP * 0.6, buff = 0, 
            stroke_width = 4, max_tip_length_to_length_ratio = 0.24, color = YELLOW_A
        )
        a_label = MathTex(r"A", font_size = 36, color = TEAL_B).next_to(numberline.n2p(0.2), UP, buff = 0.7)
        self.play(Create(arrow), FadeIn(a_label, shift = 0.05 * UP))
        self.wait()
        b_dot = Dot(numberline.n2p(0.5), color = YELLOW, radius = 0.08)
        b_arrow = Arrow(
            start = b_dot.get_center() + UP * 0.2, end = b_dot.get_center() + UP * 0.6, buff = 0, 
            stroke_width = 4, max_tip_length_to_length_ratio = 0.24, color = YELLOW_A
        )
        b_label = MathTex(r"B", font_size = 36, color = GREEN_B).next_to(numberline.n2p(0.5), UP, buff = 0.7)
        self.play(FadeIn(b_dot), Create(b_arrow), FadeIn(b_label, shift = 0.05 * UP))
        self.wait()
        
        # 写出第一次估计
        current_formula = self.create_formula([r"\frac{1}{2}"], "n-1")
        self.play(Write(current_formula), run_time = 1.4)
        self.wait(0.8)

        # 第一次继续代入
        expanded_formula = self.create_formula([r"\frac{1}{2}", r"\cdot", r"\frac{1}{2}"], "n-2")
        current_formula = self.change_formula(current_formula, expanded_formula)
        squared_formula = self.create_formula([r"\frac{1}{2^2}"], "n-2")
        current_formula = self.change_formula(current_formula, squared_formula, run_time = 1.0)

        # 第二次继续代入
        expanded_formula = self.create_formula([r"\frac{1}{2^2}", r"\cdot", r"\frac{1}{2}"], "n-3")
        current_formula = self.change_formula(current_formula, expanded_formula)
        cubed_formula = self.create_formula([r"\frac{1}{2^3}"], "n-3")
        current_formula = self.change_formula(current_formula, cubed_formula, run_time = 1.0)

        # 第三次继续代入
        expanded_formula = self.create_formula([r"\frac{1}{2^3}", r"\cdot", r"\frac{1}{2}"], "n-4")
        current_formula = self.change_formula(current_formula, expanded_formula)
        fourth_power_formula = self.create_formula([r"\frac{1}{2^4}"], "n-4")
        current_formula = self.change_formula(current_formula, fourth_power_formula, run_time = 1.0)

        # 推广到一般形式
        final_formula = self.create_formula([r"\frac{1}{2^{n-1}}"], "1")
        current_formula = self.change_formula(current_formula, final_formula, run_time = 1.4)
        self.play(Indicate(current_formula, color = WHITE, scale_factor = 1.05), run_time = 0.8)
        self.wait(1.6)
        formula_1 = MathTex(
            r"\lvert", "B", "-", "A", r"\rvert", "=", "C", ">", "0", font_size = 44, color = WHITE
        ).shift(1.4 * UP + 3.2 * LEFT)
        formula_1[1].set_color(GREEN_B), formula_1[3].set_color(TEAL_B), formula_1[6].set_color(YELLOW)
        formula_2 = MathTex(
            r"\exists", "N", ",", r"\forall", "n", ">", "N", ":", r"\frac{1}{2^{n-1}}",
            r"\lvert", r"b_1", "-", r"a_1", r"\rvert", "<", "C", font_size = 44, color = WHITE
        ).shift(1.4 * UP + 2.4 * RIGHT)
        formula_2[1].set_color(ORANGE), formula_2[4].set_color(YELLOW_A), formula_2[6].set_color(ORANGE) 
        formula_2[8].set_color(YELLOW_A), formula_2[10].set_color(GREEN_B), formula_2[12].set_color(TEAL_B)
        formula_2[15].set_color(YELLOW)
        formula_3 =  MathTex("A", "=", "B", font_size = 48, color = WHITE).shift(2 * UP)
        formula_3[0].set_color(TEAL_B), formula_3[2].set_color(GREEN_B)
        self.play(current_formula.animate.shift(0.4 * UP), run_time = 0.8)
        self.play(Write(formula_1), run_time = 0.8)
        self.wait()
        self.play(Write(formula_2), run_time = 1.4)
        self.wait()
        self.play(current_formula.animate.shift(3 * UP), formula_2.animate.shift(9 * RIGHT), formula_1.animate.shift(0.6 * UP + 3.2 * RIGHT), run_time = 1.6)
        b = VGroup(b_dot, b_arrow, b_label)
        self.play(ReplacementTransform(formula_1, formula_3), b.animate.shift(4 / 15 * LEFT), run_time = 1.8)
        self.wait()
        formula = VGroup(formula_3, a_label)
        x_label = MathTex(r"x", font_size = 40, color = YELLOW).next_to(numberline.n2p(0.2), UP, buff = 0.7)
        self.play(FadeOut(b), ReplacementTransform(formula, x_label), run_time = 1.6)
        self.wait(2.5)

    def create_formula(self, factor_parts, right_index):
        # 使用独立的绝对值符号，避免颜色匹配和渲染错误
        parts = [
            r"\lvert", r"b_n", "-", r"a_n", r"\rvert", r"\leq", *factor_parts, r"\lvert", rf"b_{{{right_index}}}", "-",
            rf"a_{{{right_index}}}", r"\rvert"
        ]
        formula = MathTex(*parts, font_size = 48, color = WHITE)

        # 按照完整的独立部分设置颜色
        for index, part in enumerate(parts):
            if part.startswith("b_"):
                formula[index].set_color(GREEN_B)
            elif part.startswith("a_"):
                formula[index].set_color(TEAL_B)
            elif r"\frac{1}{2" in part:
                formula[index].set_color(YELLOW_A)

        formula.move_to(UP * 2.4)
        return formula

    def change_formula(self, old_formula, new_formula, run_time = 1.2):
        self.play(
            TransformMatchingTex(old_formula, new_formula, transform_mismatches = True), run_time = run_time
        )
        self.wait(0.6)
        return new_formula

# 展示单调递增有界数列最终收敛到它的上确界
class MonotoneBoundedConvergence(MovingCameraScene):

    def axis_key(self, value, decimal_places):
        return round(float(value), decimal_places + 3)

    def create_local_axis(self, focus_min, focus_max, step, decimal_places, labeled_values, anchor_point):
        # 根据当前区间计算十倍放大后的单位长度
        focus_span = focus_max - focus_min
        left_edge_x = -AXIS_LENGTH / 2
        anchor_fraction = (anchor_point[0] - left_edge_x) / AXIS_LENGTH

        # 调整数轴显示范围，使数轴两端始终伸出屏幕
        visible_min = SUPREMUM - anchor_fraction * focus_span
        visible_max = visible_min + focus_span

        axis = NumberLine(
            x_range = [visible_min, visible_max, step], length = AXIS_LENGTH, include_ticks = False, include_numbers = False,
            include_tip = False, color = AXIS_COLOR, stroke_width = AXIS_STROKE_WIDTH
        )
        axis.move_to(UP * AXIS_Y)

        # 消除浮点误差，使上确界的屏幕位置严格固定
        axis.shift(anchor_point - axis.n2p(SUPREMUM))
        axis.set_z_index(0)
        axis.label_map = {}

        # 手动生成与十进制精度对齐的刻度
        ticks = VGroup()
        first_tick = np.ceil((visible_min - 1e-12) / step) * step
        tick_values = np.arange(first_tick, visible_max + step * 0.5, step)

        for value in tick_values:
            tick = Line(DOWN * AXIS_TICK_SIZE, UP * AXIS_TICK_SIZE, color = AXIS_COLOR, stroke_width = AXIS_STROKE_WIDTH)
            tick.move_to(axis.n2p(value))
            ticks.add(tick)

        axis.add(ticks)
        seen_keys = set()
        tolerance = step * 0.1

        # 只显示当前阶段必要的数字标签
        for value in labeled_values:
            value = float(value)

            if not (visible_min - tolerance <= value <= visible_max + tolerance):
                continue

            key = self.axis_key(value, decimal_places)

            if key in seen_keys:
                continue

            seen_keys.add(key)
            label = MathTex(f"{value:.{decimal_places}f}", color = AXIS_COLOR, font_size = LOCAL_LABEL_FONT_SIZE,)
            label.next_to(axis.n2p(value), DOWN, buff = 0.24)
            label.set_z_index(2)
            axis.add(label)
            axis.label_map[key] = label

        return axis

    def create_sequence_dots(self, axis, values):
        # 创建半径完全相同的黄色点
        dots = VGroup()

        for index, value in enumerate(values):
            offset = DOT_VERTICAL_OFFSET * np.sin(index * 2.4)
            dot = Dot(axis.n2p(value) + UP * offset, radius = DOT_RADIUS, color = DOT_COLOR)
            dot.set_fill(DOT_COLOR, opacity = 1)
            dot.set_stroke(DOT_COLOR, width = 0)
            dot.set_z_index(3)
            dots.add(dot)

        return dots

    def create_candidate_line(self, axis, value):
        # 创建候选上界竖线
        base = axis.n2p(value)
        line = Line(
            base, base + UP * CANDIDATE_LINE_HEIGHT, color = WHITE, stroke_width = CANDIDATE_LINE_WIDTH
        )
        line.set_z_index(5)
        return line

    def scan_candidate_lines(self, axis, candidate_values, chosen_upper_bound, fast = False):
        # 排除不是上界的候选值
        rejected_values = [
            value for value in candidate_values
            if not np.isclose(value, chosen_upper_bound, atol = 1e-12, rtol = 0)
        ]

        if fast and rejected_values:
            sequences = []

            for value in rejected_values:
                line = self.create_candidate_line(axis, value)
                sequences.append(
                    Succession(
                        GrowFromEdge(line, DOWN), line.animate.set_color(REJECTED_COLOR),
                        FadeOut(line, shift = DOWN * 0.1, scale = 0.82)
                    )
                )

            self.play(LaggedStart(*sequences, lag_ratio = 0.18), run_time = FAST_SCAN_TIME)
            self.wait(PAUSE_AFTER_SCAN)

        else:
            for value in rejected_values:
                line = self.create_candidate_line(axis, value)
                self.play(GrowFromEdge(line, DOWN), run_time = REJECT_GROW_TIME)
                self.play(line.animate.set_color(REJECTED_COLOR), run_time = REJECT_COLOR_TIME)
                self.play(FadeOut(line, shift = DOWN * 0.1, scale = 0.82), run_time = REJECT_FADE_TIME)
                self.wait(PAUSE_BETWEEN_CANDIDATES)

        # 选中当前精度下最小的上界
        chosen_line = self.create_candidate_line(axis, chosen_upper_bound)
        self.play(GrowFromEdge(chosen_line, DOWN), run_time = SELECT_GROW_TIME)
        self.play(
            chosen_line.animate.set_color(SELECTED_COLOR),
            Flash(
                axis.n2p(chosen_upper_bound) + UP * 0.32, color = SELECTED_COLOR, flash_radius = 0.34, line_length = 0.11, num_lines = 10
            ), run_time = SELECT_FLASH_TIME
        )
        self.wait(PAUSE_AFTER_SCAN)

        return chosen_line

    def create_interval_highlight(self, axis, left_value, right_value):
        # 创建被选中区间的半透明高亮
        highlight = Line(
            axis.n2p(left_value) + UP * 0.075, axis.n2p(right_value) + UP * 0.075,
            color = SELECTED_COLOR, stroke_width = 14
        )
        highlight.set_opacity(0.30)
        highlight.set_z_index(1)
        return highlight

    def remap_dots_to_axis(self, dots, values, new_axis, new_min, new_max):
        # 重新映射黄色点，只改变位置和透明度
        animations = []
        tolerance = max(abs(new_max - new_min) * 1e-10, 1e-13)
        frame_left = self.camera.frame.get_left()[0] - 0.35
        frame_right = self.camera.frame.get_right()[0] + 0.35

        for index, (dot, value) in enumerate(zip(dots, values)):
            offset = DOT_VERTICAL_OFFSET * np.sin(index * 2.4)
            inside = (new_min - tolerance <= value <= new_max + tolerance)

            if inside:
                target = new_axis.n2p(value) + UP * offset
                animations.append(dot.animate.move_to(target).set_opacity(1))
            else:
                target_x = frame_left if value < new_min else frame_right
                target = np.array([target_x, AXIS_Y + offset, 0])
                animations.append(dot.animate.move_to(target).set_opacity(0))

        return animations

    def transition_to_local_axis(
        self, old_axis, new_axis, dots, values, new_min, new_max, anchor_point,
        selected_line = None, interval_highlight = None, run_time = 1.4
    ):
        # 围绕固定的上确界位置进行语义放大
        new_axis.set_opacity(0)
        self.add(new_axis)

        animations = [
            old_axis.animate.stretch(1.22, dim = 0, about_point = anchor_point).set_opacity(0),
            new_axis.animate.set_opacity(1)
        ]

        animations.extend(self.remap_dots_to_axis(dots, values, new_axis, new_min, new_max))

        if selected_line is not None:
            animations.append(FadeOut(selected_line, shift = UP * 0.08))

        if interval_highlight is not None:
            expanded_highlight = self.create_interval_highlight(new_axis, new_min, new_max)
            animations.append(Transform(interval_highlight, expanded_highlight))

        self.play(AnimationGroup(*animations, lag_ratio = 0), run_time = run_time, rate_func = smooth)
        self.remove(old_axis)

        if interval_highlight is not None:
            self.play(FadeOut(interval_highlight), run_time = 0.16)

        self.wait(PAUSE_AFTER_ZOOM)

    def get_last_glyph(self, label):
        # 提取数学标签的最后一个字符
        if len(label) > 0 and len(label[0]) > 0:
            return label[0][-1]
        return label

    def move_digit_to_result(self, source_digit, target_position, digit_text):
        # 将数轴上的数字复制到顶部固定槽位
        target_digit = MathTex(digit_text, color = RESULT_COLOR, font_size = RESULT_FONT_SIZE)
        target_digit.move_to(target_position)
        target_digit.set_z_index(10)

        self.play(
            TransformFromCopy(source_digit, target_digit, path_arc = 0.48),
            run_time = DIGIT_MOVE_TIME, rate_func = smooth
        )
        self.play(
            Indicate(target_digit, color = RESULT_COLOR, scale_factor = 1.15),
            Flash(
                target_position, color = SELECTED_COLOR, flash_radius = 0.28, line_length = 0.08, num_lines = 8
            ), run_time = DIGIT_PULSE_TIME
        )
        self.wait(PAUSE_AFTER_DIGIT)

        return target_digit

    def get_result_positions(self):
        # 使用不可见模板确定每个字符的固定位置
        result_template = MathTex("3.11451", color = RESULT_COLOR, font_size = RESULT_FONT_SIZE)
        result_template.move_to(UP * RESULT_Y)
        result_template.set_opacity(0)
        glyphs = result_template[0]

        if len(glyphs) >= 7:
            return [
                glyphs[index].get_center().copy()
                for index in range(7)
            ]

        left_x = result_template.get_left()[0] + 0.13
        right_x = result_template.get_right()[0] - 0.13

        return [
            np.array([x, RESULT_Y, 0])
            for x in np.linspace(left_x, right_x, 7)
        ]

    def construct(self):
        result_positions = self.get_result_positions()
        result_characters = VGroup()

        # 生成严格单调递增且始终小于上确界的数列
        values = [
            SUPREMUM - (SUPREMUM + 7) * np.exp(-0.18 * (n - 1))
            for n in range(1, 101)
        ]

        # 创建略宽于默认画面的初始数轴
        numberline = NumberLine(
            x_range = [-8, 8, 1], length = 16, include_ticks = True, include_numbers = True, include_tip = False, tick_size = 0.1, 
            color = GREY_B, stroke_width = 3.2, font_size = 36, label_direction = DOWN, line_to_number_buff = 0.24
        )
        numberline.move_to(UP * AXIS_Y)
        numberline.set_z_index(0)

        # 记录上确界最初对应的屏幕位置
        anchor_point = numberline.n2p(SUPREMUM).copy()

        self.play(Create(numberline), run_time = INITIAL_AXIS_TIME, rate_func = smooth)
        self.wait(PAUSE_AFTER_AXIS)

        # 依次生成黄色点
        dots = self.create_sequence_dots(numberline, values)
        first_part = list(dots[:28])
        later_part = list(dots[28:])

        self.play(
            LaggedStart(
                *[
                    FadeIn(dot, scale = 0.4)
                    for dot in first_part
                ], lag_ratio = 0.05
            ), run_time = FIRST_DOTS_TIME
        )
        self.play(
            LaggedStart(
                *[
                    FadeIn(dot, scale = 0.4)
                    for dot in later_part
                ], lag_ratio = 0.013
            ), run_time = LATER_DOTS_TIME
        )
        self.wait(PAUSE_AFTER_DOTS)
        self.play(
            LaggedStart(
                *[
                    Flash(dot.get_center(), color = DOT_COLOR, flash_radius = 0.14, line_length = 0.04, num_lines = 7)
                    for dot in dots[-7:]
                ], lag_ratio = 0.16
            ), run_time = DOT_FLASH_TIME
        )
        self.wait(PAUSE_AFTER_DOTS)

        # 确定整数部分
        selected_line = self.scan_candidate_lines(numberline, [0, 1, 2, 3, 4], 4)
        interval_highlight = self.create_interval_highlight(numberline, 3, 4)
        self.play(Create(interval_highlight), run_time = HIGHLIGHT_TIME)
        self.wait(PAUSE_AFTER_HIGHLIGHT)

        source_three = MathTex("3", color = AXIS_COLOR, font_size = 36)
        source_three.next_to(numberline.n2p(3), DOWN, buff = 0.24)
        source_three.set_z_index(2)
        source_three.set_opacity(0)
        numberline.add(source_three)
        self.play(source_three.animate.set_opacity(1), run_time = 0.24,)
        top_three = self.move_digit_to_result(self.get_last_glyph(source_three), result_positions[0], "3")
        result_characters.add(top_three)

        # 各级十进制细分参数
        stages = [
            {
                "x_min": 3.0, "x_max": 4.0, "step": 0.1, "decimal_places": 1, "candidates": [3.0, 3.1, 3.2], 
                "lower": 3.1, "upper": 3.2, "digit": "1", "fast": False, "transition_time": 1.50,
            },
            {
                "x_min": 3.10, "x_max": 3.20, "step": 0.01, "decimal_places": 2, "candidates": [3.10, 3.11, 3.12],
                "lower": 3.11, "upper": 3.12, "digit": "1", "fast": False, "transition_time": 1.45,
            },
            {
                "x_min": 3.110, "x_max": 3.120, "step": 0.001, "decimal_places": 3,
                "candidates": [3.110, 3.111, 3.112, 3.113, 3.114, 3.115],
                "lower": 3.114, "upper": 3.115, "digit": "4", "fast": True, "transition_time": 1.35,
            },
            {
                "x_min": 3.1140, "x_max": 3.1150, "step": 0.0001, "decimal_places": 4,
                "candidates": [3.1140, 3.1141, 3.1142, 3.1143, 3.1144, 3.1145, 3.1146],
                "lower": 3.1145, "upper": 3.1146, "digit": "5", "fast": True, "transition_time": 1.30,
            },
            {
                "x_min": 3.11450, "x_max": 3.11460, "step": 0.00001, "decimal_places": 5,
                "candidates": [3.11450, 3.11451, 3.11452],
                "lower": 3.11451, "upper": 3.11452, "digit": "1", "fast": False, "transition_time": 1.30,
            },
        ]

        current_axis = numberline
        digit_slot_index = 2

        # 逐位确定小数部分
        for stage_index, stage in enumerate(stages):
            new_axis = self.create_local_axis(
                stage["x_min"], stage["x_max"], stage["step"], stage["decimal_places"],
                [stage["x_min"], stage["lower"], stage["upper"], stage["x_max"]], anchor_point
            )
            self.transition_to_local_axis(
                current_axis, new_axis, dots, values, stage["x_min"], stage["x_max"], anchor_point, selected_line,
                interval_highlight, stage["transition_time"]
            )
            current_axis = new_axis
            selected_line = self.scan_candidate_lines(current_axis, stage["candidates"], stage["upper"], stage["fast"])
            interval_highlight = self.create_interval_highlight(current_axis, stage["lower"], stage["upper"])
            self.play(Create(interval_highlight), run_time = HIGHLIGHT_TIME)
            self.wait(PAUSE_AFTER_HIGHLIGHT)

            # 第一位小数确定后加入小数点
            if stage_index == 0:
                decimal_point = MathTex(".", color = RESULT_COLOR, font_size = RESULT_FONT_SIZE)
                decimal_point.move_to(result_positions[1])
                decimal_point.set_z_index(10)
                self.play(FadeIn(decimal_point, scale = 0.5), run_time = 0.30)
                result_characters.add(decimal_point)

            label_key = self.axis_key(stage["lower"], stage["decimal_places"])
            source_label = current_axis.label_map[label_key]
            source_digit = self.get_last_glyph(source_label)

            top_digit = self.move_digit_to_result(source_digit, result_positions[digit_slot_index], stage["digit"])
            result_characters.add(top_digit)
            digit_slot_index += 1

        # 揭示真正的上确界
        self.wait(PAUSE_BEFORE_FINAL)
        self.play(FadeOut(selected_line), FadeOut(interval_highlight), run_time = 0.30)
        ellipsis = MathTex(r"\ldots", color = RESULT_COLOR, font_size = RESULT_FONT_SIZE)
        ellipsis.next_to(result_characters[-1], RIGHT, buff = 0.08)
        ellipsis.align_to(result_characters[-1], DOWN)
        ellipsis.set_z_index(10)
        self.play(FadeIn(ellipsis, shift = RIGHT * 0.08), run_time = ELLIPSIS_TIME)
        self.wait(0.30)

        # 上确界竖线位于始终不动的放大基准点
        supremum_line = Line(
            anchor_point, anchor_point + UP * SUPREMUM_LINE_HEIGHT, color = SELECTED_COLOR, stroke_width = 4
        )
        supremum_line.set_z_index(6)
        supremum_label = MathTex(r"\sup a_n", color = SELECTED_COLOR, font_size = 36)
        supremum_label.next_to(supremum_line, UP, buff = 0.18)
        supremum_label.set_z_index(6)
        self.play(GrowFromEdge(supremum_line, DOWN), run_time = 0.55)
        self.play(
            FadeIn(supremum_label, shift = UP * 0.06),
            Flash(
                anchor_point + UP * 0.6, color = SELECTED_COLOR, flash_radius = 0.48, line_length = 0.15, num_lines = 12
            ), run_time = 0.70
        )

        closest_dots = [
            dot for dot, value in zip(dots, values)
            if stages[-1]["x_min"] <= value <= stages[-1]["x_max"]
        ][-8:]

        self.play(
            LaggedStart(
                *[
                    Flash(dot.get_center(), color = DOT_COLOR, flash_radius = 0.13, line_length = 0.04, num_lines = 7)
                    for dot in closest_dots
                ], lag_ratio = 0.15
            ), run_time = 1.0
        )
        self.wait(FINAL_HOLD_TIME)
