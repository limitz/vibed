"""The drawing brain: converts artistic intentions to stylus event strokes."""

import math
import numpy as np
from stylus_format import StylusEvent, Stroke, Drawing
from skills import load_skills, get_tool_pressure, get_spacing


def draw_line(x1: float, y1: float, x2: float, y2: float,
              tool: str = "pen", color="black", pressure: float = 0.5,
              num_events: int = 20, pressure_curve: list = None) -> Stroke:
    """Draw a straight line from (x1,y1) to (x2,y2)."""
    events = []
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt(dx * dx + dy * dy)
    ndx = dx / dist if dist > 0 else 0
    ndy = dy / dist if dist > 0 else 0

    for i in range(num_events):
        t = i / max(1, num_events - 1)
        x = x1 + t * dx
        y = y1 + t * dy
        p = pressure_curve[min(i, len(pressure_curve) - 1)] if pressure_curve else pressure
        # Add tiny natural hand tremor
        jitter = 0.3
        jx = np.random.normal(0, jitter)
        jy = np.random.normal(0, jitter)
        events.append(StylusEvent(
            x=x + jx, y=y + jy, dx=ndx, dy=ndy,
            pressure=p, color=color, tool=tool,
        ))
    return Stroke(events=events)


def draw_curve(control_points: list, tool: str = "pen", color="black",
               pressure: float = 0.5, num_events: int = 40,
               pressure_curve: list = None) -> Stroke:
    """Draw a smooth curve through control points using cubic Bezier interpolation."""
    if len(control_points) < 2:
        return Stroke(events=[])

    # For 2 points, just a line
    if len(control_points) == 2:
        return draw_line(*control_points[0], *control_points[1],
                         tool=tool, color=color, pressure=pressure, num_events=num_events)

    # Generate curve points using Catmull-Rom spline
    curve_pts = _catmull_rom(control_points, num_events)

    events = []
    for i, (x, y) in enumerate(curve_pts):
        t = i / max(1, len(curve_pts) - 1)
        p = pressure_curve[min(i, len(pressure_curve) - 1)] if pressure_curve else pressure
        # Direction from neighbors
        if i < len(curve_pts) - 1:
            dx = curve_pts[i + 1][0] - x
            dy = curve_pts[i + 1][1] - y
        elif i > 0:
            dx = x - curve_pts[i - 1][0]
            dy = y - curve_pts[i - 1][1]
        else:
            dx, dy = 1, 0
        mag = math.sqrt(dx * dx + dy * dy)
        if mag > 0:
            dx /= mag
            dy /= mag
        jitter = 0.2
        events.append(StylusEvent(
            x=x + np.random.normal(0, jitter),
            y=y + np.random.normal(0, jitter),
            dx=dx, dy=dy, pressure=p, color=color, tool=tool,
        ))
    return Stroke(events=events)


def draw_circle(cx: float, cy: float, radius: float,
                tool: str = "pen", color="black", pressure: float = 0.5,
                num_events: int = 60) -> Stroke:
    """Draw a circle centered at (cx, cy)."""
    events = []
    for i in range(num_events + 1):  # +1 to close
        angle = 2 * math.pi * i / num_events
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        dx = -math.sin(angle)
        dy = math.cos(angle)
        jitter = 0.3
        events.append(StylusEvent(
            x=x + np.random.normal(0, jitter),
            y=y + np.random.normal(0, jitter),
            dx=dx, dy=dy, pressure=pressure, color=color, tool=tool,
        ))
    return Stroke(events=events)


def draw_ellipse(cx: float, cy: float, rx: float, ry: float,
                 tool: str = "pen", color="black", pressure: float = 0.5,
                 num_events: int = 60) -> Stroke:
    """Draw an ellipse."""
    events = []
    for i in range(num_events + 1):
        angle = 2 * math.pi * i / num_events
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        dx = -rx * math.sin(angle)
        dy = ry * math.cos(angle)
        mag = math.sqrt(dx * dx + dy * dy)
        if mag > 0:
            dx /= mag
            dy /= mag
        events.append(StylusEvent(
            x=x + np.random.normal(0, 0.3),
            y=y + np.random.normal(0, 0.3),
            dx=dx, dy=dy, pressure=pressure, color=color, tool=tool,
        ))
    return Stroke(events=events)


def draw_rectangle(x: float, y: float, w: float, h: float,
                   tool: str = "pen", color="black", pressure: float = 0.5,
                   num_events_per_side: int = 15) -> Stroke:
    """Draw a rectangle outline."""
    corners = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    events = []
    for i in range(len(corners) - 1):
        x1, y1 = corners[i]
        x2, y2 = corners[i + 1]
        line = draw_line(x1, y1, x2, y2, tool=tool, color=color,
                         pressure=pressure, num_events=num_events_per_side)
        events.extend(line.events)
    return Stroke(events=events)


def draw_arc(cx: float, cy: float, radius: float,
             start_angle: float, end_angle: float,
             tool: str = "pen", color="black", pressure: float = 0.5,
             num_events: int = 30) -> Stroke:
    """Draw an arc from start_angle to end_angle (radians)."""
    events = []
    for i in range(num_events):
        t = i / max(1, num_events - 1)
        angle = start_angle + t * (end_angle - start_angle)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        dx = -math.sin(angle)
        dy = math.cos(angle)
        events.append(StylusEvent(
            x=x + np.random.normal(0, 0.2),
            y=y + np.random.normal(0, 0.2),
            dx=dx, dy=dy, pressure=pressure, color=color, tool=tool,
        ))
    return Stroke(events=events)


