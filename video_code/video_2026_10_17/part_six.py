from manim import *
import math
import numpy as np
from svgelements import Path as SVGPath

# 全部可调参数
BG_COLOR = "#000012"
FRAME_WIDTH, FRAME_HEIGHT = 128 / 9, 8.0
FRAME_RATE = 60
TIME_SCALE = 1.0
PALETTE = dict(
    axis = "#FFFFFF", ink = "#FFFFFF", cyan = "#56CEE8", blue = "#56CEE8",
    green = "#9EE3A2", yellow = "#E8EE63", pale_yellow = "#FFE17D",
    mint = "#68E6C0", rose = "#EF819B", muted = "#687C98", gray = "#747B89",
)
STYLE = dict(
    formula_size = 38, label_size = 30, small_size = 26, formula_width = 12.6,
    header = (0, 3.10, 0), footer = (0, -2.90, 0), label_outline = 3.0,
    axis_width = 2.0, curve_width = 2.2, guide_width = 1.2,
    guide_opacity = 0.26, fill_opacity = 0.09, local_fill = 0.12,
    dot_radius = 0.065, open_radius = 0.070, open_width = 2.3,
    halo_radius = 0.15, halo_opacity = 0.12,
    boundary_samples = 129, boundary_dashes = 48, boundary_ratio = 0.58,
    boundary_dash_length = 0.080, boundary_gap_length = 0.060, minimum_dashes = 10,
    formula_z = 40, point_z = 20, numeric_tolerance = 1e-8,
    outline_color = "#000000",
    minimum_hold_frames = 1,
)
TIMING = dict(
    reveal = 1.35, formula = 1.20, bridge = 2.20, zoom = 3.60,
    point_move = 2.60, travel = 4.80, camera_pan = 3.10, short_hold = 0.45,
    hold = 1.10, long_hold = 2.10, join_hold = 0.20, fade = 0.85,
    output_request = 1.50, input_response = 1.60, radius_change = 2.00,
    final_hold = 3.00, animation_pause = 0.70,
)
MAPPING = dict(
    input_center = (-3.55, -0.15, 0), output_center = (3.55, -0.15, 0),
    icon_width = 3.30, icon_stroke = 2.2, icon_fill = 0.07,
    input_label = (-3.55, 2.08, 0), output_label = (3.55, 2.08, 0),
    arrow_start = (-1.55, -0.15, 0), arrow_end = (1.55, -0.15, 0),
    arrow_width = 1.8, arrow_tip = 0.17, f_position = (0, 0.23, 0),
    source_svg = (22.0, 21.0), target_svg = (12.5, 13.0),
    branch_x = 0.56, branch_y = 0.43,
    target_radius = 0.42, map_radius_cap = 1.50,
    region_fill = 0.12, region_width = 2.0, region_label_size = 31,
    target_label_offset = (0.0, 0.78, 0), source_label_offset = (0.0, -1.45, 0),
    contour_samples = 14, containment_samples = 128,
)
# 内嵌前五段使用的同一组 B 站点赞、收藏轮廓，不需要新建 SVG 素材文件
BILIBILI_ICONS = dict(
    like = r"M9.77234 30.8573V11.7471H7.54573C5.50932 11.7471 3.85742 13.3931 3.85742 15.425V27.1794C3.85742 29.2112 5.50932 30.8573 7.54573 30.8573H9.77234ZM11.9902 30.8573V11.7054C14.9897 10.627 16.6942 7.8853 17.1055 3.33591C17.2666 1.55463 18.9633 0.814421 20.5803 1.59505C22.1847 2.36964 23.243 4.32583 23.243 6.93947C23.243 8.50265 23.0478 10.1054 22.6582 11.7471H29.7324C31.7739 11.7471 33.4289 13.402 33.4289 15.4435C33.4289 15.7416 33.3928 16.0386 33.3215 16.328L30.9883 25.7957C30.2558 28.7683 27.5894 30.8573 24.528 30.8573H11.9911H11.9902Z",
    favorite = r"M19.8071 9.26152C18.7438 9.09915 17.7624 8.36846 17.3534 7.39421L15.4723 3.4972C14.8998 2.1982 13.1004 2.1982 12.4461 3.4972L10.6468 7.39421C10.1561 8.36846 9.25639 9.09915 8.19315 9.26152L3.94016 9.91102C2.63155 10.0734 2.05904 11.6972 3.04049 12.6714L6.23023 15.9189C6.96632 16.6496 7.29348 17.705 7.1299 18.7605L6.39381 23.307C6.14844 24.6872 7.62063 25.6614 8.84745 25.0119L12.4461 23.0634C13.4276 22.4951 14.6544 22.4951 15.6359 23.0634L19.2345 25.0119C20.4614 25.6614 21.8518 24.6872 21.6882 23.307L20.8703 18.7605C20.7051 17.705 21.0339 16.6496 21.77 15.9189L24.9597 12.6714C25.9412 11.6972 25.3687 10.0734 24.06 9.91102L19.8071 9.26152Z",
)
PROOF = dict(
    target_zoom_width = 4.50, input_zoom_width = 3.60,
    label_world_scale = 0.29, source_region_label = (0, -0.50, 0), region_label_gap = 0.18,
    label_offset = (0, -0.34, 0),
    epsilon_fraction = 0.79, delta_fraction = 0.78,
    input_radius_angle = 0.72 * PI, output_radius_angle = 0.27 * PI,
    radius_label_gap = 0.16, radius_width = 1.7,
    probe_units = ((0.0, 0.0), (-0.38, 0.25), (0.34, -0.26), (0.0, 0.0)),
    sample_fractions = ((-0.70, 0.10), (-0.25, 0.62), (0.28, 0.62),
                        (0.70, 0.08), (0.32, -0.58), (-0.42, -0.52)),
    focus_radius = 0.043, sample_radius = 0.038, sample_lag = 0.11, travel_handle = 1.05,
    travel_lift = 0.45, reverse_radii = (0.30, 0.21, 0.13), reverse_start_radius = 0.30,
)
FIRST_SCENE = dict(
    # 第一镜先移动取景再放大；原箭头与 f 一起自然放大且完整入镜
    zoom_width = 6.60, input_view_center = (-1.10, -0.50, 0), output_view_center = (1.10, -0.10, 0),
    reposition_time = 1.80,
    formula_position = (0, -2.25, 0), final_formula_position = (0, 3.10, 0),
    source_zoom_label_offset = (0, -0.60, 0),
    probe_units = ((0.28, 0.18), (-0.24, 0.32), (0.34, 0.30), (0.28, 0.18)),
    image_fill = 0.16, region_dashes = 18, region_travel = 4.20,
    output_point_label_gap = 0.18, region_z = 5, arrow_z = 30,
)
SECOND_SCENE = dict(
    # 默认沿用第一镜的取景和视觉尺寸；epsilon 要求与完整原像一起连续响应
    zoom_width = FIRST_SCENE['zoom_width'],
    input_view_center = FIRST_SCENE['input_view_center'], output_view_center = FIRST_SCENE['output_view_center'],
    reposition_time = FIRST_SCENE['reposition_time'],
    formula_position = FIRST_SCENE['formula_position'],
    source_zoom_label_offset = FIRST_SCENE['source_zoom_label_offset'],
    probe_unit = FIRST_SCENE['probe_units'][0], epsilon_values = PROOF['reverse_radii'],
    image_fill = FIRST_SCENE['image_fill'], region_dashes = FIRST_SCENE['region_dashes'],
    region_travel = FIRST_SCENE['region_travel'],
    output_point_label_gap = FIRST_SCENE['output_point_label_gap'],
    region_z = FIRST_SCENE['region_z'], arrow_z = FIRST_SCENE['arrow_z'],
)
CAMERA_STYLE = dict(
    stroke_exponent = 1.0,
    arrow_zoom_reference = 3.2, arrow_zoom_x = 4.45, arrow_zoom_y = -2.10,
    arrow_zoom_half_length = 1.05, arrow_label_gap = 0.30,
)
FORMULAS = dict(
    forward = (r"f \in C(X,Y),\ V = V^{\circ}", r"\ \Longrightarrow\ ", r"f^{-1}(V) = \bigl(f^{-1}(V)\bigr)^{\circ}"),
    backward = (r"\forall V = V^{\circ}:\ f^{-1}(V) = \bigl(f^{-1}(V)\bigr)^{\circ}",
                r"\ \Longrightarrow\ ", r"f \in C(X,Y)"),
    forward_output = r"B_{\varepsilon}\bigl(f(x_0)\bigr) \subset V",
    forward_input = r"B_{\delta}(x_0) \subset f^{-1}(V)",
    forward_result = r"\forall x_0 \in f^{-1}(V)\quad \exists \delta > 0:\ B_{\delta}(x_0) \subset f^{-1}(V)",
    backward_output = r"U = B_{\varepsilon}\bigl(f(x_0)\bigr)",
    backward_input = r"B_{\delta}(x_0) \subset f^{-1}(U)",
    backward_result = r"d_X(x,x_0) < \delta\quad \Longrightarrow\quad d_Y\bigl(f(x),f(x_0)\bigr) < \varepsilon",
    overview_bottom = r"V = V^{\circ}\quad \Longrightarrow\quad f^{-1}(V) = \bigl(f^{-1}(V)\bigr)^{\circ}",
    reverse_quantifier = r"\forall x_0 \in X\quad \forall \varepsilon > 0\quad \exists \delta > 0",
)

