from manim import *
from fractions import Fraction
from functools import lru_cache
import math
import numpy as np

# 所有可调参数
BG_COLOR = "#000012"
TIME_SCALE = 1.0
FRAME_RATE = 60                    # 全片默认60fps，在此调整
FRAME_WIDTH, FRAME_HEIGHT = 128 / 9, 8.0
LEFT_FORMULA_X = -4.55              # 左上两行红色公式共用的左边界
PALETTE = dict(
    axis = "#FFFFFF",
    ink = "#FFFFFF",
    cyan = "#56CEE8",
    green = "#9EE3A2",
    yellow = "#E8EE63",
    rose = "#EF819B",
    epsilon = "#FFE17D",
    safe = "#68E6C0",
    flash = "#FF526E",
)
LAYOUT = dict(
    # x轴比旧版上移0.8；字幕区域 y<=-2.45 保持空白
    origin = (-5.35, -1.75, 0),
    x_range = (0, 1.05, 0.1),
    y_range = (0, 1.08, 0.2),
    x_length = 11.55,
    y_length = 4.428,
    axis_width = 2.0,
    tick_size = 0.045,
    tick_label_gap = 0.19,
    axis_label_gap = 0.18,
    label_size = 24,
    y_axis_label_y = 2.82,
    definition_position = (0, 3.04, 0),
    definition_size = 32,
    opening_scale = 1.40,
    hud_top = (0, 3.10, 0),
    hud_left = (LEFT_FORMULA_X, 3.12, 0),
    hud_right = (3.70, 3.12, 0),
    hud_second = (0, 2.23, 0),
    row_position = (LEFT_FORMULA_X, 2.23, 0),
    count_position = (3.65, 2.23, 0),
    hud_size = 34,
    small_size = 28,
    max_formula_width = 12.2,
    row_max_width = 5.9,
    count_max_width = 3.6,
    plot_top = 2.60,
    plot_half_width = 6.65,
    baseline_screen_y = -1.75,
    subtitle_top = -2.45,
    point_label_gap = 0.18,
    point_label_size = 29,
    delta_label_y = 1.90,
    delta_label_size = 23,
    path_tolerance = 1e-10,
    plot_left = -5.35,
    plot_right = 6.20,
    x_number_y = -2.10,
    y_number_right = -5.73,
    question_position = (0, 0, 0),
    question_size = 56,
    question_scale = 1.8,
)
# 与part_one.py连续性分镜相同的数字排版、1/2/5十进制刻度及渐变方式
TICKS = dict(
    initial_precision = 1.0,
    max_precision = 8,
    font_size = 26,
    digit_spacing = 1.18,
    decimal_spacing = 0.45,
    minus_spacing = 0.85,
    decimal_drop = 0.070,
    cache_size = 1024,
    min_spacing_x = 1.38,
    min_spacing_y = 0.68,
    label_gap = 0.16,
    fade_width_x = 0.75,
    fade_width_y = 0.38,
    length = 0.075,
    width = 1.4,
    pool = 32,
    number_slots = 13,
)
# 实时公式复用刻度的数字字形；分母和N随同一个epsilon连续更新
READOUT = dict(
    denominator_places = 2,
    fraction_scale = 1.0,
    fraction_offset = 0.25,
    fraction_padding = 0.10,
    prefix_gap = 0.12,
    fraction_width = 1.4,
    integer_tolerance = 1e-9,
)
POINTS = dict(
    # radius统一控制所有普通点与开场示例；marker_radius只控制红色标记
    overview_q = 64,
    radius = 0.040,
    marker_radius = 0.068,
    opacity = 0.95,
    color_bands = 18,
    pixel_dedup = 0.056,
    max_local_points = 2600,
    exact_local_q = 512,
    denominator_samples = 2000,
    detail_reveal_portion = 0.30,
    circle_components = 5,          # 四段三次Bezier圆；每个点固定独立轮廓
    path_min_samples = 8,
    path_step_ratio = 1.40,
    path_max_samples = 24,
    draw_grid = 0.012,              # 仅省略同色点在子像素格内的重复绘制
)
STORY = dict(
    a = math.sqrt(2) / 2,
    a_tex = r"\frac{\sqrt2}{2}",
    examples = ((1, 2), (1, 3), (2, 3), (3, 10)),
    # (观察位置, 镜头倍率, 最大显示分母)，没有额外标记点或说明公式
    tour = ((0.23, 4.5, 420), (0.57, 8.0, 900), (0.83, 13.0, 1500)),
    epsilon_values = (Fraction(50, 257), Fraction(1, 10), Fraction(1, 100)),
    delta_safety = 0.80,
    initial_delta_multiplier = 1.60,
    # 摄像机放大负责纵向视野；统一横坐标变换负责拉开点距
    epsilon_height_fraction = 0.29,
    safe_screen_width = 1.30,  # 黄线占纵轴高度，最大1/3
    horizontal_expansion = True,
    proof_q = (500, 1300, 6000),
    local_margin = 1.20,
    rational_question = Fraction(1, 2),
)
STYLE = dict(
    epsilon_width = 2.5,
    guide_width = 1.8,
    write_width = 2.0,
    safe_fill = 0.12,
    safe_label_gap = 0.08,
    flash_radius = 0.09,
    flash_length = 0.14,
    flash_lines = 10,
    flash_width = 2.8,
    flash_time_width = 0.65,
    open_end_radius = 0.043,
    endpoint_width = 1.6,
    count_flash_buff = 0.18,
    count_flash_width = 3.0,
    count_flash_time_width = 0.18,
)
TIMING = dict(
    formula = 1.6,
    opening_hold = 1.3,
    formula_up = 1.7,
    axes = 1.3,
    mapping = 1.35,
    mapping_hold = 1.0,
    reveal = 1.5,
    point_row_first = 0.62,
    point_row_last = 0.05,  # 同高度逐排出现，排间隔由慢到快
    fade = 0.65,
    hold = 1.4,
    long_hold = 2.4,
    short_hold = 0.55,
    zoom = 3.5,
    proof_zoom = 4.3,
    return_zoom = 2.8,
    tour_return = 2.2,
    threshold = 1.7,
    row = 1.1,
    row_hold = 0.9,
    shrink = 2.0,
    conclusion = 1.7,
    count_flash = 1.6,
)

config.background_color = BG_COLOR
config.frame_width, config.frame_height = FRAME_WIDTH, FRAME_HEIGHT
config.frame_rate = FRAME_RATE

def _precise_equal(p0, p1):
    tol = LAYOUT["path_tolerance"]

    if np.ndim(p0) == 1:
        return abs(p0[0] - p1[0]) <= tol and abs(p0[1] - p1[1]) <= tol
    
    return bool(np.all(np.abs(np.asarray(p0) - np.asarray(p1)) <= tol))