def draw_hatching(x: float, y: float, w: float, h: float,
                  angle_deg: float = 0.0, spacing: float = 6.0,
                  tool: str = "pencil", color="black", pressure: float = 0.4,
                  num_events_per_line: int = 15) -> list:
    """Fill a rectangular region with parallel hatching lines."""
    strokes = []
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    # Direction along the lines
    line_dx = cos_a
    line_dy = sin_a

    # Perpendicular direction (spacing direction)
    perp_dx = -sin_a
    perp_dy = cos_a

    # Determine how many lines we need
    diag = math.sqrt(w * w + h * h)
    n_lines = int(diag / spacing) + 2

    cx, cy = x + w / 2, y + h / 2

    for i in range(n_lines):
        offset = (i - n_lines / 2) * spacing
        # Line center
        lcx = cx + offset * perp_dx
        lcy = cy + offset * perp_dy

        # Line endpoints (extend far enough to cover the region)
        half_len = diag / 2
        lx1 = lcx - half_len * line_dx
        ly1 = lcy - half_len * line_dy
        lx2 = lcx + half_len * line_dx
        ly2 = lcy + half_len * line_dy

        # Clip to rectangle bounds
        pts = _clip_line_to_rect(lx1, ly1, lx2, ly2, x, y, x + w, y + h)
        if pts is None:
            continue
        cx1, cy1, cx2, cy2 = pts
        strokes.append(draw_line(cx1, cy1, cx2, cy2,
                                 tool=tool, color=color, pressure=pressure,
                                 num_events=num_events_per_line))
    return strokes


def draw_crosshatching(x: float, y: float, w: float, h: float,
                       angles: list = None, spacing: float = 6.0,
                       tool: str = "pencil", color="black", pressure: float = 0.4) -> list:
    """Fill a region with crosshatching (multiple angle layers)."""
    if angles is None:
        angles = [45.0, -45.0]
    strokes = []
    for angle in angles:
        strokes.extend(draw_hatching(x, y, w, h, angle_deg=angle, spacing=spacing,
                                     tool=tool, color=color, pressure=pressure))
    return strokes


def draw_filled_circle(cx: float, cy: float, radius: float,
                       tool: str = "brush", color="black", pressure: float = 0.6,
                       fill_spacing: float = 2.0) -> list:
    """Fill a circle with dense horizontal strokes."""
    strokes = []
    y_start = cy - radius
    y_end = cy + radius
    y = y_start
    while y <= y_end:
        dy = y - cy
        if abs(dy) < radius:
            half_w = math.sqrt(radius * radius - dy * dy)
            strokes.append(draw_line(
                cx - half_w, y, cx + half_w, y,
                tool=tool, color=color, pressure=pressure, num_events=15,
            ))
        y += fill_spacing
    return strokes


def draw_filled_rectangle(x: float, y: float, w: float, h: float,
                          tool: str = "brush", color="black",
                          pressure: float = 0.6, fill_spacing: float = 2.0) -> list:
    """Fill a rectangle with dense horizontal strokes."""
    strokes = []
    cy = y
    while cy <= y + h:
        strokes.append(draw_line(x, cy, x + w, cy,
                                 tool=tool, color=color, pressure=pressure, num_events=15))
        cy += fill_spacing
    return strokes


def draw_gradient_fill(x: float, y: float, w: float, h: float,
                       start_pressure: float, end_pressure: float,
                       tool: str = "pencil", color="black",
                       spacing: float = 3.0) -> list:
    """Fill a region with a vertical pressure gradient."""
    strokes = []
    cy = y
    while cy <= y + h:
        t = (cy - y) / h if h > 0 else 0
        p = start_pressure + t * (end_pressure - start_pressure)
        strokes.append(draw_line(x, cy, x + w, cy,
                                 tool=tool, color=color, pressure=p, num_events=15))
        cy += spacing
    return strokes


def draw_triangle(x1: float, y1: float, x2: float, y2: float,
                  x3: float, y3: float, tool: str = "pen", color="black",
                  pressure: float = 0.5) -> Stroke:
    """Draw a triangle outline."""
    events = []
    for (ax, ay), (bx, by) in [((x1, y1), (x2, y2)), ((x2, y2), (x3, y3)), ((x3, y3), (x1, y1))]:
        line = draw_line(ax, ay, bx, by, tool=tool, color=color, pressure=pressure, num_events=15)
        events.extend(line.events)
    return Stroke(events=events)


def draw_s_curve(x1: float, y1: float, x2: float, y2: float,
                 amplitude: float = 50.0, tool: str = "pen", color="black",
                 pressure: float = 0.5, num_events: int = 50) -> Stroke:
    """Draw an S-curve from (x1,y1) to (x2,y2)."""
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    cp1 = (x1 + (mx - x1) * 0.5, y1 - amplitude)
    cp2 = (mx, my)
    cp3 = (x2 - (x2 - mx) * 0.5, y2 + amplitude)
    return draw_curve([(x1, y1), cp1, cp2, cp3, (x2, y2)],
                      tool=tool, color=color, pressure=pressure, num_events=num_events)


def draw_pressure_ramp(x1: float, y1: float, x2: float, y2: float,
                       tool: str = "pencil", color="black",
                       num_events: int = 40) -> Stroke:
    """Draw a line with pressure ramping up then down."""
    pressures = []
    for i in range(num_events):
        t = i / max(1, num_events - 1)
        # Smooth ramp up then down
        p = math.sin(t * math.pi) * 0.85 + 0.1
        pressures.append(p)
    return draw_line(x1, y1, x2, y2, tool=tool, color=color,
                     num_events=num_events, pressure_curve=pressures)


# ---- Lesson-specific drawing functions ----

