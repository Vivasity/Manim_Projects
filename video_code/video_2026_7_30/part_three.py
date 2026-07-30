from __future__ import annotations
from manim import *
import math

config.background_color = "#000012"  # 设置Scene背景颜色

# 中文文字模板
CHINESE_TEMPLATE = TexTemplate()
CHINESE_TEMPLATE.tex_compiler = "xelatex"
CHINESE_TEMPLATE.output_format = ".xdv"
CHINESE_TEMPLATE.add_to_preamble(r"\usepackage[UTF8]{ctex}")

# 颜色参数
A_COLORS = [RED_E, RED_D, RED_C, RED_B, RED_A]
B_COLORS = [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]
PLAYER_A_FILL, PLAYER_B_FILL = "#3A1118", "#102844"
FINAL_COLOR, CROSS_COLOR = YELLOW_A, RED

# 每个 q_n 位于甲乙选择的区间内，但位于丙丁选择的区间外
ROUNDS = [
    ((0.6000, 2.4000), 2.0000, (1.0000, 1.8500)),
    ((1.1800, 1.6800), 1.2500, (1.3100, 1.5200)),
    ((1.3700, 1.4700), 1.3800, (1.3940, 1.4350)),
    ((1.4070, 1.4240), 1.4090, (1.4108, 1.4180)),
    ((1.4128, 1.4164), 1.4150, (1.4136, 1.4149)),
]
FINAL_X = math.sqrt(2)

# 数轴参数
AXIS_RANGE, AXIS_LENGTH, AXIS_Y = (-4.0, 4.0, 1.0), 16.0, 0.0
AXIS_STROKE, AXIS_TICK_SIZE = 3.2, 0.10

# 每次旧刻度间距占屏幕宽度的 1/5 时停止放大
TICK_SCREEN_DIVISIONS = 5
SUBDIVISIONS_PER_GAP = 5
DETAIL_TICK_SIZE, DETAIL_TICK_STROKE = 0.10, 2.5
DETAIL_TICK_MARGIN = 1

# 区间、点与公式参数
INTERVAL_STROKE, ENDPOINT_RADIUS = 8.0, 0.055
Q_DOT_RADIUS, FINAL_DOT_RADIUS = 0.072, 0.082
Q_LABEL_SIZE, Q_LABEL_BUFF = 40, 0.22
FORMULA_SIZE, FORMULA_TOP_BUFF, CROSS_SIZE = 46, 1.18, 74
FINAL_TEXT_SIZE, FINAL_TEXT_GAP = 46, 1.10

# 名牌参数
CARD_W, CARD_H, CARD_RADIUS = 2.18, 0.76, 0.16
CARD_SIDE_MARGIN, CARD_BOTTOM, CARD_TEXT_SIZE = 0.40, 0.40, 36

# 动画时间参数
AXIS_TIME, FORMULA_TIME, CARD_TIME = 1.6, 1.25, 0.7
SELECT_TIME, POINT_TIME, EXCLUDE_TIME = 0.75, 0.55, 0.82
ZOOM_TIME, TICK_TIME, ROUND_PAUSE = 1.45, 0.55, 0.35
FINAL_POINT_TIME, FINAL_LABEL_TIME, FINAL_HOLD = 0.45, 0.85, 3.0

