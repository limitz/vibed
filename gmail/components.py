"""Reusable curses UI components for the Gmail client."""

import curses
import textwrap
from typing import Optional
from colors import (
    PAIR_NORMAL, PAIR_HEADER, PAIR_SIDEBAR, PAIR_SIDEBAR_SELECTED,
    PAIR_STATUS_BAR, PAIR_EMAIL_UNREAD, PAIR_EMAIL_READ,
    PAIR_EMAIL_SELECTED, PAIR_EMAIL_SELECTED_UNREAD,
    PAIR_ACCENT_RED, PAIR_ACCENT_BLUE, PAIR_ACCENT_GREEN,
    PAIR_ACCENT_YELLOW, PAIR_ACCENT_PURPLE,
    PAIR_INPUT, PAIR_BORDER, PAIR_SNIPPET, PAIR_DATE,
    PAIR_LABEL_TAG, PAIR_TITLE, PAIR_COMPOSE_FIELD,
    PAIR_HELP_KEY, PAIR_HELP_DESC, PAIR_TAB_ACTIVE, PAIR_TAB_INACTIVE,
    PAIR_SEARCH_BOX, PAIR_MSG_SENDER, PAIR_MSG_BODY,
    PAIR_ATTACHMENT, PAIR_STARRED,
    PAIR_STATUS_MSG, PAIR_STATUS_ERR,
    EMOJI,
)


def safe_addstr(win, y: int, x: int, text: str, attr: int = 0, max_width: int = 0) -> None:
    """Write text to window, clipping to avoid curses errors at boundaries."""
    h, w = win.getmaxyx()
    if y < 0 or y >= h or x >= w:
        return
    if max_width > 0:
        available = min(max_width, w - x)
    else:
        available = w - x
    if available <= 0:
        return
    # Truncate text to fit
    clipped = text[:available]
    try:
        win.addstr(y, x, clipped, attr)
    except curses.error:
        pass  # Writing to bottom-right corner raises error, safe to ignore


def fill_line(win, y: int, attr: int, start_x: int = 0) -> None:
    """Fill the rest of a line with the given attribute."""
    h, w = win.getmaxyx()
    if y < 0 or y >= h:
        return
    remaining = w - start_x
    if remaining > 0:
        safe_addstr(win, y, start_x, " " * remaining, attr)


def draw_header(win, y: int, profile_email: str, current_view: str) -> int:
    """Draw the top header bar. Returns next y position."""
    h, w = win.getmaxyx()
    attr = curses.color_pair(PAIR_HEADER) | curses.A_BOLD

    # Fill header line
    fill_line(win, y, attr)

    # Gmail logo / title — fixed positions for consistent spacing
    safe_addstr(win, y, 1, EMOJI['mail'], attr)
    safe_addstr(win, y, 4, "Gmail", attr)

    # Current view indicator — 1 space after "Gmail"
    safe_addstr(win, y, 10, current_view, attr)

    # Profile email on right
    email_text = f"{EMOJI['person']} {profile_email} "
    safe_addstr(win, y, w - len(profile_email) - 6, email_text, attr)

    return y + 1


def draw_status_bar(
    win,
    y: int,
    hints: list[tuple[str, str]],
    status_message: str = "",
    status_is_error: bool = False,
    loading: bool = False,
) -> int:
    """Draw the single bottom status bar with key hints and status message."""
    h, w = win.getmaxyx()
    attr_bar = curses.color_pair(PAIR_STATUS_BAR)
    attr_key = curses.color_pair(PAIR_HELP_KEY) | curses.A_BOLD
    attr_desc = curses.color_pair(PAIR_HELP_DESC)

    fill_line(win, y, attr_bar)

    # Status message on the left (if any)
    x = 1
    if status_message:
        attr_msg = curses.color_pair(PAIR_STATUS_ERR) if status_is_error else curses.color_pair(PAIR_STATUS_MSG)
        safe_addstr(win, y, x, f" {status_message} ", attr_msg)
        x += len(status_message) + 3
        safe_addstr(win, y, x, "│", attr_bar)
        x += 2
    elif loading:
        attr_load = curses.color_pair(PAIR_STATUS_MSG)
        safe_addstr(win, y, x, f" {EMOJI['refresh']} Loading… ", attr_load)
        x += 14
        safe_addstr(win, y, x, "│", attr_bar)
        x += 2

    # Key hints on the right portion
    for key, desc in hints:
        if x >= w - 10:
            break
        safe_addstr(win, y, x, f" {key} ", attr_key)
        x += len(key) + 2
        safe_addstr(win, y, x, f" {desc}", attr_desc)
        x += len(desc) + 3

    return y + 1