def take_lesson(lesson_number: int, canvas_w: int, canvas_h: int, attempt: int = 1) -> Drawing:
    """Generate a drawing for a specific lesson number.

    Loads current skills from skills.md and applies accumulated knowledge
    to drawing parameters. Each attempt varies the random seed.
    """
    np.random.seed(lesson_number * 42 + attempt * 7)

    sk = load_skills()

    fn_map = {
        1: _lesson_01_lines,
        2: _lesson_02_curves,
        3: _lesson_03_pressure,
        4: _lesson_04_hatching,
        5: _lesson_05_crosshatching,
        6: _lesson_06_shapes,
        7: _lesson_07_sphere,
        8: _lesson_08_cube,
        9: _lesson_09_light_shadow,
        10: _lesson_10_still_life_outline,
        11: _lesson_11_still_life_shaded,
        12: _lesson_12_perspective,
        13: _lesson_13_tree,
        14: _lesson_14_landscape,
        15: _lesson_15_water,
        16: _lesson_16_face_proportions,
        17: _lesson_17_facial_features,
        18: _lesson_18_portrait,
        19: _lesson_19_abstract,
        20: _lesson_20_food_color,
    }

    fn = fn_map.get(lesson_number)
    if fn is None:
        raise ValueError(f"No lesson function for lesson {lesson_number}")

    strokes = fn(canvas_w, canvas_h, sk)
    return Drawing(width=canvas_w, height=canvas_h, strokes=strokes)


def _lesson_01_lines(w, h, sk):
    """Straight lines: 5 horizontal, 5 vertical, 5 diagonal."""
    strokes = []
    margin = 40
    p = sk["pen_pressure"]
    n = int(sk["events_per_line"])
    for i in range(5):
        y = margin + i * (h - 2 * margin) / 6
        strokes.append(draw_line(margin, y, w - margin, y, tool="pen", pressure=p, num_events=n))
    for i in range(5):
        x = margin + (i + 1) * (w - 2 * margin) / 7
        strokes.append(draw_line(x, margin, x, h * 0.45, tool="pen", pressure=p, num_events=n))
    for i in range(5):
        x_start = margin + i * (w - 2 * margin) / 6
        strokes.append(draw_line(x_start, h * 0.55, x_start + 80, h - margin, tool="pen", pressure=p, num_events=n))
    return strokes


def _lesson_02_curves(w, h, sk):
    """Circles, arcs, S-curves."""
    strokes = []
    p = sk["pen_pressure"]
    n = int(sk["events_per_circle"])
    strokes.append(draw_circle(w * 0.2, h * 0.3, 40, tool="pen", pressure=p, num_events=n))
    strokes.append(draw_circle(w * 0.5, h * 0.3, 60, tool="pen", pressure=p, num_events=n))
    strokes.append(draw_circle(w * 0.8, h * 0.3, 30, tool="pen", pressure=p, num_events=n))
    strokes.append(draw_arc(w * 0.2, h * 0.7, 50, 0, math.pi, tool="pen", pressure=p))
    strokes.append(draw_arc(w * 0.5, h * 0.7, 40, math.pi / 4, math.pi, tool="pen", pressure=p))
    strokes.append(draw_arc(w * 0.8, h * 0.7, 45, 0, 3 * math.pi / 4, tool="pen", pressure=p))
    strokes.append(draw_s_curve(w * 0.15, h * 0.5, w * 0.45, h * 0.5, amplitude=30, tool="pen", pressure=p))
    strokes.append(draw_s_curve(w * 0.55, h * 0.5, w * 0.85, h * 0.5, amplitude=25, tool="pen", pressure=p))
    return strokes


def _lesson_03_pressure(w, h, sk):
    """Pressure ramp lines."""
    strokes = []
    margin = 50
    n = int(sk["events_per_line"]) * 2  # Extra events for smooth pressure ramp
    for i in range(5):
        y = margin + i * (h - 2 * margin) / 4
        strokes.append(draw_pressure_ramp(margin, y, w - margin, y, tool="pencil", num_events=n))
    return strokes


def _lesson_04_hatching(w, h, sk):
    """Three regions with parallel hatching at different angles."""
    strokes = []
    region_w = (w - 100) / 3
    sp = sk["hatching_spacing"]
    p = sk["pencil_pressure"]
    strokes.extend(draw_hatching(30, 50, region_w - 10, h - 100,
                                 angle_deg=0, spacing=sp, tool="pencil", pressure=p))
    strokes.extend(draw_hatching(40 + region_w, 50, region_w - 10, h - 100,
                                 angle_deg=45, spacing=sp, tool="pencil", pressure=p))
    strokes.extend(draw_hatching(50 + 2 * region_w, 50, region_w - 10, h - 100,
                                 angle_deg=90, spacing=sp, tool="pencil", pressure=p))
    return strokes


def _lesson_05_crosshatching(w, h, sk):
    """5 value zones from light to dark."""
    strokes = []
    zone_w = (w - 60) / 5
    base_sp = sk["crosshatch_spacing"]
    base_p = sk["pencil_pressure"]
    for i in range(5):
        x = 30 + i * zone_w
        density = i + 1
        spacing = max(3, base_sp * (1.3 - density * 0.15))
        pressure = base_p * (0.4 + i * 0.15)
        if density <= 2:
            strokes.extend(draw_hatching(x, 50, zone_w - 5, h - 100,
                                         angle_deg=45, spacing=spacing, tool="pencil", pressure=pressure))
        else:
            angles = [45, -45]
            if density >= 4:
                angles.append(0)
            if density >= 5:
                angles.append(90)
            for angle in angles:
                strokes.extend(draw_hatching(x, 50, zone_w - 5, h - 100,
                                             angle_deg=angle, spacing=spacing, tool="pencil", pressure=pressure))
    return strokes


