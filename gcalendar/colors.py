"""RGB color theme and styling for the Google Calendar console client."""

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


# ── Google Calendar-inspired dark theme ────────────────────────────

# Backgrounds
BG_PRIMARY = RGB(28, 28, 30)        # Main background
BG_SECONDARY = RGB(44, 44, 46)      # Sidebar / panels
BG_ELEVATED = RGB(58, 58, 60)       # Hover / selected row
BG_INPUT = RGB(38, 38, 40)          # Input fields
BG_STATUS = RGB(18, 18, 20)         # Bottom status bar (darker)
BG_TODAY = RGB(40, 48, 58)          # Today row highlight

# Text
TEXT_PRIMARY = RGB(229, 229, 234)    # Primary text
TEXT_SECONDARY = RGB(174, 174, 178)  # Secondary / dimmed
TEXT_TERTIARY = RGB(124, 124, 128)   # Placeholder / subtle
TEXT_INVERSE = RGB(28, 28, 30)       # Text on bright backgrounds

# Accents (Calendar-inspired)
ACCENT_BLUE = RGB(90, 50, 140)      # Dark purple (header/accents, matching gmail)
ACCENT_LINK = RGB(66, 133, 244)     # Links / actions
ACCENT_GREEN = RGB(52, 168, 83)     # Success / accepted
ACCENT_YELLOW = RGB(251, 188, 4)    # Tentative
ACCENT_RED = RGB(234, 67, 53)       # Declined / errors
ACCENT_ORANGE = RGB(244, 160, 0)    # Warnings
ACCENT_PURPLE = RGB(168, 100, 253)  # Labels / categories

# Calendar event colors
CAL_TOMATO = RGB(213, 0, 0)
CAL_SAGE = RGB(51, 182, 121)
CAL_PEACOCK = RGB(3, 155, 229)
CAL_BLUEBERRY = RGB(63, 81, 181)
CAL_LAVENDER = RGB(121, 134, 203)
CAL_GRAPE = RGB(142, 36, 170)
CAL_BANANA = RGB(246, 191, 38)
CAL_TANGERINE = RGB(244, 81, 30)
CAL_GRAPHITE = RGB(97, 97, 97)
CAL_BASIL = RGB(11, 128, 67)
CAL_FLAMINGO = RGB(230, 124, 115)

# Status
STATUS_UNREAD = RGB(255, 255, 255)
STATUS_ERROR = RGB(255, 69, 58)

# Borders
BORDER_SUBTLE = RGB(68, 68, 70)
BORDER_ACCENT = RGB(100, 100, 104)

# ── Emoji constants ────────────────────────────────────────────────

EMOJI = {
    "calendar": "📅",
    "clock": "🕐",
    "bell": "🔔",
    "search": "🔍",
    "plus": "✏️",
    "edit": "✏️",
    "delete": "🗑️",
    "back": "◀",
    "forward": "▶",
    "check": "✅",
    "cross": "❌",
    "question": "❓",
    "warning": "⚠️",
    "refresh": "🔄",
    "settings": "⚙️",
    "person": "👤",
    "people": "👥",
    "meeting": "👥",
    "video": "📹",
    "location": "📍",
    "link": "🔗",
    "mail": "✉️",
    "birthday": "🎂",
    "sport": "🏃",
    "food": "🍽️",
    "home": "🏠",
    "work": "💼",
    "today": "📆",
    "week": "🗓️",
    "dot_blue": "🔵",
    "dot_green": "🟢",
    "dot_red": "🔴",
    "dot_purple": "🟣",
    "dot_yellow": "🟡",
    "dot_orange": "🟠",
    "dot": "●",
    "arrow_right": "▸",
    "accepted": "✅",
    "declined": "❌",
    "tentative": "❔",
    "pending": "⏳",
    "free_time": "⏰",
}


# ── Color pair IDs ─────────────────────────────────────────────────