# Exact part_five resting composition; self-contained bridge geometry.
PREV_BG_COLOR = "#000012"
PREV_FRAME_WIDTH, PREV_FRAME_HEIGHT = 128 / 9, 8.0
PREV_PALETTE = dict(
    axis = "#FFFFFF", ink = "#FFFFFF", blue = "#56CEE8", cyan = "#56CEE8",
    green = "#9EE3A2", yellow = "#E8EE63", pale_yellow = "#FFE17D",
    mint = "#68E6C0", rose = "#EF819B", muted = "#687C98", gray = "#747B89",
)
PREV_STYLE = dict(
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
PREV_PREIMAGE = dict(
    origin = (0, -1.77, 0), x_range = (-2.6, 2.6, 1), y_range = (0, 4.9, 1),
    x_length = 7.75, y_length = 4.00, x_ticks = tuple(range(-5, 6)), y_ticks = (1, 2, 3, 4, 5),
    graph_domain = (-2.14, 2.14), gradient = (PREV_PALETTE['cyan'], PREV_PALETTE['green'], PREV_PALETTE['yellow']),
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
PREV_FORMULAS = dict(
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

# 合并第三镜的全部可调参数
TOPO_STYLE = dict(
    fill_opacity = 0.075, emphasis_fill = 0.15, universe_fill = 0.035,
    dim_opacity = 0.28, edge_width = 2.1, region_width = 2.5,
    edge_dashes = 72, dash_ratio = 0.57, arc_samples = 181,
    point_radius = 0.075, endpoint_radius = 0.083, endpoint_width = 2.7,
    formula_size = 39, small_formula_size = 31, set_label_size = 32,
    formula_width = 12.6, header = (0, 3.12, 0), footer = (0, -3.02, 0),
    local_opacity = 0.12, local_width = 2.0, local_label_gap = 0.36,
    axis_width = 2.1, axis_opacity = 1.0, line_half_width = 6.65,
    axis_y = -0.2, tick_half_height = 0.085, tick_label_y = -0.68,
    line_z = 1, fill_z = 2, edge_z = 4, point_z = 9, formula_z = 15,
    path_tip_ratio = 0.15, label_outline_width = 5.0,
)
TOPO_START = dict(
    center = (0, -0.2, 0), radius = 1.42, point = (-0.25, -0.1, 0),
    local_radius = 0.34, label_offset = (0.14, -0.3, 0),
    probe_shift = (0.60, 0.38, 0),
    formula = r"U = U^{\circ}", formula_position = (0, 3.10, 0),
)
TOPO_OPERATIONS = dict(
    universe_center = (0, -0.2, 0), universe_width = 11.65,
    universe_height = 5.05, universe_corner = 0.3,
    universe_label = (-5.31, 2.16, 0), central_label = (0, -0.2, 0),
    central_label_size = 66,
    full_formula = r"X = X^{\circ}", empty_formula = r"\varnothing = \varnothing^{\circ}",
    left_center = (-1.45, -0.35, 0), right_center = (1.45, -0.35, 0),
    radius = 2.02, labels = ((-2.55, 1.18, 0), (2.55, 1.18, 0)),
    union_probe_positions = ((-2.35, -0.35, 0), (0, -0.35, 0), (2.35, -0.35, 0)),
    union_probe_radius = 0.35, union_label_offset = (0.15, -0.42, 0),
    lens_probe_positions = ((-0.17, -0.22, 0), (0.17, -0.53, 0)),
    local_radius_fraction = 0.72, local_radius_angles = (0.70 * PI, 0.18 * PI),
    min_formula = r"r = \min(r_1,r_2) > 0", proof_position = (0, 2.06, 0),
    union_formula = r"\left(\bigcup_{i\in I}U_i\right)^{\circ} = \bigcup_{i\in I}U_i",
    intersection_formula = r"\left(\bigcap_{k=1}^{m}U_k\right)^{\circ} = \bigcap_{k=1}^{m}U_k\qquad(m<\infty)",
    small_labels = (r"U_1", r"U_2"), point_label = r"x_0",
)
TOPO_NESTED = dict(
    unit = 3.4, initial_n = 1, n_values = (2, 3, 5, 9, 16, 32),
    interval_width = 5.2, counter_gap = 0.08,
    formula_position = (0, 2.95, 0), n_position = (0, 2.1, 0),
    line_label_position = (6.34, 0.25, 0),
    tick_values = (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5),
    labelled_ticks = (-1.0, 0.0, 1.0), minor_tick_fraction = 0.65,
    finite_formula = r"U_n = \left(-\frac{1}{n},\frac{1}{n}\right)",
    intersection_formula = r"\bigcap_{n=1}^{\infty}\left(-\frac{1}{n},\frac{1}{n}\right) = \{0\}",
    nonopen_formula = r"\{0\}^{\circ} = \varnothing", nonopen_position = (0, -1.62, 0),
    limit_formula = r"n\longrightarrow\infty",
    flash_radius = 0.28, flash_length = 0.17, flash_lines = 12, flash_width = 3.0,
)
TOPO_END = dict(
    backdrop_opacity = 0.10,
    x_position = (0, 2.65, 0), x_size = 82, x_opacity = 0.26,
    axiom_positions = ((0, 1.15, 0), (0, 0.05, 0), (0, -1.05, 0)), axiom_size = 36,
    axiom_color = 'pale_yellow',
    axiom_formulas = (
        r"X,\varnothing\in\mathcal{T}",
        r"\{U_i\}_{i\in I}\subseteq\mathcal{T}\quad\Longrightarrow\quad\bigcup_{i\in I}U_i\in\mathcal{T}",
        r"U_1,\ldots,U_m\in\mathcal{T}\quad\Longrightarrow\quad\bigcap_{k=1}^{m}U_k\in\mathcal{T}\quad(m<\infty)",
    ),
    symbol_position = (0, 0.05, 0), symbol_size = 146,
    pair_position = (0, 0.05, 0), pair_size = 108,
    foreground_z = 30,
)
TOPO_TIME = dict(
    opening_hold = 0.85, scan = 2.1, short_hold = 0.7, bridge = 1.65,
    full_reveal = 1.25, full_hold = 0.8, full_release = 1.15,
    empty_reveal = 1.0, empty_hold = 0.8,
    disks_reveal = 1.8, labels_reveal = 0.8, formula = 1.15,
    region_reveal = 1.5, probe = 2.35, probe_hold = 0.65,
    intersection_reveal = 1.65, intersection_probe = 1.8, intersection_hold = 1.1,
    interval_reveal = 1.7, shrink = 1.25, shrink_hold = 0.22,
    singleton = 1.5, singleton_hold = 1.0, nonopen = 1.1,
    summary_dim = 1.2, summary_write = 1.9, summary_hold = 2.1,
    summary_collapse = 2.1, symbol_hold = 1.1, pair_build = 1.7, final_hold = 3.0,
)

# 参数与数学几何自检
config.background_color = BG_COLOR
config.frame_width, config.frame_height = FRAME_WIDTH, FRAME_HEIGHT

if FRAME_RATE is not None:
    config.frame_rate = FRAME_RATE

def _first_local_geometry(unit):
    scale = FIRST_SCENE['zoom_width'] / FRAME_WIDTH
    state = _local_geometry(unit, display_scale = scale)
    state['input_ball'] = _first_neighborhood_region(unit, 0)
    state['image_region'] = _first_neighborhood_region(unit, 1)
    output_label_center = state['points'][1].get_center() + DOWN * (state['epsilon'] + scale * FIRST_SCENE['output_point_label_gap'])
    state['labels'][1].move_to(output_label_center)
    # V 和原像的标签始终使用原场景中的同一个对象，不在此创建或替换。
    state['all'] = VGroup(state['input_ball'], state['output_ball'], state['points'],
                          state['labels'], state['markers'], state['image_region'])
    
    return state

def _first_neighborhood_region(unit, blend):
    _, _, source_center, target_center = _mapping_geometry()
    local = _source_local(unit)
    mapped = _map_local(local)
    epsilon = PROOF['epsilon_fraction'] * (MAPPING['target_radius'] - np.linalg.norm(mapped))
    delta = _safe_delta(local, epsilon)
    points = []

    for angle in np.linspace(0, TAU, STYLE['boundary_samples']):
        point = local + delta * _v((math.cos(angle), math.sin(angle), 0))
        start = source_center + point
        end = target_center + _map_local(point)
        points.append((1 - blend) * start + blend * end)

    area = VMobject(stroke_width = 0, fill_color = PALETTE['green'],
                    fill_opacity = FIRST_SCENE['image_fill'])
    area.set_points_as_corners(points).close_path()
    outline = area.copy().set_fill(opacity = 0).set_stroke(PALETTE['green'], width = STYLE['curve_width'])
    edge = DashedVMobject(outline, num_dashes = FIRST_SCENE['region_dashes'], dashed_ratio = STYLE['boundary_ratio'])

    return VGroup(area, edge).set_z_index(FIRST_SCENE['region_z'])

def _compound_formula_parts(mob):
    # 同色字形先做真实几何并集，删除推导号拼接处的内部描边
    if getattr(mob, '_formula_unioned', False):
        return mob
    if not isinstance(mob, MathTex):
        for child in mob.submobjects:
            _compound_formula_parts(child)
        return mob
    
    # 保留顶层片段和 tex_string，原有分段配色与公式变换接口不变
    for part in mob.submobjects:
        if getattr(part, '_formula_unioned_part', False):
            continue
        glyphs = list(part.family_members_with_points())
        if not glyphs:
            part._formula_unioned_part = True
            continue

        # 与自身并集同样会规范化单个 compound 的路径，并保留字形孔洞
        compound = Union(*glyphs) if len(glyphs) > 1 else Union(glyphs[0], glyphs[0].copy())
        compound.match_style(glyphs[0], family = False)
        compound.set_z_index(part.z_index, family = False)
        compound._formula_glyph = True
        compound._formula_compound = True
        part.clear_points()
        part.submobjects = [compound]
        part._formula_unioned_part = True
    mob._formula_unioned = True
    mob._formula_compounded = True

    return mob

def _motion_ease(alpha):
    # 五次平滑曲线的速度、加速度在首尾都为零
    alpha = float(np.clip(alpha, 0, 1))

    return alpha ** 3 * (10 - 15 * alpha + 6 * alpha ** 2)

def _preimage_region(raw_radius, origin):
    points = [_v(origin) + _source_local((raw_radius * math.cos(t), raw_radius * math.sin(t)))
              for t in np.linspace(0, TAU, STYLE['boundary_samples'])]
    area = VMobject(stroke_width = 0, fill_color = PALETTE['green'], fill_opacity = MAPPING['region_fill'])
    area.set_points_smoothly(points).close_path()
    outline = area.copy().set_fill(opacity = 0).set_stroke(PALETTE['green'], width = MAPPING['region_width'])
    edge = DashedVMobject(outline, num_dashes = STYLE['boundary_dashes'], dashed_ratio = STYLE['boundary_ratio'])

    return VGroup(area, edge)

def _outline_formula(mob, width = None):
    outline_width = STYLE['label_outline'] if width is None else width
    _compound_formula_parts(mob)
    mob._formula_object = True
    mob.set_background_stroke(width = 0, opacity = 0)

    for glyph in mob.family_members_with_points():
        glyph._formula_glyph = True
        glyph.set_stroke(color = STYLE['outline_color'], width = outline_width,
                         opacity = 1, background = True, family = False)
        
    return mob

def _v(value):

    return np.array(value, dtype = float)

def _tex(value, position = None, size = None, color = None, width = None):
    parts = value if isinstance(value, (tuple, list)) else (value,)
    mob = MathTex(*parts, font_size = STYLE['formula_size'] if size is None else size,
                  color = PALETTE['ink'] if color is None else color)
    maximum = STYLE['formula_width'] if width is None else width

    if mob.width > maximum:
        mob.scale_to_fit_width(maximum)
    if position is not None:
        mob.move_to(_v(position))

    return _outline_formula(mob).set_z_index(STYLE['formula_z'])

def _dot(position, color = None, radius = None):

    return Dot(_v(position), radius = STYLE['dot_radius'] if radius is None else radius,
               color = PALETTE['pale_yellow'] if color is None else color).set_z_index(STYLE['point_z'])

def _open_dot(position, color = None, radius = None):

    return Circle(radius = STYLE['open_radius'] if radius is None else radius,
                  stroke_color = PALETTE['cyan'] if color is None else color,
                  stroke_width = STYLE['open_width'], fill_color = BG_COLOR,
                  fill_opacity = 1).move_to(_v(position)).set_z_index(STYLE['point_z'])

def _disk(center, radius, color, fill = None):
    shade = Circle(radius = radius, stroke_width = 0, fill_color = color,
                   fill_opacity = STYLE['fill_opacity'] if fill is None else fill).move_to(center)
    outline = Circle(radius = radius, color = color, stroke_width = STYLE['curve_width']).move_to(center)
    dash_count = max(STYLE['minimum_dashes'], min(STYLE['boundary_dashes'],
                     int(TAU * radius / (STYLE['boundary_dash_length'] + STYLE['boundary_gap_length']))))
    edge = DashedVMobject(outline, num_dashes = dash_count,
                          dashed_ratio = STYLE['boundary_ratio'])
    
    return VGroup(shade, edge)

def _icon(kind, center, color, width = None):
    icon = VMobjectFromSVGPath(SVGPath(BILIBILI_ICONS[kind]), stroke_color = color,
                              stroke_width = MAPPING['icon_stroke'], fill_color = color,
                              fill_opacity = MAPPING['icon_fill'])
    icon.svg_center = icon.get_center().copy()
    icon.svg_scale = (MAPPING['icon_width'] if width is None else width) / icon.width
    icon.stretch(-1, dim = 1, about_point = ORIGIN)
    icon.scale(icon.svg_scale, about_point = ORIGIN).move_to(_v(center))

    return icon

def _icon_point(icon, svg_point):
    x, y = svg_point

    return icon.get_center() + icon.svg_scale * _v((x - icon.svg_center[0], icon.svg_center[1] - y, 0))

def _mapping_geometry():
    source = _icon('like', MAPPING['input_center'], PALETTE['green'])
    target = _icon('favorite', MAPPING['output_center'], PALETTE['cyan'])

    return source, target, _icon_point(source, MAPPING['source_svg']), _icon_point(target, MAPPING['target_svg'])

def _radial_scale():

    return math.atanh(1 / MAPPING['map_radius_cap'])

def _raw(local):
    # 单射椭圆坐标：一个输出开圆盘的完整原像只有一个连通区域
    return _v((local[0] / MAPPING['branch_x'], local[1] / MAPPING['branch_y'], 0))

def _map_local(local):
    raw = _raw(local)
    length = np.linalg.norm(raw)

    if length < STYLE['numeric_tolerance']:
        return np.zeros(3)
    radius = MAPPING['target_radius'] * MAPPING['map_radius_cap'] * math.tanh(_radial_scale() * length)

    return radius * raw / length

def _source_local(unit):
    u, v = unit

    return _v((MAPPING['branch_x'] * u, MAPPING['branch_y'] * v, 0))


def _inverse_radius(radius):

    return math.atanh(radius / (MAPPING['target_radius'] * MAPPING['map_radius_cap'])) / _radial_scale()

def _arrow(start, end, label_position):

    return VGroup(Arrow(_v(start), _v(end), buff = 0, color = PALETTE['axis'],
                        stroke_width = MAPPING['arrow_width'], tip_length = MAPPING['arrow_tip']),
                  _tex('f', label_position, STYLE['label_size']))

def _overview_stage():
    source, target, source_center, target_center = _mapping_geometry()
    arrow = _arrow(MAPPING['arrow_start'], MAPPING['arrow_end'], MAPPING['f_position'])
    base = VGroup(source, target, arrow,
                  _tex('X', MAPPING['input_label'], color = PALETTE['green']),
                  _tex('Y', MAPPING['output_label'], color = PALETTE['cyan']))
    regions = VGroup(_preimage_region(1, source_center))
    target_region = _disk(target_center, MAPPING['target_radius'], PALETTE['cyan'])
    labels = VGroup(_tex('V', target_center + _v(MAPPING['target_label_offset']), color = PALETTE['cyan']),
                    _tex(r'f^{-1}(V)', source_center + _v(MAPPING['source_label_offset']),
                         MAPPING['region_label_size'], PALETTE['green']))
    
    return dict(base = base, source = source, target = target, regions = regions,
                target_region = target_region, labels = labels,
                all = VGroup(base, regions, target_region, labels))

def _overview_join():
    stage = _overview_stage()

    return VGroup(stage['all'], _tex(FORMULAS['overview_bottom'], FIRST_SCENE['final_formula_position']))

def _safe_delta(local, epsilon):
    # tanh 径向压缩乘椭圆线性变换的全局 Lipschitz 上界
    lipschitz = MAPPING['target_radius'] * MAPPING['map_radius_cap'] * _radial_scale()
    lipschitz *= max(1 / MAPPING['branch_x'], 1 / MAPPING['branch_y'])

    return PROOF['delta_fraction'] * epsilon / lipschitz

def _local_geometry(unit, reverse = False, epsilon = None, display_scale = None):
    # 所有点、开球都留在原点赞/收藏的世界坐标中；只让相机靠近
    _, _, source_center, target_center = _mapping_geometry()
    scale = PROOF['label_world_scale'] if display_scale is None else display_scale
    local = _source_local(unit)
    mapped = _map_local(local)

    if epsilon is None:
        epsilon = PROOF['epsilon_fraction'] * (MAPPING['target_radius'] - np.linalg.norm(mapped))

    delta = _safe_delta(local, epsilon)
    left, right = source_center + local, target_center + mapped
    input_ball = _disk(left, delta, PALETTE['green'], STYLE['local_fill'])
    output_ball = VGroup() if reverse else _disk(right, epsilon, PALETTE['pale_yellow'], STYLE['local_fill'])
    points = VGroup(_dot(left, radius = PROOF['focus_radius'] * scale),
                    _dot(right, radius = PROOF['focus_radius'] * scale))
    labels = VGroup(_tex(r'x_0', left + scale * _v(PROOF['label_offset']), STYLE['small_size'] * scale),
                    _tex(r'f(x_0)', right + scale * _v(PROOF['label_offset']), STYLE['small_size'] * scale))
    markers = VGroup(_world_radius_marker(left, delta, r'\delta', PALETTE['green'], PROOF['input_radius_angle'], scale),
                     _world_radius_marker(right, epsilon, r'\varepsilon', PALETTE['pale_yellow'], PROOF['output_radius_angle'], scale))
    region_labels = VGroup(
        _tex(r'f^{-1}(U)' if reverse else r'f^{-1}(V)',
             source_center + _v(PROOF['source_region_label']), STYLE['label_size'] * scale, PALETTE['green']),
        _tex('U' if reverse else 'V', target_center + _v((0, (epsilon if reverse else MAPPING['target_radius']) + scale * PROOF['region_label_gap'], 0)),
             STYLE['label_size'] * scale, PALETTE['cyan']))
    
    # 字体轮廓也按世界坐标缩小，否则直接推镜后黑边会遮住字形
    for text in (labels, markers, region_labels):
        for glyph in text.family_members_with_points():
            if glyph.get_fill_opacity() > 0:
                glyph.set_stroke(STYLE['outline_color'], width = STYLE['label_outline'] * scale, background = True)

    return dict(input_ball = input_ball, output_ball = output_ball, points = points, labels = labels,
                markers = markers, region_labels = region_labels, local = local, epsilon = epsilon, delta = delta,
                all = VGroup(input_ball, output_ball, points, labels, markers, region_labels))

def _inverse_map_local(mapped):
    length = np.linalg.norm(mapped)

    if length < STYLE['numeric_tolerance']:
        return np.zeros(3)
    
    raw_radius = _inverse_radius(length)

    return _source_local((raw_radius * mapped[0] / length, raw_radius * mapped[1] / length))

def _second_preimage_region(unit, epsilon):
    _, _, source_center, _ = _mapping_geometry()
    mapped = _map_local(_source_local(unit))
    points = [source_center + _inverse_map_local(mapped + epsilon * _v((math.cos(t), math.sin(t), 0)))
              for t in np.linspace(0, TAU, STYLE['boundary_samples'])]
    area = VMobject(stroke_width = 0, fill_color = PALETTE['green'], fill_opacity = MAPPING['region_fill'])
    area.set_points_as_corners(points).close_path()
    outline = area.copy().set_fill(opacity = 0).set_stroke(PALETTE['green'], width = MAPPING['region_width'])
    edge = DashedVMobject(outline, num_dashes = STYLE['boundary_dashes'], dashed_ratio = STYLE['boundary_ratio'])

    return VGroup(area, edge).set_z_index(SECOND_SCENE['region_z'])

def _second_neighborhood_region(unit, epsilon, blend):
    _, _, source_center, target_center = _mapping_geometry()
    local = _source_local(unit)
    delta = _safe_delta(local, epsilon)
    points = []

    for angle in np.linspace(0, TAU, STYLE['boundary_samples']):
        point = local + delta * _v((math.cos(angle), math.sin(angle), 0))
        start, end = source_center + point, target_center + _map_local(point)
        points.append((1 - blend) * start + blend * end)

    area = VMobject(stroke_width = 0, fill_color = PALETTE['green'], fill_opacity = SECOND_SCENE['image_fill'])
    area.set_points_as_corners(points).close_path()
    outline = area.copy().set_fill(opacity = 0).set_stroke(PALETTE['green'], width = STYLE['curve_width'])
    edge = DashedVMobject(outline, num_dashes = SECOND_SCENE['region_dashes'], dashed_ratio = STYLE['boundary_ratio'])

    return VGroup(area, edge).set_z_index(SECOND_SCENE['region_z'])

def _second_local_geometry(unit, epsilon):
    scale = SECOND_SCENE['zoom_width'] / FRAME_WIDTH
    state = _local_geometry(unit, reverse = True, epsilon = epsilon, display_scale = scale)
    state['input_ball'] = _second_neighborhood_region(unit, epsilon, 0)
    state['image_region'] = _second_neighborhood_region(unit, epsilon, 1)
    state['labels'][1].move_to(state['points'][1].get_center() + DOWN * (epsilon + scale * SECOND_SCENE['output_point_label_gap']))
    state['all'] = VGroup(state['input_ball'], state['output_ball'], state['points'],
                          state['labels'], state['markers'], state['image_region'])
    
    return state

def _world_radius_marker(center, radius, symbol, color, angle, scale):
    direction = _v((math.cos(angle), math.sin(angle), 0))
    endpoint = center + radius * direction
    label = _tex(symbol, endpoint + scale * PROOF['radius_label_gap'] * direction,
                 STYLE['small_size'] * scale, color)
    
    return VGroup(Line(center, endpoint, color = color, stroke_width = PROOF['radius_width']), label)

class _SceneSettings:
    def setup(self):
        super().setup()
        validate_parameters()
        self.camera.background_color = BG_COLOR
        self.camera.frame.set(width = FRAME_WIDTH, height = FRAME_HEIGHT).move_to(ORIGIN)

    def update_mobjects(self, dt):
        super().update_mobjects(dt)
        ratio = self.camera.frame.width / FRAME_WIDTH
        stroke_factor = ratio ** CAMERA_STYLE['stroke_exponent']
        visited = set()
        def adjust(mob):

            if id(mob) in visited:
                return
            
            visited.add(id(mob))

            if mob is self.camera.frame or getattr(mob, '_formula_object', False) or getattr(mob, '_formula_glyph', False):
                return
            if getattr(mob, '_screen_arrow', False) or getattr(mob, '_manual_zoom_stroke', False):
                return
            if isinstance(mob, VMobject) and mob.has_points():
                if not hasattr(mob, '_unzoomed_stroke_width'):
                    mob._unzoomed_stroke_width = float(mob.get_stroke_width())
                mob.set_stroke(width = mob._unzoomed_stroke_width * stroke_factor, family = False)

            for child in mob.submobjects:
                adjust(child)

        for mob in self.mobjects:
            adjust(mob)

    def beat(self, *animations, duration = None, pause_after = True, **kwargs):
        self.play(*animations, run_time = TIME_SCALE * (TIMING['reveal'] if duration is None else duration), **kwargs)

        if pause_after:
            self.pause(TIMING['animation_pause'])

    def pause(self, duration = None):
        seconds = TIME_SCALE * (TIMING['hold'] if duration is None else duration)
        self.wait(max(seconds, STYLE['minimum_hold_frames'] / float(config.frame_rate)))

    def settle(self, group):

        for mob in tuple(self.mobjects):
            mob.clear_updaters(recursive = True)

        self.remove(*tuple(self.mobjects))
        self.add(group)
        self.pause(TIMING['join_hold'])

    def camera_motion(self, center, width):
        frame = self.camera.frame
        start_center, start_width = frame.get_center().copy(), frame.width
        stop_center = _v(center)

        def interpolate_camera(mob, alpha):
            amount = _motion_ease(alpha)
            current_width = math.exp((1 - amount) * math.log(start_width) + amount * math.log(width))
            mob.set(width = current_width).move_to((1 - amount) * start_center + amount * stop_center)

        return UpdateFromAlphaFunc(frame, interpolate_camera, rate_func = linear)

    def pin_mapping_arrow(self, arrow_group):
        # 同一根映射箭头在推镜时滑到下方，完整地留在画面内
        # 图标和区域的世界坐标不变；只有箭头作为映射指示随镜头排布
        arrow_group._screen_arrow = True
        line, label = arrow_group
        reference_height = label.height

        def follow_camera(group):
            ratio = self.camera.frame.width / FRAME_WIDTH
            zoom = math.log(max(1, 1 / ratio)) / math.log(CAMERA_STYLE['arrow_zoom_reference'])
            amount = _motion_ease(min(1, zoom))
            y = (1 - amount) * MAPPING['arrow_start'][1] + amount * CAMERA_STYLE['arrow_zoom_y']
            x = amount * CAMERA_STYLE['arrow_zoom_x']
            half = (1 - amount) * abs(MAPPING['arrow_start'][0]) + amount * CAMERA_STYLE['arrow_zoom_half_length']
            center = self.camera.frame.get_center()
            line.become(Arrow(center + ratio * _v((x - half, y, 0)), center + ratio * _v((x + half, y, 0)),
                              buff = 0, color = PALETTE['axis'], stroke_width = MAPPING['arrow_width'] * ratio,
                              tip_length = MAPPING['arrow_tip'] * ratio))
            label.set_height(reference_height * ratio)
            label.move_to(center + ratio * _v((x, y + CAMERA_STYLE['arrow_label_gap'], 0)))
            _outline_formula(label, STYLE['label_outline'] * ratio)

        arrow_group.add_updater(follow_camera, call_updater = True)

        return arrow_group

    def pin_formula(self, formula, position):
        # 只有字形的纯黑描边；不创建任何矩形、底板或不透明填充
        reference_height = getattr(formula, '_hud_reference_height', formula.height)
        formula._hud_reference_height = reference_height
        formula.clear_updaters()

        def follow_camera(mob):
            ratio = self.camera.frame.width / FRAME_WIDTH
            mob.set_height(reference_height * ratio)
            mob.move_to(self.camera.frame.get_center() + ratio * _v(position))
            _outline_formula(mob, STYLE['label_outline'] * ratio)

        formula.add_updater(follow_camera, call_updater = True)

        return formula

    def footer(self, value, color = None):

        return self.pin_formula(_tex(value, STYLE['footer'], color = color), STYLE['footer'])

    def formula_change(self, old, new):
        old.clear_updaters(recursive = True)
        new.clear_updaters(recursive = True)

        return ReplacementTransform(old, new, rate_func = _motion_ease)

    def travel_samples(self, local, delta):
        _, _, source_center, target_center = _mapping_geometry()
        source_points, moving, paths = VGroup(), VGroup(), []

        for index, fraction in enumerate(PROOF['sample_fractions']):
            point = local + delta * _v((*fraction, 0))
            start, end = source_center + point, target_center + _map_local(point)
            source_points.add(_dot(start, radius = PROOF['sample_radius'] * PROOF['label_world_scale']))
            moving.add(source_points[-1].copy())
            lift = PROOF['travel_lift'] * (1 if index % 2 == 0 else -1) * UP
            paths.append(CubicBezier(start, start + PROOF['travel_handle'] * RIGHT + lift,
                                     end - PROOF['travel_handle'] * RIGHT + lift, end))
            
        self.beat(FadeIn(source_points), duration = TIMING['short_hold'])
        self.add(moving)
        self.beat(LaggedStart(*[MoveAlongPath(point, path) for point, path in zip(moving, paths)],
                               lag_ratio = PROOF['sample_lag']),
                  self.camera_motion(target_center, PROOF['target_zoom_width']), duration = TIMING['travel'])
        self.pause(TIMING['hold'])
        self.beat(FadeOut(source_points), *[FadeOut(point) for point in moving], duration = TIMING['fade'])
        self.remove(source_points, *source_points, moving, *moving)

class ContinuityToOpenPreimages(_SceneSettings, MovingCameraScene):
    # 先移镜定位再直接放大，原箭头与 f 随场景一同放大

    def _keep_set_labels(self, stage):
        _, _, source_center, target_center = _mapping_geometry()
        source_label, target_label = stage['labels'][1], stage['labels'][0]
        source_height, target_height = source_label.height, target_label.height
        reference_ratio = FIRST_SCENE['zoom_width'] / FRAME_WIDTH

        def follow_sets(mob):
            ratio = self.camera.frame.width / FRAME_WIDTH
            amount = np.clip(math.log(max(1, 1 / ratio)) / math.log(1 / reference_ratio), 0, 1)
            source_offset = (1 - amount) * _v(MAPPING['source_label_offset']) + amount * _v(FIRST_SCENE['source_zoom_label_offset'])
            source_label.set_height(source_height * ratio).move_to(source_center + source_offset)
            target_gap = MAPPING['target_label_offset'][1] - MAPPING['target_radius']
            target_label.set_height(target_height * ratio)
            target_label.move_to(target_center + _v((0, MAPPING['target_radius'] + ratio * target_gap, 0)))
            _outline_formula(source_label, STYLE['label_outline'] * ratio)
            _outline_formula(target_label, STYLE['label_outline'] * ratio)

        stage['labels'].add_updater(follow_sets, call_updater = True)

    def _keep_initial_focus_size(self, state):
        # x_0 从全景起便使用放大后的视觉尺寸；首次推镜结束时恢复原几何
        point, label = state['points'][0], state['labels'][0]
        reference_ratio = FIRST_SCENE['zoom_width'] / FRAME_WIDTH
        point_height, label_height = point.height / reference_ratio, label.height / reference_ratio

        def follow_point(mob):
            mob.set_height(point_height * self.camera.frame.width / FRAME_WIDTH)

        def follow_label(mob):
            ratio = self.camera.frame.width / FRAME_WIDTH
            mob.set_height(label_height * ratio)
            mob.move_to(point.get_center() + ratio * _v(PROOF['label_offset']))
            _outline_formula(mob, STYLE['label_outline'] * ratio)

        point.add_updater(follow_point, call_updater = True)
        label.add_updater(follow_label, call_updater = True)

    def _proof_footer(self, value, color = None):
        position = FIRST_SCENE['formula_position']

        return self.pin_formula(_tex(value, position, color = color), position)

    def construct(self):
        previous = previous_final_stage()
        self.add(previous)
        self.pause(TIMING['join_hold'])
        stage = _overview_stage()

        # 原箭头和 f 保持世界坐标与尺寸，随镜头自然移动和放大
        arrow_group = stage['base'][2]
        arrow_group._world_mapping_arrow = True
        arrow_group._manual_zoom_stroke = True
        arrow_group[0].set_z_index(FIRST_SCENE['arrow_z'])
        self._keep_set_labels(stage)
        self._first_stage = stage
        header = self.pin_formula(_tex(FORMULAS['forward'], STYLE['header']), STYLE['header'])
        header[0].set_color(PALETTE['pale_yellow'])
        header[2].set_color(PALETTE['green'])
        self.beat(FadeOut(previous[:-1]), self.formula_change(previous[-1], header),
                  FadeIn(stage['base']), duration = TIMING['bridge'])
        self.pin_formula(header, STYLE['header'])
        self.beat(FadeIn(stage['target_region']), Write(stage['labels'][0]), duration = TIMING['output_request'])
        unit = FIRST_SCENE['probe_units'][0]
        state = _first_local_geometry(unit)
        self._first_state = state
        self._keep_initial_focus_size(state)
        self.beat(FadeIn(stage['regions']), Write(stage['labels'][1]),
                  FadeIn(state['points'][0]), FadeIn(state['labels'][0]), duration = TIMING['input_response'])
        self.add(stage['labels'])

        # 先在原画幅移动到输出侧合适的取景位置，再在该位置平滑放大
        # 取景范围同时容纳整个箭头和输出邻域，不抽出任何小区域
        self.beat(self.camera_motion(FIRST_SCENE['output_view_center'], FRAME_WIDTH),
                  duration = FIRST_SCENE['reposition_time'])
        self.beat(self.camera_motion(FIRST_SCENE['output_view_center'], FIRST_SCENE['zoom_width']),
                  duration = TIMING['zoom'])
        state['points'][0].clear_updaters()
        state['labels'][0].clear_updaters()
        output_formula = self._proof_footer(FORMULAS['forward_output'], PALETTE['pale_yellow'])
        self.beat(FadeIn(state['points'][1]), FadeIn(state['labels'][1]), FadeIn(state['output_ball']),
                  Create(state['markers'][1]), Write(output_formula), duration = TIMING['output_request'])
        self.pause(TIMING['hold'])
        self.beat(self.camera_motion(FIRST_SCENE['input_view_center'], FIRST_SCENE['zoom_width']),
                  duration = TIMING['camera_pan'])
        input_formula = self._proof_footer(FORMULAS['forward_input'], PALETTE['green'])
        self.beat(FadeIn(state['input_ball']), Create(state['markers'][0]),
                  self.formula_change(output_formula, input_formula), duration = TIMING['input_response'])
        self.pin_formula(input_formula, FIRST_SCENE['formula_position'])
        moving_region = _first_neighborhood_region(unit, 0)
        self.add(moving_region)
        def map_entire_region(mob, alpha):
            mob.become(_first_neighborhood_region(unit, alpha))
        self.beat(UpdateFromAlphaFunc(moving_region, map_entire_region, rate_func = _motion_ease),
                  self.camera_motion(FIRST_SCENE['output_view_center'], FIRST_SCENE['zoom_width']),
                  duration = FIRST_SCENE['region_travel'])
        self.remove(moving_region)
        self.add(state['image_region'])
        self.pause(TIMING['hold'])
        self.beat(self.camera_motion(FIRST_SCENE['input_view_center'], FIRST_SCENE['zoom_width']),
                  duration = TIMING['camera_pan'])
        previous_unit = unit

        for unit in FIRST_SCENE['probe_units'][1:]:
            start_unit, end_unit = np.array(previous_unit), np.array(unit)
            def update_neighborhood(mob, alpha, start = start_unit, stop = end_unit):
                mob.become(_first_local_geometry((1 - alpha) * start + alpha * stop)['all'])
            self.beat(UpdateFromAlphaFunc(state['all'], update_neighborhood), duration = TIMING['point_move'])
            previous_unit = unit
            self.pause(TIMING['short_hold'])

        result = self._proof_footer(FORMULAS['forward_result'])
        self.beat(self.formula_change(input_formula, result), duration = TIMING['formula'])
        self.pin_formula(result, FIRST_SCENE['formula_position'])
        self.pause(TIMING['long_hold'])
        final_position = FIRST_SCENE['final_formula_position']
        final_formula = self.pin_formula(_tex(FORMULAS['overview_bottom'], final_position), final_position)
        self.beat(self.formula_change(VGroup(header, result), final_formula), duration = TIMING['formula'])
        self.pin_formula(final_formula, final_position)
        self.beat(self.camera_motion(ORIGIN, FRAME_WIDTH), FadeOut(state['all']), duration = TIMING['zoom'])
        self.settle(_overview_join())
        self.pause(TIMING['long_hold'])

class OpenPreimagesToContinuity(_SceneSettings, MovingCameraScene):
    # 从第一镜原位反向推导，整块邻域随映射进入 U，再直接推近接第三镜

    def _keep_set_labels(self, stage):
        _, _, source_center, _ = _mapping_geometry()
        source_label, target_label = stage['labels'][1], stage['labels'][0]
        source_height, target_height = source_label.height, target_label.height
        reference_ratio = SECOND_SCENE['zoom_width'] / FRAME_WIDTH

        def follow_sets(mob):
            ratio = self.camera.frame.width / FRAME_WIDTH
            amount = np.clip(math.log(max(1, 1 / ratio)) / math.log(1 / reference_ratio), 0, 1)
            offset = (1 - amount) * _v(MAPPING['source_label_offset']) + amount * _v(SECOND_SCENE['source_zoom_label_offset'])
            source_label.set_height(source_height * ratio).move_to(source_center + offset)
            chosen = stage['target_region']
            gap = MAPPING['target_label_offset'][1] - MAPPING['target_radius']
            target_label.set_height(target_height * ratio)
            target_label.move_to(chosen.get_center() + UP * (chosen.height / 2 + ratio * gap))
            _outline_formula(source_label, STYLE['label_outline'] * ratio)
            _outline_formula(target_label, STYLE['label_outline'] * ratio)

        stage['labels'].add_updater(follow_sets, call_updater = True)

    def _keep_initial_focus_size(self, state):
        point, label = state['points'][0], state['labels'][0]
        reference_ratio = SECOND_SCENE['zoom_width'] / FRAME_WIDTH
        point_height, label_height = point.height / reference_ratio, label.height / reference_ratio

        def follow_point(mob):
            mob.set_height(point_height * self.camera.frame.width / FRAME_WIDTH)

        def follow_label(mob):
            ratio = self.camera.frame.width / FRAME_WIDTH
            mob.set_height(label_height * ratio)
            mob.move_to(point.get_center() + ratio * _v(PROOF['label_offset']))
            _outline_formula(mob, STYLE['label_outline'] * ratio)

        point.add_updater(follow_point, call_updater = True)
        label.add_updater(follow_label, call_updater = True)

    def _proof_footer(self, value, color = None):
        position = SECOND_SCENE['formula_position']

        return self.pin_formula(_tex(value, position, color = color), position)

    def _map_neighborhood(self, state, unit, epsilon):
        # 此时镜头已在输入侧，移除画外的旧像，避免新像到达时填充重叠
        self.remove(state['image_region'])
        moving_region = _second_neighborhood_region(unit, epsilon, 0)
        self.add(moving_region)
        def map_entire_region(mob, alpha):
            mob.become(_second_neighborhood_region(unit, epsilon, alpha))
        self.beat(UpdateFromAlphaFunc(moving_region, map_entire_region, rate_func = _motion_ease),
                  self.camera_motion(SECOND_SCENE['output_view_center'], SECOND_SCENE['zoom_width']),
                  duration = SECOND_SCENE['region_travel'])
        self.remove(moving_region)
        self.add(state['image_region'])

    def construct(self):
        # 与第一镜结尾共用同一构图；图标、V 及原像均原位延续
        stage = _overview_stage()
        previous = VGroup(stage['all'], _tex(FORMULAS['overview_bottom'], FIRST_SCENE['final_formula_position']))
        self.add(previous)
        self.pause(TIMING['join_hold'])
        self._second_stage = stage
        arrow_group = stage['base'][2]
        arrow_group._world_mapping_arrow = True
        arrow_group._manual_zoom_stroke = True
        arrow_group[0].set_z_index(SECOND_SCENE['arrow_z'])
        self._keep_set_labels(stage)
        header = self.pin_formula(_tex(FORMULAS['backward'], STYLE['header']), STYLE['header'])
        header[0].set_color(PALETTE['green'])
        header[2].set_color(PALETTE['pale_yellow'])
        self.beat(self.formula_change(previous[-1], header), duration = TIMING['bridge'])
        self.pin_formula(header, STYLE['header'])
        unit = SECOND_SCENE['probe_unit']
        epsilon = SECOND_SCENE['epsilon_values'][0]
        state = _second_local_geometry(unit, epsilon)
        self._second_state = state
        self._keep_initial_focus_size(state)
        self.beat(FadeIn(state['points'][0]), FadeIn(state['labels'][0]), duration = TIMING['input_response'])
        self.beat(self.camera_motion(SECOND_SCENE['output_view_center'], FRAME_WIDTH),
                  duration = SECOND_SCENE['reposition_time'])
        self.beat(self.camera_motion(SECOND_SCENE['output_view_center'], SECOND_SCENE['zoom_width']),
                  duration = TIMING['zoom'])
        state['points'][0].clear_updaters()
        state['labels'][0].clear_updaters()
        chosen, regions = stage['target_region'], stage['regions']
        mapped_center = state['points'][1].get_center()
        output_formula = self._proof_footer(FORMULAS['backward_output'], PALETTE['cyan'])
        output_label = _tex('U', stage['labels'][0].get_center(), color = PALETTE['cyan'])
        self.beat(Transform(chosen, _disk(mapped_center, epsilon, PALETTE['cyan']), rate_func = _motion_ease),
                  Transform(stage['labels'][0], output_label, rate_func = _motion_ease),
                  FadeIn(state['points'][1]), FadeIn(state['labels'][1]),
                  Create(state['markers'][1]), Write(output_formula), duration = TIMING['output_request'])
        self.pause(TIMING['hold'])
        input_label = _tex(r'f^{-1}(U)', stage['labels'][1].get_center(), MAPPING['region_label_size'], PALETTE['green'])
        self.beat(Transform(regions, VGroup(_second_preimage_region(unit, epsilon)), rate_func = _motion_ease),
                  Transform(stage['labels'][1], input_label, rate_func = _motion_ease), duration = TIMING['input_response'])
        self.beat(self.camera_motion(SECOND_SCENE['input_view_center'], SECOND_SCENE['zoom_width']),
                  duration = TIMING['camera_pan'])
        input_formula = self._proof_footer(FORMULAS['backward_input'], PALETTE['green'])
        self.beat(FadeIn(state['input_ball']), Create(state['markers'][0]),
                  self.formula_change(output_formula, input_formula), duration = TIMING['input_response'])
        self.pin_formula(input_formula, SECOND_SCENE['formula_position'])
        self.pause(TIMING['hold'])
        self._map_neighborhood(state, unit, epsilon)
        result = self._proof_footer(FORMULAS['backward_result'])
        self.beat(self.formula_change(input_formula, result), duration = TIMING['formula'])
        self.pin_formula(result, SECOND_SCENE['formula_position'])
        self.pause(TIMING['hold'])

        # epsilon 连续缩小，U、其完整原像和整个 delta 邻域一同连续响应
        for next_epsilon in SECOND_SCENE['epsilon_values'][1:]:
            response = VGroup(chosen, regions, state['all'])
            start_epsilon = epsilon

            def shrink_request(mob, alpha, start = start_epsilon, stop = next_epsilon):
                current = (1 - alpha) * start + alpha * stop
                mob[0].become(_disk(mapped_center, current, PALETTE['cyan']))
                mob[1].become(VGroup(_second_preimage_region(unit, current)))
                mob[2].become(_second_local_geometry(unit, current)['all'])

            self.beat(UpdateFromAlphaFunc(response, shrink_request, rate_func = _motion_ease),
                      duration = TIMING['radius_change'])
            epsilon = next_epsilon
            self.beat(self.camera_motion(SECOND_SCENE['input_view_center'], SECOND_SCENE['zoom_width']),
                      duration = TIMING['camera_pan'])
            self.pause(TIMING['hold'])
            self._map_neighborhood(state, unit, epsilon)
            self.pause(TIMING['hold'])

        quantifiers = self.pin_formula(_tex(FORMULAS['reverse_quantifier'], STYLE['header']), STYLE['header'])
        self.beat(self.formula_change(header, quantifiers), duration = TIMING['formula'])
        self.pin_formula(quantifiers, STYLE['header'])
        self.pause(TIMING['long_hold'])

        # 直接继续推近原收藏中的 U，末帧与第三镜共享同一开圆盘构图
        stage['labels'].clear_updaters()
        ratio = epsilon / TOPO_START['radius']
        final_camera_center = mapped_center - ratio * _v(TOPO_START['center'])
        match_stage = operations_start_stage().scale(ratio, about_point = ORIGIN).shift(final_camera_center)

        for item in match_stage.get_family():
            item._manual_zoom_stroke = True

        for shape in match_stage.family_members_with_points():
            shape.set_stroke(width = shape.get_stroke_width() * ratio)
            shape.set_stroke(width = shape.get_stroke_width(background = True) * ratio, background = True)

        output_focus = VGroup(state['points'][1], state['labels'][1])
        proof_details = VGroup(state['input_ball'], state['markers'], state['image_region'],
                               state['points'][0], state['labels'][0])
        self.beat(FadeOut(stage['base']), FadeOut(regions), FadeOut(stage['labels']),
                  FadeOut(proof_details), duration = TIMING['fade'])
        self.beat(ReplacementTransform(chosen, match_stage[0], rate_func = _motion_ease),
                  ReplacementTransform(output_focus, VGroup(match_stage[1][1], match_stage[1][2]), rate_func = _motion_ease),
                  FadeIn(match_stage[1][0]), self.formula_change(VGroup(quantifiers, result), match_stage[2]),
                  self.camera_motion(final_camera_center, FRAME_WIDTH * ratio), duration = TIMING['zoom'])
        self.camera.frame.set(width = FRAME_WIDTH, height = FRAME_HEIGHT).move_to(ORIGIN)
        self.settle(operations_start_stage())

def _prev_v(value):

    return np.array(value, dtype = float)

def _prev_tex(value, position = None, size = None, color = None, width = None):
    parts = value if isinstance(value, (tuple, list)) else (value,)
    mob = MathTex(*parts, font_size = PREV_STYLE['formula_size'] if size is None else size,
                  color = PREV_PALETTE['ink'] if color is None else color)
    limit = PREV_STYLE['formula_width'] if width is None else width

    if mob.width > limit:
        mob.scale_to_fit_width(limit)

    if position is not None:
        mob.move_to(_prev_v(position))

    # 仅字形路径描边；所有无路径的公式分组保持完全透明
    mob.set_background_stroke(width = 0, opacity = 0)

    for glyph in mob.family_members_with_points():
        glyph.set_stroke(color = PREV_STYLE['label_outline_color'], width = PREV_STYLE['label_outline'],
                         opacity = 1, background = True, family = False)
        
    return _outline_formula(mob, PREV_STYLE['label_outline']).set_z_index(PREV_STYLE['formula_z'])

def _prev_final_formula_outline(formula):

    return _outline_formula(formula, PREV_PREIMAGE['final_formula_outline_width']).set_z_index(PREV_STYLE['foreground_formula_z'])

def _prev_dot(position, color = None, radius = None):

    return Dot(_prev_v(position), radius = PREV_STYLE['dot_radius'] if radius is None else radius,
               color = PREV_PALETTE['pale_yellow'] if color is None else color).set_z_index(PREV_STYLE['point_z'])

def _prev_open_dot(position, color = None, radius = None):

    return Circle(radius = PREV_STYLE['open_radius'] if radius is None else radius,
                  stroke_color = PREV_PALETTE['ink'] if color is None else color,
                  stroke_width = PREV_STYLE['open_width'], fill_color = PREV_BG_COLOR,
                  fill_opacity = 1).move_to(_prev_v(position)).set_z_index(PREV_STYLE['point_z'])

def _prev_guide(start, end, color = None, opacity = None):

    return DashedLine(_prev_v(start), _prev_v(end), color = PREV_PALETTE['ink'] if color is None else color,
                      stroke_width = PREV_STYLE['guide_width'], dash_length = PREV_STYLE['dash_length'],
                      dashed_ratio = PREV_STYLE['boundary_ratio']).set_stroke(
                          opacity = PREV_STYLE['guide_opacity'] if opacity is None else opacity)

def _prev_gradient_color(t, colors):
    t = np.clip(float(t), 0, 1) * (len(colors) - 1)
    i = min(int(t), len(colors) - 2)

    return interpolate_color(ManimColor(colors[i]), ManimColor(colors[i + 1]), t - i)

def _prev_path(points, color, width):
    result = VMobject(stroke_color = color, stroke_width = width, fill_opacity = 0)
    result.set_points_smoothly(np.array(points))

    return result

def _prev_number_tex(value):
    rounded = round(value)

    if abs(value - rounded) < PREV_STYLE['numeric_tolerance']:
        return str(rounded)
    
    return f"{value:g}"

def _prev_root_tex(value):
    root = math.sqrt(value)
    rounded = round(root)

    if abs(root - rounded) < PREV_STYLE['numeric_tolerance']:
        return str(rounded)
    
    return r"\sqrt{" + _prev_number_tex(value) + "}"

def _prev_preimage_formula():
    a, b = (_prev_root_tex(PREV_PREIMAGE[key]) for key in ('range_low', 'range_high'))

    return r"f^{-1}(V)=(-" + b + ",-" + a + r")\cup(" + a + "," + b + ")"

def _prev_graph_curve(axes, start, stop, colors, width):
    segments = VGroup()
    bounds = np.linspace(start, stop, PREV_STYLE['curve_segments'] + 1)

    for i, (a, b) in enumerate(zip(bounds[:-1], bounds[1:])):
        samples = np.linspace(a, b, PREV_STYLE['samples_per_segment'])
        points = [axes.c2p(x, x * x) for x in samples]
        segments.add(_prev_path(points, _prev_gradient_color(i / (len(bounds) - 2), colors), width))

    return segments

def _prev_preimage_stage():
    p = PREV_PREIMAGE
    axes = Axes(x_range = p['x_range'], y_range = p['y_range'], x_length = p['x_length'],
                y_length = p['y_length'], tips = False,
                axis_config = dict(color = PREV_PALETTE['axis'], stroke_width = PREV_STYLE['axis_width'], include_ticks = False))
    axes.shift(_prev_v(p['origin']) - axes.c2p(0, 0))

    # 坐标变换仍由原Axes计算；把显示用的两根白色轴延伸至画面之外
    axes.x_axis.set_stroke(opacity = 0)
    axes.y_axis.set_stroke(opacity = 0)
    half_x = PREV_FRAME_WIDTH / 2 + PREV_STYLE['axis_overhang']
    half_y = PREV_FRAME_HEIGHT / 2 + PREV_STYLE['axis_overhang']
    vertical_axis = Line([p['origin'][0], -half_y, 0], [p['origin'][0], half_y, 0],
                         color = PREV_PALETTE['axis'], stroke_width = PREV_STYLE['axis_width'])
    axes.add(Line([-half_x, p['origin'][1], 0], [half_x, p['origin'][1], 0],
                  color = PREV_PALETTE['axis'], stroke_width = PREV_STYLE['axis_width']), vertical_axis)
    ticks = VGroup()

    for x in p['x_ticks']:
        if x == 0:
            continue
        point = axes.c2p(x, 0)
        ticks.add(Line(point + p['tick_half_length'] * UP, point + p['tick_half_length'] * DOWN,
                       color = PREV_PALETTE['axis'], stroke_width = PREV_STYLE['axis_width']))
        ticks.add(_prev_tex(_prev_number_tex(x), point + p['x_tick_label_gap'] * DOWN, p['tick_size']))

    ticks.add(_prev_tex('0', _prev_v(p['origin']) + _prev_v(p['origin_label_offset']), p['tick_size']))

    for y in p['y_ticks']:
        point = axes.c2p(0, y)
        ticks.add(Line(point + p['tick_half_length'] * LEFT, point + p['tick_half_length'] * RIGHT,
                       color = PREV_PALETTE['axis'], stroke_width = PREV_STYLE['axis_width']))
        ticks.add(_prev_tex(_prev_number_tex(y), point + p['y_tick_label_gap'] * LEFT, p['tick_size']))

    graph = _prev_graph_curve(axes, *p['graph_domain'], p['gradient'], PREV_STYLE['curve_width'])
    low, high = p['range_low'], p['range_high']

    # 中间这一根白色纵轴同时承载蓝色输出区间，不再重复创建右侧数轴
    output_position = lambda y: axes.c2p(0, y)
    height = output_position(high)[1] - output_position(low)[1]
    output_fill = Rectangle(width = 2 * p['output_half_width'], height = height, stroke_width = 0,
                            fill_color = PREV_PALETTE['blue'], fill_opacity = p['output_band_opacity'])
    output_fill.move_to((output_position(low) + output_position(high)) / 2)
    output_line = Line(output_position(low), output_position(high), color = PREV_PALETTE['blue'],
                       stroke_width = PREV_STYLE['interval_width'])
    output_ends = VGroup(*[_prev_open_dot(output_position(y), PREV_PALETTE['blue']) for y in (low, high)])
    x_left, x_right = p['x_range'][0], p['x_range'][1]
    graph_fill = Rectangle(width = axes.c2p(x_right, 0)[0] - axes.c2p(x_left, 0)[0],
                           height = height, stroke_width = 0, fill_color = PREV_PALETTE['blue'],
                           fill_opacity = p['graph_band_opacity'])
    graph_fill.move_to((axes.c2p(x_left, low) + axes.c2p(x_right, high)) / 2).set_z_index(PREV_STYLE['band_z'])
    band_edges = VGroup(*[_prev_guide(axes.c2p(x_left, y), axes.c2p(x_right, y), PREV_PALETTE['blue'])
                          for y in (low, high)])
    f_header = _prev_tex(PREV_FORMULAS['function'], p['f_position'], p['f_size'])
    v_header = _prev_tex("V=(" + _prev_number_tex(low) + "," + _prev_number_tex(high) + ")",
                    p['v_position'], p['v_size'], PREV_PALETTE['blue'])
    a, b = math.sqrt(low), math.sqrt(high)
    intervals = VGroup(*[Line(axes.c2p(left, 0), axes.c2p(right, 0), color = PREV_PALETTE['green'],
                              stroke_width = PREV_STYLE['interval_width']) for left, right in ((-b, -a), (a, b))])
    input_ends = VGroup(*[_prev_open_dot(axes.c2p(x, 0), PREV_PALETTE['green']) for x in (-b, -a, a, b)])
    selected = VGroup(*[_prev_graph_curve(axes, left, right, (PREV_PALETTE['green'], PREV_PALETTE['mint']),
                                    p['selected_curve_width']) for left, right in ((-b, -a), (a, b))])
    selected_ends = VGroup(*[_prev_open_dot(axes.c2p(x, x * x), PREV_PALETTE['green']) for x in (-b, -a, a, b)])
    input_formula = _prev_final_formula_outline(_prev_tex(_prev_preimage_formula(), p['input_formula_position'],
                                                p['input_formula_size'], PREV_PALETTE['green']))
    
    return dict(axes = axes, vertical_axis = vertical_axis, ticks = ticks, graph = graph,
                output_fill = output_fill, output_line = output_line, output_ends = output_ends,
                output_position = output_position, graph_fill = graph_fill, band_edges = band_edges,
                f_header = f_header, v_header = v_header, intervals = intervals, input_ends = input_ends,
                selected = selected, selected_ends = selected_ends, input_formula = input_formula)

def previous_final_stage():
    stage = _prev_preimage_stage()
    criterion = _prev_tex(PREV_FORMULAS['criterion'], PREV_STYLE['header'])
    criterion[2].set_color(PREV_PALETTE['blue'])
    criterion[3].set_color(PREV_PALETTE['green'])
    criterion = _prev_final_formula_outline(criterion)

    return VGroup(
        stage['output_fill'], stage['output_line'], stage['output_ends'],
        stage['axes'], stage['ticks'], stage['graph'],
        stage['graph_fill'], stage['band_edges'], stage['input_ends'],
        stage['intervals'], stage['selected'], stage['selected_ends'],
        stage['input_formula'], criterion,
    )

def _topo_formula(value, position = None, size = None, color = None):
    p = TOPO_STYLE
    label = _tex(value, position = p['header'] if position is None else position,
                 size = p['formula_size'] if size is None else size,
                 color = PALETTE['ink'] if color is None else color,
                 width = p['formula_width'])
    label.set_z_index(p['formula_z'])

    return label

def _topo_open_region(center, radius, color, opacity = None):
    p = TOPO_STYLE
    fill = Circle(radius = radius, stroke_width = 0,
                  fill_color = color,
                  fill_opacity = p['fill_opacity'] if opacity is None else opacity).move_to(_v(center))
    fill.set_z_index(p['fill_z'])
    outline = Circle(radius = radius, color = color, stroke_width = p['edge_width']).move_to(_v(center))
    edge = DashedVMobject(outline, num_dashes = p['edge_dashes'], dashed_ratio = p['dash_ratio'])
    edge.set_z_index(p['edge_z'])

    return VGroup(fill, edge)

def _topo_probe(position, radius, color = None, with_label = True):
    p = TOPO_STYLE
    color = PALETTE['green'] if color is None else color
    region = _topo_open_region(position, radius, color, p['local_opacity'])
    point = _dot(position, PALETTE['pale_yellow'], p['point_radius']).set_z_index(p['point_z'])
    objects = [region, point]

    if with_label:
        label = _topo_formula(TOPO_OPERATIONS['point_label'],
                              _v(position) + _v(TOPO_OPERATIONS['union_label_offset']),
                              p['small_formula_size'], PALETTE['pale_yellow'])
        objects.append(label)

    return VGroup(*objects)

def _topo_intersection_probe(position):
    p, s = TOPO_OPERATIONS, TOPO_STYLE
    position = _v(position)
    radii = [p['local_radius_fraction'] * (p['radius'] - np.linalg.norm(position - _v(center)))
             for center in (p['left_center'], p['right_center'])]
    balls = VGroup()
    markers = VGroup()

    for index, (radius, color, angle) in enumerate(zip(radii, (PALETTE['cyan'], PALETTE['green']), p['local_radius_angles'])):
        balls.add(_topo_open_region(position, radius, color, s['local_opacity']))
        direction = np.array([math.cos(angle), math.sin(angle), 0])
        end = position + radius * direction
        markers.add(Line(position, end, color = color, stroke_width = s['local_width']),
                    _topo_formula(r'r_' + str(index + 1), end + s['local_label_gap'] * direction,
                                  s['small_formula_size'], color))
        
    point = _dot(position, PALETTE['pale_yellow'], s['point_radius']).set_z_index(s['point_z'])

    return VGroup(balls, markers, point)

def operations_start_stage():
    # 第二镜落幅与第三镜首帧共用：开圆盘、局部邻域与开集公式
    p = TOPO_START
    disk = _topo_open_region(p['center'], p['radius'], PALETTE['cyan'])
    local = _topo_open_region(p['point'], p['local_radius'], PALETTE['green'], TOPO_STYLE['local_opacity'])
    point = _dot(p['point'], PALETTE['pale_yellow'], TOPO_STYLE['point_radius']).set_z_index(TOPO_STYLE['point_z'])
    label = _topo_formula(TOPO_OPERATIONS['point_label'],
                          _v(p['point']) + _v(p['label_offset']),
                          TOPO_STYLE['small_formula_size'], PALETTE['pale_yellow'])
    formula = _topo_formula(p['formula'], p['formula_position'])

    return VGroup(disk, VGroup(local, point, label), formula)

def _topo_universe():
    p, s = TOPO_OPERATIONS, TOPO_STYLE
    frame = RoundedRectangle(width = p['universe_width'], height = p['universe_height'],
                             corner_radius = p['universe_corner'], color = PALETTE['axis'],
                             stroke_width = s['edge_width'], fill_color = PALETTE['cyan'],
                             fill_opacity = s['universe_fill']).move_to(_v(p['universe_center']))
    label = _topo_formula(r"X", p['universe_label'], s['set_label_size'])

    return VGroup(frame, label)

def _topo_binary_region(kind):
    # 用两条圆弧构造真实并集/交集边界，不依赖可选的布尔几何库
    p, s = TOPO_OPERATIONS, TOPO_STYLE
    c1, c2, radius = _v(p['left_center']), _v(p['right_center']), p['radius']
    half_distance = (c2[0] - c1[0]) / 2
    angle = math.acos(half_distance / radius)

    if kind == 'union':
        ranges = ((c1, angle, TAU - angle), (c2, PI + angle, 3 * PI - angle))
    else:
        ranges = ((c1, -angle, angle), (c2, PI - angle, PI + angle))

    points = []

    for center, start, stop in ranges:
        points.extend(center + radius * np.array([math.cos(t), math.sin(t), 0])
                      for t in np.linspace(start, stop, s['arc_samples']))
        
    points.append(points[0])
    fill = VMobject(stroke_width = 0, fill_color = PALETTE['pale_yellow'],
                    fill_opacity = s['emphasis_fill'])
    fill.set_points_as_corners(points).set_z_index(s['fill_z'])
    outline = VMobject(color = PALETTE['pale_yellow'], stroke_width = s['region_width'])
    outline.set_points_as_corners(points)
    edge = DashedVMobject(outline, num_dashes = s['edge_dashes'], dashed_ratio = s['dash_ratio'])
    edge.set_z_index(s['edge_z'])

    return VGroup(fill, edge)

def _topo_interval(n, color = None):
    p, s = TOPO_NESTED, TOPO_STYLE
    color = PALETTE['cyan'] if color is None else color
    half = p['unit'] / n
    left, right = np.array([-half, s['axis_y'], 0]), np.array([half, s['axis_y'], 0])
    body = Line(left, right, color = color, stroke_width = p['interval_width']).set_z_index(s['edge_z'])
    endpoints = VGroup()

    for point in (left, right):
        endpoint = Circle(radius = s['endpoint_radius'], color = color,
                          stroke_width = s['endpoint_width'], fill_color = BG_COLOR,
                          fill_opacity = 1).move_to(point).set_z_index(s['point_z'])
        endpoints.add(endpoint)

    return VGroup(body, endpoints)

def _topo_n_counter(value):
    prefix = _topo_formula(r'n=', size = TOPO_STYLE['small_formula_size'])
    number = Integer(value, font_size = TOPO_STYLE['small_formula_size'],
                     color = PALETTE['ink'], group_with_commas = False)
    _outline_formula(number)
    number.set_z_index(TOPO_STYLE['formula_z'])

    return VGroup(prefix, number).arrange(RIGHT, buff = TOPO_NESTED['counter_gap'], aligned_edge = DOWN).move_to(_v(TOPO_NESTED['n_position']))

def operations_join_stage():
    # 合并后的第三镜：有数值刻度的实数轴与正宽度开区间
    p, s = TOPO_NESTED, TOPO_STYLE
    axis = Line([-s['line_half_width'], s['axis_y'], 0],
                [s['line_half_width'], s['axis_y'], 0],
                color = PALETTE['axis'], stroke_width = s['axis_width']).set_z_index(s['line_z'])
    ticks, numbers = VGroup(), VGroup()

    for value in p['tick_values']:
        half_height = s['tick_half_height'] * (1 if value in p['labelled_ticks'] else p['minor_tick_fraction'])
        x = p['unit'] * value
        ticks.add(Line([x, s['axis_y'] - half_height, 0], [x, s['axis_y'] + half_height, 0],
                       color = PALETTE['axis'], stroke_width = s['axis_width']).set_z_index(s['line_z']))
        if value in p['labelled_ticks']:
            numbers.add(_topo_formula(f'{value:g}', [x, s['tick_label_y'], 0], s['small_formula_size']))

    real = _topo_formula(r'\mathbb R', p['line_label_position'], s['small_formula_size'])
    interval = _topo_interval(p['initial_n'])
    formula = _topo_formula(p['finite_formula'], p['formula_position'])
    n_label = _topo_n_counter(p['initial_n'])

    return VGroup(axis, ticks, numbers, real, interval, formula, n_label)

def _topo_formula_path(mob):
    # 将三行字形的可见轮廓整体形变成符号，不用淡出替代收束
    glyphs = list(mob.family_members_with_points())
    path = VMobject()
    path.match_style(glyphs[0], family = False)

    for glyph in glyphs:
        path.append_vectorized_mobject(glyph)
    _outline_formula(path)

    return path.set_z_index(TOPO_END['foreground_z'])

class OpenSetOperations(_SceneSettings, MovingCameraScene):
    # 全集、空集、并与交、无限交反例，最终将三条性质收束为拓扑空间

    def construct(self):
        p, s, t = TOPO_OPERATIONS, TOPO_STYLE, TOPO_TIME
        start = operations_start_stage()
        self.add(start)
        self.pause(t['opening_hold'])
        self.beat(start[1].animate.shift(_v(TOPO_START['probe_shift'])), duration = t['scan'])
        self.pause(t['short_hold'])

        # 严格依照文案：先整个空间，再空集；此时尚未引入拓扑的符号
        universe = _topo_universe()
        axiom_header = _topo_formula(p['full_formula'])
        full = _topo_formula('X', p['central_label'], p['central_label_size'], PALETTE['cyan'])
        self.beat(ReplacementTransform(start[0], universe[0], rate_func = _motion_ease),
                  FadeOut(start[1]), self.formula_change(start[2], axiom_header), duration = t['bridge'])
        self.beat(GrowFromCenter(full),
                  universe[0].animate.set_fill(PALETTE['cyan'], opacity = s['emphasis_fill']), duration = t['full_reveal'])
        self.pause(t['full_hold'])
        empty_header = _topo_formula(p['empty_formula'])
        empty = _topo_formula(r'\varnothing', p['central_label'], p['central_label_size'])
        self.beat(ReplacementTransform(full, universe[1], rate_func = _motion_ease),
                  universe[0].animate.set_fill(opacity = s['universe_fill']), duration = t['full_release'])
        self.beat(GrowFromCenter(empty), self.formula_change(axiom_header, empty_header), duration = t['empty_reveal'])
        self.pause(t['empty_hold'])

        disks = VGroup(_topo_open_region(p['left_center'], p['radius'], PALETTE['cyan']),
                       _topo_open_region(p['right_center'], p['radius'], PALETTE['green']))
        labels = VGroup(*[_topo_formula(value, position, s['set_label_size'], color)
                          for value, position, color in zip(p['small_labels'], p['labels'],
                                                           (PALETTE['cyan'], PALETTE['green']))])
        formula = _topo_formula(p['union_formula'])
        self.beat(*[GrowFromCenter(disk) for disk in disks],
                  self.formula_change(VGroup(empty_header, empty), formula), duration = t['disks_reveal'])
        self.beat(*[Write(label) for label in labels], duration = t['labels_reveal'])
        union = _topo_binary_region('union')
        self.beat(FadeIn(union), disks.animate.set_stroke(opacity = s['dim_opacity']), duration = t['region_reveal'])
        probe = _topo_probe(p['union_probe_positions'][0], p['union_probe_radius'])
        self.beat(FadeIn(probe), duration = t['probe'])
        self.pause(t['probe_hold'])

        for position in p['union_probe_positions'][1:]:
            self.beat(Transform(probe, _topo_probe(position, p['union_probe_radius']), rate_func = _motion_ease),
                      duration = t['probe'])
            self.pause(t['probe_hold'])

        lens = _topo_binary_region('intersection')
        intersection_formula = _topo_formula(p['intersection_formula'])
        self.beat(ReplacementTransform(union, lens, rate_func = _motion_ease),
                  self.formula_change(formula, intersection_formula),
                  disks.animate.set_stroke(opacity = 1), FadeOut(probe), duration = t['intersection_reveal'])
        lens_probe = _topo_intersection_probe(p['lens_probe_positions'][0])
        minimum = _topo_formula(p['min_formula'], p['proof_position'], s['small_formula_size'], PALETTE['green'])
        self.beat(FadeIn(lens_probe), Write(minimum), duration = t['intersection_probe'])

        for position in p['lens_probe_positions'][1:]:
            self.beat(Transform(lens_probe, _topo_intersection_probe(position), rate_func = _motion_ease),
                      duration = t['intersection_probe'])
            
        self.pause(t['intersection_hold'])

        # 圆盘运算直接收束成有真实数值刻度的数轴，不再另起第四个 Scene
        stage = operations_join_stage()
        self.beat(ReplacementTransform(universe[0], stage[0], rate_func = _motion_ease),
                  ReplacementTransform(universe[1], stage[3], rate_func = _motion_ease),
                  FadeOut(disks), FadeOut(labels), FadeOut(lens), FadeOut(lens_probe),
                  self.formula_change(minimum, stage[6]), self.formula_change(intersection_formula, stage[5]),
                  duration = t['bridge'])
        self.beat(FadeIn(stage[1]), FadeIn(stage[2]), Create(stage[4][0]), FadeIn(stage[4][1]),
                  duration = t['interval_reveal'])
        self.settle(stage)
        nested = TOPO_NESTED
        current_n_label = stage[6]
        previous_n = nested['initial_n']

        for n in nested['n_values']:
            # 同一个连续进度同时驱动逐整数计数和 1/n 半径，不再扭曲整行数字
            def update_n(mob, alpha, start = previous_n, stop = n):
                value = (1 - alpha) * start + alpha * stop
                number = mob[0][1]
                integer_value = int(round(value))

                if number.get_value() != integer_value:
                    number.set_value(integer_value)
                    _outline_formula(number)
                    number.set_z_index(s['formula_z'])

                mob[0].arrange(RIGHT, buff = nested['counter_gap'], aligned_edge = DOWN).move_to(_v(nested['n_position']))
                mob[1].become(_topo_interval(value))

            self.beat(UpdateFromAlphaFunc(VGroup(current_n_label, stage[4]), update_n, rate_func = _motion_ease),
                      duration = t['shrink'], pause_after = False)
            previous_n = n
            self.pause(t['shrink_hold'])

        # 有限 n 仍为空心端点的正宽区间；明确进入极限后才留下黄色的 0
        limit_label = _topo_formula(nested['limit_formula'], nested['n_position'], s['small_formula_size'])
        intersection = _topo_formula(nested['intersection_formula'], nested['formula_position'])
        singleton = _dot([0, s['axis_y'], 0], PALETTE['pale_yellow'], s['point_radius']).set_z_index(s['point_z'])
        self.beat(self.formula_change(current_n_label, limit_label), self.formula_change(stage[5], intersection),
                  FadeOut(stage[4]), FadeIn(singleton),
                  Flash(singleton, color = PALETTE['pale_yellow'], flash_radius = nested['flash_radius'],
                        line_length = nested['flash_length'], num_lines = nested['flash_lines'],
                        line_stroke_width = nested['flash_width']), duration = t['singleton'])
        self.pause(t['singleton_hold'])
        nonopen = _topo_formula(nested['nonopen_formula'], nested['nonopen_position'], s['small_formula_size'], PALETTE['rose'])
        self.beat(Write(nonopen), duration = t['nonopen'])
        self.pause(t['short_hold'])

        # 停留在数轴上；只将现有画面压暗，沿用度量公理收束为符号的节奏
        backdrop = VGroup(stage[0], stage[1], stage[2], stage[3], limit_label, intersection, singleton, nonopen)
        dimmed = backdrop.copy()

        for shape in dimmed.family_members_with_points():
            shape.set_fill(opacity = shape.get_fill_opacity() * TOPO_END['backdrop_opacity'], family = False)
            shape.set_stroke(opacity = shape.get_stroke_opacity() * TOPO_END['backdrop_opacity'], family = False)
            shape.set_stroke(opacity = shape.get_stroke_opacity(background = True) * TOPO_END['backdrop_opacity'],
                             background = True, family = False)
            
        x_dim = _topo_formula('X', TOPO_END['x_position'], TOPO_END['x_size'], PALETTE['cyan'])
        x_dim.set_opacity(TOPO_END['x_opacity']).set_z_index(TOPO_END['foreground_z'])
        self.beat(Transform(backdrop, dimmed, rate_func = _motion_ease), FadeIn(x_dim), duration = t['summary_dim'])
        axioms = VGroup(*[_topo_formula(value, position, TOPO_END['axiom_size'], PALETTE[TOPO_END['axiom_color']])
                          for value, position in zip(TOPO_END['axiom_formulas'], TOPO_END['axiom_positions'])])
        axioms.set_z_index(TOPO_END['foreground_z'])
        self.beat(Write(axioms), duration = t['summary_write'])
        self.pause(t['summary_hold'])
        symbol = _topo_formula(r'\mathcal{T}', TOPO_END['symbol_position'], TOPO_END['symbol_size'], PALETTE['pale_yellow'])
        symbol.set_z_index(TOPO_END['foreground_z'])
        summary_path, symbol_path = _topo_formula_path(axioms), _topo_formula_path(symbol)
        self.remove(axioms)
        self.add(summary_path)
        self.beat(ReplacementTransform(summary_path, symbol_path, rate_func = _motion_ease), duration = t['summary_collapse'])
        self.remove(symbol_path)
        self.add(symbol)
        self.pause(t['symbol_hold'])
        pair = _topo_formula(('(', 'X', ',', r'\mathcal{T}', ')'), TOPO_END['pair_position'], TOPO_END['pair_size'])
        pair[1].set_color(PALETTE['cyan'])
        pair[3].set_color(PALETTE['pale_yellow'])
        pair.set_z_index(TOPO_END['foreground_z'])
        punctuation = VGroup(pair[0], pair[2], pair[4])
        self.beat(ReplacementTransform(x_dim, pair[1], rate_func = _motion_ease),
                  ReplacementTransform(symbol, pair[3], rate_func = _motion_ease),
                  Write(punctuation), duration = t['pair_build'])
        self.add(pair)
        self.pause(t['final_hold'])

def _contour_polygons(icon):
    polygons = []

    for subpath in icon.get_subpaths():
        samples = []

        for controls in subpath.reshape((-1, 4, 3)):

            for t in np.linspace(0, 1, MAPPING['contour_samples'], endpoint = False):
                samples.append((1 - t) ** 3 * controls[0] + 3 * (1 - t) ** 2 * t * controls[1]
                               + 3 * (1 - t) * t ** 2 * controls[2] + t ** 3 * controls[3])
                
        polygons.append(np.asarray(samples))

    return polygons

def _inside_polygon(point, polygon):
    x, y = point[:2]
    inside = False
    previous = polygon[-1]

    for current in polygon:
        ax, ay = previous[:2]
        bx, by = current[:2]

        if (ay > y) != (by > y):
            crossing = ax + (y - ay) * (bx - ax) / (by - ay)
            if x < crossing:
                inside = not inside

        previous = current

    return inside

def validate_parameters():
    # 不渲染也可调用；检查参数、小球包含关系以及同一个映射的样本
    if BG_COLOR != '#000012' or PALETTE['axis'] != '#FFFFFF':
        raise ValueError('请保持用户指定的背景与白色坐标轴。')
    if TIME_SCALE <= 0 or FRAME_WIDTH <= 0 or FRAME_HEIGHT <= 0:
        raise ValueError('时间比例与画幅尺寸必须为正。')
    if min(MAPPING['branch_x'], MAPPING['branch_y']) <= 0 or MAPPING['map_radius_cap'] <= 1:
        raise ValueError('椭圆半轴与径向压缩参数必须有效。')
    
    source, target, source_center, target_center = _mapping_geometry()
    source_polygons, target_polygons = _contour_polygons(source), _contour_polygons(target)

    for angle in np.linspace(0, TAU, MAPPING['containment_samples'], endpoint = False):
        unit = (math.cos(angle), math.sin(angle))
        point = source_center + _source_local(unit)

        if not any(_inside_polygon(point, polygon) for polygon in source_polygons):
            raise ValueError('完整原像的边界必须位于点赞掌部。')
        
        point = target_center + MAPPING['target_radius'] * MAPPING['map_radius_cap'] * _v((*unit, 0))
        
        if not any(_inside_polygon(point, polygon) for polygon in target_polygons):
            raise ValueError('映射的全部输出必须位于收藏轮廓内。')
        
    for unit in (*PROOF['probe_units'], *FIRST_SCENE['probe_units']):
        local = _source_local(unit)
        mapped = _map_local(local)
        epsilon = PROOF['epsilon_fraction'] * (MAPPING['target_radius'] - np.linalg.norm(mapped))

        if not epsilon > 0 or not np.linalg.norm(mapped) + epsilon < MAPPING['target_radius']:
            raise ValueError('输出 ε 球必须严格装在 V 内。')
        
        delta = _safe_delta(local, epsilon)

        for angle in np.linspace(0, TAU, MAPPING['containment_samples'], endpoint = False):
            point = local + delta * _v((math.cos(angle), math.sin(angle), 0))
            if np.linalg.norm(_map_local(point) - mapped) >= epsilon:
                raise ValueError('δ 球的像超出了 ε 球。')
            if not any(_inside_polygon(source_center + point, polygon) for polygon in source_polygons):
                raise ValueError('δ 球必须完整留在输入空间内。')
            
    for epsilon in PROOF['reverse_radii']:
        local = _source_local((0, 0))
        delta = _safe_delta(local, epsilon)

        for fraction in PROOF['sample_fractions']:
            point = local + delta * _v((*fraction, 0))
            if np.linalg.norm(_map_local(point)) >= epsilon:
                raise ValueError('逆向证明的样本必须落在任给的 U 中。')
            
    if any(np.linalg.norm(_v(fraction)) >= 1 for fraction in PROOF['sample_fractions']):
        raise ValueError('演示样本必须严格位于输入 δ 小球内部。')
    if any(np.linalg.norm(_map_local(_source_local(unit))) <= STYLE['numeric_tolerance'] for unit in FIRST_SCENE['probe_units']):
        raise ValueError('第一镜的 f(x_0) 必须偏离 V 的中心。')
    if not SECOND_SCENE['epsilon_values'] or min(SECOND_SCENE['epsilon_values']) <= 0:
        raise ValueError('第二镜的 epsilon 必须为正。')
    
    local = _source_local(SECOND_SCENE['probe_unit'])
    mapped = _map_local(local)
    cap = MAPPING['target_radius'] * MAPPING['map_radius_cap']

    for epsilon in np.linspace(min(SECOND_SCENE['epsilon_values']), max(SECOND_SCENE['epsilon_values']), MAPPING['contour_samples']):
        if np.linalg.norm(mapped) + epsilon >= cap:
            raise ValueError('第二镜输出球必须位于映射的可逆径向范围内。')
        
        delta = _safe_delta(local, epsilon)

        for angle in np.linspace(0, TAU, MAPPING['containment_samples'], endpoint = False):
            direction = _v((math.cos(angle), math.sin(angle), 0))
            output = mapped + epsilon * direction
            preimage = _inverse_map_local(output)

            if np.linalg.norm(_map_local(preimage) - output) > STYLE['numeric_tolerance']:
                raise ValueError('第二镜的完整原像必须使用同一个映射。')
            if not any(_inside_polygon(source_center + preimage, polygon) for polygon in source_polygons):
                raise ValueError('第二镜的完整原像必须留在点赞图标内。')
            if not any(_inside_polygon(target_center + output, polygon) for polygon in target_polygons):
                raise ValueError('第二镜的输出开球必须留在收藏图标内。')
            if np.linalg.norm(_map_local(local + delta * direction) - mapped) >= epsilon:
                raise ValueError('第二镜整个 delta 邻域的像必须留在 U 中。')
            
    return True
