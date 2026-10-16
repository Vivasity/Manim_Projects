from manim import *
import math
import numpy as np
from svgelements import Path as SVGPath

# 全部可调参数
BG_COLOR = "#000012"
FRAME_WIDTH, FRAME_HEIGHT = 128 / 9, 8.0
FRAME_RATE = 60                      # 平滑成片使用60帧；改为None可沿用命令行
TIME_SCALE = 1.0                     # 全部运动、停顿统一乘此参数
PALETTE = dict(
    axis = "#FFFFFF", ink = "#FFFFFF", blue = "#56CEE8", cyan = "#56CEE8",
    green = "#9EE3A2", yellow = "#E8EE63", pale_yellow = "#FFE17D",
    mint = "#68E6C0", rose = "#EF819B", muted = "#687C98", gray = "#747B89",
)
STYLE = dict(
    axis_width = 2.0, curve_width = 4.2, interval_width = 5.0, guide_width = 1.35,
    guide_opacity = 0.34, dash_length = 0.105, boundary_dashes = 96,
    boundary_ratio = 0.55, boundary_width = 1.65, boundary_opacity = 0.65,
    dot_radius = 0.075, open_radius = 0.078, open_width = 2.5,
    halo_radius = 0.18, halo_opacity = 0.10, fill_opacity = 0.085,
    local_opacity = 0.13, local_width = 2.3, formula_size = 38, label_size = 30,
    small_size = 27, formula_width = 12.6, header = (0, 3.10, 0),
    label_outline = 3.0, label_outline_color = "#000000", formula_z = 40, point_z = 20,
    foreground_formula_z = 52, formula_backplate_z = 51,
    halo_z = 18, local_z = 11, band_z = -1, strike_z = 45,
    curve_segments = 40, samples_per_segment = 5,
    tick_half_length = 0.058, tick_size = 25, axis_overhang = 1.25,
    formula_background_buff = 0.10,
    numeric_tolerance = 1e-8, minimum_draw_radius = 1e-4, minimum_hold_frames = 1,
)
TIMING = dict(
    symbol_write = 0.80, symbol_gap = 0.22, strike = 0.55, gray = 0.38,
    symbols_hold = 0.70, reveal = 1.35, formula = 1.15, bridge = 1.85,
    movement = 2.50, short_hold = 0.45, hold = 1.20, long_hold = 2.20,
    range_request = 1.50, range_response = 1.55, icon_morph = 2.35, neighborhood_reveal = 1.45, particle_travel = 3.40,
    endpoint_remove = 1.15, local_reveal = 0.85, point_move = 2.15,
    boundary_move = 1.80, trial_shrink = 0.95, dimensions = 2.10,
    sphere_turn = 5.20, carpet_level = 1.65, carpet_zoom = (4.20, 4.60), carpet_zoom_hold = 0.30,
    carpet_restore = 4.20, sample_sweep = 5.70, mapping_probe = 2.60,
    final_hold = 3.00, join_hold = 0.18, fade = 0.75,
    formula_flash = 1.45, disk_final_hold = 5.00, preimage_probe = 1.20, preimage_collect = 1.50,
)
OPENING = dict(
    symbols = (r"\varepsilon", r"\delta", r"d"),
    colors = (PALETTE['blue'], PALETTE['green'], PALETTE['pale_yellow']),
    positions = ((0, 1.52, 0), (0, 0.0, 0), (0, -1.52, 0)),
    size = 102, strike_half_length = 0.77, strike_width = 3.4,
)
RANGES = dict(
    input_center = (-3.55, -0.15, 0), output_center = (3.55, -0.15, 0),
    icon_width = 3.30, contour_width = 2.2, contour_fill = 0.07,
    icon_morph_arc = -PI / 12,
    input_label = (-3.55, 2.08, 0), output_label = (3.55, 2.08, 0), set_label_size = 40,
    arrow_start = (-1.55, -0.15, 0), arrow_end = (1.55, -0.15, 0),
    arrow_width = 1.8, arrow_tip = 0.17, f_position = (0, 0.22, 0),
    # 圆心使用官方SVG坐标定位。x0位于掌部，明显偏离整个点赞轮廓的中心
    x0_svg = (22.0, 21.0), fx0_svg = (12.5, 13.0), delta_radius = 0.52, epsilon_radius = 0.63,
    point_label_direction = (0, -1, 0), point_label_gap = 0.08,
    point_label_outline_color = "#000000", point_label_outline_width = 4.0,
    point_label_size = 29, radius_label_size = 32, sample_radius = 0.044,
    circle_width = 2.0, circle_fill = 0.055, circle_dash_length = 0.080, circle_dash_gap = 0.060,
    radius_width = 1.55, delta_radius_angle = 0.62 * PI, epsilon_radius_angle = 0.32 * PI,
    delta_label_offset = (-0.18, 0.16, 0), epsilon_label_offset = (0.13, 0.16, 0),
    # 以下坐标为圆半径的比例；所有采样点均严格位于对应圆的内部
    input_fractions = ((-0.65, 0.10), (-0.10, 0.65), (0.62, 0.22), (0.70, -0.47), (-0.67, -0.50)),
    output_fractions = ((-0.65, 0.20), (-0.12, 0.68), (0.58, 0.30), (0.80, -0.25), (-0.80, -0.30)),
    travel_control_x = 1.15, travel_lift = -0.45, travel_lag = 0.17,
    contour_samples_per_curve = 12, containment_circle_samples = 128, containment_margin = 0.025,
)
# 直接内嵌官方SVG路径，不依赖外部图片或SVG文件；等比例缩放保留原始轮廓
# 来源：B站视频页公开HTML中的video-like-icon / video-fav-icon
BILIBILI_ICONS = dict(
    source = "https://www.bilibili.com/video/BV1xx411c7mD/",
    like = r"M9.77234 30.8573V11.7471H7.54573C5.50932 11.7471 3.85742 13.3931 3.85742 15.425V27.1794C3.85742 29.2112 5.50932 30.8573 7.54573 30.8573H9.77234ZM11.9902 30.8573V11.7054C14.9897 10.627 16.6942 7.8853 17.1055 3.33591C17.2666 1.55463 18.9633 0.814421 20.5803 1.59505C22.1847 2.36964 23.243 4.32583 23.243 6.93947C23.243 8.50265 23.0478 10.1054 22.6582 11.7471H29.7324C31.7739 11.7471 33.4289 13.402 33.4289 15.4435C33.4289 15.7416 33.3928 16.0386 33.3215 16.328L30.9883 25.7957C30.2558 28.7683 27.5894 30.8573 24.528 30.8573H11.9911H11.9902Z",
    favorite = r"M19.8071 9.26152C18.7438 9.09915 17.7624 8.36846 17.3534 7.39421L15.4723 3.4972C14.8998 2.1982 13.1004 2.1982 12.4461 3.4972L10.6468 7.39421C10.1561 8.36846 9.25639 9.09915 8.19315 9.26152L3.94016 9.91102C2.63155 10.0734 2.05904 11.6972 3.04049 12.6714L6.23023 15.9189C6.96632 16.6496 7.29348 17.705 7.1299 18.7605L6.39381 23.307C6.14844 24.6872 7.62063 25.6614 8.84745 25.0119L12.4461 23.0634C13.4276 22.4951 14.6544 22.4951 15.6359 23.0634L19.2345 25.0119C20.4614 25.6614 21.8518 24.6872 21.6882 23.307L20.8703 18.7605C20.7051 17.705 21.0339 16.6496 21.77 15.9189L24.9597 12.6714C25.9412 11.6972 25.3687 10.0734 24.06 9.91102L19.8071 9.26152Z",
)
INTERVAL = dict(
    axis_half_length = FRAME_WIDTH / 2 + STYLE['axis_overhang'], axis_y = -0.28, left = -3.35, right = 3.35,
    ticks = tuple(range(-5, 6)), axis_unit = 1.5, tick_label_gap = 0.39,
    endpoint_label_offset = (0, 0.42, 0), label_position = (0, 2.70, 0),
    endpoint_fade_shift = 0.38,
    probe_start = 0.10, probe_positions = (-2.65, 2.60, -0.75, 0.10),
    local_fraction = 0.58, local_cap = 0.95, local_height = 0.28,
    probe_label_offset = (0, 0.34, 0), wiggle_amplitude = 0.33,
    wiggle_cycles = 2, local_endpoint_radius = 0.047,
)
DISK = dict(
    center = (0, -0.12, 0), radius = 2.06,
    plane_half_x = FRAME_WIDTH / 2 + STYLE['axis_overhang'],
    plane_half_y = FRAME_HEIGHT / 2 + STYLE['axis_overhang'], plane_opacity = 0.65,
    plane_ticks_x = tuple(range(-8, 9)), plane_ticks_y = (-3, -2, -1, 1, 2, 3),
    plane_tick_unit = 1.0, plane_tick_label_gap = 0.24, plane_tick_size = 22,
    origin_label_offset = (-0.27, -0.28, 0),
    probe_start = (-0.72, 0.30),
    probe_positions = ((0.78, 0.51), (1.58, -0.29), (-1.36, -0.54), (-0.72, 0.30)),
    local_fraction = 0.58, local_cap = 0.74, label_offset = (0.19, 0.23, 0),
    radius_color = PALETTE['pale_yellow'], radius_angle = -0.32 * PI, radius_width = 1.85,
    radius_label_size = 30, radius_label_normal_gap = 0.13, radius_label_offset = (0, -0.12, 0), radius_line_z = 19,
    boundary_angle = 0.17 * PI, trial_radii = (0.53, 0.29, 0.14),
    escape_fraction = 0.82, escape_dot_radius = 0.05,
    small_disk_center = (0, -0.12, 0), small_disk_radius = 1.36,
    dimension_centers = ((-4.50, -0.12, 0), (0, -0.12, 0), (4.50, -0.12, 0)),
    dimension_label_y = -1.95, dimension_interval_half_length = 1.42,
    dimension_label_size = 44, dimension_label_color = PALETTE['pale_yellow'], dimension_label_rise = 0.32,
    formula_flash_color = YELLOW, formula_flash_width = 3.0, formula_flash_buff = 0.16, formula_flash_time_width = 0.75,
    formula_flash_glow_widths = (10.0, 6.0), formula_flash_glow_opacities = (0.10, 0.22),
    settle_probe = (-0.72, 0.30), settle_local_radius = 0.62,
)
SPHERE = dict(
    radius = 1.43, seed = 17, point_count = 6, interior_limit = 0.84,
    point_radius = 0.038, point_opacity = 0.67, latitude_count = 5,
    longitude_count = 7, samples = 97, tilt = 0.38, start_turn = 0.12,
    latitude_span = PI / 3,
    turn_angle = 1.25, wire_width = 1.10, wire_opacity = 0.25,
    outer_opacity = 0.56, fill_opacity = 0.04, depth_opacity = 0.30,
    gradient = (PALETTE['cyan'], PALETTE['green'], PALETTE['yellow']),
)
CARPET = dict(
    center = (0, -0.12, 0), side = 4.55, levels = 4,
    # 完全沿用preface.py的地毯配色：浅绿实体、蓝色外边、背景色孔洞
    scaffold_color = "#A3DCAF", frame_color = "#70CDE8",
    scaffold_fill = 1.0, frame_width = 1.2, frame_opacity = 1.0,
    hole_color = BG_COLOR, hole_overlap = 0.002,
    hole_fill = (1.0, 1.0, 1.0, 1.0),
    hole_width = (0.0, 0.0, 0.0, 0.0),
    hole_edge_opacity = (0.0, 0.0, 0.0, 0.0),
    ball_color = "#70CDE8", ball_fill_opacity = 0.085, probe_color = "#E9DD79", header_color = PALETTE['ink'],
    level_lag = 0.065, hole_reveal_scale = 0.88,
    # 两次各放大3倍，分别进入右上、左上保留块；保持分形的自相似比例
    zoom_factors = (3.0, 3.0), zoom_branches = ((1, 1), (-1, 1)), zoom_center = (0, -0.12, 0),
    detail_levels = 6, detail_pixel_fade = (1.8, 4.2), detail_zoom_reveal = (1.0, 1.80), detail_view_margin = 0.30,
    detail_overlap_ratio = 0.012,
    formula_size = 54, formula_position = (0, 3.0, 0), formula_group_scale = 0.60,
    formula_frame_color = "#70CDE8", formula_frame_width = 2.2,
    formula_frame_fill_color = "#0B2132", formula_frame_fill_opacity = 0.0,
    formula_frame_buff = 0.22, formula_frame_corner = 0.16,
    local_fraction = 0.60, local_positions = ((0, 0), (0.61, 0.43), (-0.58, -0.59), (0, 0)),
    probe_label_offset = (0.19, 0.22, 0), local_size = 29,
    recursion_mark_position = (2.79, -1.94, 0), recursion_mark_size = 34,
)
# 地毯放大时，屏幕四边渐暗；底边较宽，为后期字幕留出空间
# 中央保持preface原色；这是一张程序生成的透明度遮罩，不需要外部素材
EDGE_SHADE = dict(
    enabled = True, left_width = 1.80, right_width = 1.80, top_width = 1.85, bottom_width = 2.40,
    strength = 1.0, power = 0.80, pixel_width = 1024, pixel_height = 576, z_index = 30, overscan = 0.06,
)
ICON_PREIMAGE = dict(
    source_svg = (22.0, 21.0), target_svg = (12.5, 13.0),
    branch_x = 0.56, branch_y = 0.43, fold_width = 0.55,
    target_radius = 0.42, map_radius_cap = 1.50,
    boundary_samples = 97, boundary_dashes = 40, boundary_ratio = 0.60,
    region_fill = 0.12, region_width = 2.0, sample_radius = 0.038, sample_opacity = 0.64,
    rejected_opacity = 0.20,
    sample_seed = 20261015, sample_count = 28, accepted_sample_count = 12,
    sample_min_spacing = 0.09, sample_boundary_gap = 0.08, sample_max_attempts = 30000,
    probe_outcomes = (False, True, True, False, True, True),
    travel_handle = 1.50, travel_lift = 0.85, trail_time_width = 0.35,
    set_label_size = 40, target_label_offset = (0, 0.78, 0), target_label_size = 34,
    formula_position = (0, -2.42, 0), formula_size = 37,
)
PREIMAGE = dict(
    origin = (0, -1.77, 0), x_range = (-2.6, 2.6, 1), y_range = (0, 4.9, 1),
    x_length = 7.75, y_length = 4.00, x_ticks = tuple(range(-5, 6)), y_ticks = (1, 2, 3, 4, 5),
    graph_domain = (-2.14, 2.14), gradient = (PALETTE['cyan'], PALETTE['green'], PALETTE['yellow']),
    output_half_width = 0.17, origin_label_offset = (-0.27, -0.28, 0),
    range_low = 1.0, range_high = 4.0, graph_band_opacity = 0.060,
    output_band_opacity = 0.17, selected_curve_width = 5.2,
    f_position = (-4.03, 3.10, 0), v_position = (3.22, 3.10, 0),
    f_size = 39, v_size = 34, input_formula_position = (0.15, -2.48, 0),
    input_formula_size = 37, final_formula_outline_width = 8.0, tick_size = 26, tick_half_length = 0.062,
    x_tick_label_gap = 0.29, y_tick_label_gap = 0.36,
    sweep_margin = 0.022, sweep_line_width = 1.60, sweep_line_opacity = 0.40,
    input_probe = 1.50, probe_half_width = 0.18, probe_positions = (1.38, 1.65, 1.50),
    local_interval_height = 0.25, probe_dot_radius = 0.063,
    wire_opacity = 0.32, final_pulse_width = 5.6, final_pulse_time_width = 0.35,
)
FORMULAS = dict(
    interval = r"(a,b)", input_range = r"U", output_range = r"f(U)", mapping = r"f",
    input_focus = r"x_0", output_focus = r"f(x_0)", input_radius = r"\delta", output_radius = r"\varepsilon",
    point = r"p", dimension = (r"\mathbb R", r"\mathbb R^2", r"\mathbb R^3"),
    ball = r"B_{{r}}(p)=\{x:\ d(x,p)<{{r}}\}",
    openness = (r"\forall p\in U", r"\quad\exists {{r}}>0:", r"\quad B_{{r}}(p)\subset U"),
    local_radius = r"r",
    holes = r"{{U}}=\bigcup_{n\geq1}\ \bigcup_{Q\in\mathcal H_n}Q^{\circ}",
    preimage_domain = r"X", preimage_codomain = r"Y", preimage_target = r"V",
    preimage_set = (r"f^{-1}(V)", r"=\{x\in X:\ f(x)\in V\}"),
    recursion = r"\cdots", function = r"f(x)=x^2",
    criterion = (r"f\in C(X,Y)", r"\Leftrightarrow",
               r"\forall V\subseteq Y:\ V=V^{\circ}\ \Rightarrow",
               r"f^{-1}(V)=\left(f^{-1}(V)\right)^{\circ}"),
)

