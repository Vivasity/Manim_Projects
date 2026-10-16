from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from manim import *

# 参数区：画面、颜色、尺寸、轨迹、公式和全部镜头节奏
BACKGROUND = "#000012"
FRAME_HEIGHT, FRAME_WIDTH = 8.0, 128 / 9
TIME_SCALE, ACTION_PAUSE = 1.0, 0.8
SCENE_HEAD_HOLD, SCENE_TAIL_HOLD = 0.8, 2.0
FORMULA_RISE_DISTANCE = 0.28

PALETTE = {
    "axis": "#FFFFFF", "frame": "#FFFFFF", "arrow": "#FFFFFF",
    "cyan": "#70CDE8", "green": "#A3DCAF", "yellow": "#E9DD79",
    "rose": "#ED9BAA", "white": "#FFFFFF",
}

# 保留 thumbnail.py 的圆形、渐变和点数，仅将两圆上移到画面中央
CIRCLE_RADIUS = 1.8
CIRCLE_CENTERS = ((-3.0, 0.0, 0.0), (3.0, 0.0, 0.0))
CIRCLE_ARCS, CIRCLE_ARC_OVERLAP, CIRCLE_STROKE = 240, 0.002, 14.0
CIRCLE_DOTS, CIRCLE_DOT_RADIUS = 24, 0.11
CIRCLE_START_COLOR, CIRCLE_END_COLOR = BLUE_B, GREEN_B
CIRCLE_DIM_OPACITY, CIRCLE_HIGHLIGHT_OPACITY = 0.22, 1.0

CURVE_STROKE, CURVE_SEGMENTS = 5.2, 144
GRAPH_SEGMENTS = 2 * CURVE_SEGMENTS  # 左右各144段，与变换后的两支逐段对应
CURVE_SEGMENT_OVERLAP = 0.40  # 相邻段轻微重叠，消除Cairo抗锯齿造成的接缝
CURVE_COLORS = (PALETTE["cyan"], PALETTE["green"], PALETTE["yellow"])
AXIS_STROKE, AXIS_OPACITY, AXIS_TICK_SIZE = 2.1, 1.0, 0.055
PEN_RADIUS = 0.047
PEN_GLOW_RADII = (0.08, 0.13, 0.21)
PEN_GLOW_OPACITIES = (0.18, 0.075, 0.025)
PEN_COLOR, FORMULA_SIZE = PALETTE["white"], 45

# 平滑函数：幅度、频率、线性项；同一函数贯穿第2、4镜
FUNCTION_AMPLITUDE, FUNCTION_FREQUENCY, FUNCTION_SLOPE = 0.78, 1.18, 0.16
GRAPH_X_RANGE, GRAPH_Y_RANGE = (-4.5, 4.5, 1.0), (-2.3, 2.3, 1.0)
GRAPH_WIDTH, GRAPH_HEIGHT = 10.7, 4.7
GRAPH_CENTER = (0.0, -0.12, 0.0)
GRAPH_FORMULA_POSITION = (4.75, 2.68, 0.0)
STROKE_FORMULA = r"y=f(x)"

# 反比例函数与连续函数共用原来的坐标轴，公式中心也保持不动
RECIP_CUTOFF = 0.46
RECIP_FORMULA = r"f(x)=\frac{1}{x}"
RECIP_TRAVEL_START, RECIP_TRAVEL_END = 3.8, 0.64
RECIP_ROUND_TRIPS = 1  # 每支上的完整往返次数
RECIP_DOT_COLOR, RECIP_DOT_RADIUS = YELLOW, 0.075
ORIGIN_RING_RADIUS, ORIGIN_RING_STROKE = 0.065, 2.0
ORIGIN_RING_COLOR, ORIGIN_FLASH_COLOR = YELLOW, YELLOW
ORIGIN_FLASH_RADIUS, ORIGIN_FLASH_LINE_LENGTH = 0.20, 0.10
ORIGIN_FLASH_LINE_COUNT, ORIGIN_FLASH_STROKE = 14, 3.0

# 三个空间：框内下部专门给公式留白。先整幅画缩左，再中，再右
PANEL_WIDTH, PANEL_HEIGHT = 3.75, 4.05
PANEL_CENTERS = ((-4.38, 0.2, 0.0), (0.0, 0.2, 0.0), (4.38, 0.2, 0.0))
PANEL_CORNER, PANEL_STROKE = 0.12, 1.65
PANEL_FULL_WIDTH, PANEL_FULL_HEIGHT = 11.8, 6.25
PANEL_FULL_CENTER = (0.0, 0.0, 0.0)
PANEL_GRAPH_WIDTH, PANEL_GRAPH_HEIGHT = 3.10, 2.20
PANEL_GEOMETRY_Y, PANEL_LABEL_Y, PANEL_LABEL_SIZE = 0.40, -1.37, 40
PANEL_CONNECTOR_GAP, PANEL_CONNECTOR_STROKE, PANEL_CONNECTOR_TIP = 0.14, 1.8, 0.12
METRIC_FORMULA, TOPOLOGY_FORMULA = r"(X,d)", r"(X,\mathcal{T})"

