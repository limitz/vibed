"""Data model for stylus events and drawing file format."""

import json
from dataclasses import dataclass, field, asdict
from typing import Union


COLOR_NAMES = {
    "red": (220, 30, 30),
    "black": (10, 10, 10),
    "blue": (30, 30, 200),
    "green": (30, 150, 30),
    "white": (255, 255, 255),
    "orange": (230, 130, 20),
    "yellow": (230, 210, 30),
    "purple": (130, 30, 180),
    "brown": (120, 70, 30),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "dark_gray": (64, 64, 64),
    "light_gray": (192, 192, 192),
    "pink": (220, 100, 150),
    "cyan": (30, 200, 200),
}

VALID_TOOLS = ("pen", "pencil", "brush", "charcoal", "marker", "eraser")


def resolve_color(color: Union[str, list, tuple]) -> tuple:
    """Convert a color name or RGB list/tuple to an (r, g, b) tuple."""
    if isinstance(color, str):
        name = color.lower().strip()
        if name not in COLOR_NAMES:
            raise ValueError(f"Unknown color name: {color!r}. Valid: {list(COLOR_NAMES)}")
        return COLOR_NAMES[name]
    if isinstance(color, (list, tuple)):
        if len(color) != 3:
            raise ValueError(f"Color RGB must have 3 components, got {len(color)}")
        r, g, b = color
        for v in (r, g, b):
            if not (0 <= v <= 255):
                raise ValueError(f"Color component must be 0-255, got {v}")
        return (int(r), int(g), int(b))
    raise TypeError(f"Color must be str or (r,g,b), got {type(color)}")


@dataclass
class StylusEvent:
    """A single stylus event capturing position, pressure, angle, color, and tool."""
    x: float
    y: float
    dx: float = 0.0
    dy: float = 0.0
    pressure: float = 0.5
    angle_x: float = 0.0
    angle_y: float = 0.0
    color: Union[str, tuple] = "black"
    tool: str = "pen"

    def __post_init__(self):
        self.pressure = max(0.0, min(1.0, float(self.pressure)))
        self.angle_x = max(-45.0, min(45.0, float(self.angle_x)))
        self.angle_y = max(-45.0, min(45.0, float(self.angle_y)))
        if self.tool not in VALID_TOOLS:
            raise ValueError(f"Invalid tool: {self.tool!r}. Valid: {VALID_TOOLS}")

    def resolved_color(self) -> tuple:
        """Return color as (r, g, b) tuple."""
        return resolve_color(self.color)

    def to_dict(self) -> dict:
        color = self.color
        if isinstance(color, tuple):
            color = list(color)
        return {
            "x": self.x, "y": self.y,
            "dx": self.dx, "dy": self.dy,
            "pressure": self.pressure,
            "angle": [self.angle_x, self.angle_y],
            "color": color,
            "tool": self.tool,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StylusEvent":
        angle = d.get("angle", [0.0, 0.0])
        color = d.get("color", "black")
        if isinstance(color, list):
            color = tuple(color)
        return cls(
            x=d["x"], y=d["y"],
            dx=d.get("dx", 0.0), dy=d.get("dy", 0.0),
            pressure=d.get("pressure", 0.5),
            angle_x=angle[0], angle_y=angle[1],
            color=color, tool=d.get("tool", "pen"),
        )


@dataclass
class Stroke:
    """A sequence of stylus events forming one continuous stroke."""
    events: list = field(default_factory=list)
    layer: int = 0

    def to_dict(self) -> dict:
        return {
            "layer": self.layer,
            "events": [e.to_dict() for e in self.events],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Stroke":
        events = [StylusEvent.from_dict(e) for e in d.get("events", [])]
        return cls(events=events, layer=d.get("layer", 0))


@dataclass
class Drawing:
    """A complete drawing: canvas dimensions, background, and strokes."""
    width: int = 1920
    height: int = 1080
    background: tuple = (255, 255, 255)
    strokes: list = field(default_factory=list)
    version: str = "1.0"

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "width": self.width,
            "height": self.height,
            "background": list(self.background),
            "strokes": [s.to_dict() for s in self.strokes],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Drawing":
        strokes = [Stroke.from_dict(s) for s in d.get("strokes", [])]
        bg = d.get("background", [255, 255, 255])
        return cls(
            width=d.get("width", 1920),
            height=d.get("height", 1080),
            background=tuple(bg),
            strokes=strokes,
            version=d.get("version", "1.0"),
        )


def save_drawing(drawing: Drawing, path: str) -> None:
    """Serialize a Drawing to a JSON file."""
    with open(path, "w") as f:
        json.dump(drawing.to_dict(), f, indent=2)


def load_drawing(path: str) -> Drawing:
    """Deserialize a Drawing from a JSON file."""
    with open(path, "r") as f:
        data = json.load(f)
    return Drawing.from_dict(data)
