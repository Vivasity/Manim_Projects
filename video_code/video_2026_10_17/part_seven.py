from manim import *
from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath
from svgelements import Path as SVGPath
import itertools
import math
import numpy as np

# 全部可调参数
BG_COLOR = "#000012"
FRAME_WIDTH = 128 / 9
FRAME_HEIGHT = 8.0
FRAME_RATE = 60                 # 设为 None 时沿用 Manim 命令行帧率
TIME_SCALE = 1.0                # 同时缩放运动与停顿的时长
SUBTITLE_SAFE_TOP = -2.60       # 底部约 17.5% 的画面留给字幕
LOWER_FORMULA_Y = SUBTITLE_SAFE_TOP + 0.30
PALETTE = dict(
    axis = "#FFFFFF", ink = "#FFFFFF", pink = "#EF819B",
    cyan = "#56CEE8", green = "#9EE3A2", yellow = "#FFE17D",
    muted = "#687C98", arrow = "#FFFFFF", error = "#FF8298",
)
STYLE = dict(
    formula_size = 37, header_size = 38, label_size = 33,
    column_size = 29, row_size = 27, intro_row_size = 35,
    formula_max_width = 12.50, icon_stroke = 2.30, small_icon_stroke = 1.70,
    boundary_stroke = 1.75, boundary_opacity = 0.72,
    region_stroke = 2.10, region_fill = 0.065, region_dashes = 42,
    region_dash_ratio = 0.64, edge_stroke = 3.60, edge_opacity = 0.7,
    edge_tip = 0.17, edge_tip_width = 0.14, point_radius = 0.047,
    halo_radius = 0.14, halo_opacity = 0.13, row_focus_stroke = 1.65,
    row_focus_buff = 0.085, row_focus_corner = 0.10,
    formula_z = 30, icon_z = 15, region_z = 6, edge_z = 2,
    minimum_frames = 1, tolerance = 1e-7,
)
TIMING = dict(
    start_hold = 0.30, join_hold = 0.22, reveal = 1.40,
    letter_write = 1.35, letter_hold = 1.20, letter_to_icon = 2.20,
    icon_hold = 0.80, icon_lag = 0.24, formula = 1.20,
    subset_select = 0.68, subset_copy = 0.90, subset_hold = 0.30,
    subset_release = 0.32, list_hold = 2.20, bridge = 2.80,
    request = 1.05, response = 1.30, flow = 2.35, flow_lag = 0.16,
    case_hold = 1.25, clear = 0.65, conclusion_hold = 2.00,
    topology_swap = 3.40, identity_hold = 1.50, counterexample_hold = 1.75,
    final_hold = 4.50,
)
LAYOUT = dict(
    header = (0, 3.23, 0), footer = (0, LOWER_FORMULA_Y, 0),
    left = (-2.40, 0.35, 0), right = (2.40, 0.35, 0),
    space_width = 3.05, space_height = 3.60, space_label_y = 2.13,
    icon_height = 0.65,
    icon_offsets = ((-0.52, 0.78, 0), (0.60, 0, 0), (-0.40, -0.78, 0)),
    tag_offset = (0, -2.13, 0), tag_size = 30,
    column_x = (-5.46, 5.46), column_header_y = 2.63,
    column_top_y = 1.98, column_gap = 0.58, column_left_offset = -0.84,
    column_icon_height = 0.315, column_token_gap = 0.065,
    column_header_max_width = 2.24,
    short_column_ys = (0.73, -0.73), arbitrary_column_ys = (0.85, 0, -0.85),
    row_alignment_y = 0.0,
    selection_radius = 0.54, selection_width = 2.48, selection_height = 2.95,
    empty_mark_offset = (0, -0.03, 0), empty_mark_size = 40,
    edge_gap = 0.12, edge_handle = 1.00, edge_bends = (0.24, -0.24, -0.15),
    intro_center = (2.75, 0.60, 0), intro_space_scale = 1.34, intro_letter_size = 66,
    intro_column_x = -2.52, intro_column_top_y = 2.34, intro_column_gap = 0.65,
    intro_column_header_y = 3.23, intro_column_left_offset = -1.16,
    intro_icon_height = 0.47, intro_token_gap = 0.11,
    intro_identity_position = (2.75, LOWER_FORMULA_Y, 0), intro_identity_size = 39,
    subset_arc = -0.26 * PI, swap_arc = 0.17 * PI,
    counterexample_token_gap = 0.10, counterexample_icon_height = 0.38,
    counterexample_size = 33,
)
MODEL = dict(
    kinds = ("like", "coin", "favorite"), letters = (r"a", r"b", r"c"),
    # 空集、三个单点集、三个双点集、全集，严格从上到下排列
    subsets = ((), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)),
    arbitrary_map = (1, 1, 0), identity_map = (0, 1, 2),
    discrete_probes = ((1,), (0, 1), (2,)), counterexample = (0,),
)
FORMULAS = dict(
    x = r"X", y = r"Y", empty = r"\varnothing", dots = r"\vdots",
    left_brace = r"\{", right_brace = r"\}", comma = r",",
    discrete = r"\mathcal{T}_{\mathrm d} = \mathcal P(X)",
    indiscrete = r"\mathcal{T}_{\mathrm i}", arbitrary = r"\mathcal{T}_X",
    intro_count = r"|X| = 3\qquad |\mathcal P(X)| = 2^3 = 8",
    discrete_header = r"f:(X,\mathcal{T}_{\mathrm d})\longrightarrow(Y,\mathcal{T}_Y)",
    discrete_footer = r"f^{-1}(V)\subseteq X\quad\Longrightarrow\quad f^{-1}(V)\in\mathcal{T}_{\mathrm d}",
    discrete_result = r"\forall f:(X,\mathcal{T}_{\mathrm d})\to(Y,\mathcal{T}_Y),\quad f\in C(X,Y)",
    indiscrete_header = r"f:(X,\mathcal{T}_X)\longrightarrow(Y,\mathcal{T}_{\mathrm i})",
    indiscrete_footer = r"\mathcal{T}_{\mathrm i} = \{\varnothing,Y\}",
    empty_preimage = r"f^{-1}(\varnothing) = \varnothing",
    full_preimage = r"f^{-1}(Y) = X",
    indiscrete_result = r"\forall f:(X,\mathcal{T}_X)\to(Y,\mathcal{T}_{\mathrm i}),\quad f\in C(X,Y)",
    identity_header = r"\mathrm{id}:(X,\mathcal{T}_{\mathrm d})\longrightarrow(X,\mathcal{T}_{\mathrm i})",
    identity_footer = r"\mathrm{id}_X(x) = x",
    identity_result = r"\mathrm{id}\in C\bigl((X,\mathcal{T}_{\mathrm d}),(X,\mathcal{T}_{\mathrm i})\bigr)",
    identity_empty_preimage = r"\mathrm{id}^{-1}(\varnothing) = \varnothing",
    identity_full_preimage = r"\mathrm{id}^{-1}(X) = X",
    reversed_header = r"\mathrm{id}:(X,\mathcal{T}_{\mathrm i})\longrightarrow(X,\mathcal{T}_{\mathrm d})",
    fixed_rule = r"\mathrm{id}_X(x) = x",
    reversed_footer = r"\mathrm{id}\notin C\bigl((X,\mathcal{T}_{\mathrm i}),(X,\mathcal{T}_{\mathrm d})\bigr)",
    request = r"V\in\mathcal{T}_Y", preimage = r"f^{-1}(V)",
    empty_request = r"V = \varnothing", full_request = r"V = Y",
    identity_request = r"V\in\mathcal{T}_{\mathrm d}",
    bad_preimage_prefix = r"\mathrm{id}^{-1}\!(",
    bad_preimage_middle = r") =", bad_preimage_suffix = r"\notin\mathcal{T}_{\mathrm i}",
)
# 与前作完全相同的 B 站官方原始路径；无填充，仅以粉色勾勒轮廓
# 点赞 / 投币：B站 video.05af4e80b6081ba56c1b5b943d4c8e621df3f875.js
# 收藏：B站视频页 video-fav-icon。全部内嵌，无外部 SVG / 图片依赖
ICON_PATHS = dict(
    like = 'M9.77234 30.8573V11.7471H7.54573C5.50932 11.7471 3.85742 13.3931 3.85742 15.425V27.1794C3.85742 29.2112 5.50932 30.8573 7.54573 30.8573H9.77234ZM11.9902 30.8573V11.7054C14.9897 10.627 16.6942 7.8853 17.1055 3.33591C17.2666 1.55463 18.9633 0.814421 20.5803 1.59505C22.1847 2.36964 23.243 4.32583 23.243 6.93947C23.243 8.50265 23.0478 10.1054 22.6582 11.7471H29.7324C31.7739 11.7471 33.4289 13.402 33.4289 15.4435C33.4289 15.7416 33.3928 16.0386 33.3215 16.328L30.9883 25.7957C30.2558 28.7683 27.5894 30.8573 24.528 30.8573H11.9911H11.9902Z',
    coin = 'M14.045 25.5454C7.69377 25.5454 2.54504 20.3967 2.54504 14.0454C2.54504 7.69413 7.69377 2.54541 14.045 2.54541C20.3963 2.54541 25.545 7.69413 25.545 14.0454C25.545 17.0954 24.3334 20.0205 22.1768 22.1771C20.0201 24.3338 17.095 25.5454 14.045 25.5454ZM9.66202 6.81624H18.2761C18.825 6.81624 19.27 7.22183 19.27 7.72216C19.27 8.22248 18.825 8.62807 18.2761 8.62807H14.95V10.2903C17.989 10.4444 20.3766 12.9487 20.3855 15.9916V17.1995C20.3854 17.6997 19.9799 18.1052 19.4796 18.1052C18.9793 18.1052 18.5738 17.6997 18.5737 17.1995V15.9916C18.5667 13.9478 16.9882 12.2535 14.95 12.1022V20.5574C14.95 21.0577 14.5444 21.4633 14.0441 21.4633C13.5437 21.4633 13.1382 21.0577 13.1382 20.5574V12.1022C11.1 12.2535 9.52148 13.9478 9.51448 15.9916V17.1995C9.5144 17.6997 9.10883 18.1052 8.60856 18.1052C8.1083 18.1052 7.70273 17.6997 7.70265 17.1995V15.9916C7.71158 12.9487 10.0992 10.4444 13.1382 10.2903V8.62807H9.66202C9.11309 8.62807 8.66809 8.22248 8.66809 7.72216C8.66809 7.22183 9.11309 6.81624 9.66202 6.81624Z',
    favorite = 'M19.8071 9.26152C18.7438 9.09915 17.7624 8.36846 17.3534 7.39421L15.4723 3.4972C14.8998 2.1982 13.1004 2.1982 12.4461 3.4972L10.6468 7.39421C10.1561 8.36846 9.25639 9.09915 8.19315 9.26152L3.94016 9.91102C2.63155 10.0734 2.05904 11.6972 3.04049 12.6714L6.23023 15.9189C6.96632 16.6496 7.29348 17.705 7.1299 18.7605L6.39381 23.307C6.14844 24.6872 7.62063 25.6614 8.84745 25.0119L12.4461 23.0634C13.4276 22.4951 14.6544 22.4951 15.6359 23.0634L19.2345 25.0119C20.4614 25.6614 21.8518 24.6872 21.6882 23.307L20.8703 18.7605C20.7051 17.705 21.0339 16.6496 21.77 15.9189L24.9597 12.6714C25.9412 11.6972 25.3687 10.0734 24.06 9.91102L19.8071 9.26152Z',
)