# 同一平面里的两个度量例子：欧氏直线/圆，曼哈顿折线/菱形
# 网格只是坐标参考；这里展示R²上的两个度量，不把空间限制为交点集
METRIC_PLANE_CENTER_OFFSET = (0.0, 0.35, 0.0)
METRIC_GRID_RADIUS, METRIC_GRID_STEP = 3, 0.36
METRIC_GRID_STROKE, METRIC_GRID_OPACITY, METRIC_AXIS_STROKE = 0.7, 0.18, 1.5
METRIC_START, METRIC_END = (0.0, 0.0), (2.0, 1.0)
METRIC_ENDPOINT_RADIUS, METRIC_ENDPOINT_COLOR = 0.063, YELLOW
METRIC_PATH_STROKE = 3.2
METRIC_EUCLIDEAN_COLOR, METRIC_MANHATTAN_COLOR = PALETTE["cyan"], PALETTE["green"]
METRIC_BALL_STROKE, METRIC_BALL_FILL_OPACITY = 2.0, 0.045
METRIC_CURSOR_RADIUS, METRIC_CURSOR_COLOR = 0.035, PALETTE["white"]
CARPET_SIDE, CARPET_LEVELS, CARPET_CENTER_Y = 2.46, 4, 0.42
CARPET_FILL_COLOR, CARPET_EDGE_COLOR = PALETTE["green"], PALETTE["cyan"]
CARPET_EDGE_STROKE, CARPET_HOLE_OVERLAP = 1.2, 0.002

# 输入→输出：圆盘中逐渐加密的蓝点，对应绿点总是延迟相同时间出现
MAP_INPUT_CENTER, MAP_OUTPUT_CENTER = (-3.60, 0.30, 0.0), (3.60, 0.30, 0.0)
MAP_SHAPE_WIDTH, MAP_SHAPE_HEIGHT = 5.50, 5.10
MAP_OUTLINE_STROKE = 1.8
MAP_FILL_COLORS = ("#A9D9F4", "#BFE6C6")
MAP_FILL_OPACITY = 0.13
MAP_TARGET_INPUT, MAP_TARGET_OUTPUT = MAP_INPUT_CENTER, MAP_OUTPUT_CENTER
MAP_TARGET_RADIUS = 0.092
MAP_TARGET_OUTLINE_COLOR, MAP_TARGET_OUTLINE_STROKE = "#000000", 3.0
MAP_LABEL_SIZE = 32
MAP_TARGET_LABEL_OFFSETS = ((0.0, -0.36, 0.0), (0.20, -0.42, 0.0))
MAP_TARGET_LABEL_OUTLINE_COLOR, MAP_TARGET_LABEL_OUTLINE_STROKE = "#000000", 5.0
MAP_CLOUD_RADIUS = 0.60  # 原来1.80的三分之一；输出圆盘按映射比例同比缩小
MAP_CLOUD_COUNT = 60  # 每侧点数；每个绿点对应一个蓝点
MAP_CLOUD_DOT_RADIUS_RATIO = 0.7
MAP_CLOUD_DOT_RADIUS = MAP_TARGET_RADIUS * MAP_CLOUD_DOT_RADIUS_RATIO
MAP_CLOUD_COLORS = ("#63B9F4", "#8EE3A4")
MAP_CLOUD_OPACITY = 0.92  # 圆心附近的最大不透明度
MAP_CLOUD_EDGE_OPACITY = 0.18  # 圆盘边缘更淡，保留蓝/绿原色
MAP_CLOUD_FADE_POWER = 1.2
MAP_CLOUD_MIN_SPACING = 0.10  # 仅限制散点彼此间距，不避开目标点或字形
MAP_SPAWN_TIME_POWER = 0.46  # 0<p<1，出现时刻的间隔逐渐缩短
MAP_SPAWN_FADE_TIME, MAP_OUTPUT_DELAY = 0.32, 1.35  # 每个绿点相对对应蓝点的延迟（秒）
MAP_RANDOM_SEED, MAP_RANDOM_ATTEMPT_LIMIT = 20261005, 100000
MAP_OUTPUT_SCALE, MAP_OUTPUT_ROTATION = 0.9, 20 * DEGREES
MAP_ARROW_START, MAP_ARROW_END = (-0.65, 0.30, 0.0), (0.65, 0.30, 0.0)
MAP_ARROW_STROKE, MAP_ARROW_TIP = 2.4, 0.18
MAP_F_POSITION = (0.0, 0.96, 0.0)
MAP_FUNCTION_SYMBOL = "f"
MAP_TARGET_LABELS = (r"x_0", r"f(x_0)")
MAP_FORMULA_POSITION = (0.0, 0.0, 0.0)
MAP_FORMULA_SIZE = 84  # 最初42号公式的2倍，约占画面宽度68%
MAP_FORMULA_PARTS = (r"x\to x_0", r"\Longrightarrow", r"f(x)\to f(x_0)")
MAP_QUESTION_SYMBOL, MAP_QUESTION_SIZE, MAP_QUESTION_COLOR = "?", 130, "#FF6677"
MAP_QUESTION_OFFSET = (0.0, 0.0, 0.0)  # 直接叠在推出符号中心，靠图层盖住白色笔画
MAP_QUESTION_OUTLINE_STROKE = 5.0
MAP_DIM_OPACITY = 0.68
MAP_TARGET_Z_INDEX, MAP_TARGET_LABEL_Z_INDEX, MAP_CLOUD_Z_INDEX = 4, 5, 2
MAP_DIM_Z_INDEX, MAP_FORMULA_Z_INDEX, MAP_QUESTION_Z_INDEX = 8, 10, 11

