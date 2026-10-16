from manim import *
from decimal import Decimal, localcontext
import math
import numpy as np

# 全局可调参数
BG_COLOR = "#000012"
FRAME_WIDTH = 128 / 9
TIME_SCALE = 1.0
TRANSITION_TIME = 0.65
TRANSITION_HOLD = 0.12
config.background_color = BG_COLOR

THERMAL = dict(
    background = "#000012", ink = "#EAF4FF", muted = "#687C98",
    cursor = "#FFE17D",
    # 曲线、旋钮色环、温度读数、菱形共用此蓝红渐变
    curve_cold = "#4777D6", curve_hot = "#D64C4C",
    axis_color = "#FFFFFF", projection_color = "#FFF0A6", needle_color = "#FFF0A6",
    theta_min = -np.pi / 2, theta_max = np.pi / 2, break_theta = 0.12,
    temperature_min = 0.0, temperature_max = 400.0,
    low_start = 75.0, low_end = 125.0, high_start = 325.0, high_end = 375.0,
    continuous_low = 75.0, continuous_high = 375.0,
    continuous_midpoint = 0.12, continuous_steepness = 3.7,
    comfortable_temperature = 310.0,
    # 整张坐标图相对上一版上移0.55；左右端点的温度仍为75和375 K
    plot_left = -1.42, plot_right = 4.67, plot_bottom = -1.58, plot_top = 2.55,
    temperature_axis_x = 5.52, axis_width = 2.0, tick_length = 0.10,
    temperature_ticks = (0, 100, 200, 300, 400), tick_font_size = 32,
    axis_label_font_size = 36, theta_label_left_gap = 0.48, temperature_label_y = 3.04,
    theta_tick_label_offset = 0.45, temperature_tick_label_gap = 0.32,
    mapping_position = (-4.63, 2.22, 0), mapping_font_size = 35, mapping_arrow_tex = r"\longmapsto",
    curve_width = 4.2, curve_segments = 44, curve_samples_per_segment = 4,
    end_radius = 0.071, end_stroke = 2.5, cursor_radius = 0.071,
    cursor_glow_radius = 0.16, cursor_glow_opacity = 0.11,
    projection_width = 2.8, projection_opacity = 0.85, projection_dash = 0.10,
    diamond_half_width = 0.20, diamond_half_height = 0.10, diamond_stroke = 2.2, diamond_fill = 1.0,
    dial_center = (-4.63, -0.25, 0), dial_radius = 1.37,
    dial_inner_ratio = 0.88, dial_hub_radius = 0.12, dial_needle_ratio = 0.83,
    dial_arc_width = 5.0, dial_inner_width = 1.1, dial_segments = 54,
    dial_tick_count = 13, dial_tick_ratio = 0.91, dial_tick_width = 1.6,
    dial_base_width = 1.6, needle_base_width = 0.23, needle_tip_width = 0.028,
    needle_tail_length = 0.045, needle_stroke_width = 0.8,
    readout_value_x_offset = -0.31, readout_label_gap = 0.13,
    theta_readout_y_offset = -0.72, temperature_readout_y_offset = -1.34,
    readout_font_size = 35, theta_decimal_places = 2, temperature_decimal_places = 1,
    readout_unit_gap = 0.10,
    # 指针从靠近断点的已有角度开始，先微调，再意外多转约4.6度
    start_theta = -0.12, small_adjustment_angles = (-0.04, -0.10, 0.08),
    accidental_theta = 0.16,
    intro_time = 1.1, curve_reveal_time = 1.3, instrument_reveal_time = 0.8,
    initial_hold = 0.8, small_adjustment_time = 1.1, small_adjustment_hold = 0.25,
    before_jump_hold = 0.65, jump_time = 0.32, hot_hold = 1.3,
    mapping_reveal_time = 1.15, mapping_hold = 0.75, morph_time = 2.5,
    comfort_sweep_time = 2.8, final_hold = 2.0,
)

DIGITS = dict(
    # 三个小数分镜共用布局：紧凑数位、上下两行、无箭头/计数/横线
    count = 100, mismatch = 60, spacing = 0.36, first_x = -3.50,
    top_y = 0.50, bottom_y = -0.50, font_size = 43,
    upper_color = "#EAF4FF", lower_color = "#85D8E5",
    green = "#6EE7AE", red = "#FF657C", muted = "#687C98",
    label_x = -5.80, label_font_size = 43, prefix_x = -4.05,
    box_width = 0.34, box_height = 0.72, box_radius = 0.075,
    box_stroke = 2.6, box_fill = 0.08, camera_blend_width = 1.35,
    follow_x = 1.90, left_mask_edge = -4.80, right_mask_edge = 6.45,
    mask_width = 3.0, mask_height = 3.1, mask_y = 0.12,
    # 固定于镜头的连续渐变遮罩：每个数字内部也能平滑隐去
    # 起点对齐开场整数，尾部延长至两端；所有分镜完全共用同一渐变
    fade_start_offset = 0.0, fade_tail_width = 0.45, fade_power = 1.0,
    fade_mask_samples = 512, fade_mask_pixel_height = 8,
    result_y = -1.60, result_font_size = 56,
    intro_time = 1.2, step_time = 0.50, step_hold = 0.12,
    slow_last = 8, fast_stop = 55, fast_time = 1.18,
    finish_step_time = 0.32, mismatch_hold = 1.1,
    color_time = 0.28, shake_time = 0.55, shake_angle = 0.045,
    shake_scale = 1.065, shake_wiggles = 5,
    rewind_time = 1.65, rewind_hold = 0.25,
    precision_steps = 6, precision_move_time = 0.64, precision_hold = 0.70,
    precision_font_size = 38, precision_formula_gap = 0.30,
    nines_steps = 20, nines_move_time = 0.26, nines_shake_time = 0.22,
    nines_fast_time = 0.12, nines_shake_angle = 0.025,
    nines_dim_opacity = 0.14,
    nines_equality_font_size = 81, nines_equality_y = 0.0, nines_equality_time = 1.6,
    equality_time = 1.1, final_hold = 1.6,
)

# 比较实数的开场与扫描时长；数字布局和渐隐统一使用DIGITS
COMPARE = dict(
    definition_color = "#FFF0A6", definition_font_size = 48, definition_y = 2.35,
    definition_write_time = 1.8, definition_hold = 2.2, definition_fade_time = 0.65,
    equation_color = "#FFFFFF", equation_font_size = 120,
    question_color = "#FF5268", question_font_size = 150,
    question_outline_color = "#000000", question_outline_width = 5.0,
    equation_write_time = 1.15, equation_hold = 1.6, split_time = 1.55,
    digits_reveal_time = 1.0, first_digit_hold = 0.65,
    walk_last = 7, walk_step_time = 0.65, walk_step_hold = 0.15,
    # 在上一版基础上再提高约44%的峰值速度，仍保留逐格开头与缓起缓停
    scan_time = 5.0,
)

CONTINUITY = dict(
    # 几何与配色：所有宽度、半径都会补偿相机缩放，保持屏幕尺寸
    unit_x = 4.8, unit_y = 4.8, delta_cap = 1.0,
    white = "#EDF4FF", muted = "#7D90AB", background = "#000012",
    curve = "#F3DEA1", curve_width = 4.3,
    axis_color = "#FFFFFF", axis_width = 2.2, guide_width = 1.8,
    input = "#58D7D5", output = "#A5E5B0", point = "#FFD56A",
    clip_x = (-5.55, 5.85), clip_y = (-1.95, 1.95),
    endpoint_width = 1.65,
    output_opacity = 0.065, input_opacity = 0.060, overlap_opacity = 0.085,
    guide_dash = 0.10, dashed_ratio = 0.50, reference_opacity = 0.28,
    dot_radius = 0.058, static_radius = 0.025, endpoint_radius = 0.045, projection_radius = 0.042,
    halo_radius = 0.115, halo_width = 1.0, halo_opacity = 0.32,
    graph_samples = 241, ruler_y = -2.10, ruler_x = -5.55, ruler_tick = 0.075,
    show_rulers = True, show_projection = True, show_halo = True,
    tolerance = 1e-8, hud_z_index = 40,
    # 实际坐标刻度：随镜头向边缘移动，边缘与新小数位均平滑渐变
    tick_initial_precision = 1.0, tick_max_precision = 6,
    tick_font_size = 26, tick_digit_spacing = 1.18,
    tick_decimal_spacing = 0.45, tick_minus_spacing = 0.85,
    tick_decimal_drop = 0.070, tick_cache_size = 1024,
    tick_min_spacing_x = 1.38, tick_min_spacing_y = 0.68,
    tick_fade_width_x = 0.75, tick_fade_width_y = 0.38,
    tick_label_y = -2.46, tick_label_right = -5.73, tick_width = 1.4,
    # 先展示1至4位小数，再只替换全称公式中的底数
    decimal_powers = (1, 2, 3, 4), display_bases = ("2", "3.14"), delta_extra_digits = 3,
    intro_width = 10.0, initial_fraction = 0.9, width_per_error = 75.0,
    # epsilon带的完整高度不得超过可见纵轴的这一比例
    epsilon_axis_fraction_max = 0.50,
    error_lead_fraction = 0.86,
    title_position = (4.10, 2.06, 0), title_font_size = 28,
    main_position = (0, 3.12, 0), main_font_size = 35,
    definition_position = (0, 1.90, 0), definition_font_size = 33,
    bridge_position = (0, 0.78, 0), bridge_font_size = 31,
    proof_position = (0, 0.25, 0), proof_font_size = 38,
    focus_position = (0, 1.90, 0), focus_font_size = 56,
    # 青色输入框在左、绿色输出框在右，分别迁移到delta与误差界的位置
    # Both panels shift right by 0.25; their combined outer bounds are centered.
    delta_card_position = (-2.00, 2.86, 0), delta_card_width = 4.4,
    epsilon_card_position = (2.50, 2.86, 0), epsilon_card_width = 3.4,
    card_font_size = 33, card_height = 0.78, card_padding = 0.22,
    card_radius = 0.13, card_stroke = 1.8, card_fill_opacity = 0.08,
    # 尺寸标注与图像一起缩放、变暗，尺寸本身保持固定屏幕大小
    dimension_initial_index = 1, dimension_indices = (1, 2, 3, 4),
    dimension_font_size = 27, dimension_line_width = 1.45, dimension_extension_width = 1.05,
    dimension_tip_length = 0.115, dimension_tip_half_width = 0.043,
    dimension_top_inset = 0.60, dimension_top_label_gap = 0.27,
    dimension_right_inset = 0.32, dimension_epsilon_label_gap = 0.50,
    dimension_epsilon_rotation = 0.0,
    dimension_extension = 0.065,
    show_input_dimension = True, show_output_dimension = True,
    hud_max_width = 12.9, final_graph_opacity = 0.13,
    intro_time = 1.3, approach_time = 1.4, refine_time = 2.5,
    formula_time = 1.0, token_time = 1.2, scale_hold = 0.45,
    sweep_fractions = (-0.86, 0.86, 0.0), sweep_times = (0.70, 1.0, 0.45),
    quantifier_hold = 2.0, base_hold = 1.8, phase_hold = 1.2,
    dim_time = 1.8, definition_hold = 1.8, bridge_hold = 1.8, equivalence_hold = 2.0,
    card_change_time = 1.2, card_release_time = 0.6, cards_to_formula_time = 1.3, grammar_write_time = 1.1,
    label_path_arc = 0.18, grammar_lag = 0.09, formula_write_width = 1.8,
    focus_move_time = 1.1, focus_hold = 0.6, bound_to_epsilon_time = 1.7, focus_return_time = 1.5,
    definition_copy_time = 1.6, proof_transform_time = 1.7, final_hold = 3.0,
    proof_flash_color = YELLOW, proof_flash_buff = 0.20, proof_flash_width = 3.0,
    # time_width is the moving segment length; keep it well below one full loop.
    proof_flash_wait = 0.45, proof_flash_time = 2.0, proof_flash_time_width = 0.18,
)

