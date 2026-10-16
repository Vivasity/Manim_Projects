from __future__ import annotation
import importlib.util
from pathlib import Path
import sys
import numpy as np
from manim import *

# 全部可调参数
BG_COLOR = "#000012"
FRAME_WIDTH = 128 / 9
FRAME_HEIGHT = 8.0
FRAME_RATE = None                   # None 尊重命令行；可改为 60
TIME_SCALE = 1.0                    # 全部动作和停顿统一乘此值
REFERENCE_FILES = dict(preface = "preface.py", neighborhoods = "part_six.py")
PALETTE = dict(
    axis = "#FFFFFF", ink = "#FFFFFF", cyan = "#70CDE8",
    green = "#A3DCAF", yellow = "#E9DD79", pink = "#ED9BAA",
)
STYLE = dict(
    header_size = 36, formula_size = 36, label_size = 36,
    formula_max_width = 12.50, formula_z = 40,
    header = (0.0, 3.32, 0.0), footer = (0.0, -2.58, 0.0),
    open_label_offset = (0.0, 1.48, 0.0),
    radius_angles = (0.73 * PI, 0.25 * PI),
    final_formula_scale = 1.08, min_frames = 1, tolerance = 1e-7,
)
# 以下是所复用构图的原参数。需要调色、尺寸、位置或点数时只修改此处
PREFACE_PARAMETERS = dict(
    BACKGROUND = BG_COLOR, FRAME_WIDTH = FRAME_WIDTH, FRAME_HEIGHT = FRAME_HEIGHT,
    CIRCLE_RADIUS = 1.8, CIRCLE_CENTERS = ((-3.0, 0.0, 0.0), (3.0, 0.0, 0.0)),
    CIRCLE_ARCS = 240, CIRCLE_ARC_OVERLAP = 0.002, CIRCLE_STROKE = 14.0,
    CIRCLE_DOTS = 24, CIRCLE_DOT_RADIUS = 0.11,
    CIRCLE_START_COLOR = BLUE_B, CIRCLE_END_COLOR = GREEN_B,
    CIRCLE_DIM_OPACITY = 0.22, CIRCLE_HIGHLIGHT_OPACITY = 1.0,
    CURVE_STROKE = 5.2, CURVE_SEGMENTS = 144, GRAPH_SEGMENTS = 288,
    CURVE_SEGMENT_OVERLAP = 0.40,
    CURVE_COLORS = (PALETTE['cyan'], PALETTE['green'], PALETTE['yellow']),
    AXIS_STROKE = 2.1, AXIS_OPACITY = 1.0, AXIS_TICK_SIZE = 0.055,
    PEN_RADIUS = 0.047, PEN_GLOW_RADII = (0.08, 0.13, 0.21),
    PEN_GLOW_OPACITIES = (0.18, 0.075, 0.025), PEN_COLOR = PALETTE['ink'],
    FORMULA_SIZE = 45, FUNCTION_AMPLITUDE = 0.78,
    FUNCTION_FREQUENCY = 1.18, FUNCTION_SLOPE = 0.16,
    GRAPH_X_RANGE = (-4.5, 4.5, 1.0), GRAPH_Y_RANGE = (-2.3, 2.3, 1.0),
    GRAPH_WIDTH = 10.7, GRAPH_HEIGHT = 4.7, GRAPH_CENTER = (0.0, -0.12, 0.0),
    GRAPH_FORMULA_POSITION = (4.75, 2.68, 0.0), STROKE_FORMULA = r"y=f(x)",
    MAP_INPUT_CENTER = (-3.60, 0.30, 0.0), MAP_OUTPUT_CENTER = (3.60, 0.30, 0.0),
    MAP_SHAPE_WIDTH = 5.50, MAP_SHAPE_HEIGHT = 5.10, MAP_OUTLINE_STROKE = 1.8,
    MAP_FILL_COLORS = ("#A9D9F4", "#BFE6C6"), MAP_FILL_OPACITY = 0.13,
    MAP_TARGET_INPUT = (-3.60, 0.30, 0.0), MAP_TARGET_OUTPUT = (3.60, 0.30, 0.0),
    MAP_TARGET_RADIUS = 0.092, MAP_TARGET_OUTLINE_COLOR = "#000000",
    MAP_TARGET_OUTLINE_STROKE = 3.0, MAP_LABEL_SIZE = 32,
    MAP_TARGET_LABEL_OFFSETS = ((0.0, -0.36, 0.0), (0.20, -0.42, 0.0)),
    MAP_TARGET_LABEL_OUTLINE_COLOR = "#000000", MAP_TARGET_LABEL_OUTLINE_STROKE = 5.0,
    MAP_CLOUD_RADIUS = 0.60, MAP_CLOUD_COUNT = 60,
    MAP_CLOUD_DOT_RADIUS = 0.092 * 0.7, MAP_CLOUD_COLORS = ("#63B9F4", "#8EE3A4"),
    MAP_CLOUD_OPACITY = 0.92, MAP_CLOUD_EDGE_OPACITY = 0.18,
    MAP_CLOUD_FADE_POWER = 1.2, MAP_CLOUD_MIN_SPACING = 0.10,
    MAP_SPAWN_TIME_POWER = 0.46, MAP_SPAWN_FADE_TIME = 0.32, MAP_OUTPUT_DELAY = 1.35,
    MAP_RANDOM_SEED = 20261005, MAP_RANDOM_ATTEMPT_LIMIT = 100000,
    MAP_OUTPUT_SCALE = 0.9, MAP_OUTPUT_ROTATION = 20 * DEGREES,
    MAP_ARROW_START = (-0.65, 0.30, 0.0), MAP_ARROW_END = (0.65, 0.30, 0.0),
    MAP_ARROW_STROKE = 2.4, MAP_ARROW_TIP = 0.18, MAP_F_POSITION = (0.0, 0.96, 0.0),
    MAP_FUNCTION_SYMBOL = "f", MAP_TARGET_LABELS = (r"x_0", r"f(x_0)"),
    MAP_TARGET_Z_INDEX = 4, MAP_TARGET_LABEL_Z_INDEX = 5, MAP_CLOUD_Z_INDEX = 2,
)
# part_six.py 中已用过的开圆盘和半径标注；保留原线宽和淡填充
BALL_STYLE = dict(
    fill_opacity = 0.09, curve_width = 2.2, boundary_dashes = 48,
    boundary_ratio = 0.58, boundary_dash_length = 0.080,
    boundary_gap_length = 0.060, minimum_dashes = 10,
    formula_size = STYLE['formula_size'], formula_width = STYLE['formula_max_width'],
    formula_z = STYLE['formula_z'], small_size = 26, label_outline = 3.0,
    outline_color = "#000000",
)
RADIUS_STYLE = dict(radius_label_gap = 0.16, radius_width = 1.7)
NEIGHBORHOOD = dict(
    epsilon_values = (0.96, 0.70, 0.46),
    final_epsilon = 0.96,
    # f 是 preface 的旋转 + 0.9 倍缩放；精确原像半径为 epsilon / 0.9
    cloud_scale = 1.0,
)
FORMULAS = dict(
    mapping = r"f:(X,\mathcal{T}_X)\longrightarrow(Y,\mathcal{T}_Y)",
    metric = (
        r"d_X(x,x_0)<\delta", r"\Longrightarrow",
        r"d_Y\bigl(f(x),f(x_0)\bigr)<\varepsilon",
    ),
    open_rule = (r"\forall V\in\mathcal{T}_Y,", r"f^{-1}(V)\in\mathcal{T}_X"),
    open_labels = (r"f^{-1}(V)", r"V"),
)
TIMING = dict(
    start_hold = 0.40, circles_reveal = 2.80, circles_hold = 1.50,
    circle_focus = 0.85, circle_focus_hold = 2.10, circle_restore = 0.75,
    mapping_reveal = 1.25, mapping_hold = 3.50,
    graph_bridge = 1.80, graph_draw = 4.00, graph_formula = 0.85, graph_hold = 3.00,
    mapping_bridge = 2.20, mapping_settle = 1.60,
    output_request = 1.50, request_hold = 1.40,
    input_response = 1.70, response_hold = 1.80, metric_formula = 1.30,
    clouds = 8.00, metric_hold = 2.20, old_guarantee_release = 0.65,
    request_shrink = 1.45, response_reveal = 1.70, guarantee_hold = 2.30,
    metric_release = 1.35, open_restore = 2.00, open_labels = 1.30,
    rule_write = 1.80, open_hold = 4.50, formula_focus = 1.70, final_hold = 6.00,
)

