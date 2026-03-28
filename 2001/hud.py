"""HUD overlay: timeline bar, scene title, and dialogue subtitles."""

from renderer import Color


def draw_hud(buffer, player):
    """Draw the full HUD overlay on the bottom 3 rows of the buffer."""
    result = player.timeline.get_scene_at(player.position)
    if result is None:
        # At the end, show final state
        draw_scene_title(buffer, "THE END")
        draw_timeline_bar(buffer, player)
        return

    scene, progress, idx = result

    # Scene title with fade at boundaries
    alpha = 1.0
    if progress < 0.1:
        alpha = progress / 0.1
    draw_scene_title(buffer, scene.title, alpha)

    # Timeline bar
    draw_timeline_bar(buffer, player)

    # Dialogue
    dialogue = get_active_dialogue(scene, progress)
    if dialogue:
        draw_dialogue(buffer, dialogue.text, dialogue.speaker)


def draw_scene_title(buffer, title, fade_alpha=1.0):
    """Draw the scene title centered on row height-3."""
    if fade_alpha <= 0:
        return
    row = buffer.height - 3
    fg = Color.BRIGHT_WHITE if fade_alpha > 0.5 else Color.GRAY
    buffer.draw_text_centered(row, title, fg, Color.BLACK)


def draw_timeline_bar(buffer, player):
    """Draw the progress bar on row height-2.

    Format: [=====>-----------] 2:15 / 3:20  [>>2x]
    """
    row = buffer.height - 2
    total = player.timeline.total_duration
    if total <= 0:
        return

    speed_str = format_speed(player.speed)
    time_str = f" {format_time(player.position)} / {format_time(total)}  [{speed_str}]"

    bar_width = buffer.width - len(time_str) - 4  # 2 for brackets, 2 padding
    if bar_width < 5:
        bar_width = 5

    frac = min(1.0, player.position / total)
    filled = int(frac * (bar_width - 1))

    bar = '=' * filled + '>' + '-' * (bar_width - filled - 1)
    full = f" [{bar}]{time_str}"

    buffer.draw_text(0, row, full, Color.CYAN, Color.BLACK)


def draw_dialogue(buffer, dialogue_text, speaker=""):
    """Draw subtitle text centered on row height-1."""
    row = buffer.height - 1
    if speaker:
        text = f"{speaker}: {dialogue_text}"
    else:
        text = dialogue_text
    buffer.draw_text_centered(row, text, Color.BRIGHT_WHITE, Color.BLACK)


def format_time(seconds):
    """Format seconds as M:SS."""
    seconds = max(0, int(seconds))
    m = seconds // 60
    s = seconds % 60
    return f"{m}:{s:02d}"


def format_speed(speed):
    """Format speed indicator, e.g. '>>2x', '<<4x', '>1x'."""
    abs_speed = abs(speed)
    speed_int = int(abs_speed)
    if speed < 0:
        return f"<<{speed_int}x"
    elif abs_speed > 1.0:
        return f">>{speed_int}x"
    else:
        return f">{speed_int}x"


def get_active_dialogue(scene, progress):
    """Find the active dialogue entry for the current progress."""
    for d in scene.dialogues:
        if d.start <= progress <= d.end:
            return d
    return None