def draw_sidebar(
    win,
    y_start: int,
    y_end: int,
    width: int,
    items: list[dict],
    selected_idx: int,
    scroll_offset: int = 0,
) -> None:
    """Draw the sidebar with label/folder items.

    Each item dict has: name, emoji, count (optional), unread (optional)
    Supports: is_separator (divider line), is_action (compose button style)
    """
    attr_normal = curses.color_pair(PAIR_SIDEBAR)
    attr_selected = curses.color_pair(PAIR_SIDEBAR_SELECTED) | curses.A_BOLD
    attr_border = curses.color_pair(PAIR_BORDER)
    attr_action = curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD
    attr_action_sel = curses.color_pair(PAIR_TAB_ACTIVE) | curses.A_BOLD

    visible = y_end - y_start
    for i in range(visible):
        idx = i + scroll_offset
        y = y_start + i

        if idx >= len(items):
            fill_line(win, y, attr_normal, 0)
            safe_addstr(win, y, width - 1, "│", attr_border)
            continue

        item = items[idx]
        is_selected = idx == selected_idx
        is_separator = item.get("is_separator", False)
        is_action = item.get("is_action", False)

        # Separator line
        if is_separator:
            fill_line(win, y, attr_normal, 0)
            safe_addstr(win, y, 2, "─" * (width - 4), attr_border)
            safe_addstr(win, y, width - 1, "│", attr_border)
            continue

        # Compose button style
        if is_action:
            if is_selected:
                fill_line(win, y, attr_action_sel, 0)
                safe_addstr(win, y, 0, "▌", curses.color_pair(PAIR_ACCENT_RED) | curses.A_BOLD)
            else:
                fill_line(win, y, attr_normal, 0)
            emoji = item.get("emoji", "")
            name = item.get("name", "")
            text = f" {emoji} {name} "
            attr = attr_action_sel if is_selected else attr_action
            safe_addstr(win, y, 2, text, attr)
            safe_addstr(win, y, width - 1, "│", attr_border)
            continue

        # Normal item
        attr = attr_selected if is_selected else attr_normal
        fill_line(win, y, attr, 0)

        # Selection indicator
        if is_selected:
            safe_addstr(win, y, 0, "▌", curses.color_pair(PAIR_ACCENT_RED) | curses.A_BOLD)

        x = 2

        # Emoji — use fixed 3-col slot (2 for emoji + 1 space)
        emoji = item.get("emoji", "")
        if emoji:
            safe_addstr(win, y, x, emoji, attr)
            x += 3  # fixed: emoji takes ~2 cols + 1 space

        # Name
        name = item.get("name", "")
        max_name_w = width - x - 8
        if len(name) > max_name_w:
            name = name[:max_name_w - 1] + "…"
        safe_addstr(win, y, x, name, attr)

        # Unread count (in a rounded badge style)
        unread = item.get("unread", 0)
        if unread > 0:
            count_str = str(unread)
            cx = width - len(count_str) - 3
            safe_addstr(win, y, cx, count_str,
                        curses.color_pair(PAIR_ACCENT_RED) | curses.A_BOLD)

        # Right border
        safe_addstr(win, y, width - 1, "│", attr_border)


