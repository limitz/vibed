"""Tests for the mock Gmail MCP client."""

import asyncio
import unittest
from mock_client import MockGmailClient
from models import Profile, Label, EmailHeader, Email, Thread, Draft, SearchResult


def run(coro):
    """Helper to run async tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


class TestMockGetProfile(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()

    def test_returns_profile(self):
        profile = run(self.client.get_profile())
        self.assertIsInstance(profile, Profile)
        self.assertIn("@", profile.email)
        self.assertGreater(profile.messages_total, 0)


class TestMockListLabels(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()

    def test_returns_labels(self):
        labels = run(self.client.list_labels())
        self.assertIsInstance(labels, list)
        self.assertTrue(all(isinstance(l, Label) for l in labels))

    def test_has_system_labels(self):
        labels = run(self.client.list_labels())
        names = [l.name for l in labels]
        self.assertIn("INBOX", names)
        self.assertIn("SENT", names)
        self.assertIn("DRAFT", names)

    def test_has_user_labels(self):
        labels = run(self.client.list_labels())
        user_labels = [l for l in labels if l.label_type == "user"]
        self.assertGreater(len(user_labels), 0)


class TestMockSearchMessages(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()

    def test_returns_all_messages(self):
        result = run(self.client.search_messages())
        self.assertIsInstance(result, SearchResult)
        self.assertGreater(len(result.messages), 0)
        self.assertTrue(all(isinstance(m, EmailHeader) for m in result.messages))

    def test_search_unread(self):
        result = run(self.client.search_messages(query="is:unread"))
        self.assertTrue(all(m.is_unread for m in result.messages))

    def test_search_starred(self):
        result = run(self.client.search_messages(query="is:starred"))
        self.assertTrue(all(m.is_starred for m in result.messages))

    def test_search_attachment(self):
        result = run(self.client.search_messages(query="has:attachment"))
        self.assertTrue(all(m.has_attachment for m in result.messages))

    def test_search_text(self):
        result = run(self.client.search_messages(query="launch"))
        self.assertGreater(len(result.messages), 0)
        # Check the word appears in subject or snippet
        for m in result.messages:
            text = f"{m.subject} {m.snippet}".lower()
            self.assertIn("launch", text)

    def test_search_from(self):
        result = run(self.client.search_messages(query="from:sarah"))
        self.assertGreater(len(result.messages), 0)

    def test_pagination(self):
        result = run(self.client.search_messages(max_results=5))
        self.assertEqual(len(result.messages), 5)
        self.assertIsNotNone(result.next_page_token)

        result2 = run(self.client.search_messages(max_results=5, page_token=result.next_page_token))
        self.assertGreater(len(result2.messages), 0)
        # No overlap
        ids1 = {m.message_id for m in result.messages}
        ids2 = {m.message_id for m in result2.messages}
        self.assertEqual(ids1 & ids2, set())


class TestMockReadMessage(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()

    def test_read_detailed_message(self):
        email = run(self.client.read_message("msg_001"))
        self.assertIsInstance(email, Email)
        self.assertEqual(email.message_id, "msg_001")
        self.assertIn("Sarah", email.sender)
        self.assertGreater(len(email.body_text), 50)
        self.assertTrue(email.has_attachment)
        self.assertGreater(len(email.attachments), 0)

    def test_read_generated_message(self):
        email = run(self.client.read_message("msg_010"))
        self.assertIsInstance(email, Email)
        self.assertGreater(len(email.body_text), 0)

    def test_read_nonexistent(self):
        with self.assertRaises(ValueError):
            run(self.client.read_message("nonexistent"))


class TestMockReadThread(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()

    def test_read_detailed_thread(self):
        thread = run(self.client.read_thread("thread_005"))
        self.assertIsInstance(thread, Thread)
        self.assertEqual(len(thread.messages), 3)
        self.assertIn("auth-service", thread.subject)

    def test_read_generated_thread(self):
        thread = run(self.client.read_thread("thread_010"))
        self.assertEqual(len(thread.messages), 1)

    def test_read_nonexistent(self):
        with self.assertRaises(ValueError):
            run(self.client.read_thread("nonexistent"))


class TestMockCreateDraft(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()

    def test_create_simple_draft(self):
        draft = run(self.client.create_draft(
            body="Hello!", to="test@test.com", subject="Test"
        ))
        self.assertIsInstance(draft, Draft)
        self.assertEqual(draft.body, "Hello!")
        self.assertEqual(draft.to, "test@test.com")
        self.assertTrue(draft.draft_id.startswith("draft_"))

    def test_create_reply_draft(self):
        draft = run(self.client.create_draft(
            body="Thanks!", thread_id="thread_001"
        ))
        self.assertEqual(draft.thread_id, "thread_001")


class TestMockListDrafts(unittest.TestCase):
    def setUp(self):
        self.client = MockGmailClient()

    def test_list_drafts(self):
        result = run(self.client.list_drafts())
        self.assertGreater(len(result.drafts), 0)
        self.assertTrue(all(isinstance(d, Draft) for d in result.drafts))


if __name__ == "__main__":
    unittest.main()