def _tex(text, size = None, color = None, width = None):
    m = MathTex(text, font_size = size or LAYOUT["hud_size"], color = color or PALETTE["ink"])
    limit = width or LAYOUT["max_formula_width"]

    if m.width > limit:
        m.scale_to_fit_width(limit)

    # 防止 Manim 0.18 在镜头缩放时把字形的独立轮廓误合并
    for part in m.get_family():
        if isinstance(part, VMobject):
            part.consider_points_equals = _precise_equal
            part.consider_points_equals_2d = _precise_equal

    return m

@lru_cache(maxsize = 32)
def _fractions(qmax, lo = 0.0, hi = 1.0):

    return tuple((p, q)
                 
        for q in range(1, int(qmax) + 1)
        for p in range(max(0, math.ceil(lo * q)), min(q, math.floor(hi * q)) + 1)
        if math.gcd(p, q) == 1)


def _safe_data(epsilon):
    epsilon = Fraction(epsilon)

    if not (0 < epsilon <= 1 and 0 < STORY["a"] < 1 and 0 < STORY["delta_safety"] < 1):
        raise ValueError("Require 0<epsilon<=1, 0<a<1 and 0<delta_safety<1.")
    
    n = epsilon.denominator // epsilon.numerator
    bad = _fractions(n)  # 包括 1/q 恰等于 epsilon 的点。
    nearest = min(bad, key = lambda pq: abs(pq[0] / pq[1] - STORY["a"]))
    distance = abs(nearest[0] / nearest[1] - STORY["a"])
    delta = STORY["delta_safety"] * min(distance, STORY["a"], 1 - STORY["a"])

    if delta <= 0:
        raise ValueError("The chosen a must avoid all forbidden rational points.")
    
    return n, bad, nearest, delta

@lru_cache(maxsize = 8)
def _proof_profile(qmax):
    # 完整[0,1]计数，以及每个分母上界对应的安全半径，不用可见点估计
    rows = [[] for _ in range(qmax + 1)]

    for p, q in _fractions(qmax):
        rows[q].append(p / q)

    counts, radii = [0], [0.0]
    total, distance = 0, min(STORY["a"], 1 - STORY["a"])

    for row in rows[1:]:
        total += len(row)
        distance = min(distance, *(abs(x - STORY["a"]) for x in row))
        counts.append(total)
        radii.append(STORY["delta_safety"] * distance)

    return tuple(counts), tuple(radii)

class _PointBatch(VMobject):
    # 每个点有固定轮廓边界，缩放时不靠浮点相等来重新切分
    def __init__(self, points_per_dot, **kwargs):
        super().__init__(**kwargs)
        self.points_per_dot = points_per_dot

    def gen_subpaths_from_points_2d(self, points):

        return iter(points.reshape(-1, self.points_per_dot, 3))

    def get_subpaths_from_points(self, points):

        return list(points.reshape(-1, self.points_per_dot, 3))

class _TickTypography:
    # 复用part_one的数位间距和小数点高度；动画中不重复编译TeX
    def __init__(self):
        glyphs = {ch: _tex(ch, TICKS["font_size"], PALETTE["axis"]).move_to(ORIGIN) for ch in "0123456789.-"}
        self.advance = max(glyphs[ch].width for ch in "0123456789") * TICKS["digit_spacing"]
        self.glyphs = {ch: glyph.get_all_points().copy() for ch, glyph in glyphs.items()}
        self.cache = {}

    def layout(self, text):

        if text not in self.cache:
            cursor, paths = 0.0, []

            for ch in text:
                advance = self.advance

                if ch == ".":
                    advance *= TICKS["decimal_spacing"]
                elif ch == "-":
                    advance *= TICKS["minus_spacing"]

                drop = TICKS["decimal_drop"] if ch == "." else 0.0
                paths.append(self.glyphs[ch] + np.array([cursor + advance / 2, -drop, 0]))
                cursor += advance

            all_points = np.concatenate(paths)
            low, high = all_points.min(axis = 0), all_points.max(axis = 0)
            origin = np.array([low[0], (low[1] + high[1]) / 2, 0])

            if len(self.cache) >= TICKS["cache_size"]:
                self.cache.pop(next(iter(self.cache)))

            self.cache[text] = ([path - origin for path in paths], high - low)

        return self.cache[text]

class _NumberReadout(VGroup):
    # 保留字形对象身份，避免Cairo残影；新增加的小数位单独渐显
    def __init__(self, typography, color = None):
        super().__init__(*[VMobject(fill_color = color or PALETTE["axis"], fill_opacity = 1, stroke_width = 0) for _ in range(TICKS["number_slots"])])

        for slot in self:
            slot.consider_points_equals = _precise_equal
            slot.consider_points_equals_2d = _precise_equal

        self.typography = typography
        self.last_text = None

    def display(self, text, center, scale, reference_width, opacity, prefix_length, trailing_opacity, align_right = False, reset_opacity = True):

        if len(text) > len(self):
            raise ValueError("Increase TICKS['number_slots'] for this range.")
        
        paths, self.text_extent = self.typography.layout(text)
        self.last_text = text
        origin = center - RIGHT * reference_width * scale * (1 if align_right else 0.5)

        for i, slot in enumerate(self):
            if i < len(paths):
                slot.set_points(paths[i] * scale + origin)
                if reset_opacity:
                    slot.set_fill(opacity = opacity if i < prefix_length else trailing_opacity)
            else:
                slot.set_points(np.empty((0, 3)))

        return self

def _tick_smooth(value):
    t = float(np.clip(value, 0, 1))

    return t * t * (3 - 2 * t)

def _tick_density(places, screen_unit, axis, min_spacing = None):
    separation = TICKS["min_spacing_" + axis] if min_spacing is None else min_spacing
    desired = max(1.0, separation / (10.0 ** (-places) * screen_unit))

    if desired <= 1:
        return [(1, 1.0)]
    
    power = int(math.floor(math.log10(desired)))
    candidates = sorted({
        int(multiplier * 10 ** exponent)
        for exponent in range(max(0, power - 1), power + 2)
        for multiplier in (1, 2, 5, 10)
    })
    lower = max(n for n in candidates if n <= desired)
    upper = min(n for n in candidates if n > desired)
    weight = _tick_smooth(math.log(desired / lower) / math.log(upper / lower))

    return [(lower, 1 - weight), (upper, weight)]

def _tick_text(integer, places):
    sign = "-" if integer < 0 else ""
    digits = str(abs(integer)).zfill(places + 1)

    return sign + (digits[:-places] + "." + digits[-places:] if places else digits)