def draw_email_list(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    emails: list,
    selected_idx: int,
    scroll_offset: int = 0,
) -> None:
    """Draw the email list. Each email gets 2 lines."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)
    visible_lines = y_end - y_start

    y = y_start
    for i in range(len(emails)):
        idx = i + scroll_offset
        if idx >= len(emails):
            break
        if y + 1 >= y_end:
            break

        email = emails[idx]
        is_selected = idx == selected_idx
        is_unread = getattr(email, "is_unread", False)
        is_starred = getattr(email, "is_starred", False)
        has_attachment = getattr(email, "has_attachment", False)

        # Choose colors
        if is_selected and is_unread:
            attr_main = curses.color_pair(PAIR_EMAIL_SELECTED_UNREAD) | curses.A_BOLD
            attr_snip = curses.color_pair(PAIR_EMAIL_SELECTED)
        elif is_selected:
            attr_main = curses.color_pair(PAIR_EMAIL_SELECTED)
            attr_snip = curses.color_pair(PAIR_EMAIL_SELECTED)
        elif is_unread:
            attr_main = curses.color_pair(PAIR_EMAIL_UNREAD) | curses.A_BOLD
            attr_snip = curses.color_pair(PAIR_SNIPPET)
        else:
            attr_main = curses.color_pair(PAIR_EMAIL_READ)
            attr_snip = curses.color_pair(PAIR_SNIPPET)

        content_w = w - x_start

        # Line 1: [star] [unread dot] sender    date  [attachment]
        fill_line(win, y, attr_main if is_selected else curses.color_pair(PAIR_NORMAL), x_start)
        x = x_start + 1

        # Selection highlight bar
        if is_selected:
            safe_addstr(win, y, x_start, "▌", curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD)

        # Star
        if is_starred:
            safe_addstr(win, y, x, EMOJI["starred"], curses.color_pair(PAIR_STARRED))
            x += 3
        else:
            x += 3

        # Unread dot
        if is_unread:
            safe_addstr(win, y, x, EMOJI["dot"], curses.color_pair(PAIR_ACCENT_BLUE))
            x += 2
        else:
            x += 2

        # Sender
        sender = getattr(email, "sender", "Unknown")
        max_sender = min(22, content_w // 3)
        if len(sender) > max_sender:
            sender = sender[:max_sender - 1] + "…"
        safe_addstr(win, y, x, sender, attr_main)
        x += max_sender + 1

        # Subject
        subject = getattr(email, "subject", "(no subject)")
        # Date
        date = getattr(email, "date", None)
        date_str = _format_date(date) if date else ""
        attachment_str = f" {EMOJI['attachment']}" if has_attachment else ""
        right_text = f"{attachment_str} {date_str} "
        right_x = w - len(right_text) - 1

        max_subject = right_x - x - 1
        if max_subject > 0:
            if len(subject) > max_subject:
                subject = subject[:max_subject - 1] + "…"
            safe_addstr(win, y, x, subject, attr_main)

        # Date and attachment on right
        if has_attachment:
            safe_addstr(win, y, right_x, f" {EMOJI['attachment']}",
                        curses.color_pair(PAIR_ATTACHMENT))
            safe_addstr(win, y, right_x + 3, f" {date_str} ",
                        curses.color_pair(PAIR_DATE))
        else:
            safe_addstr(win, y, right_x + 3, f" {date_str} ",
                        curses.color_pair(PAIR_DATE))

        y += 1
        if y >= y_end:
            break

        # Line 2: snippet
        fill_line(win, y, attr_snip if is_selected else curses.color_pair(PAIR_NORMAL), x_start)
        snippet = getattr(email, "snippet", "")
        max_snippet = content_w - 8
        if len(snippet) > max_snippet:
            snippet = snippet[:max_snippet - 1] + "…"
        safe_addstr(win, y, x_start + 7, snippet, attr_snip)

        y += 1

        # Separator line
        if y < y_end:
            fill_line(win, y, curses.color_pair(PAIR_NORMAL), x_start)
            separator = "─" * (content_w - 2)
            safe_addstr(win, y, x_start + 1, separator, curses.color_pair(PAIR_BORDER))
            y += 1


def draw_message_view(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    email,
    scroll_offset: int = 0,
) -> None:
    """Draw full message view."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)
    content_w = w - x_start - 2

    lines = _build_message_lines(email, content_w)

    y = y_start
    for i, (text, attr) in enumerate(lines):
        if i < scroll_offset:
            continue
        if y >= y_end:
            break
        fill_line(win, y, attr_normal, x_start)
        safe_addstr(win, y, x_start + 1, text, attr, max_width=content_w)
        y += 1

    # Fill remaining
    while y < y_end:
        fill_line(win, y, attr_normal, x_start)
        y += 1


