from manim import *
import numpy as np
from svgelements import Path as SVGPath
from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath

# 所有可调参数
BG_COLOR = "#000012"
FRAME_WIDTH, FRAME_HEIGHT = 128 / 9, 8.0
FRAME_RATE = None  # None 沿用命令行；可填60
TIME_SCALE = 1.0  # 全局速度：动画与停顿一起缩放
PALETTE = dict(
    axis = "#FFFFFF", ink = "#FFFFFF", cyan = "#56CEE8", green = "#9EE3A2",
    yellow = "#E8EE63", rose = "#EF819B", epsilon = "#FFE17D", safe = "#68E6C0",
    muted = "#687C98", error = "#FF526E",
)
STYLE = dict(
    axis_width = 2.0, curve_width = 4.2, line_width = 2.6, guide_width = 1.5,
    tick_size = 0.065, dot_radius = 0.041, focus_radius = 0.075, halo_radius = 0.18,
    halo_opacity = 0.10, outline_width = 1.4, outline_opacity = 0.35, cloud_opacity = 0.60,
    dim_opacity = 0.20, fill_opacity = 0.060, strip_opacity = 0.12, guide_opacity = 0.34,
    label_gap = 0.20, dash_length = 0.095, arrow_tip = 0.13, formula_size = 39,
    small_size = 29, point_label_size = 31, opening_size = 82, mapping_size = 46,
    max_formula_width = 12.4, curve_samples = 121, curve_segments = 40, segment_samples = 5,
    compare_lag = 0.045, curve_lag = 0.075, zero_length = 1e-6, path_tolerance = 1e-8,
)
# 第一镜：点列无间隙，数轴两端始终在画面外；颜色沿用PALETTE
OPENING = dict(
    mapping_position = (0, 0, 0), mapping_size = 82, retained_r_position = (-0.40, 2.10, 0),
    retained_r_size = 76, axis_length = 22.0, axis_y = -0.85, unit_length = 1.45,
    point_radius = 0.030, point_spacing = 0.042, point_opacity = 0.76, seed_radius = 0.007,
    flight_radius = None, flight_scale = 0.75, flight_opacity = 1.0,
    # flight_radius=None 时，以x、y点大小为基准，再乘flight_scale。
    takeoff_growth_fraction = 0.20, landing_shrink_fraction = 0.35, fall_time = 4.00, fall_flight_time = 0.55,
    fall_power = 2.0, show_ticks = True, tick_min = -7, tick_max = 7,
    tick_step = 1, tick_height = 0.09, tick_width = 1.55, show_numbers = True,
    number_gap = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, number_size = 28, number_edge_margin = 0.35,
    x_start = -2.0, y_start = 2.0, moves = ((-0.9, 2.5), (0.2, 1.1), (-2.4, 0.2), (-1.6, 1.7)),
    marker_radius = 0.075, label_y = -1.65, label_size = 34, brace_gap = 0.24,
    brace_height = 0.25, brace_sharpness = 2.0, formula_gap = 0.12, formula_size = 46,
    intro_time = 1.6, opening_hold = 1.4, seed_time = 0.18, retained_r_move_time = 0.90,
    tick_reveal_time = 0.12, line_hold = 1.2, reveal_time = 1.7, move_time = 2.3,
    move_hold = 0.30, distance_hold = 1.3, clear_time = 1.4, isolate_hold = 0.6,
    assemble_time = 2.0, final_position = (0, 0, 0), final_scale = 1.70, center_time = 1.80,
    final_hold = 2.7,
)

# 第二镜：公式变换、数轴上的三条距离性质。数轴尺寸沿用OPENING
AXIOMS = dict(
    intro_position = (0, 0, 0), intro_size = OPENING['mapping_size'], intro_arrow_tex = r'\longrightarrow',
    formula_size = 44, property_position = (0, 2.15, 0), formula_buff = 0.12, axis_y = 0.0,
    x_start = -2.0, y_start = 2.0, label_y = -0.90, label_size = 35,
    distance_label_gap = 0.18, segment_width = 4.2, mapping_arrow_tex = r'\longmapsto',
    show_axis_point_row = False, swap_angle = -PI / 3, coincidence_radius = 0.11, coincidence_width = 2.1,
    z_outside = 3.4, z_between = 0.3, route_y = (0.60, 1.08), guide_width = 1.3,
    guide_opacity = 0.24, guide_dash = 0.070, icon_color = PALETTE['rose'], icon_height = 1.10,
    icon_gap = 0.46, icon_width = 3.3,
    # B站网页VideoLike / VideoCoin原始矢量路径；无填充，只描边
    # 来源：https://s1.hdslb.com/bfs/static/jinkela/video/video.05af4e80b6081ba56c1b5b943d4c8e621df3f875.js
    like_paths = (
        'M9.77234 30.8573V11.7471H7.54573C5.50932 11.7471 3.85742 13.3931 3.85742 15.425V27.1794C3.85742 29.2112 5.50932 30.8573 7.54573 30.8573H9.77234ZM11.9902 30.8573V11.7054C14.9897 10.627 16.6942 7.8853 17.1055 3.33591C17.2666 1.55463 18.9633 0.814421 20.5803 1.59505C22.1847 2.36964 23.243 4.32583 23.243 6.93947C23.243 8.50265 23.0478 10.1054 22.6582 11.7471H29.7324C31.7739 11.7471 33.4289 13.402 33.4289 15.4435C33.4289 15.7416 33.3928 16.0386 33.3215 16.328L30.9883 25.7957C30.2558 28.7683 27.5894 30.8573 24.528 30.8573H11.9911H11.9902Z',
    ),
    coin_paths = (
        'M14.045 25.5454C7.69377 25.5454 2.54504 20.3967 2.54504 14.0454C2.54504 7.69413 7.69377 2.54541 14.045 2.54541C20.3963 2.54541 25.545 7.69413 25.545 14.0454C25.545 17.0954 24.3334 20.0205 22.1768 22.1771C20.0201 24.3338 17.095 25.5454 14.045 25.5454ZM9.66202 6.81624H18.2761C18.825 6.81624 19.27 7.22183 19.27 7.72216C19.27 8.22248 18.825 8.62807 18.2761 8.62807H14.95V10.2903C17.989 10.4444 20.3766 12.9487 20.3855 15.9916V17.1995C20.3854 17.6997 19.9799 18.1052 19.4796 18.1052C18.9793 18.1052 18.5738 17.6997 18.5737 17.1995V15.9916C18.5667 13.9478 16.9882 12.2535 14.95 12.1022V20.5574C14.95 21.0577 14.5444 21.4633 14.0441 21.4633C13.5437 21.4633 13.1382 21.0577 13.1382 20.5574V12.1022C11.1 12.2535 9.52148 13.9478 9.51448 15.9916V17.1995C9.5144 17.6997 9.10883 18.1052 8.60856 18.1052C8.1083 18.1052 7.70273 17.6997 7.70265 17.1995V15.9916C7.71158 12.9487 10.0992 10.4444 13.1382 10.2903V8.62807H9.66202C9.11309 8.62807 8.66809 8.22248 8.66809 7.72216C8.66809 7.22183 9.11309 6.81624 9.66202 6.81624Z',
    ),
    intro_write = 1.25, intro_morph = 1.35, intro_hold = 0.80, icon_hold = 1.20,
    axis_reveal = 1.70, points_reveal = 1.10, letters_move = 1.50, segment_reveal = 1.10,
    copy_lift = 0.60, copy_morph = 0.65, distance_label_hold = 0.35, formula_move = 1.25,
    operator_write = 0.80, property_hold = 1.50, clear_time = 0.75, collapse_time = 2.00,
    separate_time = 1.80, swap_time = 2.40, triangle_reveal = 1.30, triangle_move = 2.30,
    equality_hold = 1.10, triangle_negation_color = PALETTE['error'], triangle_slash_width = 2.6,
    triangle_slash_margin = 0.045, triangle_reverse_sign_gap = 0.14, triangle_slash_time = 0.60,
    triangle_reverse_sign_time = 0.80, triangle_negation_hold = 0.60,
    contradiction_tex = r'0=d(x,x)>d(x,y)+d(y,x)=2d(x,y)>0', contradiction_position = (0, -1.80, 0),
    contradiction_size = 34, contradiction_marker = r'\bot', contradiction_marker_size = 36,
    contradiction_marker_gap = 0.25, contradiction_color = PALETTE['error'], contradiction_write = 1.70,
    contradiction_hold = 2.40, summary_dim = 0.10, summary_position = (0, 0.20, 0), summary_size = 44,
    summary_gap = 0.55, summary_dim_time = 1.20, summary_write = 1.90, summary_hold = 2.10,
    summary_collapse_time = 2.10, summary_d_position = (0, 0, 0), summary_d_size = 156, summary_d_hold = 1.10,
    metric_pair_size = 112, metric_pair_position = (0, 0, 0), metric_pair_build = 1.70,
    metric_pair_hold = 1.20, metric_pair_upper = (0, 1.35, 0), metric_pair_lift = 1.40,
    continuity_intro_position = (0, -0.30, 0), continuity_intro_size = 43, continuity_intro_write = 1.60,
    continuity_intro_hold = 1.70, continuity_intro_morph = 1.80, continuity_intro_final_hold = 2.80,
    # 底部字幕安全区从y=-2.55开始；新增公式的下沿保持在其上
    subtitle_safe_bottom = -2.55,
)

# UniformDistance：NumberPlane默认网格颜色和线宽，透明度与疏密在此调整
UNIFORM = dict(
    plane_center = (0, -0.12, 0), x_range = (-0.10, 1.10, 0.25), y_range = (-0.10, 1.10, 0.25),
    difference_y_step = 0.125, x_length = 10.2, y_length = 3.8,
    # 参考part_two.py：横轴固定，纵向倍率按对数平滑变化，刻度字号不变
    vertical_zoom = 3.5, vertical_zoom_time = 2.80, zoom_tick_fade_start = 0.25, zoom_tick_fade_end = 0.80,
    zoom_edge_fade = 0.18, grid_opacity = 0.40, grid_faded_ratio = 0, domain = (0.0, 1.0),
    f_color = BLUE_C, g_color = RED_C, difference_color = PALETTE['green'],
    distance_color = PALETTE['epsilon'], curve_width = 4.2, segment_width = 3.4, point_radius = 0.060,
    # 与part_two.py的黎曼函数相同：按横坐标分为18档，青 -> 绿 -> 黄
    difference_gradient = (PALETTE['cyan'], PALETTE['green'], PALETTE['yellow']), gradient_bands = 18,
    segment_samples = 8, curve_samples = 121, axis_width = 2.0, tick_size = 0.050,
    number_size = 25, number_gap = 0.17, axis_label_size = 28, axis_label_gap = 0.17,
    x_ticks = (0.0, 0.5, 1.0), x_tick_tex = ('0', '0.5', '1.0'), y_ticks = (0.5, 1.0),
    y_tick_tex = ('0.5', '1.0'), difference_y_ticks = (0.125, 0.25),
    difference_y_tick_tex = ('0.125', '0.25'), formula_size = 43, header = (0, 2.85, 0),
    f_label = (-2.65, 2.85, 0), g_label = (2.65, 2.85, 0), domain_label = (0, 2.10, 0),
    domain_label_size = 27, scan_start = 0.15, scan_stops = (0.85, 0.18, 0.75, 0.30), maximum_x = 0.50,
    distance_offset = (0.45, 0, 0), distance_above_offset = (0.40, 0.38, 0), distance_size = 29,
    distance_decimals = 2, maximum_tex = '0.25', plane_reveal = 1.30, curves_reveal = 1.65,
    opening_hold = 1.00, endpoint_flash_time = 1.10, endpoint_flash_radius = 0.10,
    endpoint_flash_length = 0.16, endpoint_flash_lines = 12, endpoint_flash_width = 3.0,
    endpoint_flash_time_width = 0.35, membership_position = (0, 2.10, 0), membership_size = 32,
    membership_reveal = 1.10, segment_reveal = 1.00, scan_time = 2.10, scan_hold = 0.25,
    difference_morph = 2.50, difference_hold = 0.65, maximum_move = 1.80, formula_morph = 1.60,
    maximum_hold = 1.70, supremum_hold = 1.50, flash_color = YELLOW, flash_width = 3.0,
    flash_curve_width = 6.0, flash_time_width = 0.40, flash_time = 2.20, flash_curve = True,
    final_hold = 2.40,
)

