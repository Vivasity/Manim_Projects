from __future__ import annotations
from manim import *
import math

config.background_color = "#000012"  # 设置Scene背景颜色

# 中文模板：使用 XeLaTeX 与 ctex
CHINESE_TEMPLATE = TexTemplate()
CHINESE_TEMPLATE.tex_compiler = "xelatex"
CHINESE_TEMPLATE.output_format = ".xdv"
CHINESE_TEMPLATE.add_to_preamble(r"\usepackage[UTF8]{ctex}")

# 配色：U_n 为逐渐加深的红色，V_n 为逐渐加深的蓝色
U_COLORS = [RED_E, RED_D, RED_C, RED_B, RED_A]
V_COLORS = [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]
PLAYER_A_FILL, PLAYER_B_FILL = "#3A1118", "#102844"
FINAL_YELLOW = YELLOW_A

# 十个区间严格嵌套、交替错位，并全部包含 sqrt(2)
ROUNDS = [
    ((0.6000, 2.4000), (1.0000, 1.8500)),
    ((1.1800, 1.6800), (1.3100, 1.5200)),
    ((1.3700, 1.4700), (1.3940, 1.4350)),
    ((1.4070, 1.4240), (1.4108, 1.4180)),
    ((1.4128, 1.4164), (1.4136, 1.4149)),
]

# 一些参数设置
AXIS_RANGE, AXIS_LENGTH, AXIS_Y = (0.0, 3.0), 16.0, 0.0
INITIAL_TICK_STEP, TICK_THRESHOLD = 0.5, 1 / 5
ZOOM_FACTORS = [2.6, 2.5, 2.4, 2.3]

AXIS_STROKE, INTERVAL_STROKE = 3.2, 8.0
TICK_LENGTH, NUMBER_SIZE, NUMBER_BUFF = 0.2, 36, 0.24
INTERVAL_LABEL_SIZE = 44
LABEL_GAPS = {"U": 0.9, "V": 0.6}

CHAIN_SIZE, CHAIN_LEFT, CHAIN_TOP, CHAIN_BUFF = 48, 1.8, 1.4, 0.12
CARD_W, CARD_H, CARD_RADIUS = 2.18, 0.76, 0.16
CARD_SIDE_MARGIN, CARD_BOTTOM, CARD_TEXT_SIZE = 0.4, 0.4, 36

AXIS_TIME, CARD_TIME = 1.8, 0.7
SELECT_TIME, LABEL_HOLD, DOCK_TIME = 0.68, 0.22, 0.62
ZOOM_TIME, ZOOM_HOLD, TICK_TIME = 1.55, 0.24, 0.55
ELLIPSIS_TIME, POINT_TIME, FINAL_LABEL_TIME = 0.72, 0.38, 0.82
RATIONAL_HOLD, IRRATIONAL_HOLD, FINAL_HOLD = 1.5, 1.5, 3.0

DOT_RADIUS, FLASH_RADIUS = 0.08, 0.4
FLASH_LINE_LENGTH, FLASH_STROKE = 0.16, 4.0