# 公共几何与动画工具
config.background_color = BG_COLOR
config.frame_width = FRAME_WIDTH
config.frame_height = FRAME_HEIGHT

if FRAME_RATE is not None:
    config.frame_rate = FRAME_RATE

def _v(point):

    return np.asarray(point, dtype = float)

def _tex(source, size = None, color = None, position = None):
    result = MathTex(
        source,
        font_size = STYLE['formula_size'] if size is None else size,
        color = PALETTE['ink'] if color is None else color,
    ).set_z_index(STYLE['formula_z'])

    if result.width > STYLE['formula_max_width']:
        result.scale_to_fit_width(STYLE['formula_max_width'])
    if position is not None:
        result.move_to(_v(position))

    return result

def _icon(index, height, small = False):
    path = ICON_PATHS[MODEL['kinds'][index]]
    result = VMobjectFromSVGPath(SVGPath(path))

    # SVG 纵轴向下，仅反转纵向，等比例缩放以保留官方轮廓
    result.flip(RIGHT).center().scale_to_fit_height(height)
    result.set_fill(opacity = 0)
    result.set_stroke(
        PALETTE['pink'],
        STYLE['small_icon_stroke'] if small else STYLE['icon_stroke'],
    )

    return result.set_z_index(STYLE['icon_z'])