# 每个数字都是秒；以下字典是配音对齐时主要要修改的部分
TIMING = {
    "01": dict(appear = 2.8, hold = 1.2, focus_left = 0.8, left_hold = 2.4, focus_right = 0.8, right_hold = 2.6, settle = 0.7),
    "02": dict(axes = 1.0, draw = 3.8, formula = 0.8, hold = 1.5, morph = 2.3),
    "03": dict(
        axes = 1.0, branches = 2.4, formula = 0.8, point_in = 0.45, travel = 2.2, branch_switch = 0.35, hold = 1.2, clean = 0.65, origin_ring = 0.6, flash = 1.0
    ),
    "04": dict(
        axes = 1.0, draw = 2.8, frame = 0.7, shrink = 2.0, left_hold = 0.5, center_frame = 0.65,
        points = 0.8, distance = 0.8, euclidean_walk = 2.4, metric_change = 1.4, manhattan_walk = 2.4,
        metric_label = 0.7, metric_hold = 0.7, right_frame = 0.8, square = 0.7, carpet_level = 0.85,
        carpet_pause = 0.15, topology_label = 0.8
    ),
    "05": dict(regions = 1.2, targets = 0.9, mapping = 0.9, populate = 14.0, cloud_hold = 1.4, dim = 1.0,formula = 1.0, question = 0.65, hold = 2.6),
}

# 不覆盖命令行的分辨率和帧率，也不继承封面脚本的save_last_frame
config.background_color = BACKGROUND
config.frame_height = FRAME_HEIGHT
config.frame_width = FRAME_WIDTH

# 可复用几何对象（下方没有需要为日常调色/调速而修改的参数）
def p(value):

    return np.asarray(value, dtype = float)

def smooth_function(x):

    return FUNCTION_AMPLITUDE * np.sin(FUNCTION_FREQUENCY * x) + FUNCTION_SLOPE * x

def colored_path(point_function, start, end, width = CURVE_STROKE, segments = CURVE_SEGMENTS):
    # 分段三次路径，颜色连续；数学对象始终为向量图形
    colors = color_gradient(CURVE_COLORS, segments)
    values = np.linspace(start, end, segments + 1)
    result = VGroup()
    for index, (a, b) in enumerate(zip(values[:-1], values[1:])):
        segment = VMobject(stroke_color = colors[index], stroke_width = width)
        extended_end = min(end, b + CURVE_SEGMENT_OVERLAP * (b - a))
        segment.set_points_smoothly([point_function(t) for t in np.linspace(a, extended_end, 4)])
        result.add(segment)

    return result

def thumbnail_circles():
    continuous, dotted = VGroup(), VGroup()

    for i in range(CIRCLE_ARCS):
        theta = TAU * i / CIRCLE_ARCS
        color = interpolate_color(CIRCLE_START_COLOR, CIRCLE_END_COLOR, (np.cos(theta) + 1) / 2)
        continuous.add(
            Arc(
                radius = CIRCLE_RADIUS, start_angle = theta,
                angle = TAU / CIRCLE_ARCS + CIRCLE_ARC_OVERLAP,
                stroke_color = color, stroke_width = CIRCLE_STROKE).shift(p(CIRCLE_CENTERS[0])
            )
        )

    for i in range(CIRCLE_DOTS):
        theta = TAU * i / CIRCLE_DOTS
        color = interpolate_color(CIRCLE_START_COLOR, CIRCLE_END_COLOR, (np.cos(theta) + 1) / 2)
        dotted.add(
            Dot(p(CIRCLE_CENTERS[1]) + CIRCLE_RADIUS * p((np.cos(theta), np.sin(theta), 0)),
            radius = CIRCLE_DOT_RADIUS, color = color)
        )

    return VGroup(continuous, dotted)

def pen_at(point, color = PEN_COLOR):
    glow = VGroup(*[Dot(point, radius = radius, color = color).set_opacity(opacity) for radius, opacity in zip(PEN_GLOW_RADII, PEN_GLOW_OPACITIES)])
    glow.add(Dot(point, radius = PEN_RADIUS, color = color))

    return glow.set_z_index(8)

def axes_for(x_range, y_range, width, height, center):
    axes = Axes(
        x_range = x_range, y_range = y_range, x_length = width, y_length = height,
        tips = False, axis_config = dict(color = PALETTE["axis"], stroke_width = AXIS_STROKE,
        tick_size = AXIS_TICK_SIZE, include_numbers = False)
    )

    return axes.move_to(p(center)).set_opacity(AXIS_OPACITY)

@dataclass
class GraphStage:
    axes: Axes
    curve: VGroup
    formula: MathTex

    @property
    def group(self):

        return VGroup(self.axes, self.curve, self.formula)

def ordinary_graph():
    axes = axes_for(GRAPH_X_RANGE, GRAPH_Y_RANGE, GRAPH_WIDTH, GRAPH_HEIGHT, GRAPH_CENTER)
    curve = colored_path(lambda x: axes.c2p(x, smooth_function(x)), *GRAPH_X_RANGE[:2], segments = GRAPH_SEGMENTS)
    formula = MathTex(STROKE_FORMULA, font_size = FORMULA_SIZE, color = PALETTE["white"])
    formula.move_to(p(GRAPH_FORMULA_POSITION))

    return GraphStage(axes, curve, formula)

@dataclass
class ReciprocalStage:
    axes: Axes
    branches: VGroup
    formula: MathTex

    @property
    def group(self):

        return VGroup(self.axes, self.branches, self.formula)

def reciprocal_graph(axes = None):

    if axes is None:
        axes = axes_for(GRAPH_X_RANGE, GRAPH_Y_RANGE, GRAPH_WIDTH, GRAPH_HEIGHT, GRAPH_CENTER)
    branches = VGroup(
        *[colored_path(lambda x: axes.c2p(x, 1 / x), a, b)
        for a, b in ((GRAPH_X_RANGE[0], -RECIP_CUTOFF), (RECIP_CUTOFF, GRAPH_X_RANGE[1]))]
    )

    formula = MathTex(RECIP_FORMULA, font_size = FORMULA_SIZE, color = PALETTE["white"])
    formula.move_to(p(GRAPH_FORMULA_POSITION))

    return ReciprocalStage(axes, branches, formula)