# 动画实现
def build_water_temperature(scene):
    # 演示模型：75–375 K，不附加水的相变等物理条件
    p = THERMAL
    scene.camera.background_color = p["background"]

    def point(theta, temperature):

        return np.array([
            np.interp(theta, [p["theta_min"], p["theta_max"]], [p["plot_left"], p["plot_right"]]),
            np.interp(temperature, [p["temperature_min"], p["temperature_max"]], [p["plot_bottom"], p["plot_top"]]), 0.0,
        ])

    def low_curve(theta):
        u = (theta - p["theta_min"]) / (p["break_theta"] - p["theta_min"])

        return p["low_start"] + (p["low_end"] - p["low_start"]) * u * u

    def high_curve(theta):
        u = (theta - p["break_theta"]) / (p["theta_max"] - p["break_theta"])

        return p["high_start"] + (p["high_end"] - p["high_start"]) * (2 * u - u * u)

    def sigmoid(theta):

        return 1 / (1 + np.exp(-p["continuous_steepness"] * (theta - p["continuous_midpoint"])))

    sigmoid_min = sigmoid(p["theta_min"])
    sigmoid_max = sigmoid(p["theta_max"])

    def continuous_curve(theta):
        # 归一化后，左右端点严格为75 K和375 K，而不是渐近到这两个值
        amount = (sigmoid(theta) - sigmoid_min) / (sigmoid_max - sigmoid_min)

        return p["continuous_low"] + (p["continuous_high"] - p["continuous_low"]) * amount

    def curve_color(value):
        amount = np.clip((value - p["continuous_low"]) / (p["continuous_high"] - p["continuous_low"]), 0, 1)

        return interpolate_color(ManimColor(p["curve_cold"]), ManimColor(p["curve_hot"]), amount)

    def colored_curve(function, start, end):
        result = VGroup()
        boundaries = np.linspace(start, end, p["curve_segments"] + 1)

        for left, right in zip(boundaries[:-1], boundaries[1:]):
            coordinates = [point(t, function(t)) for t in np.linspace(left, right, p["curve_samples_per_segment"])]
            piece = VMobject().set_points_smoothly(coordinates)
            piece.set_stroke(curve_color(function((left + right) / 2)), p["curve_width"])
            result.add(piece)

        return result

    theta = ValueTracker(p["start_theta"])
    continuity = ValueTracker(0.0)

    def temperature_at_angle(angle):
        broken = low_curve(angle) if angle < p["break_theta"] else high_curve(angle)

        return (1 - continuity.get_value()) * broken + continuity.get_value() * continuous_curve(angle)

    def current_temperature():

        return temperature_at_angle(theta.get_value())

    # The second axis is placed on the right, matching the user's temperature gauge.
    axes = VGroup(
        Line([p["plot_left"], p["plot_bottom"], 0], [p["plot_right"], p["plot_bottom"], 0], color = p["axis_color"], stroke_width = p["axis_width"]),
        Line([p["temperature_axis_x"], p["plot_bottom"], 0], [p["temperature_axis_x"], p["plot_top"], 0], color = p["axis_color"], stroke_width = p["axis_width"]),
    )

    for angle, label in zip(np.linspace(p["theta_min"], p["theta_max"], 5), [r"-\frac{\pi}{2}", r"-\frac{\pi}{4}", "0", r"\frac{\pi}{4}", r"\frac{\pi}{2}"]):
        q = point(angle, p["temperature_min"])
        axes.add(Line(q + DOWN * p["tick_length"], q + UP * p["tick_length"], color = p["axis_color"], stroke_width = p["axis_width"]))
        axes.add(MathTex(label, font_size = p["tick_font_size"], color = p["ink"]).move_to(q + DOWN * p["theta_tick_label_offset"]))

    for temperature in p["temperature_ticks"]:
        q = np.array([p["temperature_axis_x"], point(0, temperature)[1], 0])
        axes.add(Line(q + LEFT * p["tick_length"], q + RIGHT * p["tick_length"], color = p["axis_color"], stroke_width = p["axis_width"]))
        axes.add(MathTex(str(temperature), font_size = p["tick_font_size"], color = p["ink"]).next_to(q, RIGHT, buff = p["temperature_tick_label_gap"]))

    axes.add(MathTex(r"\theta", font_size = p["axis_label_font_size"], color = p["ink"]).move_to([p["plot_left"] - p["theta_label_left_gap"], p["plot_bottom"], 0]))
    axes.add(MathTex(r"T\,(\mathrm{K})", font_size = p["axis_label_font_size"], color = p["ink"]).move_to([p["temperature_axis_x"], p["temperature_label_y"], 0]))
    center = np.array(p["dial_center"])
    radius = p["dial_radius"]
    dial = VGroup()

    for left, right in zip(np.linspace(0, PI, p["dial_segments"] + 1)[:-1], np.linspace(0, PI, p["dial_segments"] + 1)[1:]):
        angle_value = PI / 2 - (left + right) / 2
        arc = Arc(
            radius = radius, start_angle = left, angle = right - left, arc_center = center,
            stroke_color = curve_color(temperature_at_angle(angle_value)), stroke_width = p["dial_arc_width"]
        )

        # 色环按该位置对应的温度着色，曲线连续化时也一起更新
        arc.add_updater(lambda mob, angle_value = angle_value: mob.set_stroke(color = curve_color(temperature_at_angle(angle_value))))
        dial.add(arc)

    dial.add(Arc(radius = radius * p["dial_inner_ratio"], start_angle = 0, angle = PI, arc_center = center, stroke_color = p["muted"], stroke_width = p["dial_inner_width"]))
    dial.add(Line(center + LEFT * radius, center + RIGHT * radius, color = p["muted"], stroke_width = p["dial_base_width"]))

    for angle in np.linspace(0, PI, p["dial_tick_count"]):
        direction = np.array([np.cos(angle), np.sin(angle), 0])
        dial.add(Line(center + direction * radius * p["dial_tick_ratio"], center + direction * radius, color = p["ink"], stroke_width = p["dial_tick_width"]))

    def needle_shape():
        # 用局部方向构造上窄下宽的实心指针，旋转时底座不漂移
        angle = theta.get_value()
        direction = np.array([np.sin(angle), np.cos(angle), 0.0])
        normal = np.array([np.cos(angle), -np.sin(angle), 0.0])
        base = center - direction * p["needle_tail_length"]
        tip = center + direction * radius * p["dial_needle_ratio"]

        return Polygon(
            base - normal * p["needle_base_width"] / 2,
            base + normal * p["needle_base_width"] / 2,
            tip + normal * p["needle_tip_width"] / 2,
            tip - normal * p["needle_tip_width"] / 2,
            fill_color = p["needle_color"], fill_opacity = 1,
            stroke_color = p["needle_color"], stroke_width = p["needle_stroke_width"],
        )

    needle = always_redraw(needle_shape).set_z_index(2)
    hub = Circle(radius = p["dial_hub_radius"], color = p["needle_color"], stroke_width = p["axis_width"])
    hub.set_fill(p["background"], 1).move_to(center).set_z_index(3)

    # 两行读数统一固定数值左端与等号位置；角度以弧度显示，与横轴一致
    theta_anchor = center + np.array([p["readout_value_x_offset"], p["theta_readout_y_offset"], 0])
    temperature_anchor = center + np.array([p["readout_value_x_offset"], p["temperature_readout_y_offset"], 0])
    theta_label = MathTex(r"\theta=", font_size = p["readout_font_size"], color = p["ink"])
    theta_label.move_to(theta_anchor + LEFT * p["readout_label_gap"], aligned_edge = RIGHT)
    theta_reading = DecimalNumber(
        theta.get_value(), num_decimal_places = p["theta_decimal_places"], font_size = p["readout_font_size"], color = p["needle_color"]
    )
    theta_reading.add_updater(lambda mob: mob.set_value(theta.get_value()).move_to(theta_anchor, aligned_edge = LEFT))
    theta_reading.update(0)
    temperature_label = MathTex("T=", font_size = p["readout_font_size"], color = p["ink"])
    temperature_label.move_to(temperature_anchor + LEFT * p["readout_label_gap"], aligned_edge = RIGHT)
    temperature_reading = DecimalNumber(
        current_temperature(), num_decimal_places = p["temperature_decimal_places"],
        font_size = p["readout_font_size"], color = curve_color(current_temperature())
    )
    temperature_reading.add_updater(lambda mob: mob.set_value(current_temperature()).set_color(curve_color(current_temperature())).move_to(temperature_anchor, aligned_edge = LEFT))
    temperature_reading.update(0)
    unit = MathTex(r"\mathrm{K}", font_size = p["readout_font_size"], color = p["ink"])
    unit.add_updater(lambda mob: mob.next_to(temperature_reading, RIGHT, buff = p["readout_unit_gap"]))
    unit.update(0)
    readouts = VGroup(theta_label, theta_reading, temperature_label, temperature_reading, unit)

    # 初始先显示完整的两支间断曲线，再开始调节旋钮
    low = colored_curve(low_curve, p["theta_min"], p["break_theta"])
    high = colored_curve(high_curve, p["break_theta"], p["theta_max"])
    open_end = Circle(radius = p["end_radius"], color = curve_color(p["low_end"]), stroke_width = p["end_stroke"])
    open_end.set_fill(p["background"], 1).move_to(point(p["break_theta"], p["low_end"])).set_z_index(4)
    closed_end = Dot(point(p["break_theta"], p["high_start"]), radius = p["end_radius"], color = curve_color(p["high_start"])).set_z_index(4)

    def projection_lines():
        q = point(theta.get_value(), current_temperature())

        return VGroup(
            DashedLine([q[0], p["plot_bottom"], 0], q, dash_length = p["projection_dash"], color = p["projection_color"], stroke_width = p["projection_width"]),
            DashedLine(q, [p["temperature_axis_x"], q[1], 0], dash_length = p["projection_dash"], color = p["projection_color"], stroke_width = p["projection_width"]),
        ).set_opacity(p["projection_opacity"])
    
    projections = always_redraw(projection_lines)

    def diamond_shape():
        q = np.array([p["temperature_axis_x"], point(0, current_temperature())[1], 0])
        color = curve_color(current_temperature())

        return Polygon(q + UP * p["diamond_half_height"], q + RIGHT * p["diamond_half_width"], q + DOWN * p["diamond_half_height"], q + LEFT * p["diamond_half_width"], stroke_color = color, stroke_width = p["diamond_stroke"], fill_color = color, fill_opacity = p["diamond_fill"])
    diamond = always_redraw(diamond_shape).set_z_index(5)
    cursor = always_redraw(lambda: VGroup(
        Dot(point(theta.get_value(), current_temperature()), radius = p["cursor_glow_radius"], color = p["cursor"]).set_opacity(p["cursor_glow_opacity"]),
        Dot(point(theta.get_value(), current_temperature()), radius = p["cursor_radius"], color = p["cursor"]),
    )).set_z_index(6)

    scene.play(FadeIn(dial), FadeIn(axes), run_time = scene.seconds(p["intro_time"]))
    scene.play(Create(low), Create(high), FadeIn(open_end), FadeIn(closed_end), run_time = scene.seconds(p["curve_reveal_time"]))
    scene.play(FadeIn(needle), FadeIn(hub), FadeIn(readouts), FadeIn(projections), FadeIn(diamond), FadeIn(cursor), run_time = scene.seconds(p["instrument_reveal_time"]))
    scene.wait(scene.seconds(p["initial_hold"]))

    for angle in p["small_adjustment_angles"]:
        scene.play(theta.animate.set_value(angle), run_time = scene.seconds(p["small_adjustment_time"]), rate_func = smooth)
        scene.wait(scene.seconds(p["small_adjustment_hold"]))

    scene.wait(scene.seconds(p["before_jump_hold"]))

    # 指针仅越过一个小角度；函数分支切换让黄点和温标瞬间跳高
    scene.play(theta.animate.set_value(p["accidental_theta"]), run_time = scene.seconds(p["jump_time"]), rate_func = linear)
    scene.wait(scene.seconds(p["hot_hold"]))

    mapping = MathTex(r"T:\theta" + p["mapping_arrow_tex"] + r" T(\theta)", font_size = p["mapping_font_size"], color = p["ink"])
    mapping.move_to(p["mapping_position"])
    scene.play(Write(mapping), run_time = scene.seconds(p["mapping_reveal_time"]))
    scene.wait(scene.seconds(p["mapping_hold"]))
    continuous_low = colored_curve(continuous_curve, p["theta_min"], p["break_theta"])
    continuous_high = colored_curve(continuous_curve, p["break_theta"], p["theta_max"])
    scene.play(
        Transform(low, continuous_low), Transform(high, continuous_high),
        FadeOut(open_end), FadeOut(closed_end), continuity.animate.set_value(1),
        run_time = scene.seconds(p["morph_time"])
    )
    target_ratio = (p["comfortable_temperature"] - p["continuous_low"]) / (p["continuous_high"] - p["continuous_low"])
    target_sigmoid = sigmoid_min + target_ratio * (sigmoid_max - sigmoid_min)
    comfortable_theta = p["continuous_midpoint"] + np.log(target_sigmoid / (1 - target_sigmoid)) / p["continuous_steepness"]
    scene.play(theta.animate.set_value(comfortable_theta), run_time = scene.seconds(p["comfort_sweep_time"]))
    scene.wait(scene.seconds(p["final_hold"]))

    for item in (dial, needle, readouts, projections, diamond, cursor):
        item.clear_updaters(recursive = True)

    return VGroup(axes, dial, needle, hub, readouts, low, high, projections, diamond, cursor, mapping)

