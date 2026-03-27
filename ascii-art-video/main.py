#!/usr/bin/env python3
"""
ASCII Art Video - Ultimate Stick Figure Showdown

An animated ASCII art video featuring:
- Epic title screen with fire and sparkle effects
- Two stick figures in an intense fighting sequence
- A hilarious banana peel incident
- Beautiful sunset fade out
- Star Wars style scrolling credits

Run: python main.py
"""

import sys
import signal
from renderer import ScreenBuffer, TerminalRenderer
from animation import Scene, Timeline, AnimationEngine
from scenes import (
    render_title, FightChoreography, FunnyMoment,
    render_fade_out, render_credits
)


def build_timeline() -> Timeline:
    """Build the complete animation timeline."""
    timeline = Timeline()

    # Scene 1: Title screen (7 seconds)
    timeline.add_scene(Scene("title", 7.0, render_title))

    # Scene 2: Fight sequence (20 seconds)
    fight = FightChoreography()
    timeline.add_scene(Scene("fight", 20.0, fight.render))

    # Scene 3: Funny moment - banana peel! (16 seconds)
    funny = FunnyMoment()
    timeline.add_scene(Scene("funny", 16.0, funny.render))

    # Scene 4: Fade out with sunset (8 seconds)
    timeline.add_scene(Scene("fade_out", 8.0, render_fade_out))

    # Scene 5: End credits (14 seconds)
    timeline.add_scene(Scene("credits", 14.0, render_credits))

    return timeline


def main():
    """Run the ASCII art video."""
    renderer = TerminalRenderer()
    width, height = renderer.get_terminal_size()

    # Ensure minimum size
    if width < 60 or height < 20:
        print("Terminal too small! Need at least 60x20.")
        print(f"Current size: {width}x{height}")
        sys.exit(1)

    buffer = ScreenBuffer(width, height)
    timeline = build_timeline()
    engine = AnimationEngine(timeline, buffer, fps=30)

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        engine.stop()

    signal.signal(signal.SIGINT, signal_handler)

    renderer.setup()
    try:
        engine.run(renderer.render)
    finally:
        renderer.cleanup()
        print("\n  Thanks for watching ASCII FIGHT - Ultimate Showdown!")
        print(f"  Total runtime: {timeline.total_duration:.0f} seconds")
        print()


if __name__ == "__main__":
    main()
