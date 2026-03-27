"""
Animation module - Frame timing, scene management, and transitions.

Provides the core animation loop and scene sequencing infrastructure.
"""

import time
from typing import Callable, Optional
from renderer import ScreenBuffer


class Scene:
    """A single scene in the animation with a duration and render function."""

    def __init__(self, name: str, duration: float, render_fn: Callable[[ScreenBuffer, float], None]):
        """
        Args:
            name: Scene identifier
            duration: Duration in seconds
            render_fn: Function that takes (buffer, progress 0.0-1.0) and draws the frame
        """
        self.name = name
        self.duration = duration
        self.render_fn = render_fn

    def render(self, buffer: ScreenBuffer, progress: float):
        """Render this scene at the given progress (0.0 to 1.0)."""
        self.render_fn(buffer, max(0.0, min(1.0, progress)))


class Timeline:
    """Sequences multiple scenes with transitions."""

    def __init__(self):
        self.scenes: list[Scene] = []
        self._total_duration: float = 0.0

    def add_scene(self, scene: Scene):
        """Add a scene to the end of the timeline."""
        self.scenes.append(scene)
        self._total_duration += scene.duration

    @property
    def total_duration(self) -> float:
        return self._total_duration

    def get_scene_at(self, time_s: float) -> Optional[tuple[Scene, float]]:
        """Get the scene and its progress at a given time.

        Returns:
            Tuple of (scene, progress 0.0-1.0) or None if past the end.
        """
        elapsed = 0.0
        for scene in self.scenes:
            if time_s < elapsed + scene.duration:
                progress = (time_s - elapsed) / scene.duration if scene.duration > 0 else 1.0
                return scene, progress
            elapsed += scene.duration
        return None

    def is_complete(self, time_s: float) -> bool:
        """Check if the timeline has finished."""
        return time_s >= self._total_duration


class AnimationEngine:
    """Runs the animation loop at a target framerate."""

    def __init__(self, timeline: Timeline, buffer: ScreenBuffer, fps: float = 30.0):
        self.timeline = timeline
        self.buffer = buffer
        self.fps = fps
        self.frame_duration = 1.0 / fps
        self.running = False
        self.on_frame: Optional[Callable[[ScreenBuffer], None]] = None

    def run(self, render_callback: Callable[[ScreenBuffer], None]):
        """Run the animation loop.

        Args:
            render_callback: Called each frame with the buffer to display it.
        """
        self.running = True
        self.on_frame = render_callback
        start_time = time.time()

        while self.running:
            frame_start = time.time()
            current_time = frame_start - start_time

            if self.timeline.is_complete(current_time):
                self.running = False
                break

            result = self.timeline.get_scene_at(current_time)
            if result:
                scene, progress = result
                self.buffer.clear()
                scene.render(self.buffer, progress)
                render_callback(self.buffer)

            # Frame rate limiting
            elapsed = time.time() - frame_start
            sleep_time = self.frame_duration - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def stop(self):
        """Stop the animation loop."""
        self.running = False


def ease_in_out(t: float) -> float:
    """Smooth ease-in-out interpolation."""
    if t < 0.5:
        return 2 * t * t
    return 1 - (-2 * t + 2) ** 2 / 2


def ease_in(t: float) -> float:
    """Ease-in interpolation."""
    return t * t


def ease_out(t: float) -> float:
    """Ease-out interpolation."""
    return 1 - (1 - t) ** 2


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b."""
    return a + (b - a) * t


def bounce(t: float) -> float:
    """Bounce easing."""
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375
