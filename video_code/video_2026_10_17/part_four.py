from manim import *
import math
import numpy as np

# 所有可调参数
BG_COLOR = "#000012"
FRAME_WIDTH, FRAME_HEIGHT = 128 / 9, 8.0
FRAME_RATE = 60                    # 默认60帧；设为None则沿用命令行帧率
TIME_SCALE = 1.0                   # 所有动画和停顿统一乘此参数
SUBTITLE = dict(top = -2.45, margin = 0.12)  # 下方保留给后期字幕；不在动画里绘制字幕
PALETTE = dict(
    axis = "#FFFFFF", ink = "#FFFFFF", cyan = "#56CEE8", green = "#9EE3A2",
    yellow = "#E8EE63", rose = "#EF819B", epsilon = "#FFE17D",
    safe = "#68E6C0", muted = "#687C98", error = "#FF526E",
)
STYLE = dict(
    axis_width = 2.0, curve_width = 4.2, guide_width = 1.45, guide_opacity = 0.42,
    dash_length = 0.10, dash_ratio = 0.55, tick_size = 0.055, tick_label_gap = 0.22,
    dot_radius = 0.059, focus_radius = 0.080, open_radius = 0.072, open_width = 2.8,
    halo_radius = 0.18, halo_opacity = 0.10, formula_size = 37, small_size = 28,
    label_size = 30, formula_width = 12.8, header = (0, 3.12, 0), footer = (0, -2.92, 0), header_min_y = 2.0,
    curve_segments = 40, samples_per_segment = 5, curve_samples = 161, band_samples = 81,
    flash_width = 6.0, flash_time_width = 0.35, arrow_tip = 0.14,
    outline_width = 1.8, faint_opacity = 0.18, algorithm_tolerance = 1e-9,
    math_label_outline_width = 4.0, math_label_z = 35,
)
GRID = dict(
    enabled = True, color = "#607089", opacity = 0.40, line_width = 1.40,
    cell_size = 0.50,  # 画面单位：横、纵格边都等于此值，独立于坐标缩放比例
)
# 与part_three.py中函数区间的白色边界虚线保持一致
BOUNDARY = dict(color = WHITE, opacity = 0.70, line_width = 1.7,
                dash_length = 0.13, dash_ratio = 0.55, z_index = 7)