def comparison_decimals():
    # x = sqrt(2) - 10^-60; retain 100 actual digits, never binary floats.
    with localcontext() as ctx:
        ctx.prec = DIGITS["count"] + 30
        root = Decimal(2).sqrt()
        other = root - Decimal(10) ** (-DIGITS["mismatch"])
        top = format(root, "f").split(".")[1][:DIGITS["count"]]
        bottom = format(other, "f").split(".")[1][:DIGITS["count"]]
    assert len(top) == len(bottom) == DIGITS["count"]
    assert next(i for i, (a, b) in enumerate(zip(top, bottom), 1) if a != b) == DIGITS["mismatch"]

    return top, bottom

def pin_to_camera(scene, mob):
    reference = mob.get_center().copy() - scene.camera.frame.get_center()
    mob.add_updater(lambda item: item.move_to(scene.camera.frame.get_center() + reference))

    return mob

class DecimalRibbon:
    # A real 100-column ribbon: the camera travels, while row labels stay fixed.
    def __init__(self, scene, nines = False, initial_column = 1, style = None):
        self.p = p = {**DIGITS, **(style or {})}
        self.scene = scene
        self.nines = nines
        self.index = ValueTracker(initial_column)
        self.color = p["red"] if nines else p["green"]
        a, b = ("9" * p["count"], "0" * p["count"]) if nines else comparison_decimals()
        templates = {c: MathTex(c, font_size = p["font_size"]) for c in "0123456789"}
        self.rows = VGroup()

        for text, y, color in ((a, p["top_y"], p["upper_color"]), (b, p["bottom_y"], p["lower_color"])):
            row = VGroup(*[templates[c].copy().set_color(color).move_to([self.x(i), y, 0]) for i, c in enumerate(text, 1)])
            row.add(MathTex(r"\cdots", font_size = p["font_size"], color = color).move_to([self.x(p["count"] + 1), y, 0]))
            self.rows.add(row)

        self.prefixes = VGroup(*[
            MathTex(prefix, color = color, font_size = p["font_size"]).move_to([p["prefix_x"], y, 0])
            for prefix, y, color in (("0." if nines else "1.", p["top_y"], p["upper_color"]), ("1.", p["bottom_y"], p["lower_color"]))
        ])
        self.rows.add(self.prefixes)
        self.boxes = VGroup(*[
            RoundedRectangle(
                width = p["box_width"], height = p["box_height"], corner_radius = p["box_radius"],
                stroke_color = self.color, stroke_width = p["box_stroke"], fill_color = self.color,
                fill_opacity = p["box_fill"]).move_to([self.x(initial_column), y, 0]
            )
            for y in (p["top_y"], p["bottom_y"])
        ]).set_z_index(5)
        self.boxes.add_updater(lambda m: m.set_x(self.x(self.index.get_value())))

        # 保留开场整数与标签的间距；遮罩固定在屏幕两端，不依赖运动速度
        fade_left_start = self.prefixes[0][0][0].get_x() + p["fade_start_offset"]
        fade_left_edge = p["left_mask_edge"] - p["fade_tail_width"]
        fade_right_edge = p["right_mask_edge"] + p["fade_tail_width"]
        fade_width = fade_left_start - fade_left_edge
        self.masks = Group(*[
            Rectangle(width = p["mask_width"], height = p["mask_height"], stroke_width = 0, fill_color = BG_COLOR, fill_opacity = 1).move_to([x, p["mask_y"], 0])
            for x in (fade_left_edge - p["mask_width"] / 2, fade_right_edge + p["mask_width"] / 2)
        ])
        u = np.linspace(0, 1, p["fade_mask_samples"])
        visibility = (u * u * u * (u * (u * 6 - 15) + 10)) ** p["fade_power"]
        pixels = np.empty((p["fade_mask_pixel_height"], p["fade_mask_samples"], 4), dtype = np.uint8)
        pixels[:, :, :3] = np.rint(255 * np.array(ManimColor(BG_COLOR).to_rgb())).astype(np.uint8)
        pixels[:, :, 3] = np.rint(255 * (1 - visibility)).astype(np.uint8)

        for rgba, center_x in ((pixels, fade_left_edge + fade_width / 2),
                               (pixels[:, ::-1].copy(), fade_right_edge - fade_width / 2)):
            gradient = ImageMobject(rgba)
            gradient.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
            gradient.stretch_to_fit_width(fade_width).stretch_to_fit_height(p["mask_height"])
            gradient.move_to([center_x, p["mask_y"], 0])
            self.masks.add(gradient)

        self.masks.set_z_index(10)

        for mask in self.masks.get_family():
            mask.is_decimal_edge_mask = True

        pin_to_camera(scene, self.masks)
        labels = (r"0.\dot{9}", "1") if nines else (r"\sqrt{2}", "x")
        self.labels = VGroup(*[
            MathTex(label, font_size = p["label_font_size"], color = color).move_to([p["label_x"], y, 0])
            for label, y, color in ((labels[0], p["top_y"], p["upper_color"]), (labels[1], p["bottom_y"], p["lower_color"]))
        ]).set_z_index(11)
        pin_to_camera(scene, self.labels)
        self.all_mobjects = [self.rows, self.masks, self.labels, self.boxes]

    def x(self, index):

        return self.p["first_x"] + (index - 1) * self.p["spacing"]

    def camera_x(self, column):
        offset = self.x(column) - self.p["follow_x"]
        width = self.p["camera_blend_width"]

        if offset <= 0:
            return 0
        if offset >= width:
            return offset - width / 2
        
        u = offset / width

        return width * (u ** 3 - u ** 4 / 2)

    def add(self, animate = True):
        self.scene.add(*self.all_mobjects)

        if animate:
            self.scene.play(*[FadeIn(mob) for mob in self.all_mobjects if mob is not self.masks], run_time = self.scene.seconds(self.p["intro_time"]))

    def move(self, column, duration, rate_func = smooth):
        self.scene.play(
            self.index.animate.set_value(column),
            self.scene.camera.frame.animate.set_x(self.camera_x(column)),
            run_time = self.scene.seconds(duration), rate_func = rate_func
        )

    def shake(self, quick = False):
        p = self.p

        # Suspend the position updater during the shake so it cannot cancel the motion.
        self.boxes.suspend_updating()
        self.scene.play(
            Wiggle(self.boxes, scale_value = p["shake_scale"],
            rotation_angle = p["nines_shake_angle"] if quick else p["shake_angle"],
            n_wiggles = p["shake_wiggles"]),
            run_time = self.scene.seconds(p["nines_shake_time"] if quick else p["shake_time"])
        )
        self.boxes.resume_updating()