# 视频开头的引入部分：Banach-Mazur游戏
class BanachMazurGame(MovingCameraScene):
    def construct(self):
        self.initial_frame_width = float(self.camera.frame.width)
        self.initial_frame_height = float(self.camera.frame.height)
        self.current_step = INITIAL_TICK_STEP
        self.interval_lines = VGroup()
        self.round_groups = VGroup()
        self.chain_items = VGroup()
        self.chain_metric_cache = {}
        self.validate_intervals()
        self.chain_cursor = -self.initial_frame_width / 2 + CHAIN_LEFT
        self.chain_y = self.initial_frame_height / 2 - CHAIN_TOP - 0.18

        # 开场阶段只显示数轴
        self.reference_axis = self.create_number_line(INITIAL_TICK_STEP)
        self.active_axis = self.reference_axis
        self.play(Create(self.active_axis), run_time = AXIS_TIME, rate_func = smooth)
        self.wait(0.5)
        self.card_visibility = ValueTracker(0.0)
        self.player_a_level = ValueTracker(0.32)
        self.player_b_level = ValueTracker(0.32)
        self.player_a = self.create_player_card("甲乙", U_COLORS[3], PLAYER_A_FILL, LEFT, self.player_a_level)
        self.player_b = self.create_player_card("丙丁", V_COLORS[3], PLAYER_B_FILL, RIGHT, self.player_b_level)
        self.add(self.player_a, self.player_b)
        self.play(self.card_visibility.animate.set_value(1.0), run_time = CARD_TIME, rate_func = smooth)
        self.wait(0.5)
        u1_label = None

        for n, (u_interval, v_interval) in enumerate(ROUNDS, start = 1):
            u_group = self.select_interval("U", n, u_interval, U_COLORS[n - 1], "A")
            if n == 1:
                u1_label = u_group[1]
            else:
                self.append_to_chain(u_group[1], rf"U_{{{n}}}")

            v_group = self.select_interval("V", n, v_interval, V_COLORS[n - 1], "B")
            if n == 1:
                self.dock_first_pair(u1_label, v_group[1])
            else:
                self.append_to_chain(v_group[1], rf"V_{{{n}}}")

            self.round_groups.add(VGroup(u_group, v_group))
            if n < 5:
                self.zoom_to_interval(*v_interval, ZOOM_FACTORS[n - 1])
                self.wait(ZOOM_HOLD)
                self.refine_ticks_if_needed()
                self.wait(0.65)

        self.append_chain_ellipsis()
        self.wait(0.4)
        chain_box = SurroundingRectangle(
            self.chain_items, color = YELLOW, buff = 0.24 * self.screen_scale(), stroke_width = 4.6 * self.screen_scale()
        )
        self.play(ShowPassingFlash(chain_box), time_width = 0.7, run_time = 2.4)
        self.wait(0.4)
        self.create_final_point_effect()
        self.play_membership_sequence()
        self.wait(FINAL_HOLD)
        self.clear_all_updaters()

    # 基础检查与尺寸补偿
    def validate_intervals(self):
        root2 = math.sqrt(2)
        intervals = [interval for pair in ROUNDS for interval in pair]
        previous_center = None

        for i, (left, right) in enumerate(intervals):
            if not left < root2 < right:
                raise ValueError(f"第 {i + 1} 个区间不包含 sqrt(2)。")
            center = (left + right) / 2
            if previous_center is not None and math.isclose(
                center, previous_center, abs_tol = 1e-12
            ):
                raise ValueError(f"第 {i + 1} 个区间与前一区间中点重合。")
            if i:
                old_left, old_right = intervals[i - 1]
                if not old_left < left < right < old_right:
                    raise ValueError(f"第 {i + 1} 个区间没有严格嵌套。")
            previous_center = center

    def screen_scale(self):
        return float(self.camera.frame.width / self.initial_frame_width)

    def overlay_point(self, offset):
        return self.camera.frame.get_center() + self.screen_scale() * offset

    def compensate_stroke_width(self, mob, base_width):
        mob.set_stroke(width=base_width * self.screen_scale(), family = False)

    def attach_fixed_overlay(self, mob, offset, base_height):
        def updater(target):
            target.set_height(max(base_height * self.screen_scale(), 1e-6))
            target.move_to(self.overlay_point(offset))

        mob.add_updater(updater, call_updater=True)
        return mob

    # 数轴与刻度
    def create_number_line(self, step):
        decimals = (
            len(str(step).split(".")[1].rstrip("0"))
            if "." in str(step) else 0
        )
        axis = NumberLine(
            x_range = [AXIS_RANGE[0], AXIS_RANGE[1], step],
            length = AXIS_LENGTH, include_ticks = True, include_numbers = True, include_tip = False,
            tick_size = TICK_LENGTH / 2, color = GREY_B, stroke_width = AXIS_STROKE, font_size = NUMBER_SIZE,
            label_direction = DOWN, line_to_number_buff = NUMBER_BUFF, decimal_number_config = {"num_decimal_places": decimals}
        )
        axis.shift(AXIS_Y * UP).set_z_index(0, family = True)
        self.attach_axis_updaters(axis)
        return axis

    def attach_axis_updaters(self, axis):
        axis.add_updater(lambda mob: self.compensate_stroke_width(mob, AXIS_STROKE), call_updater = True)

        for tick in axis.ticks:
            base_height = max(float(tick.height), 1e-6)

            def update_tick(mob, height = base_height):
                mob.set_height(height * self.screen_scale())
                self.compensate_stroke_width(mob, AXIS_STROKE)

            tick.add_updater(update_tick, call_updater=True)

        for number in axis.numbers:
            value = (
                float(number.get_value())
                if hasattr(number, "get_value")
                else float(axis.p2n(number.get_center()))
            )
            base_height = max(float(number.height), 1e-6)

            def update_number(mob, x = value, height = base_height):
                scale = self.screen_scale()
                mob.set_height(height * scale)
                mob.next_to(axis.n2p(x), DOWN, buff = NUMBER_BUFF * scale)

            number.add_updater(update_number, call_updater = True)

    @staticmethod
    def clear_axis_updaters(axis):
        axis.clear_updaters()

        for tick in getattr(axis, "ticks", []):
            tick.clear_updaters()
        
        for number in getattr(axis, "numbers", []):
            number.clear_updaters()

    def refine_ticks_if_needed(self):
        a = AXIS_RANGE[0]
        tick_gap = abs(float(self.active_axis.n2p(a + self.current_step)[0] - self.active_axis.n2p(a)[0]))

        if tick_gap <= float(self.camera.frame.width) * TICK_THRESHOLD:
            return

        new_step = self.current_step / 2
        new_axis = self.create_number_line(new_step)
        old_axis = self.active_axis
        self.play(FadeOut(old_axis), FadeIn(new_axis), run_time = TICK_TIME, rate_func = smooth)
        self.clear_axis_updaters(old_axis)
        self.active_axis = new_axis
        self.current_step = new_step

    # 玩家名牌
    def create_player_card(self, name, border_color, fill_color, side, level_tracker):
        glow = RoundedRectangle(
            width = CARD_W + 0.16, height = CARD_H + 0.15, corner_radius = CARD_RADIUS + 0.03,
            stroke_color = border_color, stroke_width = 7, fill_opacity = 0
        )
        body = RoundedRectangle(
            width = CARD_W, height = CARD_H, corner_radius = CARD_RADIUS,
            stroke_color = border_color, stroke_width = 2.8, fill_color = fill_color, fill_opacity = 0.42
        )
        label = Tex(name, tex_template = CHINESE_TEMPLATE, color = border_color, font_size = CARD_TEXT_SIZE).move_to(body)
        card = VGroup(glow, body, label).set_z_index(1000, family = True)
        base_width = float(card.width)

        def update_card(mob):
            scale = self.screen_scale()
            level = float(level_tracker.get_value())
            visible = float(self.card_visibility.get_value())
            mob.set_width(base_width * scale * (1 + 0.045 * level))

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

    def activate_player(self, player):
        if player == "A":
            return [
                self.player_a_level.animate.set_value(1.0), self.player_b_level.animate.set_value(0.18),
            ]
        return [
            self.player_a_level.animate.set_value(0.18), self.player_b_level.animate.set_value(1.0),
        ]

    # 区间与临时标签
    def create_interval(self, left, right, color, z_index):
        line = Line(
            self.reference_axis.n2p(left), self.reference_axis.n2p(right), color = color,
            stroke_width = INTERVAL_STROKE * self.screen_scale()
        )
        line.set_z_index(z_index).set_opacity(1)
        line.add_updater(lambda mob: self.compensate_stroke_width(mob, INTERVAL_STROKE), call_updater = True)
        return line

    def create_interval_label(self, tex, color, interval, symbol, z_index):
        left, right = interval
        scale = self.screen_scale()
        label = MathTex(tex, color = color, font_size = INTERVAL_LABEL_SIZE).scale(scale)
        midpoint = self.reference_axis.n2p((left + right) / 2)
        label.move_to(midpoint + LABEL_GAPS[symbol] * scale * UP)
        label.set_z_index(300 + z_index, family = True).set_opacity(1)
        return label

    def select_interval(self, symbol, index, interval, color, player):
        z_index = (10 + 2 * (index - 1) + (1 if symbol == "V" else 0))
        line = self.create_interval(*interval, color, z_index)
        label = self.create_interval_label(rf"{symbol}_{{{index}}}", color, interval, symbol, z_index)
        self.play(
            *self.activate_player(player), GrowFromCenter(line), FadeIn(label, shift = 0.08 * self.screen_scale() * UP),
            run_time = SELECT_TIME, rate_func = smooth
        )
        self.wait(LABEL_HOLD)
        self.interval_lines.add(line)
        return VGroup(line, label)

    # 左上角标签链
    def chain_metrics(self, tex):
        if tex not in self.chain_metric_cache:
            prototype = MathTex(tex, font_size = CHAIN_SIZE)
            self.chain_metric_cache[tex] = (float(prototype.width), float(prototype.height))
        return self.chain_metric_cache[tex]

    def reserve_chain_slot(self, tex):
        width, height = self.chain_metrics(tex)
        offset = np.array([self.chain_cursor + width / 2, self.chain_y, 0.0])
        self.chain_cursor += width + CHAIN_BUFF
        return offset, height

    def make_chain_symbol(self, tex, offset, height, z_index):
        symbol = MathTex(tex, color = WHITE, font_size = CHAIN_SIZE)
        symbol.set_height(height * self.screen_scale()).move_to(self.overlay_point(offset))
        symbol.set_z_index(z_index, family = True).set_opacity(1)
        return symbol

    def register_chain_item(self, mob, offset, height):
        self.attach_fixed_overlay(mob, offset, height)
        self.chain_items.add(mob)

    def dock_first_pair(self, u_label, v_label):
        u_offset, u_height = self.reserve_chain_slot(r"U_{1}")
        s_offset, s_height = self.reserve_chain_slot(r"\supset")
        v_offset, v_height = self.reserve_chain_slot(r"V_{1}")
        superset = self.make_chain_symbol(r"\supset", s_offset, s_height, 901)
        scale = self.screen_scale()
        self.play(
            u_label.animate.set_height(u_height * scale).move_to(self.overlay_point(u_offset)),
            FadeIn(superset),
            v_label.animate.set_height(v_height * scale).move_to(self.overlay_point(v_offset)),
            run_time = DOCK_TIME, rate_func = smooth
        )
        u_label.set_z_index(902, family = True)
        v_label.set_z_index(904, family = True)
        self.register_chain_item(u_label, u_offset, u_height)
        self.register_chain_item(superset, s_offset, s_height)
        self.register_chain_item(v_label, v_offset, v_height)

    def append_to_chain(self, label, tex):
        s_offset, s_height = self.reserve_chain_slot(r"\supset")
        l_offset, l_height = self.reserve_chain_slot(tex)
        z_index = 905 + len(self.chain_items)
        superset = self.make_chain_symbol(r"\supset", s_offset, s_height, z_index)
        scale = self.screen_scale()
        self.play(
            FadeIn(superset), label.animate.set_height(l_height * scale).move_to(self.overlay_point(l_offset)),
            run_time = DOCK_TIME, rate_func = smooth
        )
        label.set_z_index(z_index + 1, family = True)
        self.register_chain_item(superset, s_offset, s_height)
        self.register_chain_item(label, l_offset, l_height)

    def append_chain_ellipsis(self):
        s_offset, s_height = self.reserve_chain_slot(r"\supset")
        d_offset, d_height = self.reserve_chain_slot(r"\cdots")
        z_index = 930
        superset = self.make_chain_symbol(r"\supset", s_offset, s_height, z_index)
        dots = self.make_chain_symbol(r"\cdots", d_offset, d_height, z_index + 1)
        self.play(LaggedStart(FadeIn(superset), FadeIn(dots), lag_ratio = 0.35), run_time = ELLIPSIS_TIME, rate_func = smooth)
        self.register_chain_item(superset, s_offset, s_height)
        self.register_chain_item(dots, d_offset, d_height)

    # 镜头
    def zoom_to_interval(self, left, right, factor):
        target_width = (float(self.camera.frame.width) / factor)
        target_scale = (target_width / self.initial_frame_width)
        center = (self.reference_axis.n2p((left + right) / 2) + 0.16 * target_scale * UP)
        self.play(self.camera.frame.animate.set_width(target_width).move_to(center), run_time = ZOOM_TIME, rate_func = smooth)

    # 最终点、箭头和集合判定
    def create_final_point_effect(self):
        scale = self.screen_scale()
        point = self.active_axis.n2p(math.sqrt(2))
        dot = Dot(point, radius = DOT_RADIUS * scale, color = FINAL_YELLOW).set_z_index(700)
        self.play(GrowFromCenter(dot), run_time = POINT_TIME, rate_func = smooth)
        self.play(
            Flash(
                dot, color = FINAL_YELLOW, num_lines = 12, flash_radius = FLASH_RADIUS * scale,
                line_length = FLASH_LINE_LENGTH * scale, line_stroke_width = FLASH_STROKE * scale, time_width = 0.7
            ), run_time = 1.2
        )
        x_label = MathTex("x", color = FINAL_YELLOW, font_size = 44).scale(scale)
        x_label.move_to(point + 0.48 * scale * DOWN)
        arrow = Arrow(
            point + 0.24 * scale * UP, point + 0.8 * scale * UP, buff = 0, color = FINAL_YELLOW, stroke_width = 4.0 * scale,
            max_tip_length_to_length_ratio = 0.24
        )
        value = MathTex(r"1.41421\ldots", color = FINAL_YELLOW, font_size = 44).scale(scale)
        value.move_to(point + 1.12 * scale * UP)
        x_label.set_z_index(710, family = True)
        arrow.set_z_index(711, family = True)
        value.set_z_index(712, family = True)
        self.final_group = VGroup(dot, x_label, arrow, value)
        self.final_value = value
        self.play(
            FadeIn(x_label, shift = 0.05 * scale * DOWN), GrowArrow(arrow),
            FadeIn(value, shift = 0.05 * scale * UP),
            run_time = FINAL_LABEL_TIME, rate_func = smooth,
        )

    def place_membership(self, mob):
        scale = self.screen_scale()
        mob.next_to(self.final_value, RIGHT, buff = 0.16 * scale)
        mob.align_to(self.final_value, DOWN)
        mob.set_z_index(713, family = True)
        return mob

    def play_membership_sequence(self):
        scale = self.screen_scale()
        rational = MathTex(r"\in \mathbb{Q}", color = YELLOW, font_size = 44).scale(scale)
        self.place_membership(rational)
        self.play(
            *self.activate_player("A"),
            FadeIn(rational, shift = 0.08 * scale * RIGHT), run_time = 0.70, rate_func = smooth
        )
        self.wait(RATIONAL_HOLD)
        irrational = MathTex(r"\in \overline{\mathbb{Q}}", color = YELLOW, font_size = 44).scale(scale)
        self.place_membership(irrational)
        self.play(
            *self.activate_player("B"),
            ReplacementTransform(rational, irrational), run_time = 0.82, rate_func = smooth
        )
        self.wait(IRRATIONAL_HOLD)
        self.play(
            self.player_a_level.animate.set_value(0.26), self.player_b_level.animate.set_value(0.26),
            FadeOut(irrational), run_time = 0.65, rate_func = smooth
        )

    # 清理 
    def clear_all_updaters(self):
        self.clear_axis_updaters(self.active_axis)

        if self.reference_axis is not self.active_axis:
            self.clear_axis_updaters(self.reference_axis)

        for line in self.interval_lines:
            line.clear_updaters()

        for item in self.chain_items:
            item.clear_updaters()

        self.player_a.clear_updaters()
        self.player_b.clear_updaters()
    