def _build_message_lines(email, width: int) -> list[tuple[str, int]]:
    """Build the rendered lines for an email message view."""
    lines: list[tuple[str, int]] = []
    attr_title = curses.color_pair(PAIR_TITLE) | curses.A_BOLD
    attr_sender = curses.color_pair(PAIR_MSG_SENDER) | curses.A_BOLD
    attr_field = curses.color_pair(PAIR_ACCENT_BLUE)
    attr_body = curses.color_pair(PAIR_MSG_BODY)
    attr_dim = curses.color_pair(PAIR_SNIPPET)
    attr_attachment = curses.color_pair(PAIR_ATTACHMENT)

    # Subject
    subject = getattr(email, "subject", "(no subject)")
    lines.append(("", attr_body))
    for sub_line in textwrap.wrap(subject, width - 2):
        lines.append((f" {sub_line}", attr_title))
    lines.append(("", attr_body))

    # Divider
    lines.append((" " + "─" * (width - 2), curses.color_pair(PAIR_BORDER)))
    lines.append(("", attr_body))

    # From
    sender = getattr(email, "sender", "")
    sender_email = getattr(email, "sender_email", "")
    lines.append((f" {EMOJI['person']} From:  {sender} <{sender_email}>", attr_sender))

    # To
    to = getattr(email, "to", "")
    if to:
        lines.append((f"    To:    {to}", attr_field))

    # CC
    cc = getattr(email, "cc", "")
    if cc:
        lines.append((f"    Cc:    {cc}", attr_field))

    # Date
    date = getattr(email, "date", None)
    if date:
        date_str = date.strftime("%A, %B %d, %Y at %I:%M %p")
        lines.append((f" {EMOJI['clock']} Date:  {date_str}", attr_dim))

    # Labels
    labels = getattr(email, "labels", [])
    if labels:
        label_str = " ".join(f"[{l}]" for l in labels if not l.startswith("CATEGORY_"))
        lines.append((f" {EMOJI['label']} Labels: {label_str}", curses.color_pair(PAIR_ACCENT_PURPLE)))

    # Attachments
    attachments = getattr(email, "attachments", [])
    if attachments:
        lines.append(("", attr_body))
        lines.append((f" {EMOJI['attachment']} Attachments:", attr_attachment))
        for att in attachments:
            lines.append((f"    • {att}", attr_attachment))

    # Body
    lines.append(("", attr_body))
    lines.append((" " + "─" * (width - 2), curses.color_pair(PAIR_BORDER)))
    lines.append(("", attr_body))

    body = getattr(email, "body_text", "") or getattr(email, "snippet", "")
    for paragraph in body.split("\n"):
        if paragraph.strip() == "":
            lines.append(("", attr_body))
        else:
            wrapped = textwrap.wrap(paragraph, width - 4)
            for wl in wrapped:
                lines.append((f"  {wl}", attr_body))

    lines.append(("", attr_body))
    return lines