def build_real_comparison(scene):
    c = COMPARE
    sec = scene.seconds
    definition = MathTex(
        r"\forall\varepsilon>0,\ \exists\delta>0,\ \forall x:\ |x-x_0|<\delta\Rightarrow|f(x)-f(x_0)|<\varepsilon",
        font_size = c["definition_font_size"], color = c["definition_color"],
    ).move_to(UP * c["definition_y"])
    scene.play(Write(definition), run_time = sec(c["definition_write_time"]))
    scene.wait(sec(c["definition_hold"]))
    scene.play(FadeOut(definition), run_time = sec(c["definition_fade_time"]))
    equation = MathTex("x", "=", r"\sqrt{2}", font_size = c["equation_font_size"], color = c["equation_color"]).move_to(ORIGIN).set_z_index(11)
    question = MathTex("?", font_size = c["question_font_size"], color = c["question_color"])
    question.set_stroke(c["question_outline_color"], width = c["question_outline_width"], background = True)
    question.move_to(equation[1].get_center()).set_z_index(12)

    # 问号和等式同时出现，避免把待判断的等式呈现为已成立的结论
    scene.play(Write(equation), FadeIn(question), run_time = sec(c["equation_write_time"]))
    scene.wait(sec(c["equation_hold"]))
    ribbon = DecimalRibbon(scene, style = c)
    p = ribbon.p

    # 目标标签组暂不加入Scene，防止它的固定镜头updater干扰分离动画
    scene.play(
        ReplacementTransform(equation[0], ribbon.labels[1]),
        ReplacementTransform(equation[2], ribbon.labels[0]),
        FadeOut(equation[1]), FadeOut(question), run_time = sec(c["split_time"])
    )
    scene.remove(equation, ribbon.labels[0], ribbon.labels[1])
    ribbon.add(animate = False)
    scene.play(FadeIn(ribbon.rows), FadeIn(ribbon.boxes), run_time = sec(c["digits_reveal_time"]))
    scene.wait(sec(c["first_digit_hold"]))

    def place_scan(frame, column):
        ribbon.index.set_value(column)

        # 三个分镜共用同一镜头轨迹，回移场景从相同的第60位画面接续
        frame.set_x(ribbon.camera_x(column))

    def ease(alpha):

        return 6 * alpha ** 5 - 15 * alpha ** 4 + 10 * alpha ** 3

    # 开头明确逐格走、逐格停，先让观众看清每一对数字
    for column in range(2, c["walk_last"] + 1):

        def step(frame, alpha, start = column - 1, stop = column):
            place_scan(frame, start + (stop - start) * ease(alpha))

        scene.play(UpdateFromAlphaFunc(scene.camera.frame, step), run_time = sec(c["walk_step_time"]), rate_func = linear)
        scene.wait(sec(c["walk_step_hold"]))

    # 从刚停下的数位接续扫描，平缓加速，最后减速到第60位
    def scan(frame, alpha):
        column = c["walk_last"] + (p["mismatch"] - c["walk_last"]) * ease(alpha)
        place_scan(frame, column)

    scene.play(UpdateFromAlphaFunc(scene.camera.frame, scan), run_time = sec(c["scan_time"]), rate_func = linear)
    scene.play(ribbon.boxes.animate.set_stroke(p["red"]).set_fill(p["red"], opacity = p["box_fill"]), run_time = sec(p["color_time"]))
    ribbon.shake()
    result = MathTex(r"x<\sqrt{2}", font_size = p["result_font_size"], color = p["red"])
    result.move_to(scene.camera.frame.get_center() + UP * p["result_y"])
    scene.play(Write(result), run_time = sec(p["equality_time"]))
    scene.wait(sec(p["mismatch_hold"]))

def build_decimal_carry(scene):
    p = DIGITS
    ribbon = DecimalRibbon(scene, nines = True)
    ribbon.add()
    ribbon.shake(quick = True)

    # 只移动红框；数字和镜头始终留在原位
    for k in range(2, p["nines_steps"] + 1):
        scene.play(ribbon.index.animate.set_value(k), run_time = scene.seconds(p["nines_move_time"] if k <= p["slow_last"] else p["nines_fast_time"]))
        ribbon.shake(quick = True)

    equality = MathTex(r"0.\dot{9}", "=", "1", font_size = p["nines_equality_font_size"], color = p["upper_color"]).set_z_index(12)
    equality.move_to(scene.camera.frame.get_center() + UP * p["nines_equality_y"])

    # 解开标签与镜头的绑定，让原来的两个数直接移到中央组成等式
    ribbon.labels.clear_updaters(recursive = True)
    scene.remove(ribbon.labels)
    scene.add(*ribbon.labels)

    # 数字变暗、红框隐去和中央等式的形成同步开始、同步结束
    scene.play(
        ribbon.rows.animate.set_opacity(p["nines_dim_opacity"]), FadeOut(ribbon.boxes),
        ribbon.labels[0].animate.match_height(equality[0]).move_to(equality[0]).set_color(p["upper_color"]),
        ribbon.labels[1].animate.match_height(equality[2]).move_to(equality[2]).set_color(p["upper_color"]),
        Write(equality[1]), run_time = scene.seconds(p["nines_equality_time"]), rate_func = smooth
    )
    scene.remove(*ribbon.labels, *equality)
    scene.add(equality)
    scene.wait(scene.seconds(p["final_hold"]))

def build_decimal_precision(scene):
    p = DIGITS
    ribbon = DecimalRibbon(scene, initial_column = p["mismatch"])
    ribbon.boxes.set_stroke(p["red"]).set_fill(p["red"], opacity = p["box_fill"])

    # Revisit the same column, then bring the whole camera back to the first decimal.
    ribbon.add(animate = False)
    scene.camera.frame.set_x(ribbon.camera_x(p["mismatch"]))
    scene.update_mobjects(0)
    scene.play(FadeIn(ribbon.rows), FadeIn(ribbon.boxes), FadeIn(ribbon.labels), run_time = scene.seconds(p["intro_time"]))
    scene.wait(scene.seconds(p["rewind_hold"]))
    ribbon.move(1, p["rewind_time"])
    scene.play(ribbon.boxes.animate.set_stroke(p["green"]).set_fill(p["green"], opacity = p["box_fill"]), run_time = scene.seconds(p["color_time"]))

    def precision_formula(n):
        denominator = "10" if n == 1 else rf"10^{{{n}}}"
        formula = MathTex(rf"\left|x-\sqrt{{2}}\right|<\frac{{1}}{{{denominator}}}", font_size = p["precision_font_size"], color = p["green"]).set_z_index(12)
        anchor = np.array([ribbon.x(n), p["bottom_y"] - p["box_height"] / 2, 0])

        return formula.next_to(anchor, DOWN, buff = p["precision_formula_gap"])

    formula = precision_formula(1)
    scene.play(Write(formula), run_time = scene.seconds(p["equality_time"]))
    scene.wait(scene.seconds(p["precision_hold"]))

    for n in range(2, p["precision_steps"] + 1):
        # 公式与数位使用同一节奏，同时移动到下一格正下方
        target = precision_formula(n)
        scene.play(ribbon.index.animate.set_value(n), Transform(formula, target), run_time = scene.seconds(p["precision_move_time"]), rate_func = smooth)
        scene.wait(scene.seconds(p["precision_hold"]))
    scene.wait(scene.seconds(p["final_hold"]))

