#!/usr/bin/env python3
"""Generate a screenshot of the Gmail console client.

Builds the exact text buffer the curses renderer would produce and
renders it to an image using Pillow — monospace font, fixed-width cells,
foreground color on background rectangles, black terminal background.
"""

import os
import sys
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# ── Configuration ──────────────────────────────────────────────────

COLS = 120
ROWS = 38
CELL_W = 11
CELL_H = 22
FONT_SIZE = 16

# Try to find a monospace font
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttf",
]

# ── Color palette (matches colors.py) ─────────────────────────────

BG_PRIMARY = (28, 28, 30)
BG_SECONDARY = (44, 44, 46)
BG_ELEVATED = (58, 58, 60)
BG_INPUT = (38, 38, 40)

TEXT_PRIMARY = (229, 229, 234)
TEXT_SECONDARY = (174, 174, 178)
TEXT_TERTIARY = (124, 124, 128)
TEXT_INVERSE = (28, 28, 30)

ACCENT_RED = (90, 50, 140)           # Dark purple
ACCENT_BLUE = (66, 133, 244)
ACCENT_GREEN = (52, 168, 83)
ACCENT_YELLOW = (251, 188, 4)
ACCENT_ORANGE = (255, 138, 80)
ACCENT_PURPLE = (168, 100, 253)

BORDER = (68, 68, 70)


# ── Text buffer ───────────────────────────────────────────────────

class Cell:
    """A single character cell with colors."""
    __slots__ = ("char", "fg", "bg", "bold")

    def __init__(self, char=" ", fg=TEXT_PRIMARY, bg=BG_PRIMARY, bold=False):
        self.char = char
        self.fg = fg
        self.bg = bg
        self.bold = bold


def make_grid():
    return [[Cell() for _ in range(COLS)] for _ in range(ROWS)]


def put_str(grid, row, col, text, fg=TEXT_PRIMARY, bg=BG_PRIMARY, bold=False):
    """Write a string into the grid at (row, col)."""
    for i, ch in enumerate(text):
        c = col + i
        if c >= COLS or row >= ROWS or row < 0 or c < 0:
            break
        grid[row][c] = Cell(ch, fg, bg, bold)


def fill_row(grid, row, bg, start=0, end=None):
    """Fill a row with a background color."""
    if end is None:
        end = COLS
    for c in range(start, min(end, COLS)):
        if row < ROWS:
            grid[row][c].bg = bg


def fill_region(grid, row_start, row_end, col_start, col_end, bg):
    """Fill a rectangular region with a background color."""
    for r in range(row_start, min(row_end, ROWS)):
        for c in range(col_start, min(col_end, COLS)):
            grid[r][c].bg = bg


# ── Build the demo screen ─────────────────────────────────────────

SIDEBAR_W = 26


def _fmt_date_ago(minutes=0, hours=0, days=0):
    if minutes > 0:
        return f"{minutes}m ago"
    if hours > 0:
        return f"{hours}h ago"
    if days > 0:
        return f"{days}d ago"
    return "just now"