def draw_compose_screen(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    fields: dict,
    active_field: str,
    cursor_pos: int = 0,
) -> None:
    """Draw the compose/draft screen."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)
    attr_label = curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD
    attr_field = curses.color_pair(PAIR_COMPOSE_FIELD)
    attr_active = curses.color_pair(PAIR_INPUT) | curses.A_UNDERLINE
    content_w = w - x_start - 4

    y = y_start + 1

    # Title
    fill_line(win, y, attr_normal, x_start)
    safe_addstr(win, y, x_start + 2, f"{EMOJI['compose']} New Message",
                curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
    y += 1
    fill_line(win, y, attr_normal, x_start)
    safe_addstr(win, y, x_start + 2, "─" * (content_w - 2), curses.color_pair(PAIR_BORDER))
    y += 2

    field_order = [("to", "To:     "), ("cc", "Cc:     "), ("bcc", "Bcc:    "),
                   ("subject", "Subject:"), ("body", "Body:   ")]

    for field_key, label in field_order:
        fill_line(win, y, attr_normal, x_start)
        is_active = field_key == active_field
        safe_addstr(win, y, x_start + 2, label, attr_label)

        value = fields.get(field_key, "")
        field_attr = attr_active if is_active else attr_field

        if field_key == "body":
            # Multi-line body
            y += 1
            body_lines = value.split("\n") if value else [""]
            for bl in body_lines:
                if y >= y_end - 1:
                    break
                fill_line(win, y, attr_normal, x_start)
                safe_addstr(win, y, x_start + 4, bl[:content_w - 6], field_attr)
                y += 1
            # Add empty lines for editing space
            for _ in range(3):
                if y >= y_end - 1:
                    break
                fill_line(win, y, attr_normal, x_start)
                safe_addstr(win, y, x_start + 4, " " * (content_w - 6), field_attr)
                y += 1
        else:
            # Single-line field
            field_w = content_w - len(label) - 4
            display_val = value[:field_w] if value else ""
            padded = display_val + " " * max(0, field_w - len(display_val))
            safe_addstr(win, y, x_start + 2 + len(label) + 1, padded, field_attr)
            y += 2

    # Fill remaining
    while y < y_end:
        fill_line(win, y, attr_normal, x_start)
        y += 1


def draw_thread_view(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    thread,
    scroll_offset: int = 0,
) -> None:
    """Draw a thread/conversation view."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)
    content_w = w - x_start - 2

    lines = _build_thread_lines(thread, content_w)

    y = y_start
    for i, (text, attr) in enumerate(lines):
        if i < scroll_offset:
            continue
        if y >= y_end:
            break
        fill_line(win, y, attr_normal, x_start)
        safe_addstr(win, y, x_start + 1, text, attr, max_width=content_w)
        y += 1

    while y < y_end:
        fill_line(win, y, attr_normal, x_start)
        y += 1


def _build_thread_lines(thread, width: int) -> list[tuple[str, int]]:
    """Build rendered lines for a thread view."""
    lines: list[tuple[str, int]] = []
    attr_title = curses.color_pair(PAIR_TITLE) | curses.A_BOLD
    attr_sender = curses.color_pair(PAIR_MSG_SENDER) | curses.A_BOLD
    attr_body = curses.color_pair(PAIR_MSG_BODY)
    attr_dim = curses.color_pair(PAIR_SNIPPET)
    attr_border = curses.color_pair(PAIR_BORDER)

    # Thread subject
    lines.append(("", attr_body))
    subject = getattr(thread, "subject", "")
    msg_count = len(getattr(thread, "messages", []))
    for sub_line in textwrap.wrap(f"{subject}  ({msg_count} messages)", width - 2):
        lines.append((f" {sub_line}", attr_title))
    lines.append(("", attr_body))
    lines.append((" " + "═" * (width - 2), attr_border))

    messages = getattr(thread, "messages", [])
    for mi, msg in enumerate(messages):
        lines.append(("", attr_body))

        # Sender and date
        sender = getattr(msg, "sender", "Unknown")
        sender_email = getattr(msg, "sender_email", "")
        date = getattr(msg, "date", None)
        date_str = _format_date(date) if date else ""

        lines.append((f" {EMOJI['person']} {sender} <{sender_email}>", attr_sender))
        if date_str:
            lines.append((f"   {date_str}", attr_dim))
        lines.append(("", attr_body))

        # Body
        body = getattr(msg, "body_text", "") or getattr(msg, "snippet", "")
        for paragraph in body.split("\n"):
            if paragraph.strip() == "":
                lines.append(("", attr_body))
            else:
                wrapped = textwrap.wrap(paragraph, width - 6)
                for wl in wrapped:
                    lines.append((f"    {wl}", attr_body))

        # Divider between messages
        if mi < len(messages) - 1:
            lines.append(("", attr_body))
            lines.append((" " + "─" * (width - 2), attr_border))

    lines.append(("", attr_body))
    return lines