def panel_frame(center, full = False):

    return RoundedRectangle(
        width = PANEL_FULL_WIDTH if full else PANEL_WIDTH,
        height = PANEL_FULL_HEIGHT if full else PANEL_HEIGHT,
        corner_radius = PANEL_CORNER, stroke_width = PANEL_STROKE,
        stroke_color = PALETTE["frame"], stroke_opacity = 1, fill_opacity = 0
    ).move_to(p(center))

def panel_label(tex, center):

    return MathTex(
        tex, font_size = PANEL_LABEL_SIZE, color = PALETTE["white"]
    ).move_to(p(center) + PANEL_LABEL_Y * UP)

def curve_panel():
    center = p(PANEL_CENTERS[0])
    axes = axes_for(GRAPH_X_RANGE, GRAPH_Y_RANGE, PANEL_GRAPH_WIDTH, PANEL_GRAPH_HEIGHT, center + PANEL_GEOMETRY_Y * UP)
    curve = colored_path(lambda x: axes.c2p(x, smooth_function(x)), *GRAPH_X_RANGE[:2], segments = GRAPH_SEGMENTS)

    return VGroup(panel_frame(center), axes, curve, panel_label(STROKE_FORMULA, center))

def metric_path(vertices, color):

    return VMobject(
        stroke_color = color, stroke_width = METRIC_PATH_STROKE
    ).set_points_as_corners(vertices).set_z_index(3)

def metric_route_vertices(axes):
    start, end = METRIC_START, METRIC_END
    corner = (end[0], start[1])

    return tuple(axes.c2p(*point) for point in (start, corner, end))

def polyline_point(vertices, progress):
    # 按真实弧长走折线，使转弯前后的移动速度一致
    lengths = np.linalg.norm(np.diff(np.array(vertices), axis = 0), axis = 1)
    remaining = float(np.clip(progress, 0, 1)) * lengths.sum()

    for start, end, length in zip(vertices[:-1], vertices[1:], lengths):
        if length <= np.finfo(float).eps:
            continue
        if remaining <= length:
            return interpolate(start, end, remaining / length)
        remaining -= length

    return vertices[-1]

def metric_geometry():
    center = p(PANEL_CENTERS[1]) + p(METRIC_PLANE_CENTER_OFFSET)
    extent = METRIC_GRID_RADIUS * METRIC_GRID_STEP
    limits = (-METRIC_GRID_RADIUS, METRIC_GRID_RADIUS, 1)
    axes = axes_for(limits, limits, 2 * extent, 2 * extent, center)
    axes.set_stroke(width = METRIC_AXIS_STROKE).set_z_index(2)
    grid = VGroup()

    for index in range(-METRIC_GRID_RADIUS, METRIC_GRID_RADIUS + 1):
        if index == 0:
            continue
        for start, end in (((index, -METRIC_GRID_RADIUS), (index, METRIC_GRID_RADIUS)),
                           ((-METRIC_GRID_RADIUS, index), (METRIC_GRID_RADIUS, index))):
            grid.add(Line(axes.c2p(*start), axes.c2p(*end), color = PALETTE["white"],
                          stroke_width = METRIC_GRID_STROKE, stroke_opacity = METRIC_GRID_OPACITY))
            
    start, end = axes.c2p(*METRIC_START), axes.c2p(*METRIC_END)
    endpoints = VGroup(
        *[Dot(point, radius = METRIC_ENDPOINT_RADIUS, color = METRIC_ENDPOINT_COLOR) for point in (start, end)]
    ).set_z_index(5)
    straight = metric_path((start, end), METRIC_EUCLIDEAN_COLOR)
    euclidean_radius = np.linalg.norm(end - start)
    circle = Circle(
        radius = euclidean_radius, stroke_color = METRIC_EUCLIDEAN_COLOR,
        stroke_width = METRIC_BALL_STROKE, fill_color = METRIC_EUCLIDEAN_COLOR,
        fill_opacity = METRIC_BALL_FILL_OPACITY
    ).move_to(start).set_z_index(1)
    route = metric_path(metric_route_vertices(axes), METRIC_MANHATTAN_COLOR)
    manhattan_radius = np.abs(end - start).sum()
    diamond = Polygon(
        *[start + manhattan_radius * direction for direction in (RIGHT, UP, LEFT, DOWN)],
        stroke_color = METRIC_MANHATTAN_COLOR, stroke_width = METRIC_BALL_STROKE,
        fill_color = METRIC_MANHATTAN_COLOR, fill_opacity = METRIC_BALL_FILL_OPACITY
    ).set_z_index(1)
    
    return VGroup(grid, axes, endpoints, straight, circle, route, diamond)

def carpet_geometry():
    # 正方形减去各层中央开方块；4层只有585个孔，不创建4096个剩余小方块
    center = p(PANEL_CENTERS[2]) + CARPET_CENTER_Y * UP
    base = Square(
        side_length = CARPET_SIDE, stroke_width = CARPET_EDGE_STROKE,
        stroke_color = CARPET_EDGE_COLOR, fill_color = CARPET_FILL_COLOR, fill_opacity = 1
    )
    base.move_to(center)
    cells = [(center, CARPET_SIDE)]
    layers = VGroup()

    for _ in range(CARPET_LEVELS):
        layer = VGroup()
        next_cells = []

        for cell_center, side in cells:
            child_side = side / 3
            hole = Square(
                side_length = child_side + CARPET_HOLE_OVERLAP, stroke_width = 0,
                fill_color = BACKGROUND, fill_opacity = 1
            ).move_to(cell_center)
            layer.add(hole)

            for ix in (-1, 0, 1):
                for iy in (-1, 0, 1):
                    if ix or iy:
                        next_cells.append((cell_center + child_side * p((ix, iy, 0)), child_side))
        
        layers.add(layer)
        cells = next_cells

    return VGroup(base, layers)