PAIR_NORMAL = 1
PAIR_HEADER = 2
PAIR_SIDEBAR = 3
PAIR_SIDEBAR_SELECTED = 4
PAIR_STATUS_BAR = 5
PAIR_EVENT_NORMAL = 6
PAIR_EVENT_DIM = 7
PAIR_EVENT_SELECTED = 8
PAIR_EVENT_SELECTED_BOLD = 9
PAIR_ACCENT_RED = 10
PAIR_ACCENT_BLUE = 11
PAIR_ACCENT_GREEN = 12
PAIR_ACCENT_YELLOW = 13
PAIR_ACCENT_PURPLE = 14
PAIR_INPUT = 15
PAIR_BORDER = 16
PAIR_SNIPPET = 17
PAIR_DATE = 18
PAIR_CAL_BLUE = 19
PAIR_TITLE = 20
PAIR_COMPOSE_FIELD = 21
PAIR_HELP_KEY = 22
PAIR_HELP_DESC = 23
PAIR_TAB_ACTIVE = 24
PAIR_TAB_INACTIVE = 25
PAIR_SEARCH_BOX = 26
PAIR_CAL_GREEN = 27
PAIR_CAL_RED = 28
PAIR_CAL_PURPLE = 29
PAIR_CAL_YELLOW = 30
PAIR_STATUS_MSG = 31
PAIR_STATUS_ERR = 32
PAIR_TODAY_HIGHLIGHT = 33
PAIR_CAL_ORANGE = 34
PAIR_CAL_GRAPHITE = 35
PAIR_LINK = 36
PAIR_NOW_LINE = 37


# ── 256-color xterm palette lookup ─────────────────────────────────

_CUBE_LEVELS = [0, 95, 135, 175, 215, 255]
_GRAY_LEVELS = [8 + 10 * i for i in range(24)]


def _rgb_to_xterm256(rgb: RGB) -> int:
    """Map an RGB color to the closest xterm-256 color index."""
    r, g, b = rgb.r, rgb.g, rgb.b

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

    best_gray_idx = 0
    best_gray_dist = 999999
    for i, lv in enumerate(_GRAY_LEVELS):
        d = (r - lv) ** 2 + (g - lv) ** 2 + (b - lv) ** 2
        if d < best_gray_dist:
            best_gray_dist = d
            best_gray_idx = i

    gray_color = 232 + best_gray_idx

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

    if best_basic_dist <= cube_dist and best_basic_dist <= best_gray_dist:
        return best_basic
    if cube_dist <= best_gray_dist:
        return cube_color
    return gray_color


_next_color_id = 50
_can_redefine = False


def _alloc_color(rgb: RGB) -> int:
    """Allocate a curses color and return its ID."""
    global _next_color_id

    if _can_redefine:
        cid = _next_color_id
        _next_color_id += 1
        r, g, b = rgb.to_curses()
        try:
            curses.init_color(cid, r, g, b)
            return cid
        except curses.error:
            pass

    return _rgb_to_xterm256(rgb)


