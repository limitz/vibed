"""RGB color theme and styling for the Gmail console client."""

import curses
from dataclasses import dataclass


@dataclass(frozen=True)
class RGB:
    """An RGB color value."""
    r: int
    g: int
    b: int

    def to_curses(self) -> tuple[int, int, int]:
        """Convert 0-255 RGB to curses 0-1000 scale."""
        return (
            int(self.r / 255 * 1000),
            int(self.g / 255 * 1000),
            int(self.b / 255 * 1000),
        )


# ── Gmail-inspired dark theme ──────────────────────────────────────

# Backgrounds
BG_PRIMARY = RGB(28, 28, 30)        # Main background
BG_SECONDARY = RGB(44, 44, 46)      # Sidebar / panels
BG_ELEVATED = RGB(58, 58, 60)       # Hover / selected row
BG_INPUT = RGB(38, 38, 40)          # Input fields
BG_STATUS = RGB(18, 18, 20)         # Bottom status bar (darker)

# Text
TEXT_PRIMARY = RGB(229, 229, 234)    # Primary text
TEXT_SECONDARY = RGB(174, 174, 178)  # Secondary / dimmed
TEXT_TERTIARY = RGB(124, 124, 128)   # Placeholder / subtle
TEXT_INVERSE = RGB(28, 28, 30)       # Text on bright backgrounds

# Accents (Gmail-inspired)
ACCENT_RED = RGB(90, 50, 140)        # Dark purple (header/accents)
ACCENT_BLUE = RGB(66, 133, 244)      # Links / actions
ACCENT_GREEN = RGB(52, 168, 83)      # Success / sent
ACCENT_YELLOW = RGB(251, 188, 4)     # Starred
ACCENT_ORANGE = RGB(255, 138, 80)    # Important
ACCENT_PURPLE = RGB(168, 100, 253)   # Labels

# Status
STATUS_UNREAD = RGB(255, 255, 255)   # Bold unread
STATUS_ERROR = RGB(255, 69, 58)      # Errors

# Borders
BORDER_SUBTLE = RGB(68, 68, 70)      # Subtle dividers
BORDER_ACCENT = RGB(100, 100, 104)   # Emphasized borders

# ── Emoji constants ────────────────────────────────────────────────

EMOJI = {
    "inbox": "📥",
    "sent": "📤",
    "drafts": "📝",
    "starred": "⭐",
    "important": "🔶",
    "spam": "⚠️",
    "trash": "🗑️",
    "all_mail": "📧",
    "unread": "🔵",
    "attachment": "📎",
    "reply": "↩️",
    "forward": "↪️",
    "compose": "✏️",
    "search": "🔍",
    "label": "🏷️",
    "settings": "⚙️",
    "refresh": "🔄",
    "check": "✅",
    "error": "❌",
    "arrow_right": "▸",
    "arrow_down": "▾",
    "dot": "●",
    "mail": "✉️",
    "person": "👤",
    "clock": "🕐",
    "pin": "📌",
}


# ── Color pair management ──────────────────────────────────────────

# Color pair IDs
PAIR_NORMAL = 1
PAIR_HEADER = 2
PAIR_SIDEBAR = 3
PAIR_SIDEBAR_SELECTED = 4
PAIR_STATUS_BAR = 5
PAIR_EMAIL_UNREAD = 6
PAIR_EMAIL_READ = 7
PAIR_EMAIL_SELECTED = 8
PAIR_EMAIL_SELECTED_UNREAD = 9
PAIR_ACCENT_RED = 10
PAIR_ACCENT_BLUE = 11
PAIR_ACCENT_GREEN = 12
PAIR_ACCENT_YELLOW = 13
PAIR_ACCENT_PURPLE = 14
PAIR_INPUT = 15
PAIR_BORDER = 16
PAIR_SNIPPET = 17
PAIR_DATE = 18
PAIR_LABEL_TAG = 19
PAIR_TITLE = 20
PAIR_COMPOSE_FIELD = 21
PAIR_HELP_KEY = 22
PAIR_HELP_DESC = 23
PAIR_TAB_ACTIVE = 24
PAIR_TAB_INACTIVE = 25
PAIR_SEARCH_BOX = 26
PAIR_MSG_SENDER = 27
PAIR_MSG_BODY = 28
PAIR_ATTACHMENT = 29
PAIR_STARRED = 30
PAIR_STATUS_MSG = 31
PAIR_STATUS_ERR = 32