def _lesson_06_shapes(w, h, sk):
    """Outlined and filled geometric shapes."""
    strokes = []
    p = sk["pen_pressure"]
    fsp = sk["fill_spacing"]
    strokes.append(draw_rectangle(50, 30, 100, 100, tool="pen", pressure=p))
    strokes.append(draw_triangle(250, 130, 350, 130, 300, 30, tool="pen", pressure=p))
    strokes.append(draw_circle(500, 80, 50, tool="pen", pressure=p))
    strokes.extend(draw_filled_rectangle(50, h * 0.5, 100, 100,
                                         tool="pen", color="black", pressure=p + 0.1, fill_spacing=fsp))
    strokes.extend(draw_hatching(250, h * 0.5, 100, 100, angle_deg=0, spacing=fsp,
                                 tool="pen", pressure=p + 0.1))
    strokes.extend(draw_filled_circle(500, h * 0.5 + 50, 50, tool="pen", pressure=p + 0.1, fill_spacing=fsp))
    return strokes


def _lesson_07_sphere(w, h, sk):
    """Sphere with smooth shading."""
    strokes = []
    cx, cy = w / 2, h / 2
    radius = min(w, h) * 0.35
    p = sk["pencil_pressure"]
    n = int(sk["events_per_line"])

    strokes.append(draw_circle(cx, cy, radius, tool="pencil", pressure=p))
    for r_frac in np.linspace(0.1, 0.95, 20):
        r = radius * r_frac
        for angle_offset in np.linspace(-1.0, 1.0, 10):
            arc_extent = 0.5
            start = angle_offset - arc_extent
            end = angle_offset + arc_extent
            shade_p = 0.1 + (p + 0.1) * (1.0 + angle_offset) / 2 * r_frac
            strokes.append(draw_arc(cx, cy, r, start, end,
                                    tool="pencil", pressure=shade_p, num_events=n))
    return strokes


def _lesson_08_cube(w, h, sk):
    """Cube with three visible faces at different values."""
    strokes = []
    cx, cy = w / 2, h / 2
    s = min(w, h) * 0.25
    p = sk["pen_pressure"]
    pp = sk["pencil_pressure"]
    sp = sk["hatching_spacing"]

    offset = s * 0.5
    fl = (cx - s, cy)
    fr = (cx + s * 0.3, cy)
    ftr = (cx + s * 0.3, cy - s)
    ftl = (cx - s, cy - s)
    rr = (cx + s, cy - offset * 0.5)
    rtr = (cx + s, cy - s - offset * 0.5)
    ttl = (cx - s + offset, cy - s - offset)
    ttr = (cx + s, cy - s - offset * 0.5)

    for (x1, y1), (x2, y2) in [
        (fl, fr), (fr, ftr), (ftr, ftl), (ftl, fl),
        (fr, rr), (rr, rtr), (rtr, ftr),
        (ftl, ttl), (ttl, ttr), (ttr, ftr),
    ]:
        strokes.append(draw_line(x1, y1, x2, y2, tool="pen", pressure=p))
    strokes.extend(draw_hatching(fl[0], ftl[1], fr[0] - fl[0], fl[1] - ftl[1],
                                 angle_deg=45, spacing=sp, tool="pencil", pressure=pp))
    strokes.extend(draw_hatching(fr[0], ftr[1], rr[0] - fr[0], fr[1] - ftr[1],
                                 angle_deg=-30, spacing=sp * 0.7, tool="pencil", pressure=pp + 0.2))
    strokes.extend(draw_hatching(ftl[0], ttl[1], ttr[0] - ftl[0], ftl[1] - ttl[1],
                                 angle_deg=30, spacing=sp * 1.5, tool="pencil", pressure=pp * 0.5))
    return strokes


def _lesson_09_light_shadow(w, h, sk):
    """Sphere with cast shadow."""
    strokes = []
    cx, cy = w * 0.45, h * 0.4
    radius = min(w, h) * 0.2
    pp = sk["pencil_pressure"]
    sp = sk["hatching_spacing"]

    ground_y = cy + radius + 10
    strokes.append(draw_line(30, ground_y, w - 30, ground_y, tool="pen", pressure=sk["pen_pressure"] * 0.6))
    strokes.append(draw_circle(cx, cy, radius, tool="pencil", pressure=pp))
    for r_frac in np.linspace(0.2, 0.9, 12):
        r = radius * r_frac
        for angle in np.linspace(-0.5, 1.2, 8):
            shade_p = 0.1 + pp * (1.0 + angle) / 2
            strokes.append(draw_arc(cx, cy, r, angle - 0.3, angle + 0.3,
                                    tool="pencil", pressure=shade_p, num_events=12))
    shadow_cx = cx + radius * 0.6
    shadow_cy = ground_y + 5
    strokes.extend(draw_hatching(shadow_cx - radius * 1.2, shadow_cy,
                                 radius * 2.0, radius * 0.4,
                                 angle_deg=0, spacing=sp * 0.5, tool="pencil", pressure=pp + 0.05))
    return strokes


def _lesson_10_still_life_outline(w, h, sk):
    """Outlines of cup, apple, book on a table."""
    strokes = []
    p = sk["pen_pressure"]
    table_y = h * 0.7

    strokes.append(draw_line(20, table_y, w - 20, table_y, tool="pen", pressure=p))
    cup_x, cup_w, cup_h = w * 0.15, 80, 100
    cup_y = table_y - cup_h
    strokes.append(draw_line(cup_x, cup_y, cup_x, table_y, tool="pen", pressure=p))
    strokes.append(draw_line(cup_x + cup_w, cup_y, cup_x + cup_w, table_y, tool="pen", pressure=p))
    strokes.append(draw_line(cup_x, table_y, cup_x + cup_w, table_y, tool="pen", pressure=p))
    strokes.append(draw_arc(cup_x + cup_w / 2, cup_y, cup_w / 2, math.pi, 2 * math.pi, tool="pen", pressure=p))
    strokes.append(draw_arc(cup_x + cup_w + 5, cup_y + cup_h * 0.3, 15,
                            -math.pi / 2, math.pi / 2, tool="pen", pressure=p * 0.8))
    apple_cx, apple_cy = w * 0.5, table_y - 45
    strokes.append(draw_circle(apple_cx, apple_cy, 40, tool="pen", pressure=p))
    strokes.append(draw_line(apple_cx, apple_cy - 40, apple_cx + 5, apple_cy - 55,
                             tool="pen", pressure=p * 0.7, num_events=8))
    book_x, book_w, book_h = w * 0.7, 120, 30
    book_y = table_y - book_h
    strokes.append(draw_rectangle(book_x, book_y, book_w, book_h, tool="pen", pressure=p))
    strokes.append(draw_line(book_x, book_y + 3, book_x + book_w, book_y + 3,
                             tool="pen", pressure=p * 0.5, num_events=10))
    return strokes