config.background_color = BG_COLOR
config.frame_width, config.frame_height = FRAME_WIDTH, FRAME_HEIGHT

if FRAME_RATE is not None:
    config.frame_rate = FRAME_RATE

# 轻量几何与分镜公共方法
def _v(value):

    return np.array(value, dtype = float)

def _tex(value, position = None, size = None, color = None, width = None):
    parts = value if isinstance(value, (tuple, list)) else (value,)
    mob = MathTex(*parts, font_size = STYLE['formula_size'] if size is None else size,
                  color = PALETTE['ink'] if color is None else color)
    limit = STYLE['formula_width'] if width is None else width

    if mob.width > limit:
        mob.scale_to_fit_width(limit)

    if position is not None:
        mob.move_to(_v(position))

    # 仅字形路径描边；所有无路径的公式分组保持完全透明
    mob.set_background_stroke(width = 0, opacity = 0)

    for glyph in mob.family_members_with_points():
        glyph.set_stroke(color = STYLE['label_outline_color'], width = STYLE['label_outline'],
                         opacity = 1, background = True, family = False)
        
    return mob.set_z_index(STYLE['formula_z'])

def _final_formula_outline(formula):
    # 先统一绘制全部字形的黑轮廓，再绘制全部彩色文字；没有矩形或背景填充
    # 这样相邻字形的描边不会遮断等价号、分数线等连接部位
    formula.set_stroke(width = 0, opacity = 0)
    formula.set_background_stroke(width = 0, opacity = 0)
    outline = VMobject(fill_opacity = 0, stroke_color = STYLE['label_outline_color'],
                       stroke_width = PREIMAGE['final_formula_outline_width'], stroke_opacity = 1)
    
    for glyph in formula.family_members_with_points():
        outline.append_vectorized_mobject(glyph)

    z = STYLE['foreground_formula_z']
    outline.set_z_index(z - 1)
    formula.set_z_index(z)

    return VGroup(outline, formula).set_z_index(z, family = False)

def _dot(position, color = None, radius = None):

    return Dot(_v(position), radius = STYLE['dot_radius'] if radius is None else radius,
               color = PALETTE['pale_yellow'] if color is None else color).set_z_index(STYLE['point_z'])

def _open_dot(position, color = None, radius = None):

    return Circle(radius = STYLE['open_radius'] if radius is None else radius,
                  stroke_color = PALETTE['ink'] if color is None else color,
                  stroke_width = STYLE['open_width'], fill_color = BG_COLOR,
                  fill_opacity = 1).move_to(_v(position)).set_z_index(STYLE['point_z'])

def _halo(position, color = None):

    return Circle(radius = STYLE['halo_radius'], stroke_width = 0,
                  fill_color = PALETTE['pale_yellow'] if color is None else color,
                  fill_opacity = STYLE['halo_opacity']).move_to(_v(position)).set_z_index(STYLE['halo_z'])

def _guide(start, end, color = None, opacity = None):

    return DashedLine(_v(start), _v(end), color = PALETTE['ink'] if color is None else color,
                      stroke_width = STYLE['guide_width'], dash_length = STYLE['dash_length'],
                      dashed_ratio = STYLE['boundary_ratio']).set_stroke(
                          opacity = STYLE['guide_opacity'] if opacity is None else opacity)

def _boundary(radius, center, color = None):
    circle = Circle(radius = radius, color = PALETTE['ink'] if color is None else color,
                    stroke_width = STYLE['boundary_width']).move_to(_v(center))
    
    return DashedVMobject(circle, num_dashes = STYLE['boundary_dashes'],
                         dashed_ratio = STYLE['boundary_ratio']).set_stroke(
                             opacity = STYLE['boundary_opacity']).set_fill(opacity = 0)

def _gradient_color(t, colors):
    t = np.clip(float(t), 0, 1) * (len(colors) - 1)
    i = min(int(t), len(colors) - 2)

    return interpolate_color(ManimColor(colors[i]), ManimColor(colors[i + 1]), t - i)

def _path(points, color, width):
    result = VMobject(stroke_color = color, stroke_width = width, fill_opacity = 0)
    result.set_points_smoothly(np.array(points))

    return result

def _range_icon(kind, center, color):
    icon = VMobjectFromSVGPath(SVGPath(BILIBILI_ICONS[kind]), stroke_color = color,
                              stroke_width = RANGES['contour_width'], fill_color = color,
                              fill_opacity = RANGES['contour_fill'])
    icon.svg_center = icon.get_center().copy()
    icon.svg_scale = RANGES['icon_width'] / icon.width

    # SVG的y轴向下，Manim的y轴向上。只翻转y轴并等比例缩放，不改变曲线形状
    icon.stretch(-1, dim = 1, about_point = ORIGIN)
    icon.scale(icon.svg_scale, about_point = ORIGIN)
    icon.move_to(_v(center))

    return icon

def _icon_point(icon, svg_point):
    x, y = svg_point
    relative = np.array([x - icon.svg_center[0], icon.svg_center[1] - y, 0])

    return icon.get_center() + icon.svg_scale * relative

def _contour_polygons(icon):
    polygons = []

    for subpath in icon.get_subpaths():
        samples = []

        for controls in subpath.reshape((-1, 4, 3)):

            for t in np.linspace(0, 1, RANGES['contour_samples_per_curve'], endpoint = False):
                point = (1 - t) ** 3 * controls[0] + 3 * (1 - t) ** 2 * t * controls[1]
                point += 3 * (1 - t) * t ** 2 * controls[2] + t ** 3 * controls[3]
                samples.append(point[:2])

        polygons.append(np.array(samples))

    return polygons