def panel_connectors():
    arrows = VGroup()

    for a, b in zip(PANEL_CENTERS[:-1], PANEL_CENTERS[1:]):
        start = p(a) + RIGHT * (PANEL_WIDTH / 2 + PANEL_CONNECTOR_GAP)
        end = p(b) + LEFT * (PANEL_WIDTH / 2 + PANEL_CONNECTOR_GAP)
        arrows.add(
            Arrow(
                start, end, buff = 0, color = PALETTE["arrow"],
                stroke_width = PANEL_CONNECTOR_STROKE, tip_length = PANEL_CONNECTOR_TIP,
                max_tip_length_to_length_ratio = 1 / 3
            ).set_opacity(1)
        )
        
    return arrows

def three_panels():
    left = curve_panel()
    center = VGroup(panel_frame(PANEL_CENTERS[1]), metric_geometry(), panel_label(METRIC_FORMULA, PANEL_CENTERS[1]))
    right = VGroup(panel_frame(PANEL_CENTERS[2]), carpet_geometry(), panel_label(TOPOLOGY_FORMULA, PANEL_CENTERS[2]))

    return VGroup(left, center, right, panel_connectors())

def map_displacement(vector):
    v = np.asarray(vector, dtype = float)
    cosine, sine = np.cos(MAP_OUTPUT_ROTATION), np.sin(MAP_OUTPUT_ROTATION)
    rotation = np.array(((cosine, -sine), (sine, cosine)))

    return MAP_OUTPUT_SCALE * (rotation @ v)

def map_shell():
    domains = VGroup(*[
        Ellipse(
            width = MAP_SHAPE_WIDTH, height = MAP_SHAPE_HEIGHT,
            stroke_color = PALETTE["frame"], stroke_width = MAP_OUTLINE_STROKE, stroke_opacity = 1,
            fill_color = color, fill_opacity = MAP_FILL_OPACITY
        ).move_to(p(center))
        for center, color in zip((MAP_INPUT_CENTER, MAP_OUTPUT_CENTER), MAP_FILL_COLORS)
    ])
    arrow = Arrow(
        p(MAP_ARROW_START), p(MAP_ARROW_END), buff = 0, tip_length = MAP_ARROW_TIP,
        color = PALETTE["arrow"], stroke_width = MAP_ARROW_STROKE
    ).set_opacity(1)
    label = MathTex(MAP_FUNCTION_SYMBOL, font_size = FORMULA_SIZE, color = PALETTE["white"]).move_to(p(MAP_F_POSITION))

    return VGroup(domains, arrow, label)

def map_targets():
    targets = VGroup(
        *[Dot(p(center), radius = MAP_TARGET_RADIUS, color = PALETTE["yellow"])
        for center in (MAP_TARGET_INPUT, MAP_TARGET_OUTPUT)]
    )
    targets.set_z_index(MAP_TARGET_Z_INDEX)
    targets.set_stroke(MAP_TARGET_OUTLINE_COLOR, width = MAP_TARGET_OUTLINE_STROKE, opacity = 1, background = True)
    labels = VGroup(
        *[MathTex(tex, font_size = MAP_LABEL_SIZE, color = PALETTE["yellow"])
        for tex in MAP_TARGET_LABELS]
    ).set_z_index(MAP_TARGET_LABEL_Z_INDEX)

    for label, target, offset in zip(labels, (MAP_TARGET_INPUT, MAP_TARGET_OUTPUT), MAP_TARGET_LABEL_OFFSETS):
        label.move_to(p(target) + p(offset))
        label.set_stroke(
            MAP_TARGET_LABEL_OUTLINE_COLOR, width = MAP_TARGET_LABEL_OUTLINE_STROKE,
            opacity = 1, background = True
        )

    return VGroup(targets, labels)

def map_cloud_positions():
    # 整个圆盘内随机取样，不为目标/文字挖空；统一映射得到对应绿点
    rng = np.random.default_rng(MAP_RANDOM_SEED)
    centers = (p(MAP_TARGET_INPUT), p(MAP_TARGET_OUTPUT))
    displacements = []

    # 缩小映射的输出侧更密；输入的最小间距相应增大
    spacing = MAP_CLOUD_MIN_SPACING / min(1.0, MAP_OUTPUT_SCALE)

    for _ in range(MAP_RANDOM_ATTEMPT_LIMIT):
        radius = MAP_CLOUD_RADIUS * np.sqrt(rng.random())
        angle = rng.uniform(0, TAU)
        delta = radius * np.array((np.cos(angle), np.sin(angle)))
        if displacements and np.any(np.linalg.norm(np.array(displacements) - delta, axis = 1) < spacing):
            continue
        displacements.append(delta)
        if len(displacements) == MAP_CLOUD_COUNT:
            inputs = np.array([centers[0] + p((*delta, 0)) for delta in displacements])
            outputs = np.array([centers[1] + p((*map_displacement(delta), 0)) for delta in displacements])
            return inputs, outputs
        
    raise ValueError("圆盘无法容纳设定点数：请减少点数/间距或增大圆盘半径")

def map_clouds():

    return VGroup(*[
        VGroup(
            *[Dot(point, radius = MAP_CLOUD_DOT_RADIUS, color = color,
            fill_opacity = 0, stroke_width = 0) for point in points]
        )
        for points, color in zip(map_cloud_positions(), MAP_CLOUD_COLORS)
    ]).set_z_index(MAP_CLOUD_Z_INDEX)