def _subset(indices, height = None, size = None, gap = None):
    indices = tuple(indices)
    height = LAYOUT['column_icon_height'] if height is None else height
    size = STYLE['row_size'] if size is None else size
    gap = LAYOUT['column_token_gap'] if gap is None else gap
    elements = {}

    if not indices:
        result = VGroup(_tex(FORMULAS['empty'], size = size))
    else:
        tokens = [_tex(FORMULAS['left_brace'], size = size)]

        for place, index in enumerate(indices):

            if place:
                tokens.append(_tex(FORMULAS['comma'], size = size))
            element = _icon(index, height, small = True)
            elements[index] = element
            tokens.append(element)

        tokens.append(_tex(FORMULAS['right_brace'], size = size))
        result = VGroup(*tokens).arrange(RIGHT, buff = gap)

        for element in elements.values():
            element.set_y(LAYOUT['row_alignment_y'])

    result.indices = indices
    result.elements = elements

    return result

def _column(kind, x, introductory = False):
    header_y = LAYOUT['intro_column_header_y'] if introductory else LAYOUT['column_header_y']
    header = _tex(
        FORMULAS[kind], size = STYLE['header_size'] if introductory else STYLE['column_size'],
        position = (x, header_y, 0),
    )

    if not introductory and header.width > LAYOUT['column_header_max_width']:
        header.scale_to_fit_width(LAYOUT['column_header_max_width'])

    if kind == 'discrete':
        indices = MODEL['subsets']
        top = LAYOUT['intro_column_top_y'] if introductory else LAYOUT['column_top_y']
        gap = LAYOUT['intro_column_gap'] if introductory else LAYOUT['column_gap']
        ys = tuple(top - gap * i for i in range(len(indices)))
    elif kind == 'indiscrete':
        indices = (MODEL['subsets'][0], MODEL['subsets'][-1])
        ys = LAYOUT['short_column_ys']
    else:
        indices = (MODEL['subsets'][0], None, MODEL['subsets'][-1])
        ys = LAYOUT['arbitrary_column_ys']

    rows = VGroup()
    lookup = {}

    for items, y in zip(indices, ys):

        if items is None:
            row = VGroup(_tex(FORMULAS['dots'], size = STYLE['row_size']))
        else:
            row = _subset(
                items,
                height = LAYOUT['intro_icon_height'] if introductory else None,
                size = STYLE['intro_row_size'] if introductory else None,
                gap = LAYOUT['intro_token_gap'] if introductory else None,
            )
            lookup[tuple(items)] = row

        row.move_to(_v((x, y, 0)))
        left = x + (LAYOUT['intro_column_left_offset'] if introductory else LAYOUT['column_left_offset'])
        row.shift((left - row.get_left()[0]) * RIGHT)
        rows.add(row)

    result = VGroup(header, rows)
    result.header = header
    result.rows = rows
    result.lookup = lookup
    result.kind = kind

    return result