def _inside_polygon(point, polygon):
    x, y = point[:2]
    inside = False

    for a, b in zip(polygon, np.roll(polygon, -1, axis = 0)):

        if (a[1] > y) != (b[1] > y):
            intersection = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])

            if x < intersection:
                inside = not inside

    return inside

def _check_icon_ball(icon, center, radius):
    polygons = _contour_polygons(icon)

    if not any(_inside_polygon(center, polygon) for polygon in polygons):
        raise ValueError('邻域的圆心须位于图标集合内部。')
    
    for polygon in polygons:

        for start, end in zip(polygon, np.roll(polygon, -1, axis = 0)):
            direction = end - start
            length_squared = np.dot(direction, direction)

            if length_squared <= STYLE['numeric_tolerance']:
                continue

            t = np.clip(np.dot(center[:2] - start, direction) / length_squared, 0, 1)
            distance = np.linalg.norm(center[:2] - start - t * direction)

            if distance <= radius + RANGES['containment_margin']:
                raise ValueError('圆半径过大，会碰到点赞或收藏集合的轮廓。')
            
    for angle in np.linspace(0, TAU, RANGES['containment_circle_samples'], endpoint = False):
        point = center + radius * np.array([math.cos(angle), math.sin(angle), 0])

        if not any(_inside_polygon(point, polygon) for polygon in polygons):

            raise ValueError('邻域圆必须完全留在图标集合内部。')

def _range_ball(center, radius, color):
    # 两个邻域共用同一线宽、虚线长度和间隔；仅半径与配色由各自参数决定
    p = RANGES
    fill = Circle(radius = radius, stroke_width = 0, fill_color = color,
                  fill_opacity = p['circle_fill']).move_to(center)
    period = p['circle_dash_length'] + p['circle_dash_gap']
    count = max(3, round(TAU * radius / period))
    edge = DashedVMobject(Circle(radius = radius, stroke_color = color,
                                 stroke_width = p['circle_width']).move_to(center),
                          num_dashes = count, dashed_ratio = p['circle_dash_length'] / period)
    edge.set_stroke(color = color, width = p['circle_width']).set_fill(opacity = 0)

    return VGroup(fill, edge)

def _range_neighborhoods(input_region, output_region):
    p = RANGES
    x0 = _icon_point(input_region, p['x0_svg'])
    fx0 = _icon_point(output_region, p['fx0_svg'])
    _check_icon_ball(input_region, x0, p['delta_radius'])
    _check_icon_ball(output_region, fx0, p['epsilon_radius'])

    if np.linalg.norm(x0 - input_region.get_center()) <= STYLE['numeric_tolerance']:
        raise ValueError('x0不能恰好位于点赞集合的整体中心。')
    
    if np.linalg.norm(fx0 - output_region.get_center()) <= STYLE['numeric_tolerance']:
        raise ValueError('f(x0)不能恰好位于收藏集合的整体中心。')
    
    delta = _range_ball(x0, p['delta_radius'], PALETTE['green'])
    epsilon = _range_ball(fx0, p['epsilon_radius'], PALETTE['blue'])
    centers = VGroup(_dot(x0), _dot(fx0))
    halos = VGroup(_halo(x0), _halo(fx0))
    point_labels = VGroup()

    for point, formula in zip(centers, (FORMULAS['input_focus'], FORMULAS['output_focus'])):
        label = _tex(formula, size = p['point_label_size'])
        label.next_to(point, _v(p['point_label_direction']), buff = p['point_label_gap'])
        label.set_background_stroke(color = p['point_label_outline_color'],
                                    width = p['point_label_outline_width'], opacity = 1)
        point_labels.add(label)

    radius_lines, radius_labels = VGroup(), VGroup()
    entries = ((x0, p['delta_radius'], p['delta_radius_angle'], p['delta_label_offset'],
                FORMULAS['input_radius'], PALETTE['green']),
               (fx0, p['epsilon_radius'], p['epsilon_radius_angle'], p['epsilon_label_offset'],
                FORMULAS['output_radius'], PALETTE['blue']))
    
    for center, radius, angle, offset, value, color in entries:
        end = center + radius * np.array([math.cos(angle), math.sin(angle), 0])
        radius_lines.add(Line(center, end, color = color, stroke_width = p['radius_width']))
        radius_labels.add(_tex(value, end + _v(offset), p['radius_label_size'], color))

    circles = VGroup(delta, epsilon)

    return dict(x0 = x0, fx0 = fx0, circles = circles, centers = centers, halos = halos,
                point_labels = point_labels, radius_lines = radius_lines, radius_labels = radius_labels,
                all = VGroup(circles, halos, centers, point_labels, radius_lines, radius_labels))

def _local_interval(x, radius, y, height = None):
    radius = max(radius, STYLE['minimum_draw_radius'])
    fill = Rectangle(width = 2 * radius, height = INTERVAL['local_height'] if height is None else height, stroke_width = 0,
                     fill_color = PALETTE['mint'], fill_opacity = STYLE['local_opacity']).move_to([x, y, 0])
    line = Line([x - radius, y, 0], [x + radius, y, 0], color = PALETTE['mint'],
                stroke_width = STYLE['local_width'])
    ends = VGroup(*[_open_dot([x + sign * radius, y, 0], PALETTE['mint'],
                              INTERVAL['local_endpoint_radius']) for sign in (-1, 1)])
    
    return VGroup(fill, line, ends).set_z_index(STYLE['local_z'])

def _horizontal_ticks(center, values, unit, label_gap, size):
    ticks = VGroup()

    for value in values:
        position = _v(center) + value * unit * RIGHT
        ticks.add(Line(position + STYLE['tick_half_length'] * UP,
                       position + STYLE['tick_half_length'] * DOWN,
                       color = PALETTE['axis'], stroke_width = STYLE['axis_width']))
        ticks.add(_tex(_number_tex(value), position + label_gap * DOWN, size))

    return ticks

def _interval_stage():
    p = INTERVAL
    axis = Line([-p['axis_half_length'], p['axis_y'], 0],
                [p['axis_half_length'], p['axis_y'], 0],
                color = PALETTE['axis'], stroke_width = STYLE['axis_width'])
    segment = Line([p['left'], p['axis_y'], 0], [p['right'], p['axis_y'], 0],
                   color = PALETTE['cyan'], stroke_width = STYLE['interval_width'])
    ends = VGroup(*[_open_dot([x, p['axis_y'], 0], PALETTE['cyan']) for x in (p['left'], p['right'])])
    labels = VGroup(*[_tex(label, _v([x, p['axis_y'], 0]) + _v(p['endpoint_label_offset']),
                          STYLE['label_size']) for x, label in ((p['left'], 'a'), (p['right'], 'b'))])
    header = _tex(FORMULAS['interval'], p['label_position'], color = PALETTE['cyan'])
    ticks = _horizontal_ticks((0, p['axis_y'], 0), p['ticks'], p['axis_unit'],
                              p['tick_label_gap'], STYLE['tick_size'])
    
    return dict(axis = axis, ticks = ticks, segment = segment, ends = ends, labels = labels, header = header,
                all = VGroup(axis, ticks, segment, ends, labels, header))

def _disk_geometry(center = None, radius = None):
    center = DISK['center'] if center is None else center
    radius = DISK['radius'] if radius is None else radius
    fill = Circle(radius = radius, stroke_width = 0, fill_color = PALETTE['cyan'],
                  fill_opacity = STYLE['fill_opacity']).move_to(_v(center))
    edge = _boundary(radius, center)

    return VGroup(fill, edge)

def _openness_header():
    header = _tex(FORMULAS['openness'], STYLE['header'])
    ball_part = False

    for part in header:

        if r'\forall' in part.tex_string:
            part.set_color(PALETTE['cyan'])
        if 'B_' in part.tex_string:
            ball_part = True
        if ball_part:
            part.set_color(PALETTE['mint'])

    # 双花括号只分离目标r字形，不拆开包含字母r的LaTeX命令
    header.set_color_by_tex('r', DISK['radius_color'], substring = False)

    return header

def _ball_header():
    header = _tex(FORMULAS['ball'], STYLE['header'])
    header.set_color_by_tex('r', DISK['radius_color'], substring = False)

    return header

def _radius_end(center, radius):
    angle = DISK['radius_angle']

    return _v(center) + radius * np.array([math.cos(angle), math.sin(angle), 0])

def _radius_label_position(center, radius):
    angle = DISK['radius_angle']
    normal = np.array([-math.sin(angle), math.cos(angle), 0])

    return (_v(center) + _radius_end(center, radius)) / 2 + DISK['radius_label_normal_gap'] * normal + _v(DISK['radius_label_offset'])

def _radius_marker(center, radius):
    line = Line(_v(center), _radius_end(center, radius), color = DISK['radius_color'],
                stroke_width = DISK['radius_width']).set_z_index(DISK['radius_line_z'])
    label = _tex(FORMULAS['local_radius'], _radius_label_position(center, radius),
                 DISK['radius_label_size'], DISK['radius_color'])
    
    return VGroup(line, label)

def _disk_stage():
    geom = _disk_geometry()
    point_pos = _v(DISK['center']) + _v((*DISK['settle_probe'], 0))
    local = Circle(radius = DISK['settle_local_radius'], color = PALETTE['mint'],
                   stroke_width = STYLE['local_width'], fill_color = PALETTE['mint'],
                   fill_opacity = STYLE['local_opacity']).move_to(point_pos)
    point = _dot(point_pos)
    halo = _halo(point_pos)
    label = _tex(FORMULAS['point'], point_pos + _v(DISK['label_offset']), STYLE['label_size'])
    radius_marker = _radius_marker(point_pos, DISK['settle_local_radius'])
    header = _openness_header()

    return dict(geometry = geom, local = local, point = point, halo = halo, label = label,
                radius_marker = radius_marker, header = header,
                all = VGroup(geom, local, halo, radius_marker, point, label, header))

def _sphere_cloud():
    rng = np.random.default_rng(SPHERE['seed'])
    directions = rng.normal(size = (SPHERE['point_count'], 3))
    directions /= np.linalg.norm(directions, axis = 1)[:, None]
    radial = SPHERE['interior_limit'] * rng.random(SPHERE['point_count']) ** (1 / 3)

    return directions * radial[:, None]

def _project3(points, angle):
    ct, st = math.cos(angle), math.sin(angle)
    tilt = SPHERE['tilt']
    cx, sx = math.cos(tilt), math.sin(tilt)
    rotation = np.array([[ct, 0, st], [sx * st, cx, -sx * ct], [-cx * st, sx, cx * ct]])
    rotated = np.array(points) @ rotation.T

    return np.column_stack((rotated[:, 0], rotated[:, 1], np.zeros(len(rotated)))), rotated[:, 2]