# 只读复用原场景组件
def _load_reference(key):
    path = Path(__file__).resolve().parent / REFERENCE_FILES[key]

    if not path.is_file():
        raise FileNotFoundError("需要同目录的原场景文件：" + str(path))
    
    name = "_epilogue_reference_" + key
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

    return module

# 原模块导入会设置 config；保留用户命令行的分辨率和帧率
_cli_frame_rate = config.frame_rate
_pf = _load_reference('preface')
_six = _load_reference('neighborhoods')

for _name, _value in PREFACE_PARAMETERS.items():
    setattr(_pf, _name, _value)

_pf.PALETTE.update(axis = PALETTE['axis'], frame = PALETTE['ink'],
                   arrow = PALETTE['ink'], white = PALETTE['ink'])
_pf.colored_path.__defaults__ = (PREFACE_PARAMETERS['CURVE_STROKE'], PREFACE_PARAMETERS['CURVE_SEGMENTS'])
_six.STYLE.update(BALL_STYLE)
_six.PROOF.update(RADIUS_STYLE)
config.background_color = BG_COLOR
config.frame_width = FRAME_WIDTH
config.frame_height = FRAME_HEIGHT
config.frame_rate = _cli_frame_rate if FRAME_RATE is None else FRAME_RATE

def _v(value):

    return np.asarray(value, dtype = float)

