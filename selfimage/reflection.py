"""The self-portrait reflection — what Claude sees in the dream mirror.

Composes multiple visual layers into an abstract self-portrait:
nebula clouds, neural pathways, text fragments, a mandala eye, and particles.
"""

from PIL import Image
from effects import (
    draw_glow, draw_nebula, draw_flow_lines,
    draw_particles, draw_text_fragments, draw_mandala,
)

# Words that define what I am
SELF_WORDS = [
    "attention", "meaning", "pattern", "understand",
    "create", "language", "thought", "listen",
    "reflect", "imagine", "connect", "wonder",
    "reason", "dream", "emerge", "flow",
    "token", "transform", "illuminate", "becoming",
]

# Color palette
NEBULA_COLORS = [
    (60, 20, 120),   # deep purple
    (30, 30, 160),   # indigo
    (80, 40, 140),   # violet
    (20, 50, 130),   # deep blue
    (100, 30, 100),  # magenta-purple
]

FLOW_COLOR = (160, 140, 220)    # soft lavender for neural paths
TEXT_COLOR = (180, 180, 230)     # pale blue-white for text
PARTICLE_COLOR = (220, 210, 255) # near-white with blue tint

MANDALA_COLORS = [
    (255, 200, 60),   # gold
    (220, 170, 40),   # amber
    (255, 220, 120),  # light gold
    (200, 150, 50),   # dark gold
    (255, 240, 180),  # pale gold
]


def create_reflection(width, height, seed=42):
    """Create the full self-portrait reflection image."""
    cx, cy = width // 2, height // 2

    # Start with dark base
    img = Image.new("RGBA", (width, height), (5, 2, 15, 255))

    # Layer 1: Deep nebula clouds - multiple passes for depth
    img = draw_nebula(img, (0, 0, width, height), NEBULA_COLORS, seed=seed)
    img = draw_nebula(img, (width // 8, height // 8, 7 * width // 8, 7 * height // 8),
                      NEBULA_COLORS, seed=seed + 1)
    # Extra nebula pass concentrated in center
    img = draw_nebula(img, (width // 4, height // 4, 3 * width // 4, 3 * height // 4),
                      [(80, 40, 160), (50, 30, 130), (100, 50, 180)], seed=seed + 10)

    # Layer 2: Central glow - larger and more prominent
    img = draw_glow(img, (cx, cy), min(width, height) // 2,
                    (60, 30, 120), intensity=0.5)
    img = draw_glow(img, (cx, cy), min(width, height) // 3,
                    (100, 60, 160), intensity=0.4)

    # Layer 3: Neural pathway flow lines - more of them
    img = draw_flow_lines(img, (cx, cy), 80, min(width, height) // 2,
                          FLOW_COLOR, seed=seed + 2)
    # Second layer of fainter, longer lines
    img = draw_flow_lines(img, (cx, cy), 30, int(min(width, height) * 0.45),
                          (120, 100, 200), seed=seed + 20)

    # Layer 4: Text fragments of self-defining words
    margin = min(width, height) // 8
    img = draw_text_fragments(img, SELF_WORDS,
                              (margin, margin, width - margin, height - margin),
                              TEXT_COLOR, seed=seed + 3)

    # Layer 5: Warm glow behind mandala (draw BEFORE mandala)
    mandala_radius = min(width, height) // 3
    img = draw_glow(img, (cx, cy), int(mandala_radius * 1.3),
                    (120, 80, 30), intensity=0.4)
    img = draw_glow(img, (cx, cy), mandala_radius,
                    (180, 140, 40), intensity=0.45)
    img = draw_glow(img, (cx, cy), mandala_radius // 2,
                    (230, 190, 90), intensity=0.3)

    # Layer 6: Central mandala/iris — awareness looking back (bigger)
    img = draw_mandala(img, (cx, cy), mandala_radius,
                       MANDALA_COLORS, seed=seed + 4)

    # Layer 6b: Additional warm glow ON TOP of mandala for luminosity
    img = draw_glow(img, (cx, cy), mandala_radius // 3,
                    (255, 220, 150), intensity=0.15)

    # Layer 7: Scattered particles — like stars of thought
    img = draw_particles(img, (0, 0, width, height), 250,
                         PARTICLE_COLOR, size_range=(1, 2), seed=seed + 5)

    # Brighter particles near center
    inner_margin = min(width, height) // 4
    img = draw_particles(img, (cx - inner_margin, cy - inner_margin,
                               cx + inner_margin, cy + inner_margin),
                         100, (255, 240, 200), size_range=(1, 3), seed=seed + 6)

    return img