def _sphere_view(center, angle, cloud):
    p = SPHERE
    center, radius = _v(center), p['radius']
    fill = Circle(radius = radius, stroke_width = 0, fill_color = PALETTE['cyan'],
                  fill_opacity = p['fill_opacity']).move_to(center)
    edge = _boundary(radius, center).set_stroke(opacity = p['outer_opacity'])
    wire = VGroup()
    t = np.linspace(0, TAU, p['samples'])

    for latitude in np.linspace(-p['latitude_span'], p['latitude_span'], p['latitude_count']):
        raw = np.column_stack((math.cos(latitude) * np.cos(t),
                               np.full_like(t, math.sin(latitude)), math.cos(latitude) * np.sin(t)))
        projected, _ = _project3(raw, angle)
        wire.add(_path(center + radius * projected, PALETTE['cyan'], p['wire_width']))

    for longitude in np.linspace(0, PI, p['longitude_count'], endpoint = False):
        raw = np.column_stack((math.cos(longitude) * np.cos(t), np.sin(t),
                               math.sin(longitude) * np.cos(t)))
        projected, _ = _project3(raw, angle)
        wire.add(_path(center + radius * projected, PALETTE['cyan'], p['wire_width']))

    wire.set_stroke(opacity = p['wire_opacity'])
    wire.set_fill(opacity = 0)
    projected, depth = _project3(cloud, angle)
    points = VGroup()

    for q, d in zip(projected, depth):
        color = _gradient_color((d / p['interior_limit'] + 1) / 2, p['gradient'])
        opacity = p['point_opacity'] + p['depth_opacity'] * d / p['interior_limit']
        points.add(_dot(center + radius * q, color, p['point_radius']).set_opacity(opacity))

    # 球心和二维圆心共用STYLE中的点半径，独立于装饰散点的大小
    return VGroup(fill, wire, edge, points, _dot(center))

def _carpet_cells():
    # 第n层只在上一层保留的八个方块中继续挖孔，边框始终保留
    cells = [(_v(CARPET['center']), CARPET['side'])]
    levels = []

    for _ in range(CARPET['levels']):
        holes, remaining = [], []

        for center, side in cells:
            child = side / 3
            holes.append((center.copy(), child))

            for i in (-1, 0, 1):

                for j in (-1, 0, 1):

                    if i != 0 or j != 0:
                        remaining.append((center + np.array([i * child, j * child, 0]), child))

        levels.append(holes)
        cells = remaining

    return levels

def _carpet_hole_overlap(side):
    # 极细孔按比例限制扩边，避免放大后细孔侵入相邻的绿色保留块
    return min(CARPET['hole_overlap'], side * CARPET['detail_overlap_ratio'])

def _carpet_ease(t):
    # 起止的速度与加速度都为零，镜头和细孔渐显采用同一条平滑曲线
    t = float(np.clip(t, 0, 1))

    return t ** 3 * (10 - 15 * t + 6 * t ** 2)

def _carpet_formula():
    p = CARPET
    formula = _tex(FORMULAS['holes'], p['formula_position'], p['formula_size'], p['header_color'])
    formula.set_color_by_tex('U', p['frame_color'], substring = False)
    formula.set_background_stroke(color = STYLE['label_outline_color'], width = STYLE['label_outline'], opacity = 1)
    formula.set_z_index(STYLE['foreground_formula_z'])
    frame = RoundedRectangle(
        width = formula.width + 2 * p['formula_frame_buff'],
        height = formula.height + 2 * p['formula_frame_buff'],
        corner_radius = p['formula_frame_corner'],
        stroke_color = p['formula_frame_color'], stroke_width = p['formula_frame_width'],
        fill_color = p['formula_frame_fill_color'], fill_opacity = p['formula_frame_fill_opacity'],
    ).move_to(formula).set_z_index(STYLE['formula_backplate_z'])

    return VGroup(frame, formula).scale(p['formula_group_scale'], about_point = _v(p['formula_position']))

def _carpet_zoom_targets():
    focus, side, scale = _v(CARPET['center']), CARPET['side'], 1.0
    targets = []

    for factor, branch in zip(CARPET['zoom_factors'], CARPET['zoom_branches']):
        side /= 3
        focus = focus + side * _v((*branch, 0))
        scale *= factor
        targets.append((scale, focus.copy()))

    # 最终聚焦保留块的中央三分之一，就是用于演示开球的空洞
    return targets, side / 3

def _carpet_visible_holes(scale, focus):
    p = CARPET
    destination = _v(p['zoom_center'])
    pixel_unit = float(config.pixel_width) / FRAME_WIDTH
    low, high = p['detail_pixel_fade']
    zoom_low, zoom_high = p['detail_zoom_reveal']
    detail_visibility = _carpet_ease((scale - zoom_low) / (zoom_high - zoom_low))
    margin = p['detail_view_margin']
    lower = np.array([-FRAME_WIDTH / 2 - margin, -FRAME_HEIGHT / 2 - margin])
    upper = -lower
    levels = [[] for _ in range(p['detail_levels'])]

    def visit(center, side, depth):
        projected = destination + scale * (center - focus)
        half = scale * side / 2

        if np.any(projected[:2] + half < lower) or np.any(projected[:2] - half > upper):
            return
        
        child = side / 3
        pixel_side = child * scale * pixel_unit

        if depth > p['levels'] and (pixel_side <= low or detail_visibility == 0):
            return
        
        hole_half = scale * (child + _carpet_hole_overlap(child)) / 2

        if not (np.any(projected[:2] + hole_half < lower) or np.any(projected[:2] - hole_half > upper)):
            levels[depth - 1].append((projected, scale * (child + _carpet_hole_overlap(child))))

        if depth < p['detail_levels']:
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i or j:
                        visit(center + child * np.array([i, j, 0]), child, depth + 1)

    visit(_v(p['center']), p['side'], 1)
    opacities = []

    for depth in range(1, p['detail_levels'] + 1):
        pixel_side = p['side'] * scale * pixel_unit / 3 ** depth
        opacity = 1.0 if depth <= p['levels'] else detail_visibility * _carpet_ease((pixel_side - low) / (high - low))
        opacities.append(opacity)

    return levels, opacities

def _carpet_zoom_geometry(scale, focus):
    # 每层合并成一条包含多个子路径的矢量图；仅递归生成画面内的细孔
    p = CARPET
    scaffold = Square(side_length = 1, stroke_color = p['frame_color'],
                      stroke_width = p['frame_width'], stroke_opacity = p['frame_opacity'],
                      fill_color = p['scaffold_color'], fill_opacity = p['scaffold_fill'])
    holes = VGroup(*[VMobject(stroke_width = 0, fill_color = p['hole_color'], fill_opacity = 0)
                     for _ in range(p['detail_levels'])])
    geometry = VGroup(scaffold, holes)
    geometry.unit_square_points = scaffold.get_points().copy()

    return _update_carpet_zoom_geometry(geometry, scale, focus)

def _update_carpet_zoom_geometry(geometry, scale, focus):
    # 直接更新固定数量的图层，避免become给成千上万个孔洞逐一对齐曲线
    p = CARPET
    template = geometry.unit_square_points
    body_center = _v(p['zoom_center']) + scale * (_v(p['center']) - focus)
    geometry[0].set_points(template * (p['side'] * scale) + body_center)
    levels, opacities = _carpet_visible_holes(scale, focus)

    for shape, cells, opacity in zip(geometry[1], levels, opacities):
        if cells:
            centers = np.array([center for center, _ in cells])
            sides = np.array([side for _, side in cells])
            shape.set_points((template[None, :, :] * sides[:, None, None] + centers[:, None, :]).reshape((-1, 3)))
        else:
            shape.set_points(np.empty((0, 3)))
        shape.set_fill(opacity = opacity)

    return geometry

def _carpet_stage():
    p = CARPET
    scaffold = Square(side_length = p['side'], stroke_color = p['frame_color'],
                      stroke_width = p['frame_width'], stroke_opacity = p['frame_opacity'],
                      fill_color = p['scaffold_color'], fill_opacity = p['scaffold_fill']).move_to(_v(p['center']))
    levels, data = VGroup(), _carpet_cells()

    for level, cells in enumerate(data):
        group = VGroup()

        for center, side in cells:
            hole = Square(side_length = side + _carpet_hole_overlap(side), stroke_color = p['frame_color'],
                          stroke_width = p['hole_width'][level],
                          stroke_opacity = p['hole_edge_opacity'][level],
                          fill_color = p['hole_color'], fill_opacity = p['hole_fill'][level]).move_to(center)
            group.add(hole)

        levels.add(group)

    header = _carpet_formula()
    recursion = _tex(FORMULAS['recursion'], p['recursion_mark_position'],
                     p['recursion_mark_size'], PALETTE['muted'])
    geometry = VGroup(scaffold, levels)

    return dict(scaffold = scaffold, levels = levels, data = data, geometry = geometry,
                header = header, recursion = recursion, all = VGroup(geometry, header, recursion))

def _screen_edge_mask():
    p = EDGE_SHADE
    overscan = p['overscan']
    x = np.linspace(-FRAME_WIDTH / 2 - overscan, FRAME_WIDTH / 2 + overscan, p['pixel_width'])[None, :]
    y = np.linspace(FRAME_HEIGHT / 2 + overscan, -FRAME_HEIGHT / 2 - overscan, p['pixel_height'])[:, None]

    def falloff(distance, width):
        t = np.clip(1 - distance / width, 0, 1)

        return (t * t * (3 - 2 * t)) ** p['power']

    left = falloff(x + FRAME_WIDTH / 2, p['left_width'])
    right = falloff(FRAME_WIDTH / 2 - x, p['right_width'])
    top = falloff(FRAME_HEIGHT / 2 - y, p['top_width'])
    bottom = falloff(y + FRAME_HEIGHT / 2, p['bottom_width'])

    # 用透明度合成四边，角落也平滑过渡，不留下亮角或硬矩形
    alpha = p['strength'] * (1 - (1 - left) * (1 - right) * (1 - top) * (1 - bottom))
    rgba = np.empty((p['pixel_height'], p['pixel_width'], 4), dtype = np.uint8)
    rgba[:, :, :3] = np.array([int(BG_COLOR[i:i + 2], 16) for i in (1, 3, 5)], dtype = np.uint8)
    rgba[:, :, 3] = np.round(255 * np.clip(alpha, 0, 1)).astype(np.uint8)
    mask = ImageMobject(rgba)
    mask.stretch_to_fit_width(FRAME_WIDTH + 2 * overscan).stretch_to_fit_height(FRAME_HEIGHT + 2 * overscan)

    return mask.move_to(ORIGIN).set_z_index(p['z_index'])

def _number_tex(value):
    rounded = round(value)

    if abs(value - rounded) < STYLE['numeric_tolerance']:
        return str(rounded)
    
    return f"{value:g}"

def _root_tex(value):
    root = math.sqrt(value)
    rounded = round(root)

    if abs(root - rounded) < STYLE['numeric_tolerance']:
        return str(rounded)
    
    return r"\sqrt{" + _number_tex(value) + "}"

def _preimage_formula():
    a, b = (_root_tex(PREIMAGE[key]) for key in ('range_low', 'range_high'))

    return r"f^{-1}(V)=(-" + b + ",-" + a + r")\cup(" + a + "," + b + ")"

