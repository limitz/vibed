"""Tests for UI components (non-curses logic)."""

import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from models import Email, EmailHeader, Thread, ThreadMessage

# Check if we can initialize curses (need a terminal)
_HAVE_CURSES = False
try:
    import curses
    # We can't actually init curses in test, so we mock color_pair
    _HAVE_CURSES = True
except ImportError:
    pass


class TestFormatDate(unittest.TestCase):
    def test_format_just_now(self):
        from components import _format_date
        result = _format_date(datetime.now())
        self.assertEqual(result, "just now")

    def test_format_minutes(self):
        from components import _format_date
        dt = datetime.now() - timedelta(minutes=15)
        result = _format_date(dt)
        self.assertIn("m ago", result)

    def test_format_hours(self):
        from components import _format_date
        dt = datetime.now() - timedelta(hours=5)
        result = _format_date(dt)
        self.assertIn("h ago", result)

    def test_format_days(self):
        from components import _format_date
        dt = datetime.now() - timedelta(days=3)
        result = _format_date(dt)
        self.assertIn("d ago", result)

    def test_format_old_date(self):
        from components import _format_date
        dt = datetime.now() - timedelta(days=30)
        result = _format_date(dt)
        self.assertIn(dt.strftime("%b"), result)

    def test_format_none(self):
        from components import _format_date
        self.assertEqual(_format_date(None), "")


def _mock_curses_for_build():
    """Patch curses.color_pair and curses.A_BOLD for testing without a terminal."""
    return patch.multiple(
        "curses",
        color_pair=lambda x: x,
        A_BOLD=0,
        A_UNDERLINE=0,
    )


class TestBuildMessageLines(unittest.TestCase):
    def test_builds_lines_for_email(self):
        with _mock_curses_for_build():
            from components import _build_message_lines
            email = Email(
                message_id="m1", thread_id="t1",
                subject="Test Subject",
                sender="Alice", sender_email="alice@test.com",
                to="bob@test.com",
                body_text="Hello world!\n\nSecond paragraph.",
                attachments=["doc.pdf"],
            )
            lines = _build_message_lines(email, 80)
            texts = [l[0] for l in lines]
            combined = " ".join(texts)
            self.assertIn("Test Subject", combined)
            self.assertIn("Alice", combined)
            self.assertIn("bob@test.com", combined)
            self.assertIn("Hello world", combined)
            self.assertIn("doc.pdf", combined)

    def test_wraps_long_subject(self):
        with _mock_curses_for_build():
            from components import _build_message_lines
            email = Email(
                message_id="m1", thread_id="t1",
                subject="A" * 120,
                sender="X", sender_email="x@y.com",
                to="z@y.com",
                body_text="Short body",
            )
            lines = _build_message_lines(email, 40)
            subject_lines = [l for l in lines if "A" * 10 in l[0]]
            self.assertGreater(len(subject_lines), 1)


class TestBuildThreadLines(unittest.TestCase):
    def test_builds_thread_lines(self):
        with _mock_curses_for_build():
            from components import _build_thread_lines
            thread = Thread(
                thread_id="t1",
                subject="Conversation",
                messages=[
                    ThreadMessage(
                        message_id="m1", sender="Alice", sender_email="a@b.com",
                        date=datetime.now(), body_text="First message",
                    ),
                    ThreadMessage(
                        message_id="m2", sender="Bob", sender_email="b@b.com",
                        date=datetime.now(), body_text="Reply message",
                    ),
                ],
            )
            lines = _build_thread_lines(thread, 80)
            texts = " ".join(l[0] for l in lines)
            self.assertIn("Conversation", texts)
            self.assertIn("2 messages", texts)
            self.assertIn("Alice", texts)
            self.assertIn("Bob", texts)
            self.assertIn("First message", texts)
            self.assertIn("Reply message", texts)


class TestColorModule(unittest.TestCase):
    def test_rgb_to_curses(self):
        from colors import RGB
        white = RGB(255, 255, 255)
        r, g, b = white.to_curses()
        self.assertEqual(r, 1000)
        self.assertEqual(g, 1000)
        self.assertEqual(b, 1000)

    def test_rgb_black(self):
        from colors import RGB
        black = RGB(0, 0, 0)
        r, g, b = black.to_curses()
        self.assertEqual(r, 0)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)

    def test_rgb_midtone(self):
        from colors import RGB
        mid = RGB(128, 128, 128)
        r, g, b = mid.to_curses()
        self.assertTrue(490 <= r <= 510)  # ~501


class TestEmojiConstants(unittest.TestCase):
    def test_all_emojis_are_strings(self):
        from colors import EMOJI
        for key, val in EMOJI.items():
            self.assertIsInstance(val, str, f"EMOJI[{key}] is not a string")
            self.assertGreater(len(val), 0, f"EMOJI[{key}] is empty")


if __name__ == "__main__":
    unittest.main()