LAYOUT = dict(
    header = (0, 3.05, 0), secondary = (0, 2.22, 0), subtitle_top = -2.55, set_label = (-5.78, 1.60, 0),
    x = (-3.25, -0.75, 0), y = (3.15, -0.75, 0), z = (1.05, 1.12, 0), property_formula = (0, 2.17, 0),
    contradiction = (0, -2.02, 0), triangle_fraction = 0.48, domain_center = (-3.55, -0.18, 0),
    codomain_center = (3.55, -0.18, 0), space_label_y = 1.70, anchor_label_y = -1.57, space_width = 4.70,
    space_height = 2.90, mapping_arrow_y = 0.70, mapping_arrow_half = 0.93, mapping_label = (0, 1.13, 0),
    continuity_formula = (0, -2.03, 0), domain_point = (-4.20, -0.40, 0), codomain_point = (2.90, -0.40, 0),
    continuity_delta = 0.85, continuity_epsilon = 1.02, continuity_scales = (1.0, 0.70, 0.43),
    probe_fractions = (0.73, -0.67, 0.46), delta_label_offset = (0.35, 0.23, 0),
    epsilon_label_offset = (0.47, 0.28, 0), probe_y_factor = 0.36, probe_output_factor = 0.63,
)
CLOUD = dict(
    count = 31, golden_angle = 2.399963229728653, radial_power = 0.55, half_width = 5.05,
    half_height = 1.32, center = (0, -0.10, 0), envelope_wobble = 0.10, envelope_samples = 96,
    small_count = 23, small_half_width = 1.90, small_half_height = 1.18,
)
PLOT = dict(
    origin = (-4.85, -1.65, 0), x_length = 9.60, y_length = 3.35, x_range = (0, 1.06, 0.25),
    y_range = (0, 1.10, 0.25), ticks = (0, 0.5, 1), tick_labels = ("0", r"\frac12", "1"),
    tick_label_size = 27, axis_label_size = 30, y_label_gap = 0.31, x_label_gap = 0.28,
    f_label = (-2.45, 1.98, 0), g_label = (2.36, 1.98, 0), max_x = 0.5, max_gap = 0.25,
    scan_start = 0.10, scan_stops = (0.22, 0.78, 0.50), sample_count = 21, sample_start = 0.045,
    sample_end = 0.955, sample_opacity = 0.28, sample_width = 1.8, maximum_label_offset = (0.60, 0.20, 0),
    maximum_label_size = 27, epsilon = 0.10, bounded_position = (0, 2.24, 0),
)
FUNCTIONS = dict(
    # [0,1]宽4.1，小于画面宽度的1/3；只显示白色横轴
    interval_width = 4.1, axis_width = 13.4, plane_center = (0, 0.00, 0), y_range = (-1.1, 1.1),
    y_length = 4.4, grid_x_step = 0.25, grid_opacity = 0.40, grid_faded_ratio = 0,
    axis_stroke_width = 2.0, boundary_color = WHITE, boundary_opacity = 0.70, boundary_width = 1.7,
    boundary_dash_length = 0.13, boundary_dash_ratio = 0.55, tick_size = 0.05, tick_gap = 0.18,
    tick_size_font = 27, tick_outline_color = BLACK, tick_outline_width = 4.0,
    axis_ticks = (-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0),
    axis_tick_tex = ('-1', '-0.5', '0', '0.5', '1', '1.5', '2'), x_label_size = 28, x_label_gap = 0.15,
    curve_count = 100, main_curve_count = 60, curve_seed = 23, curve_segments = 20,
    samples_per_segment = 6, dim_curve_levels = (0.72, 0.84), dim_curve_amplitude = (0.19, 0.24),
    dim_curve_samples = 257, curve_colors = (PALETTE['cyan'], PALETTE['green'], PALETTE['yellow']),
    curve_width = 4.2, curve_opacity = 0.93, curve_extent = 0.97, curve_bias_span = 0.63,
    curve_linear_amplitude = 0.20, curve_wave_amplitude = (0.32, 0.20, 0.11), model_amplitude_min = 0.55,
    dim_floor = 0.10, dim_decay = 1.80, dim_tail_start = 0.65, dim_tail_decay = 10.0,
    title_position = (0, 3.20, 0), title_size = 68, glyph_stroke_width = 1.7, dot_radius = 0.055,
    dot_color = PALETTE['green'], dot_arrival_radius = 0.018, dot_arrival_color = PALETTE['ink'],
    collapse_time = 0.12, flight_time = 0.65, glyph_form_time = 0.16, flight_lag = 0.045,
    flight_seed = 31, flight_lift = 1.05, flight_sway = 0.38, flight_angle = 2.399963,
    d_start = (-4.05, 3.20, 0), d_color = PALETTE['epsilon'], frame_color = YELLOW, frame_width = 3.0,
    frame_buffer = 0.22, frame_corner_radius = 0.10, frame_time_width = 0.40, final_f_color = BLUE_C,
    final_g_color = RED_C, final_curve_width = 4.2,
    # 直接选开场第54、57条曲线；其最大距离约0.0668，小于epsilon
    selected_curve_indices = (53, 56), epsilon = 0.14, band_color = GREEN_C, band_opacity = 0.09,
    band_edge_width = 2.0, band_edge_opacity = 0.90, band_dash_length = 0.14, band_dash_ratio = 0.65,
    epsilon_x = 1.08, epsilon_label_offset = (0.27, 0, 0), epsilon_label_size = 27,
    closing_formula_position = (0, 2.45, 0), closing_formula_size = 33, probe_start = 0.10,
    probe_stops = (0.90, 0.50), probe_width = 2.5, probe_radius = 0.034, plane_reveal = 1.40,
    boundary_reveal = 0.80, curves_reveal = 3.20, curves_lag = 0.045, curves_hold = 1.70,
    title_fill = 0.75, title_hold = 1.30, d_reveal = 1.00, d_hold = 0.40,
    pair_morph = 1.70, frame_flash = 1.80, pair_hold = 0.70, final_reveal = 1.90,
    probe_reveal = 0.75, probe_move = 2.10, probe_hold = 0.30, final_hold = 2.60,
    # 保留手动调用_thumbnail辅助函数的参数
    thumb_width = 0.65, thumb_height = 0.43, thumb_offset = (0.12, 0.23, 0),
)

GRID = dict(
    enabled = True, color = "#607089", opacity = 0.20, line_width = 0.80,
    plane_x_step = 1.0, plane_y_step = 1.0, graph_x_step = 0.10, graph_y_step = 0.20,
)
PLANE = dict(
    main_center = (0, -0.15, 0), main_width = 11.30, main_height = 3.10, main_x_range = (-7, 7, 1),
    x_range = (-3, 3, 1), y_range = (-2, 2, 1), tick_size = 0.045, label_size = 23,
    label_gap = 0.17, origin_offset = (-0.19, -0.21, 0),
)
TIMING = dict(
    write = 1.55, morph = 1.90, reveal = 1.50, fade = 0.72,
    bridge = 1.90, hold = 1.35, short_hold = 0.55, long_hold = 2.20,
    final_hold = 2.80, mapping_hold = 1.60, line_birth = 2.30, distance_move = 2.10,
    collapse = 1.80, unroll = 1.80, symmetry = 2.40, triangle = 2.70,
    trace = 1.70, radius_change = 2.10, probe = 1.50, scan = 2.55,
    max_hold = 2.30, function_gather = 2.65, function_close = 2.80,
)

# 动画实现
config.background_color = BG_COLOR
config.frame_width, config.frame_height = FRAME_WIDTH, FRAME_HEIGHT

if FRAME_RATE is not None:
    config.frame_rate = FRAME_RATE

def _v(value):
    return np.array(value, dtype = float)

def _tex(text, position = None, size = None, color = None):
    m = MathTex(text, font_size = size or STYLE["formula_size"], color = color or PALETTE["ink"])

    if m.width > STYLE["max_formula_width"]:
        m.scale_to_fit_width(STYLE["max_formula_width"])

    if position is not None:
        m.move_to(position)

    for part in m.get_family():
        if isinstance(part, VMobject):
            part.consider_points_equals = _precise_equal
            part.consider_points_equals_2d = _precise_equal

    return m.set_z_index(12)

def _formula_change(source, target):
    # 公式先淡出再淡入；几何对象继续运动，避免异形字形相互拉扯
    return Succession(FadeOut(source), FadeIn(target))

def _follow_label(text, position_fn, color, direction = None):
    # 只移动已有字形，不逐帧重建MathTex，防止缓存轮廓被扰动
    mob = _tex(text, size = STYLE["point_label_size"], color = color)

    def place(m):

        if direction is None:
            m.move_to(position_fn())
        else:
            m.next_to(position_fn(), direction, buff = STYLE["label_gap"])

    mob.add_updater(place)
    place(mob)

    return mob

def _precise_equal(a, b):

    return bool(np.all(np.abs(np.asarray(a) - np.asarray(b)) <= STYLE["path_tolerance"]))

def _dot(p, color, focus = False):

    return Dot(
        p, radius = STYLE["focus_radius"] if focus else STYLE["dot_radius"], color = color
    ).set_z_index(7)

def _outline(center, width, height):
    wobble = CLOUD["envelope_wobble"]
    pts = [
        _v(center)
        + np.array(
            [
                width / 2 * np.cos(a) * (1 + wobble * np.sin(3 * a)),
                height / 2 * np.sin(a) * (1 + wobble * np.cos(2 * a)),
                0,
            ]
        )
        for a in np.linspace(0, TAU, CLOUD["envelope_samples"])
    ]

    return (
        VMobject()
        .set_points_smoothly(pts)
        .set_stroke(PALETTE["muted"], STYLE["outline_width"], STYLE["outline_opacity"])
        .set_fill(PALETTE["cyan"], STYLE["fill_opacity"])
        .set_z_index(-3)
    )

def _cloud(center, count, half_width, half_height):
    colors = color_gradient([PALETTE["cyan"], PALETTE["green"], PALETTE["yellow"]], count)
    result = VGroup()

    for i in range(count):
        angle = i * CLOUD["golden_angle"]
        radius = ((i + 1) / (count + 1)) ** CLOUD["radial_power"]
        p = _v(center) + np.array(
            [half_width * radius * np.cos(angle), half_height * radius * np.sin(angle), 0]
        )
        result.add(_dot(p, colors[i]).set_opacity(STYLE["cloud_opacity"]))

    return result

def _distance_line(a, b, color):
    a, b = _v(a), _v(b)

    if np.linalg.norm(b - a) < STYLE["zero_length"]:
        return Line(a, a + STYLE["zero_length"] * RIGHT, stroke_opacity = 0)
    
    return Line(a, b, color = color, stroke_width = STYLE["line_width"])

def _dimension(a, b, color):
    caps = VGroup(
        *[
            Line(
                p - STYLE["tick_size"] * UP,
                p + STYLE["tick_size"] * UP,
                color = color,
                stroke_width = STYLE["line_width"],
            )
            for p in (_v(a), _v(b))
        ]
    )

    return VGroup(_distance_line(a, b, color), caps)

def _curve(axes, fn, gradient = False, color = None):

    if gradient:
        pieces = VGroup()
        edges = np.linspace(0, 1, STYLE["curve_segments"] + 1)
        colors = color_gradient(
            [PALETTE["cyan"], PALETTE["green"], PALETTE["yellow"]], STYLE["curve_segments"]
        )

        for a, b, c in zip(edges[:-1], edges[1:], colors):
            pts = [axes.c2p(t, fn(t)) for t in np.linspace(a, b, STYLE["segment_samples"])]
            pieces.add(VMobject().set_points_smoothly(pts).set_stroke(c, STYLE["curve_width"]))

        return pieces.set_z_index(4)
    
    pts = [axes.c2p(t, fn(t)) for t in np.linspace(0, 1, STYLE["curve_samples"])]

    return (
        VMobject()
        .set_points_smoothly(pts)
        .set_stroke(color or PALETTE["rose"], STYLE["curve_width"])
        .set_z_index(4)
    )