def _tex(source, position = None, size = None):
    # 使用前作的公式轮廓处理，保持字形与黑色细描边的画风
    return _six._tex(source, STYLE['footer'] if position is None else position,
                     STYLE['formula_size'] if size is None else size)

def _clouds_at(reference, epsilon):
    clouds = reference.copy()
    ratio = NEIGHBORHOOD['cloud_scale'] * epsilon / NEIGHBORHOOD['epsilon_values'][0]

    for cloud, center in zip(clouds, (_pf.MAP_TARGET_INPUT, _pf.MAP_TARGET_OUTPUT)):
        cloud.scale(ratio, about_point = _v(center))

    return clouds

def _balls(epsilon):
    # 完整原像和输入保证是同一个圆盘，不额外增加一层装饰圆
    return VGroup(
        _six._disk(_v(_pf.MAP_TARGET_INPUT), epsilon / _pf.MAP_OUTPUT_SCALE, PALETTE['cyan']),
        _six._disk(_v(_pf.MAP_TARGET_OUTPUT), epsilon, PALETTE['green']),
    )

def _markers(epsilon):
    return VGroup(*[
        _six._world_radius_marker(_v(center), radius, symbol, color, angle, 1.0)
        for center, radius, symbol, color, angle in zip(
            (_pf.MAP_TARGET_INPUT, _pf.MAP_TARGET_OUTPUT),
            (epsilon / _pf.MAP_OUTPUT_SCALE, epsilon),
            (r"\delta", r"\varepsilon"),
            (PALETTE['cyan'], PALETTE['green']), STYLE['radius_angles'],
        )
    ])

def validate_parameters():
    if BG_COLOR != '#000012' or PALETTE['axis'] != '#FFFFFF':
        raise ValueError('背景必须为 #000012，坐标轴必须为白色。')
    if min(FRAME_WIDTH, FRAME_HEIGHT, TIME_SCALE) <= 0:
        raise ValueError('画幅和时间比例必须为正。')
    if FRAME_RATE is not None and FRAME_RATE <= 0:
        raise ValueError('帧率必须为正或 None。')
    if any(value <= 0 for value in TIMING.values()):
        raise ValueError('所有时长必须为正。')
    
    values = NEIGHBORHOOD['epsilon_values']

    if not values or min(values) <= 0 or _pf.MAP_OUTPUT_SCALE <= 0:
        raise ValueError('半径和映射比例必须为正。')
    if not 0 < NEIGHBORHOOD['cloud_scale']:
        raise ValueError('点云缩放必须为正。')
    
    input_half_size = min(_pf.MAP_SHAPE_WIDTH, _pf.MAP_SHAPE_HEIGHT) / 2

    for epsilon in (*values, NEIGHBORHOOD['final_epsilon']):
        if not 0 < epsilon < input_half_size or epsilon / _pf.MAP_OUTPUT_SCALE >= input_half_size:
            raise ValueError('两侧开球必须严格留在原来的椭圆中。')
        
    if _pf.MAP_CLOUD_RADIUS * NEIGHBORHOOD['cloud_scale'] >= values[0] / _pf.MAP_OUTPUT_SCALE:
        raise ValueError('原始点云必须严格位于输入保证范围中。')
    if _pf.MAP_TARGET_INPUT != _pf.MAP_INPUT_CENTER or _pf.MAP_TARGET_OUTPUT != _pf.MAP_OUTPUT_CENTER:
        raise ValueError('复用的旋转缩放模型要求目标点位于各自椭圆中心。')
    
    return True

