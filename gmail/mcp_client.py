"""Gmail MCP client interface and implementations."""

from abc import ABC, abstractmethod
from typing import Optional

from models import (
    Profile, Label, EmailHeader, Email, Thread, Draft,
    SearchResult, DraftList
)


class GmailMCPClient(ABC):
    """Abstract interface for Gmail MCP operations."""

    @abstractmethod
    async def get_profile(self) -> Profile:
        """Get the authenticated user's Gmail profile."""
        ...

    @abstractmethod
    async def list_labels(self) -> list[Label]:
        """List all Gmail labels."""
        ...

    @abstractmethod
    async def search_messages(
        self,
        query: str = "",
        max_results: int = 20,
        page_token: Optional[str] = None,
        include_spam_trash: bool = False,
    ) -> SearchResult:
        """Search for messages using Gmail query syntax."""
        ...

    @abstractmethod
    async def read_message(self, message_id: str) -> Email:
        """Read a full email message by ID."""
        ...

    @abstractmethod
    async def read_thread(self, thread_id: str) -> Thread:
        """Read an entire email thread."""
        ...

    @abstractmethod
    async def create_draft(
        self,
        body: str,
        to: Optional[str] = None,
        subject: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        content_type: str = "text/plain",
        thread_id: Optional[str] = None,
    ) -> Draft:
        """Create a new email draft."""
        ...

    @abstractmethod
    async def list_drafts(
        self,
        max_results: int = 20,
        page_token: Optional[str] = None,
    ) -> DraftList:
        """List saved drafts."""
        ...
