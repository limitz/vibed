"""Timeline management: Scene, Dialogue, and Timeline with seeking."""

from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class Dialogue:
    """A timed subtitle/dialogue entry within a scene."""
    start: float
    end: float
    text: str
    speaker: str = ""


@dataclass
class Scene:
    """A named segment of the film with a render function."""
    name: str
    title: str
    duration: float
    render_fn: Callable
    dialogues: list = field(default_factory=list)


class Timeline:
    """Ordered sequence of scenes with seeking support."""

    def __init__(self, scenes):
        self.scenes = scenes
        self.total_duration = sum(s.duration for s in scenes)
        # Precompute cumulative start times
        self._start_times = []
        t = 0.0
        for s in scenes:
            self._start_times.append(t)
            t += s.duration

    def get_scene_at(self, time_s):
        """Get the scene at a given time.

        Returns (scene, local_progress, scene_index) or None if past end.
        """
        if not self.scenes:
            return None
        time_s = max(0.0, time_s)
        if time_s >= self.total_duration:
            return None
        idx = self.get_scene_index(time_s)
        scene = self.scenes[idx]
        local_time = time_s - self._start_times[idx]
        progress = local_time / scene.duration if scene.duration > 0 else 0.0
        progress = max(0.0, min(1.0, progress))
        return (scene, progress, idx)

    def get_scene_index(self, time_s):
        """Get the index of the scene at a given time."""
        time_s = max(0.0, time_s)
        for i in range(len(self._start_times) - 1, -1, -1):
            if time_s >= self._start_times[i]:
                return i
        return 0

    def get_scene_start_time(self, index):
        """Get the start time in seconds of scene at given index."""
        if index < 0 or index >= len(self._start_times):
            return self.total_duration
        return self._start_times[index]

    def get_scene_count(self):
        """Return the number of scenes."""
        return len(self.scenes)
