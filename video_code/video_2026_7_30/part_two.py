from manim import *
from fractions import Fraction
import math
from math import gcd

config.background_color = "#000012"  # 设置Scene背景颜色

# 分数阵列
NUM_ROWS, NUM_COLS = 6, 8
NUMERATORS = [1, -1, 2, -2, 3, -3, 4, -4]
DENOMINATORS = [1, 2, 3, 4, 5, 6]
FRACTION_COLOR, FRACTION_FONT_SIZE = TEAL_A, 48
ROW_SPACING, COL_SPACING = 1.60, 1.85
FIRST_FRACTION_POSITION = np.array([-1.80, 0.35, 0.0])

# 遍历箭头
ARROW_COLOR, ARROW_BUFF = WHITE, 0.54
ARROW_STROKE_WIDTH, ARROW_TIP_RATIO = 2.4, 0.13

# 编号方格
NUM_BOXES, BOX_COLOR, INDEX_COLOR = 16, ORANGE, YELLOW
BOX_WIDTH, BOX_HEIGHT, BOX_CORNER_RADIUS = 1.6, 1.6, 0.24
BOX_SPACING, BOX_VERTICAL_OFFSET = 0.3, 1.58
BOX_STROKE_WIDTH, BOX_FILL_OPACITY = 3.2, 0.06
INDEX_FONT_SIZE, BOX_FRACTION_SCALE = 44, 0.96

# 动画时间
ROW_APPEAR_TIME, ARROW_APPEAR_TIME = 1.2, 0.4
NON_REDUCED_FADE_TIME, ARROW_FADE_TIME = 1.6, 0.65
BOX_APPEAR_TIME, MOVE_TO_BOX_TIME = 1.40, 0.34
INSERT_ZERO_TIME, FINAL_WAIT_TIME = 1.20, 2.50

# 动画间隔
FRACTION_LAG_RATIO, BOX_LAG_RATIO = 0.2, 0.16
NON_REDUCED_LAG_RATIO = 0.03

# 有理树
class RationalTree(Scene):
    def construct(self):
        numberline = NumberLine(
            x_range = [-4, 4, 1], length = 16, include_ticks = True, include_numbers = True, include_tip = False, 
            tick_size = 0.1, color = GREY_B, stroke_width = 3.2, font_size = 36, label_direction = DOWN, line_to_number_buff = 0.24
        )
        self.play(GrowFromCenter(numberline), run_time = 1.5)
        max_denominator = 30
        height_factor = 2
        denominator_groups = []

        for denominator in range(1, max_denominator + 1):
            lines = VGroup()

            for numerator in range(-4 * denominator, 4 * denominator + 1):
                rational = Fraction(numerator, denominator)

                # 只在最简分数的实际分母等于当前 denominator 时生成，
                # 避免同一个有理数被重复绘制。
                if rational.denominator != denominator:
                    continue

                x_value = float(rational)
                height = height_factor / denominator
                start_point = numberline.n2p(x_value)
                end_point = start_point + height * UP
                line = Line(
                    start = start_point, end = end_point,
                    color = interpolate_color(GREEN_B, TEAL_B, denominator / max_denominator),
                    stroke_width = max(1.2, 4.5 / np.sqrt(denominator))
                )
                lines.add(line)

            denominator_groups.append(lines)

        for denominator, lines in enumerate(denominator_groups, start=1):
            self.play(
                LaggedStart(
                    *[
                        GrowFromPoint(line, line.get_start())
                        for line in lines
                    ], lag_ratio = min(0.08, 1 / max(len(lines), 1))
                ), run_time = max(0.15, 0.8 / np.sqrt(denominator))
            )

        gamma_value = 0.577
        g_dot = Dot(point = numberline.n2p(gamma_value), color = YELLOW)
        g_arrow = Arrow(
            start = numberline.n2p(gamma_value) + 0.2 * DOWN, end = numberline.n2p(gamma_value) + 1 * DOWN,
            buff = 0, color = YELLOW_A, stroke_width = 4, max_tip_length_to_length_ratio = 0.18
        )
        gamma_label = MathTex(r"\gamma", color = ORANGE, font_size = 36).next_to(g_arrow, DOWN, buff = 0.15)
        self.wait(0.3)
        self.play(Create(g_dot), run_time = 0.6)
        self.play(GrowArrow(g_arrow), FadeIn(gamma_label, shift = 0.05 * DOWN), run_time = 0.6)
        self.wait(0.3)
        root_value = math.sqrt(2)
        r_dot = Dot(point = numberline.n2p(root_value), color = YELLOW)
        r_arrow = Arrow(
            start = numberline.n2p(root_value) + 0.2 * DOWN, end = numberline.n2p(root_value) + 1 * DOWN,
            buff = 0, color = YELLOW_A, stroke_width = 4, max_tip_length_to_length_ratio = 0.18
        )
        root_label = MathTex(r"\sqrt{2}", color = ORANGE, font_size = 36).next_to(r_arrow, DOWN, buff = 0.15)
        self.play(Create(r_dot), run_time = 0.6)
        self.play(GrowArrow(r_arrow), FadeIn(root_label, shift = 0.05 * DOWN), run_time = 0.6)
        self.wait(0.3)
        e_value = 2.718
        e_dot = Dot(point = numberline.n2p(e_value), color = YELLOW)
        e_arrow = Arrow(
            start = numberline.n2p(e_value) + 0.2 * DOWN, end = numberline.n2p(e_value) + 1 * DOWN,
            buff = 0, color = YELLOW_A, stroke_width = 4, max_tip_length_to_length_ratio = 0.18
        )
        e_label = MathTex(r"e", color = ORANGE, font_size = 36).next_to(e_arrow, DOWN, buff = 0.15)
        self.play(Create(e_dot), run_time = 0.6)
        self.play(GrowArrow(e_arrow), FadeIn(e_label, shift = 0.05 * DOWN), run_time = 0.6)
        self.wait(0.3)
        pi_dot = Dot(point = numberline.n2p(PI), color = YELLOW)
        pi_arrow = Arrow(
            start = numberline.n2p(PI) + 0.2 * DOWN, end = numberline.n2p(PI) + 1 * DOWN,
            buff = 0, color = YELLOW_A, stroke_width = 4, max_tip_length_to_length_ratio = 0.18
        )
        pi_label = MathTex(r"\pi", color = ORANGE, font_size = 36).next_to(pi_arrow, DOWN, buff = 0.15)
        self.play(Create(pi_dot), run_time = 0.6)
        self.play(GrowArrow(pi_arrow), FadeIn(pi_label, shift = 0.05 * DOWN), run_time = 0.6)
        self.wait(3)