def _space(center, label, color, scale = 1.0):
    center = _v(center)
    boundary = Ellipse(
        width = LAYOUT['space_width'] * scale,
        height = LAYOUT['space_height'] * scale,
        stroke_color = color, stroke_width = STYLE['boundary_stroke'],
        stroke_opacity = STYLE['boundary_opacity'], fill_opacity = 0,
    ).move_to(center)
    icons = VGroup(*[
        _icon(i, LAYOUT['icon_height'] * scale).move_to(center + scale * _v(offset))
        for i, offset in enumerate(LAYOUT['icon_offsets'])
    ])
    name = _tex(
        label, size = STYLE['label_size'],
        position = center + scale * LAYOUT['space_label_y'] * UP,
    )
    result = VGroup(boundary, icons, name)
    result.boundary = boundary
    result.icons = icons
    result.label = name
    result.center_point = center
    result.space_scale = scale

    return result

def _selection(space, indices, color):
    indices = tuple(indices)

    if not indices:
        return _tex(
            FORMULAS['empty'], size = LAYOUT['empty_mark_size'], color = color,
            position = space.center_point + _v(LAYOUT['empty_mark_offset']),
        )
    
    scale = space.space_scale
    points = [space.icons[i].get_center() for i in indices]
    radius = LAYOUT['selection_radius'] * scale

    if len(indices) == 1:
        outline = Circle(radius = radius).move_to(points[0])
    elif len(indices) == 2:
        displacement = points[1] - points[0]
        outline = RoundedRectangle(
            width = np.linalg.norm(displacement) + 2 * radius,
            height = 2 * radius, corner_radius = radius,
        ).rotate(math.atan2(displacement[1], displacement[0])).move_to((points[0] + points[1]) / 2)
    else:
        outline = Ellipse(
            width = LAYOUT['selection_width'] * scale,
            height = LAYOUT['selection_height'] * scale,
        ).move_to(space.center_point)

    shade = outline.copy().set_stroke(width = 0).set_fill(color, opacity = STYLE['region_fill'])
    edge = DashedVMobject(
        outline, num_dashes = STYLE['region_dashes'], dashed_ratio = STYLE['region_dash_ratio'],
    ).set_fill(opacity = 0).set_stroke(color, width = STYLE['region_stroke'])

    return VGroup(shade, edge).set_z_index(STYLE['region_z'])

def _links(left, right, images):
    result = VGroup()

    for i, image in enumerate(images):
        start = left.icons[i].get_right() + LAYOUT['edge_gap'] * RIGHT
        end = right.icons[image].get_left() + LAYOUT['edge_gap'] * LEFT
        bend = LAYOUT['edge_bends'][i] * UP
        path = CubicBezier(
            start, start + LAYOUT['edge_handle'] * RIGHT + bend,
            end + LAYOUT['edge_handle'] * LEFT + bend, end,
        ).set_stroke(PALETTE['arrow'], width = STYLE['edge_stroke'], opacity = STYLE['edge_opacity'])
        tangent = end - path.get_nth_curve_points(path.get_num_curves() - 1)[-2]
        tip = Triangle(
            fill_color = PALETTE['arrow'], fill_opacity = STYLE['edge_opacity'], stroke_width = 0,
        ).set_height(STYLE['edge_tip']).set_width(STYLE['edge_tip_width'])
        tip.rotate(math.atan2(tangent[1], tangent[0]) - PI / 2).move_to(end)
        edge = VGroup(path, tip).set_z_index(STYLE['edge_z'])
        edge.path = path
        result.add(edge)

    return result