def _lesson_11_still_life_shaded(w, h, sk):
    """Still life with shading and shadows."""
    strokes = _lesson_10_still_life_outline(w, h, sk)
    table_y = h * 0.7
    pp = sk["pencil_pressure"]
    sp = sk["hatching_spacing"]
    gsp = sk["gradient_spacing"]

    cup_x = w * 0.15
    strokes.extend(draw_gradient_fill(cup_x + 5, table_y - 95, 35, 85,
                                      start_pressure=pp * 0.3, end_pressure=pp, tool="pencil", spacing=gsp))
    strokes.extend(draw_gradient_fill(cup_x + 40, table_y - 95, 35, 85,
                                      start_pressure=pp, end_pressure=pp * 0.3, tool="pencil", spacing=gsp))
    apple_cx, apple_cy = w * 0.5, table_y - 45
    for r in np.linspace(10, 35, 10):
        for a in np.linspace(0.2, 1.5, 6):
            shade_p = pp * 0.2 + pp * 0.8 * (a / 1.5)
            strokes.append(draw_arc(apple_cx, apple_cy, r, a - 0.3, a + 0.3,
                                    tool="pencil", pressure=shade_p, num_events=10))
    book_x = w * 0.7
    strokes.extend(draw_hatching(book_x + 2, table_y - 27, 116, 25,
                                 angle_deg=0, spacing=sp, tool="pencil", pressure=pp * 0.6))
    for sx, sw in [(w * 0.15, 90), (w * 0.45, 100), (w * 0.7, 130)]:
        strokes.extend(draw_hatching(sx, table_y + 2, sw, 20,
                                     angle_deg=0, spacing=sp * 0.5, tool="pencil", pressure=pp * 0.8))
    return strokes


def _lesson_12_perspective(w, h, sk):
    """Road/hallway with vanishing point."""
    strokes = []
    p = sk["pen_pressure"]
    vx, vy = w / 2, h * 0.35

    strokes.append(draw_line(0, h, vx, vy, tool="pen", pressure=p))
    strokes.append(draw_line(w, h, vx, vy, tool="pen", pressure=p))
    for i in range(8):
        t1 = 0.1 + i * 0.1
        t2 = t1 + 0.05
        bx = w / 2
        x1 = bx + (vx - bx) * t1
        y1 = h + (vy - h) * t1
        x2 = bx + (vx - bx) * t2
        y2 = h + (vy - h) * t2
        strokes.append(draw_line(x1, y1, x2, y2, tool="pen", pressure=p * 0.7, num_events=8))
    strokes.append(draw_line(0, vy, w, vy, tool="pen", pressure=p * 0.5, num_events=25))
    for i in range(6):
        t = 0.15 + i * 0.12
        px = (vx - 0) * t
        py = h + (vy - h) * t
        post_h = 80 * (1.0 - t)
        strokes.append(draw_line(px - 20, py, px - 20, py - post_h, tool="pen", pressure=p))
        rpx = w + (vx - w) * t
        strokes.append(draw_line(rpx + 20, py, rpx + 20, py - post_h, tool="pen", pressure=p))
    # Fill road with gradient shading
    sp = sk["hatching_spacing"]
    strokes.extend(draw_hatching(w * 0.2, h * 0.5, w * 0.6, h * 0.4,
                                 angle_deg=0, spacing=sp, tool="pencil", pressure=sk["pencil_pressure"] * 0.4))
    return strokes


def _lesson_13_tree(w, h, sk):
    """Tree with trunk, branches, foliage."""
    strokes = []
    pp = sk["pencil_pressure"]
    trunk_x = w / 2
    trunk_bottom = h * 0.85
    trunk_top = h * 0.4
    trunk_w = 15

    for offset in np.linspace(-trunk_w / 2, trunk_w / 2, 8):
        strokes.append(draw_line(trunk_x + offset + np.random.normal(0, 1),
                                 trunk_bottom,
                                 trunk_x + offset * 0.6 + np.random.normal(0, 2),
                                 trunk_top, tool="pencil", color="brown", pressure=pp + 0.1))
    branch_points = [
        (trunk_x, trunk_top, trunk_x - 100, trunk_top - 50),
        (trunk_x, trunk_top, trunk_x + 120, trunk_top - 40),
        (trunk_x, trunk_top + 30, trunk_x - 80, trunk_top - 20),
        (trunk_x, trunk_top + 30, trunk_x + 90, trunk_top + 10),
        (trunk_x, trunk_top + 60, trunk_x - 60, trunk_top + 30),
        (trunk_x, trunk_top + 60, trunk_x + 70, trunk_top + 40),
    ]
    for bx1, by1, bx2, by2 in branch_points:
        strokes.append(draw_line(bx1, by1, bx2, by2, tool="pencil", color="brown", pressure=pp))
    foliage_centers = [
        (trunk_x - 100, trunk_top - 60, 40), (trunk_x + 120, trunk_top - 50, 45),
        (trunk_x - 80, trunk_top - 30, 35), (trunk_x + 90, trunk_top, 38),
        (trunk_x, trunk_top - 70, 50), (trunk_x - 30, trunk_top - 40, 35),
        (trunk_x + 40, trunk_top - 30, 40),
    ]
    for fcx, fcy, fr in foliage_centers:
        for _ in range(20):
            rx = np.random.normal(fcx, fr * 0.5)
            ry = np.random.normal(fcy, fr * 0.5)
            r = fr * 0.3
            strokes.append(draw_arc(rx, ry, r, np.random.uniform(0, math.pi),
                                    np.random.uniform(math.pi, 2 * math.pi),
                                    tool="pencil", color=(30, 100, 30), pressure=pp, num_events=10))
    strokes.append(draw_line(20, trunk_bottom + 5, w - 20, trunk_bottom + 5, tool="pencil", pressure=pp * 0.6))
    return strokes