class _SqrtContinuityView:
    """Cairo-safe local geometry, centred at the exact point (2, sqrt(2)).

    epsilon / input_reveal / fraction are public ValueTrackers.  fraction gives
    x = 2 + fraction * delta; use abs(fraction) < 1 for the open neighbourhood.
    The caller owns the timeline, adds geometry, and controls camera.frame.
    """
    def __init__(self, scene, p, epsilon, frame_width, input_reveal = 1.0):
        self.scene = scene
        self.p = dict(p)
        self.root = math.sqrt(2.0)
        self.reference_width = FRAME_WIDTH
        self.frame = scene.camera.frame
        self.frame.set_width(float(frame_width)).move_to(ORIGIN)
        self.epsilon = epsilon if isinstance(epsilon, ValueTracker) else ValueTracker(float(epsilon))
        self.input_reveal = input_reveal if isinstance(input_reveal, ValueTracker) else ValueTracker(float(input_reveal))
        self.output_reveal = ValueTracker(1.0)
        self.fraction = ValueTracker(0.0)
        self.tick_precision = ValueTracker(float(self.p["tick_initial_precision"]))
        self.visual_opacity = ValueTracker(1.0)
        self.dimension_index = ValueTracker(float(self.p["dimension_initial_index"]))

        if not 0 < self.p["delta_cap"] <= 2:
            raise ValueError("delta_cap must lie in (0, 2].")
        if min(self.p["unit_x"], self.p["unit_y"], float(frame_width)) <= 0:
            raise ValueError("The geometric units and camera width must be positive.")
        # Compile only twelve glyphs once. Numeric labels are assembled from
        # copies; new decimal values never invoke LaTeX during playback.

        self.digit_templates = {
            char: MathTex(char, font_size = self.p["tick_font_size"], color = self.p["axis_color"])
            for char in "0123456789.-"
        }
        self.digit_advance = max(self.digit_templates[c].width for c in "0123456789") * self.p["tick_digit_spacing"]
        self.number_templates = {}
        self.dimension_templates = {
            index: MathTex(r"2\delta" + ("" if index < 0 else "_n" if index == 0 else "_{" + str(index) + "}"),
                           font_size = self.p["dimension_font_size"], color = self.p["input"])
            for index in (-1,0,*self.p["dimension_indices"])
        }
        self.epsilon_dimension_template = MathTex(r"2\varepsilon", font_size = self.p["dimension_font_size"], color = self.p["output"])
        self.epsilon_dimension_template.rotate(self.p["dimension_epsilon_rotation"])

        self.geometry = always_redraw(self._draw)

        # Its children include a changing number of clipped dashes.  Replace the
        # freshly built family atomically instead of repeatedly align_data-ing
        # old/new dash families (which also distorts nested cached TeX glyphs).
        self.geometry.clear_updaters()
        self.geometry.add_updater(lambda item: self._refresh_geometry(item))

    def _refresh_geometry(self, item):
        fresh = self._draw()

        # Cairo snapshots a flattened moving-family list at play() start.  Old
        # leaves can therefore remain referenced after replacing this subtree.
        # Empty every retired leaf so only the current tree can contribute pixels.
        for retired in item.get_family():
            if isinstance(retired, VMobject):
                retired.clear_points()

        item.submobjects = fresh.submobjects

    def scale(self):

        return self.frame.width / self.reference_width

    def delta(self, epsilon = None):
        e = self.epsilon.get_value() if epsilon is None else float(epsilon)

        return min(self.p["delta_cap"], self.root * e)

    def map(self, x, y):

        return np.array([(x - 2.0) * self.p["unit_x"], (y - self.root) * self.p["unit_y"], 0.0])

    def curve_point(self, h):
        # Use h directly, avoiding the cancellation in sqrt(2+h)-sqrt(2).
        dy = h / (math.sqrt(max(0.0, 2.0 + h)) + self.root)

        return np.array([h * self.p["unit_x"], dy * self.p["unit_y"], 0.0])

    def _screen(self, point):

        return self.frame.get_center() + self.scale() * np.array(point, dtype = float)

    def _tolerance(self, mob):
        tol = self.p["tolerance"] * self.scale()

        for part in mob.get_family():
            if isinstance(part, VMobject):
                part.tolerance_for_point_equality = tol

        return mob

    def fixed(self, mob, anchor):
        """Return mob with a HUD updater; anchor is in the original 16:9 frame.

        FadeIn/FadeOut while the camera is stationary is supported.  Replace the
        HUD object when its formula changes, rather than Transform-ing its points
        while this updater is active.  No TeX is compiled inside the updater.
        """
        template = mob.copy().clear_updaters(recursive = True).move_to(ORIGIN)
        bases = [
            (part.points.copy(), part.get_stroke_width(), part.get_stroke_width(background = True))
            for part in template.get_family() if isinstance(part, VMobject)
        ]

        def update(item):
            s = self.scale()
            centre = self._screen(anchor)

            # Resolve the receiving object's family, not the original mob's:
            # FadeIn creates copies carrying this updater, and those copies must
            # never write points into the original object's family.
            members = [part for part in item.get_family() if isinstance(part, VMobject)]

            for part, (points, width, background_width) in zip(members, bases):
                part.points = points * s + centre
                part.set_stroke(width = width * s, family = False)
                part.set_stroke(width = background_width * s, background = True, family = False)

            self._tolerance(item)
            item.set_z_index(self.p["hud_z_index"])

        update(mob)
        mob.add_updater(update)

        return mob

    def _number_template(self, text):
        if text not in self.number_templates:
            glyphs = VGroup()
            cursor = 0.0

            for char in text:
                glyph = self.digit_templates[char].copy()
                advance = self.digit_advance
                if char == ".":
                    advance *= self.p["tick_decimal_spacing"]
                elif char == "-":
                    advance *= self.p["tick_minus_spacing"]
                glyph.move_to([cursor + advance / 2, 0, 0])
                if char == ".":
                    glyph.shift(DOWN * self.p["tick_decimal_drop"])
                glyphs.add(glyph)
                cursor += advance
            glyphs.move_to(ORIGIN)

            if len(self.number_templates) >= self.p["tick_cache_size"]:
                self.number_templates.pop(next(iter(self.number_templates)))

            self.number_templates[text] = glyphs

        return self.number_templates[text]

    @staticmethod
    def _tick_smooth(value):
        value = float(np.clip(value, 0, 1))

        return value * value * (3 - 2 * value)

    def _density_levels(self, precision, axis):
        # Crossfade neighbouring 1/2/5 spacings; positions stay at real values.
        base = 10.0 ** (-precision)
        separation = self.p["tick_min_spacing_" + axis]
        screen_step = base * self.p["unit_" + axis] / self.scale()
        desired = max(1.0, separation / screen_step)

        if desired <= 1:
            return [(1, 1.0)]
        
        power = int(math.floor(math.log10(desired)))
        candidates = sorted(
            set(int(multiplier * 10 ** exponent)
            for exponent in range(max(0,power - 1),power + 2)
            for multiplier in (1,2,5,10))
        )
        lower = max(n for n in candidates if n <= desired)
        upper = min(n for n in candidates if n > desired)
        weight = self._tick_smooth(math.log(desired / lower) / math.log(upper / lower))

        return [(lower,1 - weight),(upper,weight)]

    def _numeric_ticks(self, axis, low, high, ruler_coordinate):
        p, s = self.p, self.scale()
        unit = p["unit_" + axis]
        target = 2.0 if axis == "x" else self.root
        camera_coordinate = self.frame.get_center()[0 if axis == "x" else 1]
        precision = float(np.clip(self.tick_precision.get_value(),0,p["tick_max_precision"]))
        lower = int(math.floor(precision))
        upper = min(lower + 1,p["tick_max_precision"])
        blend = self._tick_smooth(precision - lower)
        precision_levels = [(lower,1 - blend)]

        if upper != lower and blend > 0:
            precision_levels.append((upper,blend))
        actual_low, actual_high = target + low / unit, target + high / unit
        labels = {}

        for places, precision_weight in precision_levels:
            if precision_weight <= 0:
                continue
            base = 10.0 ** (-places)

            for multiplier, density_weight in self._density_levels(places,axis):
                weight = precision_weight * density_weight
                if weight <= 0:
                    continue
                step = base * multiplier
                first = math.ceil(actual_low / step - 1e-8)
                last = math.floor(actual_high / step + 1e-8)

                for index in range(first,last + 1):
                    # Every tick is an immutable decimal-grid value. Zooming
                    # changes its projected position, never the underlying value.
                    integer = index * multiplier
                    key = (places,integer)
                    labels[key] = min(1.0,labels.get(key,0.0) + weight)

        ticks, numbers = VGroup(), VGroup()
        line_weights = {}

        for (places, integer), weight in labels.items():
            value = integer * 10.0 ** (-places)
            coordinate = (value - target) * unit
            screen_coordinate = (coordinate - camera_coordinate) / s
            limits = p["clip_x"] if axis == "x" else p["clip_y"]
            edge_distance = min(screen_coordinate - limits[0], limits[1] - screen_coordinate)
            edge_weight = self._tick_smooth(edge_distance / p["tick_fade_width_" + axis])
            opacity = weight * edge_weight

            if opacity <= 0:
                continue

            # Integer formatting avoids binary floating-point rounding at 10^-4.
            sign = "-" if integer < 0 else ""
            digits = str(abs(integer)).zfill(places + 1)
            text = sign + (digits[:-places] + "." + digits[-places:] if places else digits)
            template = self._number_template(text)

            # Keep shared prefix glyphs exactly aligned during a precision
            # crossfade. Centre/right alignment is recovered continuously as
            # the appended decimal digit fades in, instead of double-printing
            # every old digit at a slightly displaced position.
            old_width = self._number_template(format(value, "." + str(lower) + "f")).width
            new_width = self._number_template(format(value, "." + str(upper) + "f")).width
            reference_width = (1 - blend) * old_width + blend * new_width
            label = template.copy().scale(s)

            if axis == "x":
                label.move_to([coordinate,self._screen([0,p["tick_label_y"],0])[1],0])
                label.shift(RIGHT * (coordinate - reference_width * s / 2 - label.get_left()[0]))
            else:
                label.move_to([self._screen([p["tick_label_right"],0,0])[0],coordinate,0])
                label.shift(RIGHT * (self._screen([p["tick_label_right"],0,0])[0] - reference_width * s - label.get_left()[0]))

            label.set_opacity(opacity)
            numbers.add(self._tolerance(label))
            tick_key = round(value, p["tick_max_precision"] + 2)
            old = line_weights.get(tick_key,(coordinate,0.0))
            line_weights[tick_key] = (coordinate,min(1.0,old[1] + opacity))

        length = p["ruler_tick"] * s

        for coordinate, opacity in line_weights.values():
            if axis == "x":
                start = [coordinate,ruler_coordinate - length,0]
                end = [coordinate,ruler_coordinate + length,0]
            else:
                start = [ruler_coordinate - length,coordinate,0]
                end = [ruler_coordinate + length,coordinate,0]
            ticks.add(self._line(start,end,p["axis_color"],p["tick_width"],opacity))

        return VGroup(ticks,numbers)


    def _line(self, start, end, color, width, opacity = 1.0, dashed = False):
        s = self.scale()

        if np.linalg.norm(np.array(end) - np.array(start)) < self.p["tolerance"] * s:
            return VGroup()
        
        kwargs = dict(color = color, stroke_width = width * s, stroke_opacity = opacity)

        if dashed:
            item = DashedLine(start, end, dash_length = self.p["guide_dash"] * s,
                              dashed_ratio = self.p["dashed_ratio"], **kwargs)
        else:
            item = Line(start, end, **kwargs)

        return self._tolerance(item)

    def _open_dot(self, point, color, opacity = 1.0):
        p = self.p

        return self._tolerance(Circle(
            radius = p["endpoint_radius"] * self.scale(),
            stroke_color = color, stroke_width = p["endpoint_width"] * self.scale(),
            stroke_opacity = opacity, fill_color = p["background"], fill_opacity = opacity,
        ).move_to(point))

    def _fill(self, left, right, bottom, top, color, opacity):
        if right <= left or top <= bottom:
            return VGroup()
        
        return self._tolerance(Rectangle(
            width = right - left, height = top - bottom, stroke_width = 0,
            fill_color = color, fill_opacity = opacity,
        ).move_to([(left + right) / 2, (bottom + top) / 2, 0]))

    def _curve(self, hlo, hhi, count, color, width, opacity = 1.0):
        if hhi <= hlo:
            return VGroup()
        
        hs = np.linspace(hlo, hhi, max(3, int(count)))

        if hlo < 0 < hhi:
            hs = np.sort(np.unique(np.append(hs, 0.0)))

        dys = hs / (np.sqrt(np.maximum(0.0, 2.0 + hs)) + self.root)
        pts = np.column_stack((hs * self.p["unit_x"], dys * self.p["unit_y"], np.zeros_like(hs)))
        item = VMobject(stroke_color = color, stroke_width = width * self.scale(), stroke_opacity = opacity, fill_opacity = 0)
        item.set_points_as_corners(pts)

        return self._tolerance(item)

    def _dimension_arrow(self, start, end, color, opacity):
        # Explicit geometry avoids DoubleArrow's length-based stroke/tip clamp.
        p, s = self.p, self.scale()
        start, end = np.array(start,dtype = float), np.array(end,dtype = float)
        direction = end - start
        length = np.linalg.norm(direction)

        if length < p["tolerance"] * s:
            return VGroup()
        
        direction /= length
        perpendicular = np.array([-direction[1],direction[0],0])
        tip_length = p["dimension_tip_length"] * s
        tip_half_width = p["dimension_tip_half_width"] * s
        shaft = self._line(start,end,color,p["dimension_line_width"],opacity)
        left_tip = Polygon(start,
            start + direction * tip_length + perpendicular * tip_half_width,
            start + direction * tip_length - perpendicular * tip_half_width,
            stroke_width = 0,fill_color = color,fill_opacity = opacity)
        right_tip = Polygon(end,
            end - direction * tip_length + perpendicular * tip_half_width,
            end - direction * tip_length - perpendicular * tip_half_width,
            stroke_width = 0,fill_color = color,fill_opacity = opacity)
        
        return self._tolerance(VGroup(shaft,left_tip,right_tip))

    def _dimensions(self, dx, ey, plot_top, plot_right, input_opacity, output_opacity):
        p, s = self.p, self.scale()
        dimensions = VGroup()
        # Put both dimensions inside their corresponding filled error bands.
        top_y = plot_top - p["dimension_top_inset"] * s
        right_x = plot_right - p["dimension_right_inset"] * s
        extension = p["dimension_extension"] * s

        if p["show_input_dimension"]:
            dimensions.add(self._dimension_arrow([-dx,top_y,0],[dx,top_y,0],p["input"],input_opacity))

            for x in (-dx,dx):
                dimensions.add(self._line([x,top_y - extension,0],[x,top_y + extension,0], p["input"],p["dimension_extension_width"],input_opacity))
                
            index = int(round(self.dimension_index.get_value()))
            template = self.dimension_templates.get(index,self.dimension_templates[0])
            label = template.copy().scale(s).move_to([0,top_y + p["dimension_top_label_gap"] * s,0])
            label.set_opacity(input_opacity)
            dimensions.add(self._tolerance(label))

        if p["show_output_dimension"]:
            dimensions.add(self._dimension_arrow([right_x,-ey,0],[right_x,ey,0],p["output"],output_opacity))

            for y in (-ey,ey):
                dimensions.add(self._line([right_x - extension,y,0],[right_x + extension,y,0], p["output"],p["dimension_extension_width"],output_opacity))

            label = self.epsilon_dimension_template.copy().scale(s).move_to([right_x - p["dimension_epsilon_label_gap"] * s,0,0])
            label.set_opacity(output_opacity)
            dimensions.add(self._tolerance(label))

        return dimensions

    def _draw(self):
        p, s = self.p, self.scale()
        e = self.epsilon.get_value()

        if e <= 0:
            raise ValueError("epsilon must stay positive throughout the animation.")
        
        d = self.delta(e)
        reveal = float(np.clip(self.input_reveal.get_value(), 0, 1))
        output_reveal = float(np.clip(self.output_reveal.get_value(), 0, 1))
        fc = self.frame.get_center()
        left, right = fc[0] + s * p["clip_x"][0], fc[0] + s * p["clip_x"][1]
        bottom, top = fc[1] + s * p["clip_y"][0], fc[1] + s * p["clip_y"][1]
        dx, ey = p["unit_x"] * d, p["unit_y"] * e
        x_ruler = self._screen([p["ruler_x"], 0, 0])[0]
        y_ruler = self._screen([0, p["ruler_y"], 0])[1]
        bands = VGroup(
            self._fill(left, right, max(bottom, -ey), min(top, ey), p["output"], p["output_opacity"] * output_reveal),
            self._fill(max(left, -dx), min(right, dx), bottom, top, p["input"], p["input_opacity"] * reveal),
            self._fill(max(left, -dx), min(right, dx), max(bottom, -ey), min(top, ey), p["output"], p["overlap_opacity"] * reveal * output_reveal),
        )
        guides = VGroup()

        for y in (-ey, ey):
            if bottom <= y <= top:
                guides.add(self._line([left,y,0], [right,y,0], p["output"], p["guide_width"], output_reveal, dashed = True))
        for x in (-dx, dx):
            if left <= x <= right:
                guides.add(self._line([x,bottom,0], [x,top,0], p["input"], p["guide_width"], reveal, dashed = True))
        if bottom <= 0 <= top:
            guides.add(self._line([left,0,0], [right,0,0], p["muted"], p["guide_width"], p["reference_opacity"], dashed = True))
        if left <= 0 <= right:
            guides.add(self._line([0,bottom,0], [0,top,0], p["muted"], p["guide_width"], p["reference_opacity"], dashed = True))

        # Intersect the monotone square-root curve with BOTH screen dimensions.
        root_lo = max(0.0, self.root + bottom / p["unit_y"])
        root_hi = self.root + top / p["unit_y"]
        h_ylo = (root_lo - self.root) * (root_lo + self.root)
        h_yhi = (root_hi - self.root) * (root_hi + self.root)
        hlo = max(-2.0, left / p["unit_x"], h_ylo)
        hhi = min(right / p["unit_x"], h_yhi)
        curve = self._curve(hlo, hhi, p["graph_samples"], p["curve"], p["curve_width"])
        highlight = VGroup()  # The complete curve keeps one pale-yellow colour.
        endpoints = VGroup()

        for h in (-d, d):
            q = self.curve_point(h)
            if left <= q[0] <= right and bottom <= q[1] <= top:
                endpoints.add(self._open_dot(q, p["output"], reveal))

        rulers = VGroup()

        if p["show_rulers"]:
            # Both axes share the same lower-left corner at every zoom level.
            rulers.add(self._line([x_ruler,y_ruler,0], [right,y_ruler,0], p["axis_color"], p["axis_width"]))
            rulers.add(self._line([x_ruler,y_ruler,0], [x_ruler,top,0], p["axis_color"], p["axis_width"]))
            rulers.add(self._numeric_ticks("x", left, right, y_ruler))
            rulers.add(self._numeric_ticks("y", bottom, top, x_ruler))

            for sign in (-1, 1):
                x, y = sign * dx, sign * ey
                if left <= x <= right:
                    rulers.add(self._open_dot([x,y_ruler,0], p["input"], reveal))
                if bottom <= y <= top:
                    rulers.add(self._open_dot([x_ruler,y,0], p["output"], output_reveal))

        static_point = self._tolerance(Dot(ORIGIN, radius = p["static_radius"] * s, color = p["white"]))
        moving = VGroup()
        h = float(np.clip(self.fraction.get_value(), -1.0, 1.0)) * d
        q = self.curve_point(h)

        if left <= q[0] <= right and bottom <= q[1] <= top:

            if p["show_projection"]:
                moving.add(self._line([q[0],max(y_ruler,bottom),0], q, p["input"], p["guide_width"], reveal, dashed = True))
                moving.add(self._line([max(x_ruler,left),q[1],0], q, p["output"], p["guide_width"], reveal, dashed = True))

                if p["show_rulers"]:
                    for qp, color in (([q[0],y_ruler,0],p["input"]),([x_ruler,q[1],0],p["output"])):
                        moving.add(self._tolerance(Dot(qp, radius = p["projection_radius"] * s, color = color, fill_opacity = reveal)))
                        
            if p["show_halo"]:
                moving.add(self._tolerance(Circle(radius = p["halo_radius"] * s,
                    stroke_color = p["point"], stroke_width = p["halo_width"] * s,
                    stroke_opacity = p["halo_opacity"] * reveal).move_to(q)))
            moving.add(self._tolerance(Dot(q, radius = p["dot_radius"] * s,
                                           color = p["point"], fill_opacity = 1.0)))
        dimensions = self._dimensions(dx,ey,top,right,reveal,output_reveal)
        result = VGroup(bands, guides, curve, highlight, endpoints, rulers, static_point, moving, dimensions)
        dim = float(np.clip(self.visual_opacity.get_value(), 0, 1))

        if dim < 1:

            for leaf in result.family_members_with_points():
                leaf.set_fill(opacity = leaf.get_fill_opacity() * dim, family = False)
                leaf.set_stroke(opacity = leaf.get_stroke_opacity() * dim, family = False)
                leaf.set_stroke(opacity = leaf.get_stroke_opacity(background = True) * dim, background = True, family = False)
                
        return result