def init_colors() -> None:
    """Initialize all curses color pairs. Must be called after curses.start_color()."""
    global _can_redefine, _next_color_id

    curses.start_color()
    curses.use_default_colors()

    _can_redefine = curses.can_change_color()
    _next_color_id = 50

    # Allocate colors
    c_bg_primary = _alloc_color(BG_PRIMARY)
    c_bg_secondary = _alloc_color(BG_SECONDARY)
    c_bg_elevated = _alloc_color(BG_ELEVATED)
    c_bg_input = _alloc_color(BG_INPUT)
    c_bg_status = _alloc_color(BG_STATUS)
    c_bg_today = _alloc_color(BG_TODAY)
    c_text_primary = _alloc_color(TEXT_PRIMARY)
    c_text_secondary = _alloc_color(TEXT_SECONDARY)
    c_text_tertiary = _alloc_color(TEXT_TERTIARY)
    c_text_inverse = _alloc_color(TEXT_INVERSE)
    c_accent_blue = _alloc_color(ACCENT_BLUE)
    c_accent_link = _alloc_color(ACCENT_LINK)
    c_accent_green = _alloc_color(ACCENT_GREEN)
    c_accent_yellow = _alloc_color(ACCENT_YELLOW)
    c_accent_red = _alloc_color(ACCENT_RED)
    c_accent_orange = _alloc_color(ACCENT_ORANGE)
    c_accent_purple = _alloc_color(ACCENT_PURPLE)
    c_cal_blue = _alloc_color(CAL_PEACOCK)
    c_cal_green = _alloc_color(CAL_SAGE)
    c_cal_red = _alloc_color(CAL_TOMATO)
    c_cal_purple = _alloc_color(CAL_GRAPE)
    c_cal_yellow = _alloc_color(CAL_BANANA)
    c_cal_orange = _alloc_color(CAL_TANGERINE)
    c_cal_graphite = _alloc_color(CAL_GRAPHITE)
    c_border = _alloc_color(BORDER_SUBTLE)
    c_status_unread = _alloc_color(STATUS_UNREAD)

    # Initialize pairs
    curses.init_pair(PAIR_NORMAL, c_text_primary, c_bg_primary)
    curses.init_pair(PAIR_HEADER, c_text_inverse, c_accent_blue)
    curses.init_pair(PAIR_SIDEBAR, c_text_secondary, c_bg_secondary)
    curses.init_pair(PAIR_SIDEBAR_SELECTED, c_text_primary, c_bg_elevated)
    curses.init_pair(PAIR_STATUS_BAR, c_text_secondary, c_bg_status)
    curses.init_pair(PAIR_EVENT_NORMAL, c_status_unread, c_bg_primary)
    curses.init_pair(PAIR_EVENT_DIM, c_text_secondary, c_bg_primary)
    curses.init_pair(PAIR_EVENT_SELECTED, c_text_primary, c_bg_elevated)
    curses.init_pair(PAIR_EVENT_SELECTED_BOLD, c_status_unread, c_bg_elevated)
    curses.init_pair(PAIR_ACCENT_RED, c_accent_red, c_bg_primary)
    curses.init_pair(PAIR_ACCENT_BLUE, c_accent_link, c_bg_primary)
    curses.init_pair(PAIR_ACCENT_GREEN, c_accent_green, c_bg_primary)
    curses.init_pair(PAIR_ACCENT_YELLOW, c_accent_yellow, c_bg_primary)
    curses.init_pair(PAIR_ACCENT_PURPLE, c_accent_purple, c_bg_primary)
    curses.init_pair(PAIR_INPUT, c_text_primary, c_bg_input)
    curses.init_pair(PAIR_BORDER, c_border, c_bg_primary)
    curses.init_pair(PAIR_SNIPPET, c_text_tertiary, c_bg_primary)
    curses.init_pair(PAIR_DATE, c_text_tertiary, c_bg_primary)
    curses.init_pair(PAIR_CAL_BLUE, c_cal_blue, c_bg_primary)
    curses.init_pair(PAIR_TITLE, c_accent_blue, c_bg_primary)
    curses.init_pair(PAIR_COMPOSE_FIELD, c_text_primary, c_bg_input)
    curses.init_pair(PAIR_HELP_KEY, c_accent_link, c_bg_status)
    curses.init_pair(PAIR_HELP_DESC, c_text_secondary, c_bg_status)
    curses.init_pair(PAIR_TAB_ACTIVE, c_text_inverse, c_accent_blue)
    curses.init_pair(PAIR_TAB_INACTIVE, c_text_tertiary, c_bg_secondary)
    curses.init_pair(PAIR_SEARCH_BOX, c_text_primary, c_bg_input)
    curses.init_pair(PAIR_CAL_GREEN, c_cal_green, c_bg_primary)
    curses.init_pair(PAIR_CAL_RED, c_cal_red, c_bg_primary)
    curses.init_pair(PAIR_CAL_PURPLE, c_cal_purple, c_bg_primary)
    curses.init_pair(PAIR_CAL_YELLOW, c_cal_yellow, c_bg_primary)
    curses.init_pair(PAIR_STATUS_MSG, c_accent_green, c_bg_status)
    curses.init_pair(PAIR_STATUS_ERR, c_accent_red, c_bg_status)
    curses.init_pair(PAIR_TODAY_HIGHLIGHT, c_text_primary, c_bg_today)
    curses.init_pair(PAIR_CAL_ORANGE, c_cal_orange, c_bg_primary)
    curses.init_pair(PAIR_CAL_GRAPHITE, c_cal_graphite, c_bg_primary)
    curses.init_pair(PAIR_LINK, c_accent_link, c_bg_primary)
    curses.init_pair(PAIR_NOW_LINE, c_accent_red, c_bg_primary)