# 有理数是可列的
class CountableRationalNumbers(Scene):
    def construct(self):
        self.validate_parameters()
        self.fraction_grid = self.create_fraction_grid()
        traversal_path = self.build_diagonal_path()
        path_arrows = self.create_path_arrows(traversal_path)
        self.remove_non_reduced()
        self.play(FadeOut(path_arrows), run_time = ARROW_FADE_TIME)
        boxes, box_indices = self.create_boxes()
        reduced_fractions = self.get_reduced_in_path_order(traversal_path)
        boxed_fractions = self.move_fractions_to_boxes(reduced_fractions, boxes)
        self.wait()
        self.insert_zero(boxed_fractions, boxes)
        self.wait(FINAL_WAIT_TIME)

    def validate_parameters(self):

        # 检查开头参数是否能够生成所需动画
        if len(NUMERATORS) < NUM_COLS:
            raise ValueError("NUMERATORS must contain at least NUM_COLS values.")

        if len(DENOMINATORS) < NUM_ROWS:
            raise ValueError("DENOMINATORS must contain at least NUM_ROWS values.")

        if NUM_BOXES < 1:
            raise ValueError("NUM_BOXES must be positive.")

    def fraction_tex(self, numerator, denominator):

        # 生成正负分数对应的 LaTeX 字符串
        absolute_numerator = abs(numerator)
        fraction = rf"\frac{{{absolute_numerator}}}{{{denominator}}}"

        if numerator < 0:
            return rf"-{fraction}"

        return fraction

    def fraction_position(self, row, col):

        # 计算分数阵列中指定位置的坐标
        return (FIRST_FRACTION_POSITION + col * COL_SPACING * RIGHT + row * ROW_SPACING * DOWN)

    def is_reduced_fraction(self, numerator, denominator):

        # 判断分数是否为最简分数
        return gcd(abs(numerator), denominator) == 1

    def create_fraction_grid(self):

        # 逐行创建六行八列的分数阵列
        fraction_grid = []

        for row in range(NUM_ROWS):
            denominator = DENOMINATORS[row]
            current_row = []

            for col in range(NUM_COLS):
                numerator = NUMERATORS[col]
                fraction = MathTex(self.fraction_tex(numerator, denominator), font_size = FRACTION_FONT_SIZE, color = FRACTION_COLOR)
                fraction.move_to(self.fraction_position(row, col))
                fraction.set_opacity(1)
                fraction.set_z_index(2)
                current_row.append(fraction)

            fraction_grid.append(current_row)
            self.play(
                LaggedStart(
                    *[GrowFromCenter(fraction) for fraction in current_row], lag_ratio = FRACTION_LAG_RATIO
                ), run_time = ROW_APPEAR_TIME
            )

        return fraction_grid

    def build_diagonal_path(self):

        # 自动生成到达第六行第一列为止的锯齿形路径
        traversal_path = []
        target = (NUM_ROWS - 1, 0)

        for diagonal_index in range(NUM_ROWS):
            diagonal = [
                (row, diagonal_index - row)
                for row in range(diagonal_index + 1)
                if row < NUM_ROWS and diagonal_index - row < NUM_COLS
            ]

            if diagonal_index % 2 == 0:
                diagonal.reverse()

            for position in diagonal:
                traversal_path.append(position)

                if position == target:
                    return traversal_path

        raise ValueError("The traversal path cannot reach the final position.")

    def create_path_arrows(self, path):

        # 按照遍历顺序逐根生成箭头
        arrows = VGroup()

        for start_position, end_position in zip(path, path[1:]):
            start_row, start_col = start_position
            end_row, end_col = end_position
            start_point = self.fraction_grid[start_row][start_col].get_center()
            end_point = self.fraction_grid[end_row][end_col].get_center()
            arrow = Arrow(
                start = start_point, end = end_point, buff = ARROW_BUFF, color = ARROW_COLOR, stroke_width = ARROW_STROKE_WIDTH,
                max_tip_length_to_length_ratio = ARROW_TIP_RATIO, max_stroke_width_to_length_ratio = 3
            )
            arrow.set_z_index(5)
            arrows.add(arrow)
            self.play(GrowArrow(arrow), run_time = ARROW_APPEAR_TIME)

        return arrows

    def remove_non_reduced(self):

        # 淡出阵列中所有非最简分数
        fade_animations = []

        for row in range(NUM_ROWS):
            denominator = DENOMINATORS[row]

            for col in range(NUM_COLS):
                numerator = NUMERATORS[col]

                if not self.is_reduced_fraction(numerator, denominator):
                    fade_animations.append(FadeOut(self.fraction_grid[row][col]))

        if fade_animations:
            self.play(LaggedStart(*fade_animations, lag_ratio = NON_REDUCED_LAG_RATIO), run_time = NON_REDUCED_FADE_TIME)

    def box_position(self, index):

        # 计算指定方格的中心位置
        box_step = BOX_WIDTH + BOX_SPACING
        first_box_position = (FIRST_FRACTION_POSITION + BOX_VERTICAL_OFFSET * UP + 2 * LEFT)

        return first_box_position + index * box_step * RIGHT

    def create_boxes(self):

        # 创建橙色圆角方格及其编号
        boxes = []
        box_indices = []
        appear_animations = []

        for index in range(NUM_BOXES):
            box = RoundedRectangle(
                width = BOX_WIDTH, height = BOX_HEIGHT, corner_radius = BOX_CORNER_RADIUS, color = BOX_COLOR,
                stroke_width = BOX_STROKE_WIDTH, fill_color = BOX_COLOR, fill_opacity = BOX_FILL_OPACITY
            )
            box.move_to(self.box_position(index))
            box.set_z_index(0)
            box_index = MathTex(str(index + 1), font_size = INDEX_FONT_SIZE, color = INDEX_COLOR)
            box_index.next_to(box, UP, buff = 0.22)
            box_index.set_z_index(2)
            boxes.append(box)
            box_indices.append(box_index)
            appear_animations.append(AnimationGroup(Create(box), FadeIn(box_index, shift = DOWN * 0.08), lag_ratio = 0))

        self.play(
            LaggedStart(*appear_animations, lag_ratio = BOX_LAG_RATIO), run_time = BOX_APPEAR_TIME
        )

        return boxes, box_indices

    def get_reduced_in_path_order(self, path):

        # 按照对角线路径筛选最简分数
        reduced_fractions = []

        for row, col in path:
            numerator = NUMERATORS[col]
            denominator = DENOMINATORS[row]

            if self.is_reduced_fraction(numerator, denominator):
                reduced_fractions.append(self.fraction_grid[row][col])

        if len(reduced_fractions) < NUM_BOXES:
            raise ValueError("The traversal path does not contain enough reduced fractions.")

        return reduced_fractions

    def move_fractions_to_boxes(self, fractions, boxes):

        # 把前十个最简分数依次放入方格
        boxed_fractions = []

        for fraction, box in zip(fractions[:NUM_BOXES], boxes):
            fraction.set_z_index(3)
            self.play(
                fraction.animate.scale(BOX_FRACTION_SCALE).move_to(box.get_center()),
                run_time = MOVE_TO_BOX_TIME, rate_func = smooth
            )
            boxed_fractions.append(fraction)

        return boxed_fractions

    def insert_zero(self, boxed_fractions, boxes):

        # 整体后移已有分数并在第一个方格插入零
        box_step = BOX_WIDTH + BOX_SPACING
        zero = MathTex("0", font_size = FRACTION_FONT_SIZE, color = FRACTION_COLOR)
        zero.scale(BOX_FRACTION_SCALE)
        zero.move_to(boxes[0].get_center() + 0.65 * DOWN)
        zero.set_opacity(0)
        zero.set_z_index(3)
        self.add(zero)
        shift_animations = [
            fraction.animate.shift(box_step * RIGHT)
            for fraction in boxed_fractions
        ]
        self.play(
            *shift_animations, zero.animate.set_opacity(1).move_to(boxes[0].get_center()),
            run_time = INSERT_ZERO_TIME, rate_func = smooth
        )
        