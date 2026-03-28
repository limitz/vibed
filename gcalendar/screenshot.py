#!/usr/bin/env python3
"""Generate screenshot.png that looks like the running calendar app."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Terminal dimensions and font
# ---------------------------------------------------------------------------
COLS = 120
ROWS = 40
CELL_W = 10
CELL_H = 20
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_SIZE = 14

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font_bold = ImageFont.truetype(FONT_BOLD_PATH, FONT_SIZE)

# ---------------------------------------------------------------------------
# Colors (RGB tuples) — matching the app's dark theme
# ---------------------------------------------------------------------------
BG_PRIMARY = (28, 28, 30)
BG_SECONDARY = (44, 44, 46)
BG_ELEVATED = (58, 58, 60)
BG_HEADER = (90, 50, 140)
BG_STATUS = (18, 18, 20)
BG_TODAY = (40, 48, 58)

TEXT_PRIMARY = (229, 229, 234)
TEXT_SECONDARY = (174, 174, 178)
TEXT_TERTIARY = (124, 124, 128)
TEXT_INVERSE = (28, 28, 30)

ACCENT_BLUE = (90, 50, 140)
ACCENT_GREEN = (52, 168, 83)
ACCENT_RED = (234, 67, 53)
ACCENT_YELLOW = (251, 188, 4)
ACCENT_PURPLE = (142, 36, 170)

CAL_BLUE = (3, 155, 229)
CAL_GREEN = (51, 182, 121)
CAL_RED = (213, 0, 0)
CAL_PURPLE = (142, 36, 170)

BORDER_COLOR = (68, 68, 70)

# ---------------------------------------------------------------------------
# Text buffer: 2D grid of (char, fg, bg, bold)
# ---------------------------------------------------------------------------
buffer = [[(' ', TEXT_PRIMARY, BG_PRIMARY, False) for _ in range(COLS)] for _ in range(ROWS)]


def put(row, col, text, fg=TEXT_PRIMARY, bg=BG_PRIMARY, bold=False):
    for i, ch in enumerate(text):
        c = col + i
        if 0 <= row < ROWS and 0 <= c < COLS:
            buffer[row][c] = (ch, fg, bg, bold)


def fill_row(row, bg, fg=TEXT_PRIMARY, start=0, end=COLS):
    for c in range(start, min(end, COLS)):
        if 0 <= row < ROWS:
            buffer[row][c] = (' ', fg, bg, False)


# ---------------------------------------------------------------------------
# Build the screen — matching the app's draw() output
# ---------------------------------------------------------------------------
SW = 26  # sidebar width

# === HEADER (row 0) ===
fill_row(0, BG_HEADER, TEXT_INVERSE)
put(0, 1, "\U0001f4c5", TEXT_INVERSE, BG_HEADER)
put(0, 4, "Calendar", TEXT_INVERSE, BG_HEADER, bold=True)
put(0, 13, "Agenda", TEXT_INVERSE, BG_HEADER)
put(0, 78, "Today \u00b7 Saturday, Mar 28", TEXT_INVERSE, BG_HEADER)

# === MARGIN (row 1) ===
fill_row(1, BG_PRIMARY)

# === SIDEBAR (rows 2 to ROWS-2) ===
for r in range(2, ROWS - 1):
    fill_row(r, BG_SECONDARY, TEXT_SECONDARY, 0, SW)
    # Right border
    buffer[r][SW - 1] = ('\u2502', BORDER_COLOR, BG_PRIMARY, False)

sidebar = [
    ("action", "\u270f\ufe0f", "New Event", False),
    ("sep", "", "", False),
    ("item", "\U0001f4c6", "Today", True),   # selected
    ("item", "\u25c0", "< Prev Day", False),
    ("item", "\u25b6", "Next Day >", False),
    ("item", "\U0001f50d", "Search", False),
    ("item", "\u23f0", "Free Time", False),
    ("sep", "", "", False),
    ("heading", "", "Calendars", False),
    ("item", "\U0001f535", "Alex Johnson", False),
    ("item", "\U0001f7e2", "Work", False),
    ("item", "\U0001f7e3", "Family", False),
    ("item", "\U0001f534", "Birthdays", False),
    ("item", "\U0001f7e0", "US Holidays", False),
    ("sep", "", "", False),
    ("item", "\u2753", "Help", False),
    ("item", "\u274c", "Quit", False),
]

row = 2
for kind, emoji, name, selected in sidebar:
    if row >= ROWS - 1:
        break
    if kind == "sep":
        put(row, 2, "\u2500" * (SW - 4), BORDER_COLOR, BG_SECONDARY)
        row += 1
        continue
    if kind == "heading":
        put(row, 2, name, TEXT_SECONDARY, BG_SECONDARY, bold=True)
        row += 1
        continue
    if kind == "action":
        bg = BG_HEADER if selected else BG_SECONDARY
        fg = TEXT_INVERSE if selected else ACCENT_BLUE
        fill_row(row, bg, fg, 0, SW - 1)
        if selected:
            put(row, 0, "\u258c", ACCENT_GREEN, bg, bold=True)
        put(row, 2, f" {emoji} {name}", fg, bg, bold=True)
        row += 1
        continue
    # Normal item
    bg = BG_ELEVATED if selected else BG_SECONDARY
    fg = TEXT_PRIMARY if selected else TEXT_SECONDARY
    fill_row(row, bg, fg, 0, SW - 1)
    if selected:
        put(row, 0, "\u258c", ACCENT_BLUE, bg, bold=True)
    put(row, 2, f"{emoji}", fg, bg)
    put(row, 5, name, fg, bg, bold=selected)
    row += 1

# === WEEK HEADER (row 2 in content area) ===
CX = SW  # content x start
CW = COLS - CX
week_days = [
    ("Mon", "23", False, False),
    ("Tue", "24", False, False),
    ("Wed", "25", False, False),
    ("Thu", "26", False, False),
    ("Fri", "27", False, False),
    ("Sat", "28", True, True),   # today + selected
    ("Sun", "29", False, False),
]
col_w = max(1, (CW - 2) // 7)
for i, (day, num, is_today, is_sel) in enumerate(week_days):
    cx = CX + 1 + i * col_w
    label = f"{day} {num}"
    if is_today and is_sel:
        bg = BG_HEADER
        fg = TEXT_INVERSE
    elif is_today:
        bg = BG_TODAY
        fg = TEXT_PRIMARY
    else:
        bg = BG_PRIMARY
        fg = TEXT_TERTIARY
    for c in range(cx, min(cx + col_w, COLS)):
        buffer[2][c] = (' ', fg, bg, False)
    offset = (col_w - len(label)) // 2
    put(2, cx + offset, label, fg, bg, bold=is_today)

# Separator (row 3)
put(3, CX + 1, "\u2500" * (CW - 2), ACCENT_BLUE, BG_PRIMARY)

# === EVENT LIST (single day: Saturday, Mar 28) ===
day_events = [
    (CAL_RED, "All day", "Mom's Birthday", "", "", False),
    (CAL_GREEN, "7:00 AM \u2013 8:00 AM", "Morning Run", "(1h)", "", False),
    (CAL_PURPLE, "11:00 AM \u2013 1:00 PM", "Brunch with Family", "(2h)", "\U0001f4cd Sarabeth's, 40 Central Park S", True),
]

# Date header
row = 4
fill_row(row, BG_TODAY, TEXT_PRIMARY, CX, COLS)
put(row, CX + 2, " Today \u00b7 Saturday, Mar 28", TEXT_PRIMARY, BG_TODAY, bold=True)
row += 1
put(row, CX + 2, "\u2500" * (CW - 4), BORDER_COLOR, BG_PRIMARY)
row += 1

for color, time_str, title, dur, detail, selected in day_events:
    if row >= ROWS - 3:
        break
    # Line 1: [▌] ● time  title  (duration)
    line_bg = BG_ELEVATED if selected else BG_PRIMARY
    line_fg = (255, 255, 255) if selected else TEXT_PRIMARY
    fill_row(row, line_bg, line_fg, CX, COLS)
    if selected:
        put(row, CX, "\u258c", ACCENT_BLUE, line_bg, bold=True)
    put(row, CX + 1, "\u25cf", color, line_bg)
    put(row, CX + 3, time_str, line_fg, line_bg, bold=selected)
    title_x = CX + 3 + 25
    put(row, title_x, title, line_fg, line_bg, bold=selected)
    if dur:
        put(row, title_x + len(title) + 1, dur,
            TEXT_TERTIARY if not selected else line_fg, line_bg)
    row += 1

    # Line 2: detail
    fill_row(row, line_bg, TEXT_TERTIARY, CX, COLS)
    if detail:
        put(row, CX + 6, detail, TEXT_TERTIARY if not selected else line_fg, line_bg)
    row += 1

    # Separator
    fill_row(row, BG_PRIMARY, TEXT_PRIMARY, CX, COLS)
    put(row, CX + 1, "\u2500" * (CW - 2), BORDER_COLOR, BG_PRIMARY)
    row += 1

# Fill remaining content rows
while row < ROWS - 1:
    fill_row(row, BG_PRIMARY, TEXT_PRIMARY, CX, COLS)
    row += 1

# === STATUS BAR (last row) ===
fill_row(ROWS - 1, BG_STATUS, TEXT_SECONDARY)
# Styled hints like gmail
hints = [
    ("\u2191\u2193", "Navigate"),
    ("\u2190\u2192", "Day"),
    ("Enter", "Open"),
    ("/", "Search"),
    ("n", "New"),
    ("?", "Help"),
    ("q", "Quit"),
]
x = 1
for key, desc in hints:
    if x >= COLS - 10:
        break
    put(ROWS - 1, x, f" {key} ", ACCENT_BLUE, BG_STATUS, bold=True)
    x += len(key) + 2
    put(ROWS - 1, x, f" {desc}", TEXT_SECONDARY, BG_STATUS)
    x += len(desc) + 3

# ---------------------------------------------------------------------------
# Render buffer to image
# ---------------------------------------------------------------------------
img_w = COLS * CELL_W
img_h = ROWS * CELL_H
img = Image.new("RGB", (img_w, img_h), BG_PRIMARY)
draw = ImageDraw.Draw(img)

for r in range(ROWS):
    for c in range(COLS):
        ch, fg, bg, bold = buffer[r][c]
        x = c * CELL_W
        y = r * CELL_H
        # Background
        draw.rectangle([x, y, x + CELL_W - 1, y + CELL_H - 1], fill=bg)
        # Character
        if ch and ch != ' ':
            f = font_bold if bold else font
            try:
                draw.text((x + 1, y + 2), ch, fill=fg, font=f)
            except Exception:
                pass

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshot.png")
img.save(out_path)
print(f"Saved: {out_path}")