def _lesson_14_landscape(w, h, sk):
    """Landscape with foreground, middle ground, sky."""
    strokes = []
    pp = sk["pencil_pressure"]
    sp = sk["hatching_spacing"]
    horizon_y = h * 0.45

    strokes.extend(draw_hatching(0, 0, w, horizon_y * 0.8, angle_deg=0, spacing=sp * 2,
                                 tool="pencil", pressure=pp * 0.25))
    for i in range(3):
        hill_cx = w * (0.2 + i * 0.3)
        hill_r = w * 0.2
        for y_off in range(0, 30, 3):
            half_w = math.sqrt(max(0, hill_r ** 2 - (y_off + 10) ** 2)) if y_off < hill_r else 0
            if half_w > 5:
                strokes.append(draw_line(hill_cx - half_w, horizon_y - y_off,
                                         hill_cx + half_w, horizon_y - y_off,
                                         tool="pencil", pressure=pp * 0.5, num_events=15))
    strokes.append(draw_line(0, horizon_y, w, horizon_y, tool="pen", pressure=sk["pen_pressure"] * 0.5))
    strokes.extend(draw_hatching(0, horizon_y + 5, w, h * 0.2, angle_deg=10, spacing=sp,
                                 tool="pencil", pressure=pp * 0.7))
    for i in range(30):
        gx = np.random.uniform(20, w - 20)
        gy = h * 0.85 + np.random.normal(0, 15)
        glen = np.random.uniform(15, 35)
        strokes.append(draw_line(gx, gy, gx + np.random.normal(0, 5), gy - glen,
                                 tool="pencil", color=(40, 80, 30), pressure=pp * 0.8, num_events=8))
    strokes.extend(draw_hatching(0, h * 0.8, w, h * 0.2, angle_deg=80, spacing=sp * 0.8,
                                 tool="pencil", pressure=pp * 0.9))
    return strokes


def _lesson_15_water(w, h, sk):
    """Lake scene with reflections."""
    strokes = []
    pp = sk["pencil_pressure"]
    sp = sk["hatching_spacing"]
    horizon_y = h * 0.45

    strokes.extend(draw_hatching(0, 0, w, horizon_y - 10, angle_deg=0, spacing=sp * 1.5,
                                 tool="pencil", pressure=pp * 0.25))
    for i in range(15):
        tx = 20 + i * (w - 40) / 15
        th = np.random.uniform(30, 60)
        strokes.append(draw_line(tx, horizon_y, tx, horizon_y - th,
                                 tool="pencil", pressure=pp, num_events=10))
        strokes.append(draw_triangle(tx - 8, horizon_y - th + 10,
                                     tx + 8, horizon_y - th + 10,
                                     tx, horizon_y - th - 5, tool="pencil", pressure=pp * 0.8))
    strokes.append(draw_line(0, horizon_y, w, horizon_y, tool="pen", pressure=sk["pen_pressure"] * 0.7))
    for y_off in range(5, int(h * 0.55), 3):
        y = horizon_y + y_off
        pressure = pp * 0.3 + pp * 0.4 * (y_off / (h * 0.55))
        strokes.append(draw_line(20, y, w - 20, y, tool="pencil", pressure=pressure, num_events=20))
    for i in range(15):
        tx = 20 + i * (w - 40) / 15
        th = np.random.uniform(20, 40)
        ry = horizon_y + 2
        strokes.append(draw_line(tx, ry, tx, ry + th, tool="pencil", pressure=pp * 0.7, num_events=8))
    return strokes


def _lesson_16_face_proportions(w, h, sk):
    """Face oval with proportion guidelines."""
    strokes = []
    p = sk["pen_pressure"]
    pp = sk["pencil_pressure"]
    cx, cy = w / 2, h * 0.45
    rx, ry = w * 0.25, h * 0.3

    strokes.append(draw_ellipse(cx, cy, rx, ry, tool="pen", pressure=p))
    eye_y = cy
    strokes.append(draw_line(cx - rx * 0.8, eye_y, cx + rx * 0.8, eye_y, tool="pencil", pressure=pp * 0.5))
    nose_y = cy + ry * 0.35
    strokes.append(draw_line(cx - rx * 0.5, nose_y, cx + rx * 0.5, nose_y, tool="pencil", pressure=pp * 0.5))
    mouth_y = cy + ry * 0.55
    strokes.append(draw_line(cx - rx * 0.6, mouth_y, cx + rx * 0.6, mouth_y, tool="pencil", pressure=pp * 0.5))
    strokes.append(draw_line(cx, cy - ry * 0.9, cx, cy + ry * 0.9, tool="pencil", pressure=pp * 0.4))
    return strokes