# 开场函数只是演示曲线；中点读数由同一个函数计算，绝不手填假数值
FUNCTION = dict(
    domain = (0.0, 1.0), midpoint = 0.5, base = 0.33, slope = 0.42,
    wave_amplitude = 0.075, wave_frequency = 2.0,
    dip_amplitude = 0.10, irrational_offset = 0.018,
    gap_floor = 0.65, gap_wave = 0.35, gap_frequency = 2.0,
    gradient = (PALETTE['cyan'], PALETTE['green'], PALETTE['yellow']),
)
MACHINE = dict(
    width = 1.72, height = 1.72, corner = 0.10, frame_width = 2.3,
    mouth_width = 0.66, mouth_height = 1.35, neck_height = 0.53,
    mouth_gap = 0.10, fill_opacity = 0.94, glyph_size = 54,
    proof_scale = 0.69,
    shake_x = 0.11, shake_y = 0.035, shake_cycles = 3.0,
)
EVALUATION = dict(
    origin = (-6.18, -1.12, 0), x_range = (0, 1.10, 0.5), y_range = (0, 1.12, 0.5),
    x_length = 3.80, y_length = 3.10, ticks = (0, 0.5, 1), tick_tex = ('0', '0.5', '1.0'),
    y_ticks = (0.5, 1), tick_decimal_places = 1, y_tick_label_gap = 0.32,
    origin_label_offset = (-0.13, -0.20, 0),
    smooth_origin = True, origin_joint_radius = 0.012,
    # NumberPlane 默认网格：BLUE_D、stroke_width=2；保留正方形和0.4透明度
    grid_color = BLUE_D, grid_line_width = 2.0,
    boundary_height = 1.02,
    f_label = (-4.50, 1.37, 0), machine_center = (-0.03, 0.26, 0),
    output_position = (4.47, 0.38, 0), output_size = 38, output_width = 4.7,
    mapping_position = (0, 2.80, 0), mapping_size = 41,
    travel_mouth_scale = 0.33, travel_lift = 0.37,
    decimals = 3, sample_decimal_places = 1, ingest_shift = 0.75, ingest_scale = 0.12,
    machine_fill_opacity = 1.0, machine_body_z = 13, machine_glyph_z = 14,
    exit_pulse_end = (2.54, 0.26, 0),
)
PROOF = dict(
    origin = (-6.12, -0.85, 0), x_range = (0, 1.10, 0.5), y_range = (0, 1.12, 0.5),
    x_length = 6.00, y_length = 2.80, ticks = (0, 0.5, 1), tick_tex = ('0', '0.5', '1.0'),
    y_ticks = (0.5, 1), tick_decimal_places = 1, y_tick_label_gap = 0.32,
    smooth_origin = True, origin_joint_radius = EVALUATION['origin_joint_radius'],
    origin_label_offset = EVALUATION['origin_label_offset'],
    grid_color = EVALUATION['grid_color'], grid_line_width = EVALUATION['grid_line_width'],
    boundary_height = 1.02,
    machine_center = (1.10, 0.44, 0), f1_label = (-5.72, -0.10, 0), f2_label = (-4.86, 1.16, 0),
    gap_start = 0.12, epsilon_start = 0.19,
    refinements = ((0.085, 0.140), (0.058, 0.090), (0.038, 0.055)),
    band_opacity = 0.080, band_edge_opacity = 0.63,
    scan_start = 0.08, scan_lead_stop = 0.16, scan_stops = (0.25, 0.76, 0.5), scan_width = 3.1,
    band_bracket_x = 0.91, band_label_offset = (0.0, 0.20, 0), band_cap_half_width = 0.070,
    output_axis_x = 3.03, output_axis_bottom = -0.80, output_axis_scale = 3.00,
    output_ticks = (0, 0.5, 1), output_tick_tex = ('0.0', '0.5', '1.0'),
    output_label_offset = (0.38, 0, 0), output_label_gap = 0.32,
    output_band_half_width = 0.12, output_band_opacity = 0.10, output_cap_half_width = 0.18,
    output_epsilon_bracket_x = 0.14, output_epsilon_label_offset = (0.20, -0.04, 0),  # 相对黄色竖线中点
    output_dot_radius = 0.065, probe_label_offset = (0.32, -0.21, 0),
    wire_opacity = 0.31, wire_width = 1.45, wire_bend = 0.42,
    readout_size = 31, readout_buff = 0.055, readout_width = 3.65,
    inequality_position = (0, -1.78, 0), inequality_size = 36,
    delta_position = (1.10, 1.72, 0), delta_size = 35,
    pulse_bend = 0.55,
)
# 自变量是整个函数：f2在一致距离下逐步接近f1。横坐标和相机保持不动
# 只调整纵向读数比例，保留完整[0,1]上的函数；最终画面不再缩小
APPROACH = dict(
    vertical_factors = (1.18, 1.55, 2.00),
    tick_initial_precision = 1.0, tick_max_precision = 4,
    tick_min_spacing_x = 1.10, tick_min_spacing_y = 0.50, tick_min_spacing_output = 0.60,
    tick_fade_width_x = 0.50, tick_fade_width_y = 0.28,
    tick_digit_spacing = 1.18, tick_decimal_spacing = 0.45, tick_minus_spacing = 0.85,
    tick_decimal_drop = 0.070, tick_cache_size = 512, legend_gap = 0.22,
    bracket_inset = 0.30, output_label_inset = 0.28, mapped_label_time = 0.65,
)
# 在此增删条目即可调整机器依次处理的函数数量；f2与下一镜的比较模型一致
INPUTS = (
    dict(offset = 0.0, slope = 0.0, wave = 0.0, frequency = 2.0, gap = 0.0, gradient = FUNCTION['gradient']),
    dict(offset = 0.0, slope = 0.0, wave = 0.0, frequency = 2.0, gap = PROOF['gap_start'],
         gradient = (PALETTE['rose'], PALETTE['rose'], PALETTE['rose'])),
    dict(offset = 0.06, slope = -0.18, wave = 0.10, frequency = 3.0, gap = 0.0,
         gradient = (PALETTE['cyan'], PALETTE['green'], PALETTE['green'])),
)
DISCRETE = dict(
    definition_center = (0, 0, 0), definition_size = 46,
    header_position = (0, 3.12, 0), header_size = 40,
    definition_hold = 2.80, definition_move_time = 1.55,
    axis_y = 0.0, axis_half_length = FRAME_WIDTH/2+1.20, axis_unit = 1.50,
    ticks = (-4, -3, -2, -1, 0, 1, 2, 3, 4), tick_font = 25, tick_decimals = 0,
    axis_reveal_time = 1.15, anchor_x = -2.80, anchor_label_offset = (0, -0.70, 0),
    anchor_reveal_time = 0.65, anchor_hold = 0.50,
    circle_height = 1.30, circle_radius = 1.0,  # 圆心始终在数轴x0正上方；高度相对数轴
    circle_color = WHITE, circle_width = 1.9, circle_opacity = 0.60,
    center_label_offset = (-0.20, -0.32, 0), center_label_size = 30,
    copy_move_time = 2.30, copy_controls = (1/3, 2/3), anchor_z = 20,
    circle_reveal_time = 1.10, circle_hold = 0.35,
    point_count = 16, random_seed = 23, source_offset_bounds = (0.16, 0.95),
    # 随机落点保留最小角间距；种子相同即可复现，改种子即可换一组位置
    minimum_angular_gap = 0.20, angular_gap_randomness = 1.0,
    point_colors = (PALETTE['green'], PALETTE['rose'], PALETTE['yellow'], PALETTE['cyan']),
    point_radius = STYLE['focus_radius'], point_pick_scale = 0.65, point_birth_time = 0.18,
    # 所有点共用一个快→慢→快的时钟。以下两个间隔是时钟内的时间
    launch_interval = 0.65, flight_time = 2.80,
    stream_time = 15.00, stream_speed_contrast = 0.35,
    # 每点仅在首尾16%的航程时间柔和起落，中途不再反复刹车
    ease_fraction = 0.16, path_samples = 2049,
    flight_vertical_controls = (0.35, 0.65),  # 向上为主的柔和弧线，避免横向绕行
    radius_angle_degrees = 0, radius_color = PALETTE['epsilon'], radius_width = 2.50,
    radius_label_offset = (0, 0.22, 0), radius_label_size = 34, radius_reveal_time = 0.90,
    final_hold = 3.30,
)
STEP_POINT_COUNT = 65              # 其中1点为观察中心，其余64点位于圆周
STEP = dict(
    origin = (0, -1.05, 0), x_range = (-2.65, 2.65, 1), y_range = (-0.12, 1.38, 0.5),
    x_length = 11.6, y_length = 3.20, x_ticks = (-2, -1, 0, 1, 2),
    origin_label_offset = (-0.14, -0.24, 0),
    header_size = 37, metric_size = 36, graph_hold = 1.20,
    sample_x = tuple(np.linspace(-2.30, 2.30, STEP_POINT_COUNT)+0.015), point_radius = 0.040,
    sample_reveal_time = 0.80, sample_reveal_lag = 0.055, sample_hold = 0.35,
    mini_width = 4.7, mini_center = (-4.55, 1.45, 0),
    disk_center = (1.65, 0.0, 0), disk_radius = 2.0,
    disk_color = WHITE, disk_width = 2.1, disk_opacity = 0.65,
    disk_fill_color = PALETTE['cyan'], disk_fill_opacity = 0.035,
    # 借鉴庞加莱圆盘的圆盘自同构和正交圆弧，作为移动观察坐标的背景
    guide_samples = 65, guide_color = PALETTE['cyan'], guide_width = 1.3,
    guide_opacity = 0.28, guide_motion_opacity = 0.035,
    # 四瓣正交圆弧网：52条连线，包含4条中心半径，其余全部为圆弧
    # weave_seed_fractions 的两端为一象限内的槽位比例；自动作D4旋转与镜像
    weave_seed_fractions = ((1/4,5/4),(1/8,9/8)),
    geodesic_diameter_tolerance = 1e-3, ring_start_angle = 0,
    entry_flight_time = 2.75, entry_lag = 0.010, entry_start_lift = 0.85, entry_end_lift = 0.40,
    # 按原横轴点的身份编号观察，编号从0开始；点的颜色和H值全程不变
    focus_sequence = (STEP_POINT_COUNT//2, STEP_POINT_COUNT//5, 4*STEP_POINT_COUNT//5, STEP_POINT_COUNT//10, 2*STEP_POINT_COUNT//3),
    # 4次换中心，每次旋转半圈，前半段共转两圈；此时尚无delta小圆
    pre_move_time = 4.60, pre_rotation = PI, pre_focus_hold = 0.45,
    # 小圆出现后继续换6个不同中心；两行证明随下标一起变换
    ball_focus_sequence = (STEP_POINT_COUNT//4, 3*STEP_POINT_COUNT//4, STEP_POINT_COUNT//8,
                         7*STEP_POINT_COUNT//8, STEP_POINT_COUNT//3, 5*STEP_POINT_COUNT//9),
    after_flash_focus_sequence = (STEP_POINT_COUNT//7, 6*STEP_POINT_COUNT//7, 4*STEP_POINT_COUNT//9),
    # 小圆出现后的观察旋转先移再回，停稳时始终恢复同一对称方向
    view_move_time = 2.70, view_rotation = 0, view_sway = 25*DEGREES, view_pan_strength = 0.28,
    focus_hold = 0.65, exchange_bend = 0.18, select_time = 0.22,
    halo_radius = 0.11, halo_width = 1.75,
    observation_reveal_time = 0.65,
    focus_label_offset = (0, -0.34, 0), focus_label_size = 28,
    readout_position = (-4.55, -0.15, 0), readout_size = 36, readout_gap = 0.07,
    unit_width = 2.4, unit_label_offset = (0, 0.20, 0), unit_label_size = 34,
    ball_radius = 0.5, ball_width = 2.0, ball_opacity = 0.035,
    ball_label_angle = PI/3, ball_label_offset = (0.25, 0.14, 0), ball_label_size = 28,
    ball_reveal_time = 1.20, ball_hold = 0.75, ball_motion_opacity = 0.50,
    singleton_position = (-4.55, -1.15, 0), singleton_size = 30, singleton_width = 4.70,
    error_position = (-4.55, -1.86, 0), error_size = 28, error_width = 4.80,
    metric_flash_time = 0.65, metric_flash_width = 2.2, metric_flash_buff = 0.08,
    metric_flash_time_width = 0.45, metric_flash_color = PALETTE['epsilon'],
    final_hold = 2.20,
)
TIMING = dict(
    reveal = 1.45, curve = 2.15, bridge = 1.65, formula = 1.35, fade = 0.75,
    hold = 1.15, short_hold = 0.48, long_hold = 2.20,
    entry = 1.80, swallow = 1.30, output = 1.30,
    machine_shake = 0.55, input_change = 1.35, input_hold = 1.05,
    copy = 1.50, probe = 2.25, probe_lead = 0.85, zoom_setup = 0.75, refine = 2.80, ruler = 2.00,
    coincide = 1.45, triangle = 1.65, metric_swap = 1.80,
    jump = 1.15, pocket = 2.20, epsilon_shrink = 2.15,
    generic_input = 1.70, cloud = 1.80, selection = 1.70, final_hold = 2.80,
)
FORMULAS = dict(
    evaluation = r'M:f\longmapsto f(0.5)',
    evaluation_spaces = r'M:(C([0,1]),d_\infty)\longrightarrow(\mathbb R,|\cdot|)',
    evaluation_epsilon_bound = r'|M(f_2)-M(f_1)|\leq\varepsilon',
    evaluation_bound = r'|M(f_2)-M(f_1)|\leq d_\infty(f_1,f_2)<\delta=\varepsilon',
    delta_epsilon = r'\delta=\varepsilon',
    input_band_delta = r'\delta', output_axis_epsilon = r'\varepsilon',
    usual_distance = r'd_{\mathbb R}(x,y)=|x-y|',
    discrete_distance = r'd_{\mathrm{disc}}(x,y)=\begin{cases}0,&x=y,\\1,&x\ne y.\end{cases}',
    triangle = r'1\leq1+1',
    step = r'H(x)=\begin{cases}0,&x<0,\\1,&x\geq0.\end{cases}',
    step_usual = r'(\mathbb R,|\cdot|)\overset{H}{\longrightarrow}(\mathbb R,|\cdot|)',
    step_discrete = r'(\mathbb R,d_{\mathrm{disc}})\overset{H}{\longrightarrow}(\mathbb R,|\cdot|)',
    jump = r'|H(-\eta)-H(0)|=1',
    delta_half = r'\delta=\tfrac12',
    singleton = r'B_{d_{\mathrm{disc}}}\!\left(x_0,\tfrac12\right)=\{x_0\}',
    zero = r'|H(x)-H(x_0)|=0<\varepsilon',
    disk_focus = r'x_{%d}', disk_readout = r'H(x_{%d})=', disk_unit = r'1', disk_half = r'\tfrac12',
    disk_singleton = r'B_{d_{\mathrm{disc}}}\!\bigl(x_{%d},\delta\bigr)=\{x_{%d}\}',
    disk_error = r'\bigl|H(x_{%d})-H(x_{%d})\bigr|=0<\varepsilon',
    disk_metric_token = r'd_{\mathrm{disc}}',
)
FORMULA_COLORS = {
    r'f_1': PALETTE['cyan'], r'f_2': PALETTE['rose'],
    r'f_3': PALETTE['cyan'],
    r'\varepsilon': PALETTE['epsilon'], r'\delta': PALETTE['safe'],
}

# 动画实现
config.background_color = BG_COLOR
config.frame_width, config.frame_height = FRAME_WIDTH, FRAME_HEIGHT

if FRAME_RATE is not None:
    config.frame_rate = FRAME_RATE

def _v(point):

    return np.asarray(point, dtype = float)

def _f1(x):
    p = FUNCTION

    return (p['base'] + p['slope'] * x + p['wave_amplitude'] * np.sin(p['wave_frequency'] * PI * x) - p['dip_amplitude'] * np.sin(PI * x)
        + p['irrational_offset'] * math.sqrt(2))

def _f2(x, gap):
    p = FUNCTION

    return _f1(x) + gap * (p['gap_floor'] + p['gap_wave'] * np.sin(p['gap_frequency'] * PI * x) ** 2)

def _input_function(x, spec):

    return _f2(x, spec['gap']) + spec['offset'] + spec['slope'] * x + spec['wave'] * np.sin(spec['frequency'] * PI * x)

def _tex(text, position = None, size = None, color = None, max_width = None, extra_colors = None):
    result = MathTex(text, font_size = size or STYLE['formula_size'], color = color or PALETTE['ink'],
        tex_to_color_map = {**FORMULA_COLORS, **(extra_colors or {})})
    limit = max_width or STYLE['formula_width']

    if result.width > limit:
        result.scale_to_fit_width(limit)

    if position is not None:
        result.move_to(_v(position))

    limit_bottom = SUBTITLE['top'] + SUBTITLE['margin']

    if result.get_bottom()[1] < limit_bottom:
        result.shift(UP * (limit_bottom - result.get_bottom()[1]))

    return result.set_z_index(25)

def _dot(position, color, focus = False):

    return Dot(position, radius = STYLE['focus_radius'] if focus else STYLE['dot_radius'], color = color).set_z_index(15)

def _halo(position, color, radius = None):

    return (Circle(radius = radius or STYLE['halo_radius'], stroke_width = 0, fill_color = color, fill_opacity = STYLE['halo_opacity'])
        .move_to(position).set_z_index(8))

def _guide(a, b, color = None, opacity = None):

    return DashedLine(a, b, dash_length = STYLE['dash_length'], dashed_ratio = STYLE['dash_ratio'], color = color or PALETTE['axis'],
        stroke_width = STYLE['guide_width'], stroke_opacity = STYLE['guide_opacity'] if opacity is None else opacity).set_z_index(2)

def _domain_boundary(a, b):

    return DashedLine(a, b, color = BOUNDARY['color'], stroke_width = BOUNDARY['line_width'], dash_length = BOUNDARY['dash_length'],
        dashed_ratio = BOUNDARY['dash_ratio'], stroke_opacity = BOUNDARY['opacity']).set_z_index(BOUNDARY['z_index'])

def _graph_axes(p):
    axes = Axes(x_range = p['x_range'], y_range = p['y_range'], x_length = p['x_length'], y_length = p['y_length'], tips = False,
        axis_config = dict(color = PALETTE['axis'], stroke_width = STYLE['axis_width'], include_ticks = False, include_numbers = False))
    axes.shift(_v(p['origin']) - axes.c2p(0, 0))
    labels, ticks, bounds = VGroup(), VGroup(), VGroup()

    for x, text in zip(p['ticks'], p['tick_tex']):
        q = axes.c2p(x, 0)

        if not (p.get('smooth_origin', False) and abs(x) < STYLE['algorithm_tolerance']):
            ticks.add(Line(q + UP * STYLE['tick_size'], q + DOWN * STYLE['tick_size'], color = PALETTE['axis'],
                    stroke_width = STYLE['axis_width']))
        label_position = (q + _v(p['origin_label_offset']) if abs(x) < STYLE['algorithm_tolerance'] and 'origin_label_offset' in p
            else q + DOWN * STYLE['tick_label_gap'])
        labels.add(_tex(text, label_position, STYLE['small_size']))

    for y in p.get('y_ticks', ()):

        if abs(y) < STYLE['algorithm_tolerance']:
            continue

        q = axes.c2p(0, y)

        if abs(y) > STYLE['algorithm_tolerance']:
            ticks.add(Line(q + LEFT * STYLE['tick_size'], q + RIGHT * STYLE['tick_size'], color = PALETTE['axis'],
                    stroke_width = STYLE['axis_width']))
            
        labels.add(_tex(f"{y:.{p['tick_decimal_places']}f}", q + LEFT * p['y_tick_label_gap'], STYLE['small_size']))

    if p.get('smooth_origin', False):
        # 取消原点穿轴刻度，以微小圆接头连接两条白色轴，不改变数学坐标
        ticks.add(Dot(axes.c2p(0, 0), radius = p['origin_joint_radius'], color = PALETTE['axis'], stroke_width = 0))

    for x in FUNCTION['domain']:
        if p.get('smooth_origin', False) and abs(x) < STYLE['algorithm_tolerance']:
            continue
        bounds.add(_domain_boundary(axes.c2p(x, 0), axes.c2p(x, p['boundary_height'])))

    return axes, VGroup(_grid(axes, p), axes, ticks, bounds, labels)

def _grid(axes, p):
    result = VGroup().set_z_index(-5)

    if not GRID['enabled']:
        return result
    
    xmin, xmax = p['x_range'][:2]
    ymin, ymax = p['y_range'][:2]
    xunit = np.linalg.norm(axes.c2p(1, 0) - axes.c2p(0, 0))
    yunit = np.linalg.norm(axes.c2p(0, 1) - axes.c2p(0, 0))
    xstep, ystep = GRID['cell_size'] / xunit, GRID['cell_size'] / yunit
    color, width = p.get('grid_color', GRID['color']), p.get('grid_line_width', GRID['line_width'])

    for x in np.arange(math.ceil(xmin / xstep) * xstep, xmax + STYLE['algorithm_tolerance'], xstep):
        if abs(x) > STYLE['algorithm_tolerance']:
            result.add(Line(axes.c2p(x, ymin), axes.c2p(x, ymax), color = color, stroke_width = width, stroke_opacity = GRID['opacity']))

    for y in np.arange(math.ceil(ymin / ystep) * ystep, ymax + STYLE['algorithm_tolerance'], ystep):
        if abs(y) > STYLE['algorithm_tolerance']:
            result.add(Line(axes.c2p(xmin, y), axes.c2p(xmax, y), color = color, stroke_width = width, stroke_opacity = GRID['opacity']))

    return result.set_z_index(-5)

def _single_curve(axes, function, color, width = None):
    xs = np.linspace(*FUNCTION['domain'], STYLE['curve_samples'])
    curve = VMobject(color = color, stroke_width = width or STYLE['curve_width'])
    curve.set_points_smoothly([axes.c2p(x, function(x)) for x in xs])

    return curve.set_z_index(6)

def _gradient_curve(axes, function, gradient = None):
    count = STYLE['curve_segments']
    colors = color_gradient(gradient or FUNCTION['gradient'], count)
    edges = np.linspace(*FUNCTION['domain'], count + 1)
    result = VGroup()

    for a, b, color in zip(edges[:-1], edges[1:], colors):
        xs = np.linspace(a, b, STYLE['samples_per_segment'])
        piece = VMobject(stroke_color = color, stroke_width = STYLE['curve_width'])
        piece.set_points_smoothly([axes.c2p(x, function(x)) for x in xs])
        result.add(piece)

    return result.set_z_index(6)

def _machine(center, scale = 1.0, opaque = False):
    p = MACHINE
    body = RoundedRectangle(width = p['width'], height = p['height'], corner_radius = p['corner'], color = PALETTE['ink'],
        stroke_width = p['frame_width'], fill_color = BG_COLOR, fill_opacity = p['fill_opacity'])
    neck = p['width'] / 2 + p['mouth_gap']
    outer = neck + p['mouth_width']
    left = Polygon([-outer, p['mouth_height'] / 2, 0], [-neck, p['neck_height'] / 2, 0], [-neck, -p['neck_height'] / 2, 0],
        [-outer, -p['mouth_height'] / 2, 0], stroke_color = PALETTE['ink'], stroke_width = p['frame_width'], fill_color = BG_COLOR,
        fill_opacity = p['fill_opacity'])
    right = left.copy().flip(UP, about_point = ORIGIN)
    glyph = _tex('M', size = p['glyph_size'])
    result = VGroup(body, left, right, glyph).scale(scale).move_to(_v(center)).set_z_index(10)

    if opaque:
        # 只在第一镜遮住机器内部；曲线可以经过入口，始终不会显示在箱体里
        body.set_fill(opacity = EVALUATION['machine_fill_opacity']).set_z_index(EVALUATION['machine_body_z'])
        glyph.set_z_index(EVALUATION['machine_glyph_z'])

    return result

def _decimal_prefix(value):
    # 省略号前必须显示真实小数的前几位，使用截断而非四舍五入
    digits = EVALUATION['decimals']
    multiplier = 10**digits
    prefix = math.floor(value * multiplier) / multiplier

    return f'{prefix:.{digits}f}'

def _sample_color(spec):
    lo, hi = FUNCTION['domain']
    fraction = (FUNCTION['midpoint'] - lo) / (hi - lo)
    colors = color_gradient(spec['gradient'], STYLE['curve_segments'])
    index = min(len(colors) - 1, max(0, int(fraction * len(colors))))

    return colors[index]

def _evaluation_readout(index, function, spec):
    p = EVALUATION
    argument = f"{FUNCTION['midpoint']:.{p['sample_decimal_places']}f}"
    value = _decimal_prefix(function(FUNCTION['midpoint']))
    result = MathTex(rf'f_{index}', rf'({argument})=', value, r'\ldots', arg_separator = '', font_size = p['output_size'],
        color = PALETTE['ink'])
    result[0].set_color(spec['gradient'][0])
    result[2:].set_color(_sample_color(spec))

    if result.width > p['output_width']:
        result.scale_to_fit_width(p['output_width'])

    return result.move_to(p['output_position']).set_z_index(25)

def _mapped_readout(index, value, shade):
    p = PROOF
    prefix = _tex(rf'M(f_{index})=', size = p['readout_size'])
    number = DecimalNumber(float(_decimal_prefix(value)), num_decimal_places = EVALUATION['decimals'], font_size = p['readout_size'],
        color = shade)
    ellipsis = _tex(r'\ldots', size = p['readout_size'], color = shade)
    result = VGroup(prefix, number, ellipsis).arrange(RIGHT, buff = p['readout_buff']).set_z_index(25)

    if result.width > p['readout_width']:
        result.scale_to_fit_width(p['readout_width'])

    return result

def _output_epsilon_neighborhood(point, reference, epsilon, scale = 1.0):
    # 数轴上以M(f1)为中心的epsilon邻域；半径括线明确表示epsilon而非2epsilon
    lower, centre, upper = point(reference - epsilon), point(reference), point(reference + epsilon)
    half_width = PROOF['output_band_half_width'] * scale
    fill = Rectangle(width = 2 * half_width, height = upper[1] - lower[1], stroke_width = 0, fill_color = PALETTE['epsilon'],
        fill_opacity = PROOF['output_band_opacity']).move_to(centre)
    caps = VGroup(*[Line(q + LEFT * PROOF['output_cap_half_width'] * scale, q + RIGHT * PROOF['output_cap_half_width'] * scale,
                color = PALETTE['epsilon'], stroke_width = STYLE['guide_width'] * scale) for q in (lower, upper)])
    offset = RIGHT * PROOF['output_epsilon_bracket_x'] * scale
    radius = Line(centre + offset, upper + offset, color = PALETTE['epsilon'], stroke_width = STYLE['axis_width'] * scale)

    return VGroup(fill, caps, radius).set_z_index(4)

class _ZoomNumbers:
    # 复用数字字形；放大过程和数值变化不逐帧调用LaTeX

    def __init__(self, size):
        self.glyphs = {c: MathTex(c, font_size = size, color = PALETTE['axis']) for c in '0123456789.-'}
        self.advance = max(self.glyphs[c].width for c in '0123456789') * APPROACH['tick_digit_spacing']
        self.cache = {}

    def get(self, text):

        if text not in self.cache:
            row, cursor = VGroup(), 0.0

            for char in text:
                advance = self.advance

                if char == '.':
                    advance *= APPROACH['tick_decimal_spacing']
                elif char == '-':
                    advance *= APPROACH['tick_minus_spacing']

                glyph = self.glyphs[char].copy().move_to([cursor + advance / 2, 0, 0])

                if char == '.':
                    glyph.shift(DOWN * APPROACH['tick_decimal_drop'])

                row.add(glyph)
                cursor += advance

            row.move_to(ORIGIN)

            if len(self.cache) >= APPROACH['tick_cache_size']:
                self.cache.pop(next(iter(self.cache)))

            self.cache[text] = row

        return self.cache[text]

class _FunctionApproachView:
    # 整个函数逐步靠近；只增加纵向比例，横坐标范围和相机始终不变

    def __init__(self, scene, axes, gap, epsilon, heading):
        self.scene, self.axes, self.gap, self.epsilon = scene, axes, gap, epsilon
        self.magnification = ValueTracker(1.0)
        self.precision = ValueTracker(APPROACH['tick_initial_precision'])
        self.probe = ValueTracker(PROOF['scan_start'])
        self.scan_reveal, self.output_reveal = ValueTracker(0), ValueTracker(0)
        self.epsilon_reveal, self.delta_reveal = ValueTracker(0), ValueTracker(0)
        self.mapped_reveal = ValueTracker(0)
        xs = np.linspace(*FUNCTION['domain'], STYLE['curve_samples'])
        values = _f1(xs)
        self.focus_value = (float(values.min()) + float(values.max())) / 2
        self.focus_y = axes.c2p(0, self.focus_value)[1]
        self.unit_y = np.linalg.norm(axes.c2p(0, 1) - axes.c2p(0, 0))
        self.left, self.bottom = PROOF['origin'][:2]
        self.right = axes.c2p(PROOF['x_range'][1], 0)[0]
        self.top = self.bottom + PROOF['y_length']
        self.tick_numbers = _ZoomNumbers(STYLE['small_size'])
        self.readout_numbers = _ZoomNumbers(PROOF['readout_size'])
        self.machine_template = _machine(PROOF['machine_center'], MACHINE['proof_scale'], opaque = True)
        self.heading_template = heading.copy()
        self.legend1 = _tex('f_1', size = STYLE['label_size'], color = PALETTE['cyan'])
        self.legend2 = _tex('f_2', size = STYLE['label_size'], color = PALETTE['rose'])
        self.delta_label = _tex(FORMULAS['input_band_delta'], size = STYLE['small_size'], color = PALETTE['safe'])
        self.epsilon_label = _tex(FORMULAS['output_axis_epsilon'], size = STYLE['small_size'], color = PALETTE['epsilon'])

        for label in (self.delta_label, self.epsilon_label):
            label.set_background_stroke(color = BG_COLOR, width = STYLE['math_label_outline_width'], opacity = 1)
            label.set_z_index(STYLE['math_label_z'])

        self.probe_label = _tex('x', size = STYLE['small_size'], color = PALETTE['epsilon'])
        self.scan_prefixes = [_tex(rf'f_{i}(x)=', size = PROOF['readout_size']) for i in (1, 2)]
        self.mapped_prefixes = [_tex(rf'M(f_{i})=', size = PROOF['readout_size']) for i in (1, 2)]
        self.ellipsis = _tex(r'\ldots', size = PROOF['readout_size'])
        self.f1_template = _gradient_curve(axes, _f1, FUNCTION['gradient'])
        self.mono_points = _single_curve(axes, _f1, PALETTE['rose']).get_points().copy()
        self.gap_points = _single_curve(axes, lambda u: _f2(u, 1), PALETTE['rose']).get_points() - self.mono_points
        self.band_points = np.array([axes.c2p(u, _f1(u)) for u in np.linspace(*FUNCTION['domain'], STYLE['band_samples'])])
        self.grid_template = _grid(axes, PROOF)
        self.geometry_key, self.geometry_template = None, None
        self.root = self.draw()
        self.root.add_updater(self.refresh)

    @staticmethod
    def ease(value):
        value = float(np.clip(value, 0, 1))

        return value * value * (3 - 2 * value)

    def point(self, x, y):
        result = self.axes.c2p(x, y)
        result[1] = self.focus_y + (result[1] - self.focus_y) * self.magnification.get_value()

        return result

    def output_point(self, value):
        centre = PROOF['output_axis_bottom'] + PROOF['output_axis_scale'] * self.focus_value
        y = centre + (value - self.focus_value) * PROOF['output_axis_scale'] * self.magnification.get_value()

        return np.array([PROOF['output_axis_x'], y, 0])

    def refresh(self, item):
        fresh = self.draw()

        # 原子替换旧轮廓，避免Cairo在连续变形时残留曲线或数字字形
        for retired in item.get_family():
            if isinstance(retired, VMobject):
                retired.clear_points()

        item.submobjects = fresh.submobjects

    def density(self, places, unit, minimum):
        separation = 10 ** (-places) * unit
        desired = max(1.0, minimum / separation)

        if desired <= 1:
            return [(1, 1.0)]
        
        exponent = int(math.floor(math.log10(desired)))
        candidates = sorted({int(m * 10**n) for n in range(max(0, exponent - 1), exponent + 2) for m in (1, 2, 5, 10)})
        lo, hi = max(n for n in candidates if n <= desired), min(n for n in candidates if n > desired)
        blend = self.ease(math.log(desired / lo) / math.log(hi / lo))

        return [(lo, 1 - blend), (hi, blend)]

    def ticks(self, low, high, coordinate, ruler, limits, unit, kind):
        precision = float(np.clip(self.precision.get_value(), 1, APPROACH['tick_max_precision']))
        lower = int(math.floor(precision))
        upper = min(lower + 1, APPROACH['tick_max_precision'])
        blend = self.ease(precision - lower)
        weights = {}

        for places, precision_weight in ((lower, 1 - blend), (upper, blend)):

            if precision_weight <= 0:
                continue

            for multiplier, density_weight in self.density(places, unit, APPROACH['tick_min_spacing_' + kind]):
                step = 10 ** (-places) * multiplier

                for index in range(math.ceil(low / step - STYLE['algorithm_tolerance']),
                    math.floor(high / step + STYLE['algorithm_tolerance']) + 1):
                    key = (places, index * multiplier)
                    weights[key] = min(1, weights.get(key, 0) + precision_weight * density_weight)

        marks, numbers, line_weights = VGroup(), VGroup(), {}

        for (places, integer), weight in weights.items():
            value = integer * 10 ** (-places)
            y = coordinate(value)
            weight *= self.ease(min(y - limits[0], limits[1] - y) / APPROACH['tick_fade_width_y'])

            if weight < STYLE['algorithm_tolerance'] or (kind == 'y' and abs(value) < STYLE['algorithm_tolerance']):
                continue

            text = '0' if abs(value) < STYLE['algorithm_tolerance'] else f'{value:.{places}f}'
            label = self.tick_numbers.get(text).copy().set_opacity(weight).set_z_index(25)
            a = '0' if text == '0' else f'{value:.{lower}f}'
            b = '0' if text == '0' else f'{value:.{upper}f}'
            width = (1 - blend) * self.tick_numbers.get(a).width + blend * self.tick_numbers.get(b).width
            label.move_to([ruler - STYLE['tick_label_gap'], y, 0])
            label.shift(RIGHT * (ruler - STYLE['tick_label_gap'] - width - label.get_left()[0]))
            numbers.add(label)
            key = round(value, APPROACH['tick_max_precision'] + 2)
            line_weights[key] = (y, min(1, line_weights.get(key, (y, 0))[1] + weight))

        for y, opacity in line_weights.values():
            q = np.array([ruler, y, 0])
            marks.add(Line(q + LEFT * STYLE['tick_size'], q + RIGHT * STYLE['tick_size'], color = PALETTE['axis'],
                    stroke_width = STYLE['axis_width'], stroke_opacity = opacity))
            
        return VGroup(marks, numbers)

    def shaped_curve(self, points, color, width = None, opacity = 1):
        # 贝塞尔控制点对函数值线性，预先计算差形即可连续变形，无需逐帧重新拟合
        current = points.copy()
        current[:, 1] = self.focus_y + (current[:, 1] - self.focus_y) * self.magnification.get_value()
        curve = VMobject(stroke_color = color, stroke_width = width or STYLE['curve_width'], stroke_opacity = opacity)
        curve.tolerance_for_point_equality = STYLE['algorithm_tolerance']

        return curve.set_points(current).set_z_index(6)

    def readout(self, index, value, shade, point, direction):
        blend = self.ease(self.mapped_reveal.get_value())
        old, new = self.scan_prefixes[index - 1], self.mapped_prefixes[index - 1]
        prefix_width = (1 - blend) * old.width + blend * new.width
        prefix = VGroup()

        for template, opacity in ((old, 1 - blend), (new, blend)):
            if opacity <= 0:
                continue

            part = template.copy().set_opacity(opacity).move_to(ORIGIN)
            part.shift(RIGHT * (-part.get_left()[0]))
            prefix.add(part)

        number = self.readout_numbers.get(_decimal_prefix(value)).copy().set_color(shade).move_to(ORIGIN)
        number.shift(RIGHT * (prefix_width + PROOF['readout_buff'] - number.get_left()[0]))
        tail = self.ellipsis.copy().set_color(shade).move_to(ORIGIN)
        tail.shift(RIGHT * (number.get_right()[0] + PROOF['readout_buff'] - tail.get_left()[0]))

        return VGroup(prefix, number, tail).next_to(point, direction, buff = PROOF['output_label_gap']).set_z_index(25)

    def geometry(self):
        factor = self.magnification.get_value()
        gap, epsilon = self.gap.get_value(), self.epsilon.get_value()
        key = (factor, gap, epsilon, self.delta_reveal.get_value(), self.precision.get_value())

        if key == self.geometry_key:
            return self.geometry_template.copy()
        
        lo, hi = FUNCTION['domain']
        grid = self.grid_template.copy()
        ylow = self.focus_value + (self.bottom - self.focus_y) / (self.unit_y * factor)
        yhigh = self.focus_value + (self.top - self.focus_y) / (self.unit_y * factor)
        axes = VGroup(Line([self.left, self.bottom, 0], [self.right, self.bottom, 0], color = PALETTE['axis'],
                stroke_width = STYLE['axis_width']), Line([self.left, self.bottom, 0], [self.left, self.top, 0], color = PALETTE['axis'],
                stroke_width = STYLE['axis_width']),
            Dot([self.left, self.bottom, 0], radius = PROOF['origin_joint_radius'], color = PALETTE['axis']))
        
        # 横轴刻度永远是同一个0、0.5、1.0，横向位置不随函数靠近或纵向放大变化
        for value, text in zip(PROOF['ticks'], PROOF['tick_tex']):
            q = self.axes.c2p(value, 0)
            q[1] = self.bottom

            if value == 0:
                label = self.tick_numbers.get('0').copy().move_to(q + _v(PROOF['origin_label_offset']))
            else:
                axes.add(Line(q + UP * STYLE['tick_size'], q + DOWN * STYLE['tick_size'], color = PALETTE['axis'],
                        stroke_width = STYLE['axis_width']))
                label = self.tick_numbers.get(text).copy().move_to(q + DOWN * STYLE['tick_label_gap'])

            axes.add(label)

        axes.add(self.ticks(ylow, yhigh, lambda y: self.point(0, y)[1], self.left, (self.bottom, self.top), self.unit_y * factor, 'y'))
        boundary_x = self.axes.c2p(FUNCTION['domain'][1], 0)[0]
        boundary = _domain_boundary([boundary_x, self.bottom, 0], [boundary_x, self.top, 0])
        axes.add(boundary)
        f1 = self.f1_template.copy().stretch(factor, 1, about_point = [0, self.focus_y, 0])
        f2 = self.shaped_curve(self.mono_points + gap * self.gap_points, PALETTE['rose'])
        band = VGroup()

        if self.delta_reveal.get_value() > 0:
            upper, lower = self.band_points.copy(), self.band_points[::-1].copy()
            upper[:, 1] = self.focus_y + (upper[:, 1] + epsilon * self.unit_y - self.focus_y) * factor
            lower[:, 1] = self.focus_y + (lower[:, 1] - epsilon * self.unit_y - self.focus_y) * factor
            fill = Polygon(*np.vstack([upper, lower]), stroke_width = 0, fill_color = PALETTE['safe'], fill_opacity = PROOF['band_opacity']
            ).set_z_index(0)
            edges = VGroup(*[self.shaped_curve(self.mono_points + UP * sign * epsilon * self.unit_y, PALETTE['safe'], STYLE['guide_width'],
                        PROOF['band_edge_opacity']) for sign in (-1, 1)])
            bracket_x = PROOF['band_bracket_x']
            bracket = Line(self.point(bracket_x, _f1(bracket_x)), self.point(bracket_x, _f1(bracket_x) + epsilon), color = PALETTE['safe'],
                stroke_width = STYLE['axis_width'])
            caps = VGroup(*[Line(q + LEFT * PROOF['band_cap_half_width'], q + RIGHT * PROOF['band_cap_half_width'], color = PALETTE['safe'],
                        stroke_width = STYLE['guide_width']) for q in (bracket.get_start(), bracket.get_end())])
            band_label = self.delta_label.copy().move_to(bracket.get_end() + _v(PROOF['band_label_offset']))
            band = VGroup(fill, edges, bracket, caps, band_label).fade(1 - self.delta_reveal.get_value())

        legends = VGroup()

        for template, anchor, function, sign in ((self.legend1, PROOF['f1_label'], _f1, -1),
            (self.legend2, PROOF['f2_label'], lambda u: _f2(u, gap), 1),):
            u = np.clip(self.axes.p2c(anchor)[0], lo, hi)
            y = self.point(u, function(u))[1] + sign * APPROACH['legend_gap']
            legends.add(template.copy().move_to(
                    [anchor[0], np.clip(y, self.bottom + APPROACH['legend_gap'], self.top - APPROACH['legend_gap']), 0]))
        endpoints = VGroup(*[Dot(self.point(u, _f1(u)), radius = STYLE['dot_radius'], color = color)
                for u, color in zip(FUNCTION['domain'], (FUNCTION['gradient'][0], FUNCTION['gradient'][-1]))]).set_z_index(8)
        
        self.geometry_template = VGroup(grid, band, axes, f1, f2, endpoints, legends)
        self.geometry_key = key

        return self.geometry_template.copy()

    def draw(self):
        factor = self.magnification.get_value()
        gap, epsilon, x = self.gap.get_value(), self.epsilon.get_value(), self.probe.get_value()
        plot = self.geometry()
        lower, upper = self.point(x, _f1(x)), self.point(x, _f2(x, gap))
        shade = color_gradient(FUNCTION['gradient'], STYLE['curve_segments'])[
            min(int(x * STYLE['curve_segments']), STYLE['curve_segments'] - 1)]
        scan_line = Line(lower, upper, color = PALETTE['epsilon'], stroke_width = PROOF['scan_width']).set_z_index(15)
        dots = VGroup(Dot(lower, radius = STYLE['dot_radius'], color = shade),
            Dot(upper, radius = STYLE['dot_radius'], color = PALETTE['rose'])).set_z_index(16)
        probe_label = self.probe_label.copy().move_to(np.array([lower[0], self.bottom, 0]) + _v(PROOF['probe_label_offset']))
        probe_label.fade(self.mapped_reveal.get_value())
        scan = VGroup(scan_line, dots, probe_label).fade(1 - self.scan_reveal.get_value())
        plot.add(scan)
        output_bottom = PROOF['output_axis_bottom']
        output_top = output_bottom + PROOF['output_axis_scale'] * PROOF['y_range'][1]
        output_centre = PROOF['output_axis_bottom'] + PROOF['output_axis_scale'] * self.focus_value
        value_low = self.focus_value + (output_bottom - output_centre) / (PROOF['output_axis_scale'] * factor)
        value_high = self.focus_value + (output_top - output_centre) / (PROOF['output_axis_scale'] * factor)
        output_axis = VGroup(Line([PROOF['output_axis_x'], output_bottom, 0], [PROOF['output_axis_x'], output_top, 0],
                color = PALETTE['axis'], stroke_width = STYLE['axis_width']), self.ticks(value_low, value_high,
                lambda value: self.output_point(value)[1], PROOF['output_axis_x'], (output_bottom, output_top),
                PROOF['output_axis_scale'] * factor, 'output')).set_z_index(15)
        output_lower, output_upper = self.output_point(_f1(x)), self.output_point(_f2(x, gap))
        output_points = VGroup(Line(output_lower, output_upper, color = PALETTE['epsilon'], stroke_width = PROOF['scan_width']),
            Dot(output_lower, radius = PROOF['output_dot_radius'], color = shade),
            Dot(output_upper, radius = PROOF['output_dot_radius'], color = PALETTE['rose'])).set_z_index(18)
        row1 = self.readout(1, _f1(x), shade, output_lower, DR)
        row2 = self.readout(2, _f2(x, gap), PALETTE['rose'], output_upper, UR)
        output_points.fade(1 - self.output_reveal.get_value())
        row1.fade(1 - self.output_reveal.get_value())
        row2.fade(1 - self.output_reveal.get_value())
        neighborhood = _output_epsilon_neighborhood(self.output_point, _f1(x), epsilon)
        epsilon_anchor = (self.output_point(_f1(x)) + self.output_point(_f1(x) + epsilon)) / 2
        epsilon_anchor += RIGHT * PROOF['output_epsilon_bracket_x'] + _v(PROOF['output_epsilon_label_offset'])
        epsilon_label = self.epsilon_label.copy().move_to(epsilon_anchor)
        accepted = VGroup(neighborhood, epsilon_label).fade(1 - self.epsilon_reveal.get_value())

        return VGroup(plot, self.machine_template.copy(), output_axis, accepted, output_points, row1, row2, self.heading_template.copy())

def _evaluation_stage():
    p = EVALUATION
    spec = INPUTS[0]
    fn = lambda x: _input_function(x, spec)
    axes, art = _graph_axes(p)
    curve = _gradient_curve(axes, fn, spec['gradient'])
    endpoints = VGroup(*[_dot(axes.c2p(x, fn(x)), color)
            for x, color in zip(FUNCTION['domain'], (spec['gradient'][0], spec['gradient'][-1]))])
    label = _tex('f_1', p['f_label'], color = spec['gradient'][0])
    machine = _machine(p['machine_center'], opaque = True)
    readout = _evaluation_readout(1, fn, spec)
    mapping = _tex(FORMULAS['evaluation'], p['mapping_position'], p['mapping_size'])
    xmid, shade = FUNCTION['midpoint'], _sample_color(spec)
    projection = _guide(axes.c2p(xmid, 0), axes.c2p(xmid, fn(xmid)), shade)
    midpoint = _dot(axes.c2p(xmid, fn(xmid)), shade)

    return dict(axes = axes, art = art, curve = curve, endpoints = endpoints, label = label, projection = projection, midpoint = midpoint,
        graph = VGroup(art, curve, endpoints, label, projection, midpoint), machine = machine, readout = readout, mapping = mapping)

def _discrete_flight_rate(alpha):
    # 单次柔和起步和停稳；位移、速度、加速度、加加速度连续
    alpha = float(np.clip(alpha, 0, 1))
    ramp = DISCRETE['ease_fraction']

    def integral(value):

        return value**4 * (2.5 - 3 * value + value**2)

    if alpha < ramp:
        return ramp * integral(alpha / ramp) / (1 - ramp)
    
    if alpha > 1 - ramp:
        return 1 - ramp * integral((1 - alpha) / ramp) / (1 - ramp)
    
    return (alpha - ramp / 2) / (1 - ramp)

def _discrete_clock(alpha):
    # 整组只有一次快→慢→快变化，最低速度仍然大于0
    alpha = float(np.clip(alpha, 0, 1))

    return alpha + DISCRETE['stream_speed_contrast'] * math.sin(TAU * alpha) / TAU

def _discrete_path_data(controls):
    # 累计弧长查表，避免贝塞尔参数均匀变化时空间速度忽快忽慢
    controls = np.asarray(controls, dtype = float)
    parameter = np.linspace(0, 1, DISCRETE['path_samples'])
    t = parameter[:, None]
    points = ((1 - t) ** 3 * controls[0] + 3 * (1 - t) ** 2 * t * controls[1] + 3 * (1 - t) * t**2 * controls[2] + t**3 * controls[3])
    lengths = np.concatenate(([0.0], np.cumsum(np.linalg.norm(np.diff(points, axis = 0), axis = 1))))

    return dict(controls = controls, parameter = parameter, distance = lengths / lengths[-1], length = float(lengths[-1]))

def _discrete_path_point(path, fraction):

    if fraction <= 0:
        return path['controls'][0].copy()
    if fraction >= 1:
        return path['controls'][3].copy()
    
    t = float(np.interp(fraction, path['distance'], path['parameter']))
    one = 1 - t
    c = path['controls']

    return one**3 * c[0] + 3 * one**2 * t * c[1] + 3 * one * t**2 * c[2] + t**3 * c[3]

def _discrete_particle_plan(anchor, centre):
    p = DISCRETE
    count = p['point_count']
    rng = np.random.default_rng(p['random_seed'])

    # 随机间距总和为2pi；每个间距都大于下限，不将落点排成等距圆
    free_angle = TAU - count * p['minimum_angular_gap']
    gaps = p['minimum_angular_gap'] + free_angle * rng.dirichlet(np.full(count, p['angular_gap_randomness']))
    angles = (rng.uniform(0, TAU) + np.concatenate(([0.0], np.cumsum(gaps[:-1])))) % TAU
    rng.shuffle(angles)
    offsets = rng.uniform(*p['source_offset_bounds'], size = count) * rng.choice((-1, 1), size = count)
    sources = anchor + offsets[:, None] * RIGHT
    targets = centre + p['circle_radius'] * np.column_stack((np.cos(angles), np.sin(angles), np.zeros(count)))

    # 均匀错开发射，多点航程重叠；统一时钟平滑调节发射和飞行的速度
    starts = np.arange(count, dtype = float) * p['launch_interval']
    durations = np.full(count, p['flight_time'])
    ends = starts + durations
    rise = (targets[:, 1] - sources[:, 1])[:, None]
    controls1 = sources + UP * rise * p['flight_vertical_controls'][0]
    controls2 = targets - UP * rise * (1 - p['flight_vertical_controls'][1])
    paths = [_discrete_path_data((source, c1, c2, target)) for source, c1, c2, target in zip(sources, controls1, controls2, targets)]

    return dict(sources = sources, targets = targets, angles = angles, starts = starts, durations = durations, ends = ends,
        total_time = p['stream_time'], clock_span = float(ends.max()), paths = paths)

def _discrete_particle_frame(plan, alpha):
    time = _discrete_clock(alpha) * plan['clock_span']
    ages = time - plan['starts']
    fractions = np.clip(ages / plan['durations'], 0, 1)
    positions = np.array([_discrete_path_point(path, _discrete_flight_rate(fraction)) for path, fraction in zip(plan['paths'], fractions)])
    fade = np.clip(ages / DISCRETE['point_birth_time'], 0, 1)
    opacity = fade**3 * (10 + fade * (-15 + 6 * fade))

    return positions, opacity, ages

def validate_parameters():

    if TIME_SCALE <= 0:
        raise ValueError('TIME_SCALE must be positive.')
    if not 0 < FUNCTION['midpoint'] < 1:
        raise ValueError('The machine sample must be inside the interval.')
    if GRID['cell_size'] <= 0 or not 0 <= GRID['opacity'] <= 1 or GRID['line_width'] <= 0:
        raise ValueError('Grid cell size, opacity and stroke width are invalid.')
    if not INPUTS:
        raise ValueError('The machine needs at least one input function.')
    
    for spec in INPUTS:
        values = _input_function(np.linspace(*FUNCTION['domain'], STYLE['curve_samples']), spec)
        if values.min() < EVALUATION['y_range'][0] or values.max() > EVALUATION['y_range'][1]:
            raise ValueError('An input curve is outside the opening coordinate frame.')
        
    if not math.isclose(FUNCTION['gap_floor'] + FUNCTION['gap_wave'], 1.0):
        raise ValueError('The normalized difference profile must have supremum 1.')
    profiles = [(PROOF['gap_start'], PROOF['epsilon_start'])] + list(PROOF['refinements'])
    if any(not 0 < gap < epsilon for gap, epsilon in profiles):
        raise ValueError('Every proof frame requires 0 < d_infinity < delta = epsilon.')
    factors = APPROACH['vertical_factors']
    if len(factors) != len(PROOF['refinements']) or any(a >= b for a, b in zip((1.0,) + tuple(factors), factors)):
        raise ValueError('Each function refinement needs an increasing vertical magnification.')
    
    profiles = [(PROOF['gap_start'], PROOF['epsilon_start'])] + list(PROOF['refinements'])
    all_factors = (1.0,) + tuple(factors)

    if any(g2 * f2 >= g1 * f1 or e2 * f2 >= e1 * f1
        for (g1, e1), f1, (g2, e2), f2 in zip(profiles[:-1], all_factors[:-1], profiles[1:], all_factors[1:])):
        raise ValueError('Both the true function distance and the visible gap must shrink at each step.')
    
    xs = np.linspace(*FUNCTION['domain'], STYLE['curve_samples'])
    baseline = _f1(xs)
    centre = (baseline.min() + baseline.max()) / 2
    unit_y = PROOF['y_length'] / PROOF['y_range'][1]
    centre_y = PROOF['origin'][1] + centre * unit_y

    for (gap, epsilon), factor in zip(profiles, all_factors):
        for values in (baseline, _f2(xs, gap), baseline - epsilon, baseline + epsilon):
            plotted_y = centre_y + (values - centre) * unit_y * factor
            if plotted_y.min() < PROOF['origin'][1] or plotted_y.max() > PROOF['origin'][1] + PROOF['y_length']:
                raise ValueError('Vertical magnification would crop a whole function or its delta band.')
            
    if not math.isclose(PROOF['scan_stops'][-1], FUNCTION['midpoint']):
        raise ValueError('The scan must finish at 0.5 before displaying M(fi).')
    
    discrete = DISCRETE

    if discrete['axis_half_length'] <= FRAME_WIDTH / 2:
        raise ValueError('The discrete-metric number line must extend beyond both screen edges.')
    
    count = discrete['point_count']

    if not isinstance(count, int) or count < 2 or not discrete['point_colors']:
        raise ValueError('The discrete-metric stream needs multiple points and a color palette.')
    if not 0 < discrete['source_offset_bounds'][0] <= discrete['source_offset_bounds'][1]:
        raise ValueError('Nearby sampled points must be distinct from x0.')
    if count * discrete['minimum_angular_gap'] >= TAU or discrete['minimum_angular_gap'] < 0:
        raise ValueError('The chosen point count and minimum angular gap do not fit on the circle.')
    if discrete['angular_gap_randomness'] <= 0 or discrete['path_samples'] < 3:
        raise ValueError('Random spacing and timing interpolation need positive, sufficient samples.')
    if not 0 <= discrete['stream_speed_contrast'] < 1 or not 0 < discrete['ease_fraction'] < 0.5:
        raise ValueError('The shared clock must move forward and the single ease ramp must fit the flight.')
    if (min(discrete['stream_time'], discrete['point_birth_time'], discrete['launch_interval'], discrete['flight_time']) <= 0):
        raise ValueError('Particle-stream durations must be positive.')
    if (discrete['flight_time'] <= discrete['launch_interval'] or discrete['point_birth_time'] >= discrete['flight_time']):
        raise ValueError('Flights must overlap and points must finish appearing before they arrive.')
    if discrete['circle_radius'] <= 0:
        raise ValueError('The circle radius must be positive.')
    
    centre = np.array([discrete['anchor_x'], discrete['axis_y'] + discrete['circle_height'], 0])

    if (abs(centre[0]) + discrete['circle_radius'] >= FRAME_WIDTH / 2 or centre[1] - discrete['circle_radius'] < discrete['axis_y']):
        raise ValueError('The copied anchor and its circle must fit above the number line.')
    
    step = STEP
    count = len(step['sample_x'])

    if count < 9 or (count - 1) % 8 or len(set(step['sample_x'])) != count:
        raise ValueError('The fourfold disk needs 8k+1 distinct input identities.')
    if any(not step['x_range'][0] < x < step['x_range'][1] for x in step['sample_x']):
        raise ValueError('Every sampled input must lie on the opening horizontal axis.')
    
    all_focus = step['focus_sequence'] + step['ball_focus_sequence'] + step['after_flash_focus_sequence']

    if not all_focus or any(not 0 <= index < count for index in all_focus):
        raise ValueError('The viewpoint sequence contains an invalid point identity.')
    if any(a == b for a, b in zip(step['focus_sequence'], step['focus_sequence'][1:])):
        raise ValueError('Successive viewpoints must select different points.')
    if not 0 <= step['view_pan_strength'] < 0.5 or not 0 < step['exchange_bend'] < 0.3:
        raise ValueError('Disk remapping and exchange curvature are outside the smooth display range.')
    
    center = _v(step['disk_center'])
    radius = step['disk_radius']

    if radius <= 0 or center[1] - radius - STYLE['focus_radius'] < SUBTITLE['top'] + SUBTITLE['margin']:
        raise ValueError('The disk or its dots would enter the subtitle area.')
    if abs(center[0]) + radius + STYLE['focus_radius'] >= FRAME_WIDTH / 2:
        raise ValueError('The disk must fit inside the visible frame.')

def _disk_ease(alpha):
    alpha = float(np.clip(alpha, 0, 1))

    return alpha**3 * (10 + alpha * (-15 + 6 * alpha))

def _disk_initial_angles():
    p = STEP
    count = len(p['sample_x'])
    focus = p['focus_sequence'][0]
    ring = p['ring_start_angle'] + TAU * np.arange(count - 1) / (count - 1)

    # 首次落盘按横向位置分配槽位，减少从横轴进入时的路径交叉
    ring = ring[np.argsort(np.cos(ring))]
    angles = np.full(count, np.nan)
    angles[np.arange(count) != focus] = ring

    return angles

def _disk_focus_pose(angles, focus):
    result = np.zeros(len(angles), dtype = complex)
    ring = np.arange(len(angles)) != focus
    result[ring] = np.exp(1j * angles[ring])

    return result

def _disk_mobius(z, parameter):
    # 保圆盘的观察坐标重映射；只借用可视化，离散距离仍由点身份定义
    z = np.asarray(z, dtype = complex)

    return (z - parameter) / (1 - np.conjugate(parameter) * z)

def _disk_view_map(angles, new_focus, alpha, direction = 1, rotation_amount = None):
    u = _disk_ease(alpha)
    weight = math.sin(PI * u) ** 2
    amount = STEP['view_rotation'] if rotation_amount is None else rotation_amount
    rotation = direction * (amount * u + STEP['view_sway'] * weight)
    parameter = STEP['view_pan_strength'] * weight * np.exp(1j * (angles[new_focus] + rotation))

    return parameter, rotation, weight

def _disk_switch_pose(angles, old_focus, new_focus, alpha, direction = 1, rotation_amount = None):
    # 观察布局的换中心：其他点留在圆周，两交换点沿相反浅弧运动
    u = _disk_ease(alpha)
    _, rotation, _ = _disk_view_map(angles, new_focus, alpha, direction, rotation_amount)
    result = _disk_focus_pose(angles, old_focus) * np.exp(1j * rotation)
    ray = np.exp(1j * (angles[new_focus] + rotation))
    bend = STEP['exchange_bend'] * math.sin(PI * u)
    result[old_focus] = ray * (u + 1j * bend)
    result[new_focus] = ray * (1 - u - 1j * bend)
    parameter, _, _ = _disk_view_map(angles, new_focus, alpha, direction, rotation_amount)

    return _disk_mobius(result, parameter)

def _disk_finish_angles(angles, old_focus, new_focus, direction = 1, rotation_amount = None):
    result = angles.copy() + direction * (STEP['view_rotation'] if rotation_amount is None else rotation_amount)
    result[old_focus] = result[new_focus]
    result[new_focus] = np.nan

    return result

def _disk_link_edges(angles, focus, rotation = 0):
    # 四瓣理想多边形与交织正交弧；整体具有D4旋转和镜像对称
    ring = [i for i in range(len(angles)) if i != focus]
    count = len(ring)
    step = TAU / count
    origin = STEP['ring_start_angle'] + rotation
    ring.sort(key = lambda index: round((angles[index] - origin) / step) % count)
    quadrant = count // 4
    slot_edges = set()

    def connect(first, last):
        pair = tuple(sorted((int(first) % count, int(last) % count)))

        if pair[0] != pair[1]:
            slot_edges.add(pair)

    for turn in range(4):
        origin_slot = turn * quadrant

        for offset in range(1, quadrant // 2):
            connect(origin_slot + offset, origin_slot + quadrant - offset)

        connect(origin_slot, origin_slot + quadrant)

    for first, last in STEP['weave_seed_fractions']:
        a, b = round(first * quadrant), round(last * quadrant)

        for turn in range(4):
            shift = turn * quadrant
            connect(a + shift, b + shift)
            connect(-a + shift, -b + shift)

    edges = [(ring[a], ring[b]) for a, b in sorted(slot_edges)]
    edges.extend((focus, ring[turn * quadrant + quadrant // 2]) for turn in range(4))

    return tuple(edges)

def _disk_geodesic(start, end):
    # 连接当前点身份的正交圆弧；经过圆心的情形是直径线
    p = STEP
    original_start, original_end = complex(start), complex(end)
    t = np.linspace(0, 1, p['guide_samples'])
    determinant = start.real * end.imag - start.imag * end.real

    if abs(determinant) < STYLE['algorithm_tolerance']:
        points = (1 - t) * start + t * end
    else:
        first_rhs = (1 + abs(start) ** 2) / 2
        last_rhs = (1 + abs(end) ** 2) / 2
        center = ((first_rhs * end.imag - start.imag * last_rhs) + 1j * (start.real * last_rhs - first_rhs * end.real)) / determinant

        if abs(center) > 1 / p['geodesic_diameter_tolerance']:
            points = (1 - t) * start + t * end
        else:
            # 按圆角度均匀采样，端点接近圆周时也不会变成长弦或突然弹弯
            radius = abs(start - center)
            first = np.angle(start - center)
            sweep = np.angle((end - center) / (start - center))
            points = center + radius * np.exp(1j * (first + sweep * t))

    points = np.asarray(points, dtype = complex)
    points[0], points[-1] = original_start, original_end

    return points

class _DiscreteDiskView:
    # 以观察点为中心的距离视图，不用圆周弦长表示离散度量

    def __init__(self, nodes):
        p = STEP
        self.nodes = nodes
        self.center = _v(p['disk_center'])
        self.radius = p['disk_radius']
        self.angles = _disk_initial_angles()
        self.focus = p['focus_sequence'][0]
        self.local = _disk_focus_pose(self.angles, self.focus)
        self.map_parameter = 0j
        self.frame_rotation = 0.0
        self.guide_rotation = 0.0
        self.guide_weight = 0.0
        self.template = Circle().get_points().copy()
        self.surface = Circle(stroke_width = 0, fill_color = p['disk_fill_color'], fill_opacity = p['disk_fill_opacity']).set_z_index(2)
        self.boundary = Circle(color = p['disk_color'], stroke_width = p['disk_width'], stroke_opacity = p['disk_opacity']).set_z_index(4)
        self.edges = _disk_link_edges(self.angles, self.focus)
        self.old_edge_count = None
        self.common_edge_count = 0
        self.guide_transition = 0.0
        self.guides = VGroup(*[VMobject(color = p['guide_color'], stroke_width = p['guide_width']).set_z_index(3) for _ in self.edges])
        self.geometry = VGroup(self.surface, self.boundary)
        self.refresh_geometry()

    def project(self, local):
        z = np.asarray(local, dtype = complex)

        return self.center + self.radius * np.stack((z.real, z.imag, np.zeros(z.shape)), axis = -1)

    def refresh_geometry(self):
        p = STEP
        points = self.template * self.radius + self.center
        self.surface.set_points(points)
        self.boundary.set_points(points)

        for index, (curve, (start, end)) in enumerate(zip(self.guides, self.edges)):
            local = _disk_geodesic(self.local[start], self.local[end])
            curve.set_points_as_corners(self.project(local))
            weight = 1.0

            if self.old_edge_count is not None and index >= self.common_edge_count:
                weight = 1 - self.guide_transition if index < self.old_edge_count else self.guide_transition
            curve.set_stroke(opacity = (p['guide_opacity'] + p['guide_motion_opacity'] * self.guide_weight) * weight)

    def begin_switch(self, new_focus, direction, rotation):
        # 两套连线均贴着真实节点，用平滑淡变完成观察角色的交接
        next_angles = _disk_finish_angles(self.angles, self.focus, new_focus, direction, rotation)
        next_edges = _disk_link_edges(next_angles, new_focus, self.frame_rotation + direction * rotation)
        next_keys = {frozenset(edge) for edge in next_edges}
        old_keys = {frozenset(edge) for edge in self.edges}
        common = [(edge, curve) for edge, curve in zip(self.edges, self.guides) if frozenset(edge) in next_keys]
        old_only = [(edge, curve) for edge, curve in zip(self.edges, self.guides) if frozenset(edge) not in next_keys]
        new_only = [edge for edge in next_edges if frozenset(edge) not in old_keys]
        self.common_edge_count = len(common)
        self.old_edge_count = len(common) + len(old_only)
        self.guide_transition = 0.0
        self.edges = tuple(edge for edge, _ in common + old_only) + tuple(new_only)
        self.guides.submobjects = [curve for _, curve in common + old_only] + [
            VMobject(color = STEP['guide_color'], stroke_width = STEP['guide_width'], stroke_opacity = 0).set_z_index(3) for _ in new_only]
        self.refresh_geometry()

    def finish_switch(self):
        count = self.old_edge_count
        common = self.common_edge_count
        self.guides.remove(*list(self.guides[common:count]))
        self.edges = self.edges[:common] + self.edges[count:]
        self.old_edge_count = None
        self.common_edge_count = 0
        self.guide_transition = 0.0

    def set_pose(self, local, map_parameter = 0j, guide_rotation = None, guide_weight = 0):
        self.local = np.asarray(local, dtype = complex)
        self.map_parameter = map_parameter
        self.guide_rotation = self.frame_rotation if guide_rotation is None else guide_rotation
        self.guide_weight = guide_weight
        self.refresh_geometry()

        for node, position in zip(self.nodes, self.project(self.local)):
            node.move_to(position)

    def observations(self, graph, index):
        p = STEP
        value = 0 if p['sample_x'][index] < 0 else 1
        shade = PALETTE['cyan'] if value == 0 else PALETTE['green']
        label = _tex(FORMULAS['disk_focus'] % (index + 1), self.center + _v(p['focus_label_offset']), p['focus_label_size'], shade)
        label.set_background_stroke(color = BG_COLOR, width = STYLE['math_label_outline_width'], opacity = 1)
        label.set_z_index(STYLE['math_label_z'])
        identity = FORMULAS['disk_focus'] % (index + 1)
        readout = VGroup(_tex(FORMULAS['disk_readout'] % (index + 1), size = p['readout_size'], extra_colors = {identity: shade}),
            _tex(str(value), size = p['readout_size'], color = shade))
        readout.arrange(RIGHT, buff = p['readout_gap']).move_to(p['readout_position'])
        unit = Line(self.center, self.center + RIGHT * self.radius, color = PALETTE['epsilon'], stroke_width = p['unit_width']
        ).set_z_index(6)
        one = _tex(FORMULAS['disk_unit'], self.center + RIGHT * self.radius / 2 + _v(p['unit_label_offset']), p['unit_label_size'],
            PALETTE['epsilon'])
        one.set_background_stroke(color = BG_COLOR, width = STYLE['math_label_outline_width'], opacity = 1)
        one.set_z_index(STYLE['math_label_z'])

        return VGroup(label, readout, unit, one)

    def evidence(self, index):
        p = STEP
        shade = PALETTE['cyan'] if p['sample_x'][index] < 0 else PALETTE['green']
        identity = FORMULAS['disk_focus'] % (index + 1)
        colors = {identity: shade}
        singleton = _tex(FORMULAS['disk_singleton'] % (index + 1, index + 1), p['singleton_position'], p['singleton_size'],
            max_width = p['singleton_width'], extra_colors = colors)
        error = _tex(FORMULAS['disk_error'] % (index + 1, index + 1), p['error_position'], p['error_size'], max_width = p['error_width'],
            extra_colors = colors)
        
        return VGroup(singleton, error)

    def halo(self, index):

        return (Circle(radius = STEP['halo_radius'], color = PALETTE['epsilon'], stroke_width = STEP['halo_width'])
            .move_to(self.nodes[index]).set_z_index(23))

class _Story:
    def __init__(self, scene):
        self.s = scene
        self.stage = None

    def beat(self, *animations, duration = 'reveal', **kwargs):
        seconds = TIMING[duration] if isinstance(duration, str) else duration
        self.s.play(*animations, run_time = seconds * TIME_SCALE, **kwargs)

    def pause(self, duration = 'hold'):
        seconds = TIMING[duration] if isinstance(duration, str) else duration
        self.s.wait(seconds * TIME_SCALE)

    def settle(self, *objects):

        for obj in objects:
            obj.clear_updaters(recursive = True)

        self.s.clear()
        self.s.add(*objects)
        self.stage = VGroup(*objects)

    def cross(self, *objects):

        if self.stage is None:
            animations = [FadeIn(obj) for obj in objects]
        else:
            # 顶部公式先退场再入场，几何对象同时交接，避免两套公式叠印
            old_headers = [obj for obj in self.stage if isinstance(obj, MathTex) and obj.get_center()[1] > STYLE['header_min_y']]
            new_headers = [obj for obj in objects if isinstance(obj, MathTex) and obj.get_center()[1] > STYLE['header_min_y']]
            old_ids, new_ids = {id(obj) for obj in old_headers}, {id(obj) for obj in new_headers}
            old_geometry = VGroup(*[obj for obj in self.stage if id(obj) not in old_ids])
            new_geometry = VGroup(*[obj for obj in objects if id(obj) not in new_ids])
            s = self.s
            s.clear()
            s.add(old_geometry, *old_headers)
            animations = [FadeOut(old_geometry), FadeIn(new_geometry)]

            if old_headers and new_headers:
                animations.append(Succession(FadeOut(VGroup(*old_headers)), FadeIn(VGroup(*new_headers))))
            elif old_headers:
                animations.append(FadeOut(VGroup(*old_headers)))
            elif new_headers:
                animations.append(FadeIn(VGroup(*new_headers)))

        self.beat(*animations, duration = 'bridge')
        self.s.clear()
        self.s.add(*objects)

    def machine(self):
        s, p, m = self.s, EVALUATION, MACHINE
        st = _evaluation_stage()
        self.beat(Create(st['art']), FadeIn(st['machine']))
        self.beat(Create(st['curve']), FadeIn(st['endpoints']), Write(st['label']), Create(st['projection']), FadeIn(st['midpoint']),
            duration = 'curve')
        self.pause('hold')
        xmid = FUNCTION['midpoint']

        for index, spec in enumerate(INPUTS, 1):
            fn = lambda x, spec = spec: _input_function(x, spec)
            shade = _sample_color(spec)
            new_readout = _evaluation_readout(index, fn, spec)

            if index > 1:
                new_curve = _gradient_curve(st['axes'], fn, spec['gradient'])
                new_label = _tex(rf'f_{index}', p['f_label'], color = spec['gradient'][0])
                old_label = st['label']
                endpoint_moves = [dot.animate.move_to(st['axes'].c2p(x, fn(x))).set_color(color) for dot, x, color in zip(
                        st['endpoints'], FUNCTION['domain'], (spec['gradient'][0], spec['gradient'][-1]))]
                new_projection = _guide(st['axes'].c2p(xmid, 0), st['axes'].c2p(xmid, fn(xmid)), shade)
                self.beat(Transform(st['curve'], new_curve), ReplacementTransform(old_label, new_label), FadeOut(st['readout']),
                    *endpoint_moves, Transform(st['projection'], new_projection),
                    st['midpoint'].animate.move_to(st['axes'].c2p(xmid, fn(xmid))).set_color(shade), duration = 'input_change')
                st['graph'] = VGroup(st['art'], st['curve'], st['endpoints'], new_label, st['projection'], st['midpoint'])
                st['label'] = new_label

            st['readout'] = new_readout
            travelling = st['curve'].copy().set_z_index(12)
            mouth_target = travelling.copy().scale(p['travel_mouth_scale'])
            mouth_target.move_to(st['machine'][1].get_center() + UP * p['travel_lift'])
            s.add(travelling)
            self.beat(Transform(travelling, mouth_target), duration = 'entry')
            self.beat(FadeOut(travelling, shift = RIGHT * p['ingest_shift'], scale = p['ingest_scale']), duration = 'swallow')
            center = st['machine'].get_center().copy()

            def shake(machine, alpha):
                envelope = math.sin(PI * alpha) ** 2
                dx = m['shake_x'] * math.sin(TAU * m['shake_cycles'] * alpha) * envelope
                dy = m['shake_y'] * math.sin(2 * TAU * m['shake_cycles'] * alpha) * envelope
                machine.move_to(center + RIGHT * dx + UP * dy)

            self.beat(UpdateFromAlphaFunc(st['machine'], shake), duration = 'machine_shake', rate_func = linear)
            st['machine'].move_to(center)
            spark = _dot(st['machine'][2].get_center(), shade, True)
            self.beat(spark.animate.move_to(_v(p['exit_pulse_end'])), duration = 'output')
            self.beat(FadeOut(spark), Write(st['readout']), duration = 'formula')
            self.pause('input_hold')

        self.beat(Write(st['mapping']), duration = 'formula')
        self.pause('long_hold')
        self.settle(st['graph'], st['machine'], st['readout'], st['mapping'])
        self.evaluation_state = st

    def machine_continuity(self):
        self.machine()
        self.evaluation_continuity()

    def evaluation_continuity(self):
        s, p = self.s, PROOF
        axes, art = _graph_axes(p)
        f1 = _gradient_curve(axes, _f1)
        label1 = _tex('f_1', p['f1_label'], STYLE['label_size'], PALETTE['cyan'])
        label2 = _tex('f_2', p['f2_label'], STYLE['label_size'], PALETTE['rose'])
        base_graph = VGroup(art, f1, label1)
        machine = _machine(p['machine_center'], MACHINE['proof_scale'], opaque = True)
        heading = _tex(FORMULAS['evaluation_spaces'], STYLE['header'], size = STYLE['formula_size'])

        def output_point(value):

            return np.array([p['output_axis_x'], p['output_axis_bottom'] + p['output_axis_scale'] * value, 0])

        output_axis = VGroup(Line(
                output_point(0), output_point(p['y_range'][1]), color = PALETTE['axis'], stroke_width = STYLE['axis_width']))
        
        for y, text in zip(p['output_ticks'], p['output_tick_tex']):
            q = output_point(y)
            output_axis.add(Line(q + LEFT * STYLE['tick_size'], q + RIGHT * STYLE['tick_size'], color = PALETTE['axis'],
                    stroke_width = STYLE['axis_width']))
            output_axis.add(_tex(text, q + LEFT * p['output_label_gap'], STYLE['small_size']))

        if hasattr(self, 'evaluation_state'):
            old = self.evaluation_state
        else:
            # 独立渲染第二镜也从第一镜的落幅开始，便于直接剪辑拼接
            old = _evaluation_stage()

        # 坐标、曲线、标签各自对应变换，不将不同层级的大组硬插值
        s.clear()
        s.add(*old['art'], old['curve'], old['label'], old['endpoints'], old['projection'], old['midpoint'], old['machine'], old['readout'],
            old['mapping'])
        art_changes = [(Succession(FadeOut(old['art'][i]), FadeIn(art[i])) if i in (2, 4) else ReplacementTransform(old['art'][i], art[i]))
            for i in range(1, len(art))]
        grid_change = Succession(FadeOut(old['art'][0]), FadeIn(art[0]))
        shade = _sample_color(INPUTS[0])
        first_projection = _guide(axes.c2p(FUNCTION['midpoint'], 0), axes.c2p(FUNCTION['midpoint'], _f1(FUNCTION['midpoint'])), shade)
        endpoint_moves = [dot.animate.move_to(axes.c2p(x, _f1(x))).set_color(color) for dot, x, color in zip(
                old['endpoints'], FUNCTION['domain'], (FUNCTION['gradient'][0], FUNCTION['gradient'][-1]))]
        self.beat(*art_changes, grid_change, ReplacementTransform(old['curve'], f1), Succession(FadeOut(old['label']), FadeIn(label1)),
            *endpoint_moves, old['midpoint'].animate.move_to(axes.c2p(FUNCTION['midpoint'], _f1(FUNCTION['midpoint']))).set_color(shade),
            Transform(old['projection'], first_projection), ReplacementTransform(old['machine'], machine),
            Succession(FadeOut(old['readout']), Create(output_axis)), Succession(FadeOut(old['mapping']), FadeIn(heading)),
            duration = 'bridge')
        base_graph.add(old['endpoints'], old['midpoint'])
        s.clear()
        s.add(base_graph, machine, heading, output_axis, old['projection'])

        # 先看到两个完整函数；所有横坐标在之后的演示中保持原位
        gap, epsilon = ValueTracker(p['gap_start']), ValueTracker(p['epsilon_start'])
        f2 = _single_curve(axes, lambda x: _f2(x, gap.get_value()), PALETTE['rose'])
        self.beat(Create(f2), Write(label2), duration = 'copy')
        previous = Group(*s.mobjects)
        previous.clear_updaters(recursive = True)
        view = _FunctionApproachView(s, axes, gap, epsilon, heading)
        view.root.clear_updaters(recursive = True)
        s.clear()
        s.add(previous)
        self.beat(FadeOut(previous), FadeIn(view.root), duration = 'zoom_setup')
        s.clear()
        s.add(view.root)
        view.root.add_updater(view.refresh)
        self.approach_view = view

        # 线段先在两条函数之间滑动，随后数轴上的两个点与线段两端同步
        self.continuity_phase = 'scan_line'
        self.beat(view.scan_reveal.animate.set_value(1), duration = 'fade')
        self.beat(view.probe.animate.set_value(p['scan_lead_stop']), duration = 'probe_lead')
        self.continuity_phase = 'scan_outputs'
        self.beat(view.output_reveal.animate.set_value(1), duration = 'fade')

        for x in p['scan_stops']:
            self.beat(view.probe.animate.set_value(x), duration = 'probe')
            self.pause('short_hold')

        # 扫描读数是fi(x)。回到0.5后才将标签改为机器M的输出，值保持不跳变
        self.beat(view.mapped_reveal.animate.set_value(1), duration = APPROACH['mapped_label_time'])

        def smootherstep(alpha):
            alpha = float(np.clip(alpha, 0, 1))

            return alpha**3 * (10 + alpha * (-15 + 6 * alpha))

        def reciprocal_lerp(start, end, fraction):

            return 1 / ((1 - fraction) / start + fraction / end)

        def approach(profile, factor):
            next_gap, next_epsilon = profile
            factor_start = view.magnification.get_value()
            visible_gap_start = gap.get_value() * factor_start
            visible_epsilon_start = epsilon.get_value() * factor_start

            def change(magnification, alpha):
                progress = smootherstep(alpha)
                current_factor = (1 - progress) * factor_start + progress * factor
                magnification.set_value(current_factor)

                # 一致距离和画面里的竖直间距都单调缩小；纵向放大不造成回弹
                gap.set_value(reciprocal_lerp(visible_gap_start, next_gap * factor, progress) / current_factor)
                epsilon.set_value(reciprocal_lerp(visible_epsilon_start, next_epsilon * factor, progress) / current_factor)
                view.precision.set_value(APPROACH['tick_initial_precision'] + math.log10(current_factor))

            self.beat(UpdateFromAlphaFunc(view.magnification, change), duration = 'refine', rate_func = linear)

        self.continuity_phase = 'functions_approach'
        approach(p['refinements'][0], APPROACH['vertical_factors'][0])
        self.pause('short_hold')

        # 先提出输出允许误差epsilon，delta此时完全未出现
        self.continuity_phase = 'epsilon'
        self.beat(view.epsilon_reveal.animate.set_value(1), duration = 'fade')
        bound = _tex(FORMULAS['evaluation_epsilon_bound'], p['inequality_position'], p['inequality_size'])
        self.beat(Write(bound), duration = 'formula')
        self.pause('hold')

        # 再选delta=epsilon，展示函数空间中的整条delta条带
        self.continuity_phase = 'delta'
        self.beat(view.delta_reveal.animate.set_value(1), duration = 'copy')
        delta = _tex(FORMULAS['delta_epsilon'], p['delta_position'], p['delta_size'])
        self.beat(Write(delta), duration = 'formula')
        full_bound = _tex(FORMULAS['evaluation_bound'], p['inequality_position'], p['inequality_size'])
        self.beat(ReplacementTransform(bound, full_bound), duration = 'formula')
        self.pause('hold')
        self.continuity_phase = 'functions_approach_with_bounds'

        for profile, factor in zip(p['refinements'][1:], APPROACH['vertical_factors'][1:]):
            approach(profile, factor)
            self.pause('short_hold')

        self.continuity_phase = 'final_enlarged'
        self.pause('long_hold')

        # 结尾保留纵向放大后的完整函数，直接交接到下一镜，不做缩小或相机复位动画
        view.refresh(view.root)
        self.settle(*view.root.submobjects, full_bound, delta)

    def discrete_metric(self):
        s, p = self.s, DISCRETE
        formula = _tex(FORMULAS['discrete_distance'], p['definition_center'], p['definition_size'])
        self.discrete_phase = 'definition'

        # 此镜不承接前镜落幅，也不做开场淡入；第一帧直接给出居中的定义
        s.clear()
        self.stage = None
        s.add(formula)
        self.pause(p['definition_hold'])
        self.beat(formula.animate.scale(p['header_size'] / p['definition_size']).move_to(p['header_position']),
            duration = p['definition_move_time'])

        axis = Line([-p['axis_half_length'], p['axis_y'], 0], [p['axis_half_length'], p['axis_y'], 0], color = PALETTE['axis'],
            stroke_width = STYLE['axis_width'])
        
        # 此数轴有意超出镜头左右边缘，几何检查只豁免它的横向裁切
        axis.intentional_horizontal_clip = True
        ticks = VGroup()

        for value in p['ticks']:
            q = np.array([value * p['axis_unit'], p['axis_y'], 0])
            ticks.add(Line(q + UP * STYLE['tick_size'], q + DOWN * STYLE['tick_size'], color = PALETTE['axis'],
                    stroke_width = STYLE['axis_width']))
            text = '0' if value == 0 else f"{value:.{p['tick_decimals']}f}"
            ticks.add(_tex(text, q + DOWN * STYLE['tick_label_gap'], p['tick_font']))

        self.discrete_phase = 'number_line'
        self.beat(Create(axis), FadeIn(ticks), duration = p['axis_reveal_time'])
        anchor_position = np.array([p['anchor_x'], p['axis_y'], 0])
        anchor = _dot(anchor_position, PALETTE['cyan'], True).set_z_index(p['anchor_z'])
        anchor_label = _tex('x_0', anchor_position + _v(p['anchor_label_offset']), p['center_label_size'], PALETTE['cyan'])
        self.beat(FadeIn(anchor, scale = p['point_pick_scale']), Write(anchor_label), duration = p['anchor_reveal_time'])
        self.pause(p['anchor_hold'])
        centre = anchor_position + UP * p['circle_height']
        centre_dot = anchor.copy().clear_updaters()
        s.add(centre_dot)
        copy_path = _discrete_path_data((anchor_position, anchor_position + (centre - anchor_position) * p['copy_controls'][0],
                anchor_position + (centre - anchor_position) * p['copy_controls'][1], centre,))
        self.discrete_phase = 'copy_anchor'
        self.beat(UpdateFromAlphaFunc(centre_dot,
                lambda dot, alpha: dot.move_to(_discrete_path_point(copy_path, _discrete_flight_rate(alpha)))),
            duration = p['copy_move_time'], rate_func = linear)
        centre_dot.move_to(centre)
        centre_label = _tex('x_0', centre + _v(p['center_label_offset']), p['center_label_size'], PALETTE['cyan'])
        centre_label.set_background_stroke(color = BG_COLOR, width = STYLE['math_label_outline_width'], opacity = 1)

        # 圆仅表示这些不同点到x0的离散距离都为1，不表示圆周点之间的欧氏弦长
        circle = (Circle(radius = p['circle_radius'], color = p['circle_color'], stroke_width = p['circle_width'],
                stroke_opacity = p['circle_opacity']).move_to(centre).set_z_index(5))
        self.beat(Create(circle), Write(centre_label), duration = p['circle_reveal_time'])
        self.pause(p['circle_hold'])
        angle = p['radius_angle_degrees'] * DEGREES
        radius_end = centre + p['circle_radius'] * np.array([math.cos(angle), math.sin(angle), 0])
        radius = Line(centre, radius_end, color = p['radius_color'], stroke_width = p['radius_width']).set_z_index(10)
        radius_label = _tex('1', (centre + radius_end) / 2 + _v(p['radius_label_offset']), p['radius_label_size'], p['radius_color'])
        radius_label.set_background_stroke(color = BG_COLOR, width = STYLE['math_label_outline_width'], opacity = 1)
        radius_label.set_z_index(STYLE['math_label_z'])
        self.beat(Create(radius), Write(radius_label), duration = p['radius_reveal_time'])
        plan = _discrete_particle_plan(anchor_position, centre)
        particles = VGroup(*[Dot(position, radius = p['point_radius'], color = p['point_colors'][i % len(p['point_colors'])])
                .set_z_index(17).set_opacity(0) for i, position in enumerate(plan['sources'])])
        landed = VGroup()
        self.discrete_state = dict(axis = axis, ticks = ticks, formula = formula, anchor = anchor, anchor_label = anchor_label,
            center_dot = centre_dot, center_label = centre_label, circle = circle, radius = radius, radius_label = radius_label,
            landed_points = landed, particles = particles, source_positions = plan['sources'], target_positions = plan['targets'],
            plan = plan, stream_progress = 0.0, launched_points = 0)
        s.discrete_metric_state = self.discrete_state
        s.add(particles)

        def flow(group, alpha):
            positions, opacity, ages = _discrete_particle_frame(plan, alpha)
            self.discrete_state['stream_progress'] = float(alpha)
            self.discrete_state['launched_points'] = int(np.count_nonzero(ages >= 0))
            landed.submobjects = [token for token, age, duration in zip(group, ages, plan['durations'])
                if age >= duration - STYLE['algorithm_tolerance']]
            
            # 直接按当前时间求位置，不累积位移；淡入与起步同时进行
            for token, position, visibility in zip(group, positions, opacity):
                token.move_to(position).set_opacity(float(visibility))

        self.discrete_phase = 'particle_stream'
        self.beat(UpdateFromAlphaFunc(particles, flow), duration = plan['total_time'], rate_func = linear)
        flow(particles, 1)
        self.discrete_phase = 'final'
        self.pause(p['final_hold'])
        self.settle(axis, ticks, formula, anchor, anchor_label, centre_dot, centre_label, circle, radius, radius_label, particles)

    def discrete_step(self):
        s, p = self.s, STEP
        axes = Axes(x_range = p['x_range'], y_range = p['y_range'], x_length = p['x_length'], y_length = p['y_length'], tips = False,
            axis_config = dict(color = PALETTE['axis'], stroke_width = STYLE['axis_width'], include_ticks = False, include_numbers = False)
        )
        axes.shift(_v(p['origin']) - axes.c2p(0, 0))
        ticks = VGroup()

        for x in p['x_ticks']:
            q = axes.c2p(x, 0)
            ticks.add(Line(q + UP * STYLE['tick_size'], q + DOWN * STYLE['tick_size'], color = PALETTE['axis'],
                    stroke_width = STYLE['axis_width']))
            label_position = q + (_v(p['origin_label_offset']) if x == 0 else DOWN * STYLE['tick_label_gap'])
            ticks.add(_tex(str(x), label_position, STYLE['small_size']))

        ticks.add(_tex('1', axes.c2p(0, 1) + LEFT * STYLE['tick_label_gap'], STYLE['small_size']))
        negative = Line(axes.c2p(p['x_range'][0], 0), axes.c2p(0, 0), color = PALETTE['cyan'], stroke_width = STYLE['curve_width']
        ).set_z_index(7)
        positive = Line(axes.c2p(0, 1), axes.c2p(p['x_range'][1], 1), color = PALETTE['green'], stroke_width = STYLE['curve_width']
        ).set_z_index(7)
        open_point = (Circle(radius = STYLE['open_radius'], color = PALETTE['cyan'], stroke_width = STYLE['open_width'],
                fill_color = BG_COLOR, fill_opacity = 1).move_to(axes.c2p(0, 0)).set_z_index(16))
        closed_point = _dot(axes.c2p(0, 1), PALETTE['green'], True)
        graph = VGroup(axes, ticks, negative, positive, open_point, closed_point, _grid(axes, p))
        heading = _tex(FORMULAS['step'], STYLE['header'], p['header_size'])
        self.step_phase = 'graph'

        if self.stage is None:
            s.add(graph, heading)
        else:
            self.cross(graph, heading)

        self.pause(p['graph_hold'])
        source_positions = np.array([axes.c2p(x, 0) for x in p['sample_x']])
        colors = [PALETTE['cyan'] if x < 0 else PALETTE['green'] for x in p['sample_x']]
        nodes = VGroup(*[Dot(position, radius = p['point_radius'], color = color).set_z_index(15)
                for position, color in zip(source_positions, colors)])
        self.step_phase = 'samples'
        self.beat(LaggedStart(*[FadeIn(node) for node in nodes], lag_ratio = p['sample_reveal_lag']), duration = p['sample_reveal_time'])
        self.pause(p['sample_hold'])
        view = _DiscreteDiskView(nodes)
        targets = view.project(view.local)
        entry_paths = [_discrete_path_data((source, source + UP * p['entry_start_lift'], target + UP * p['entry_end_lift'], target))
            for source, target in zip(source_positions, targets)]
        total = p['entry_flight_time'] + (len(nodes) - 1) * p['entry_lag']
        mini = graph.copy().scale_to_fit_width(p['mini_width']).move_to(p['mini_center'])
        metric = _tex(FORMULAS['step_discrete'], STYLE['header'], p['metric_size'],
            extra_colors = {FORMULAS['disk_metric_token']: PALETTE['ink']})
        self.step_state = dict(graph = graph, metric = metric, view = view, nodes = nodes, focus = view.focus,
            positions = source_positions.copy(), phase_progress = 0.0, entry_targets = targets, ball_visible = False, evidence = None,
            completed_pre = 0, completed_ball = 0)
        s.step_disk_state = self.step_state
        self.step_phase = 'enter_disk'

        def enter(group, alpha):
            self.step_state['phase_progress'] = float(alpha)
            positions = []

            for index, (node, path) in enumerate(zip(group, entry_paths)):
                age = alpha * total - index * p['entry_lag']
                position = _discrete_path_point(path, _disk_ease(age / p['entry_flight_time']))
                node.move_to(position)
                positions.append(position)

            self.step_state['positions'] = np.array(positions)

        self.beat(Transform(graph, mini, rate_func = _disk_ease), ReplacementTransform(heading, metric, rate_func = _disk_ease),
            FadeIn(view.geometry, rate_func = _disk_ease), UpdateFromAlphaFunc(nodes, enter, rate_func = linear), duration = total)
        enter(nodes, 1)
        view.set_pose(view.local)
        halo = view.halo(view.focus)
        observations = view.observations(graph, view.focus)
        self.step_state.update(
            halo = halo, observations = observations, ball_visible = False, evidence = None, completed_pre = 0, completed_ball = 0)
        self.step_phase = 'focus'
        self.beat(Create(view.guides), FadeIn(halo), FadeIn(observations), duration = p['observation_reveal_time'])
        self.pause(p['pre_focus_hold'])
        ball = half = evidence = None

        def change_focus(chosen, move_number, with_ball):
            nonlocal halo, observations, evidence
            old = view.focus
            direction = (1 if move_number % 2 == 0 else -1) if with_ball else 1
            rotation = p['view_rotation'] if with_ball else p['pre_rotation']
            duration = p['view_move_time'] if with_ball else p['pre_move_time']
            target_halo = view.halo(chosen)
            next_observations = view.observations(graph, chosen)
            next_evidence = view.evidence(chosen) if with_ball else None
            self.step_phase = 'select_viewpoint'
            self.beat(FadeOut(halo), FadeIn(target_halo), duration = p['select_time'])
            self.step_phase = 'move_viewpoint'
            view.begin_switch(chosen, direction, rotation)

            def turn(group, alpha):
                local = _disk_switch_pose(view.angles, old, chosen, alpha, direction, rotation)
                parameter, angle, weight = _disk_view_map(view.angles, chosen, alpha, direction, rotation)
                view.guide_transition = _disk_ease(alpha)
                view.set_pose(local, parameter, view.frame_rotation + angle, weight)
                target_halo.move_to(nodes[chosen])

                if with_ball:
                    # 内圆保持可见；观察坐标转换的中间帧不作为度量读数
                    opacity = 1 - (1 - p['ball_motion_opacity']) * weight
                    ball.set_stroke(opacity = opacity)
                    ball.set_fill(opacity = p['ball_opacity'] * opacity)
                self.step_state.update(positions = view.project(local), phase_progress = float(alpha), old_focus = old, new_focus = chosen)

            animations = [UpdateFromAlphaFunc(nodes, turn, rate_func = linear),
                Transform(observations, next_observations, rate_func = _disk_ease),]
            
            if with_ball:
                animations.append(Transform(evidence, next_evidence, rate_func = _disk_ease))

            self.beat(*animations, duration = duration)
            turn(nodes, 1)

            # 保留平滑变换的落幅，再换成目标文字，令下标、配色元数据也同步更新
            s.remove(observations)
            s.add(next_observations)
            observations = next_observations

            if with_ball:
                s.remove(evidence)
                s.add(next_evidence)
                evidence = next_evidence

            view.angles = _disk_finish_angles(view.angles, old, chosen, direction, rotation)
            view.focus = chosen
            view.frame_rotation += direction * rotation
            view.finish_switch()
            view.set_pose(_disk_focus_pose(view.angles, chosen))
            s.camera.frame.move_to(ORIGIN)
            halo = target_halo
            self.step_state.update(focus = chosen, halo = halo, observations = observations, evidence = evidence, phase_progress = 1.0,
                positions = view.project(view.local))
            key = 'completed_ball' if with_ball else 'completed_pre'
            self.step_state[key] += 1
            self.step_phase = 'ball_focus' if with_ball else 'focus'

            if with_ball and self.step_state['completed_ball'] == len(p['ball_focus_sequence']):
                token = metric.get_part_by_tex(FORMULAS['disk_metric_token'], substring = False)
                box = Rectangle(width = token.width + 2 * p['metric_flash_buff'], height = token.height + 2 * p['metric_flash_buff'],
                    color = p['metric_flash_color'], stroke_width = p['metric_flash_width'], fill_opacity = 0)
                box.move_to(token).set_z_index(45)
                self.beat(ShowPassingFlash(box, time_width = p['metric_flash_time_width']), duration = p['metric_flash_time'])
                self.pause(p['focus_hold'])
            elif with_ball:
                self.pause(p['focus_hold'])
            else:
                self.pause(p['pre_focus_hold'])

        for move_number, chosen in enumerate(p['focus_sequence'][1:]):
            change_focus(chosen, move_number, False)

        self.step_phase = 'delta_ready'
        ball = (Circle(radius = view.radius * p['ball_radius'], color = PALETTE['safe'], stroke_width = p['ball_width'],
                fill_color = PALETTE['safe'], fill_opacity = p['ball_opacity']).move_to(view.center).set_z_index(5))
        angle = p['ball_label_angle']
        label_position = view.center + view.radius * p['ball_radius'] * np.array([math.cos(angle), math.sin(angle), 0])
        half = _tex(FORMULAS['delta_half'], label_position + _v(p['ball_label_offset']), p['ball_label_size'], PALETTE['safe'])
        half.set_background_stroke(color = BG_COLOR, width = STYLE['math_label_outline_width'], opacity = 1)
        half.set_z_index(STYLE['math_label_z'])
        evidence = view.evidence(view.focus)
        self.step_state.update(ball = ball, delta_label = half, evidence = evidence, ball_visible = True)
        self.beat(GrowFromCenter(ball), Write(half), Write(evidence), duration = p['ball_reveal_time'])
        self.pause(p['ball_hold'])

        for move_number, chosen in enumerate(p['ball_focus_sequence']):
            change_focus(chosen, move_number, True)
        for move_number, chosen in enumerate(p['after_flash_focus_sequence'], start = len(p['ball_focus_sequence'])):
            change_focus(chosen, move_number, True)

        self.step_phase = 'final'
        self.pause(p['final_hold'])
        self.settle(graph, metric, view.geometry, view.guides, nodes, halo, observations, ball, half, evidence)

class _SceneSettings:
    def setup(self):
        super().setup()
        validate_parameters()
        self.camera.background_color = BG_COLOR
        self.camera.frame.set(width = FRAME_WIDTH, height = FRAME_HEIGHT).move_to(ORIGIN)

def _independent(scene, method):
    # 只计算前镜落幅，不输出前镜帧；独立Scene也能直接首尾拼接
    # 整段入口不经过这里，所以没有额外渲染或重复内容
    sequence = ('machine_continuity', 'discrete_metric', 'discrete_step')
    story = _Story(scene)
    preceding = sequence[: sequence.index(method)]

    if preceding:
        scene.next_section(name = 'prepare_previous_frame', skip_animations = True)
        for name in preceding:
            getattr(story, name)()
        scene.next_section(name = method, skip_animations = False)

    getattr(story, method)()

class EvaluationMachine(_SceneSettings, MovingCameraScene):
    # 合并场景：三个函数输入M，再用相同机器演示一致度量下的连续性

    def construct(self):
        _independent(self, 'machine_continuity')

class DiscreteMetric(_SceneSettings, MovingCameraScene):
    # 中央定义、数轴选点、单位圆周上的离散距离

    def construct(self):
        _Story(self).discrete_metric()

class DiscreteStepContinuity(_SceneSettings, MovingCameraScene):
    # 阶跃图的横轴点进入圆盘；平滑换观察点，展示单点邻域

    def construct(self):
        _Story(self).discrete_step()

class PartFourFilm(_SceneSettings, MovingCameraScene):
    # 整段版；离散度量镜直接切入中央定义，其余分镜沿用几何衔接

    def construct(self):
        story = _Story(self)
        story.machine_continuity()
        story.discrete_metric()
        story.discrete_step()