# 将有理数一个一个地排除
class RationalExclusionGame(MovingCameraScene):
    def construct(self):
        self.initial_frame_width = float(self.camera.frame.width)
        self.initial_frame_height = float(self.camera.frame.height)
        self.interval_mobjects = VGroup()
        self.rational_mobjects = VGroup()
        self.detail_tick_groups = VGroup()
        self.crosses = VGroup()

        # 当前最细刻度之间的数值间距
        self.current_tick_step = AXIS_RANGE[2]
        self.validate_data()

        # 生成初始数轴
        self.reference_axis = self.create_number_line()
        self.play(Create(self.reference_axis), run_time = AXIS_TIME, rate_func = smooth)

        # 生成有理数分解式
        self.q_formula, self.q_parts = self.create_q_formula()
        self.add(self.q_formula)
        self.play(Write(self.q_formula), run_time = FORMULA_TIME, rate_func = smooth)

        # 生成玩家名牌
        self.card_visibility = ValueTracker(0.0)
        self.player_a_level = ValueTracker(0.30)
        self.player_b_level = ValueTracker(0.30)
        self.player_a = self.create_player_card("甲乙", A_COLORS[3], PLAYER_A_FILL, LEFT, self.player_a_level)
        self.player_b = self.create_player_card("丙丁", B_COLORS[3], PLAYER_B_FILL, RIGHT, self.player_b_level)
        self.add(self.player_a, self.player_b)
        self.play(
            self.card_visibility.animate.set_value(1.0), run_time = CARD_TIME, rate_func = smooth
        )
        self.wait(0.35)

        # 依次进行五轮区间选择与有理数排除
        for index, (a_interval, q_value, b_interval) in enumerate(ROUNDS, start = 1):
            # 甲乙选择闭区间
            a_group = self.create_interval(*a_interval, A_COLORS[index - 1], 20 + 2 * index)
            self.play(
                *self.activate_player("A"), GrowFromCenter(a_group[0]), FadeIn(a_group[1]),
                run_time = SELECT_TIME, rate_func = smooth
            )
            self.interval_mobjects.add(a_group)

            # 标出本轮需要排除的有理数
            q_group = self.create_rational_point(q_value, index)
            self.play(
                GrowFromCenter(q_group[0]), FadeIn(q_group[1], shift = 0.06 * self.screen_scale() * UP),
                run_time = POINT_TIME, rate_func = smooth
            )
            self.rational_mobjects.add(q_group)

            # 丙丁选择更小的闭区间并排除 q_n
            b_group = self.create_interval(*b_interval, B_COLORS[index - 1], 21 + 2 * index)
            cross, cross_opacity = self.create_cross(self.q_parts[index - 1])
            self.add(cross)
            self.play(
                *self.activate_player("B"), GrowFromCenter(b_group[0]), FadeIn(b_group[1]),
                cross_opacity.animate.set_value(1.0), run_time = EXCLUDE_TIME, rate_func = smooth
            )
            self.interval_mobjects.add(b_group)
            self.crosses.add(cross)
            self.wait(ROUND_PAUSE)

            # 最后一轮选择区间后不再放大，也不再添加新刻度
            if index == len(ROUNDS):
                continue

            # 放大到当前最细刻度间距达到屏幕宽度的 1/5
            self.zoom_until_tick_spacing(*b_interval, tick_step = self.current_tick_step)

            # 在每两个旧刻度之间补充四个新刻度
            ticks = self.create_subdivision_ticks(self.current_tick_step)
            self.detail_tick_groups.add(ticks)
            self.play(
                LaggedStart(*[Create(tick) for tick in ticks], lag_ratio = 0.025),
                run_time = TICK_TIME, rate_func = smooth
            )
            self.current_tick_step /= SUBDIVISIONS_PER_GAP
            self.wait(ROUND_PAUSE)

        # 将双方名牌恢复为非激活状态
        self.play(
            self.player_a_level.animate.set_value(0.25), self.player_b_level.animate.set_value(0.25),
            run_time = 0.4
        )

        # 标出最终保留下来的点
        self.show_final_point()
        self.wait(FINAL_HOLD)
        self.clear_all_updaters()

    # 检查区间嵌套关系与每轮排除关系
    def validate_data(self):
        previous = None

        for index, (a_interval, q_value, b_interval) in enumerate(ROUNDS, start = 1):
            a_left, a_right = a_interval
            b_left, b_right = b_interval

            if previous is not None:
                p_left, p_right = previous

                if not p_left < a_left < a_right < p_right:
                    raise ValueError(f"第 {index} 轮甲乙的区间没有严格位于上一闭区间内。")

            if not a_left < b_left < b_right < a_right:
                raise ValueError(f"第 {index} 轮丙丁的区间没有严格位于甲乙的区间内。")

            if not a_left < q_value < a_right:
                raise ValueError(f"q_{index} 不在甲乙选择的区间内。")

            if b_left <= q_value <= b_right:
                raise ValueError(f"q_{index} 没有被丙丁选择的区间排除。")

            if not b_left < FINAL_X < b_right:
                raise ValueError(f"最终点不在第 {index} 轮丙丁的区间内。")

            previous = b_interval

    # 返回当前镜头相对于初始镜头的缩放比例
    def screen_scale(self):
        return float(self.camera.frame.width / self.initial_frame_width)

    # 返回某个数值间距在场景中的实际长度
    def number_distance_to_scene(self, distance):
        x1 = self.reference_axis.n2p(0.0)[0]
        x2 = self.reference_axis.n2p(distance)[0]
        return abs(float(x2 - x1))

    # 保持线条在画面中的视觉粗细不变
    def compensate_stroke_width(self, mob, base_width):
        mob.set_stroke(width = base_width * self.screen_scale(), family = False)

    # 生成初始数轴
    def create_number_line(self):
        axis = NumberLine(
            x_range = list(AXIS_RANGE), length = AXIS_LENGTH, include_ticks = True, include_numbers = False, include_tip = False,
            tick_size = AXIS_TICK_SIZE, color = GREY_B, stroke_width = AXIS_STROKE, font_size = 36, label_direction = DOWN, line_to_number_buff = 0.24
        )
        axis.shift(AXIS_Y * UP)
        axis.set_z_index(0, family = True)
        axis.add_updater(lambda mob: self.compensate_stroke_width(mob, AXIS_STROKE), call_updater = True)

        for tick in axis.ticks:
            def update_tick(mob):
                scale = self.screen_scale()
                mob.set_height(2 * AXIS_TICK_SIZE * scale)
                self.compensate_stroke_width(mob, AXIS_STROKE)

            tick.add_updater(update_tick, call_updater = True)

        return axis

    # 生成始终位于镜头上方的公式
    def create_q_formula(self):
        q_tokens = [rf"q_{{{index}}}" for index in range(1, 6)]

        formula = MathTex(
            r"\mathbb{Q} = \{q_{1}\} \cup \{q_{2}\} "
            r"\cup \{q_{3}\} \cup \{q_{4}\} "
            r"\cup \{q_{5}\} \cup \cdots",
            substrings_to_isolate = q_tokens, font_size = FORMULA_SIZE, color = YELLOW_A
        )
        base_height = float(formula.height)

        def update_formula(mob):
            scale = self.screen_scale()
            mob.set_height(base_height * scale)
            mob.move_to(self.camera.frame.get_top() + FORMULA_TOP_BUFF * scale * DOWN, aligned_edge = UP)

        formula.set_z_index(900, family = True)
        formula.add_updater(update_formula, call_updater = True)
        q_parts = [
            formula.get_part_by_tex(token)
            for token in q_tokens
        ]

        if any(part is None for part in q_parts):
            raise ValueError("无法定位公式中的 q_n。")

        return formula, q_parts

    # 生成尺寸固定、位置固定的红色叉号
    def create_cross(self, target):
        opacity = ValueTracker(0.0)
        cross = MathTex(r"\times", color = CROSS_COLOR, font_size = CROSS_SIZE)
        base_height = float(cross.height)

        def update_cross(mob):
            scale = self.screen_scale()
            mob.set_height(base_height * scale)
            mob.move_to(target.get_center())
            mob.set_opacity(opacity.get_value())

        cross.set_z_index(950, family = True)
        cross.add_updater(update_cross, call_updater = True)

        return cross, opacity

    # 生成玩家名牌
    def create_player_card(self, name, border_color, fill_color, side, level_tracker):
        glow = RoundedRectangle(
            width = CARD_W + 0.16, height = CARD_H + 0.15, corner_radius = CARD_RADIUS + 0.03, stroke_color = border_color,
            stroke_width = 7, fill_opacity = 0
        )
        body = RoundedRectangle(
            width = CARD_W, height = CARD_H, corner_radius = CARD_RADIUS, stroke_color = border_color, stroke_width = 2.8,
            fill_color = fill_color, fill_opacity = 0.42
        )
        label = Tex(name, tex_template = CHINESE_TEMPLATE, color = border_color, font_size = CARD_TEXT_SIZE).move_to(body)
        card = VGroup(glow, body, label)
        card.set_z_index(1000, family = True)
        base_width = float(card.width)

        def update_card(mob):
            scale = self.screen_scale()
            level = float(level_tracker.get_value())
            visible = float(self.card_visibility.get_value())
            mob.set_width( base_width * scale * (1 + 0.045 * level))

            if side[0] < 0:
                anchor = (self.camera.frame.get_corner(DL) + CARD_SIDE_MARGIN * scale * RIGHT + CARD_BOTTOM * scale * UP)
                mob.move_to(anchor, aligned_edge = DL)

            else:
                anchor = (self.camera.frame.get_corner(DR) + CARD_SIDE_MARGIN * scale * LEFT + CARD_BOTTOM * scale * UP)
                mob.move_to(anchor, aligned_edge = DR)

            halo, panel, text = mob

            halo.set_stroke(border_color, width = 7 * scale, opacity = visible * 0.14 * level)
            panel.set_stroke(border_color, width = 2.8 * scale, opacity = visible * (0.42 + 0.58 * level))
            panel.set_fill(fill_color, opacity = visible * (0.24 + 0.28 * level))
            text.set_opacity(visible * (0.55 + 0.45 * level))

        card.add_updater(update_card, call_updater = True)
        return card

    # 切换当前行动玩家的名牌状态
    def activate_player(self, player):
        if player == "A":
            return [self.player_a_level.animate.set_value(1.0), self.player_b_level.animate.set_value(0.18)]

        return [self.player_a_level.animate.set_value(0.18), self.player_b_level.animate.set_value(1.0)]

    # 生成带实心端点的闭区间
    def create_interval(self, left, right, color, z_index):
        scale = self.screen_scale()
        line = Line(
            self.reference_axis.n2p(left), self.reference_axis.n2p(right),
            color = color, stroke_width = INTERVAL_STROKE * scale
        )
        endpoints = VGroup(
            Dot(self.reference_axis.n2p(left), radius = ENDPOINT_RADIUS * scale, color = color),
            Dot(self.reference_axis.n2p(right), radius = ENDPOINT_RADIUS * scale, color = color)
        )
        line.set_z_index(z_index)
        endpoints.set_z_index(z_index + 1, family = True)
        line.add_updater(lambda mob: self.compensate_stroke_width(mob, INTERVAL_STROKE), call_updater = True)

        for endpoint in endpoints:
            endpoint.add_updater(
                lambda mob: mob.set_width(2 * ENDPOINT_RADIUS * self.screen_scale()),
                call_updater = True
            )

        return VGroup(line, endpoints)

    # 生成数轴上的 q_n 点与标签
    def create_rational_point(self, value, index):
        point = self.reference_axis.n2p(value)
        dot = Dot(point, radius = Q_DOT_RADIUS * self.screen_scale(), color = YELLOW)
        dot.set_z_index(500)
        label = MathTex(rf"q_{{{index}}}", color = YELLOW_A, font_size = Q_LABEL_SIZE)
        base_height = float(label.height)
        dot.add_updater(lambda mob: mob.set_width(2 * Q_DOT_RADIUS * self.screen_scale()), call_updater = True)

        def update_label(mob):
            scale = self.screen_scale()
            mob.set_height(base_height * scale)
            mob.next_to(self.reference_axis.n2p(value), UP, buff = Q_LABEL_BUFF * scale)

        label.set_z_index(510, family = True)
        label.add_updater(update_label, call_updater = True)

        return VGroup(dot, label)

    # 放大至旧刻度间距恰好占屏幕宽度的 1/5
    def zoom_until_tick_spacing(self, left, right, tick_step):
        tick_scene_spacing = self.number_distance_to_scene(tick_step)
        target_width = (TICK_SCREEN_DIVISIONS * tick_scene_spacing)
        midpoint = self.reference_axis.n2p((left + right) / 2)

        # 镜头的纵坐标始终与数轴相同，使数轴位于画面正中间
        target_center = np.array([midpoint[0], self.reference_axis.get_center()[1], 0.0])
        self.play(
            self.camera.frame.animate.set_width(target_width).move_to(target_center),
            run_time = ZOOM_TIME, rate_func = smooth
        )

    # 在每两个旧刻度之间添加四个新刻度
    def create_subdivision_ticks(self, old_step):
        new_step = old_step / SUBDIVISIONS_PER_GAP
        frame_left = self.camera.frame.get_left()[0]
        frame_right = self.camera.frame.get_right()[0]
        axis_origin_x = self.reference_axis.n2p(0.0)[0]
        scene_units_per_number = self.number_distance_to_scene(1.0)
        left_value = (frame_left - axis_origin_x) / scene_units_per_number
        right_value = (frame_right - axis_origin_x) / scene_units_per_number
        first_index = (math.floor(left_value / new_step) - DETAIL_TICK_MARGIN)
        last_index = (math.ceil(right_value / new_step) + DETAIL_TICK_MARGIN)
        ticks = VGroup()

        for index in range(first_index, last_index + 1):
            # 旧刻度已经存在，只添加两个旧刻度之间的四个新刻度
            if index % SUBDIVISIONS_PER_GAP == 0:
                continue

            value = index * new_step
            center = self.reference_axis.n2p(value)
            scale = self.screen_scale()

            tick = Line(
                center + DETAIL_TICK_SIZE * scale * DOWN, center + DETAIL_TICK_SIZE * scale * UP,
                color = GREY_B, stroke_width = DETAIL_TICK_STROKE * scale
            )
            tick.set_z_index(2)

            def update_tick(mob, x = value):
                current_scale = self.screen_scale()
                mob.set_height(2 * DETAIL_TICK_SIZE * current_scale)
                mob.move_to(self.reference_axis.n2p(x))
                self.compensate_stroke_width(mob, DETAIL_TICK_STROKE)

            tick.add_updater(update_tick, call_updater = True)
            ticks.add(tick)

        return ticks

    # 生成最终保留下来的点、箭头与集合关系
    def show_final_point(self):
        scale = self.screen_scale()
        point = self.reference_axis.n2p(FINAL_X)
        dot = Dot(point, radius = FINAL_DOT_RADIUS * scale, color = FINAL_COLOR)
        dot.set_z_index(700)
        label = MathTex(r"x \in \overline{\mathbb{Q}}", color = YELLOW, font_size = FINAL_TEXT_SIZE).scale(scale)
        label.move_to(point + FINAL_TEXT_GAP * scale * UP)
        arrow = Arrow(
            point + 0.18 * scale * UP, label.get_bottom() + 0.10 * scale * DOWN, buff = 0,
            color = FINAL_COLOR, stroke_width = 4.2 * scale, max_tip_length_to_length_ratio = 0.22
        )
        arrow.set_z_index(701)
        label.set_z_index(702, family = True)
        self.play(GrowFromCenter(dot), run_time = FINAL_POINT_TIME, rate_func = smooth)
        self.play(
            Flash(
                dot, color = FINAL_COLOR, num_lines = 12, flash_radius = 0.36 * scale, line_length = 0.14 * scale,
                line_stroke_width = 3.8 * scale, time_width = 0.7
            ), run_time = 0.6
        )
        self.play(
            GrowArrow(arrow), FadeIn(label, shift = 0.06 * scale * UP),
            run_time = FINAL_LABEL_TIME, rate_func = smooth
        )

    # 结束前清除所有动态更新器
    def clear_all_updaters(self):
        self.reference_axis.clear_updaters()

        for tick in self.reference_axis.ticks:
            tick.clear_updaters()

        self.q_formula.clear_updaters()
        self.player_a.clear_updaters()
        self.player_b.clear_updaters()

        for group in self.interval_mobjects:
            group[0].clear_updaters()

            for endpoint in group[1]:
                endpoint.clear_updaters()

        for group in self.rational_mobjects:
            group[0].clear_updaters()
            group[1].clear_updaters()

        for group in self.detail_tick_groups:
            for tick in group:
                tick.clear_updaters()

        for cross in self.crosses:
            cross.clear_updaters()