def _lesson_17_facial_features(w, h, sk):
    """Face with eyes, nose, mouth."""
    strokes = _lesson_16_face_proportions(w, h, sk)
    p = sk["pen_pressure"]
    pp = sk["pencil_pressure"]
    sp = sk["hatching_spacing"]
    cx, cy = w / 2, h * 0.45
    rx, ry = w * 0.25, h * 0.3
    eye_y = cy
    eye_sep = rx * 0.35

    for side in [-1, 1]:
        ex = cx + side * eye_sep
        strokes.append(draw_arc(ex, eye_y, 15, math.pi, 2 * math.pi, tool="pen", pressure=p, num_events=20))
        strokes.append(draw_arc(ex, eye_y, 12, 0, math.pi, tool="pen", pressure=p * 0.8, num_events=15))
        strokes.append(draw_circle(ex, eye_y + 2, 5, tool="pen", pressure=p + 0.1, num_events=20))
        strokes.extend(draw_filled_circle(ex, eye_y + 2, 4, tool="pencil", pressure=pp, fill_spacing=sk["fill_spacing"]))
    for side in [-1, 1]:
        bx = cx + side * eye_sep
        strokes.append(draw_arc(bx, eye_y - 20, 18, math.pi + 0.3, 2 * math.pi - 0.3, tool="pencil", pressure=pp))
    nose_y = cy + ry * 0.35
    strokes.append(draw_line(cx - 2, eye_y + 10, cx - 3, nose_y - 5, tool="pencil", pressure=pp * 0.6, num_events=10))
    strokes.append(draw_line(cx + 2, eye_y + 10, cx + 3, nose_y - 5, tool="pencil", pressure=pp * 0.6, num_events=10))
    strokes.append(draw_arc(cx, nose_y, 8, 0.3, math.pi - 0.3, tool="pencil", pressure=pp * 0.9))
    strokes.append(draw_arc(cx - 8, nose_y + 2, 4, 0, math.pi, tool="pencil", pressure=pp * 0.8))
    strokes.append(draw_arc(cx + 8, nose_y + 2, 4, 0, math.pi, tool="pencil", pressure=pp * 0.8))
    mouth_y = cy + ry * 0.55
    strokes.append(draw_curve([(cx - 20, mouth_y), (cx - 5, mouth_y - 5), (cx, mouth_y - 3),
                                (cx + 5, mouth_y - 5), (cx + 20, mouth_y)], tool="pen", pressure=p))
    strokes.append(draw_curve([(cx - 18, mouth_y + 1), (cx, mouth_y + 10),
                                (cx + 18, mouth_y + 1)], tool="pen", pressure=p * 0.8))
    strokes.extend(draw_hatching(cx + 3, nose_y - 10, 15, 15, angle_deg=60, spacing=sp * 0.5,
                                 tool="pencil", pressure=pp * 0.5))
    return strokes


def _lesson_18_portrait(w, h, sk):
    """Complete portrait with hair and shading."""
    strokes = _lesson_17_facial_features(w, h, sk)
    pp = sk["pencil_pressure"]
    sp = sk["hatching_spacing"]
    cx, cy = w / 2, h * 0.45
    rx, ry = w * 0.25, h * 0.3

    hair_top = cy - ry - 10
    for i in range(40):
        hx = cx + np.random.normal(0, rx * 0.6)
        strokes.append(draw_curve(
            [(hx, hair_top + np.random.uniform(-10, 10)),
             (hx + np.random.normal(0, 15), cy - ry * 0.5),
             (hx + np.random.normal(0, 20), cy - ry * 0.1 + np.random.uniform(0, 20))],
            tool="pencil", pressure=np.random.uniform(pp * 0.5, pp + 0.1), num_events=15))
    for side in [-1, 1]:
        shade_x = cx + side * rx * 0.6
        strokes.extend(draw_hatching(shade_x - 15, cy + 10, 30, 40, angle_deg=70 * side,
                                     spacing=sp * 0.7, tool="pencil", pressure=pp * 0.4))
    chin_y = cy + ry * 0.85
    strokes.extend(draw_hatching(cx - rx * 0.4, chin_y, rx * 0.8, 15, angle_deg=0,
                                 spacing=sp * 0.5, tool="pencil", pressure=pp * 0.6))
    strokes.append(draw_line(cx - 15, cy + ry * 0.9, cx - 18, h * 0.85, tool="pencil", pressure=pp * 0.8))
    strokes.append(draw_line(cx + 15, cy + ry * 0.9, cx + 18, h * 0.85, tool="pencil", pressure=pp * 0.8))
    return strokes


def _lesson_19_abstract(w, h, sk):
    """Abstract composition with rhythm, contrast, and movement."""
    strokes = []
    bp = sk["brush_pressure"]
    pp = sk["pencil_pressure"]
    cp = sk["charcoal_pressure"]
    sp = sk["hatching_spacing"]

    for i in range(5):
        x1 = np.random.uniform(w * 0.05, w * 0.4)
        y1 = np.random.uniform(h * 0.1, h * 0.9)
        x2 = x1 + np.random.uniform(w * 0.2, w * 0.5)
        y2 = y1 + np.random.normal(0, h * 0.2)
        strokes.append(draw_line(x1, y1, x2, y2, tool="brush", color="black",
                                 pressure=np.random.uniform(bp * 0.7, bp + 0.1)))
    strokes.extend(draw_hatching(w * 0.55, h * 0.05, w * 0.4, h * 0.35,
                                 angle_deg=30, spacing=sp * 0.7, tool="charcoal", pressure=cp))
    for i in range(20):
        ccx = np.random.uniform(w * 0.1, w * 0.4)
        ccy = np.random.uniform(h * 0.4, h * 0.7)
        r = np.random.uniform(5, 25)
        strokes.append(draw_circle(ccx, ccy, r, tool="pen", pressure=sk["pen_pressure"], num_events=25))
    strokes.extend(draw_crosshatching(w * 0.2, h * 0.65, w * 0.5, h * 0.3,
                                      angles=[20, -45, 70], spacing=sp * 0.8, tool="pencil", pressure=pp))
    for i in range(3):
        pts = [(np.random.uniform(w * 0.3, w * 0.7), np.random.uniform(h * 0.2, h * 0.8)) for _ in range(5)]
        strokes.append(draw_curve(pts, tool="brush", color="black",
                                  pressure=np.random.uniform(bp * 0.5, bp), num_events=30))
    return strokes