def _icon_preimage_stage():
    p = ICON_PREIMAGE
    source = _range_icon('like', RANGES['input_center'], PALETTE['green'])
    target = _range_icon('favorite', RANGES['output_center'], PALETTE['blue'])
    source_center = _icon_point(source, p['source_svg'])
    target_center = _icon_point(target, p['target_svg'])
    _check_icon_ball(target, target_center, p['target_radius'] * p['map_radius_cap'])
    source_polygons = _contour_polygons(source)

    def source_point(sign, unit):
        u, v = unit

        return source_center + np.array([sign * p['branch_x'] * math.sqrt(1 + p['fold_width'] * u),
                                         p['branch_y'] * v, 0])

    # 连续折叠映射：开圆盘的完整原像是两块开区域，所有采样也由同一映射确定
    # 径向压缩保证整个点赞集合的输出都位于收藏轮廓内，且不改变是否落入V的判定
    def map_point(point):
        local = point - source_center
        raw = np.array([((local[0] / p['branch_x']) ** 2 - 1) / p['fold_width'],
                        local[1] / p['branch_y'], 0])
        norm = np.linalg.norm(raw)

        if norm <= STYLE['numeric_tolerance']:
            return target_center.copy(), True
        
        radius = p['target_radius'] * p['map_radius_cap'] * math.tanh(norm * math.atanh(1 / p['map_radius_cap']))

        return target_center + radius * raw / norm, norm < 1

    regions = VGroup()

    for sign in (-1, 1):
        boundary = [source_point(sign, (math.cos(t), math.sin(t)))
                    for t in np.linspace(0, TAU, p['boundary_samples'])]
        
        if not all(any(_inside_polygon(q, polygon) for polygon in source_polygons) for q in boundary):
            raise ValueError('原像的两块开区域必须完整位于点赞轮廓内。')
        
        shape = VMobject(stroke_width = 0, fill_color = PALETTE['green'], fill_opacity = p['region_fill'])
        shape.set_points_smoothly(boundary)
        outline = shape.copy().set_fill(opacity = 0).set_stroke(PALETTE['green'], width = p['region_width'])
        edge = DashedVMobject(outline, num_dashes = p['boundary_dashes'], dashed_ratio = p['boundary_ratio'])
        regions.add(VGroup(shape, edge))

    # 在整个点赞轮廓内随机拒绝采样，各点独立生成，不镜像复制或按行排列
    rng = np.random.default_rng(p['sample_seed'])
    samples, images, accepted, positions = VGroup(), [], [], []
    wanted = {True: p['accepted_sample_count'], False: p['sample_count'] - p['accepted_sample_count']}
    counts = {True: 0, False: 0}

    for _ in range(p['sample_max_attempts']):
        if len(positions) == p['sample_count']:
            break
        position = np.array([rng.uniform(source.get_left()[0], source.get_right()[0]),
                             rng.uniform(source.get_bottom()[1], source.get_top()[1]), 0])
        if not any(_inside_polygon(position, polygon) for polygon in source_polygons):
            continue
        if any(np.linalg.norm(position - other) < p['sample_min_spacing'] for other in positions):
            continue
        local = position - source_center
        raw_norm = math.hypot(((local[0] / p['branch_x']) ** 2 - 1) / p['fold_width'], local[1] / p['branch_y'])
        if abs(raw_norm - 1) < p['sample_boundary_gap']:
            continue
        image_position, is_inside = map_point(position)
        if counts[is_inside] == wanted[is_inside]:
            continue
        positions.append(position)
        counts[is_inside] += 1
        samples.add(_dot(position, PALETTE['muted'], p['sample_radius']).set_opacity(p['sample_opacity']))
        images.append(image_position)
        accepted.append(is_inside)

    if len(positions) != p['sample_count']:
        raise ValueError('随机散点采样不足，请降低点数或最小间距。')
    
    candidates = {flag: list(rng.permutation([i for i, result in enumerate(accepted) if result == flag]))
                  for flag in (False, True)}
    probe_indices = [candidates[flag].pop() for flag in p['probe_outcomes']]
    source_label = _tex(FORMULAS['preimage_domain'], RANGES['input_label'], p['set_label_size'], PALETTE['green'])
    target_label = _tex(FORMULAS['preimage_codomain'], RANGES['output_label'], p['set_label_size'], PALETTE['blue'])
    target_region = _range_ball(target_center, p['target_radius'], PALETTE['blue'])
    target_name = _tex(FORMULAS['preimage_target'], target_center + _v(p['target_label_offset']),
                       p['target_label_size'], PALETTE['blue'])
    arrow = Arrow(_v(RANGES['arrow_start']), _v(RANGES['arrow_end']), buff = 0,
                  color = PALETTE['axis'], stroke_width = RANGES['arrow_width'], tip_length = RANGES['arrow_tip'])
    arrow_label = _tex(FORMULAS['mapping'], RANGES['f_position'], STYLE['label_size'])
    definition = _tex(FORMULAS['preimage_set'], p['formula_position'], p['formula_size'])
    definition[0].set_color(PALETTE['green'])
    definition.set_z_index(STYLE['foreground_formula_z'])

    return dict(source = source, target = target, source_label = source_label, target_label = target_label,
                target_region = target_region, target_name = target_name, regions = regions, samples = samples,
                images = images, accepted = accepted, probe_indices = probe_indices,
                arrow = arrow, arrow_label = arrow_label, definition = definition)

def _graph_curve(axes, start, stop, colors, width):
    segments = VGroup()
    bounds = np.linspace(start, stop, STYLE['curve_segments'] + 1)

    for i, (a, b) in enumerate(zip(bounds[:-1], bounds[1:])):
        samples = np.linspace(a, b, STYLE['samples_per_segment'])
        points = [axes.c2p(x, x * x) for x in samples]
        segments.add(_path(points, _gradient_color(i / (len(bounds) - 2), colors), width))

    return segments

def _preimage_stage():
    p = PREIMAGE
    axes = Axes(x_range = p['x_range'], y_range = p['y_range'], x_length = p['x_length'],
                y_length = p['y_length'], tips = False,
                axis_config = dict(color = PALETTE['axis'], stroke_width = STYLE['axis_width'], include_ticks = False))
    axes.shift(_v(p['origin']) - axes.c2p(0, 0))

    # 坐标变换仍由原Axes计算；把显示用的两根白色轴延伸至画面之外
    axes.x_axis.set_stroke(opacity = 0)
    axes.y_axis.set_stroke(opacity = 0)
    half_x = FRAME_WIDTH / 2 + STYLE['axis_overhang']
    half_y = FRAME_HEIGHT / 2 + STYLE['axis_overhang']
    vertical_axis = Line([p['origin'][0], -half_y, 0], [p['origin'][0], half_y, 0],
                         color = PALETTE['axis'], stroke_width = STYLE['axis_width'])
    axes.add(Line([-half_x, p['origin'][1], 0], [half_x, p['origin'][1], 0],
                  color = PALETTE['axis'], stroke_width = STYLE['axis_width']), vertical_axis)
    ticks = VGroup()

    for x in p['x_ticks']:
        if x == 0:
            continue
        point = axes.c2p(x, 0)
        ticks.add(Line(point + p['tick_half_length'] * UP, point + p['tick_half_length'] * DOWN,
                       color = PALETTE['axis'], stroke_width = STYLE['axis_width']))
        ticks.add(_tex(_number_tex(x), point + p['x_tick_label_gap'] * DOWN, p['tick_size']))
    ticks.add(_tex('0', _v(p['origin']) + _v(p['origin_label_offset']), p['tick_size']))

    for y in p['y_ticks']:
        point = axes.c2p(0, y)
        ticks.add(Line(point + p['tick_half_length'] * LEFT, point + p['tick_half_length'] * RIGHT,
                       color = PALETTE['axis'], stroke_width = STYLE['axis_width']))
        ticks.add(_tex(_number_tex(y), point + p['y_tick_label_gap'] * LEFT, p['tick_size']))

    graph = _graph_curve(axes, *p['graph_domain'], p['gradient'], STYLE['curve_width'])
    low, high = p['range_low'], p['range_high']

    # 中间这一根白色纵轴同时承载蓝色输出区间，不再重复创建右侧数轴
    output_position = lambda y: axes.c2p(0, y)
    height = output_position(high)[1] - output_position(low)[1]
    output_fill = Rectangle(width = 2 * p['output_half_width'], height = height, stroke_width = 0,
                            fill_color = PALETTE['blue'], fill_opacity = p['output_band_opacity'])
    output_fill.move_to((output_position(low) + output_position(high)) / 2)
    output_line = Line(output_position(low), output_position(high), color = PALETTE['blue'],
                       stroke_width = STYLE['interval_width'])
    output_ends = VGroup(*[_open_dot(output_position(y), PALETTE['blue']) for y in (low, high)])
    x_left, x_right = p['x_range'][0], p['x_range'][1]
    graph_fill = Rectangle(width = axes.c2p(x_right, 0)[0] - axes.c2p(x_left, 0)[0],
                           height = height, stroke_width = 0, fill_color = PALETTE['blue'],
                           fill_opacity = p['graph_band_opacity'])
    graph_fill.move_to((axes.c2p(x_left, low) + axes.c2p(x_right, high)) / 2).set_z_index(STYLE['band_z'])
    band_edges = VGroup(*[_guide(axes.c2p(x_left, y), axes.c2p(x_right, y), PALETTE['blue'])
                          for y in (low, high)])
    f_header = _tex(FORMULAS['function'], p['f_position'], p['f_size'])
    v_header = _tex("V=(" + _number_tex(low) + "," + _number_tex(high) + ")",
                    p['v_position'], p['v_size'], PALETTE['blue'])
    a, b = math.sqrt(low), math.sqrt(high)
    intervals = VGroup(*[Line(axes.c2p(left, 0), axes.c2p(right, 0), color = PALETTE['green'],
                              stroke_width = STYLE['interval_width']) for left, right in ((-b, -a), (a, b))])
    input_ends = VGroup(*[_open_dot(axes.c2p(x, 0), PALETTE['green']) for x in (-b, -a, a, b)])
    selected = VGroup(*[_graph_curve(axes, left, right, (PALETTE['green'], PALETTE['mint']),
                                    p['selected_curve_width']) for left, right in ((-b, -a), (a, b))])
    selected_ends = VGroup(*[_open_dot(axes.c2p(x, x * x), PALETTE['green']) for x in (-b, -a, a, b)])
    input_formula = _final_formula_outline(_tex(_preimage_formula(), p['input_formula_position'],
                                                p['input_formula_size'], PALETTE['green']))
    
    return dict(axes = axes, vertical_axis = vertical_axis, ticks = ticks, graph = graph,
                output_fill = output_fill, output_line = output_line, output_ends = output_ends,
                output_position = output_position, graph_fill = graph_fill, band_edges = band_edges,
                f_header = f_header, v_header = v_header, intervals = intervals, input_ends = input_ends,
                selected = selected, selected_ends = selected_ends, input_formula = input_formula)