def draw_search_bar(
    win,
    y: int,
    x_start: int,
    query: str,
    is_active: bool,
) -> None:
    """Draw the search input bar."""
    h, w = win.getmaxyx()
    attr = curses.color_pair(PAIR_SEARCH_BOX)
    attr_active = curses.color_pair(PAIR_INPUT) | curses.A_UNDERLINE

    fill_line(win, y, curses.color_pair(PAIR_NORMAL), x_start)

    # Search icon
    safe_addstr(win, y, x_start + 1, f" {EMOJI['search']} ", curses.color_pair(PAIR_ACCENT_BLUE))

    # Input field
    field_w = w - x_start - 8
    if is_active:
        display = query[:field_w]
        padded = display + " " * max(0, field_w - len(display))
        safe_addstr(win, y, x_start + 5, padded, attr_active)
    else:
        if query:
            safe_addstr(win, y, x_start + 5, query[:field_w], attr)
        else:
            safe_addstr(win, y, x_start + 5, "Search mail…"[:field_w],
                        curses.color_pair(PAIR_SNIPPET))


def draw_draft_list(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    drafts: list,
    selected_idx: int,
    scroll_offset: int = 0,
) -> None:
    """Draw the drafts list."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)
    content_w = w - x_start

    y = y_start
    fill_line(win, y, attr_normal, x_start)
    safe_addstr(win, y, x_start + 2, f"{EMOJI['drafts']} Drafts ({len(drafts)})",
                curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
    y += 1
    fill_line(win, y, attr_normal, x_start)
    safe_addstr(win, y, x_start + 2, "─" * (content_w - 4), curses.color_pair(PAIR_BORDER))
    y += 1

    for i in range(len(drafts)):
        idx = i + scroll_offset
        if idx >= len(drafts):
            break
        if y + 1 >= y_end:
            break

        draft = drafts[idx]
        is_selected = idx == selected_idx

        if is_selected:
            attr = curses.color_pair(PAIR_EMAIL_SELECTED) | curses.A_BOLD
        else:
            attr = curses.color_pair(PAIR_EMAIL_READ)

        fill_line(win, y, attr if is_selected else attr_normal, x_start)

        if is_selected:
            safe_addstr(win, y, x_start, "▌", curses.color_pair(PAIR_ACCENT_GREEN) | curses.A_BOLD)

        # To
        to = getattr(draft, "to", "") or "(no recipient)"
        subject = getattr(draft, "subject", "") or "(no subject)"
        safe_addstr(win, y, x_start + 2, f"To: {to[:30]}", attr)
        safe_addstr(win, y, x_start + 36, f"  {subject[:content_w - 40]}", attr)
        y += 1

        # Snippet of body
        fill_line(win, y, attr_normal, x_start)
        body = getattr(draft, "body", "")[:content_w - 8]
        if not body:
            body = "(empty draft)"
        safe_addstr(win, y, x_start + 4, body, curses.color_pair(PAIR_SNIPPET))
        y += 1

        # Separator
        if y < y_end:
            fill_line(win, y, attr_normal, x_start)
            safe_addstr(win, y, x_start + 2, "─" * (content_w - 4), curses.color_pair(PAIR_BORDER))
            y += 1

    while y < y_end:
        fill_line(win, y, attr_normal, x_start)
        y += 1


def _format_date(dt) -> str:
    """Format a datetime for display — relative if recent."""
    if dt is None:
        return ""
    from datetime import datetime, timedelta
    now = datetime.now()
    diff = now - dt

    if diff < timedelta(minutes=1):
        return "just now"
    elif diff < timedelta(hours=1):
        mins = int(diff.total_seconds() / 60)
        return f"{mins}m ago"
    elif diff < timedelta(hours=24):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours}h ago"
    elif diff < timedelta(days=7):
        days = diff.days
        return f"{days}d ago"
    else:
        return dt.strftime("%b %d")
