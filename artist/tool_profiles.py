"""Tool-specific rendering parameters for each drawing instrument."""

from dataclasses import dataclass
from typing import Callable
import math


@dataclass
class ToolProfile:
    """Rendering parameters for a drawing tool."""
    name: str
    base_width: float
    pressure_width_fn: Callable[[float], float]
    pressure_opacity_fn: Callable[[float], float]
    texture_type: str  # "none", "grain", "bristle", "charcoal"
    edge_softness: float  # 0.0 = hard edge, 1.0 = very soft
    angle_sensitivity: float  # how much tilt affects shape, 0.0-1.0
    overlap_spacing: float  # fraction of stamp width between stamps (lower = denser)


def _pen_width(p: float) -> float:
    return 1.0 + 0.3 * p


def _pen_opacity(p: float) -> float:
    return 0.85 + 0.15 * p


def _pencil_width(p: float) -> float:
    return 0.5 + p


def _pencil_opacity(p: float) -> float:
    return 0.15 + 0.7 * p


def _brush_width(p: float) -> float:
    return 0.2 + 1.6 * p


def _brush_opacity(p: float) -> float:
    return 0.3 + 0.5 * p


def _charcoal_width(p: float) -> float:
    return 0.6 + 0.8 * p


def _charcoal_opacity(p: float) -> float:
    return 0.2 + 0.6 * p


def _marker_width(p: float) -> float:
    return 0.9 + 0.2 * p


def _marker_opacity(p: float) -> float:
    return 0.4


def _eraser_width(p: float) -> float:
    return 0.5 + 1.0 * p


def _eraser_opacity(p: float) -> float:
    return 0.3 + 0.7 * p


_PROFILES = {
    "pen": ToolProfile(
        name="pen", base_width=4.0,
        pressure_width_fn=_pen_width, pressure_opacity_fn=_pen_opacity,
        texture_type="none", edge_softness=0.1,
        angle_sensitivity=0.1, overlap_spacing=0.25,
    ),
    "pencil": ToolProfile(
        name="pencil", base_width=3.5,
        pressure_width_fn=_pencil_width, pressure_opacity_fn=_pencil_opacity,
        texture_type="grain", edge_softness=0.3,
        angle_sensitivity=0.7, overlap_spacing=0.2,
    ),
    "brush": ToolProfile(
        name="brush", base_width=16.0,
        pressure_width_fn=_brush_width, pressure_opacity_fn=_brush_opacity,
        texture_type="bristle", edge_softness=0.8,
        angle_sensitivity=0.4, overlap_spacing=0.15,
    ),
    "charcoal": ToolProfile(
        name="charcoal", base_width=8.0,
        pressure_width_fn=_charcoal_width, pressure_opacity_fn=_charcoal_opacity,
        texture_type="charcoal", edge_softness=0.5,
        angle_sensitivity=0.5, overlap_spacing=0.2,
    ),
    "marker": ToolProfile(
        name="marker", base_width=8.0,
        pressure_width_fn=_marker_width, pressure_opacity_fn=_marker_opacity,
        texture_type="none", edge_softness=0.2,
        angle_sensitivity=0.1, overlap_spacing=0.2,
    ),
    "eraser": ToolProfile(
        name="eraser", base_width=10.0,
        pressure_width_fn=_eraser_width, pressure_opacity_fn=_eraser_opacity,
        texture_type="none", edge_softness=0.6,
        angle_sensitivity=0.1, overlap_spacing=0.2,
    ),
}


def get_profile(tool_name: str) -> ToolProfile:
    """Get the rendering profile for a tool by name."""
    if tool_name not in _PROFILES:
        raise ValueError(f"Unknown tool: {tool_name!r}. Valid: {list(_PROFILES)}")
    return _PROFILES[tool_name]


def list_tools() -> list:
    """Return list of available tool names."""
    return list(_PROFILES.keys())
