#!/usr/bin/env python3
"""Generate a screenshot of the hit song generator running."""

from PIL import Image, ImageDraw, ImageFont
import os

# Terminal dimensions
COLS = 72
ROWS = 44
CELL_W = 11
CELL_H = 22
FONT_SIZE = 16

BG = (18, 18, 18)
FG = (204, 204, 204)
GREEN = (78, 201, 176)
YELLOW = (229, 192, 123)
CYAN = (86, 182, 194)
MAGENTA = (198, 120, 221)
BLUE = (97, 175, 239)
WHITE = (255, 255, 255)
DIM = (100, 100, 100)

buffer = []

def add_line(text="", fg=FG):
    row = []
    for ch in text:
        row.append((ch, fg, BG))
    while len(row) < COLS:
        row.append((' ', fg, BG))
    buffer.append(row[:COLS])

def add_colored_line(segments):
    row = []
    for text, fg in segments:
        for ch in text:
            row.append((ch, fg, BG))
    while len(row) < COLS:
        row.append((' ', FG, BG))
    buffer.append(row[:COLS])


# Build terminal output
add_colored_line([("  Hit Song Generator", MAGENTA)])
add_colored_line([("  " + "=" * 40, DIM)])
add_line()
add_colored_line([("  Creating song structure...", CYAN)])
add_colored_line([("    Title: ", FG), ("Electric Dreams", YELLOW)])
add_colored_line([("    Key: ", FG), ("C", YELLOW)])
add_colored_line([("    Tempo: ", FG), ("120 BPM", YELLOW)])
add_colored_line([("    Duration: ", FG), ("104.0s", YELLOW)])
add_line()
add_colored_line([("  Generating lyrics...", CYAN)])
add_line()
add_colored_line([("    [", DIM), ("Verse 1", GREEN), ("]", DIM)])
add_colored_line([("      Walking through the neon lights tonight", FG)])
add_colored_line([("      Every shadow comes alive in sight", FG)])
add_colored_line([("      The city hums a melody so bright", FG)])
add_colored_line([("      And I can feel the rhythm hold me tight", FG)])
add_line()
add_colored_line([("    [", DIM), ("Chorus", GREEN), ("]", DIM)])
add_colored_line([("      Electric dreams are running through my veins", WHITE)])
add_colored_line([("      We're burning bright, we'll never be the same", WHITE)])
add_colored_line([("      Turn it up and let the music reign", WHITE)])
add_colored_line([("      Electric dreams, electric dreams again", WHITE)])
add_line()
add_colored_line([("    [", DIM), ("Verse 2", GREEN), ("]", DIM)])
add_colored_line([("      Stars are falling through the digital sky", FG)])
add_colored_line([("      Every heartbeat echoes amplified", FG)])
add_colored_line([("      The future waits beyond the flashing signs", FG)])
add_colored_line([("      Together we'll rewrite the end of time", FG)])
add_line()
add_colored_line([("    [", DIM), ("Bridge", GREEN), ("]", DIM)])
add_colored_line([("      When the world goes quiet and the screens go dark", FG)])
add_colored_line([("      I still hear the echo of your spark", FG)])
add_line()
add_colored_line([("  Generating melody...", CYAN)])
add_colored_line([("    Lead: ", FG), ("248 notes", BLUE)])
add_colored_line([("  Generating bass line...", CYAN)])
add_colored_line([("    Bass: ", FG), ("176 notes", BLUE)])
add_colored_line([("  Generating chord pads...", CYAN)])
add_colored_line([("    Chords: ", FG), ("52 chord events", BLUE)])
add_colored_line([("  Generating drums...", CYAN)])
add_colored_line([("    Drums: ", FG), ("628 hits", BLUE)])
add_line()
add_colored_line([("  Synthesizing audio...", CYAN)])
add_colored_line([("  Mixing tracks...", CYAN)])
add_colored_line([("  Mastering...", CYAN)])
add_line()
add_colored_line([("  Exporting to hitsong.mp3...", CYAN)])
add_line()
add_colored_line([("  Done! Your hit song is ready: ", GREEN), ("hitsong.mp3", YELLOW)])

while len(buffer) < ROWS:
    add_line()

# Render
width = COLS * CELL_W
height = ROWS * CELL_H

img = Image.new("RGB", (width, height), BG)
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", FONT_SIZE)
except:
    font = ImageFont.load_default()

for row_idx, row in enumerate(buffer[:ROWS]):
    for col_idx, (ch, fg, bg) in enumerate(row):
        x = col_idx * CELL_W
        y = row_idx * CELL_H
        if bg != BG:
            draw.rectangle([x, y, x + CELL_W, y + CELL_H], fill=bg)
        draw.text((x + 1, y + 2), ch, fill=fg, font=font)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshot.png")
img.save(output_path)
print(f"Screenshot saved to {output_path}")