def _ct_formula(view, parts, colors, slot):
    p = view.p
    mob = MathTex(*parts, arg_separator = " ", color = p["white"], font_size = p[slot + "_font_size"])

    for index, key in colors.items():
        mob[index].set_color(p[key])

    if mob.width > p["hud_max_width"]:
        mob.scale_to_fit_width(p["hud_max_width"])

    return view.fixed(mob, p[slot + "_position"])

def _ct_card(view, n, kind):
    p = view.p
    error = 10.0 ** (-n)

    if kind == "epsilon":
        parts = [r"\varepsilon=", rf"10^{{-{n}}}", rf"={error:.{n}f}"]
        color = p["output"]  
    else:
        parts = [rf"\delta_{{{n}}}", rf"=\sqrt{{2}}\cdot 10^{{-{n}}}", rf"\approx {view.delta(error):.{n+p['delta_extra_digits']}f}"]
        color = p["input"]

    label = MathTex(*parts, arg_separator = " ", color = color, font_size = p["card_font_size"])
    max_width = p[kind + "_card_width"] - 2 * p["card_padding"]

    if label.width > max_width:
        label.scale_to_fit_width(max_width)

    panel = RoundedRectangle(
        width = p[kind + "_card_width"], height = p["card_height"],
        corner_radius = p["card_radius"], stroke_color = color,
        stroke_width = p["card_stroke"], fill_color = color,
        fill_opacity = p["card_fill_opacity"]
    )
    label.move_to(panel)

    return view.fixed(VGroup(panel, label), p[kind + "_card_position"])

