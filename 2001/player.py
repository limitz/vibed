"""Player state machine: manages playback position, speed, and state."""

from enum import Enum, auto


class PlayerState(Enum):
    PLAYING = auto()
    PAUSED = auto()


class Player:
    """Controls playback of a Timeline."""

    SPEED_OPTIONS = [1.0, 2.0, 4.0]

    def __init__(self, timeline):
        self.timeline = timeline
        self.position = 0.0
        self.speed = 1.0
        self.state = PlayerState.PAUSED

    def update(self, dt):
        """Advance position by dt * speed. Clamp to [0, total_duration]."""
        if self.state == PlayerState.PAUSED:
            return
        self.position += dt * self.speed
        self.position = max(0.0, min(self.timeline.total_duration, self.position))

    def play(self):
        """Start playback."""
        self.state = PlayerState.PLAYING

    def pause(self):
        """Pause playback."""
        self.state = PlayerState.PAUSED

    def toggle_pause(self):
        """Toggle between play and pause."""
        if self.state == PlayerState.PLAYING:
            self.state = PlayerState.PAUSED
        else:
            self.state = PlayerState.PLAYING

    def set_speed(self, speed):
        """Set playback speed (positive = forward, negative = rewind)."""
        self.speed = speed

    def cycle_forward_speed(self):
        """Cycle forward speed: 1x -> 2x -> 4x -> 1x.
        If currently rewinding, reset to 1x forward."""
        if self.speed < 0:
            self.speed = 1.0
            return
        try:
            idx = self.SPEED_OPTIONS.index(self.speed)
            self.speed = self.SPEED_OPTIONS[(idx + 1) % len(self.SPEED_OPTIONS)]
        except ValueError:
            self.speed = 1.0

    def cycle_rewind_speed(self):
        """Cycle rewind speed: -1x -> -2x -> -4x -> back to 1x forward."""
        if self.speed > 0:
            self.speed = -1.0
            return
        rewind_speeds = [-1.0, -2.0, -4.0]
        try:
            idx = rewind_speeds.index(self.speed)
            if idx + 1 >= len(rewind_speeds):
                self.speed = 1.0
            else:
                self.speed = rewind_speeds[idx + 1]
        except ValueError:
            self.speed = -1.0

    def skip_scene_forward(self):
        """Jump to the start of the next scene."""
        result = self.timeline.get_scene_at(self.position)
        if result is None:
            return
        _, _, idx = result
        next_start = self.timeline.get_scene_start_time(idx + 1)
        self.position = min(next_start, self.timeline.total_duration)

    def skip_scene_back(self):
        """Jump to the start of the current scene. If already near the start, go to previous."""
        result = self.timeline.get_scene_at(self.position)
        if result is None:
            # At the end, jump to last scene
            if self.timeline.get_scene_count() > 0:
                self.position = self.timeline.get_scene_start_time(
                    self.timeline.get_scene_count() - 1
                )
            return
        _, _, idx = result
        scene_start = self.timeline.get_scene_start_time(idx)
        # If we're more than 1 second into the scene, go to its start
        if self.position - scene_start > 1.0:
            self.position = scene_start
        else:
            # Go to previous scene start
            if idx > 0:
                self.position = self.timeline.get_scene_start_time(idx - 1)
            else:
                self.position = 0.0

    def restart(self):
        """Jump to the beginning."""
        self.position = 0.0

    def is_finished(self):
        """Return True if playback has reached the end."""
        return self.position >= self.timeline.total_duration

    def get_current_frame(self, buffer):
        """Render the current position to the buffer."""
        result = self.timeline.get_scene_at(self.position)
        if result is None:
            return
        scene, progress, _ = result
        scene.render_fn(buffer, progress)