def _grid_lines(axes, x_bounds, y_bounds, x_step, y_step):
    grid = VGroup()

    if not GRID["enabled"]:
        return grid
    
    xmin, xmax = x_bounds
    ymin, ymax = y_bounds

    for k in range(int(np.ceil(xmin / x_step)), int(np.floor(xmax / x_step)) + 1):
        x = k * x_step
        if abs(x) > STYLE["zero_length"]:
            grid.add(Line(axes.c2p(x, ymin), axes.c2p(x, ymax)))

    for k in range(int(np.ceil(ymin / y_step)), int(np.floor(ymax / y_step)) + 1):
        y = k * y_step
        if abs(y) > STYLE["zero_length"]:
            grid.add(Line(axes.c2p(xmin, y), axes.c2p(xmax, y)))

    return grid.set_stroke(GRID["color"], GRID["line_width"], GRID["opacity"]).set_z_index(-3)

def _axes(origin = None, x_length = None, y_length = None, detail = False):
    axes = Axes(
        x_range = PLOT["x_range"],
        y_range = PLOT["y_range"],
        x_length = x_length or PLOT["x_length"],
        y_length = y_length or PLOT["y_length"],
        tips = False,
        axis_config = dict(
            color = PALETTE["axis"],
            stroke_width = STYLE["axis_width"],
            include_ticks = False,
            include_numbers = False,
        ),
    )
    axes.shift(_v(origin or PLOT["origin"]) - axes.c2p(0, 0))
    grid = _grid_lines(axes, (0, 1), (0, 1), GRID["graph_x_step"], GRID["graph_y_step"])
    art = VGroup(grid, axes)

    for value, label in zip(PLOT["ticks"], PLOT["tick_labels"]):
        p = axes.c2p(value, 0)
        art.add(
            Line(
                p - STYLE["tick_size"] * UP,
                p + STYLE["tick_size"] * UP,
                color = PALETTE["axis"],
                stroke_width = STYLE["axis_width"],
            )
        )
        art.add(
            _tex(label, size = PLOT["tick_label_size"]).next_to(p, DOWN, buff = PLOT["x_label_gap"])
        )

    for value in PLOT["ticks"][1:]:
        p = axes.c2p(0, value)
        art.add(
            Line(
                p - STYLE["tick_size"] * RIGHT,
                p + STYLE["tick_size"] * RIGHT,
                color = PALETTE["axis"],
                stroke_width = STYLE["axis_width"],
            )
        )
        label = r"\frac12" if value == 0.5 else "1"
        number = _tex(label, size = PLOT["tick_label_size"]).next_to(
            p, LEFT, buff = PLOT["y_label_gap"]
        )

        if detail:
            number.set_opacity(0)
        art.add(number)
    art.add(
        _tex("t" if detail else "x", size = PLOT["axis_label_size"]).next_to(
            axes.x_axis.get_end(), RIGHT, buff = STYLE["label_gap"]
        )
    )

    return axes, art

def _coordinate_plane(center, width, height, labels = False):
    # 平面直角坐标用于承载几何示意；三角形展示欧氏距离的实例
    # 在一般(X,d)中，屏幕的像素长度不用于定义d
    xr = PLANE["main_x_range"] if labels else PLANE["x_range"]
    axes = Axes(
        x_range = xr,
        y_range = PLANE["y_range"],
        x_length = width,
        y_length = height,
        tips = False,
        axis_config = dict(
            color = PALETTE["axis"],
            stroke_width = STYLE["axis_width"],
            include_numbers = False,
            include_ticks = True,
            tick_size = PLANE["tick_size"],
        ),
    )
    axes.shift(_v(center) - axes.c2p(0, 0))
    grid = _grid_lines(
        axes, xr[:2], PLANE["y_range"][:2], GRID["plane_x_step"], GRID["plane_y_step"]
    )
    art = VGroup(grid, axes)
    art.add(_tex("0", _v(center) + _v(PLANE["origin_offset"]), PLANE["label_size"]))

    if labels:
        art.add(
            _tex(r"\xi_1", size = PLANE["label_size"]).next_to(
                axes.x_axis.get_end(), RIGHT, buff = PLANE["label_gap"]
            )
        )
        art.add(
            _tex(r"\xi_2", size = PLANE["label_size"]).next_to(
                axes.y_axis.get_end(), UP, buff = PLANE["label_gap"]
            )
        )

    return art.set_z_index(-2)

def _thumbnail(point, fn, color):
    p = _v(point) + _v(FUNCTIONS["thumb_offset"])
    pts = [
        p
        + np.array(
            [FUNCTIONS["thumb_width"] * (t - 0.5), FUNCTIONS["thumb_height"] * (fn(t) - 0.5), 0]
        )
        for t in np.linspace(0, 1, STYLE["curve_samples"])
    ]

    return VMobject().set_points_smoothly(pts).set_stroke(color, STYLE["line_width"]).set_z_index(5)

def _axiom_tex(*parts, size = None):
    m = MathTex(
        *parts,
        font_size = size or AXIOMS['formula_size'],
        substrings_to_isolate = ['d', 'x', 'y', 'z'],
        color = PALETTE['ink'],
    )

    for letter, color in [
        ('d', PALETTE['epsilon']),
        ('x', PALETTE['cyan']),
        ('y', PALETTE['rose']),
        ('z', PALETTE['green']),
    ]:
        m.set_color_by_tex(letter, color, substring = False)

    for part in m.get_family():
        if isinstance(part, VMobject):
            part.consider_points_equals = _precise_equal
            part.consider_points_equals_2d = _precise_equal

    return m.set_z_index(12)

def _axiom_row(*parts):

    return (
        VGroup(*[_axiom_tex(part) for part in parts])
        .arrange(RIGHT, buff = AXIOMS['formula_buff'])
        .move_to(AXIOMS['property_position'])
    )

def _axiom_mapsto():
    # 映射箭头沿用同一行公式的字号，不单独放大或拉伸
    return _axiom_tex(AXIOMS['mapping_arrow_tex'])

def _axiom_icons():
    p = AXIOMS

    def outline(paths):
        pieces = VGroup(*[VMobjectFromSVGPath(SVGPath(path)) for path in paths])
        # SVG的纵轴向下；转成Manim方向后，保持官方图标的原始比例。
        pieces.flip(RIGHT).center().scale_to_fit_height(p['icon_height'])

        return pieces.set_stroke(p['icon_color'], p['icon_width']).set_fill(opacity = 0)

    thumb = outline(p['like_paths'])
    coin = outline(p['coin_paths'])
    icons = (
        VGroup(
            _axiom_tex('f:', size = p['intro_size']),
            thumb,
            _axiom_tex(p['intro_arrow_tex'], size = p['intro_size']),
            coin,
        )
        .arrange(RIGHT, buff = p['icon_gap'])
        .move_to(p['intro_position'])
        .set_z_index(12)
    )

    for part in icons.get_family():
        if isinstance(part, VMobject):
            part.consider_points_equals = _precise_equal
            part.consider_points_equals_2d = _precise_equal

    return icons

def _axiom_axis():
    p = OPENING
    length = max(p['axis_length'], FRAME_WIDTH + 2 * p['point_radius'])
    y = AXIOMS['axis_y']
    row = VGroup().set_z_index(1)

    if AXIOMS['show_axis_point_row']:
        count = int(np.ceil(length / min(p['point_spacing'], 2 * p['point_radius']))) + 1
        colors = color_gradient([PALETTE['cyan'], PALETTE['green'], PALETTE['yellow']], count)
        row.add(
            *[
                Dot([u, y, 0], radius = p['point_radius'], color = c, fill_opacity = p['point_opacity'])
                for u, c in zip(np.linspace(-length / 2, length / 2, count), colors)
            ]
        )
    axis = Line(
        [-length / 2, y, 0],
        [length / 2, y, 0],
        color = PALETTE['axis'],
        stroke_width = STYLE['axis_width'],
    ).set_z_index(3)
    ticks = VGroup()

    if p['show_ticks']:
        for value in range(p['tick_min'], p['tick_max'] + 1, p['tick_step']):
            q = np.array([p['unit_length'] * value, y, 0])
            ticks.add(
                Line(
                    q - p['tick_height'] * UP,
                    q + p['tick_height'] * UP,
                    color = PALETTE['axis'],
                    stroke_width = p['tick_width'],
                )
            )
            if p['show_numbers'] and abs(q[0]) < FRAME_WIDTH / 2 - p['number_edge_margin']:
                ticks.add(
                    _tex(str(value), size = p['number_size'], color = PALETTE['axis']).next_to(
                        q, DOWN, buff = p['number_gap']
                    )
                )

    return VGroup(row, axis, ticks.set_z_index(3))

def _morph_glyphs(mobject):
    # 在同一层级变换真正的字形路径，避免MathTex的不同嵌套层级干扰插值
    return VGroup(*[part.copy() for part in mobject.family_members_with_points()]).set_z_index(30)

def _align_morph_glyphs(source, target):
    # 将首字形复制到同一位置补齐数量；全程保持字形不透明
    # 绝对值的首竖线因此可以直接展开为d_X(或d_Y(
    count = max(len(source), len(target))
    groups = []

    for group in (source, target):
        extra = count - len(group)
        groups.append(
            VGroup(
                *[group[0].copy() for _ in range(extra + 1)], *group.submobjects[1:]
            ).set_z_index(30)
        )

    return tuple(groups)

def _continuity_intro_tex(metric = False):
    p = AXIOMS

    if metric:
        left = r'd_X(x,x_0)<\delta'
        right = r'd_Y(f(x),f(x_0))<\varepsilon'
    else:
        left = r'|x-x_0|<\delta'
        right = r'|f(x)-f(x_0)|<\varepsilon'

    formula = MathTex(
        left,
        r'\Longrightarrow',
        right,
        font_size = p['continuity_intro_size'],
        substrings_to_isolate = [r'\delta', r'\varepsilon', r'd_X', r'd_Y'],
        color = PALETTE['ink'],
    )

    for token, color in [
        (r'\delta', PALETTE['cyan']),
        (r'\varepsilon', PALETTE['epsilon']),
        (r'd_X', PALETTE['cyan']),
        (r'd_Y', PALETTE['rose']),
    ]:
        formula.set_color_by_tex(token, color, substring = False)

    for part in formula.get_family():
        if isinstance(part, VMobject):
            part.consider_points_equals = _precise_equal
            part.consider_points_equals_2d = _precise_equal

    if formula.width > STYLE['max_formula_width']:
        formula.scale_to_fit_width(STYLE['max_formula_width'])

    return formula.move_to(p['continuity_intro_position']).set_z_index(30)

def _uniform_tex(text, position = None, size = None, color = None):
    p = UNIFORM
    mob = MathTex(
        text,
        font_size = size or p['formula_size'],
        color = color or PALETTE['ink'],
        substrings_to_isolate = [
            r'\max',
            r'\sup',
            p['maximum_tex'],
            r'd_\infty',
            r'f(x)',
            r'g(x)',
            'f',
            'g',
        ],
    )

    for token, shade in [
        (p['maximum_tex'], p['distance_color']),
        (r'd_\infty', p['distance_color']),
        (r'f(x)', p['f_color']),
        (r'g(x)', p['g_color']),
        ('f', p['f_color']),
        ('g', p['g_color']),
    ]:
        mob.set_color_by_tex(token, shade, substring = False)

    for part in mob.get_family():
        if isinstance(part, VMobject):
            part.consider_points_equals = _precise_equal
            part.consider_points_equals_2d = _precise_equal

    if mob.width > STYLE['max_formula_width']:
        mob.scale_to_fit_width(STYLE['max_formula_width'])
    if position is not None:
        mob.move_to(position)

    return mob.set_z_index(12)