class _RiemannAnimator:
    # 公共绘图工具，不是 Scene，不出现在场景选择器中
    def __init__(self, scene):
        self.scene = scene
        self.camera.background_color = BG_COLOR
        self.camera.frame.set(width = FRAME_WIDTH).move_to(ORIGIN)
        self.x_stretch = ValueTracker(1.0)
        self.install_point_clip()

    def install_point_clip(self):
        # 原生矢量裁切，不加遮挡板；点离开视窗时保持真实大小
        display = self.camera.display_vectorized
        def clipped_display(mob, ctx):

            if not getattr(mob, "_riemann_point", False):
                return display(mob, ctx)
            
            s, c = self.scale_factor(), self.camera.frame.get_center()
            left, right = LAYOUT["plot_left"], LAYOUT["plot_right"]
            bottom, top = LAYOUT["baseline_screen_y"], LAYOUT["plot_top"]

            # 红色a标记是横轴上的指示器；普通函数点严格裁切
            if getattr(mob, "_baseline_marker", False):
                bottom -= POINTS["marker_radius"]

            ctx.save()

            try:
                ctx.new_path()
                ctx.rectangle(c[0] + left * s, c[1] + bottom * s, (right - left) * s, (top - bottom) * s)
                ctx.clip()
                return display(mob, ctx)
            finally:
                ctx.restore()

        self.camera.display_vectorized = clipped_display

    def __getattr__(self, name):

        return getattr(self.scene, name)

    def beat(self, *animations, duration = "reveal", moving_graph = False, **kwargs):
        seconds = TIMING[duration] if isinstance(duration, str) else duration

        # 图形不动时暂停位置更新；公式/闪光仍正常动画，减少静止点的更新计算
        frozen = [] if moving_graph else [getattr(self, name, None) for name in ("axis_art", "cloud")]
        frozen = [m for m in frozen if m is not None]

        for m in frozen:
            m.suspend_updating()

        try:
            self.play(*animations, run_time = seconds * TIME_SCALE, **kwargs)
        finally:
            for m in frozen:
                m.resume_updating()

    def pause(self, duration = "hold"):
        self.wait(TIMING[duration] * TIME_SCALE)

    def scale_factor(self):

        return self.camera.frame.width / FRAME_WIDTH

    def write(self, mob):

        return Write(mob, stroke_width = STYLE["write_width"] * self.scale_factor())

    def hud(self, text, position = None, color = None, size = None, width = None, align_left = False):
        # 完全没有背景矩形；所有 HUD 位于图形上方的独立留白区域
        mob = _tex(text, size, color, width)
        original_width = mob.width
        pos = np.array(position if position is not None else LAYOUT["hud_top"])

        def update(m):
            s = self.scale_factor()
            m.set(width = original_width * s)
            m.move_to(self.camera.frame.get_center() + pos * s)

            if align_left:
                m.shift(RIGHT * original_width * s / 2)

        mob.add_updater(update)
        mob.set_z_index(30)
        update(mob)

        return mob

    def live_proof_formula(self, epsilon, kind, count_progress = None):
        # 固定字形槽，公式全程留在顶部；仅更新数字轮廓和镜头补偿
        typography = self.number_typography
        max_denominator = math.ceil(max(1 / float(eps) for eps in STORY["epsilon_values"]))
        counts, _ = _proof_profile(max_denominator + 1)
        is_epsilon = kind == "epsilon"
        color = PALETTE["epsilon" if is_epsilon else "rose"]
        size = LAYOUT["hud_size" if is_epsilon else "small_size"]
        prefix = _tex(r"\varepsilon=" if is_epsilon else r"N_{\ge\varepsilon}=", size, color).move_to(ORIGIN)
        digits = _NumberReadout(typography, color)
        number_scale = size / TICKS["font_size"] * (READOUT["fraction_scale"] if is_epsilon else 1)
        reserve = "8" * len(str(max_denominator if is_epsilon else counts[max_denominator]))

        if is_epsilon and READOUT["denominator_places"]:
            reserve += "." + "8" * READOUT["denominator_places"]

        number_width = typography.layout(reserve)[1][0] * number_scale
        fraction_width = number_width + 2 * READOUT["fraction_padding"] if is_epsilon else number_width
        prefix_width = prefix.width
        total_width = prefix_width + READOUT["prefix_gap"] + fraction_width
        fit = 1 if is_epsilon else min(1, LAYOUT["count_max_width"] / total_width)
        stage_denominators = tuple(1 / float(eps) for eps in STORY["epsilon_values"])
        anchor_width = total_width

        if is_epsilon:
            initial_text = f"{stage_denominators[0]:.{READOUT['denominator_places']}f}"

            if READOUT["denominator_places"]:
                initial_text = initial_text.rstrip("0").rstrip(".")

            anchor_width = (prefix_width + READOUT["prefix_gap"] + typography.layout(initial_text)[1][0] * number_scale + 2 * READOUT["fraction_padding"])

        prefix_x = -anchor_width / 2 + prefix_width / 2
        number_left = -anchor_width / 2 + prefix_width + READOUT["prefix_gap"]
        parts = [(prefix, 0)]
        group = VGroup(prefix, digits)
        rule = None

        if is_epsilon:
            numerator = _tex("1", size * READOUT["fraction_scale"], color).move_to(ORIGIN)
            rule = Line(LEFT, RIGHT, color = color, stroke_width = READOUT["fraction_width"])
            parts.append((numerator, READOUT["fraction_offset"]))
            group.add(numerator, rule)
            number_y = -READOUT["fraction_offset"]
        else:
            number_y = (prefix.height - typography.layout("8")[1][1] * number_scale) / 2

        templates = [(piece, piece.points.copy(), y, part is prefix) for part, y in parts for piece in part.family_members_with_points()]
        position = np.array(LAYOUT["hud_right" if is_epsilon else "count_position"])

        def update(m):
            denominator = 1 / epsilon.get_value()

            if is_epsilon:
                unit = 10 ** READOUT["denominator_places"]
                value = math.floor(denominator * unit + READOUT["integer_tolerance"]) / unit
                text = f"{value:.{READOUT['denominator_places']}f}"
                # 运动中保留小数位，避免每逢整数就缩短再拉长；仅阶段终点简写
                settled = any(abs(denominator - target) <= READOUT["integer_tolerance"] for target in stage_denominators)

                if settled and READOUT["denominator_places"]:
                    text = text.rstrip("0").rstrip(".")
            else:
                n = min(len(counts) - 1, max(1, math.floor(denominator + READOUT["integer_tolerance"])))
                value = counts[n] if count_progress is None or count_progress.get_value() < 0 else round(count_progress.get_value())
                text = str(value)

            s, camera_center = self.scale_factor(), self.camera.frame.get_center()
            center = camera_center + position * s
            width = typography.layout(text)[1][0]
            current_fraction_width = width * number_scale + (2 * READOUT["fraction_padding"] if is_epsilon else 0)

            # 等号位置固定；数字紧接等号，随实际位数向右扩展，不预留空白数字槽
            current_number_x = number_left + current_fraction_width / 2

            for piece, points, y, is_prefix in templates:
                x = prefix_x if is_prefix else current_number_x
                piece.set_points((points + np.array([x, y, 0])) * fit * s + center)

            digits.display(text, center + np.array([current_number_x, number_y, 0]) * fit * s, number_scale * fit * s, width, 1, len(text), 1, reset_opacity = False)
            
            if rule is not None:
                rule.put_start_and_end_on(
                    center + np.array([current_number_x - current_fraction_width / 2, 0, 0]) * s,
                    center + np.array([current_number_x + current_fraction_width / 2, 0, 0]) * s
                )
                rule.set_stroke(width = READOUT["fraction_width"] * s)
            m.numeric_value = value

        group.set_z_index(30)
        group.add_updater(update)
        update(group)

        return group

    def point(self, x, y):
        a = STORY["a"]

        return self.axes.c2p(a + (x - a) * self.x_stretch.get_value(), y)

    def screen_point(self, x, y):

        return (self.point(x, y) - self.camera.frame.get_center()) / self.scale_factor()

    def screen_to_data(self, screen_x, screen_y):
        s, c = self.scale_factor(), self.camera.frame.get_center()
        origin = self.axes.c2p(0, 0)
        stretched_x = (c[0] + screen_x * s - origin[0]) / self.unit_x
        x = STORY["a"] + (stretched_x - STORY["a"]) / self.x_stretch.get_value()
        y = (c[1] + screen_y * s - origin[1]) / self.unit_y

        return x, y

    def pin(self, x, y = 0, color = None, radius = None):
        r = radius or POINTS["marker_radius"]
        dot = Dot(radius = r, color = color or PALETTE["rose"]).set_z_index(14)
        dot._riemann_point = True
        dot._baseline_marker = y == 0

        def update(m):
            s = self.scale_factor()
            value = x.get_value() if isinstance(x, ValueTracker) else x
            m.set(width = 2 * r * s).move_to(self.point(value, y))

        dot.add_updater(update)
        update(dot)

        return dot

    def point_label(self, text, x, y, color = None):
        m = _tex(text, LAYOUT["point_label_size"], color)
        width0, height0 = m.width, m.height

        def update(label):
            s = self.scale_factor()
            p = self.screen_point(x, y)
            label.set(width = width0 * s)
            label.move_to(self.point(x, y) + UP * (LAYOUT["point_label_gap"] + height0 / 2) * s)
            visible = (p[1] + LAYOUT["point_label_gap"] + height0 < LAYOUT["plot_top"] and abs(p[0]) + width0 / 2 < LAYOUT["plot_half_width"])

            if getattr(label, "_visible_flag", None) != visible:
                label.set_opacity(1 if visible else 0)
                label._visible_flag = visible

        m.add_updater(update)
        m.set_z_index(20)
        update(m)

        return m

    def initialize(self, empty = False):
        self.clear()
        self.x_stretch.set_value(1)
        self.camera.frame.set(width = FRAME_WIDTH).move_to(ORIGIN)
        self.axes = Axes(
            x_range = LAYOUT["x_range"], y_range = LAYOUT["y_range"],
            x_length = LAYOUT["x_length"], y_length = LAYOUT["y_length"],
            tips = False, axis_config = dict(include_ticks = False, color = PALETTE["axis"])
        )
        self.axes.shift(np.array(LAYOUT["origin"]) - self.axes.c2p(0, 0))
        self.unit_x = np.linalg.norm(self.axes.c2p(1, 0) - self.axes.c2p(0, 0))
        self.unit_y = np.linalg.norm(self.axes.c2p(0, 1) - self.axes.c2p(0, 0))
        self.palette = color_gradient([PALETTE["cyan"], PALETTE["green"], PALETTE["yellow"]], POINTS["color_bands"])
        self.known_points = set()
        self.cloud = VGroup().set_z_index(6)
        self.axis_art = self.make_live_axes()
        self.definition = _tex(
            r"R(x)=\begin{cases}\dfrac1q,&x=\dfrac pq,\ \gcd(p,q)=1,\ q\in\mathbb N\\[3pt]"
            r"0,&x\notin\mathbb Q\end{cases}", LAYOUT["definition_size"]
        ).move_to(LAYOUT["definition_position"]).set_z_index(20)
        self.base = VGroup(self.axis_art, self.cloud)

        if not empty:
            self.append_points(_fractions(POINTS["overview_q"]))

    def make_live_axes(self):
        typography, pool = _TickTypography(), TICKS["pool"]
        self.number_typography = typography
        lines = VGroup(Line(), Line())
        ticks = VGroup(*[Line() for _ in range(2 * pool)])
        xnums = VGroup(*[_NumberReadout(typography) for _ in range(pool)])
        ynums = VGroup(*[_NumberReadout(typography) for _ in range(pool)])
        xlabel, ylabel = _tex("x", LAYOUT["small_size"]), _tex("R(x)", LAYOUT["small_size"])
        widths = (xlabel.width, ylabel.width)
        group = VGroup(lines, ticks, xnums, ynums, xlabel, ylabel).set_z_index(8)

        def update(m):
            lines, ticks, xnums, ynums, xlabel, ylabel = m
            scale, center = self.scale_factor(), self.camera.frame.get_center()

            def pos(x, y):

                return center + np.array([x, y, 0]) * scale
            
            left, right, bottom, top = (LAYOUT[k] for k in ("plot_left", "plot_right", "baseline_screen_y", "plot_top"))
            lines[0].put_start_and_end_on(pos(left, bottom), pos(right, bottom))
            lines[1].put_start_and_end_on(pos(left, bottom), pos(left, top))
            lines.set_stroke(PALETTE["axis"], width = LAYOUT["axis_width"] * scale)

            for axis, name, labels, gain, unit, lo, hi in (
                (0, "x", xnums, self.x_stretch.get_value() / scale, self.unit_x, left, right),
                (1, "y", ynums, 1 / scale, self.unit_y, bottom, top),
            ):
                precision = float(np.clip(TICKS["initial_precision"] + math.log10(max(gain, 1e-12)), TICKS["initial_precision"], TICKS["max_precision"]))
                lower = math.floor(precision)
                upper = min(lower + 1, TICKS["max_precision"])
                blend = _tick_smooth(precision - lower)
                places = upper if blend > 0 else lower
                actual_low = self.screen_to_data(left, bottom)[axis]
                actual_high = self.screen_to_data(right, top)[axis]
                separation = TICKS["min_spacing_" + name]

                if axis == 0:
                    widest = max(typography.layout(f"{v:.{places}f}")[1][0] for v in (actual_low, actual_high, (actual_low + actual_high) / 2))
                    separation = max(separation, math.sqrt(2.5) * (widest + TICKS["label_gap"]))

                density = _tick_density(places, unit * gain, name, separation)
                values = {}

                for layer, (multiplier, weight) in enumerate(density):
                    # 2与5两种网格并不嵌套；旧网格先淡出，再引入新网格
                    # 两种网格共有的刻度始终保留，避免0.14、0.15、0.16挤在一起
                    phase = _tick_smooth(2 * weight - 1) if len(density) == 2 else 1.0
                    step = multiplier * 10.0 ** (-places)
                    first = math.ceil(actual_low / step - 1e-8)
                    last = math.floor(actual_high / step + 1e-8)

                    for index in range(first, last + 1):
                        key = index * multiplier * 10 ** (TICKS["max_precision"] - places)
                        entry = values.setdefault(key, [0.0, 0])
                        entry[0] = max(entry[0], phase)
                        entry[1] |= 1 << layer

                if len(values) > pool:
                    raise ValueError("Increase TICKS['pool'] for this axis range.")
                
                for i in range(pool):
                    ticks[axis * pool + i].set_stroke(opacity = 0)
                    labels[i].set_opacity(0)

                for i, (key, (phase, membership)) in enumerate(sorted(values.items())):
                    value = key * 10.0 ** (-TICKS["max_precision"])
                    location = self.screen_point(value, 0)[0] if axis == 0 else self.screen_point(0, value)[1]
                    text = _tick_text(key // 10 ** (TICKS["max_precision"] - places), places)
                    old_text, new_text = f"{value:.{lower}f}", f"{value:.{upper}f}"
                    old_width = typography.layout(old_text)[1][0]
                    new_width = typography.layout(new_text)[1][0]
                    reference_width = (1 - blend) * old_width + blend * new_width
                    extent = typography.layout(text)[1]
                    edge = min(location - lo, hi - location)
                    fade_width = TICKS["fade_width_" + name]
                    edge_fade = _tick_smooth(edge / fade_width)
                    half_extent = max(reference_width, extent[0]) / 2 if axis == 0 else extent[1] / 2
                    label_fade = _tick_smooth((edge - half_extent) / fade_width)
                    density_opacity = 1.0 if membership == 3 else phase
                    old_grid = key % 10 ** (TICKS["max_precision"] - lower) == 0
                    opacity = density_opacity * (1.0 if old_grid else blend)
                    tick, label = ticks[axis * pool + i], labels[i]
                    t = TICKS["length"]

                    if axis == 0:
                        tick.put_start_and_end_on(pos(location, bottom - t), pos(location, bottom + t))
                        label_position = pos(location, LAYOUT["x_number_y"])
                    else:
                        tick.put_start_and_end_on(pos(left - t, location), pos(left + t, location))
                        label_position = pos(LAYOUT["y_number_right"], location)

                    tick.set_stroke(PALETTE["axis"], width = TICKS["width"] * scale, opacity = opacity * edge_fade)
                    prefix = len(old_text) if places == upper and upper != lower else len(text)
                    label.display(text, label_position, scale, reference_width, opacity * label_fade, prefix, density_opacity * blend * label_fade, align_right = axis == 1)

            xlabel.set(width = widths[0] * scale).move_to(pos(right + LAYOUT["axis_label_gap"], bottom))
            ylabel.set(width = widths[1] * scale).move_to(pos(left, LAYOUT["y_axis_label_y"]))

        group.add_updater(update)
        update(group)

        return group

    def intro(self, show_cloud = True):
        self.definition.scale(LAYOUT["opening_scale"]).move_to(ORIGIN)
        self.beat(self.write(self.definition), duration = "formula")
        self.pause("opening_hold")
        self.beat(self.definition.animate.scale(1 / LAYOUT["opening_scale"]).move_to(LAYOUT["definition_position"]), duration = "formula_up")
        self.beat(FadeIn(self.axis_art), duration = "axes")

        if show_cloud:
            self.beat(FadeIn(self.cloud))
            self.pause("short_hold")

    def start(self, with_intro = True):
        # 只有第一镜播放中央定义式；其余独立Scene直接进入图形
        if with_intro or not hasattr(self, "axes"):
            self.initialize()
            self.add(self.axis_art, self.cloud)
            self.pause("short_hold")
        elif self.definition in self.mobjects:
            self.beat(FadeOut(self.definition), duration = "fade")

    def point_color(self, x):

        return self.palette[min(len(self.palette) - 1, max(0, int(x * len(self.palette))))]

    def sample_detail(self, qmax, zoom, center_x, stretch, known = None):
        # 仅筛选新增点；已出现的最简分数身份永不删除，也不重新采样
        half = FRAME_WIDTH / zoom / self.unit_x / stretch / 2 * STORY["local_margin"]
        lo, hi = max(0, center_x - half), min(1, center_x + half)
        known = self.known_points if known is None else known
        ymax = (LAYOUT["plot_top"] - LAYOUT["baseline_screen_y"]) / zoom / self.unit_y
        exact = min(qmax, POINTS["exact_local_q"])
        qs = list(range(1, exact + 1))

        if qmax > exact:
            qs += list(np.unique(np.geomspace(exact + 1, qmax, POINTS["denominator_samples"]).astype(int)))

        seen, selected = set(), []

        for p, q in known:
            if lo <= p / q <= hi and 1 / q <= ymax:
                seen.add((round((p / q - lo) * self.unit_x * stretch * zoom / POINTS["pixel_dedup"]), round(self.unit_y * zoom / q / POINTS["pixel_dedup"])))
                
        for q in qs:
            if 1 / q > ymax:
                continue
            for p in range(max(0, math.ceil(lo * q)), min(q, math.floor(hi * q)) + 1):
                if math.gcd(p, q) != 1 or (p, q) in known:
                    continue
                key = (round((p / q - lo) * self.unit_x * stretch * zoom / POINTS["pixel_dedup"]),
                       round(self.unit_y * zoom / q / POINTS["pixel_dedup"]))
                if key in seen:
                    continue
                seen.add(key)
                selected.append((p, q))
                if len(selected) >= POINTS["max_local_points"]:
                    return selected
                
        return selected

    def prepare_motion(self, width0, center0, stretch0, target_width, target_x, target_stretch, qmax, anchor_x = None):
        # 对实际相机轨迹预补样，而不只对终点取样；复位时同样调用
        zoom0, zoom1 = FRAME_WIDTH / width0, FRAME_WIDTH / target_width
        ratio = max(zoom0 / zoom1, zoom1 / zoom0, zoom0 * stretch0 / (zoom1 * target_stretch), zoom1 * target_stretch / (zoom0 * stretch0))
        steps = int(np.clip(math.ceil(math.log(max(1, ratio)) / math.log(POINTS["path_step_ratio"])) + 1, POINTS["path_min_samples"], POINTS["path_max_samples"]))
        known, additions = set(self.known_points), []
        origin = self.axes.c2p(0, 0)
        density = max(self.unit_y / POINTS["radius"], qmax / max(zoom0, zoom1))

        if anchor_x is not None:
            def anchor_world(stretch):

                return origin[0] + self.unit_x * (STORY["a"] + (anchor_x - STORY["a"]) * stretch)
            
            screen0 = (anchor_world(stretch0) - center0[0]) * zoom0
            screen1 = (anchor_world(target_stretch) - target_x) * zoom1

        for t in np.linspace(0, 1, steps):
            zoom = zoom0 * math.exp(math.log(zoom1 / zoom0) * t)
            stretch = stretch0 * math.exp(math.log(target_stretch / stretch0) * t)
            camera_x = (1 - t) * center0[0] + t * target_x

            if anchor_x is not None:
                camera_x = anchor_world(stretch) - ((1 - t) * screen0 + t * screen1) / zoom

            x = STORY["a"] + ((camera_x - origin[0]) / self.unit_x - STORY["a"]) / stretch
            samples = self.sample_detail(max(POINTS["overview_q"], math.ceil(density * zoom)), zoom, x, stretch, known = known)
            known.update(samples)
            additions.extend(samples)

        return self.append_points(additions, opacity = 0)

    def append_points(self, samples, opacity = 1.0, row_births = None, row_clock = None):
        samples = [pq for pq in dict.fromkeys(samples) if pq not in self.known_points]
        self.known_points.update(samples)
        reveal = ValueTracker(opacity)
        layer = VGroup()
        bands = {}

        for p, q in samples:
            band = min(POINTS["color_bands"] - 1, int(p / q * POINTS["color_bands"]))
            radius = POINTS["radius"]
            birth = 0.0 if row_births is None else row_births[q]
            bands.setdefault((band, radius), []).append((p / q, 1 / q, birth))

        template = Circle(radius = 1, num_components = POINTS["circle_components"]).points
        origin = self.axes.c2p(0, 0)

        for (band, radius), coords in bands.items():
            data = np.array(coords)
            mob = _PointBatch(len(template), fill_color = self.palette[band], stroke_width = 0)
            mob._riemann_point = True
            mob.consider_points_equals = _precise_equal
            mob.consider_points_equals_2d = _precise_equal

            def update(m, data = data, radius = radius):
                scale, center = self.scale_factor(), self.camera.frame.get_center()
                points = np.zeros((len(data), 3))
                points[:, 0] = origin[0] + self.unit_x * (STORY["a"] + (data[:, 0] - STORY["a"]) * self.x_stretch.get_value())
                points[:, 1] = origin[1] + self.unit_y * data[:, 1]
                screen = (points - center) / scale
                pad = POINTS["marker_radius"] + radius
                visible = (
                    (screen[:, 0] >= LAYOUT["plot_left"] - pad) &
                    (screen[:, 0] <= LAYOUT["plot_right"] + pad) &
                    (screen[:, 1] <= LAYOUT["plot_top"] + radius) &
                    (screen[:, 1] >= LAYOUT["baseline_screen_y"] - pad)
                )
                if row_clock is not None:
                    visible &= data[:, 2] <= row_clock.get_value()
                centers = points[visible]

                # 只跳过已被同色同大小圆覆盖的子像素重复绘制；真实点身份仍完整保留
                cells = np.floor(screen[visible, :2] / POINTS["draw_grid"]).astype(np.int64)

                if len(cells):
                    _, chosen = np.unique(cells, axis = 0, return_index = True)
                    centers = centers[np.sort(chosen)]

                m.set_points((centers[:, None, :] + template[None, :, :] * radius * scale).reshape(-1, 3))
                m.set_fill(opacity = POINTS["opacity"] * reveal.get_value())

            mob.add_updater(update)
            update(mob)
            layer.add(mob)

        self.cloud.add(layer)

        return reveal

    def hide_overview_labels(self):
        # 刻度保留并持续更新；这里只收起定义式
        if self.definition in self.mobjects:
            self.beat(FadeOut(self.definition), duration = "fade")

    def zoom_view(self, zoom, center_x, qmax, stretch = 1, duration = "zoom", changes = ()):
        width0, center0 = self.camera.frame.width, self.camera.frame.get_center().copy()
        stretch0 = self.x_stretch.get_value()
        states = [(tracker, tracker.get_value(), target) for tracker, target in changes]
        target_x = self.axes.c2p(center_x, 0)[0]
        reveal = self.prepare_motion(width0, center0, stretch0, FRAME_WIDTH / zoom, target_x, stretch, qmax)

        def camera_motion(frame, alpha):
            t = smootherstep(alpha)
            width = width0 * math.exp(math.log((FRAME_WIDTH / zoom) / width0) * t)
            frame.set(width = width)
            self.x_stretch.set_value(stretch0 * math.exp(math.log(stretch / stretch0) * t))

            for tracker, initial, target in states:
                tracker.set_value(initial * math.exp(math.log(target / initial) * t))

            y = self.axes.c2p(0, 0)[1] - LAYOUT["baseline_screen_y"] * width / FRAME_WIDTH
            frame.move_to([(1 - t) * center0[0] + t * target_x, y, 0])
            reveal.set_value(smooth(min(1, alpha / POINTS["detail_reveal_portion"])))

        self.beat(UpdateFromAlphaFunc(self.camera.frame, camera_motion), duration = duration, rate_func = linear, moving_graph = True)
        reveal.set_value(1)

        for tracker, initial, target in states:
            tracker.set_value(target)

    def restore(self, formula = False, duration = "return_zoom", retain = ()):
        # 指定保留对象一直跟随复原镜头，复原后再收起
        keep = {id(self.axis_art), id(self.cloud), id(self.camera.frame), *(id(m) for m in retain)}

        if formula:
            keep.add(id(self.definition))

        extra = [m for m in self.mobjects if id(m) not in keep]

        if extra:
            self.beat(*[FadeOut(m) for m in extra], duration = "fade")

        width0, c0 = self.camera.frame.width, self.camera.frame.get_center().copy()
        stretch0 = self.x_stretch.get_value()
        anchor_x = STORY["a"] if retain else None

        # 默认缓存会读取回调的全部闭包变量；无矩形时也必须先赋值
        anchor_screen0 = anchor_screen1 = 0.0

        if anchor_x is not None:
            anchor_world = self.point(anchor_x, 0)[0]
            anchor_screen0 = (anchor_world - c0[0]) / (width0 / FRAME_WIDTH)
            anchor_screen1 = self.axes.c2p(anchor_x, 0)[0]

        reveal = self.prepare_motion(
            width0, c0, stretch0, FRAME_WIDTH, 0, 1, math.ceil(self.unit_y / POINTS["radius"] / self.scale_factor()), anchor_x = anchor_x
        )

        def retreat(frame, alpha):
            t = smootherstep(alpha)
            w = width0 * math.exp(math.log(FRAME_WIDTH / width0) * t)
            frame.set(width = w)
            self.x_stretch.set_value(stretch0 * math.exp(math.log(1 / stretch0) * t))
            y = self.axes.c2p(0, 0)[1] - LAYOUT["baseline_screen_y"] * w / FRAME_WIDTH
            camera_x = (1 - t) * c0[0]

            if anchor_x is not None:
                # 按屏幕位置平滑移动a，避免对数退镜头时把矩形甩出画面
                camera_x = self.point(anchor_x, 0)[0] - ((1 - t) * anchor_screen0 + t * anchor_screen1) * w / FRAME_WIDTH

            frame.move_to([camera_x, y, 0])
            reveal.set_value(smooth(min(1, alpha / POINTS["detail_reveal_portion"])))

        # 从不淡出/替换点云；相机和所有点的updater始终同时运行
        self.beat(UpdateFromAlphaFunc(self.camera.frame, retreat), duration = duration, rate_func = linear, moving_graph = True)
        reveal.set_value(1)
        self.x_stretch.set_value(1)
        self.camera.frame.set(width = FRAME_WIDTH).move_to(ORIGIN)

    def threshold(self, epsilon):
        line = Line(color = PALETTE["epsilon"]).set_z_index(10)

        def update(m):
            s, c = self.scale_factor(), self.camera.frame.get_center()
            value = epsilon.get_value() if isinstance(epsilon, ValueTracker) else float(epsilon)
            y = self.point(0, value)[1]
            m.put_start_and_end_on(
                [max(c[0] + LAYOUT["plot_left"] * s, self.point(0, value)[0]), y, 0],
                [min(c[0] + LAYOUT["plot_right"] * s, self.point(1, value)[0]), y, 0]
            )
            m.set_stroke(width = STYLE["epsilon_width"] * s)

        line.add_updater(update)
        update(line)

        return line

    def neighborhood(self, delta_tracker, label_height):
        area = Rectangle(stroke_width = 0, fill_color = PALETTE["safe"], fill_opacity = STYLE["safe_fill"])
        sides = VGroup(Line(color = PALETTE["safe"]), Line(color = PALETTE["safe"]))
        group = VGroup(area, sides).set_z_index(1)

        def update(m):
            d = delta_tracker.get_value()
            s, c = self.scale_factor(), self.camera.frame.get_center()
            p0 = self.point(STORY["a"] - d, 0)
            p1 = self.point(STORY["a"] + d, 0)

            # 输入邻域是竖直条带；上边缘紧接a±delta标签的下方
            top = LAYOUT["delta_label_y"] - label_height / 2 - STYLE["safe_label_gap"]
            p1[1] = c[1] + min(top, LAYOUT["plot_top"]) * s

            # 只改几何，不重建对象/不重设透明度，FadeIn和FadeOut才能连续工作
            m[0].stretch_to_fit_width(p1[0] - p0[0]).stretch_to_fit_height(p1[1] - p0[1])
            m[0].move_to((p0 + p1) / 2)

            for side, x in zip(m[1], (p0[0], p1[0])):
                side.put_start_and_end_on([x, p0[1], 0], [x, p1[1], 0])
                side.set_stroke(width = STYLE["guide_width"] * s)

        group.add_updater(update)
        update(group)

        return group

    def delta_labels(self, delta):
        group = VGroup()

        for sign, tex in ((-1, r"a-\delta"), (1, r"a+\delta")):
            m = _tex(tex, LAYOUT["delta_label_size"], PALETTE["safe"])
            width0 = m.width

            def update(label, sign = sign, width0 = width0):
                s = self.scale_factor()
                label.set(width = width0 * s)
                value = delta.get_value() if isinstance(delta, ValueTracker) else delta
                x = self.point(STORY["a"] + sign * value, 0)[0]
                y = self.camera.frame.get_center()[1] + LAYOUT["delta_label_y"] * s
                label.move_to([x, y, 0])

            m.add_updater(update)
            update(m)
            group.add(m)

        group.set_z_index(20)

        return group

    def proof_zoom(self, epsilon, delta, qmax, changes = ()):
        height = (LAYOUT["plot_top"] - LAYOUT["baseline_screen_y"]) * min(STORY["epsilon_height_fraction"], 1 / 3)
        zoom = height / (float(epsilon) * self.unit_y)
        stretch = 1.0

        if STORY["horizontal_expansion"]:
            stretch = max(1.0, STORY["safe_screen_width"] / (2 * delta * self.unit_x * zoom))

        self.zoom_view(zoom, STORY["a"], qmax, stretch, duration = "proof_zoom", changes = changes)

    def proof_headers(self, epsilon):
        left = self.hud("a=" + STORY["a_tex"] + r",\quad R(a)=0", LAYOUT["hud_left"], PALETTE["rose"], LAYOUT["small_size"], align_left = True)
        right = self.live_proof_formula(epsilon, "epsilon")

        return left, right

    def definition_sequence(self, with_intro = True):
        self.initialize(empty = True)
        self.intro(show_cloud = False)
        self.add(self.cloud)

        # 示例点保留原对象、颜色和半径，然后只补入未出现的分数
        for p, q in STORY["examples"]:
            x, y = p / q, 1 / q
            dot = Dot(self.point(x, 0), radius = POINTS["radius"], color = self.point_color(x))
            label = self.point_label(
                rf"R\!\left(\frac{{{p}}}{{{q}}}\right)=\frac1{{{q}}}", x, y, self.point_color(x))
            dot._riemann_point = True
            self.add(dot)
            self.beat(dot.animate.move_to(self.point(x, y)), FadeIn(label), duration = "mapping")
            self.pause("mapping_hold")
            self.beat(FadeOut(label), duration = "fade")
            follower = self.pin(x, y, self.point_color(x), POINTS["radius"])
            dot.add_updater(follower.updaters[0])
            dot.set_z_index(6)
            dot._riemann_point = True
            self.remove(dot)
            self.cloud.add(dot)
            self.known_points.add((p, q))

        # 按函数值1/q自上而下逐排补点；已有示例不隐藏、不重复创建
        additions = [pq for pq in _fractions(POINTS["overview_q"]) if pq not in self.known_points]
        rows = sorted({q for p, q in additions})

        if rows:
            intervals = np.geomspace(TIMING["point_row_first"], TIMING["point_row_last"], len(rows))
            starts = np.concatenate(([0.0], np.cumsum(intervals[:-1])))
            clock = ValueTracker(0)
            self.append_points(additions, row_births = dict(zip(rows, starts)), row_clock = clock)
            duration = float(np.sum(intervals))
            self.beat(clock.animate.set_value(duration), duration = duration, rate_func = linear, moving_graph = True)
            self.remove(clock)

        self.pause("long_hold")

    def dense_sequence(self, with_intro = True):
        if with_intro or not hasattr(self, "axes"):
            self.initialize()

        # 与第一镜完全相同的顶部定义式，随镜头保持位置和字号
        self.remove(self.definition)
        self.definition = self.hud(self.definition.tex_string, LAYOUT["definition_position"], size = LAYOUT["definition_size"])
        self.add(self.axis_art, self.cloud, self.definition)
        self.pause("short_hold")

        for i, (x, zoom, qmax) in enumerate(STORY["tour"]):
            self.zoom_view(zoom, x, qmax)
            self.pause("long_hold")

            if i < len(STORY["tour"]) - 1:
                self.restore(formula = True, duration = "tour_return")

        self.restore(formula = True)
        self.pause("short_hold")

    def safe_sequence(self, with_intro = True):
        self.start(with_intro)
        self.hide_overview_labels()
        eps = STORY["epsilon_values"][0]
        n, bad, nearest, delta = _safe_data(eps)
        epsilon = ValueTracker(float(eps))
        left, right = self.proof_headers(epsilon)
        a_position = ValueTracker(STORY["a"])
        marker = self.pin(a_position, 0)
        self.beat(self.write(left), FadeIn(marker))
        line = self.threshold(epsilon)
        self.beat(self.write(right), Create(line), duration = "threshold")
        self.pause()
        count_progress = ValueTracker(0)
        count = self.live_proof_formula(epsilon, "count", count_progress)
        self.beat(FadeIn(count), duration = "fade")
        total, row_label = 0, None
        highlighted = []

        for q in range(n, 0, -1):
            row = [(p, qq) for p, qq in bad if qq == q]
            dots = VGroup(*[self.pin(p / q, 1 / q, PALETTE["flash"], POINTS["marker_radius"]) for p, q in row])
            total += len(row)
            new_label = self.hud(
                rf"q={q},\quad R\!\left(\frac pq\right)=\frac1{{{q}}}",
                LAYOUT["row_position"], PALETTE["rose"],
                LAYOUT["small_size"], LAYOUT["row_max_width"], align_left = True
            )
            anims = [FadeIn(dots), count_progress.animate.set_value(total)]

            if row_label is not None:
                anims.append(ReplacementTransform(row_label, new_label))
            else:
                anims.append(FadeIn(new_label))

            self.beat(*anims, duration = "row")
            self.beat(AnimationGroup(*[
                Flash(
                    dot, color = PALETTE["flash"], flash_radius = STYLE["flash_radius"],
                    line_length = STYLE["flash_length"], num_lines = STYLE["flash_lines"],
                    line_stroke_width = STYLE["flash_width"], time_width = STYLE["flash_time_width"]
                )
                for dot in dots], lag_ratio = 0), duration = "row_hold"
            )
            self.pause("row_hold")
            row_label = new_label
            highlighted.append(dots)

        # 真实轮廓边界，不把尚未使用的数字空槽算进闪光框
        count_boundary = VMobject().set_points(count.get_all_points())
        outline = SurroundingRectangle(
            count_boundary, buff = STYLE["count_flash_buff"] * self.scale_factor(),
            color = PALETTE["flash"], stroke_width = STYLE["count_flash_width"] * self.scale_factor()
        ).set_z_index(31)
        self.beat(ShowPassingFlash(outline, time_width = STYLE["count_flash_time_width"]), duration = "count_flash", rate_func = linear)
        self.pause()
        count_progress.set_value(-1)  # 从逐排累加切换到完整违规点集的实时计数
        self.beat(FadeOut(row_label), *[FadeOut(m) for m in highlighted], duration = "fade")
        self.proof_zoom(eps, delta, STORY["proof_q"][0])
        d = ValueTracker(delta * STORY["initial_delta_multiplier"])
        bounds = self.delta_labels(d)
        label_height = max(label.height for label in bounds) / self.scale_factor()
        band = self.neighborhood(d, label_height)
        self.beat(FadeIn(band))
        self.beat(d.animate.set_value(delta), duration = "shrink")
        implication = self.hud(
            r"|x-a|<\delta\quad\Longrightarrow\quad 0\le R(x)<\varepsilon",
            LAYOUT["hud_second"], PALETTE["safe"], LAYOUT["small_size"]
        )
        self.beat(FadeIn(bounds), self.write(implication))
        self.pause("long_hold")
        near_dot = near_label = None

        for stage in (1, 2):
            eps = STORY["epsilon_values"][stage]
            n, bad, nearest, delta = _safe_data(eps)
            removals = [implication, bounds] + [m for m in (near_dot, near_label) if m is not None]
            self.beat(*[FadeOut(m) for m in removals], duration = "fade")

            # 沿用原版的同一段平滑对数插值；计数只读取epsilon，不再驱动镜头
            # 同步改变epsilon、delta、镜头和横向比例，黄线高度与矩形宽度保持稳定
            self.proof_zoom(eps, delta, STORY["proof_q"][stage], changes = ((epsilon, float(eps)), (d, delta)))
            near_dot = self.pin(nearest[0] / nearest[1], 1 / nearest[1])
            near_label = self.point_label(rf"\frac{{{nearest[0]}}}{{{nearest[1]}}}", nearest[0] / nearest[1], 1 / nearest[1], PALETTE["rose"])
            bounds = self.delta_labels(d)
            implication = self.hud(r"|x-a|<\delta\quad\Longrightarrow\quad 0\le R(x)<\varepsilon", LAYOUT["hud_second"], PALETTE["safe"], LAYOUT["small_size"])
            self.beat(FadeIn(bounds), FadeIn(near_dot), FadeIn(near_label), FadeIn(implication))
            self.pause("long_hold")

        self.beat(FadeOut(implication), FadeOut(bounds), FadeOut(near_dot), FadeOut(near_label), duration = "fade")
        limit = self.hud(r"\lim_{x\to a}R(x)=R(a)=0\qquad(a\notin\mathbb Q)", LAYOUT["hud_second"], PALETTE["safe"], LAYOUT["small_size"])
        self.beat(self.write(limit), duration = "conclusion")
        self.pause("long_hold")
        self.restore(retain = (band, marker, line))

        # 全景复原完成以后，才收起邻域与黄线
        self.beat(FadeOut(band), FadeOut(line), duration = "fade")
        question = self.hud(r"a\in\mathbb Q\quad ?", LAYOUT["question_position"], PALETTE["rose"], LAYOUT["question_size"] * LAYOUT["question_scale"])
        self.beat(a_position.animate.set_value(float(STORY["rational_question"])), self.write(question), duration = "conclusion")
        self.pause("long_hold")

class Definition(MovingCameraScene):
    def construct(self):
        _RiemannAnimator(self).definition_sequence()

class DenseZoom(MovingCameraScene):
    def construct(self):
        _RiemannAnimator(self).dense_sequence()

class SafeNeighborhood(MovingCameraScene):
    def construct(self):
        _RiemannAnimator(self).safe_sequence()

class RiemannFilm(MovingCameraScene):
    def construct(self):
        animator = _RiemannAnimator(self)
        animator.definition_sequence()
        animator.dense_sequence(with_intro = False)
        animator.safe_sequence(with_intro = False)