def map_spawn_times():
    # 同一序号的两点相差固定时间；相邻生成间隔严格缩短
    inputs = TIMING["05"]["populate"] * np.linspace(0, 1, MAP_CLOUD_COUNT) ** MAP_SPAWN_TIME_POWER

    return inputs, inputs + MAP_OUTPUT_DELAY

def map_cloud_reveal(clouds):
    birth_times = np.concatenate(map_spawn_times())
    duration = float(birth_times[-1] + MAP_SPAWN_FADE_TIME)
    points = [dot for cloud in clouds for dot in cloud]

    # 两侧按各自圆盘半径归一化，保证对应点深浅相同；越远离目标越淡
    radial_fractions = np.concatenate([
        np.array([np.linalg.norm(dot.get_center() - p(center)) / radius for dot in cloud])
        for cloud, center, radius in zip(
            clouds, (MAP_TARGET_INPUT, MAP_TARGET_OUTPUT),
            (MAP_CLOUD_RADIUS, MAP_CLOUD_RADIUS * MAP_OUTPUT_SCALE)
        )
    ])
    final_opacities = MAP_CLOUD_EDGE_OPACITY + (MAP_CLOUD_OPACITY - MAP_CLOUD_EDGE_OPACITY) * (1 - np.clip(radial_fractions, 0, 1)) ** MAP_CLOUD_FADE_POWER
    previous = np.full(len(points), -1.0)

    def reveal(group, alpha):
        ages = np.clip((alpha * duration - birth_times) / MAP_SPAWN_FADE_TIME, 0, 1)
        opacities = final_opacities * ages * ages * (3 - 2 * ages)

        # 完全显示后保持不变，每帧只更新正在出现的少数点
        for index in np.flatnonzero(np.abs(opacities - previous) > np.finfo(float).eps):
            points[index].set_fill(opacity = float(opacities[index]))
        previous[:] = opacities

    return UpdateFromAlphaFunc(clouds, reveal, rate_func = linear), duration

def map_formula():
    formula = MathTex(*MAP_FORMULA_PARTS, font_size = MAP_FORMULA_SIZE, color = PALETTE["white"])
    formula[0].set_color(MAP_CLOUD_COLORS[0])
    formula[2].set_color(MAP_CLOUD_COLORS[1])

    return formula.move_to(p(MAP_FORMULA_POSITION)).set_z_index(MAP_FORMULA_Z_INDEX)

def map_question(formula):
    question = MathTex(MAP_QUESTION_SYMBOL, font_size = MAP_QUESTION_SIZE, color = MAP_QUESTION_COLOR)
    question.move_to(formula[1].get_center() + p(MAP_QUESTION_OFFSET))
    question.set_stroke(BACKGROUND, width = MAP_QUESTION_OUTLINE_STROKE, background = True)

    return question.set_z_index(MAP_QUESTION_Z_INDEX)

class PrefaceTools:
    # 统一调节速度、剪辑停顿及公式上浮；本身不是可渲染Scene
    def setup(self):
        super().setup()
        self.camera.background_color = BACKGROUND

        if TIME_SCALE <= 0 or CARPET_LEVELS < 1 or CIRCLE_DOTS < 3 or CURVE_SEGMENTS < 2:
            raise ValueError("TIME_SCALE > 0; CARPET_LEVELS >= 1; CIRCLE_DOTS >= 3; CURVE_SEGMENTS >= 2")
        if MAP_CLOUD_COUNT < 2 or MAP_CLOUD_RADIUS <= 0 or MAP_OUTPUT_SCALE <= 0:
            raise ValueError("MAP_CLOUD_COUNT >= 2; MAP_CLOUD_RADIUS > 0; MAP_OUTPUT_SCALE > 0")
        if not 0 < MAP_SPAWN_TIME_POWER < 1 or MAP_SPAWN_FADE_TIME <= 0 or MAP_OUTPUT_DELAY <= 0:
            raise ValueError("0 < MAP_SPAWN_TIME_POWER < 1; fade time and output delay > 0")
        if not 0 <= MAP_CLOUD_EDGE_OPACITY <= MAP_CLOUD_OPACITY <= 1 or MAP_CLOUD_FADE_POWER <= 0:
            raise ValueError("0 <= edge opacity <= center opacity <= 1; MAP_CLOUD_FADE_POWER > 0")
        if METRIC_GRID_RADIUS < 1 or METRIC_GRID_STEP <= 0:
            raise ValueError("METRIC_GRID_RADIUS >= 1; METRIC_GRID_STEP > 0")

    def play_for(self, seconds, *animations, pause_after = True, **kwargs):
        self.play(*animations, run_time = seconds * TIME_SCALE, **kwargs)

        if pause_after:
            self.hold(ACTION_PAUSE)

    def rise(self, formula):

        return FadeIn(formula, shift = FORMULA_RISE_DISTANCE * UP)

    def begin_shot(self):
        self.stage()
        self.hold(SCENE_HEAD_HOLD)

    def end_shot(self):
        self.hold(SCENE_TAIL_HOLD)

    def hold(self, seconds):

        if seconds > 0:
            self.wait(seconds * TIME_SCALE)

    def stage(self, *mobjects):
        # 只切换场景内容，不增加分镜之间的转场动画
        for mob in self.mobjects:
            mob.clear_updaters(recursive = True)

        self.clear()
        self.add(*mobjects)

    def draw_with_pen(self, curve, point_function, start, end, seconds):
        pen = pen_at(point_function(start))
        self.add(pen)
        self.play_for(
            seconds, Create(curve, lag_ratio = 1),
            UpdateFromAlphaFunc(pen, lambda mob, a: mob.move_to(point_function(interpolate(start, end, a)))), rate_func = linear
        )
        self.remove(pen)

