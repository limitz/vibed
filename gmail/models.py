"""Data models for the Gmail console client."""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Profile:
    """Gmail user profile."""
    email: str
    messages_total: int = 0
    threads_total: int = 0
    history_id: str = ""


@dataclass
class Label:
    """Gmail label."""
    id: str
    name: str
    label_type: str = "user"  # "system" or "user"
    message_count: int = 0
    unread_count: int = 0


@dataclass
class EmailHeader:
    """Summary of an email for list display."""
    message_id: str
    thread_id: str
    subject: str
    sender: str
    sender_email: str
    snippet: str
    date: datetime
    is_unread: bool = False
    is_starred: bool = False
    has_attachment: bool = False
    labels: list[str] = field(default_factory=list)


@dataclass
class Email:
    """Full email message."""
    message_id: str
    thread_id: str
    subject: str
    sender: str
    sender_email: str
    to: str
    cc: str = ""
    bcc: str = ""
    date: datetime = field(default_factory=datetime.now)
    body_text: str = ""
    body_html: str = ""
    is_unread: bool = False
    is_starred: bool = False
    has_attachment: bool = False
    labels: list[str] = field(default_factory=list)
    attachments: list[str] = field(default_factory=list)


@dataclass
class ThreadMessage:
    """A message within a thread."""
    message_id: str
    sender: str
    sender_email: str
    date: datetime
    body_text: str = ""
    snippet: str = ""


@dataclass
class Thread:
    """Email thread/conversation."""
    thread_id: str
    subject: str
    messages: list[ThreadMessage] = field(default_factory=list)


@dataclass
class Draft:
    """Email draft."""
    draft_id: str
    message_id: str
    subject: str = ""
    to: str = ""
    cc: str = ""
    bcc: str = ""
    body: str = ""
    thread_id: str = ""


@dataclass
class SearchResult:
    """Paginated search results."""
    messages: list[EmailHeader] = field(default_factory=list)
    next_page_token: Optional[str] = None
    result_estimate: int = 0


@dataclass
class DraftList:
    """Paginated draft list."""
    drafts: list[Draft] = field(default_factory=list)
    next_page_token: Optional[str] = None