def _stage(mode):
    identity = mode in ('identity', 'reversed')
    left = _space(LAYOUT['left'], FORMULAS['x'], PALETTE['cyan'])
    right = _space(LAYOUT['right'], FORMULAS['x'] if identity else FORMULAS['y'], PALETTE['green'])

    if mode == 'discrete':
        left_kind, right_kind = 'discrete', None
    elif mode == 'indiscrete':
        left_kind, right_kind = 'arbitrary', 'indiscrete'
    elif mode == 'identity':
        left_kind, right_kind = 'discrete', 'indiscrete'
    else:
        left_kind, right_kind = 'indiscrete', 'discrete'

    left_column = _column(left_kind, LAYOUT['column_x'][0])
    right_column = VGroup() if right_kind is None else _column(right_kind, LAYOUT['column_x'][1])
    edges = _links(left, right, MODEL['identity_map'] if identity else MODEL['arbitrary_map'])
    header = _tex(FORMULAS[mode + '_header'], size = STYLE['header_size'], position = LAYOUT['header'])
    footer = _tex(FORMULAS[mode + '_footer'], position = LAYOUT['footer'])
    result = VGroup(edges, left, right, left_column, right_column, header, footer)
    result.left = left
    result.right = right
    result.left_column = left_column
    result.right_column = right_column
    result.edges = edges
    result.header = header
    result.footer = footer

    return result

def _focus(row, color):

    return SurroundingRectangle(
        row, buff = STYLE['row_focus_buff'], corner_radius = STYLE['row_focus_corner'],
        stroke_color = color, stroke_width = STYLE['row_focus_stroke'], fill_opacity = 0,
    ).set_z_index(STYLE['region_z'])

def _preimage(images, subset):

    return tuple(i for i, image in enumerate(images) if image in subset)

class _AnimationTools:
    # 普通 mixin，不增加可渲染 Scene
    def setup(self):
        super().setup()
        self.camera.background_color = BG_COLOR

    def motion(self, *animations, seconds, **kwargs):
        self.play(*animations, run_time = seconds * TIME_SCALE, **kwargs)

    def pause(self, seconds):
        minimum = STYLE['minimum_frames'] / float(config.frame_rate)
        self.wait(max(seconds * TIME_SCALE, minimum))

    def finish_at(self, stage):
        # 消除变换后的旧成员引用，让相邻分镜真正使用同一套首尾几何
        self.clear()
        self.add(stage)
        self.pause(TIMING['join_hold'])

    def flow(self, stage, indices = None):
        indices = tuple(range(len(MODEL['kinds']))) if indices is None else tuple(indices)

        if not indices:
            self.pause(TIMING['subset_hold'])
            return
        
        particles = VGroup(*[
            VGroup(
                Dot(radius = STYLE['halo_radius'], color = PALETTE['yellow'], fill_opacity = STYLE['halo_opacity']),
                Dot(radius = STYLE['point_radius'], color = PALETTE['yellow']),
            ).move_to(stage.edges[i].path.get_start()).set_z_index(STYLE['icon_z'])
            for i in indices
        ])
        self.add(particles)
        self.motion(
            LaggedStart(*[
                MoveAlongPath(particle, stage.edges[i].path)
                for particle, i in zip(particles, indices)
            ], lag_ratio = TIMING['flow_lag']),
            seconds = TIMING['flow'],
        )
        self.motion(FadeOut(particles), seconds = TIMING['subset_release'])