# 镜头逻辑：画面中仅出现数学表达式，没有中文或英文叙述性字幕
def shot_two_circles(scene):
    t = TIMING["01"]
    circles = thumbnail_circles()
    scene.begin_shot()

    # 从各圆最右端出发，共用线性角进度，逆时针同时扫过一周
    circles[1].set_opacity(0)

    def reveal_dots(group, alpha):

        for index, dot in enumerate(group):
            dot.set_opacity(float(np.clip(alpha * CIRCLE_DOTS - index, 0, 1)))

    scene.play_for(t["appear"], Create(circles[0], lag_ratio = 1), UpdateFromAlphaFunc(circles[1], reveal_dots), rate_func = linear)
    scene.stage(circles)
    scene.hold(t["hold"])
    scene.play_for(t["focus_left"], circles[0].animate.set_stroke(opacity = CIRCLE_HIGHLIGHT_OPACITY), circles[1].animate.set_opacity(CIRCLE_DIM_OPACITY))
    scene.hold(t["left_hold"])
    scene.play_for(
        t["focus_right"], circles[0].animate.set_stroke(opacity = CIRCLE_DIM_OPACITY), circles[1].animate.set_opacity(CIRCLE_HIGHLIGHT_OPACITY)
    )
    scene.hold(t["right_hold"])
    scene.play_for(t["settle"], circles[0].animate.set_stroke(opacity = 1), circles[1].animate.set_opacity(1))
    scene.end_shot()

def shot_one_stroke(scene):
    # 第2镜：直接描画连续函数，随后原位变为两支反比例函数
    t = TIMING["02"]
    graph = ordinary_graph()
    scene.begin_shot()
    scene.play_for(t["axes"], Create(graph.axes))
    scene.draw_with_pen(graph.curve, lambda x: graph.axes.c2p(x, smooth_function(x)), *GRAPH_X_RANGE[:2], t["draw"])
    scene.play_for(t["formula"], scene.rise(graph.formula))
    scene.hold(t["hold"])
    reciprocal = reciprocal_graph(axes = graph.axes)
    reciprocal.formula.move_to(graph.formula.get_center())
    midpoint = len(graph.curve) // 2
    left_half, right_half = VGroup(*graph.curve[:midpoint]), VGroup(*graph.curve[midpoint:])
    scene.stage(graph.axes, left_half, right_half, graph.formula)

    # 两半分别变形，两支之间始终没有跨过零点的连接线
    scene.play_for(
        t["morph"], ReplacementTransform(left_half, reciprocal.branches[0]),
        ReplacementTransform(right_half, reciprocal.branches[1]),
        ReplacementTransform(graph.formula, reciprocal.formula)
    )
    animate_reciprocal_point(scene, reciprocal)
    scene.end_shot()

def shot_reciprocal(scene):
    # 可选的独立反比例素材，不在Preface连播中重复播放
    t = TIMING["03"]
    graph = reciprocal_graph()
    scene.begin_shot()
    scene.play_for(t["axes"], Create(graph.axes))
    scene.play_for(
        t["branches"], Create(graph.branches[0], lag_ratio = 1), Create(graph.branches[1], lag_ratio = 1)
    )
    scene.play_for(t["formula"], scene.rise(graph.formula))
    animate_reciprocal_point(scene, graph)
    scene.end_shot()

def animate_reciprocal_point(scene, graph):
    t = TIMING["03"]

    # 始终只有一个黄点；在不可见时切换到另一支，不画穿过x = 0的连接
    tracker = ValueTracker(-RECIP_TRAVEL_START)
    dot = Dot(graph.axes.c2p(tracker.get_value(), 1 / tracker.get_value()), radius = RECIP_DOT_RADIUS, color = RECIP_DOT_COLOR).set_z_index(3)
    dot.add_updater(lambda mob: mob.move_to(graph.axes.c2p(tracker.get_value(), 1 / tracker.get_value())))
    scene.play_for(t["point_in"], FadeIn(dot))

    for _ in range(RECIP_ROUND_TRIPS):
        scene.play_for(t["travel"], tracker.animate.set_value(-RECIP_TRAVEL_END), rate_func = smooth)
        scene.play_for(t["travel"], tracker.animate.set_value(-RECIP_TRAVEL_START), rate_func = smooth)

    scene.play_for(t["branch_switch"], FadeOut(dot))
    tracker.set_value(RECIP_TRAVEL_START)
    dot.update(0)
    scene.play_for(t["branch_switch"], FadeIn(dot))

    for _ in range(RECIP_ROUND_TRIPS):
        scene.play_for(t["travel"], tracker.animate.set_value(RECIP_TRAVEL_END), rate_func = smooth)
        scene.play_for(t["travel"], tracker.animate.set_value(RECIP_TRAVEL_START), rate_func = smooth)

    scene.hold(t["hold"])
    dot.clear_updaters()
    scene.play_for(t["clean"], FadeOut(dot))

    # 先显示空心标记，下一段动画才闪光；背景色填充用于遮住环内的轴线
    origin_ring = Circle(
        radius = ORIGIN_RING_RADIUS, stroke_color = ORIGIN_RING_COLOR,
        stroke_width = ORIGIN_RING_STROKE,
        fill_color = BACKGROUND, fill_opacity = 1
    ).move_to(graph.axes.c2p(0, 0))
    origin_ring.set_z_index(5)
    scene.play_for(t["origin_ring"], FadeIn(origin_ring))
    scene.play_for(
        t["flash"], Flash(graph.axes.c2p(0, 0), color = ORIGIN_FLASH_COLOR,
        flash_radius = ORIGIN_FLASH_RADIUS, line_length = ORIGIN_FLASH_LINE_LENGTH,
        num_lines = ORIGIN_FLASH_LINE_COUNT, line_stroke_width = ORIGIN_FLASH_STROKE)
    )

