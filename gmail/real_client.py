"""Real Gmail MCP client that calls actual MCP tools.

This module is used in production. It translates MCP tool responses
into our data models. The MCP tools are injected as callables so this
module has no hard dependency on the MCP runtime.
"""

from datetime import datetime
from typing import Any, Callable, Awaitable, Optional

from models import (
    Profile, Label, EmailHeader, Email, Thread, ThreadMessage, Draft,
    SearchResult, DraftList,
)
from mcp_client import GmailMCPClient


# Type alias for an MCP tool callable
MCPTool = Callable[..., Awaitable[Any]]


def _parse_date(date_str: str) -> datetime:
    """Best-effort date parsing from email headers."""
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%d %b %Y %H:%M:%S %z",
    ):
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue
    return datetime.now()


def _get_header(headers: list[dict], name: str) -> str:
    """Extract a header value by name from a list of header dicts."""
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def _parse_sender(from_str: str) -> tuple[str, str]:
    """Parse 'Name <email>' into (name, email)."""
    if "<" in from_str and ">" in from_str:
        name = from_str[:from_str.index("<")].strip().strip('"')
        email = from_str[from_str.index("<") + 1:from_str.index(">")]
        return name or email, email
    return from_str, from_str


class RealGmailClient(GmailMCPClient):
    """Production client that delegates to Gmail MCP tools."""

    def __init__(
        self,
        get_profile_tool: MCPTool,
        list_labels_tool: MCPTool,
        search_messages_tool: MCPTool,
        read_message_tool: MCPTool,
        read_thread_tool: MCPTool,
        create_draft_tool: MCPTool,
        list_drafts_tool: MCPTool,
    ):
        self._get_profile = get_profile_tool
        self._list_labels = list_labels_tool
        self._search_messages = search_messages_tool
        self._read_message = read_message_tool
        self._read_thread = read_thread_tool
        self._create_draft = create_draft_tool
        self._list_drafts = list_drafts_tool

    async def get_profile(self) -> Profile:
        data = await self._get_profile()
        return Profile(
            email=data.get("emailAddress", ""),
            messages_total=data.get("messagesTotal", 0),
            threads_total=data.get("threadsTotal", 0),
            history_id=str(data.get("historyId", "")),
        )

    async def list_labels(self) -> list[Label]:
        data = await self._list_labels()
        labels_data = data.get("labels", [])
        return [
            Label(
                id=l.get("id", ""),
                name=l.get("name", ""),
                label_type=l.get("type", "user"),
                message_count=l.get("messagesTotal", 0),
                unread_count=l.get("messagesUnread", 0),
            )
            for l in labels_data
        ]

    async def search_messages(
        self,
        query: str = "",
        max_results: int = 20,
        page_token: Optional[str] = None,
        include_spam_trash: bool = False,
    ) -> SearchResult:
        kwargs: dict[str, Any] = {"maxResults": max_results}
        if query:
            kwargs["q"] = query
        if page_token:
            kwargs["pageToken"] = page_token
        if include_spam_trash:
            kwargs["includeSpamTrash"] = True

        data = await self._search_messages(**kwargs)
        messages_data = data.get("messages", [])
        headers_list: list[EmailHeader] = []

        for msg in messages_data:
            hdrs = msg.get("payload", {}).get("headers", [])
            sender_raw = _get_header(hdrs, "From")
            sender_name, sender_email = _parse_sender(sender_raw)
            label_ids = msg.get("labelIds", [])

            headers_list.append(EmailHeader(
                message_id=msg.get("id", ""),
                thread_id=msg.get("threadId", ""),
                subject=_get_header(hdrs, "Subject"),
                sender=sender_name,
                sender_email=sender_email,
                snippet=msg.get("snippet", ""),
                date=_parse_date(_get_header(hdrs, "Date")),
                is_unread="UNREAD" in label_ids,
                is_starred="STARRED" in label_ids,
                has_attachment=any(
                    p.get("filename") for p in msg.get("payload", {}).get("parts", [])
                ),
                labels=label_ids,
            ))

        return SearchResult(
            messages=headers_list,
            next_page_token=data.get("nextPageToken"),
            result_estimate=data.get("resultSizeEstimate", len(headers_list)),
        )

    async def read_message(self, message_id: str) -> Email:
        data = await self._read_message(messageId=message_id)
        hdrs = data.get("payload", {}).get("headers", [])
        sender_raw = _get_header(hdrs, "From")
        sender_name, sender_email = _parse_sender(sender_raw)
        label_ids = data.get("labelIds", [])

        # Extract body
        body_text = ""
        body_html = ""
        attachments = []
        payload = data.get("payload", {})

        def _extract_parts(part: dict) -> None:
            nonlocal body_text, body_html
            mime = part.get("mimeType", "")
            if mime == "text/plain" and not body_text:
                body_data = part.get("body", {}).get("data", "")
                if body_data:
                    import base64
                    body_text = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="replace")
            elif mime == "text/html" and not body_html:
                body_data = part.get("body", {}).get("data", "")
                if body_data:
                    import base64
                    body_html = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="replace")
            if part.get("filename"):
                attachments.append(part["filename"])
            for sub in part.get("parts", []):
                _extract_parts(sub)

        _extract_parts(payload)

        return Email(
            message_id=data.get("id", ""),
            thread_id=data.get("threadId", ""),
            subject=_get_header(hdrs, "Subject"),
            sender=sender_name,
            sender_email=sender_email,
            to=_get_header(hdrs, "To"),
            cc=_get_header(hdrs, "Cc"),
            bcc=_get_header(hdrs, "Bcc"),
            date=_parse_date(_get_header(hdrs, "Date")),
            body_text=body_text,
            body_html=body_html,
            is_unread="UNREAD" in label_ids,
            is_starred="STARRED" in label_ids,
            has_attachment=bool(attachments),
            labels=label_ids,
            attachments=attachments,
        )

    async def read_thread(self, thread_id: str) -> Thread:
        data = await self._read_thread(threadId=thread_id)
        messages_data = data.get("messages", [])
        subject = ""
        thread_msgs: list[ThreadMessage] = []

        for msg in messages_data:
            hdrs = msg.get("payload", {}).get("headers", [])
            sender_raw = _get_header(hdrs, "From")
            sender_name, sender_email = _parse_sender(sender_raw)
            if not subject:
                subject = _get_header(hdrs, "Subject")

            body_text = ""
            def _extract_text(part: dict) -> None:
                nonlocal body_text
                if part.get("mimeType") == "text/plain" and not body_text:
                    body_data = part.get("body", {}).get("data", "")
                    if body_data:
                        import base64
                        body_text = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="replace")
                for sub in part.get("parts", []):
                    _extract_text(sub)

            _extract_text(msg.get("payload", {}))

            thread_msgs.append(ThreadMessage(
                message_id=msg.get("id", ""),
                sender=sender_name,
                sender_email=sender_email,
                date=_parse_date(_get_header(hdrs, "Date")),
                body_text=body_text,
                snippet=msg.get("snippet", ""),
            ))

        return Thread(thread_id=thread_id, subject=subject, messages=thread_msgs)

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
        kwargs: dict[str, Any] = {"body": body}
        if to:
            kwargs["to"] = to
        if subject:
            kwargs["subject"] = subject
        if cc:
            kwargs["cc"] = cc
        if bcc:
            kwargs["bcc"] = bcc
        if content_type != "text/plain":
            kwargs["contentType"] = content_type
        if thread_id:
            kwargs["threadId"] = thread_id

        data = await self._create_draft(**kwargs)
        return Draft(
            draft_id=data.get("draftId", data.get("id", "")),
            message_id=data.get("messageId", ""),
            subject=subject or "",
            to=to or "",
            cc=cc or "",
            bcc=bcc or "",
            body=body,
            thread_id=thread_id or "",
        )

    async def list_drafts(
        self,
        max_results: int = 20,
        page_token: Optional[str] = None,
    ) -> DraftList:
        kwargs: dict[str, Any] = {"maxResults": max_results}
        if page_token:
            kwargs["pageToken"] = page_token

        data = await self._list_drafts(**kwargs)
        drafts_data = data.get("drafts", [])
        return DraftList(
            drafts=[
                Draft(
                    draft_id=d.get("id", ""),
                    message_id=d.get("message", {}).get("id", ""),
                    subject=d.get("subject", ""),
                    to=d.get("to", ""),
                    body=d.get("body", ""),
                )
                for d in drafts_data
            ],
            next_page_token=data.get("nextPageToken"),
        )