def _lesson_20_food_color(w, h, sk):
    """Colorful food still life (apple/fruit)."""
    strokes = []
    bp = sk["brush_pressure"]
    pp = sk["pencil_pressure"]
    sp = sk["hatching_spacing"]
    cx, cy = w / 2, h / 2
    fruit_r = min(w, h) * 0.25

    for y_off in np.linspace(-fruit_r * 0.9, fruit_r * 0.9, 40):
        half_w = math.sqrt(max(0, fruit_r ** 2 - y_off ** 2))
        if half_w > 2:
            p = bp * (0.5 + 0.5 * (1 - abs(y_off) / fruit_r))
            strokes.append(draw_line(cx - half_w * 0.95, cy + y_off,
                                     cx + half_w * 0.95, cy + y_off,
                                     tool="brush", color=(200, 30, 30), pressure=p, num_events=12))
    for y_off in np.linspace(-fruit_r * 0.6, -fruit_r * 0.1, 10):
        half_w = math.sqrt(max(0, (fruit_r * 0.4) ** 2 - (y_off + fruit_r * 0.35) ** 2))
        if half_w > 2:
            strokes.append(draw_line(cx - fruit_r * 0.3 - half_w, cy + y_off,
                                     cx - fruit_r * 0.3 + half_w, cy + y_off,
                                     tool="brush", color=(240, 120, 80), pressure=bp * 0.5, num_events=8))
    strokes.extend(draw_hatching(cx + fruit_r * 0.2, cy - fruit_r * 0.5,
                                 fruit_r * 0.6, fruit_r, angle_deg=70, spacing=sp * 0.5,
                                 tool="pencil", color=(120, 15, 15), pressure=pp * 0.7))
    strokes.append(draw_line(cx, cy - fruit_r, cx + 5, cy - fruit_r - 25,
                             tool="pen", color="brown", pressure=sk["pen_pressure"], num_events=8))
    leaf_cx, leaf_cy = cx + 15, cy - fruit_r - 15
    strokes.append(draw_curve([(cx + 5, cy - fruit_r - 20), (leaf_cx + 15, leaf_cy - 10),
                                (leaf_cx + 25, leaf_cy + 5), (leaf_cx + 10, leaf_cy + 5)],
                              tool="brush", color=(40, 140, 30), pressure=bp, num_events=20))
    for i in range(5):
        strokes.append(draw_line(leaf_cx + 5 + i * 3, leaf_cy - 5, leaf_cx + 10 + i * 3, leaf_cy + 3,
                                 tool="brush", color=(50, 130, 40), pressure=bp * 0.5, num_events=6))
    strokes.extend(draw_hatching(cx - fruit_r * 0.5, cy + fruit_r + 5,
                                 fruit_r * 1.5, fruit_r * 0.25, angle_deg=0, spacing=sp * 0.5,
                                 tool="pencil", color=(80, 80, 80), pressure=pp * 0.6))
    strokes.append(draw_line(20, cy + fruit_r + 5, w - 20, cy + fruit_r + 5,
                             tool="pen", pressure=sk["pen_pressure"] * 0.5))
    return strokes


# ---- Utility functions ----

def _catmull_rom(points, num_points):
    """Generate points along a Catmull-Rom spline through given control points."""
    if len(points) < 2:
        return points

    # Pad endpoints
    pts = [points[0]] + points + [points[-1]]
    result = []
    segments = len(pts) - 3

    for seg in range(segments):
        p0 = np.array(pts[seg], dtype=float)
        p1 = np.array(pts[seg + 1], dtype=float)
        p2 = np.array(pts[seg + 2], dtype=float)
        p3 = np.array(pts[seg + 3], dtype=float)

        n_seg = max(2, num_points // segments)
        for i in range(n_seg):
            t = i / n_seg
            t2 = t * t
            t3 = t2 * t
            pt = 0.5 * (
                (2 * p1) +
                (-p0 + p2) * t +
                (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
                (-p0 + 3 * p1 - 3 * p2 + p3) * t3
            )
            result.append((float(pt[0]), float(pt[1])))

    result.append(points[-1])
    return result


def _clip_line_to_rect(x1, y1, x2, y2, rx1, ry1, rx2, ry2):
    """Clip a line segment to a rectangle using Cohen-Sutherland algorithm."""
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

    def code(x, y):
        c = INSIDE
        if x < rx1: c |= LEFT
        elif x > rx2: c |= RIGHT
        if y < ry1: c |= BOTTOM
        elif y > ry2: c |= TOP
        return c

    c1, c2 = code(x1, y1), code(x2, y2)
    for _ in range(20):
        if not (c1 | c2):
            return (x1, y1, x2, y2)
        if c1 & c2:
            return None
        c = c1 or c2
        dx, dy = x2 - x1, y2 - y1
        if c & TOP:
            x = x1 + dx * (ry2 - y1) / dy if dy else x1
            y = ry2
        elif c & BOTTOM:
            x = x1 + dx * (ry1 - y1) / dy if dy else x1
            y = ry1
        elif c & RIGHT:
            y = y1 + dy * (rx2 - x1) / dx if dx else y1
            x = rx2
        else:
            y = y1 + dy * (rx1 - x1) / dx if dx else y1
            x = rx1
        if c == c1:
            x1, y1, c1 = x, y, code(x, y)
        else:
            x2, y2, c2 = x, y, code(x, y)
    return None
