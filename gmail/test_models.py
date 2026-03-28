"""Tests for data models."""

import unittest
from datetime import datetime
from models import (
    Profile, Label, EmailHeader, Email, Thread, ThreadMessage,
    Draft, SearchResult, DraftList,
)


class TestProfile(unittest.TestCase):
    def test_create_profile(self):
        p = Profile(email="test@gmail.com", messages_total=100, threads_total=50)
        self.assertEqual(p.email, "test@gmail.com")
        self.assertEqual(p.messages_total, 100)
        self.assertEqual(p.threads_total, 50)

    def test_defaults(self):
        p = Profile(email="x@y.com")
        self.assertEqual(p.messages_total, 0)
        self.assertEqual(p.history_id, "")


class TestLabel(unittest.TestCase):
    def test_system_label(self):
        label = Label(id="INBOX", name="INBOX", label_type="system", message_count=10, unread_count=3)
        self.assertEqual(label.label_type, "system")
        self.assertEqual(label.unread_count, 3)

    def test_user_label(self):
        label = Label(id="L1", name="Work")
        self.assertEqual(label.label_type, "user")


class TestEmailHeader(unittest.TestCase):
    def test_create(self):
        now = datetime.now()
        eh = EmailHeader(
            message_id="m1", thread_id="t1", subject="Hello",
            sender="Alice", sender_email="alice@example.com",
            snippet="Hi there", date=now, is_unread=True,
        )
        self.assertTrue(eh.is_unread)
        self.assertFalse(eh.is_starred)
        self.assertEqual(eh.labels, [])

    def test_labels_independent(self):
        """Ensure default mutable list is independent per instance."""
        e1 = EmailHeader(message_id="1", thread_id="1", subject="A",
                         sender="A", sender_email="a@b.com", snippet="", date=datetime.now())
        e2 = EmailHeader(message_id="2", thread_id="2", subject="B",
                         sender="B", sender_email="b@b.com", snippet="", date=datetime.now())
        e1.labels.append("INBOX")
        self.assertEqual(e2.labels, [])


class TestEmail(unittest.TestCase):
    def test_full_email(self):
        e = Email(
            message_id="m1", thread_id="t1", subject="Test",
            sender="Bob", sender_email="bob@test.com", to="me@test.com",
            body_text="Hello world",
        )
        self.assertEqual(e.body_text, "Hello world")
        self.assertEqual(e.cc, "")
        self.assertEqual(e.attachments, [])


class TestThread(unittest.TestCase):
    def test_thread_with_messages(self):
        msgs = [
            ThreadMessage(message_id="m1", sender="A", sender_email="a@b.com",
                          date=datetime.now(), body_text="Hi"),
            ThreadMessage(message_id="m2", sender="B", sender_email="b@b.com",
                          date=datetime.now(), body_text="Hello"),
        ]
        t = Thread(thread_id="t1", subject="Conversation", messages=msgs)
        self.assertEqual(len(t.messages), 2)


class TestDraft(unittest.TestCase):
    def test_draft(self):
        d = Draft(draft_id="d1", message_id="dm1", subject="Draft", to="x@y.com", body="content")
        self.assertEqual(d.body, "content")


class TestSearchResult(unittest.TestCase):
    def test_empty(self):
        sr = SearchResult()
        self.assertEqual(sr.messages, [])
        self.assertIsNone(sr.next_page_token)

    def test_with_data(self):
        eh = EmailHeader(message_id="1", thread_id="1", subject="A",
                         sender="A", sender_email="a@b.com", snippet="", date=datetime.now())
        sr = SearchResult(messages=[eh], next_page_token="tok", result_estimate=100)
        self.assertEqual(len(sr.messages), 1)
        self.assertEqual(sr.next_page_token, "tok")


class TestDraftList(unittest.TestCase):
    def test_empty(self):
        dl = DraftList()
        self.assertEqual(dl.drafts, [])


if __name__ == "__main__":
    unittest.main()