def _ct_quantified(view, base = None, generic = False, slot = "main"):
    if base is not None:
        parts = [r"\forall", r"n\ge1,", r"\exists", r"\delta_n", r">0,", r"\forall x:",
                 r"|x-2|<", r"\delta_n", r"\Longrightarrow", r"|\sqrt{x}-\sqrt{2}|<", rf"\frac{{1}}{{{base}^n}}"]
        colors = {3:"input", 7:"input", 10:"output"}
    else:
        parts = [r"\forall", r"\varepsilon>0,", r"\exists", r"\delta", r">0,", r"\forall x:",
                 r"|x-x_0|<" if generic else r"|x-2|<", r"\delta", r"\Longrightarrow",
                 r"|f(x)-f(x_0)|<" if generic else r"|\sqrt{x}-\sqrt{2}|<", r"\varepsilon"]
        colors = {1:"output", 3:"input", 7:"input", 10:"output"}

    return _ct_formula(view, parts, colors, slot)

def _ct_suspend(mob):
    updaters = list(mob.updaters)
    mob.clear_updaters(recursive = True)

    return updaters

def _ct_restore(scene, mob, updaters):
    scene.add(mob)

    for updater in updaters:
        mob.add_updater(updater)

def _ct_morph(scene, context, slot, new, duration = None):
    # Existing glyphs become new glyphs; no complete formula fades into existence.
    old = context[slot]
    _ct_suspend(old)
    updaters = _ct_suspend(new)

    if len(old) == len(new):
        old_parts, new_parts = list(old), list(new)
        scene.remove(old)
        scene.add(*old_parts)
        animations = [ReplacementTransform(a,b) for a,b in zip(old_parts,new_parts)]
    else:
        old_parts, new_parts = [old], [new]
        animations = [ReplacementTransform(old,new)]

    scene.play(*animations, run_time = scene.seconds(duration or context["view"].p["token_time"]), rate_func = smooth)
    scene.remove(*old_parts,*new_parts)
    _ct_restore(scene,new,updaters)
    context[slot] = new

def _ct_from_copy(scene, context, source, new, slot, duration):
    clone = source.copy().clear_updaters(recursive = True)
    updaters = _ct_suspend(new)
    scene.add(clone)
    scene.play(ReplacementTransform(clone,new), run_time = scene.seconds(duration), rate_func = smooth)
    scene.remove(clone)
    _ct_restore(scene,new,updaters)
    context[slot] = new

def _ct_update_cards(scene, context, n):
    if n == context["n"]:
        return
    
    view, p = context["view"], context["view"].p
    pending, animations = [], []

    for kind in ("delta","epsilon"):
        old, new = context[kind + "_card"], _ct_card(view,n,kind)
        _ct_suspend(old)
        updaters = _ct_suspend(new)
        animations.append(ReplacementTransform(old,new))
        pending.append((kind,old,new,updaters))

    scene.play(*animations,run_time = scene.seconds(p["card_change_time"]),rate_func = smooth)

    for kind,old,new,updaters in pending:
        scene.remove(old)
        _ct_restore(scene,new,updaters)
        context[kind + "_card"] = new

    context["n"] = n
    view.dimension_index.set_value(n)

def _ct_cards_to_formula(scene, context):
    view, p = context["view"], context["view"].p
    delta_card, epsilon_card = context.pop("delta_card"), context.pop("epsilon_card")
    _ct_suspend(delta_card)
    _ct_suspend(epsilon_card)
    new = _ct_quantified(view,"10")
    updaters = _ct_suspend(new)
    delta_text, epsilon_text = delta_card[1], epsilon_card[1]
    delta_symbol, error_power = delta_text[0], epsilon_text[1]
    delta_copy = delta_symbol.copy()
    scene.remove(delta_card,epsilon_card)
    scene.add(delta_card[0],epsilon_card[0],*list(delta_text),*list(epsilon_text),delta_copy)
    unused = [*list(delta_text)[1:],epsilon_text[0],epsilon_text[2]]

    # Keep only the source symbols visible before moving them, so the newly
    # written logic never crosses a collapsing string of approximate digits.
    scene.play(FadeOut(delta_card[0]),FadeOut(epsilon_card[0]), *[FadeOut(item) for item in unused],run_time = scene.seconds(p["card_release_time"]))
    scene.play(
        ReplacementTransform(delta_symbol,new[3]),
        ReplacementTransform(delta_copy,new[7],path_arc = p["label_path_arc"]),
        ReplacementTransform(error_power,new[10]),
        run_time = scene.seconds(p["cards_to_formula_time"]),rate_func = smooth
    )
    grammar = [i for i in range(len(new)) if i not in (3,7,10)]
    scene.play(LaggedStart(
        *[Write(new[i],stroke_width = p["formula_write_width"] * view.scale())
        for i in grammar],lag_ratio = p["grammar_lag"]),
        run_time = scene.seconds(p["grammar_write_time"])
    )
    scene.remove(delta_card[0],epsilon_card[0],delta_symbol,error_power,delta_copy,*unused,*list(new))
    _ct_restore(scene,new,updaters)
    context["main"] = new
    view.dimension_index.set_value(0)

def _ct_smootherstep(t):

    return t * t * t * (10 + t * (-15 + 6 * t))

def _ct_sweep(scene, view):

    for fraction,duration in zip(view.p["sweep_fractions"],view.p["sweep_times"]):
        scene.play(view.fraction.animate.set_value(fraction),run_time = scene.seconds(duration),rate_func = smooth)

def _ct_minimum_frame_width(p, epsilon):
    # Keep the actual 2*epsilon band below the requested axis-height fraction.
    axis_height = p["clip_y"][1] - p["ruler_y"]

    return 2 * p["unit_y"] * FRAME_WIDTH * epsilon / (axis_height * p["epsilon_axis_fraction_max"])

def _ct_refine(scene, context, n):
    view, p = context["view"],context["view"].p
    _ct_update_cards(scene,context,n)
    start_error, start_width = view.epsilon.get_value(),view.frame.width
    start_precision, start_fraction = view.tick_precision.get_value(),view.fraction.get_value()
    error = 10.0 ** (-n)
    width = max(_ct_minimum_frame_width(p,error), min(start_width,p["width_per_error"] * error))
    def refine(frame,alpha):
        # A fixed value projects proportionally to 1/width. Ease that quantity
        # directly so the visible ticks have zero speed and acceleration at both ends.
        q = _ct_smootherstep(alpha)
        qe = _ct_smootherstep(min(1.0,alpha / p["error_lead_fraction"]))
        current_error = 1.0 / ((1 - qe) / start_error + qe / error)
        current_width = 1.0 / ((1 - q) / start_width + q / width)

        # Constrain the camera rather than clipping the mathematical error band.
        frame.set_width(max(current_width,_ct_minimum_frame_width(p,current_error)))
        view.epsilon.set_value(current_error)
        view.tick_precision.set_value(start_precision + (n - start_precision) * q)
        view.fraction.set_value(start_fraction * (1 - q))

    scene.play(UpdateFromAlphaFunc(view.frame,refine),run_time = scene.seconds(p["refine_time"]),rate_func = linear)
    view.epsilon.set_value(error)
    view.tick_precision.set_value(n)
    view.dimension_index.set_value(n)
    _ct_sweep(scene,view)
    scene.wait(scene.seconds(p["scale_hold"]))

def _ct_context(scene):
    p = CONTINUITY
    n = p["decimal_powers"][0]
    view = _SqrtContinuityView(scene,p,10.0 ** (-n),p["intro_width"],input_reveal = 1.0)
    view.tick_precision.set_value(n)
    view.dimension_index.set_value(n)
    view.fraction.set_value(p["initial_fraction"])
    view.geometry.update(0)
    context = {"view":view,"n":n}
    context["title"] = _ct_formula(view,[r"f(x)=\sqrt{x}"],{},"title")

    for kind in ("delta","epsilon"):
        context[kind + "_card"] = _ct_card(view,n,kind)

    scene.play(FadeIn(view.geometry),FadeIn(context["title"]), FadeIn(context["delta_card"]),FadeIn(context["epsilon_card"]),run_time = scene.seconds(p["intro_time"]))

    return context