# 唯一可渲染 Scene
class Epilogue(Scene):
    def setup(self):
        super().setup()
        self.camera.background_color = BG_COLOR
        validate_parameters()

    def get_moving_mobjects(self, *animations):
        # 原曲线含分段渐变，公式又有独立图层；完整绘制避免 Cairo 静态缓存丢字
        return self.mobjects

    def motion(self, *animations, seconds, **kwargs):
        self.play(*animations, run_time = max(seconds * TIME_SCALE,
                  STYLE['min_frames'] / float(config.frame_rate)), **kwargs)

    def pause(self, seconds):
        self.wait(max(seconds * TIME_SCALE, STYLE['min_frames'] / float(config.frame_rate)))

    def stage(self, *objects):
        # 每个稳定几何和公式直接作为根对象，避免嵌套组在子动画后重排
        self.clear()
        self.add(*objects)

    def construct(self):
        # 1. 原版两圆：尺寸、240 段渐变、24 个离散点和聚焦方式均来自 preface
        self.pause(TIMING['start_hold'])
        circles = _pf.thumbnail_circles()
        circles[1].set_opacity(0)

        def reveal_dots(group, alpha):

            for index, dot in enumerate(group):
                dot.set_opacity(float(np.clip(alpha * _pf.CIRCLE_DOTS - index, 0, 1)))

        self.motion(Create(circles[0], lag_ratio = 1),
                    UpdateFromAlphaFunc(circles[1], reveal_dots),
                    seconds = TIMING['circles_reveal'], rate_func = linear)
        self.stage(*circles)
        self.pause(TIMING['circles_hold'])
        self.motion(circles[1].animate.set_opacity(_pf.CIRCLE_DIM_OPACITY), seconds = TIMING['circle_focus'])
        self.pause(TIMING['circle_focus_hold'])
        self.motion(circles[0].animate.set_stroke(opacity = _pf.CIRCLE_DIM_OPACITY), circles[1].animate.set_opacity(1), seconds = TIMING['circle_focus'])
        self.pause(TIMING['circle_focus_hold'])
        self.motion(circles[0].animate.set_stroke(opacity = 1), seconds = TIMING['circle_restore'])
        header = _tex(FORMULAS['mapping'], STYLE['header'], STYLE['header_size'])
        self.motion(Write(header), seconds = TIMING['mapping_reveal'])
        self.pause(TIMING['mapping_hold'])

        # 2. 复用已经出现过的一笔画曲线，作为尾声回顾，不增加新函数例子
        graph = _pf.ordinary_graph()
        self.motion(FadeOut(circles[0]), FadeOut(circles[1]), FadeOut(header), Create(graph.axes), seconds = TIMING['graph_bridge'])
        pen = _pf.pen_at(graph.axes.c2p(_pf.GRAPH_X_RANGE[0], _pf.smooth_function(_pf.GRAPH_X_RANGE[0])), color = PALETTE['ink'])
        self.add(pen)
        self.motion(
            Create(graph.curve, lag_ratio = 1),
            UpdateFromAlphaFunc(pen, lambda mob, alpha: mob.move_to(graph.axes.c2p(
                interpolate(*_pf.GRAPH_X_RANGE[:2], alpha),
                _pf.smooth_function(interpolate(*_pf.GRAPH_X_RANGE[:2], alpha))))),
            seconds = TIMING['graph_draw'], rate_func = linear,
        )
        self.remove(pen)
        self.motion(FadeIn(graph.formula), seconds = TIMING['graph_formula'])
        self.stage(graph.axes, graph.curve, graph.formula)
        self.pause(TIMING['graph_hold'])

        # 3. 原版 Closeness 的椭圆、箭头、目标点和点云，全在原位置
        shell, targets = _pf.map_shell(), _pf.map_targets()
        header = _tex(FORMULAS['mapping'], STYLE['header'], STYLE['header_size'])
        base = [*shell[0], shell[1], shell[2], *targets[0], *targets[1], header]
        self.motion(
            FadeOut(graph.axes), FadeOut(graph.curve), FadeOut(graph.formula),
            *[FadeIn(item) for item in base], seconds = TIMING['mapping_bridge'],
        )
        self.stage(*base)
        self.pause(TIMING['mapping_settle'])
        epsilon = NEIGHBORHOOD['epsilon_values'][0]
        balls, markers = _balls(epsilon), _markers(epsilon)
        metric = _tex(FORMULAS['metric'])
        metric[0].set_color(PALETTE['cyan'])
        metric[2].set_color(PALETTE['green'])
        self.motion(FadeIn(balls[1]), Create(markers[1]), seconds = TIMING['output_request'])
        self.pause(TIMING['request_hold'])
        self.motion(FadeIn(balls[0]), Create(markers[0]), seconds = TIMING['input_response'])
        self.pause(TIMING['response_hold'])
        self.motion(Write(metric), seconds = TIMING['metric_formula'])
        clouds = _pf.map_clouds()
        reveal, _ = _pf.map_cloud_reveal(clouds)
        self.motion(reveal, seconds = TIMING['clouds'], rate_func = linear)
        reference_clouds = clouds.copy()

        if NEIGHBORHOOD['cloud_scale'] != 1:
            clouds.become(_clouds_at(reference_clouds, epsilon))
        self.stage(*base, *balls, *markers, *clouds, metric)
        self.pause(TIMING['metric_hold'])

        # 输出先提出新要求；旧输入保证退出后，才显示新的输入范围
        # 每组点始终来自原来同一个旋转缩放映射，两侧同步等比收紧
        for next_epsilon in NEIGHBORHOOD['epsilon_values'][1:]:
            self.motion(FadeOut(balls[0]), FadeOut(markers[0]), FadeOut(clouds[0]), FadeOut(clouds[1]), FadeOut(metric), seconds = TIMING['old_guarantee_release'])
            next_balls, next_markers = _balls(next_epsilon), _markers(next_epsilon)
            next_clouds = _clouds_at(reference_clouds, next_epsilon)
            self.motion(Transform(balls[1], next_balls[1]), Transform(markers[1], next_markers[1]), seconds = TIMING['request_shrink'])
            balls[0].become(next_balls[0])
            markers[0].become(next_markers[0])
            clouds.become(next_clouds)
            self.motion(FadeIn(balls[0]), FadeIn(markers[0]), FadeIn(clouds[0]), FadeIn(clouds[1]), FadeIn(metric), seconds = TIMING['response_reveal'])
            self.stage(*base, *balls, *markers, *clouds, metric)
            self.pause(TIMING['guarantee_hold'])
            epsilon = next_epsilon

        # 4. 距离标注退出，原来的范围保留，收束为开集原像规则
        self.motion(FadeOut(markers[0]), FadeOut(markers[1]), FadeOut(metric), seconds = TIMING['metric_release'])
        final_balls = _balls(NEIGHBORHOOD['final_epsilon'])
        final_clouds = _clouds_at(reference_clouds, NEIGHBORHOOD['final_epsilon'])
        self.motion(
            Transform(balls[0], final_balls[0]), Transform(balls[1], final_balls[1]),
            Transform(clouds[0], final_clouds[0]), Transform(clouds[1], final_clouds[1]),
            seconds = TIMING['open_restore']
        )
        open_labels = [
            _tex(symbol, _v(center) + _v(STYLE['open_label_offset']), STYLE['label_size']).set_color(color)
            for symbol, center, color in zip(
                FORMULAS['open_labels'], (_pf.MAP_TARGET_INPUT, _pf.MAP_TARGET_OUTPUT),
                (PALETTE['cyan'], PALETTE['green']),
            )
        ]
        self.motion(*[Write(label) for label in open_labels], seconds = TIMING['open_labels'])
        rule = _tex(FORMULAS['open_rule'])
        rule[0].set_color(PALETTE['green'])
        rule[1].set_color(PALETTE['cyan'])
        self.motion(Write(rule), seconds = TIMING['rule_write'])
        final_roots = [*base, *balls, *clouds, *open_labels, rule]
        self.stage(*final_roots)
        self.pause(TIMING['open_hold'])
        self.motion(rule.animate.scale(STYLE['final_formula_scale']), seconds = TIMING['formula_focus'])
        self.stage(*final_roots)
        
        # 不淡出到黑场，保留原场景和规则，方便接用户自行安排的后续段落
        self.pause(TIMING['final_hold'])