class DiscreteTopology(_AnimationTools, Scene):
    def construct(self):
        self.pause(TIMING['start_hold'])
        space = _space(
            LAYOUT['intro_center'], FORMULAS['x'], PALETTE['cyan'],
            scale = LAYOUT['intro_space_scale'],
        )
        column = _column('discrete', LAYOUT['intro_column_x'], introductory = True)
        count = _tex(
            FORMULAS['intro_count'], size = LAYOUT['intro_identity_size'],
            position = LAYOUT['intro_identity_position'],
        )
        self.motion(Create(space.boundary), Write(space.label), seconds = TIMING['reveal'])
        letters = VGroup(*[
            _tex(letter, size = LAYOUT['intro_letter_size']).move_to(icon.get_center())
            for letter, icon in zip(MODEL['letters'], space.icons)
        ])
        self.motion(
            LaggedStart(*[Write(letter) for letter in letters], lag_ratio = TIMING['icon_lag']),
            seconds = TIMING['letter_write'],
        )
        self.pause(TIMING['letter_hold'])
        self.motion(
            LaggedStart(*[
                ReplacementTransform(letter, icon)
                for letter, icon in zip(letters, space.icons)
            ], lag_ratio = TIMING['icon_lag']),
            seconds = TIMING['letter_to_icon'],
        )
        self.clear()
        self.add(space)
        self.pause(TIMING['icon_hold'])
        self.motion(Write(column.header), seconds = TIMING['formula'])

        for indices, row in zip(MODEL['subsets'], column.rows):
            selected = _selection(space, indices, PALETTE['green'])
            self.motion(FadeIn(selected), seconds = TIMING['subset_select'])

            if indices:
                punctuation = VGroup(*[token for token in row if not any(token is item for item in row.elements.values())])
                self.motion(
                    FadeIn(punctuation),
                    *[TransformFromCopy(space.icons[i], row.elements[i], path_arc = LAYOUT['subset_arc']) for i in indices],
                    seconds = TIMING['subset_copy'],
                )
            else:
                self.motion(TransformFromCopy(selected, row), seconds = TIMING['subset_copy'])

            self.pause(TIMING['subset_hold'])
            self.motion(FadeOut(selected), seconds = TIMING['subset_release'])

        self.motion(Write(count), seconds = TIMING['formula'])
        self.pause(TIMING['list_hold'])

        # 列表缩小移到左侧，原集合进入映射图；列表的每个图标保留粉色轮廓
        self.clear()
        old = VGroup(space, column, count)
        self.add(old)
        target = _stage('discrete')
        self.motion(
            ReplacementTransform(space, target.left),
            ReplacementTransform(column, target.left_column, path_arc = LAYOUT['swap_arc']),
            FadeOut(count),
            seconds = TIMING['bridge'],
        )
        self.motion(
            FadeIn(target.right), FadeIn(target.edges), Write(target.header), Write(target.footer),
            seconds = TIMING['reveal'],
        )
        self.finish_at(target)
        self._show_outgoing_maps(target)

    def _show_outgoing_maps(self, stage):
        # 非单射、也非满射的例子：两个输入落到同一枚投币图标，收藏没有原像
        self.flow(stage)

        for subset in MODEL['discrete_probes']:
            preimage = _preimage(MODEL['arbitrary_map'], subset)
            output = _selection(stage.right, subset, PALETTE['green'])
            input_region = _selection(stage.left, preimage, PALETTE['cyan'])
            output_tag = _tex(
                FORMULAS['request'], size = LAYOUT['tag_size'],
                position = stage.right.center_point + _v(LAYOUT['tag_offset']),
            )
            input_tag = _tex(
                FORMULAS['preimage'], size = LAYOUT['tag_size'],
                position = stage.left.center_point + _v(LAYOUT['tag_offset']),
            )
            row_focus = _focus(stage.left_column.lookup[preimage], PALETTE['cyan'])
            self.motion(FadeIn(output), Write(output_tag), seconds = TIMING['request'])
            self.motion(FadeIn(input_region), Write(input_tag), Create(row_focus), seconds = TIMING['response'])
            self.flow(stage, preimage)
            self.pause(TIMING['case_hold'])
            self.motion(
                *[FadeOut(item) for item in (output, input_region, output_tag, input_tag, row_focus)],
                seconds = TIMING['clear'],
            )

        result = _tex(FORMULAS['discrete_result'], position = LAYOUT['footer'])
        self.motion(Succession(FadeOut(stage.footer), FadeIn(result)), seconds = TIMING['formula'])
        stage.footer = result
        self.pause(TIMING['conclusion_hold'])

        # 从任意拓扑的输入出发，转向只有空集与全集的输出
        target = _stage('indiscrete')
        self.motion(
            Succession(FadeOut(stage.left_column), FadeIn(target.left_column)),
            FadeIn(target.right_column),
            Succession(FadeOut(stage.header), FadeIn(target.header)),
            Succession(FadeOut(stage.footer), FadeIn(target.footer)),
            seconds = TIMING['bridge'],
        )
        self.finish_at(target)