# ── 256-color xterm palette lookup ─────────────────────────────────

# The 6x6x6 color cube occupies indices 16-231.
# Each channel uses levels: 0, 95, 135, 175, 215, 255 (indices 0-5).
_CUBE_LEVELS = [0, 95, 135, 175, 215, 255]

# Grayscale ramp occupies indices 232-255 (24 shades).
_GRAY_LEVELS = [8 + 10 * i for i in range(24)]


def _rgb_to_xterm256(rgb: RGB) -> int:
    """Map an RGB color to the closest xterm-256 color index."""
    r, g, b = rgb.r, rgb.g, rgb.b

    # Find closest in the 6x6x6 cube
    def _cube_idx(v):
        min_dist = 999
        best = 0
        for i, lv in enumerate(_CUBE_LEVELS):
            d = abs(v - lv)
            if d < min_dist:
                min_dist = d
                best = i
        return best

    ri, gi, bi = _cube_idx(r), _cube_idx(g), _cube_idx(b)
    cube_color = 16 + 36 * ri + 6 * gi + bi
    cube_r, cube_g, cube_b = _CUBE_LEVELS[ri], _CUBE_LEVELS[gi], _CUBE_LEVELS[bi]
    cube_dist = (r - cube_r) ** 2 + (g - cube_g) ** 2 + (b - cube_b) ** 2

    # Find closest in the grayscale ramp
    gray_avg = (r + g + b) // 3
    best_gray_idx = 0
    best_gray_dist = 999999
    for i, lv in enumerate(_GRAY_LEVELS):
        d = (r - lv) ** 2 + (g - lv) ** 2 + (b - lv) ** 2
        if d < best_gray_dist:
            best_gray_dist = d
            best_gray_idx = i

    gray_color = 232 + best_gray_idx

    # Also check the basic 16 colors for exact matches
    basic_colors = [
        (0, 0, 0, 0), (128, 0, 0, 1), (0, 128, 0, 2), (128, 128, 0, 3),
        (0, 0, 128, 4), (128, 0, 128, 5), (0, 128, 128, 6), (192, 192, 192, 7),
        (128, 128, 128, 8), (255, 0, 0, 9), (0, 255, 0, 10), (255, 255, 0, 11),
        (0, 0, 255, 12), (255, 0, 255, 13), (0, 255, 255, 14), (255, 255, 255, 15),
    ]
    best_basic_dist = 999999
    best_basic = 0
    for br, bg_, bb, idx in basic_colors:
        d = (r - br) ** 2 + (g - bg_) ** 2 + (b - bb) ** 2
        if d < best_basic_dist:
            best_basic_dist = d
            best_basic = idx

    # Return whichever is closest
    if best_basic_dist <= cube_dist and best_basic_dist <= best_gray_dist:
        return best_basic
    if cube_dist <= best_gray_dist:
        return cube_color
    return gray_color


_next_color_id = 50  # start custom color IDs above curses defaults
_can_redefine = False  # whether terminal supports init_color


def _alloc_color(rgb: RGB) -> int:
    """Allocate a curses color and return its ID.

    If the terminal supports redefining colors, we create a custom color
    with exact RGB values. Otherwise, we map to the nearest xterm-256 index.
    """
    global _next_color_id

    if _can_redefine:
        cid = _next_color_id
        _next_color_id += 1
        r, g, b = rgb.to_curses()
        try:
            curses.init_color(cid, r, g, b)
            return cid
        except curses.error:
            pass  # Fall through to xterm-256 mapping

    return _rgb_to_xterm256(rgb)