def validate_parameters():
    if TIME_SCALE <= 0:
        raise ValueError('TIME_SCALE 必须为正数。')
    if not INTERVAL['left'] < INTERVAL['right']:
        raise ValueError('开区间的左端点必须小于右端点。')
    if RANGES['icon_width'] <= 0 or RANGES['delta_radius'] <= 0 or RANGES['epsilon_radius'] <= 0:
        raise ValueError('图标宽度和两个邻域半径必须为正数。')
    if RANGES['circle_dash_length'] <= 0 or RANGES['circle_dash_gap'] <= 0:
        raise ValueError('两个圆共用的虚线长度与间隔必须为正数。')
    if len(RANGES['input_fractions']) != len(RANGES['output_fractions']):
        raise ValueError('输入和输出采样点须一一对应。')
    if any(np.linalg.norm(point) >= 1 for key in ('input_fractions', 'output_fractions') for point in RANGES[key]):
        raise ValueError('映射采样点须严格位于δ圆和ε圆内部。')
    if not 0 < DISK['local_fraction'] < 1 or not 0 < INTERVAL['local_fraction'] < 1:
        raise ValueError('局部邻域的安全比例必须严格介于0和1之间。')
    for point in (DISK['probe_start'], *DISK['probe_positions']):
        if np.linalg.norm(point) >= DISK['radius']:
            raise ValueError('圆盘内演示点必须严格位于内部。')
    if not 1 <= CARPET['levels'] <= len(CARPET['hole_fill']):
        raise ValueError('地毯层数与逐层样式数组不匹配。')
    if not len(CARPET['zoom_factors']) == len(CARPET['zoom_branches']) == len(TIMING['carpet_zoom']) == 2:
        raise ValueError('第三镜需配置两次放大的倍率、目标分支与时间。')
    if any(factor <= 1 for factor in CARPET['zoom_factors']):
        raise ValueError('两次放大的倍率均须大于1。')
    if any(branch == (0, 0) or any(value not in (-1, 0, 1) for value in branch) for branch in CARPET['zoom_branches']):
        raise ValueError('放大目标须位于周围八个绿色保留块中。')
    if CARPET['detail_levels'] < CARPET['levels'] or not 0 < CARPET['detail_pixel_fade'][0] < CARPET['detail_pixel_fade'][1]:
        raise ValueError('细孔层数和渐显像素阈值配置不正确。')
    if not 1 <= CARPET['detail_zoom_reveal'][0] < CARPET['detail_zoom_reveal'][1]:
        raise ValueError('细孔随放大渐显的倍率阈值配置不正确。')
    if CARPET['formula_group_scale'] <= 0:
        raise ValueError('公式和圆角框的整体缩放倍率须为正数。')
    if not 0 < CARPET['local_fraction'] < 1 or any(max(abs(x), abs(y)) >= 1 for x, y in CARPET['local_positions']):
        raise ValueError('孔洞内的点与开球必须严格位于孔洞内部。')
    if not 0 <= EDGE_SHADE['strength'] <= 1 or EDGE_SHADE['power'] <= 0:
        raise ValueError('四周渐暗的强度须介于0和1之间，曲线参数须为正数。')
    if any(EDGE_SHADE[key] <= 0 for key in ('left_width', 'right_width', 'top_width', 'bottom_width')):
        raise ValueError('四边的渐暗宽度须为正数。')
    if not 0 < PREIMAGE['range_low'] < PREIMAGE['range_high'] < PREIMAGE['y_range'][1]:
        raise ValueError('x²演示的输出区间须严格在正半轴可视范围内。')
    
    a, b = math.sqrt(PREIMAGE['range_low']), math.sqrt(PREIMAGE['range_high'])

    for x in (PREIMAGE['input_probe'], *PREIMAGE['probe_positions']):
        if not a < x - PREIMAGE['probe_half_width'] < x + PREIMAGE['probe_half_width'] < b:
            raise ValueError('输入点及局部活动范围必须留在正半轴原像内部。')

def _frozen(group):
    group.clear_updaters(recursive = True)

    return group

class _SceneSettings:
    # 此类不继承 Scene，Manim 只会发现下面四个公开分镜
    def setup(self):
        super().setup()
        validate_parameters()
        self.camera.background_color = BG_COLOR
        self.camera.frame.set(width = FRAME_WIDTH, height = FRAME_HEIGHT).move_to(ORIGIN)

    def beat(self, *animations, duration = None, **kwargs):
        self.play(*animations, run_time = TIME_SCALE * (TIMING['reveal'] if duration is None else duration), **kwargs)

    def pause(self, duration = None):
        seconds = TIME_SCALE * (TIMING['hold'] if duration is None else duration)
        # 加速预览时也至少保留一帧，避免产生没有视频流的空片段
        self.wait(max(seconds, STYLE['minimum_hold_frames'] / float(config.frame_rate)))

    def settle(self, group):

        for mob in tuple(self.mobjects):
            mob.clear_updaters(recursive = True)

        self.remove(*tuple(self.mobjects))
        self.add(group)
        self.pause(TIMING['join_hold'])

    def flash_formula(self, formula):
        # 普通直角矩形：柔和黄色光晕与清晰描边同步沿周长闪过
        frame = Rectangle(width = formula.width + 2 * DISK['formula_flash_buff'],
                          height = formula.height + 2 * DISK['formula_flash_buff'],
                          stroke_color = DISK['formula_flash_color'], stroke_width = DISK['formula_flash_width'],
                          fill_opacity = 0).move_to(formula).set_z_index(STYLE['foreground_formula_z'] + 1)
        layers = [frame.copy().set_stroke(width = width, opacity = opacity)
                  for width, opacity in zip(DISK['formula_flash_glow_widths'],
                                            DISK['formula_flash_glow_opacities'])]
        layers.append(frame)
        self.beat(*[ShowPassingFlash(layer, time_width = DISK['formula_flash_time_width'])
                    for layer in layers], duration = TIMING['formula_flash'], rate_func = linear)

class RangeAndInterval(_SceneSettings, MovingCameraScene):
    # 划去ε、δ、d；把允许范围转化为开区间，观察内部点的活动余地
    def construct(self):
        symbols, strikes = VGroup(), VGroup()

        for value, color, position in zip(OPENING['symbols'], OPENING['colors'], OPENING['positions']):
            symbol = _tex(value, position, OPENING['size'], color)
            symbols.add(symbol)
            self.beat(Write(symbol), duration = TIMING['symbol_write'])
            self.pause(TIMING['symbol_gap'])

        for symbol, color in zip(symbols, OPENING['colors']):
            center = symbol.get_center()
            strike = Line(center + OPENING['strike_half_length'] * LEFT,
                          center + OPENING['strike_half_length'] * RIGHT,
                          stroke_color = color, stroke_width = OPENING['strike_width']).set_z_index(STYLE['strike_z'])
            strikes.add(strike)
            self.beat(Create(strike), duration = TIMING['strike'])
            self.beat(symbol.animate.set_color(PALETTE['gray']), strike.animate.set_color(PALETTE['gray']),
                      duration = TIMING['gray'])
            
        self.pause(TIMING['symbols_hold'])
        self.beat(FadeOut(symbols), FadeOut(strikes), duration = TIMING['fade'])
        p = RANGES
        input_region = _range_icon('like', p['input_center'], PALETTE['green'])
        input_label = _tex(FORMULAS['input_range'], p['input_label'], p['set_label_size'], PALETTE['green'])
        self.beat(DrawBorderThenFill(input_region), Write(input_label), duration = TIMING['range_request'])
        self.pause(TIMING['short_hold'])
        output = _range_icon('favorite', p['output_center'], PALETTE['blue'])
        output_label = _tex(FORMULAS['output_range'], p['output_label'], p['set_label_size'], PALETTE['blue'])

        # 左边U保留；从点赞轮廓复制出的几何对象移动并变形，形成右边f(U)
        self.beat(TransformFromCopy(input_region, output, path_arc = p['icon_morph_arc']),
                  Write(output_label), duration = TIMING['icon_morph'])
        arrow = Arrow(_v(p['arrow_start']), _v(p['arrow_end']), buff = 0, color = PALETTE['axis'],
                      stroke_width = p['arrow_width'], tip_length = p['arrow_tip'])
        f_label = _tex(FORMULAS['mapping'], p['f_position'], STYLE['label_size'])
        self.beat(GrowArrow(arrow), Write(f_label),
                  duration = TIMING['range_response'])
        neighborhoods = _range_neighborhoods(input_region, output)
        self.beat(AnimationGroup(*[GrowFromCenter(circle) for circle in neighborhoods['circles']], lag_ratio = 0),
                  FadeIn(neighborhoods['halos']), FadeIn(neighborhoods['centers']), Write(neighborhoods['point_labels']),
                  duration = TIMING['neighborhood_reveal'])
        self.beat(Create(neighborhoods['radius_lines']), Write(neighborhoods['radius_labels']),
                  duration = TIMING['local_reveal'])
        seeds = VGroup(*[_dot(neighborhoods['x0'] + p['delta_radius'] * _v((*q, 0)),
                              PALETTE['green'], p['sample_radius']) for q in p['input_fractions']])
        self.beat(LaggedStart(*[GrowFromCenter(q) for q in seeds], lag_ratio = p['travel_lag']),
                  duration = TIMING['local_reveal'])
        flights, mapped = [], VGroup()

        for seed, offset in zip(seeds, p['output_fractions']):
            copy = seed.copy()
            mapped.add(copy)
            end = neighborhoods['fx0'] + p['epsilon_radius'] * _v((*offset, 0))
            path = CubicBezier(seed.get_center(), seed.get_center() + p['travel_control_x'] * RIGHT + p['travel_lift'] * UP,
                               end + p['travel_control_x'] * LEFT + p['travel_lift'] * UP, end)

            def fly(mob, alpha, trajectory = path):
                mob.move_to(trajectory.point_from_proportion(alpha))
                mob.set_color(_gradient_color(alpha, (PALETTE['green'], PALETTE['blue'])))

            flights.append(UpdateFromAlphaFunc(copy, fly, rate_func = smooth))

        self.beat(LaggedStart(*flights, lag_ratio = p['travel_lag']), duration = TIMING['particle_travel'])
        self.pause(TIMING['long_hold'])
        interval = _interval_stage()
        closed_ends = VGroup(*[_dot([x, INTERVAL['axis_y'], 0], PALETTE['cyan'])
                               for x in (INTERVAL['left'], INTERVAL['right'])])
        leftovers = VGroup(output, output_label, input_label, arrow, f_label, seeds, mapped, neighborhoods['all'])
        self.beat(ReplacementTransform(input_region, interval['segment']), FadeOut(leftovers),
                  Create(interval['axis']), FadeIn(interval['ticks']), FadeIn(closed_ends), Write(interval['labels']),
                  duration = TIMING['bridge'])
        self.pause(TIMING['short_hold'])
        self.beat(*[end.animate.shift(INTERVAL['endpoint_fade_shift'] * sign * UP).set_opacity(0)
                    for end, sign in zip(closed_ends, (-1, 1))],
                  FadeIn(interval['ends']), Write(interval['header']), duration = TIMING['endpoint_remove'])
        self.remove(closed_ends)
        position = ValueTracker(INTERVAL['probe_start'])
        radius = lambda: min(INTERVAL['local_cap'], INTERVAL['local_fraction'] *
                             min(position.get_value() - INTERVAL['left'], INTERVAL['right'] - position.get_value()))
        local = always_redraw(lambda: _local_interval(position.get_value(), radius(), INTERVAL['axis_y']))
        point = always_redraw(lambda: _dot([position.get_value(), INTERVAL['axis_y'], 0]))
        halo = always_redraw(lambda: _halo([position.get_value(), INTERVAL['axis_y'], 0]))
        label = _tex(FORMULAS['point'], size = STYLE['label_size'])
        label.add_updater(lambda mob: mob.move_to(np.array([position.get_value(), INTERVAL['axis_y'], 0])
                                                 + _v(INTERVAL['probe_label_offset'])), call_updater = True)
        self.beat(FadeIn(local), FadeIn(halo), FadeIn(point), FadeIn(label), duration = TIMING['local_reveal'])

        for target in INTERVAL['probe_positions']:
            self.beat(position.animate.set_value(target), duration = TIMING['point_move'], rate_func = smooth)
            self.pause(TIMING['short_hold'])

        wiggle = ValueTracker(0)
        center = position.get_value()
        point.clear_updaters()
        point.add_updater(lambda mob: mob.become(_dot([center + INTERVAL['wiggle_amplitude'] *
                                                      math.sin(TAU * INTERVAL['wiggle_cycles'] * wiggle.get_value()),
                                                      INTERVAL['axis_y'], 0])))
        self.beat(wiggle.animate.set_value(1), duration = TIMING['movement'], rate_func = linear)
        self.pause(TIMING['long_hold'])
        self.beat(FadeOut(_frozen(VGroup(local, point, halo, label))), duration = TIMING['fade'])
        self.settle(interval['all'])