class IndiscreteTopology(_AnimationTools, Scene):
    def construct(self):
        stage = _stage('indiscrete')
        self.add(stage)
        self.pause(TIMING['join_hold'])

        for subset, request, equality in (
            (MODEL['subsets'][0], 'empty_request', 'empty_preimage'),
            (MODEL['subsets'][-1], 'full_request', 'full_preimage'),
        ):
            preimage = _preimage(MODEL['arbitrary_map'], subset)
            output = _selection(stage.right, subset, PALETTE['green'])
            input_region = _selection(stage.left, preimage, PALETTE['cyan'])
            right_focus = _focus(stage.right_column.lookup[subset], PALETTE['green'])
            left_focus = _focus(stage.left_column.lookup[preimage], PALETTE['cyan'])
            request_label = _tex(
                FORMULAS[request], size = LAYOUT['tag_size'],
                position = stage.right.center_point + _v(LAYOUT['tag_offset']),
            )
            formula = _tex(FORMULAS[equality], position = LAYOUT['footer'])
            self.motion(FadeIn(output), Write(request_label), Create(right_focus), seconds = TIMING['request'])
            self.motion(
                FadeIn(input_region), Create(left_focus),
                Succession(FadeOut(stage.footer), FadeIn(formula)),
                seconds = TIMING['response'],
            )
            stage.footer = formula
            self.flow(stage, preimage)
            self.pause(TIMING['case_hold'])
            self.motion(
                *[FadeOut(item) for item in (output, input_region, left_focus, right_focus, request_label)],
                seconds = TIMING['clear'],
            )

        result = _tex(FORMULAS['indiscrete_result'], position = LAYOUT['footer'])
        self.motion(Succession(FadeOut(stage.footer), FadeIn(result)), seconds = TIMING['formula'])
        stage.footer = result
        self.pause(TIMING['conclusion_hold'])

        # 收束到同一集合上的恒等映射，随后只交换拓扑
        target = _stage('identity')
        self.motion(
            Succession(FadeOut(stage.left_column), FadeIn(target.left_column)),
            ReplacementTransform(stage.edges, target.edges),
            Succession(FadeOut(stage.right.label), FadeIn(target.right.label)),
            Succession(FadeOut(stage.header), FadeIn(target.header)),
            Succession(FadeOut(stage.footer), FadeIn(target.footer)),
            seconds = TIMING['bridge'],
        )
        self.clear()
        self.add(target)
        self.finish_at(target)

class TopologyChangesContinuity(_AnimationTools, Scene):
    def construct(self):
        stage = _stage('identity')
        self.add(stage)
        self.pause(TIMING['join_hold'])
        self.flow(stage)

        # 正向恒等映射：输出只允许空集 / 全集，两种原像都在输入开集族中
        for subset, equality in (
            (MODEL['subsets'][0], 'identity_empty_preimage'),
            (MODEL['subsets'][-1], 'identity_full_preimage'),
        ):
            output = _selection(stage.right, subset, PALETTE['green'])
            input_region = _selection(stage.left, subset, PALETTE['cyan'])
            right_focus = _focus(stage.right_column.lookup[subset], PALETTE['green'])
            left_focus = _focus(stage.left_column.lookup[subset], PALETTE['cyan'])
            equation = _tex(FORMULAS[equality], position = LAYOUT['footer'])
            self.motion(FadeIn(output), Create(right_focus), seconds = TIMING['request'])
            self.motion(
                FadeIn(input_region), Create(left_focus),
                Succession(FadeOut(stage.footer), FadeIn(equation)),
                seconds = TIMING['response'],
            )
            stage.footer = equation
            self.pause(TIMING['case_hold'])
            self.motion(
                *[FadeOut(item) for item in (output, input_region, right_focus, left_focus)],
                seconds = TIMING['clear'],
            )

        result = _tex(FORMULAS['identity_result'], position = LAYOUT['footer'])
        self.motion(Succession(FadeOut(stage.footer), FadeIn(result)), seconds = TIMING['formula'])
        stage.footer = result
        self.pause(TIMING['identity_hold'])
        fixed_rule = _tex(FORMULAS['fixed_rule'], position = LAYOUT['footer'])
        self.motion(Succession(FadeOut(stage.footer), FadeIn(fixed_rule)), seconds = TIMING['formula'])
        stage.footer = fixed_rule
        target = _stage('reversed')

        # 中间的集合、三个图标、三条恒等映射箭头完全不动，只交换两侧开集族
        self.motion(
            ReplacementTransform(stage.left_column, target.right_column, path_arc = -LAYOUT['swap_arc']),
            ReplacementTransform(stage.right_column, target.left_column, path_arc = -LAYOUT['swap_arc']),
            Succession(FadeOut(stage.header), FadeIn(target.header)),
            seconds = TIMING['topology_swap'],
        )
        self.clear()

        # 先保留恒等规则，反例完成后才揭示“不连续”的公式
        target.footer.become(fixed_rule)
        self.add(target)
        self.flow(target)
        indices = MODEL['counterexample']
        output = _selection(target.right, indices, PALETTE['green'])
        input_region = _selection(target.left, indices, PALETTE['yellow'])
        right_focus = _focus(target.right_column.lookup[indices], PALETTE['green'])
        request = _tex(
            FORMULAS['identity_request'], size = LAYOUT['tag_size'],
            position = target.right.center_point + _v(LAYOUT['tag_offset']),
        )
        self.motion(FadeIn(output), Create(right_focus), Write(request), seconds = TIMING['request'])
        self.motion(FadeIn(input_region), seconds = TIMING['response'])
        self.flow(target, indices)

        # 反例公式的两处单点集仍使用图标，不出现 a / b / c
        counterexample = VGroup(
            _tex(FORMULAS['bad_preimage_prefix'], size = LAYOUT['counterexample_size']),
            _subset(indices, height = LAYOUT['counterexample_icon_height'], size = LAYOUT['counterexample_size']),
            _tex(FORMULAS['bad_preimage_middle'], size = LAYOUT['counterexample_size']),
            _subset(indices, height = LAYOUT['counterexample_icon_height'], size = LAYOUT['counterexample_size']),
            _tex(FORMULAS['bad_preimage_suffix'], size = LAYOUT['counterexample_size'], color = PALETTE['error']),
        ).arrange(RIGHT, buff = LAYOUT['counterexample_token_gap']).move_to(_v(LAYOUT['footer']))
        self.motion(Succession(FadeOut(target.footer), FadeIn(counterexample)), seconds = TIMING['formula'])
        self.pause(TIMING['counterexample_hold'])

        # 检查左侧允许的空集 / 全集，突出单点原像没有出现在开集列表中
        for row in target.left_column.rows:
            scan = _focus(row, PALETTE['muted'])
            self.motion(Create(scan), seconds = TIMING['subset_select'])
            self.motion(FadeOut(scan), seconds = TIMING['subset_release'])

        self.pause(TIMING['counterexample_hold'])
        conclusion = _tex(FORMULAS['reversed_footer'], position = LAYOUT['footer'])
        conclusion.set_color_by_tex(r'\notin', PALETTE['error'])
        self.motion(Succession(FadeOut(counterexample), FadeIn(conclusion)), seconds = TIMING['formula'])

        # 末帧保留全部 8 个子集，从上到下完整可读；图标始终是粉色空心轮廓
        self.pause(TIMING['final_hold'])