def init_colors() -> None:
    """Initialize all curses color pairs. Must be called after curses.start_color()."""
    global _can_redefine, _next_color_id

    curses.start_color()
    curses.use_default_colors()

    # Check if the terminal supports redefining colors
    _can_redefine = curses.can_change_color()
    _next_color_id = 50

    # Allocate custom colors (exact RGB if supported, else nearest 256)
    c_bg_primary = _alloc_color(BG_PRIMARY)
    c_bg_secondary = _alloc_color(BG_SECONDARY)
    c_bg_elevated = _alloc_color(BG_ELEVATED)
    c_bg_input = _alloc_color(BG_INPUT)
    c_text_primary = _alloc_color(TEXT_PRIMARY)
    c_text_secondary = _alloc_color(TEXT_SECONDARY)
    c_text_tertiary = _alloc_color(TEXT_TERTIARY)
    c_text_inverse = _alloc_color(TEXT_INVERSE)
    c_accent_red = _alloc_color(ACCENT_RED)
    c_accent_blue = _alloc_color(ACCENT_BLUE)
    c_accent_green = _alloc_color(ACCENT_GREEN)
    c_accent_yellow = _alloc_color(ACCENT_YELLOW)
    c_accent_purple = _alloc_color(ACCENT_PURPLE)
    c_accent_orange = _alloc_color(ACCENT_ORANGE)
    c_border = _alloc_color(BORDER_SUBTLE)
    c_status_unread = _alloc_color(STATUS_UNREAD)
    c_bg_status = _alloc_color(BG_STATUS)

    # Initialize pairs
    curses.init_pair(PAIR_NORMAL, c_text_primary, c_bg_primary)
    curses.init_pair(PAIR_HEADER, c_text_inverse, c_accent_red)
    curses.init_pair(PAIR_SIDEBAR, c_text_secondary, c_bg_secondary)
    curses.init_pair(PAIR_SIDEBAR_SELECTED, c_text_primary, c_bg_elevated)
    curses.init_pair(PAIR_STATUS_BAR, c_text_secondary, c_bg_status)
    curses.init_pair(PAIR_EMAIL_UNREAD, c_status_unread, c_bg_primary)
    curses.init_pair(PAIR_EMAIL_READ, c_text_secondary, c_bg_primary)
    curses.init_pair(PAIR_EMAIL_SELECTED, c_text_primary, c_bg_elevated)
    curses.init_pair(PAIR_EMAIL_SELECTED_UNREAD, c_status_unread, c_bg_elevated)
    curses.init_pair(PAIR_ACCENT_RED, c_accent_red, c_bg_primary)
    curses.init_pair(PAIR_ACCENT_BLUE, c_accent_blue, c_bg_primary)
    curses.init_pair(PAIR_ACCENT_GREEN, c_accent_green, c_bg_primary)
    curses.init_pair(PAIR_ACCENT_YELLOW, c_accent_yellow, c_bg_primary)
    curses.init_pair(PAIR_ACCENT_PURPLE, c_accent_purple, c_bg_primary)
    curses.init_pair(PAIR_INPUT, c_text_primary, c_bg_input)
    curses.init_pair(PAIR_BORDER, c_border, c_bg_primary)
    curses.init_pair(PAIR_SNIPPET, c_text_tertiary, c_bg_primary)
    curses.init_pair(PAIR_DATE, c_text_tertiary, c_bg_primary)
    curses.init_pair(PAIR_LABEL_TAG, c_text_inverse, c_accent_purple)
    curses.init_pair(PAIR_TITLE, c_accent_red, c_bg_primary)
    curses.init_pair(PAIR_COMPOSE_FIELD, c_text_primary, c_bg_input)
    curses.init_pair(PAIR_HELP_KEY, c_accent_blue, c_bg_status)
    curses.init_pair(PAIR_HELP_DESC, c_text_secondary, c_bg_status)
    curses.init_pair(PAIR_TAB_ACTIVE, c_text_inverse, c_accent_red)
    curses.init_pair(PAIR_TAB_INACTIVE, c_text_tertiary, c_bg_secondary)
    curses.init_pair(PAIR_SEARCH_BOX, c_text_primary, c_bg_input)
    curses.init_pair(PAIR_MSG_SENDER, c_accent_blue, c_bg_primary)
    curses.init_pair(PAIR_MSG_BODY, c_text_primary, c_bg_primary)
    curses.init_pair(PAIR_ATTACHMENT, c_accent_orange, c_bg_primary)
    curses.init_pair(PAIR_STARRED, c_accent_yellow, c_bg_primary)
    curses.init_pair(PAIR_STATUS_MSG, c_accent_green, c_bg_status)
    curses.init_pair(PAIR_STATUS_ERR, c_accent_red, c_bg_status)