class OpenDisksAndBalls(_SceneSettings, MovingCameraScene):
    # 区间展开成圆盘；内部与边界对比，再把一、二、三维开球并置
    def construct(self):
        previous = _interval_stage()
        self.add(previous['all'])
        self.pause(TIMING['join_hold'])
        center, radius = _v(DISK['center']), DISK['radius']
        disk = _disk_geometry()
        axes = VGroup(
            Line(center + DISK['plane_half_x'] * LEFT, center + DISK['plane_half_x'] * RIGHT,
                 color = PALETTE['axis'], stroke_width = STYLE['axis_width']),
            Line(center + DISK['plane_half_y'] * DOWN, center + DISK['plane_half_y'] * UP,
                 color = PALETTE['axis'], stroke_width = STYLE['axis_width']))
        axes.set_opacity(DISK['plane_opacity'])
        plane_ticks = _horizontal_ticks(center, tuple(value for value in DISK['plane_ticks_x'] if value != 0), DISK['plane_tick_unit'],
                                        DISK['plane_tick_label_gap'], DISK['plane_tick_size'])
        plane_ticks.add(_tex('0', center + _v(DISK['origin_label_offset']), DISK['plane_tick_size']))

        for value in DISK['plane_ticks_y']:
            position = center + value * DISK['plane_tick_unit'] * UP
            plane_ticks.add(Line(position + STYLE['tick_half_length'] * LEFT,
                                 position + STYLE['tick_half_length'] * RIGHT,
                                 color = PALETTE['axis'], stroke_width = STYLE['axis_width']))
            plane_ticks.add(_tex(_number_tex(value), position + DISK['plane_tick_label_gap'] * LEFT,
                                  DISK['plane_tick_size']))
            
        self.beat(ReplacementTransform(previous['segment'], disk[0]),
                  ReplacementTransform(previous['axis'], axes[0]), Create(axes[1]), Create(disk[1]),
                  FadeIn(plane_ticks),
                  FadeOut(VGroup(previous['ticks'], previous['ends'], previous['labels'], previous['header'])),
                  duration = TIMING['bridge'])
        px, py = ValueTracker(DISK['probe_start'][0]), ValueTracker(DISK['probe_start'][1])
        current = lambda: center + np.array([px.get_value(), py.get_value(), 0])
        local_radius = lambda: min(DISK['local_cap'], DISK['local_fraction'] *
                                   (radius - np.linalg.norm(current() - center)))
        local = always_redraw(lambda: Circle(radius = max(local_radius(), STYLE['minimum_draw_radius']),
                                             color = PALETTE['mint'], stroke_width = STYLE['local_width'],
                                             fill_color = PALETTE['mint'], fill_opacity = STYLE['local_opacity']).move_to(current()))
        point = always_redraw(lambda: _dot(current()))
        halo = always_redraw(lambda: _halo(current()))
        label = _tex(FORMULAS['point'], size = STYLE['label_size'])
        label.add_updater(lambda mob: mob.move_to(current() + _v(DISK['label_offset'])), call_updater = True)
        radius_marker = _radius_marker(current(), local_radius())
        radius_marker[0].add_updater(lambda mob: mob.put_start_and_end_on(current(), _radius_end(current(), local_radius())),
                                     call_updater = True)
        radius_marker[1].add_updater(lambda mob: mob.move_to(_radius_label_position(current(), local_radius())),
                                     call_updater = True)
        self.beat(FadeIn(local), FadeIn(halo), FadeIn(point), FadeIn(label), FadeIn(radius_marker),
                  duration = TIMING['local_reveal'])
        
        for x, y in DISK['probe_positions']:
            self.beat(px.animate.set_value(x), py.animate.set_value(y), duration = TIMING['point_move'])
            self.pause(TIMING['short_hold'])

        self.beat(FadeOut(_frozen(VGroup(local, point, halo, label, radius_marker))), duration = TIMING['fade'])
        normal = np.array([math.cos(DISK['boundary_angle']), math.sin(DISK['boundary_angle']), 0])
        edge_position = center + radius * normal
        excluded = _open_dot(edge_position, PALETTE['rose'])
        trial_size = ValueTracker(DISK['trial_radii'][0])
        trial = always_redraw(lambda: Circle(radius = trial_size.get_value(), color = PALETTE['rose'],
                                             stroke_width = STYLE['local_width'], fill_color = PALETTE['rose'],
                                             fill_opacity = STYLE['local_opacity']).move_to(edge_position))
        outside = always_redraw(lambda: _dot(edge_position + DISK['escape_fraction'] * trial_size.get_value() * normal,
                                             PALETTE['rose'], DISK['escape_dot_radius']))
        self.beat(FadeIn(excluded), GrowFromCenter(trial), FadeIn(outside), duration = TIMING['boundary_move'])

        for size in DISK['trial_radii'][1:]:
            self.beat(trial_size.animate.set_value(size), duration = TIMING['trial_shrink'])
            self.pause(TIMING['short_hold'])

        self.pause(TIMING['hold'])
        self.beat(FadeOut(_frozen(VGroup(trial, outside, excluded, axes, plane_ticks))), duration = TIMING['fade'])
        left, middle, right = map(_v, DISK['dimension_centers'])
        one_segment = Line(left + DISK['dimension_interval_half_length'] * LEFT,
                           left + DISK['dimension_interval_half_length'] * RIGHT, color = PALETTE['cyan'],
                           stroke_width = STYLE['interval_width'])
        one_ends = VGroup(_open_dot(one_segment.get_start(), PALETTE['cyan']),
                          _open_dot(one_segment.get_end(), PALETTE['cyan']))
        one = VGroup(one_segment, one_ends, _dot(left))
        small_disk = _disk_geometry(middle, DISK['small_disk_radius'])
        small_center = _dot(middle)
        cloud = _sphere_cloud()
        turn = ValueTracker(SPHERE['start_turn'])
        sphere = always_redraw(lambda: _sphere_view(right, turn.get_value(), cloud))
        dim_labels = VGroup(*[_tex(value, [c[0], DISK['dimension_label_y'], 0], DISK['dimension_label_size'], DISK['dimension_label_color'])
                              for c, value in zip((left, middle, right), FORMULAS['dimension'])])
        
        # 三个维度的例子与统一的开球定义在同一拍出现
        header = _ball_header().set_z_index(STYLE['foreground_formula_z'])
        self.beat(Transform(disk, small_disk), FadeIn(one), FadeIn(sphere), FadeIn(small_center),
                  FadeIn(dim_labels, shift = DISK['dimension_label_rise'] * UP),
                  Write(header),
                  duration = TIMING['dimensions'])
        self.flash_formula(header)
        self.beat(turn.animate.increment_value(SPHERE['turn_angle']), duration = TIMING['sphere_turn'], rate_func = linear)
        self.pause(TIMING['long_hold'])
        final = _disk_stage()
        self.beat(Transform(disk, final['geometry']), FadeOut(_frozen(VGroup(one, sphere, dim_labels, small_center))),
                  FadeIn(VGroup(final['local'], final['halo'], final['radius_marker'], final['point'], final['label'])),
                  Transform(header, final['header']), duration = TIMING['bridge'])
        self.flash_formula(header)
        self.settle(final['all'])
        self.pause(TIMING['disk_final_hold'])

class CarpetOpenSet(_SceneSettings, MovingCameraScene):
    # 放大后在一个洞内移动开圆盘，再放大后在另一个洞内移动开圆盘
    def construct(self):
        previous = _disk_stage()
        self.add(previous['all'])
        self.pause(TIMING['join_hold'])
        carpet = _carpet_stage()
        self.beat(ReplacementTransform(previous['geometry'], carpet['scaffold']),
                  FadeOut(VGroup(previous['local'], previous['halo'], previous['radius_marker'], previous['point'], previous['label'], previous['header'])),
                  duration = TIMING['bridge'])
        
        for level, holes in enumerate(carpet['levels']):
            self.beat(LaggedStart(*[FadeIn(hole, scale = CARPET['hole_reveal_scale']) for hole in holes],
                                 lag_ratio = CARPET['level_lag'] / max(1, len(holes))),
                      duration = TIMING['carpet_level'])
            self.pause(TIMING['short_hold'])

        # 无穷并公式配省略号；屏幕上的有限层只是极限开集的一部分
        self.beat(Write(carpet['header']), Write(carpet['recursion']), duration = TIMING['formula'])
        self.pause(TIMING['long_hold'])
        self.remove(carpet['scaffold'], *tuple(carpet['levels']))
        zoom_log = ValueTracker(0)
        fx, fy = ValueTracker(CARPET['center'][0]), ValueTracker(CARPET['center'][1])
        focus = lambda: np.array([fx.get_value(), fy.get_value(), 0])
        geometry = _carpet_zoom_geometry(1.0, focus())
        update_geometry = lambda mob: _update_carpet_zoom_geometry(mob, math.exp(zoom_log.get_value()), focus())
        self.add(geometry)
        targets, _ = _carpet_zoom_targets()
        destination = _v(CARPET['zoom_center'])
        edge_shade = _screen_edge_mask() if EDGE_SHADE['enabled'] else None
        shade_in = [FadeIn(edge_shade)] if edge_shade is not None else []

        for step, (zoom, target_focus) in enumerate(targets):
            geometry.add_updater(update_geometry)
            extras = [FadeOut(carpet['recursion']), *shade_in] if step == 0 else []
            self.beat(zoom_log.animate.set_value(math.log(zoom)),
                      fx.animate.set_value(target_focus[0]), fy.animate.set_value(target_focus[1]),
                      *extras, duration = TIMING['carpet_zoom'][step], rate_func = _carpet_ease)
            self.pause(TIMING['carpet_zoom_hold'])

            # 每次放大后，都在当前保留块的中央空洞内演示一次圆盘移动
            geometry.clear_updaters(recursive = True)
            cell_side = CARPET['side'] / 3 ** (step + 2)
            half_side = cell_side * zoom / 2
            sx, sy = ValueTracker(0), ValueTracker(0)
            current = lambda: destination + half_side * np.array([sx.get_value(), sy.get_value(), 0])
            local_radius = lambda: CARPET['local_fraction'] * half_side * min(1 - abs(sx.get_value()), 1 - abs(sy.get_value()))
            local = always_redraw(lambda: Circle(radius = local_radius(), color = CARPET['ball_color'],
                                                 stroke_width = STYLE['local_width'], fill_color = CARPET['ball_color'],
                                                 fill_opacity = CARPET['ball_fill_opacity']).move_to(current()))
            point = always_redraw(lambda: _dot(current(), CARPET['probe_color']))
            halo = always_redraw(lambda: _halo(current(), CARPET['probe_color']))
            label = _tex(FORMULAS['point'], size = CARPET['local_size'])
            label.add_updater(lambda mob: mob.move_to(current() + _v(CARPET['probe_label_offset'])), call_updater = True)
            self.beat(FadeIn(local), FadeIn(halo), FadeIn(point), FadeIn(label), duration = TIMING['local_reveal'])

            for x, y in CARPET['local_positions']:
                self.beat(sx.animate.set_value(x), sy.animate.set_value(y), duration = TIMING['point_move'])
                self.pause(TIMING['short_hold'])

            self.pause(TIMING['long_hold'])
            self.beat(FadeOut(_frozen(VGroup(local, halo, point, label))), duration = TIMING['fade'])

        shade_out = [FadeOut(edge_shade)] if edge_shade is not None else []
        geometry.add_updater(update_geometry)
        self.beat(zoom_log.animate.set_value(0),
                  fx.animate.set_value(CARPET['center'][0]), fy.animate.set_value(CARPET['center'][1]),
                  FadeIn(carpet['recursion']), *shade_out,
                  duration = TIMING['carpet_restore'], rate_func = _carpet_ease)
        self.settle(carpet['all'])