def _uniform_plane(difference = False, zoom = None, tick_blend = None):
    p = UNIFORM
    gain = p['vertical_zoom'] if difference else 1.0

    if zoom is not None:
        gain = zoom

    live = zoom is not None
    yr = (
        p['y_range'][0] / gain,
        p['y_range'][1] / gain,
        p['difference_y_step'] if difference or live else p['y_range'][2],
    )
    # 网格沿用默认颜色与线宽，仅调整透明度及间距、取消细分线。
    plane = NumberPlane(
        x_range = p['x_range'],
        y_range = yr,
        x_length = p['x_length'],
        y_length = p['y_length'],
        tips = False,
        background_line_style = dict(stroke_opacity = p['grid_opacity']),
        faded_line_ratio = p['grid_faded_ratio'],
        axis_config = dict(
            stroke_color = PALETTE['axis'],
            stroke_width = p['axis_width'],
            include_ticks = False,
            include_numbers = False,
        ),
    )
    plane.move_to(p['plane_center'])
    plane.faded_line_style['stroke_opacity'] = p['grid_opacity']
    plane.faded_lines.set_stroke(opacity = p['grid_opacity'])

    if live:
        phase = 0.0 if tick_blend is None else tick_blend
        for line in plane.background_lines:
            delta = line.get_end() - line.get_start()
            if abs(delta[0]) > abs(delta[1]):
                value = plane.p2c(line.get_center())[1]
                old_grid = (
                    abs(value / p['y_range'][2] - round(value / p['y_range'][2]))
                    < STYLE['path_tolerance']
                )
                line.set_stroke(opacity = p['grid_opacity'] * (1.0 if old_grid else phase))

    plane.background_lines.set_z_index(-4)
    plane.faded_lines.set_z_index(-4)
    plane.x_axis.set_z_index(-2)
    plane.y_axis.set_z_index(-2)
    ticks = VGroup()

    for value, label in zip(p['x_ticks'], p['x_tick_tex']):
        q = plane.c2p(value, 0)
        ticks.add(
            Line(
                q - p['tick_size'] * UP,
                q + p['tick_size'] * UP,
                color = PALETTE['axis'],
                stroke_width = p['axis_width'],
            )
        )
        ticks.add(_tex(label, size = p['number_size']).next_to(q, DOWN, buff = p['number_gap']))

    y_values = p['difference_y_ticks'] if difference else p['y_ticks']
    y_labels = p['difference_y_tick_tex'] if difference else p['y_tick_tex']
    layers = [(y_values, y_labels, 1.0)]

    if live:
        layers = [
            (p['y_ticks'], p['y_tick_tex'], 1 - phase),
            (p['difference_y_ticks'], p['difference_y_tick_tex'], phase),
        ]

    for values, labels, opacity in layers:
        for value, label in zip(values, labels):
            q = plane.c2p(0, value)
            edge = min(plane.y_axis.get_end()[1] - q[1], q[1] - plane.y_axis.get_start()[1])
            visible = opacity * float(np.clip(edge / p['zoom_edge_fade'], 0, 1))
            tick = Line(
                q - p['tick_size'] * RIGHT,
                q + p['tick_size'] * RIGHT,
                color = PALETTE['axis'],
                stroke_width = p['axis_width'],
            )
            number = _tex(label, size = p['number_size']).next_to(q, LEFT, buff = p['number_gap'])
            ticks.add(tick.set_opacity(visible), number.set_opacity(visible))

    names = VGroup(
        _tex('x', size = p['axis_label_size']).next_to(
            plane.x_axis.get_end(), RIGHT, buff = p['axis_label_gap']
        ),
        _tex('y', size = p['axis_label_size']).next_to(
            plane.y_axis.get_end(), UP, buff = p['axis_label_gap']
        ),
    )

    return plane, VGroup(plane, ticks, names)

def _uniform_curve(plane, fn, color):
    p = UNIFORM
    count = p['gradient_bands']
    shades = color_gradient(color, count) if isinstance(color, (tuple, list)) else [color] * count
    edges = np.linspace(*p['domain'], count + 1)
    pieces = VGroup()

    for a, b, shade in zip(edges[:-1], edges[1:], shades):
        points = [plane.c2p(t, fn(t)) for t in np.linspace(a, b, p['segment_samples'])]
        pieces.add(VMobject().set_points_smoothly(points).set_stroke(shade, p['curve_width']))

    return pieces.set_z_index(4)

def _uniform_readout(plane, x, upper, lower, above = False):
    p = UNIFORM
    high, low = plane.c2p(x, upper(x)), plane.c2p(x, lower(x))
    label = DecimalNumber(
        abs(upper(x) - lower(x)),
        num_decimal_places = p['distance_decimals'],
        font_size = p['distance_size'],
        color = p['distance_color'],
    )

    for part in label.get_family():
        if isinstance(part, VMobject):
            part.consider_points_equals = _precise_equal
            part.consider_points_equals_2d = _precise_equal
    position = (
        high + _v(p['distance_above_offset'])
        if above
        else (high + low) / 2 + _v(p['distance_offset'])
    )

    return label.move_to(position).set_z_index(12)

def _uniform_difference_color(x):
    p = UNIFORM
    shades = color_gradient(p['difference_gradient'], p['gradient_bands'])
    a, b = p['domain']
    band = min(len(shades) - 1, max(0, int((x - a) / (b - a) * len(shades))))

    return shades[band]

def _uniform_flash_curve(plane):
    p = UNIFORM
    points = [plane.c2p(t, t - t * t) for t in np.linspace(*p['domain'], p['curve_samples'])]

    return (
        VMobject()
        .set_points_smoothly(points)
        .set_stroke(p['flash_color'], p['flash_curve_width'])
        .set_z_index(20)
    )

def _function_plane():
    p = FUNCTIONS
    half = (p['axis_width'] / p['interval_width'] - 1) / 2

    # 横纵网格在屏幕上的间距一致；自动适配区间宽度与纵向比例
    y_step = (
        p['interval_width'] * p['grid_x_step'] * (p['y_range'][1] - p['y_range'][0]) / p['y_length']
    )
    yr = (*p['y_range'], y_step)
    plane = NumberPlane(
        x_range = (-half, 1 + half, p['grid_x_step']),
        y_range = yr,
        x_length = p['axis_width'],
        y_length = p['y_length'],
        tips = False,
        background_line_style = dict(stroke_opacity = p['grid_opacity']),
        faded_line_ratio = p['grid_faded_ratio'],
        axis_config = dict(
            stroke_color = WHITE,
            stroke_width = p['axis_stroke_width'],
            include_ticks = False,
            include_numbers = False,
        ),
    )
    plane.move_to(p['plane_center'])
    plane.y_axis.set_opacity(0)
    plane.background_lines.set_z_index(-4)
    plane.faded_lines.set_z_index(-4)
    plane.x_axis.set_z_index(-2)
    guides = VGroup()

    for x in (0, 1):
        guides.add(
            DashedLine(
                plane.c2p(x, p['y_range'][0]),
                plane.c2p(x, p['y_range'][1]),
                color = p['boundary_color'],
                stroke_width = p['boundary_width'],
                dash_length = p['boundary_dash_length'],
                dashed_ratio = p['boundary_dash_ratio'],
            )
            .set_stroke(opacity = p['boundary_opacity'])
            .set_z_index(7)
        )

    marks = VGroup()

    for x, number in zip(p['axis_ticks'], p['axis_tick_tex']):
        q = plane.c2p(x, 0)
        label = _tex(number, size = p['tick_size_font']).next_to(q, DOWN, buff = p['tick_gap'])
        label.set_stroke(
            p['tick_outline_color'], width = p['tick_outline_width'], background = True
        ).set_z_index(19)
        marks.add(
            Line(
                q - p['tick_size'] * UP,
                q + p['tick_size'] * UP,
                color = WHITE,
                stroke_width = p['axis_stroke_width'],
            ).set_z_index(18),
            label,
        )

    xlabel = _tex('x', size = p['x_label_size']).next_to(
        plane.x_axis.get_end(), RIGHT, buff = p['x_label_gap']
    )

    return plane, VGroup(plane, guides, marks, xlabel)