def _ct_decimal_phase(scene, context):
    view,p = context["view"],context["view"].p
    scene.play(view.fraction.animate.set_value(0),run_time = scene.seconds(p["approach_time"]))

    for n in p["decimal_powers"]:
        _ct_refine(scene,context,n)

    _ct_cards_to_formula(scene,context)
    scene.wait(scene.seconds(p["quantifier_hold"]))

    for base in p["display_bases"]:
        _ct_morph(scene,context,"main",_ct_quantified(view,base))
        scene.wait(scene.seconds(p["base_hold"]))

    scene.wait(scene.seconds(p["phase_hold"]))

def _ct_bridge_from_bound(scene, context):
    view,p = context["view"],context["view"].p
    base = p["display_bases"][-1]
    bridge = _ct_formula(view,[r"\forall",r"\varepsilon>0,",r"\exists n\ge1:", rf"\frac{{1}}{{{base}^n}}",r"<",r"\varepsilon"], {1:"output",3:"output",5:"output"},"bridge")
    updaters = _ct_suspend(bridge)
    clone = context["main"][10].copy().clear_updaters(recursive = True)
    scene.add(clone)
    scene.play(
        ReplacementTransform(clone,bridge[3]),
        LaggedStart(*[Write(bridge[i], stroke_width = p["formula_write_width"] * view.scale()) for i in (0,1,2,4,5)],lag_ratio = p["grammar_lag"]),
        run_time = scene.seconds(p["formula_time"])
    )
    scene.remove(clone,*list(bridge))
    _ct_restore(scene,bridge,updaters)
    context["bridge"] = bridge

def _ct_bound_to_epsilon(scene, context):
    view,p = context["view"],context["view"].p
    base = p["display_bases"][-1]
    focus = _ct_formula(view,[rf"\frac{{1}}{{{base}^n}}"],{0:"output"},"focus")
    _ct_from_copy(scene,context,context["main"][10],focus,"focus",p["focus_move_time"])
    scene.wait(scene.seconds(p["focus_hold"]))
    _ct_morph(scene,context,"focus",_ct_formula(view,[r"\varepsilon"],{0:"output"},"focus"),p["bound_to_epsilon_time"])
    new = _ct_quantified(view)
    old, focus = context["main"],context.pop("focus")
    _ct_suspend(old)
    _ct_suspend(focus)
    updaters = _ct_suspend(new)
    old_parts,new_parts = list(old),list(new)
    scene.remove(old)
    scene.add(*old_parts)
    scene.play(
        *[ReplacementTransform(a,b) for a,b in zip(old_parts[:10],new_parts[:10])],
        FadeOut(old_parts[10]),ReplacementTransform(focus,new_parts[10],path_arc = p["label_path_arc"]),
        run_time = scene.seconds(p["focus_return_time"]),rate_func = smooth
    )
    scene.remove(*old_parts,*new_parts,focus)
    _ct_restore(scene,new,updaters)
    context["main"] = new
    view.dimension_index.set_value(-1)

def _ct_general_phase(scene, context):
    view,p = context["view"],context["view"].p
    scene.play(view.visual_opacity.animate.set_value(p["final_graph_opacity"]), FadeOut(context.pop("title")),run_time = scene.seconds(p["dim_time"]))

    # The cofinal-scale inequality stays visible during the substitution: the
    # animation replaces the error bound; it never asserts b**(-n) == epsilon.
    _ct_bridge_from_bound(scene,context)
    scene.wait(scene.seconds(p["bridge_hold"]))
    _ct_bound_to_epsilon(scene,context)
    _ct_from_copy(scene,context,context["main"],_ct_quantified(view,generic = True,slot = "definition"), "definition",p["definition_copy_time"])
    scene.wait(scene.seconds(p["definition_hold"]))
    specialization = _ct_formula(view,[r"f(x)=\sqrt{x},\qquad x_0=2"],{},"bridge")
    _ct_morph(scene,context,"bridge",specialization)
    scene.wait(scene.seconds(p["equivalence_hold"]))
    proof = _ct_formula(
        view,[
            r"\delta",r"=\min\bigl(1,\sqrt{2}",r"\varepsilon",r"\bigr)>0,\quad",
            r"|x-2|<",r"\delta",r"\Longrightarrow",r"|\sqrt{x}-\sqrt{2}|",
            r"=\frac{|x-2|}{\sqrt{x}+\sqrt{2}}",r"<",r"\varepsilon"
        ],
        {0:"input",2:"output",5:"input",10:"output"},"proof"
    )
    _ct_morph(scene,context,"bridge",proof,p["proof_transform_time"])
    scene.wait(scene.seconds(p["proof_flash_wait"]))
    s = view.scale()
    outline = SurroundingRectangle(proof, buff = p["proof_flash_buff"] * s, color = p["proof_flash_color"], stroke_width = p["proof_flash_width"] * s)
    outline.set_z_index(p["hud_z_index"] + 1)
    scene.play(
        ShowPassingFlash(outline,time_width = p["proof_flash_time_width"]),
        run_time = scene.seconds(p["proof_flash_time"]),rate_func = linear
    )
    scene.wait(scene.seconds(p["final_hold"]))

def build_continuity_story(scene):
    context = _ct_context(scene)
    _ct_decimal_phase(scene,context)
    _ct_general_phase(scene,context)

# 独立渲染入口（按文案顺序）；ContinuityFilm 将五个分镜连起来
class _StoryboardTiming:
    def setup(self):
        super().setup()
        validate_parameters()
        self.camera.background_color = BG_COLOR
        self.camera.frame.set_width(FRAME_WIDTH).move_to(ORIGIN)

    def seconds(self, value):

        return value * TIME_SCALE

def validate_parameters():
    if TIME_SCALE <= 0:
        raise ValueError("TIME_SCALE must be positive.")
    if DIGITS["count"] < DIGITS["mismatch"]:
        raise ValueError("The comparison needs at least mismatch digits.")
    if not 1 <= DIGITS["slow_last"] < DIGITS["fast_stop"] < DIGITS["mismatch"]:
        raise ValueError("Require slow_last < fast_stop < mismatch.")
    if not 1 <= DIGITS["precision_steps"] < DIGITS["mismatch"]:
        raise ValueError("Only matching decimal places can be used in the precision demonstration.")
    comparison_decimals()
    p = CONTINUITY
    if p["delta_cap"] != 1.0:
        raise ValueError("Keep delta_cap=1 to match the displayed delta construction.")
    powers = p["decimal_powers"]
    if not powers or any(not isinstance(n,int) or n < 1 or n > p["tick_max_precision"] for n in powers) or any(a >= b for a,b in zip(powers,powers[1:])):
        raise ValueError("decimal_powers must increase within 1..tick_max_precision.")
    if any(n not in p["dimension_indices"] for n in powers):
        raise ValueError("dimension_indices must include every displayed decimal power.")
    if not p["display_bases"] or any(float(base) <= 1 for base in p["display_bases"]):
        raise ValueError("Every displayed base must exceed 1.")
    if not 0 < p["epsilon_axis_fraction_max"] <= 0.5 or p["clip_y"][1] <= p["ruler_y"]:
        raise ValueError("The epsilon band must use at most half of a positive vertical axis height.")
    if p["width_per_error"] < _ct_minimum_frame_width(p,1.0):
        raise ValueError("width_per_error is too small for the epsilon band height limit.")
    if p["width_per_error"] <= 0 or p["intro_width"] < p["width_per_error"] * 10 ** (-powers[0]):
        raise ValueError("The camera must start at or outside the first error scale.")
    if not 0 < p["error_lead_fraction"] <= 1 or not 0 <= p["final_graph_opacity"] <= 1:
        raise ValueError("The refinement lead and final opacity must lie in their unit intervals.")
    if len(p["sweep_fractions"]) != len(p["sweep_times"]) or any(abs(t) >= 1 for t in p["sweep_fractions"]):
        raise ValueError("Sweeps need matching durations and points strictly inside the interval.")

class WaterTemperature(_StoryboardTiming, MovingCameraScene):
    # 旋钮微动 → 温度跳变 → 修复为连续曲线 → 舒适水温
    def construct(self):
        build_water_temperature(self)

class CompareRealNumbers(_StoryboardTiming, MovingCameraScene):
    # 两行100位小数，向右扫描，第60位9/8不同，红框抖动
    def construct(self):
        build_real_comparison(self)

class DecimalCarry(_StoryboardTiming, MovingCameraScene):
    # 0.999…与1.000…：红框逐位抖动，以循环小数等于1收尾
    def construct(self):
        build_decimal_carry(self)

class DecimalPrecision(_StoryboardTiming, MovingCameraScene):
    # 从第60位拉回最左侧，绿框逐位提高10进制精度
    def construct(self):
        build_decimal_precision(self)

class ContinuityDefinition(_StoryboardTiming, MovingCameraScene):
    # 完整连续性分镜：刻度放大、换底数、epsilon-delta定义与严格推导
    def construct(self):
        build_continuity_story(self)

class ContinuityFilm(_StoryboardTiming, MovingCameraScene):
    # 五个分镜的顺序合集；独立Scene也可分别渲染和剪辑
    def construct(self):
        for index, builder in enumerate((
            build_water_temperature, build_real_comparison, build_decimal_carry,
            build_decimal_precision, build_continuity_story,
        )):
            if index:

                for mob in self.mobjects:
                    mob.clear_updaters(recursive = True)

                # 先淡出数字，保留遮罩到清屏，避免边缘在转场中反而变亮
                outgoing = [mob for mob in self.mobjects if not getattr(mob, "is_decimal_edge_mask", False)]
                self.play(*[FadeOut(mob) for mob in outgoing], run_time = self.seconds(TRANSITION_TIME))
                self.clear()
                self.camera.frame.clear_updaters()
                self.camera.frame.set_width(FRAME_WIDTH).move_to(ORIGIN)
                self.wait(self.seconds(TRANSITION_HOLD))
                
            builder(self)
