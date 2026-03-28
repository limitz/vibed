"""Core rendering engine: converts stylus event drawings to images."""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from stylus_format import Drawing, Stroke, StylusEvent, resolve_color
from tool_profiles import get_profile, ToolProfile
from texture import pencil_grain, paper_texture, brush_bristle_pattern, charcoal_noise


def render_drawing(drawing: Drawing, apply_paper: bool = True) -> Image.Image:
    """Render a complete Drawing to a PIL Image."""
    w, h = drawing.width, drawing.height
    bg = drawing.background

    # Create canvas
    canvas = Image.new("RGBA", (w, h), (*bg, 255))

    # Optional paper texture
    if apply_paper:
        ptex = paper_texture(w, h, seed=12345)
        paper_layer = np.array(canvas, dtype=np.float64)
        for c in range(3):
            paper_layer[:, :, c] *= ptex
        canvas = Image.fromarray(np.clip(paper_layer, 0, 255).astype(np.uint8), "RGBA")

    # Sort strokes by layer
    sorted_strokes = sorted(drawing.strokes, key=lambda s: s.layer)

    for stroke in sorted_strokes:
        if len(stroke.events) < 1:
            continue
        profile = get_profile(stroke.events[0].tool)
        canvas = render_stroke(canvas, stroke, profile)

    return canvas


def render_stroke(canvas: Image.Image, stroke: Stroke, profile: ToolProfile) -> Image.Image:
    """Render a single stroke onto the canvas."""
    events = stroke.events
    if len(events) == 0:
        return canvas

    if len(events) == 1:
        e = events[0]
        _stamp_at(canvas, e.x, e.y, profile, e.pressure, e.angle_x, e.angle_y,
                  resolve_color(e.color), e.tool)
        return canvas

    for i in range(len(events) - 1):
        e1, e2 = events[i], events[i + 1]
        dist = math.sqrt((e2.x - e1.x) ** 2 + (e2.y - e1.y) ** 2)
        stamp_w = profile.base_width * profile.pressure_width_fn((e1.pressure + e2.pressure) / 2)
        spacing = max(0.5, stamp_w * profile.overlap_spacing)
        steps = max(1, int(dist / spacing))
        interpolated = interpolate_events(e1, e2, steps)
        for ev in interpolated:
            _stamp_at(canvas, ev.x, ev.y, profile, ev.pressure, ev.angle_x, ev.angle_y,
                      resolve_color(ev.color), ev.tool)

    return canvas


def interpolate_events(e1: StylusEvent, e2: StylusEvent, steps: int) -> list:
    """Linearly interpolate between two stylus events."""
    if steps <= 1:
        return [e1]
    result = []
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0.0
        x = e1.x + t * (e2.x - e1.x)
        y = e1.y + t * (e2.y - e1.y)
        pressure = e1.pressure + t * (e2.pressure - e1.pressure)
        angle_x = e1.angle_x + t * (e2.angle_x - e1.angle_x)
        angle_y = e1.angle_y + t * (e2.angle_y - e1.angle_y)
        # Recompute direction from position delta
        dx = e2.x - e1.x
        dy = e2.y - e1.y
        mag = math.sqrt(dx * dx + dy * dy)
        if mag > 0:
            dx /= mag
            dy /= mag
        result.append(StylusEvent(
            x=x, y=y, dx=dx, dy=dy,
            pressure=pressure, angle_x=angle_x, angle_y=angle_y,
            color=e1.color, tool=e1.tool,
        ))
    return result


def _stamp_at(canvas: Image.Image, x: float, y: float, profile: ToolProfile,
              pressure: float, angle_x: float, angle_y: float,
              color: tuple, tool: str) -> None:
    """Place a single stamp/dab at the given position on the canvas."""
    width_mult = profile.pressure_width_fn(pressure)
    opacity = profile.pressure_opacity_fn(pressure)
    base_radius = profile.base_width * width_mult / 2.0

    if base_radius < 0.3:
        return

    # Compute ellipse dimensions from angle
    tilt_factor = profile.angle_sensitivity
    ax_scale = 1.0 + abs(angle_x) / 45.0 * tilt_factor
    ay_scale = 1.0 + abs(angle_y) / 45.0 * tilt_factor * 0.5
    rx = base_radius * ax_scale
    ry = base_radius * ay_scale

    # Stamp size (bounding box)
    size_x = int(math.ceil(rx * 2)) + 2
    size_y = int(math.ceil(ry * 2)) + 2
    if size_x < 1 or size_y < 1:
        return

    # Create stamp alpha mask
    stamp = _create_stamp_alpha(size_x, size_y, rx, ry, profile.edge_softness)

    # Apply tool-specific texture
    if profile.texture_type == "grain":
        grain = pencil_grain(size_x, size_y, intensity=0.6, seed=int(x * 7 + y * 13) % 10000)
        stamp = stamp * grain
    elif profile.texture_type == "charcoal":
        cnoise = charcoal_noise(size_x, size_y, intensity=0.5, seed=int(x * 11 + y * 17) % 10000)
        stamp = stamp * cnoise
    elif profile.texture_type == "bristle":
        bristle = brush_bristle_pattern(size_x, seed=int(y * 3) % 10000)
        # Expand to 2D by repeating along y axis
        bristle_2d = np.tile(bristle, (size_y, 1))
        stamp = stamp * bristle_2d

    # Apply opacity
    stamp = stamp * opacity

    # Convert to RGBA stamp image
    alpha_arr = np.clip(stamp * 255, 0, 255).astype(np.uint8)
    stamp_img = Image.new("RGBA", (size_x, size_y), (0, 0, 0, 0))
    stamp_arr = np.array(stamp_img)

    if tool == "eraser":
        # Eraser composites the background color (white)
        stamp_arr[:, :, 0] = 255
        stamp_arr[:, :, 1] = 255
        stamp_arr[:, :, 2] = 255
    else:
        stamp_arr[:, :, 0] = color[0]
        stamp_arr[:, :, 1] = color[1]
        stamp_arr[:, :, 2] = color[2]
    stamp_arr[:, :, 3] = alpha_arr

    stamp_img = Image.fromarray(stamp_arr, "RGBA")

    # Paste onto canvas at the right position
    paste_x = int(round(x - size_x / 2))
    paste_y = int(round(y - size_y / 2))

    canvas.alpha_composite(stamp_img, dest=(paste_x, paste_y))


def _create_stamp_alpha(w: int, h: int, rx: float, ry: float, softness: float) -> np.ndarray:
    """Create an elliptical alpha mask with given softness.

    Returns array of shape (h, w) with values in [0, 1].
    softness=0 gives hard edge, softness=1 gives Gaussian-like falloff.
    """
    cy, cx = h / 2.0, w / 2.0
    y_coords, x_coords = np.ogrid[0:h, 0:w]
    # Normalized distance from center (1.0 at ellipse edge)
    dist = np.sqrt(((x_coords - cx) / max(rx, 0.5)) ** 2 +
                   ((y_coords - cy) / max(ry, 0.5)) ** 2)

    if softness < 0.05:
        # Hard edge
        alpha = (dist <= 1.0).astype(np.float64)
    else:
        # Soft edge: smooth falloff
        # Map distance through sigmoid-like function
        falloff_width = softness * 0.8 + 0.1  # range [0.1, 0.9]
        alpha = np.clip(1.0 - (dist - (1.0 - falloff_width)) / falloff_width, 0, 1)
        # Apply smooth easing
        alpha = alpha * alpha * (3.0 - 2.0 * alpha)  # smoothstep

    return alpha