def validate_parameters():
    # 验证数学内容、所有子集、映射反例和基本可视范围；不产生额外 Scene
    if BG_COLOR != '#000012' or PALETTE['axis'] != '#FFFFFF':
        raise ValueError('背景必须为 #000012；若添加坐标轴，必须使用白色。')
    if TIME_SCALE <= 0 or min(FRAME_WIDTH, FRAME_HEIGHT) <= 0:
        raise ValueError('时长比例与画幅必须为正。')
    if FRAME_RATE is not None and FRAME_RATE <= 0:
        raise ValueError('帧率必须为正或 None。')
    if len(MODEL['letters']) != len(MODEL['kinds']):
        raise ValueError('初始字母与三个图标必须一一对应。')
    if STYLE['edge_stroke'] <= 0 or not 0 < STYLE['edge_opacity'] <= 1:
        raise ValueError('箭头粗度必须为正，透明度应在 0 到 1 之间。')
    
    universe = frozenset(range(len(MODEL['kinds'])))
    powerset = {
        frozenset(c) for length in range(len(universe) + 1)
        for c in itertools.combinations(sorted(universe), length)
    }
    actual = [frozenset(s) for s in MODEL['subsets']]

    if len(actual) != 8 or len(set(actual)) != 8 or set(actual) != powerset:
        raise ValueError('必须按行列全 8 个不同的子集。')
    
    indiscrete = {frozenset(), universe}

    for images in itertools.product(sorted(universe), repeat = len(universe)):
        for subset in powerset:
            if frozenset(_preimage(images, subset)) not in powerset:
                raise ValueError('离散定义域的原像验证失败。')
        if any(frozenset(_preimage(images, s)) not in indiscrete for s in indiscrete):
            raise ValueError('平庸值域的空集 / 全集原像验证失败。')
        
    singleton = frozenset(MODEL['counterexample'])

    if len(singleton) != 1 or singleton in indiscrete:
        raise ValueError('反例应为平庸拓扑中不开放的单点集。')
    if frozenset(_preimage(MODEL['identity_map'], singleton)) != singleton:
        raise ValueError('恒等映射必须保持反例单点集。')
    for key, value in TIMING.items():
        if value <= 0:
            raise ValueError('时长参数必须为正：' + key)
    if LAYOUT['column_gap'] <= LAYOUT['column_icon_height']:
        raise ValueError('子集行距过小。')
    for index in range(len(MODEL['kinds'])):
        icon = _icon(index, LAYOUT['icon_height'])
        if icon.get_fill_opacity() != 0:
            raise ValueError('图标必须无填充。')
        
    return True