def animate_metric_examples(scene, metric, metric_label):
    # 同一对点量两种距离；运动点始终位于同步扩大的等距轮廓上
    t = TIMING["04"]
    grid, axes, endpoints, straight, circle, route, diamond = metric
    start, end = [dot.get_center() for dot in endpoints]
    scene.play_for(t["points"], Create(grid), Create(axes), FadeIn(endpoints))
    scene.play_for(t["distance"], Create(straight))
    cursor = Dot(start, radius = METRIC_CURSOR_RADIUS, color = METRIC_CURSOR_COLOR).set_z_index(6)
    scene.add(cursor)
    scene.play_for(
        t["euclidean_walk"], GrowFromPoint(circle, start),
        UpdateFromAlphaFunc(cursor, lambda mob, alpha: mob.move_to(interpolate(start, end, alpha))), rate_func = linear
    )
    scene.remove(cursor)

    # 保持端点，把直线折成唯一一条横竖路线；旧圆退场，菱形从起点重新长大
    scene.play_for(t["metric_change"], Transform(straight, route), FadeOut(circle))
    vertices = metric_route_vertices(axes)
    cursor.move_to(start)
    scene.add(cursor)
    scene.play_for(
        t["manhattan_walk"], GrowFromPoint(diamond, start),
        UpdateFromAlphaFunc(cursor, lambda mob, alpha: mob.move_to(polyline_point(vertices, alpha))), rate_func = linear
    )
    scene.remove(cursor)
    scene.play_for(t["metric_label"], scene.rise(metric_label))
    scene.hold(t["metric_hold"])

def shot_three_spaces(scene):
    t = TIMING["04"]
    graph = ordinary_graph()
    scene.begin_shot()
    scene.play_for(t["axes"], Create(graph.axes))
    scene.draw_with_pen(graph.curve, lambda x: graph.axes.c2p(x, smooth_function(x)), *GRAPH_X_RANGE[:2], t["draw"])
    frame = panel_frame(PANEL_FULL_CENTER, full = True)
    scene.play_for(t["frame"], Create(frame), scene.rise(graph.formula))
    large = VGroup(frame, graph.axes, graph.curve, graph.formula)
    panels = three_panels()

    # 同一个大画框及其全部内容同步缩小、移向左边；框形变给底部公式留白
    scene.play_for(t["shrink"], ReplacementTransform(large, panels[0]))
    scene.stage(panels[0])
    scene.hold(t["left_hold"])
    metric_frame, metric, metric_label = panels[1]
    scene.play_for(t["center_frame"], GrowArrow(panels[3][0]), Create(metric_frame))
    animate_metric_examples(scene, metric, metric_label)
    topo_frame, carpet, topo_label = panels[2]
    scene.play_for(t["right_frame"], GrowArrow(panels[3][1]), Create(topo_frame))
    scene.play_for(t["square"], DrawBorderThenFill(carpet[0]))

    for layer in carpet[1]:
        # 一层内的孔边长相同，各自在自己的中心同步长出，不做逐孔延迟
        scene.play_for(
            t["carpet_level"], AnimationGroup(*[GrowFromCenter(hole) for hole in layer], lag_ratio = 0)
        )
        scene.hold(t["carpet_pause"])
    
    scene.play_for(t["topology_label"], scene.rise(topo_label))
    scene.end_shot()

def shot_closeness(scene):
    t = TIMING["05"]
    shell, targets = map_shell(), map_targets()
    scene.begin_shot()
    scene.play_for(t["regions"], Create(shell[0]))
    scene.play_for(t["targets"], FadeIn(targets[0]), scene.rise(targets[1]))
    scene.play_for(t["mapping"], GrowArrow(shell[1]), scene.rise(shell[2]))
    clouds = map_clouds()
    reveal, duration = map_cloud_reveal(clouds)
    scene.add(clouds)
    scene.play_for(duration, reveal, rate_func = linear)
    scene.hold(t["cloud_hold"])

    # 同一层遮罩一起压暗区域、点集、黄点和标签；中央大公式在遮罩上层
    shade = Rectangle(
        width = FRAME_WIDTH, height = FRAME_HEIGHT, stroke_width = 0,
        fill_color = BACKGROUND, fill_opacity = MAP_DIM_OPACITY
    ).set_z_index(MAP_DIM_Z_INDEX)
    scene.play_for(t["dim"], FadeIn(shade), FadeOut(shell[1]), FadeOut(shell[2]))
    formula = map_formula()
    question = map_question(formula)
    scene.play_for(t["formula"], scene.rise(formula))
    scene.play_for(t["question"], scene.rise(question))
    scene.hold(t["hold"])
    scene.end_shot()

# 四个主分镜、一个可选反比例素材以及一个硬切连播预览
class TwoCircles(PrefaceTools, Scene):
    def construct(self):
        shot_two_circles(self)

class OneStroke(PrefaceTools, Scene):
    def construct(self):
        shot_one_stroke(self)

class Reciprocal(PrefaceTools, Scene):
    def construct(self):
        shot_reciprocal(self)

class ThreeSpaces(PrefaceTools, Scene):
    def construct(self):
        shot_three_spaces(self)

class Closeness(PrefaceTools, Scene):
    def construct(self):
        shot_closeness(self)

class Preface(PrefaceTools, Scene):
    def construct(self):
        for shot in (shot_two_circles, shot_one_stroke, shot_three_spaces, shot_closeness):
            shot(self)