def _function_models():
    p = FUNCTIONS
    rng = np.random.default_rng(p['curve_seed'])
    models = []

    for i, bias in enumerate(
        np.linspace(-p['curve_bias_span'], p['curve_bias_span'], p['main_curve_count'])
    ):
        phases = rng.uniform(-PI, PI, 3)
        amplitudes = rng.uniform(p['model_amplitude_min'], 1.0, 3) * np.array(
            p['curve_wave_amplitude']
        )
        slope = rng.uniform(-p['curve_linear_amplitude'], p['curve_linear_amplitude'])

        def fn(t, b = bias, a = amplitudes.copy(), ph = phases.copy(), s = slope):
            v = b + s * (2 * t - 1) + sum(a[k] * np.sin((k + 1) * PI * t + ph[k]) for k in range(3))
            return p['curve_extent'] * np.tanh(v / p['curve_extent'])

        models.append(fn)

    # 外层直接使用原函数的弯曲轮廓，缩放并平移，不使用近似水平的小波动
    extra = p['curve_count'] - p['main_curve_count']
    levels = np.linspace(*p['dim_curve_levels'], max(1, (extra + 1) // 2))
    sample_x = np.linspace(0, 1, p['dim_curve_samples'])

    for i in range(extra):
        level = levels[i // 2]
        sign = 1 if i % 2 == 0 else -1
        source = models[int(rng.integers(0, p['main_curve_count']))]
        ys = np.array([source(t) for t in sample_x])
        lo, span = float(ys.min()), float(ys.max() - ys.min())
        amplitude = rng.uniform(*p['dim_curve_amplitude'])

        def fn(t, b = level, s = sign, base = source, lower = lo, extent = span, a = amplitude):

            return s * (b + a * (2 * (base(t) - lower) / extent - 1))

        models.append(fn)

    return models

def _function_curve_shades(fn, color):
    p = FUNCTIONS
    count = p['curve_segments']
    base = color_gradient(color, count) if isinstance(color, (tuple, list)) else [color] * count
    centers = (np.arange(count) + 0.5) / count
    shades = []

    for t, shade in zip(centers, base):
        brightness = p['dim_floor'] + (1 - p['dim_floor']) * np.exp(-p['dim_decay'] * abs(fn(t)))

        # 外层亮度连续衰减，阈值处斜率为0，不产生突然变暗的色层
        brightness *= np.exp(-p['dim_tail_decay'] * max(0, abs(fn(t)) - p['dim_tail_start']) ** 2)
        shades.append(interpolate_color(ManimColor(BG_COLOR), ManimColor(shade), brightness))

    return shades

def _function_curve(plane, fn, color, width = None):
    p = FUNCTIONS
    parts = VGroup()
    edges = np.linspace(0, 1, p['curve_segments'] + 1)

    for a, b, shade in zip(edges[:-1], edges[1:], _function_curve_shades(fn, color)):
        coords = [plane.c2p(x, fn(x)) for x in np.linspace(a, b, p['samples_per_segment'])]
        parts.add(
            VMobject()
            .set_points_smoothly(coords)
            .set_stroke(shade, width or p['curve_width'], opacity = p['curve_opacity'])
        )

    return parts.set_z_index(4)

def _function_recolor(curve, fn, color):
    # 仅改变原曲线的颜色与线宽，不改变几何路径
    p = FUNCTIONS

    for part, shade in zip(curve, _function_curve_shades(fn, color)):
        part.set_stroke(shade, p['final_curve_width'], opacity = p['curve_opacity'])

    return curve

class _FunctionPointFlight(MoveAlongPath):
    # 将大小和颜色存为动画属性，让Manim缓存识别这些参数的修改
    def __init__(self, mobject, path, **kwargs):
        p = FUNCTIONS
        self.departure_radius = p['dot_radius']
        self.arrival_radius = p['dot_arrival_radius']
        self.departure_color = p['dot_color']
        self.arrival_color = p['dot_arrival_color']
        super().__init__(mobject, path, **kwargs)

    # 对同一个点同时移动、缩小、变白；每帧从出发形状计算，避免尺寸累积误差
    def begin(self):
        self._flight_center = self.mobject.get_center().copy()
        super().begin()

    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha)
        position = self.path.point_from_proportion(t)
        radius = (1 - t) * self.departure_radius + t * self.arrival_radius
        scale = radius / self.departure_radius

        for current, original in zip(self.mobject.get_family(), self.starting_mobject.get_family()):
            if original.has_points():
                current.set_points((original.get_points() - self._flight_center) * scale + position)

        self.mobject.set_color(
            interpolate_color(ManimColor(self.departure_color), ManimColor(self.arrival_color), t)
        )

def _function_title_chunks(title):
    p = FUNCTIONS
    glyphs = list(_morph_glyphs(title))
    count = p['curve_count']

    if count < len(glyphs):
        raise ValueError('FUNCTIONS.curve_count must cover every glyph of C([0,1]).')
    
    weights = np.array([max(g.get_num_curves(), 1) for g in glyphs], dtype = float)
    raw = (count - len(glyphs)) * weights / weights.sum()
    counts = 1 + np.floor(raw).astype(int)

    for index in np.argsort(-(raw - np.floor(raw)))[: count - counts.sum()]:
        counts[index] += 1

    chunks = []

    for glyph, n in zip(glyphs, counts):
        for index in range(n):
            part = glyph.copy().pointwise_become_partial(glyph, index / n, (index + 1) / n)
            part.set_fill(opacity = 0).set_stroke(WHITE, p['glyph_stroke_width']).set_z_index(20)
            chunks.append(part)

    return chunks

def _function_pair():
    p = FUNCTIONS
    pair = MathTex('(', r'C([0,1])', ',', r'd_\infty', ')', font_size = p['title_size'], color = WHITE)
    pair[3].set_color(p['d_color'])

    for part in pair.get_family():
        if isinstance(part, VMobject):
            part.consider_points_equals = _precise_equal
            part.consider_points_equals_2d = _precise_equal

    return pair.move_to(p['title_position']).set_z_index(20)

def _function_close_models():
    models = _function_models()
    i, j = FUNCTIONS['selected_curve_indices']

    return models[i], models[j]

class _MetricStory:
    def __init__(self, scene):
        self.s = scene
        scene.camera.background_color = BG_COLOR
        self.stage = None

    def beat(self, *animations, duration = "write", **kwargs):
        t = TIMING[duration] if isinstance(duration, str) else duration
        self.s.play(*animations, run_time = t * TIME_SCALE, **kwargs)

    def pause(self, duration = "hold"):
        self.s.wait(TIMING[duration] * TIME_SCALE)

    def metric_base(self):

        return dict(
            title = _tex(r"d:X\times X\longrightarrow[0,\infty)", LAYOUT["header"]),
            dots = _cloud(CLOUD["center"], CLOUD["count"], CLOUD["half_width"], CLOUD["half_height"]),
            border = _coordinate_plane(
                PLANE["main_center"], PLANE["main_width"], PLANE["main_height"], True
            ),
            label = _tex("X", LAYOUT["set_label"], STYLE["mapping_size"]),
        )

    def graph_base(self, ending = False):
        axes, art = _axes()
        labels = VGroup(
            _tex("f(x)=x", PLOT["f_label"], STYLE["small_size"], PALETTE["cyan"]),
            _tex("g(x)=x^2", PLOT["g_label"], STYLE["small_size"], PALETTE["rose"]),
        )
        title = _tex(
            (
                r"d_\infty(f,g)=\sup_{x\in I}|f(x)-g(x)|"
                if ending
                else r"f,\ g:[0,1]\longrightarrow\mathbb R"
            ),
            LAYOUT["header"],
        )
        obj = dict(
            axes = axes,
            art = art,
            f = _curve(axes, lambda x: x, True),
            g = _curve(axes, lambda x: x * x, color = PALETTE["rose"]),
            labels = labels,
            title = title,
        )

        if ending:
            labels.set_opacity(0)
            obj["bounded"] = _tex(
                r"f,g\in B(I,\mathbb R)", PLOT["bounded_position"], STYLE["small_size"]
            )

        return obj

    def real_line(self):
        s, p = self.s, OPENING
        flight_radius = (
            p["marker_radius"] if p["flight_radius"] is None else p["flight_radius"]
        ) * p["flight_scale"]

        def pause(key):
            s.wait(p[key] * TIME_SCALE)

        def point(value):

            return np.array([p["unit_length"] * value, p["axis_y"], 0])

        mapping = (
            MathTex(
                "f:", r"\mathbb R", r"\longrightarrow", r"\mathbb R", font_size = p["mapping_size"]
            )
            .move_to(p["mapping_position"])
            .set_z_index(12)
        )

        for part in mapping.get_family():
            if isinstance(part, VMobject):
                part.consider_points_equals = _precise_equal
                part.consider_points_equals_2d = _precise_equal

        self.beat(Write(mapping), duration = p["intro_time"])
        pause("opening_hold")

        # 拆开原式，后续确实保留原来的第二个R，并保留距离式中的原字母d
        source_r, retained_r = mapping[1], mapping[3]
        grammar = VGroup(mapping[0], mapping[2])
        s.remove(mapping)
        s.add(source_r, retained_r, grammar)
        length = max(p["axis_length"], FRAME_WIDTH + 2 * p["point_radius"])

        # 相邻圆点重叠：无论怎样调整密度，都不出现点间空隙
        spacing = min(p["point_spacing"], 2 * p["point_radius"])
        count = int(np.ceil(length / spacing)) + 1
        colors = color_gradient([PALETTE["cyan"], PALETTE["green"], PALETTE["yellow"]], count)
        row = VGroup(
            *[
                Dot(
                    [u, p["axis_y"], 0],
                    radius = p["point_radius"],
                    color = c,
                    fill_opacity = p["point_opacity"],
                )
                for u, c in zip(np.linspace(-length / 2, length / 2, count), colors)
            ]
        ).set_z_index(1)

        # 在原R的真实曲线上取点，不把点预排成矩形或方形
        curves = [
            glyph.get_nth_curve_function(k)
            for glyph in source_r.family_members_with_points()
            for k in range(glyph.get_num_curves())
        ]
        parameters = np.linspace(0, len(curves), count, endpoint = False)
        origins = np.array([curves[int(t)](t - int(t)) for t in parameters])

        # 打散出发顺序，让R的各个部位逐渐消散；落点仍从左到右
        order = np.argsort((np.arange(count) * CLOUD["golden_angle"] / TAU) % 1)
        origins = origins[order]
        seed = VGroup(
            *[
                Dot(q, radius = p["seed_radius"], color = c, fill_opacity = p["point_opacity"])
                for q, c in zip(origins, colors)
            ]
        ).set_z_index(1)
        line = Line(
            [-length / 2, p["axis_y"], 0],
            [length / 2, p["axis_y"], 0],
            color = PALETTE["axis"],
            stroke_width = STYLE["axis_width"],
        ).set_z_index(3)
        ticks = VGroup()
        tick_parts = []

        if p["show_ticks"]:

            for value in range(p["tick_min"], p["tick_max"] + 1, p["tick_step"]):
                q = point(value)
                mark = Line(
                    q - p["tick_height"] * UP,
                    q + p["tick_height"] * UP,
                    color = PALETTE["axis"],
                    stroke_width = p["tick_width"],
                )
                ticks.add(mark)
                tick_parts.append((q[0], mark))

                if p["show_numbers"] and abs(q[0]) < FRAME_WIDTH / 2 - p["number_edge_margin"]:
                    number = _tex(str(value), size = p["number_size"], color = PALETTE["axis"])
                    number.next_to(q, DOWN, buff = p["number_gap"])
                    ticks.add(number)
                    tick_parts.append((q[0], number))

        ticks.set_z_index(3).set_opacity(0)
        line.set_opacity(0)
        self.beat(ReplacementTransform(source_r, seed), duration = p["seed_time"])
        drop_art = VGroup(seed, line, ticks)

        # 字形化成点后立刻出发；数轴和留下的R同步就位，没有点簇等待阶段
        flight = np.clip(p["fall_flight_time"] / p["fall_time"], STYLE["zero_length"], 1.0)
        starts = np.linspace(0, 1 - flight, count)
        destinations = np.array([dot.get_center() for dot in row])
        unit_circle = (row[0].get_points() - row[0].get_center()) / p["point_radius"]

        def drop_points(m, alpha):
            phases = np.clip((alpha - starts) / flight, 0, 1)

            for dot, origin, target, phase in zip(m[0], origins, destinations, phases):
                position = (1 - phase) * origin + phase * target
                position[1] = origin[1] + (target[1] - origin[1]) * phase ** p["fall_power"]
                if phase >= 1:
                    radius = p["point_radius"]
                    opacity = p["point_opacity"]
                    depth = 1
                elif phase > 0:
                    growth = np.clip(phase / p["takeoff_growth_fraction"], 0, 1)
                    growth = growth * growth * (3 - 2 * growth)
                    shrink = np.clip(
                        (phase - (1 - p["landing_shrink_fraction"])) / p["landing_shrink_fraction"],
                        0,
                        1,
                    )
                    shrink = shrink * shrink * (3 - 2 * shrink)
                    radius = p["seed_radius"] + (flight_radius - p["seed_radius"]) * growth
                    radius = (1 - shrink) * radius + shrink * p["point_radius"]
                    opacity = (
                        p["point_opacity"] + (p["flight_opacity"] - p["point_opacity"]) * growth
                    )
                    opacity = (1 - shrink) * opacity + shrink * p["point_opacity"]
                    depth = 5
                else:
                    radius = p["seed_radius"]
                    opacity = p["point_opacity"]
                    depth = 1

                # 起飞与落地尺寸连续变化，飞行中段保持大圆点
                dot.set_points(unit_circle * radius + position)
                dot.set_fill(opacity = opacity).set_z_index(depth)

            # 白色数轴只延伸到已落定的最后一个点，与落点共用同一时钟
            landed = np.flatnonzero(phases >= 1)

            if len(landed):
                front = destinations[landed[-1], 0]
                front = max(front, -length / 2 + STYLE["zero_length"])
                m[1].set_points_as_corners(
                    [[-length / 2, p["axis_y"], 0], [front, p["axis_y"], 0]]
                ).set_opacity(1)
            else:
                m[1].set_opacity(0)

            for u, part in tick_parts:
                arrival = flight + (1 - flight) * np.clip((u + length / 2) / length, 0, 1)
                reveal = np.clip((alpha - arrival) / (p["tick_reveal_time"] / p["fall_time"]), 0, 1)
                part.set_opacity(reveal * reveal * (3 - 2 * reveal))

        context = AnimationGroup(
            FadeOut(grammar),
            retained_r.animate.scale(p["retained_r_size"] / p["mapping_size"]).move_to(
                p["retained_r_position"]
            ),
            run_time = p["retained_r_move_time"],
        )
        self.beat(
            AnimationGroup(
                UpdateFromAlphaFunc(
                    drop_art, drop_points, rate_func = linear, run_time = p["fall_time"]
                ),
                context,
                lag_ratio = 0,
                rate_func = linear,
            ),
            duration = p["fall_time"],
        )
        s.remove(drop_art)
        s.add(row, line, ticks)
        pause("line_hold")
        x, y = ValueTracker(p["x_start"]), ValueTracker(p["y_start"])
        px = Dot(
            point(x.get_value()), radius = p["marker_radius"], color = PALETTE["cyan"]
        ).set_z_index(7)
        py = Dot(
            point(y.get_value()), radius = p["marker_radius"], color = PALETTE["rose"]
        ).set_z_index(7)
        px.add_updater(lambda m: m.move_to(point(x.get_value())))
        py.add_updater(lambda m: m.move_to(point(y.get_value())))
        xlab = _tex("x", size = p["label_size"], color = PALETTE["cyan"])
        ylab = _tex("y", size = p["label_size"], color = PALETTE["rose"])
        xlab.add_updater(lambda m: m.move_to([point(x.get_value())[0], p["label_y"], 0]))
        ylab.add_updater(lambda m: m.move_to([point(y.get_value())[0], p["label_y"], 0]))
        xlab.update(0)
        ylab.update(0)

        def current_brace():
            lo, hi = sorted((x.get_value(), y.get_value()))
            hi = max(hi, lo + STYLE["zero_length"])
            brace = BraceBetweenPoints(
                point(lo),
                point(hi),
                direction = UP,
                buff = p["brace_gap"],
                sharpness = p["brace_sharpness"],
                color = PALETTE["epsilon"],
            )
            bottom = brace.get_bottom().copy()
            brace.stretch_to_fit_height(p["brace_height"])
            brace.shift(bottom - brace.get_bottom())

            return brace.set_z_index(6)

        bracket = always_redraw(current_brace)
        formula = MathTex(
            "d",
            r"(x,y)=|x-y|",
            font_size = p["formula_size"],
            substrings_to_isolate = ["x", "y"],
            color = PALETTE["ink"],
        ).set_z_index(12)
        formula[0].set_color(PALETTE["epsilon"])
        formula.set_color_by_tex("x", PALETTE["cyan"])
        formula.set_color_by_tex("y", PALETTE["rose"])

        for part in formula.get_family():
            if isinstance(part, VMobject):
                part.consider_points_equals = _precise_equal
                part.consider_points_equals_2d = _precise_equal

        formula.add_updater(lambda m: m.next_to(bracket, UP, buff = p["formula_gap"]))
        formula.update(0)
        self.beat(
            FadeIn(px),
            FadeIn(py),
            FadeIn(xlab),
            FadeIn(ylab),
            FadeIn(bracket),
            Write(formula),
            duration = p["reveal_time"],
        )

        for next_x, next_y in p["moves"]:
            self.beat(
                x.animate.set_value(next_x), y.animate.set_value(next_y), duration = p["move_time"]
            )
            pause("move_hold")

        pause("distance_hold")

        for mob in (px, py, xlab, ylab, bracket, formula):
            mob.clear_updaters()

        d, tail = formula[0], VGroup(*formula.submobjects[1:])
        s.remove(formula)
        s.add(d, tail)
        self.beat(
            FadeOut(VGroup(row, line, ticks, px, py, xlab, ylab, bracket, tail)),
            duration = p["clear_time"],
        )
        pause("isolate_hold")
        pair = MathTex(
            "(", r"\mathbb R", ",", "d", ")", font_size = p["retained_r_size"], color = PALETTE["ink"]
        ).set_z_index(12)

        for part in pair.get_family():
            if isinstance(part, VMobject):
                part.consider_points_equals = _precise_equal
                part.consider_points_equals_2d = _precise_equal

        pair[3].set_color(PALETTE["epsilon"])

        # 以留下来的R为锚点，d从下方距离式移动到它的右侧
        pair.shift(retained_r.get_center() - pair[1].get_center())
        punctuation = VGroup(pair[0], pair[2], pair[4])
        self.beat(
            Transform(d, pair[3]),
            Transform(retained_r, pair[1]),
            FadeIn(punctuation),
            duration = p["assemble_time"],
        )
        s.clear()
        s.add(pair)
        self.beat(
            pair.animate.scale(p["final_scale"]).move_to(p["final_position"]),
            duration = p["center_time"],
        )
        pause("final_hold")
        self.stage = {"real_metric": pair}

    def real_to_plane(self):
        # 仅用于整片串联；独立第一镜严格停在(R,d)，不提前展开第二镜
        pair = self.stage["real_metric"]
        base = self.metric_base()
        self.beat(
            _formula_change(pair, base["title"]),
            Create(base["border"]),
            FadeIn(base["dots"]),
            FadeIn(base["label"]),
            duration = "bridge",
        )
        self.stage = base

    def metric_axioms(self):
        s, p = self.s, AXIOMS

        def beat(*animations, key):
            self.beat(*animations, duration = p[key])

        def hold(key = 'property_hold'):
            s.wait(p[key] * TIME_SCALE)

        def point(value):

            return np.array([OPENING['unit_length'] * value, p['axis_y'], 0])

        def live_label(letter, track):
            label = _axiom_tex(letter, size = p['label_size'])
            label.add_updater(
                lambda m: m.move_to(
                    track.get_center() + np.array([0, p['label_y'] - p['axis_y'], 0])
                )
            )
            label.update(0)

            return label

        def stable(*objects):
            s.clear()
            s.add(*objects)

        def distance_from_segment(source, text):
            label = _axiom_tex(text).next_to(source, UP, buff = p['distance_label_gap'])
            trace = source.copy().clear_updaters()
            s.add(trace)
            beat(
                trace.animate.scale_to_fit_width(label.width).move_to(label.get_center()),
                key = 'copy_lift',
            )
            beat(FadeTransform(trace, label, stretch = False), key = 'copy_morph')
            s.remove(trace)
            s.add(label)
            hold('distance_label_hold')

            return label

        # 依照草图逐个变换，始终只展示一组居中的映射
        opening = _axiom_tex(
            'f:', r'\mathbb R', p['intro_arrow_tex'], r'\mathbb R', size = p['intro_size']
        )
        opening.move_to(p['intro_position'])

        if self.stage is not None and 'real_metric' in self.stage:
            prior = self.stage['real_metric']
            beat(Transform(prior, opening), key = 'intro_morph')
            stable(opening)
        else:
            beat(Write(opening), key = 'intro_write')

        hold('intro_hold')

        for domain, codomain in [(r'\mathbb R^2', r'\mathbb R'), (r'\mathbb R^m', r'\mathbb R^n')]:
            nxt = _axiom_tex('f:', domain, p['intro_arrow_tex'], codomain, size = p['intro_size'])
            nxt.move_to(p['intro_position'])
            beat(Transform(opening, nxt), key = 'intro_morph')
            stable(nxt)
            opening = nxt
            hold('intro_hold')

        icons = _axiom_icons()
        # 数学字母与图标轮廓的拓扑不同：保留f与箭头，两端平滑交叠
        beat(
            opening[0].animate.move_to(icons[0].get_center()),
            opening[2].animate.move_to(icons[2].get_center()),
            FadeTransform(opening[1], icons[1], stretch = False),
            FadeTransform(opening[3], icons[3], stretch = False),
            key = 'intro_morph',
        )
        stable(icons)
        hold('icon_hold')
        axis = _axiom_axis()
        beat(FadeOut(icons), FadeIn(axis[0]), Create(axis[1]), FadeIn(axis[2]), key = 'axis_reveal')
        stable(axis)
        xt, yt = VectorizedPoint(point(p['x_start'])), VectorizedPoint(point(p['y_start']))
        px = _dot(xt.get_center(), PALETTE['cyan'], True)
        py = _dot(yt.get_center(), PALETTE['rose'], True)
        px.add_updater(lambda m: m.move_to(xt.get_center()))
        py.add_updater(lambda m: m.move_to(yt.get_center()))
        lx, ly = live_label('x', xt), live_label('y', yt)
        prefix = _axiom_tex('d:')
        pair = _axiom_tex('(', 'x', ',', 'y', ')')
        mapsto = _axiom_mapsto()
        result = _axiom_tex('d(x,y)')
        nonnegative = _axiom_tex(r'\geq0')
        mapping = (
            VGroup(prefix, pair, mapsto, result, nonnegative)
            .arrange(RIGHT, buff = p['formula_buff'])
            .move_to(p['property_position'])
        )
        beat(FadeIn(px), FadeIn(py), FadeIn(lx), FadeIn(ly), Write(prefix), key = 'points_reveal')
        lx.clear_updaters()
        ly.clear_updaters()
        punctuation = VGroup(pair[0], pair[2], pair[4])
        beat(
            Transform(lx, pair[1]), Transform(ly, pair[3]), FadeIn(punctuation), key = 'letters_move'
        )
        s.remove(lx, ly, punctuation)
        s.add(pair)
        lx, ly = live_label('x', xt), live_label('y', yt)
        link = always_redraw(
            lambda: _distance_line(xt.get_center(), yt.get_center(), PALETTE['epsilon'])
            .set_stroke(width = p['segment_width'])
            .set_z_index(5)
        )
        beat(Create(link), FadeIn(lx), FadeIn(ly), key = 'segment_reveal')
        result_position = result.get_center().copy()
        metric = distance_from_segment(link, 'd(x,y)')
        beat(metric.animate.move_to(result_position), Create(mapsto), key = 'formula_move')
        s.remove(metric)
        s.add(result)
        beat(Write(nonnegative), key = 'operator_write')
        stable(axis, link, px, py, lx, ly, mapping)
        hold()

        # 留下原距离值。两个点重合后再补上零与等价关系
        other = VGroup(prefix, pair, mapsto, nonnegative)
        beat(FadeOut(other), result.animate.move_to(p['property_position']), key = 'clear_time')
        stable(axis, link, px, py, lx, ly, result)
        ring = (
            Circle(
                radius = p['coincidence_radius'],
                color = PALETTE['cyan'],
                stroke_width = p['coincidence_width'],
                fill_opacity = 0,
            )
            .move_to(xt.get_center())
            .set_z_index(8)
        )
        identity = _axiom_row('d(x,y)', '=0', r'\Longleftrightarrow', 'x=y')
        beat(yt.animate.move_to(xt.get_center()), FadeOut(ly), key = 'collapse_time')
        beat(
            Transform(result, identity[0]),
            Write(VGroup(*identity.submobjects[1:])),
            FadeIn(ring),
            key = 'operator_write',
        )
        stable(axis, link, px, py, lx, ring, identity)
        hold()
        ly = live_label('y', yt)
        beat(
            FadeOut(identity),
            FadeOut(ring),
            yt.animate.move_to(point(p['y_start'])),
            FadeIn(ly),
            key = 'separate_time',
        )
        stable(axis, link, px, py, lx, ly)
        symmetric = _axiom_row('d(x,y)', '=', 'd(y,x)')
        forward = distance_from_segment(link, 'd(x,y)')
        beat(forward.animate.move_to(symmetric[0].get_center()), key = 'formula_move')
        a, b = xt.get_center().copy(), yt.get_center().copy()
        beat(
            MoveAlongPath(xt, ArcBetweenPoints(a, b, angle = p['swap_angle'])),
            MoveAlongPath(yt, ArcBetweenPoints(b, a, angle = p['swap_angle'])),
            key = 'swap_time',
        )
        reverse = distance_from_segment(link, 'd(y,x)')
        beat(
            reverse.animate.move_to(symmetric[2].get_center()),
            Write(symmetric[1]),
            key = 'formula_move',
        )
        stable(axis, link, px, py, lx, ly, symmetric)
        hold()

        # 三角不等式仍在数轴上。抬高的平行线段只是各个距离的量尺
        beat(FadeOut(symmetric), key = 'clear_time')
        stable(axis, link, px, py, lx, ly)
        zt = VectorizedPoint(point(p['z_outside']))
        pz = _dot(zt.get_center(), PALETTE['green'], True)
        pz.add_updater(lambda m: m.move_to(zt.get_center()))
        lz = live_label('z', zt)
        beat(FadeIn(pz), FadeIn(lz), key = 'triangle_reveal')
        triangle = _axiom_row('d(x,y)', '<', 'd(x,z)', '+', 'd(z,y)')
        direct = distance_from_segment(link, 'd(x,y)')
        beat(direct.animate.move_to(triangle[0].get_center()), key = 'formula_move')

        def route(a, b, y, color):
            u, v = a.get_center().copy(), b.get_center().copy()
            u[1] = v[1] = y

            return _distance_line(u, v, color).set_stroke(width = p['segment_width']).set_z_index(5)

        lower = always_redraw(lambda: route(xt, zt, p['route_y'][0], PALETTE['cyan']))
        upper = always_redraw(lambda: route(zt, yt, p['route_y'][1], PALETTE['rose']))

        def guide(track, y):
            a = track.get_center().copy()
            b = a.copy()
            b[1] = y

            return (
                DashedLine(
                    a,
                    b,
                    color = PALETTE['axis'],
                    stroke_width = p['guide_width'],
                    dash_length = p['guide_dash'],
                )
                .set_opacity(p['guide_opacity'])
                .set_z_index(2)
            )

        gx = always_redraw(lambda: guide(xt, p['route_y'][0]))
        gy = always_redraw(lambda: guide(yt, p['route_y'][1]))
        gz = always_redraw(lambda: guide(zt, p['route_y'][1]))
        beat(Create(lower), FadeIn(gx), FadeIn(gz), key = 'triangle_reveal')
        first_leg = distance_from_segment(lower, 'd(x,z)')
        beat(first_leg.animate.move_to(triangle[2].get_center()), key = 'formula_move')
        beat(Create(upper), FadeIn(gy), key = 'triangle_reveal')
        second_leg = distance_from_segment(upper, 'd(z,y)')
        beat(
            second_leg.animate.move_to(triangle[4].get_center()),
            Write(triangle[1]),
            Write(triangle[3]),
            key = 'formula_move',
        )
        stable(axis, link, px, py, lx, ly, pz, lz, lower, upper, gx, gy, gz, triangle)
        hold()
        equality = _axiom_tex('=').move_to(triangle[1].get_center())
        beat(zt.animate.move_to(point(p['z_between'])), key = 'triangle_move')
        beat(Transform(triangle[1], equality), key = 'operator_write')
        hold('equality_hold')
        leq = _axiom_tex(r'\leq').move_to(triangle[1].get_center())
        beat(
            zt.animate.move_to(point(p['z_outside'])),
            Transform(triangle[1], leq),
            key = 'triangle_move',
        )
        hold()

        # 先划掉小于等于号，再在上方给出红色的反向假设
        comparison = triangle[1]
        margin = p['triangle_slash_margin']
        slash = Line(
            comparison.get_corner(DL) + margin * (DOWN + LEFT),
            comparison.get_corner(UR) + margin * (UP + RIGHT),
            color = p['triangle_negation_color'],
            stroke_width = p['triangle_slash_width'],
        ).set_z_index(31)
        reversed_sign = (
            _axiom_tex('>')
            .set_color(p['triangle_negation_color'])
            .next_to(comparison, UP, buff = p['triangle_reverse_sign_gap'])
            .set_z_index(31)
        )
        beat(Create(slash), key = 'triangle_slash_time')
        beat(Write(reversed_sign), key = 'triangle_reverse_sign_time')
        hold('triangle_negation_hold')

        # 矛盾链放在点标签之下、字幕安全区之上；不是度量的恒等式
        proof_terms = p['contradiction_tex'].split('>')
        proof_parts = []

        for index, term in enumerate(proof_terms):

            if index:
                proof_parts.append('>')

            proof_parts.append(term)

        proof = _axiom_tex(*proof_parts, size = p['contradiction_size'])
        proof.set_color_by_tex('>', p['contradiction_color'], substring = False)
        proof[0].set_color(p['contradiction_color'])
        proof[-1].set_color(p['contradiction_color'])
        marker = _tex(
            p['contradiction_marker'], size = p['contradiction_marker_size'], color = PALETTE['error']
        )
        marker.next_to(proof, RIGHT, buff = p['contradiction_marker_gap'])
        contradiction = VGroup(proof, marker).move_to(p['contradiction_position'])
        beat(Write(proof), key = 'contradiction_write')
        beat(FadeIn(marker), key = 'operator_write')
        hold('contradiction_hold')

        # 场景整体压暗，再将三行公理收束为度量符号d
        for mob in (px, py, lx, ly, link, pz, lz, lower, upper, gx, gy, gz):
            mob.clear_updaters()
        backdrop = VGroup(
            axis,
            link,
            px,
            py,
            lx,
            ly,
            pz,
            lz,
            lower,
            upper,
            gx,
            gy,
            gz,
            triangle,
            slash,
            reversed_sign,
            contradiction,
        )
        stable(backdrop)
        summary = (
            VGroup(
                _axiom_tex(
                    r'd(x,y)\geq0,\; d(x,y)=0\Longleftrightarrow x=y', size = p['summary_size']
                ),
                _axiom_tex('d(x,y)=d(y,x)', size = p['summary_size']),
                _axiom_tex(r'd(x,y)\leq d(x,z)+d(z,y)', size = p['summary_size']),
            )
            .arrange(DOWN, buff = p['summary_gap'])
            .move_to(p['summary_position'])
            .set_z_index(30)
        )
        beat(backdrop.animate.set_opacity(p['summary_dim']), key = 'summary_dim_time')
        beat(Write(summary), key = 'summary_write')
        hold('summary_hold')
        big_d = _tex(
            'd', p['summary_d_position'], p['summary_d_size'], PALETTE['epsilon']
        ).set_z_index(30)
        summary_forms, d_forms = _align_morph_glyphs(_morph_glyphs(summary), _morph_glyphs(big_d))
        s.remove(summary)
        s.add(summary_forms)
        beat(Transform(summary_forms, d_forms), FadeOut(backdrop), key = 'summary_collapse_time')
        stable(big_d)
        hold('summary_d_hold')

        pair = MathTex(
            '(', 'X', ',', 'd', ')', font_size = p['metric_pair_size'], color = PALETTE['ink']
        )
        pair[1].set_color(PALETTE['cyan'])
        pair[3].set_color(PALETTE['epsilon'])
        pair.move_to(p['metric_pair_position']).set_z_index(30)

        for part in pair.get_family():
            if isinstance(part, VMobject):
                part.consider_points_equals = _precise_equal
                part.consider_points_equals_2d = _precise_equal

        punctuation = VGroup(pair[0], pair[1], pair[2], pair[4])
        beat(
            big_d.animate.scale(pair[3].height / big_d.height).move_to(pair[3].get_center()),
            Write(punctuation),
            key = 'metric_pair_build',
        )
        stable(pair)
        hold('metric_pair_hold')
        beat(pair.animate.move_to(p['metric_pair_upper']), key = 'metric_pair_lift')
        real_continuity = _continuity_intro_tex(False)
        metric_continuity = _continuity_intro_tex(True)
        beat(Write(real_continuity), key = 'continuity_intro_write')
        hold('continuity_intro_hold')

        # 两个绝对值直接变为度量表达式；比较号、delta、蕴含箭头与epsilon保持字形
        left_forms = _morph_glyphs(real_continuity[0])
        right_forms = _morph_glyphs(real_continuity[3])
        metric_left_forms = _morph_glyphs(VGroup(metric_continuity[0], metric_continuity[1]))
        metric_right_forms = _morph_glyphs(VGroup(metric_continuity[4], metric_continuity[5]))
        left_less, right_less = left_forms[-1], right_forms[-1]
        metric_left_less, metric_right_less = metric_left_forms[-1], metric_right_forms[-1]
        left_forms.remove(left_less)
        right_forms.remove(right_less)
        metric_left_forms.remove(metric_left_less)
        metric_right_forms.remove(metric_right_less)
        left_forms, metric_left_forms = _align_morph_glyphs(left_forms, metric_left_forms)
        right_forms, metric_right_forms = _align_morph_glyphs(right_forms, metric_right_forms)
        s.remove(real_continuity)
        s.add(
            left_forms,
            right_forms,
            left_less,
            right_less,
            real_continuity[1],
            real_continuity[2],
            real_continuity[4],
        )
        beat(
            Transform(left_forms, metric_left_forms),
            Transform(right_forms, metric_right_forms),
            left_less.animate.move_to(metric_left_less.get_center()),
            right_less.animate.move_to(metric_right_less.get_center()),
            real_continuity[1].animate.move_to(metric_continuity[2].get_center()),
            real_continuity[2].animate.move_to(metric_continuity[3].get_center()),
            real_continuity[4].animate.move_to(metric_continuity[6].get_center()),
            key = 'continuity_intro_morph',
        )
        stable(pair, metric_continuity)
        hold('continuity_intro_final_hold')

        # 第二镜停在(X,d)与连续性公式，随后接入UniformDistance
        self.stage = dict(axioms_final = True, pair = pair, formula = metric_continuity)

    def uniform_distance(self):
        s, p = self.s, UNIFORM

        def beat(*animations, key):
            self.beat(*animations, duration = p[key])

        def hold(key):
            s.wait(p[key] * TIME_SCALE)

        def stable(*objects):
            s.clear()
            s.add(*objects)

        def change_formula(source, target):
            a, b = _align_morph_glyphs(_morph_glyphs(source), _morph_glyphs(target))
            s.remove(source)
            s.add(a)
            beat(Transform(a, b), key = 'formula_morph')
            s.remove(a)
            s.add(target)

        plane, art = _uniform_plane()
        f = _uniform_curve(plane, lambda t: t, p['f_color'])
        g = _uniform_curve(plane, lambda t: t * t, p['g_color'])
        labels = VGroup(
            _uniform_tex('f(x)=x', p['f_label'], color = p['f_color']),
            _uniform_tex('g(x)=x^2', p['g_label'], color = p['g_color']),
        )
        interval = _tex(r'I=[0,1]', p['domain_label'], p['domain_label_size'])
        prior = None

        if self.stage is not None and self.stage.get('axioms_final'):
            prior = VGroup(self.stage['pair'], self.stage['formula'])

        animations = [Create(plane), FadeIn(art[1]), FadeIn(art[2])]

        if prior is not None:
            animations.append(FadeOut(prior))

        beat(*animations, key = 'plane_reveal')
        beat(Create(f), Create(g), Write(labels), Write(interval), key = 'curves_reveal')
        stable(art, f, g, labels, interval)
        hold('opening_hold')

        # 本例两条曲线的左右端点重合，各位置仅播放一次黄色闪光
        ends = []

        for curve in (f, g):
            for point in (curve[0].get_start(), curve[-1].get_end()):
                if not any(
                    np.allclose(point, known, atol = STYLE['path_tolerance']) for known in ends
                ):
                    ends.append(point)
        beat(
            *[
                Flash(
                    point,
                    color = p['flash_color'],
                    flash_radius = p['endpoint_flash_radius'],
                    line_length = p['endpoint_flash_length'],
                    num_lines = p['endpoint_flash_lines'],
                    line_stroke_width = p['endpoint_flash_width'],
                    time_width = p['endpoint_flash_time_width'],
                )
                for point in ends
            ],
            key = 'endpoint_flash_time',
        )
        x = ValueTracker(p['scan_start'])

        def segment(current_plane, upper, lower):
            return (
                _distance_line(
                    current_plane.c2p(x.get_value(), lower(x.get_value())),
                    current_plane.c2p(x.get_value(), upper(x.get_value())),
                    p['distance_color'],
                )
                .set_stroke(width = p['segment_width'])
                .set_z_index(7)
            )

        def endpoints(current_plane, upper, lower, top_color, bottom_color):
            t = x.get_value()

            return VGroup(
                Dot(
                    current_plane.c2p(t, upper(t)),
                    radius = p['point_radius'],
                    color = top_color(t) if callable(top_color) else top_color,
                ),
                Dot(current_plane.c2p(t, lower(t)), radius = p['point_radius'], color = bottom_color),
            ).set_z_index(8)

        gap = always_redraw(lambda: segment(plane, lambda t: t, lambda t: t * t))
        points = always_redraw(
            lambda: endpoints(plane, lambda t: t, lambda t: t * t, p['f_color'], p['g_color'])
        )
        reading = always_redraw(
            lambda: _uniform_readout(plane, x.get_value(), lambda t: t, lambda t: t * t, above = True)
        )
        beat(Create(gap), FadeIn(points), FadeIn(reading), key = 'segment_reveal')

        for value in p['scan_stops']:
            beat(x.animate.set_value(value), key = 'scan_time')
            hold('scan_hold')

        # 先在原比例中把两条曲线直接变换为差函数，再平滑放大纵轴
        gap.clear_updaters()
        points.clear_updaters()
        reading.clear_updaters()
        difference = _uniform_curve(plane, lambda t: t - t * t, p['difference_gradient'])
        difference_gap = segment(plane, lambda t: t - t * t, lambda t: 0)
        difference_points = endpoints(
            plane, lambda t: t - t * t, lambda t: 0, _uniform_difference_color, PALETTE['axis']
        )
        difference_reading = _uniform_readout(
            plane, x.get_value(), lambda t: t - t * t, lambda t: 0
        )
        expression = _uniform_tex('x-x^2', p['header'], color = p['difference_color'])
        beat(
            Transform(f, difference.copy()),
            Transform(g, difference.copy()),
            Transform(gap, difference_gap),
            Transform(points, difference_points),
            Transform(reading, difference_reading),
            FadeOut(labels),
            Write(expression),
            key = 'difference_morph',
        )
        stable(art, difference, gap, points, reading, interval, expression)

        def zoom_picture(gain, blend):
            current_plane, current_art = _uniform_plane(zoom = gain, tick_blend = blend)
            current_curve = _uniform_curve(
                current_plane, lambda t: t - t * t, p['difference_gradient']
            )

            return VGroup(
                current_art,
                current_curve,
                segment(current_plane, lambda t: t - t * t, lambda t: 0),
                endpoints(
                    current_plane,
                    lambda t: t - t * t,
                    lambda t: 0,
                    _uniform_difference_color,
                    PALETTE['axis'],
                ),
                _uniform_readout(current_plane, x.get_value(), lambda t: t - t * t, lambda t: 0),
            )

        live = zoom_picture(1.0, 0.0)
        s.remove(art, difference, gap, points, reading)
        s.add(live)

        def stretch_vertical(mob, alpha):
            t = smootherstep(alpha)
            gain = np.exp(np.log(p['vertical_zoom']) * t)
            phase = smooth(
                float(
                    np.clip(
                        (t - p['zoom_tick_fade_start'])
                        / (p['zoom_tick_fade_end'] - p['zoom_tick_fade_start']),
                        0,
                        1,
                    )
                )
            )
            mob.become(zoom_picture(gain, phase))

        self.beat(
            UpdateFromAlphaFunc(live, stretch_vertical),
            duration = p['vertical_zoom_time'],
            rate_func = linear,
        )
        plane, art = _uniform_plane(True)
        difference = _uniform_curve(plane, lambda t: t - t * t, p['difference_gradient'])
        gap = always_redraw(lambda: segment(plane, lambda t: t - t * t, lambda t: 0))
        points = always_redraw(
            lambda: endpoints(
                plane, lambda t: t - t * t, lambda t: 0, _uniform_difference_color, PALETTE['axis']
            )
        )
        reading = always_redraw(
            lambda: _uniform_readout(plane, x.get_value(), lambda t: t - t * t, lambda t: 0)
        )
        stable(art, difference, gap, points, reading, interval, expression)
        hold('difference_hold')
        beat(x.animate.set_value(p['maximum_x']), key = 'maximum_move')
        maximum = _uniform_tex(r'\max_{x\in[0,1]}(x-x^2)=' + p['maximum_tex'], p['header'])
        a, b = _align_morph_glyphs(_morph_glyphs(expression), _morph_glyphs(maximum))
        s.remove(expression)
        s.add(a)
        beat(Transform(a, b), FadeOut(interval), key = 'formula_morph')
        s.remove(a)
        s.add(maximum)
        hold('maximum_hold')
        supremum = _uniform_tex(r'\sup_{x\in[0,1]}(x-x^2)=' + p['maximum_tex'], p['header'])
        change_formula(maximum, supremum)
        hold('supremum_hold')
        metric = _uniform_tex(r'd_\infty(f,g)=\sup_{x\in[0,1]}|f(x)-g(x)|', p['header'])
        change_formula(supremum, metric)
        flash = (
            _morph_glyphs(metric)
            .set_fill(opacity = 0)
            .set_stroke(p['flash_color'], p['flash_width'])
            .set_z_index(25)
        )
        flashes = [ShowPassingFlash(flash, time_width = p['flash_time_width'])]

        if p['flash_curve']:
            flashes.append(
                ShowPassingFlash(_uniform_flash_curve(plane), time_width = p['flash_time_width'])
            )

        beat(*flashes, key = 'flash_time')
        membership = _uniform_tex(
            r'f,g\in B(I,\mathbb{R})', p['membership_position'], size = p['membership_size']
        )
        beat(Write(membership), key = 'membership_reveal')
        gap.clear_updaters()
        points.clear_updaters()
        reading.clear_updaters()
        stable(art, difference, gap, points, reading, metric, membership)
        hold('final_hold')
        self.stage = dict(
            uniform_final = True,
            art = art,
            axes = plane,
            difference = difference,
            title = metric,
            auxiliary = VGroup(gap, points, reading, membership),
        )

    def function_space(self):
        s, p = self.s, FUNCTIONS

        def beat(*animations, key, **kwargs):
            self.beat(*animations, duration = p[key], **kwargs)

        def hold(key):
            s.wait(p[key] * TIME_SCALE)

        def stable(*objects):
            s.clear()
            s.add(*objects)

        plane, art = _function_plane()

        if self.stage is not None and self.stage.get('uniform_final'):
            old = self.stage
            beat(
                FadeTransform(old['art'], VGroup(plane, art[2], art[3]), stretch = False),
                FadeOut(VGroup(old['difference'], old['auxiliary'], old['title'])),
                key = 'plane_reveal',
            )
        else:
            beat(Create(plane), FadeIn(art[2]), Write(art[3]), key = 'plane_reveal')

        stable(plane, art[2], art[3])
        beat(Create(art[1]), key = 'boundary_reveal')
        stable(art)
        models = _function_models()
        f_index, g_index = p['selected_curve_indices']

        # 开场的每条曲线都使用同一套沿横坐标变化的青绿黄渐变
        curves = VGroup(*[_function_curve(plane, fn, p['curve_colors']) for fn in models])

        # 保留开场曲线的完整几何路径，结尾直接复用，不生成新函数
        f = curves[f_index].copy().set_stroke(width = p['final_curve_width'])
        g = curves[g_index].copy().set_stroke(width = p['final_curve_width'])
        f_fn, g_fn = models[f_index], models[g_index]
        beat(
            LaggedStart(*[Create(curve) for curve in curves], lag_ratio = p['curves_lag']),
            key = 'curves_reveal',
        )
        stable(art, curves)
        hold('curves_hold')

        title = _tex(r'C([0,1])', p['title_position'], p['title_size'])
        chunks = _function_title_chunks(title)
        s.remove(curves)
        s.add(*curves)
        journeys = []
        rng = np.random.default_rng(p['flight_seed'])
        curve_order = rng.permutation(len(curves))
        chunk_order = rng.permutation(len(chunks))

        for i, (curve_index, chunk_index) in enumerate(zip(curve_order, chunk_order)):
            curve, chunk = curves[curve_index], chunks[chunk_index]
            start = curve.get_center()
            target = chunk.get_center()
            dot = Dot(start, radius = p['dot_radius'], color = p['dot_color']).set_z_index(15)
            sway = p['flight_sway'] * np.sin(i * p['flight_angle'])
            path = CubicBezier(
                start,
                start + UP * p['flight_lift'] + RIGHT * sway,
                target + DOWN * (p['flight_lift'] / 2) + RIGHT * sway,
                target,
            )
            journeys.append(
                Succession(
                    Transform(
                        curve, dot, run_time = p['collapse_time'] * TIME_SCALE, rate_func = smootherstep
                    ),
                    _FunctionPointFlight(
                        curve, path, run_time = p['flight_time'] * TIME_SCALE, rate_func = smootherstep
                    ),
                    Transform(
                        curve,
                        chunk,
                        run_time = p['glyph_form_time'] * TIME_SCALE,
                        rate_func = smootherstep,
                    ),
                )
            )

        s.play(LaggedStart(*journeys, lag_ratio = p['flight_lag'], rate_func = smootherstep))
        stable(art, *chunks)
        s.play(
            DrawBorderThenFill(title, stroke_width = p['glyph_stroke_width']),
            run_time = p['title_fill'] * TIME_SCALE,
        )
        stable(art, title)
        hold('title_hold')

        distance = _tex(r'd_\infty', p['d_start'], p['title_size'], p['d_color'])
        beat(Write(distance), key = 'd_reveal')
        hold('d_hold')
        pair = _function_pair()
        punctuation = VGroup(pair[0].copy(), pair[2].copy(), pair[4].copy())
        beat(
            Transform(title, pair[1].copy()),
            Transform(distance, pair[3].copy()),
            FadeIn(punctuation),
            key = 'pair_morph',
        )
        stable(art, pair)
        outline = SurroundingRectangle(
            pair,
            buff = p['frame_buffer'],
            corner_radius = p['frame_corner_radius'],
            color = p['frame_color'],
            stroke_width = p['frame_width'],
        ).set_z_index(25)
        beat(ShowPassingFlash(outline, time_width = p['frame_time_width']), key = 'frame_flash')
        hold('pair_hold')

        # 结尾才把保留的两条原曲线强调为蓝色和红色
        _function_recolor(f, f_fn, p['final_f_color'])
        _function_recolor(g, g_fn, p['final_g_color'])
        samples = np.linspace(0, 1, p['curve_segments'] * p['samples_per_segment'])
        band_points = [plane.c2p(t, f_fn(t) + p['epsilon']) for t in samples]
        band_points += [plane.c2p(t, f_fn(t) - p['epsilon']) for t in samples[::-1]]
        band = Polygon(
            *band_points, stroke_width = 0, fill_color = p['band_color'], fill_opacity = p['band_opacity']
        ).set_z_index(1)
        edges = VGroup()

        for sign in (-1, 1):
            path = VMobject().set_points_smoothly(
                [plane.c2p(t, f_fn(t) + sign * p['epsilon']) for t in samples]
            )
            edge = DashedVMobject(
                path,
                dashed_ratio = p['band_dash_ratio'],
                num_dashes = max(1, int(path.get_arc_length() / p['band_dash_length'])),
            )
            edges.add(
                edge.set_stroke(
                    p['band_color'], p['band_edge_width'], opacity = p['band_edge_opacity']
                ).set_z_index(2)
            )

        epsilon_x = p['epsilon_x']
        bottom = plane.c2p(epsilon_x, f_fn(1))
        top = plane.c2p(epsilon_x, f_fn(1) + p['epsilon'])
        epsilon_mark = VGroup(
            Line(bottom, top, color = p['band_color'], stroke_width = p['probe_width']),
            Line(
                bottom - p['tick_size'] * RIGHT,
                bottom + p['tick_size'] * RIGHT,
                color = p['band_color'],
            ),
            Line(top - p['tick_size'] * RIGHT, top + p['tick_size'] * RIGHT, color = p['band_color']),
        )
        epsilon_label = _tex(
            r'\varepsilon', size = p['epsilon_label_size'], color = p['band_color']
        ).move_to((bottom + top) / 2 + _v(p['epsilon_label_offset']))
        formula = _uniform_tex(
            r'd_\infty(f,g)<\varepsilon', p['closing_formula_position'], p['closing_formula_size']
        )
        # 此式最后一个字形就是epsilon；仅将它与误差带统一为绿色。
        formula[-1][-1].set_color(p['band_color'])
        beat(
            FadeIn(band),
            FadeIn(edges),
            Create(f),
            Create(g),
            Create(epsilon_mark),
            Write(epsilon_label),
            Write(formula),
            key = 'final_reveal',
        )
        x = ValueTracker(p['probe_start'])
        gap = always_redraw(
            lambda: Line(
                plane.c2p(x.get_value(), f_fn(x.get_value())),
                plane.c2p(x.get_value(), g_fn(x.get_value())),
                color = p['d_color'],
                stroke_width = p['probe_width'],
            ).set_z_index(9)
        )
        points = always_redraw(
            lambda: VGroup(
                Dot(
                    plane.c2p(x.get_value(), f_fn(x.get_value())),
                    radius = p['probe_radius'],
                    color = p['final_f_color'],
                ),
                Dot(
                    plane.c2p(x.get_value(), g_fn(x.get_value())),
                    radius = p['probe_radius'],
                    color = p['final_g_color'],
                ),
            ).set_z_index(10)
        )
        beat(Create(gap), FadeIn(points), key = 'probe_reveal')

        for value in p['probe_stops']:
            beat(x.animate.set_value(value), key = 'probe_move')
            hold('probe_hold')

        gap.clear_updaters()
        points.clear_updaters()
        stable(art, pair, band, edges, f, g, epsilon_mark, epsilon_label, formula, gap, points)
        hold('final_hold')
        self.stage = None

class RealLineMetric(Scene):
    def construct(self):
        _MetricStory(self).real_line()

class MetricAxioms(Scene):
    def construct(self):
        _MetricStory(self).metric_axioms()

class UniformDistance(Scene):
    def construct(self):
        _MetricStory(self).uniform_distance()

class FunctionSpace(Scene):
    def construct(self):
        _MetricStory(self).function_space()

class MetricFilm(Scene):
    def construct(self):
        story = _MetricStory(self)
        story.real_line()
        story.metric_axioms()
        story.uniform_distance()
        story.function_space()