class OpenPreimages(_SceneSettings, MovingCameraScene):
    # 点赞与收藏展示开集原像，再用居中单纵轴的x²图像给出具体例子
    def construct(self):
        previous = _carpet_stage()
        self.add(previous['all'])
        self.pause(TIMING['join_hold'])
        concept = _icon_preimage_stage()
        self.remove(previous['all'])
        self.add(previous['scaffold'], previous['levels'], previous['header'], previous['recursion'])
        self.beat(ReplacementTransform(previous['scaffold'], concept['source']),
                  FadeOut(VGroup(previous['levels'], previous['header'], previous['recursion'])),
                  Write(concept['source_label']), duration = TIMING['bridge'])
        self.beat(TransformFromCopy(concept['source'], concept['target'], path_arc = RANGES['icon_morph_arc']),
                  Write(concept['target_label']), GrowArrow(concept['arrow']), Write(concept['arrow_label']),
                  duration = TIMING['icon_morph'])
        
        # 输出端先提出要求；输入端随后才开始搜索
        self.beat(FadeIn(concept['target_region']), Write(concept['target_name']), duration = TIMING['range_request'])
        self.pause(TIMING['hold'])
        self.beat(FadeIn(concept['samples']), duration = TIMING['local_reveal'])
        mapped_points = VGroup()

        for order, index in enumerate(concept['probe_indices']):
            sample = concept['samples'][index]
            accepted = concept['accepted'][index]
            color = PALETTE['blue'] if accepted else PALETTE['rose']
            moving = sample.copy().set_color(color).set_opacity(1)
            start, end = sample.get_center(), concept['images'][index]
            lift = (-1 if order % 2 else 1) * ICON_PREIMAGE['travel_lift'] * UP
            path = CubicBezier(start, start + ICON_PREIMAGE['travel_handle'] * RIGHT + lift,
                               end - ICON_PREIMAGE['travel_handle'] * RIGHT + lift, end)
            trail = path.copy().set_stroke(color = color, width = STYLE['guide_width'], opacity = STYLE['guide_opacity'])
            self.add(moving)
            self.beat(MoveAlongPath(moving, path),
                      ShowPassingFlash(trail, time_width = ICON_PREIMAGE['trail_time_width']),
                      duration = TIMING['preimage_probe'])
            mapped_points.add(moving)
            self.beat(sample.animate.set_color(PALETTE['green'] if accepted else PALETTE['muted']).set_opacity(
                1 if accepted else ICON_PREIMAGE['rejected_opacity']), duration = TIMING['short_hold'])
            
        # 区域表示连续的全部原像；点云仅演示同一映射对样本的判定
        changes = [sample.animate.set_color(PALETTE['green'] if accepted else PALETTE['muted']).set_opacity(
                   1 if accepted else ICON_PREIMAGE['rejected_opacity'])
                   for sample, accepted in zip(concept['samples'], concept['accepted'])]
        self.beat(FadeIn(concept['regions']), Write(concept['definition']), *changes,
                  duration = TIMING['preimage_collect'])
        self.pause(TIMING['long_hold'])
        stage = _preimage_stage()
        axes, output_position = stage['axes'], stage['output_position']
        rest = VGroup(concept['source'], concept['target'], concept['source_label'], concept['target_label'],
                      concept['arrow'], concept['arrow_label'], concept['regions'], concept['samples'],
                      mapped_points, concept['definition'])
        self.beat(ReplacementTransform(concept['target_region'][0], stage['output_fill']),
                  ReplacementTransform(concept['target_region'][1], VGroup(stage['output_line'], stage['output_ends'])),
                  ReplacementTransform(concept['target_name'], stage['v_header']), FadeOut(rest),
                  Create(axes), FadeIn(stage['ticks']), Create(stage['graph']), Write(stage['f_header']),
                  FadeIn(stage['graph_fill']), Create(stage['band_edges']), duration = TIMING['bridge'])
        self.pause(TIMING['hold'])
        p = PREIMAGE
        low, high = p['range_low'], p['range_high']
        a, b = math.sqrt(low), math.sqrt(high)
        height = ValueTracker(low + p['sweep_margin'])
        left_x = lambda: -math.sqrt(height.get_value())
        right_x = lambda: math.sqrt(height.get_value())
        scan = always_redraw(lambda: Line(axes.c2p(p['x_range'][0], height.get_value()),
                                          axes.c2p(p['x_range'][1], height.get_value()), color = PALETTE['blue'],
                                          stroke_width = p['sweep_line_width']).set_opacity(p['sweep_line_opacity']))
        curve_points = always_redraw(lambda: VGroup(*[_dot(axes.c2p(x(), height.get_value()), PALETTE['green'],
                                                          p['probe_dot_radius']) for x in (left_x, right_x)]))
        feet = always_redraw(lambda: VGroup(*[_dot(axes.c2p(x(), 0), PALETTE['green'], p['probe_dot_radius'])
                                               for x in (left_x, right_x)]))
        guides = always_redraw(lambda: VGroup(*[_guide(axes.c2p(x(), 0), axes.c2p(x(), height.get_value()),
                                                       PALETTE['green']) for x in (left_x, right_x)]))
        ranges = always_redraw(lambda: VGroup(
            Line(axes.c2p(left_x(), 0), axes.c2p(-a, 0), color = PALETTE['green'], stroke_width = STYLE['interval_width']),
            Line(axes.c2p(a, 0), axes.c2p(right_x(), 0), color = PALETTE['green'], stroke_width = STYLE['interval_width'])))
        output_point = always_redraw(lambda: _dot(output_position(height.get_value()), PALETTE['blue'], p['probe_dot_radius']))
        self.beat(FadeIn(VGroup(scan, guides, ranges, feet, curve_points, output_point)),
                  FadeIn(stage['input_ends']), duration = TIMING['local_reveal'])
        self.beat(height.animate.set_value(high - p['sweep_margin']), duration = TIMING['sample_sweep'], rate_func = smooth)
        self.pause(TIMING['short_hold'])
        self.beat(FadeOut(_frozen(VGroup(scan, guides, feet, curve_points, output_point, ranges))),
                  FadeIn(stage['intervals']), Create(stage['selected']),
                  FadeIn(stage['selected_ends']), FadeIn(stage['input_formula']),
                  duration = TIMING['formula'])
        self.pause(TIMING['long_hold'])

        # 两侧同时活动，不把“原像”误画成某一个反函数分支
        probe = ValueTracker(p['input_probe'])
        neighborhood = always_redraw(lambda: VGroup(*[_local_interval(
            axes.c2p(sign * p['input_probe'], 0)[0],
            abs(axes.c2p(p['probe_half_width'], 0)[0] - axes.c2p(0, 0)[0]), axes.c2p(0, 0)[1], p['local_interval_height'])
                                                     for sign in (-1, 1)]))
        input_points = always_redraw(lambda: VGroup(*[_dot(axes.c2p(sign * probe.get_value(), 0),
                                                           PALETTE['pale_yellow'], p['probe_dot_radius']) for sign in (-1, 1)]))
        curve_points = always_redraw(lambda: VGroup(*[_dot(axes.c2p(sign * probe.get_value(), probe.get_value() ** 2),
                                                           PALETTE['pale_yellow'], p['probe_dot_radius']) for sign in (-1, 1)]))
        output_point = always_redraw(lambda: _dot(output_position(probe.get_value() ** 2),
                                                  PALETTE['pale_yellow'], p['probe_dot_radius']))
        wires = always_redraw(lambda: VGroup(
            *[_guide(axes.c2p(sign * probe.get_value(), 0), axes.c2p(sign * probe.get_value(), probe.get_value() ** 2),
                      PALETTE['pale_yellow'], p['wire_opacity']) for sign in (-1, 1)],
            *[_guide(axes.c2p(sign * probe.get_value(), probe.get_value() ** 2), output_position(probe.get_value() ** 2),
                     PALETTE['pale_yellow'], p['wire_opacity']) for sign in (-1, 1)]))
        self.beat(FadeIn(neighborhood), FadeIn(input_points), FadeIn(curve_points), FadeIn(output_point), FadeIn(wires),
                  duration = TIMING['local_reveal'])
        
        for x in p['probe_positions']:
            self.beat(probe.animate.set_value(x), duration = TIMING['mapping_probe'])
            self.pause(TIMING['short_hold'])

        self.pause(TIMING['long_hold'])
        self.beat(FadeOut(_frozen(VGroup(neighborhood, input_points, curve_points, output_point, wires))),
                  FadeOut(VGroup(stage['f_header'], stage['v_header'])), duration = TIMING['fade'])
        criterion = _tex(FORMULAS['criterion'], STYLE['header'])
        criterion[2].set_color(PALETTE['blue'])
        criterion[3].set_color(PALETTE['green'])
        criterion = _final_formula_outline(criterion)
        self.beat(FadeIn(criterion), duration = TIMING['formula'])
        self.beat(ShowPassingFlash(stage['output_line'].copy().set_stroke(width = p['final_pulse_width']),
                                  time_width = p['final_pulse_time_width']),
                  ShowPassingFlash(stage['intervals'].copy().set_stroke(width = p['final_pulse_width']),
                                  time_width = p['final_pulse_time_width']), duration = TIMING['bridge'])
        self.pause(TIMING['final_hold'])
        
        for mob in self.mobjects:
            mob.clear_updaters(recursive = True)
