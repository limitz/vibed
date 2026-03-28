"""Tests for the Gmail app controller."""

import asyncio
import unittest
from unittest.mock import MagicMock, patch
from app import GmailApp, View
from mock_client import MockGmailClient


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestGmailAppInit(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()
        self.app = GmailApp(self.client)

    def test_initial_state(self):
        self.assertEqual(self.app.view, View.INBOX)
        self.assertTrue(self.app.running)
        self.assertIsNone(self.app.profile)
        self.assertEqual(self.app.emails, [])

    def test_init_loads_data(self):
        run(self.app.init())
        self.assertIsNotNone(self.app.profile)
        self.assertIn("@", self.app.profile.email)
        self.assertGreater(len(self.app.labels), 0)
        self.assertGreater(len(self.app.emails), 0)
        self.assertGreater(len(self.app.sidebar_items), len([]))

    def test_sidebar_has_unread_counts(self):
        run(self.app.init())
        inbox_item = next(i for i in self.app.sidebar_items if i["name"] == "Inbox")
        self.assertIn("unread", inbox_item)


class TestGmailAppNavigation(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()
        self.app = GmailApp(self.client)
        run(self.app.init())

    def test_navigate_down_in_inbox(self):
        self.assertEqual(self.app.email_idx, 0)
        run(self.app.handle_key(ord("j")))  # Down
        self.assertEqual(self.app.email_idx, 1)

    def test_navigate_up_in_inbox(self):
        self.app.email_idx = 3
        run(self.app.handle_key(ord("k")))  # Up
        self.assertEqual(self.app.email_idx, 2)

    def test_navigate_up_stops_at_zero(self):
        self.assertEqual(self.app.email_idx, 0)
        run(self.app.handle_key(ord("k")))
        self.assertEqual(self.app.email_idx, 0)

    def test_navigate_down_stops_at_end(self):
        self.app.email_idx = len(self.app.emails) - 1
        run(self.app.handle_key(ord("j")))
        self.assertEqual(self.app.email_idx, len(self.app.emails) - 1)

    def test_open_message(self):
        run(self.app.handle_key(10))  # Enter
        self.assertEqual(self.app.view, View.MESSAGE)
        self.assertIsNotNone(self.app.current_email)

    def test_back_from_message(self):
        run(self.app.handle_key(10))  # Open
        self.assertEqual(self.app.view, View.MESSAGE)
        run(self.app.handle_key(27))  # Esc
        self.assertEqual(self.app.view, View.INBOX)

    def test_open_thread(self):
        run(self.app.handle_key(10))  # Open message
        run(self.app.handle_key(ord("t")))  # Thread
        self.assertEqual(self.app.view, View.THREAD)
        self.assertIsNotNone(self.app.current_thread)

    def test_open_compose(self):
        run(self.app.handle_key(ord("c")))
        self.assertEqual(self.app.view, View.COMPOSE)
        self.assertEqual(self.app.compose_active_field, "to")

    def test_open_help(self):
        run(self.app.handle_key(ord("?")))
        self.assertEqual(self.app.view, View.HELP)
        run(self.app.handle_key(27))  # Esc
        self.assertEqual(self.app.view, View.INBOX)

    def test_sidebar_focus_toggle(self):
        self.assertFalse(self.app.sidebar_focused)
        run(self.app.handle_key(9))  # Tab
        self.assertTrue(self.app.sidebar_focused)
        run(self.app.handle_key(9))  # Tab again
        self.assertFalse(self.app.sidebar_focused)

    def test_quit(self):
        self.assertTrue(self.app.running)
        run(self.app.handle_key(ord("q")))
        self.assertFalse(self.app.running)


class TestGmailAppSearch(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()
        self.app = GmailApp(self.client)
        run(self.app.init())

    def test_open_search(self):
        run(self.app.handle_key(ord("/")))
        self.assertEqual(self.app.view, View.SEARCH)
        self.assertTrue(self.app.search_active)

    def test_search_typing(self):
        run(self.app.handle_key(ord("/")))
        run(self.app.handle_key(ord("t")))
        run(self.app.handle_key(ord("e")))
        run(self.app.handle_key(ord("s")))
        run(self.app.handle_key(ord("t")))
        self.assertEqual(self.app.search_query, "test")

    def test_search_backspace(self):
        run(self.app.handle_key(ord("/")))
        run(self.app.handle_key(ord("a")))
        run(self.app.handle_key(ord("b")))
        run(self.app.handle_key(127))  # Backspace
        self.assertEqual(self.app.search_query, "a")

    def test_search_execute(self):
        run(self.app.handle_key(ord("/")))
        for ch in "launch":
            run(self.app.handle_key(ord(ch)))
        run(self.app.handle_key(10))  # Enter
        self.assertFalse(self.app.search_active)
        self.assertGreater(len(self.app.emails), 0)

    def test_search_cancel(self):
        run(self.app.handle_key(ord("/")))
        run(self.app.handle_key(27))  # Esc
        self.assertEqual(self.app.view, View.INBOX)


class TestGmailAppCompose(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()
        self.app = GmailApp(self.client)
        run(self.app.init())

    def test_compose_field_navigation(self):
        run(self.app.handle_key(ord("c")))
        self.assertEqual(self.app.compose_active_field, "to")
        run(self.app.handle_key(9))  # Tab
        self.assertEqual(self.app.compose_active_field, "cc")
        run(self.app.handle_key(9))  # Tab
        self.assertEqual(self.app.compose_active_field, "bcc")

    def test_compose_typing(self):
        run(self.app.handle_key(ord("c")))
        for ch in "test@test.com":
            run(self.app.handle_key(ord(ch)))
        self.assertEqual(self.app.compose_fields["to"], "test@test.com")

    def test_compose_save_draft(self):
        run(self.app.handle_key(ord("c")))
        # Type to
        for ch in "test@test.com":
            run(self.app.handle_key(ord(ch)))
        # Tab to subject
        run(self.app.handle_key(9))
        run(self.app.handle_key(9))
        run(self.app.handle_key(9))
        for ch in "Test":
            run(self.app.handle_key(ord(ch)))
        # Tab to body
        run(self.app.handle_key(9))
        for ch in "Hello!":
            run(self.app.handle_key(ord(ch)))
        # Save
        run(self.app.handle_key(19))  # Ctrl+S
        self.assertNotEqual(self.app.view, View.COMPOSE)
        self.assertIn("saved", self.app.status_message.lower())

    def test_compose_cancel(self):
        run(self.app.handle_key(ord("c")))
        run(self.app.handle_key(27))  # Esc
        self.assertEqual(self.app.view, View.INBOX)

    def test_reply_prefills(self):
        run(self.app.handle_key(10))  # Open first message
        run(self.app.handle_key(ord("r")))  # Reply
        self.assertEqual(self.app.view, View.COMPOSE)
        self.assertIn("@", self.app.compose_fields["to"])
        self.assertTrue(self.app.compose_fields["subject"].startswith("Re:"))


class TestGmailAppDrafts(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()
        self.app = GmailApp(self.client)
        run(self.app.init())

    def test_open_drafts(self):
        run(self.app.handle_key(ord("d")))
        self.assertEqual(self.app.view, View.DRAFTS)
        self.assertGreater(len(self.app.drafts), 0)

    def test_draft_navigation(self):
        run(self.app.handle_key(ord("d")))
        self.assertEqual(self.app.draft_idx, 0)
        run(self.app.handle_key(ord("j")))
        self.assertEqual(self.app.draft_idx, 1)

    def test_edit_draft(self):
        run(self.app.handle_key(ord("d")))
        run(self.app.handle_key(10))  # Enter to edit
        self.assertEqual(self.app.view, View.COMPOSE)


class TestGmailAppStar(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()
        self.app = GmailApp(self.client)
        run(self.app.init())

    def test_toggle_star(self):
        original = self.app.emails[0].is_starred
        run(self.app.handle_key(ord("s")))
        self.assertNotEqual(self.app.emails[0].is_starred, original)
        run(self.app.handle_key(ord("s")))
        self.assertEqual(self.app.emails[0].is_starred, original)


class TestGmailAppQuickJump(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()
        self.app = GmailApp(self.client)
        run(self.app.init())

    def test_quick_jump_to_starred(self):
        run(self.app.handle_key(ord("4")))  # Starred (idx 3: Compose, Sep, Inbox, Starred)
        self.assertEqual(self.app.sidebar_idx, 3)

    def test_quick_jump_to_drafts(self):
        run(self.app.handle_key(ord("7")))  # Drafts (index shifted by compose+separator)
        self.assertEqual(self.app.view, View.DRAFTS)


class TestGmailAppRefresh(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()
        self.app = GmailApp(self.client)
        run(self.app.init())

    def test_refresh(self):
        run(self.app.handle_key(ord("R")))
        self.assertIn("Refresh", self.app.status_message)


class TestGmailAppStatusHints(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()
        self.app = GmailApp(self.client)

    def test_inbox_hints(self):
        self.app.view = View.INBOX
        hints = self.app._get_status_hints()
        keys = [h[0] for h in hints]
        self.assertIn("Enter", keys)
        self.assertIn("q", keys)

    def test_compose_hints(self):
        self.app.view = View.COMPOSE
        hints = self.app._get_status_hints()
        keys = [h[0] for h in hints]
        self.assertIn("Ctrl+S", keys)

    def test_message_hints(self):
        self.app.view = View.MESSAGE
        hints = self.app._get_status_hints()
        keys = [h[0] for h in hints]
        self.assertIn("Esc", keys)
        self.assertIn("r", keys)


if __name__ == "__main__":
    unittest.main()