def build_inbox_screen(grid):
    """Build the full inbox view into the grid."""

    # ── Header bar (row 0) ──
    fill_row(grid, 0, ACCENT_RED)
    put_str(grid, 0, 1, "✉️", TEXT_INVERSE, ACCENT_RED, bold=True)
    put_str(grid, 0, 4, "Gmail", TEXT_INVERSE, ACCENT_RED, bold=True)
    put_str(grid, 0, 10, "Inbox", TEXT_INVERSE, ACCENT_RED, bold=True)
    email_str = "👤 alex.johnson@gmail.com "
    put_str(grid, 0, COLS - len(email_str) - 2, email_str, TEXT_INVERSE, ACCENT_RED)

    # ── Margin line (row 1) ──
    fill_row(grid, 1, BG_PRIMARY)

    # ── Sidebar (rows 2 to ROWS-2) ──
    # Each item: (emoji, name, fg, bg, bold, is_sep, count)
    # Render emoji and name separately with fixed spacing
    sidebar_raw = [
        ("✏️", "Compose", ACCENT_BLUE, BG_SECONDARY, True, False, ""),
        ("", "─" * 22, BORDER, BG_SECONDARY, False, True, ""),
        ("📥", "Inbox", TEXT_PRIMARY, BG_ELEVATED, True, False, "14"),  # selected
        ("⭐", "Starred", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
        ("🔶", "Important", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
        ("📤", "Sent", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
        ("📝", "Drafts", TEXT_SECONDARY, BG_SECONDARY, False, False, "3"),
        ("⚠️", "Spam", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
        ("🗑️", "Trash", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
        ("📧", "All Mail", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
        ("", "─" * 22, BORDER, BG_SECONDARY, False, True, ""),
        ("🏷️", "Work", TEXT_SECONDARY, BG_SECONDARY, False, False, "5"),
        ("🏷️", "Personal", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
        ("🏷️", "Projects/Alpha", TEXT_SECONDARY, BG_SECONDARY, False, False, "2"),
        ("🏷️", "Projects/Beta", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
        ("🏷️", "Receipts", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
        ("🏷️", "Travel", TEXT_SECONDARY, BG_SECONDARY, False, False, ""),
    ]

    for i, item in enumerate(sidebar_raw):
        row = 2 + i
        if row >= ROWS - 1:
            break

        emoji = item[0]
        name = item[1]
        fg = item[2]
        bg = item[3]
        bold = item[4]
        is_sep = item[5]
        count = item[6]

        fill_row(grid, row, bg, 0, SIDEBAR_W)

        if is_sep:
            put_str(grid, row, 2, name[:SIDEBAR_W - 4], BORDER, bg)
        else:
            # Selected item highlight
            if i == 2:  # Inbox is selected
                put_str(grid, row, 0, "▌", ACCENT_RED, bg, bold=True)

            # Emoji at col 2, then name at col 5 (fixed 3-col emoji slot)
            x = 2
            if emoji:
                put_str(grid, row, x, emoji, fg, bg, bold)
                x = 5  # fixed position after emoji (2 cols emoji + 1 space)
            put_str(grid, row, x, name, fg, bg, bold)

            # Unread count
            if count:
                cx = SIDEBAR_W - len(count) - 3
                put_str(grid, row, cx, count, ACCENT_RED, bg, bold=True)

        # Right border
        put_str(grid, row, SIDEBAR_W - 1, "│", BORDER, bg)

    # Fill remaining sidebar rows
    for row in range(2 + len(sidebar_raw), ROWS - 1):
        fill_row(grid, row, BG_SECONDARY, 0, SIDEBAR_W)
        put_str(grid, row, SIDEBAR_W - 1, "│", BORDER, BG_SECONDARY)

    # ── Email list (main area) ──
    emails = [
        {
            "sender": "Sarah Chen",
            "subject": "🚀 Q1 Product Launch — Final Review Needed",
            "snippet": "Hi team, I've attached the final deck for the Q1 launch. Please review slides 12-18 for the pricing…",
            "date": "12m ago",
            "unread": True,
            "starred": False,
            "attachment": True,
        },
        {
            "sender": "Mom",
            "subject": "Re: Dinner plans for Saturday?",
            "snippet": "That sounds wonderful! I'll make your favorite lasagna. Dad says he'll pick up dessert from that bakery…",
            "date": "45m ago",
            "unread": True,
            "starred": False,
            "attachment": False,
        },
        {
            "sender": "Amazon Web Services",
            "subject": "Your AWS bill for March 2026",
            "snippet": "Your total charges for this billing period are $847.23. View your detailed bill in the AWS Billing…",
            "date": "2h ago",
            "unread": True,
            "starred": False,
            "attachment": True,
        },
        {
            "sender": "Marcus Wright",
            "subject": "Sprint 24 Retrospective Notes",
            "snippet": "Here are the action items from today's retro: 1. Improve CI pipeline speed 2. Add more integration…",
            "date": "3h ago",
            "unread": False,
            "starred": True,
            "attachment": False,
        },
        {
            "sender": "Priya Patel",
            "subject": "Re: Code review: auth-service refactor",
            "snippet": "LGTM! Just one minor comment on the token refresh logic — see inline. The rest looks solid, nice work…",
            "date": "5h ago",
            "unread": True,
            "starred": False,
            "attachment": False,
        },
        {
            "sender": "Delta Air Lines",
            "subject": "Your flight to Tokyo is confirmed ✈️",
            "snippet": "Confirmation #DL7829K — SFO → NRT on April 15, 2026. Departure 11:45 AM. Check in opens 24 hours…",
            "date": "8h ago",
            "unread": False,
            "starred": True,
            "attachment": False,
        },
        {
            "sender": "GitHub",
            "subject": "New comment on your PR #483",
            "snippet": "@devops-bot commented on your pull request: 'All checks passed. Coverage is at 94.2%, up from…",
            "date": "10h ago",
            "unread": True,
            "starred": False,
            "attachment": False,
        },
        {
            "sender": "Jake Torres",
            "subject": "Weekend hiking trip — who's in? 🥾",
            "snippet": "Hey everyone! Thinking of doing Mt. Tam this Saturday, leaving around 7am. Trail is about 8 miles…",
            "date": "1d ago",
            "unread": False,
            "starred": False,
            "attachment": False,
        },
        {
            "sender": "Stripe",
            "subject": "Invoice #INV-2026-0342",
            "snippet": "Payment of $299.00 received for your monthly subscription. Thank you for your business…",
            "date": "1d ago",
            "unread": False,
            "starred": False,
            "attachment": True,
        },
        {
            "sender": "Rachel Kim",
            "subject": "Re: Team offsite agenda — April 2026",
            "snippet": "I've updated the shared doc with everyone's suggestions. Looks like the consensus is: Day 1 = strategy…",
            "date": "1d ago",
            "unread": False,
            "starred": False,
            "attachment": False,
        },
    ]

    content_w = COLS - SIDEBAR_W
    selected_email = 0  # First email is selected

    y = 2
    for ei, email in enumerate(emails):
        if y + 2 >= ROWS - 1:
            break

        is_selected = ei == selected_email
        is_unread = email["unread"]
        is_starred = email["starred"]
        has_attach = email["attachment"]

        # Determine colors
        if is_selected and is_unread:
            main_fg = (255, 255, 255)
            main_bg = BG_ELEVATED
            snip_fg = TEXT_PRIMARY
        elif is_selected:
            main_fg = TEXT_PRIMARY
            main_bg = BG_ELEVATED
            snip_fg = TEXT_SECONDARY
        elif is_unread:
            main_fg = (255, 255, 255)
            main_bg = BG_PRIMARY
            snip_fg = TEXT_TERTIARY
        else:
            main_fg = TEXT_SECONDARY
            main_bg = BG_PRIMARY
            snip_fg = TEXT_TERTIARY

        # Line 1: star, dot, sender, subject, date, attachment
        fill_row(grid, y, main_bg, SIDEBAR_W, COLS)

        x = SIDEBAR_W + 1

        # Selection indicator
        if is_selected:
            put_str(grid, y, SIDEBAR_W, "▌", ACCENT_BLUE, main_bg, bold=True)

        # Star
        if is_starred:
            put_str(grid, y, x, "⭐", ACCENT_YELLOW, main_bg)
        x += 3

        # Unread dot
        if is_unread:
            put_str(grid, y, x, "●", ACCENT_BLUE, main_bg)
        x += 2

        # Sender (max 20 chars)
        sender = email["sender"][:20]
        put_str(grid, y, x, sender, main_fg, main_bg, bold=is_unread)
        x += 22

        # Subject
        date_str = email["date"]
        attach_str = " 📎" if has_attach else ""
        right_part = f"{attach_str}  {date_str} "
        right_x = COLS - len(right_part) - 1

        max_subj = right_x - x - 1
        subject = email["subject"]
        if len(subject) > max_subj:
            subject = subject[:max_subj - 1] + "…"
        put_str(grid, y, x, subject, main_fg, main_bg, bold=is_unread)

        # Attachment icon
        if has_attach:
            put_str(grid, y, right_x, " 📎", ACCENT_ORANGE, main_bg)
            put_str(grid, y, right_x + 3, f"  {date_str} ", TEXT_TERTIARY, main_bg)
        else:
            put_str(grid, y, right_x + 3, f"  {date_str} ", TEXT_TERTIARY, main_bg)

        y += 1

        # Line 2: snippet
        fill_row(grid, y, main_bg if is_selected else BG_PRIMARY, SIDEBAR_W, COLS)
        snippet = email["snippet"]
        max_snippet = content_w - 10
        if len(snippet) > max_snippet:
            snippet = snippet[:max_snippet - 1] + "…"
        put_str(grid, y, SIDEBAR_W + 7, snippet, snip_fg,
                main_bg if is_selected else BG_PRIMARY)

        y += 1

        # Separator line
        if y < ROWS - 1:
            fill_row(grid, y, BG_PRIMARY, SIDEBAR_W, COLS)
            sep = "─" * (content_w - 2)
            put_str(grid, y, SIDEBAR_W + 1, sep, BORDER, BG_PRIMARY)
            y += 1

    # Fill remaining main area
    while y < ROWS - 1:
        fill_row(grid, y, BG_PRIMARY, SIDEBAR_W, COLS)
        y += 1

    # ── Single status bar (last row) ──
    BG_STATUS = (18, 18, 20)
    row = ROWS - 1
    fill_row(grid, row, BG_STATUS)

    # Status message on left
    x = 1
    put_str(grid, row, x, " Loaded 20 messages ", ACCENT_GREEN, BG_STATUS)
    x += 21
    put_str(grid, row, x, "│", TEXT_TERTIARY, BG_STATUS)
    x += 2

    # Key hints
    hints = [
        ("↑↓", "Navigate"),
        ("Enter", "Open"),
        ("/", "Search"),
        ("c", "Compose"),
        ("?", "Help"),
        ("q", "Quit"),
    ]
    for key, desc in hints:
        put_str(grid, row, x, f" {key} ", ACCENT_BLUE, BG_STATUS, bold=True)
        x += len(key) + 2
        put_str(grid, row, x, f" {desc}", TEXT_SECONDARY, BG_STATUS)
        x += len(desc) + 3


# ── Render to image ───────────────────────────────────────────────

def render_grid(grid, font) -> Image.Image:
    """Render the cell grid to a PIL Image."""
    img_w = COLS * CELL_W
    img_h = ROWS * CELL_H
    img = Image.new("RGB", (img_w, img_h), BG_PRIMARY)
    draw = ImageDraw.Draw(img)

    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]
            x0 = c * CELL_W
            y0 = r * CELL_H

            # Background rectangle
            draw.rectangle([x0, y0, x0 + CELL_W - 1, y0 + CELL_H - 1],
                           fill=cell.bg)

            # Character
            if cell.char and cell.char != " ":
                draw.text((x0 + 1, y0 + 2), cell.char, fill=cell.fg, font=font)

    return img


def find_font():
    """Find a monospace font."""
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, FONT_SIZE)
    # Fallback to default
    return ImageFont.load_default()


def main():
    grid = make_grid()
    build_inbox_screen(grid)
    font = find_font()
    img = render_grid(grid, font)

    out_path = os.path.join(os.path.dirname(__file__), "screenshot.png")
    img.save(out_path)
    print(f"Screenshot saved to {out_path}")


if __name__ == "__main__":
    main()
