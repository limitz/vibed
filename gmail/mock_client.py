"""Mock Gmail MCP client with realistic test data."""

from datetime import datetime, timedelta
from typing import Optional

from models import (
    Profile, Label, EmailHeader, Email, Thread, ThreadMessage, Draft,
    SearchResult, DraftList,
)
from mcp_client import GmailMCPClient


def _ago(days: int = 0, hours: int = 0, minutes: int = 0) -> datetime:
    return datetime.now() - timedelta(days=days, hours=hours, minutes=minutes)


# ── Realistic sample data ──────────────────────────────────────────

MOCK_PROFILE = Profile(
    email="alex.johnson@gmail.com",
    messages_total=12847,
    threads_total=4293,
    history_id="987654",
)

MOCK_LABELS: list[Label] = [
    Label(id="INBOX", name="INBOX", label_type="system", message_count=128, unread_count=14),
    Label(id="SENT", name="SENT", label_type="system", message_count=856),
    Label(id="DRAFT", name="DRAFT", label_type="system", message_count=3),
    Label(id="STARRED", name="STARRED", label_type="system", message_count=23),
    Label(id="IMPORTANT", name="IMPORTANT", label_type="system", message_count=67),
    Label(id="SPAM", name="SPAM", label_type="system", message_count=12),
    Label(id="TRASH", name="TRASH", label_type="system", message_count=45),
    Label(id="CATEGORY_PROMOTIONS", name="CATEGORY_PROMOTIONS", label_type="system", message_count=234),
    Label(id="CATEGORY_SOCIAL", name="CATEGORY_SOCIAL", label_type="system", message_count=89),
    Label(id="Label_1", name="Work", label_type="user", message_count=342, unread_count=5),
    Label(id="Label_2", name="Personal", label_type="user", message_count=156),
    Label(id="Label_3", name="Projects/Alpha", label_type="user", message_count=28, unread_count=2),
    Label(id="Label_4", name="Projects/Beta", label_type="user", message_count=15),
    Label(id="Label_5", name="Receipts", label_type="user", message_count=89),
    Label(id="Label_6", name="Travel", label_type="user", message_count=34),
]

MOCK_EMAILS: list[EmailHeader] = [
    EmailHeader(
        message_id="msg_001", thread_id="thread_001",
        subject="🚀 Q1 Product Launch — Final Review Needed",
        sender="Sarah Chen", sender_email="sarah.chen@company.com",
        snippet="Hi team, I've attached the final deck for the Q1 launch. Please review slides 12-18 for the pricing section...",
        date=_ago(minutes=12), is_unread=True, has_attachment=True,
        labels=["INBOX", "IMPORTANT", "Label_1"],
    ),
    EmailHeader(
        message_id="msg_002", thread_id="thread_002",
        subject="Re: Dinner plans for Saturday?",
        sender="Mom", sender_email="linda.johnson@gmail.com",
        snippet="That sounds wonderful! I'll make your favorite lasagna. Dad says he'll pick up dessert from that bakery you like...",
        date=_ago(minutes=45), is_unread=True,
        labels=["INBOX", "Label_2"],
    ),
    EmailHeader(
        message_id="msg_003", thread_id="thread_003",
        subject="Your AWS bill for March 2026",
        sender="Amazon Web Services", sender_email="billing@aws.amazon.com",
        snippet="Your total charges for this billing period are $847.23. View your detailed bill in the AWS Billing Console...",
        date=_ago(hours=2), is_unread=True, has_attachment=True,
        labels=["INBOX", "Label_5"],
    ),
    EmailHeader(
        message_id="msg_004", thread_id="thread_004",
        subject="Sprint 24 Retrospective Notes",
        sender="Marcus Wright", sender_email="marcus.w@company.com",
        snippet="Here are the action items from today's retro: 1. Improve CI pipeline speed 2. Add more integration tests...",
        date=_ago(hours=3), is_unread=False, is_starred=True,
        labels=["INBOX", "Label_1", "Label_3"],
    ),
    EmailHeader(
        message_id="msg_005", thread_id="thread_005",
        subject="Re: Code review: auth-service refactor",
        sender="Priya Patel", sender_email="priya.p@company.com",
        snippet="LGTM! Just one minor comment on the token refresh logic — see inline. The rest looks solid, nice work on...",
        date=_ago(hours=5), is_unread=True,
        labels=["INBOX", "Label_1", "Label_3"],
    ),
    EmailHeader(
        message_id="msg_006", thread_id="thread_006",
        subject="Your flight to Tokyo is confirmed ✈️",
        sender="Delta Air Lines", sender_email="noreply@delta.com",
        snippet="Confirmation #DL7829K — SFO → NRT on April 15, 2026. Departure 11:45 AM. Check in opens 24 hours before...",
        date=_ago(hours=8), is_unread=False, is_starred=True,
        labels=["INBOX", "Label_6"],
    ),
    EmailHeader(
        message_id="msg_007", thread_id="thread_007",
        subject="New comment on your PR #483",
        sender="GitHub", sender_email="notifications@github.com",
        snippet="@devops-bot commented on your pull request: 'All checks passed. Coverage is at 94.2%, up from 93.8%...'",
        date=_ago(hours=10), is_unread=True,
        labels=["INBOX", "Label_1"],
    ),
    EmailHeader(
        message_id="msg_008", thread_id="thread_008",
        subject="Weekend hiking trip — who's in? 🥾",
        sender="Jake Torres", sender_email="jake.torres@gmail.com",
        snippet="Hey everyone! Thinking of doing Mt. Tam this Saturday, leaving around 7am. Trail is about 8 miles round trip...",
        date=_ago(days=1, hours=2), is_unread=False,
        labels=["INBOX", "Label_2"],
    ),
    EmailHeader(
        message_id="msg_009", thread_id="thread_009",
        subject="Invoice #INV-2026-0342",
        sender="Stripe", sender_email="receipts@stripe.com",
        snippet="Payment of $299.00 received for your monthly subscription. Thank you for your business...",
        date=_ago(days=1, hours=6), is_unread=False, has_attachment=True,
        labels=["INBOX", "Label_5"],
    ),
    EmailHeader(
        message_id="msg_010", thread_id="thread_010",
        subject="Re: Team offsite agenda — April 2026",
        sender="Rachel Kim", sender_email="rachel.kim@company.com",
        snippet="I've updated the shared doc with everyone's suggestions. Looks like the consensus is: Day 1 = strategy, Day 2...",
        date=_ago(days=1, hours=14), is_unread=False,
        labels=["INBOX", "Label_1"],
    ),
    EmailHeader(
        message_id="msg_011", thread_id="thread_011",
        subject="Spotify: Your 2026 listening so far",
        sender="Spotify", sender_email="noreply@spotify.com",
        snippet="You've listened to 2,847 minutes of music so far in 2026! Your top genre is Lo-Fi Hip Hop and your most...",
        date=_ago(days=2), is_unread=False,
        labels=["INBOX", "CATEGORY_PROMOTIONS"],
    ),
    EmailHeader(
        message_id="msg_012", thread_id="thread_012",
        subject="Security alert: New sign-in from Chrome on Mac",
        sender="Google", sender_email="no-reply@accounts.google.com",
        snippet="We noticed a new sign-in to your Google Account on a Mac device. If this was you, you can ignore this...",
        date=_ago(days=2, hours=5), is_unread=True, is_starred=False,
        labels=["INBOX", "IMPORTANT"],
    ),
    EmailHeader(
        message_id="msg_013", thread_id="thread_013",
        subject="[Action Required] Annual compliance training",
        sender="HR Team", sender_email="hr@company.com",
        snippet="Please complete your annual compliance training by March 31, 2026. Click the link below to access the...",
        date=_ago(days=3), is_unread=True,
        labels=["INBOX", "Label_1"],
    ),
    EmailHeader(
        message_id="msg_014", thread_id="thread_014",
        subject="Your Uber Eats order is on the way!",
        sender="Uber Eats", sender_email="noreply@uber.com",
        snippet="Your order from Sushi Palace is being prepared. Estimated delivery: 35-45 minutes. Track your order...",
        date=_ago(days=3, hours=8), is_unread=False,
        labels=["INBOX", "Label_5"],
    ),
    EmailHeader(
        message_id="msg_015", thread_id="thread_015",
        subject="Re: Book club: Next month's pick?",
        sender="Emma Liu", sender_email="emma.liu@gmail.com",
        snippet="I vote for 'Project Hail Mary'! It's perfect for our sci-fi month. Who hasn't read it yet? Also, my place...",
        date=_ago(days=4), is_unread=False,
        labels=["INBOX", "Label_2"],
    ),
    EmailHeader(
        message_id="msg_016", thread_id="thread_016",
        subject="Alpha project: v2.0 architecture proposal",
        sender="David Park", sender_email="david.park@company.com",
        snippet="I've put together a proposal for the v2.0 architecture. Key changes: microservices migration, event-driven...",
        date=_ago(days=4, hours=12), is_unread=True, has_attachment=True,
        labels=["INBOX", "Label_1", "Label_3"],
    ),
    EmailHeader(
        message_id="msg_017", thread_id="thread_017",
        subject="LinkedIn: 5 people viewed your profile",
        sender="LinkedIn", sender_email="notifications@linkedin.com",
        snippet="Your profile was viewed by: Senior Recruiter at Google, Engineering Manager at Meta, CTO at...",
        date=_ago(days=5), is_unread=False,
        labels=["INBOX", "CATEGORY_SOCIAL"],
    ),
    EmailHeader(
        message_id="msg_018", thread_id="thread_018",
        subject="Re: Apartment lease renewal",
        sender="Bay Property Mgmt", sender_email="leasing@bayproperty.com",
        snippet="Thank you for confirming your renewal. Your new lease term begins April 1, 2026. Monthly rent: $2,850...",
        date=_ago(days=5, hours=3), is_unread=False, has_attachment=True,
        labels=["INBOX", "Label_2"],
    ),
    EmailHeader(
        message_id="msg_019", thread_id="thread_019",
        subject="Deployed: auth-service v3.4.1 to production",
        sender="CI/CD Bot", sender_email="cicd@company.com",
        snippet="Deployment successful. Commit: a3f8c2d. Changes: token refresh fix, rate limiter update. All health checks...",
        date=_ago(days=6), is_unread=False,
        labels=["INBOX", "Label_1"],
    ),
    EmailHeader(
        message_id="msg_020", thread_id="thread_020",
        subject="Your NYT Cooking recipe collection",
        sender="NYT Cooking", sender_email="nytcooking@nytimes.com",
        snippet="This week's top saved recipe: Crispy Miso Salmon. Plus: 15-minute weeknight dinners your whole family...",
        date=_ago(days=7), is_unread=False,
        labels=["INBOX", "CATEGORY_PROMOTIONS"],
    ),
]

MOCK_FULL_EMAILS: dict[str, Email] = {
    "msg_001": Email(
        message_id="msg_001", thread_id="thread_001",
        subject="🚀 Q1 Product Launch — Final Review Needed",
        sender="Sarah Chen", sender_email="sarah.chen@company.com",
        to="team-leads@company.com",
        cc="alex.johnson@gmail.com, product@company.com",
        date=_ago(minutes=12),
        body_text="""Hi team,

I've attached the final deck for the Q1 launch. Please review slides 12-18 for the pricing section — we need sign-off by EOD Thursday.

Key changes since last version:
• Updated pricing tiers based on competitive analysis
• Added enterprise plan details (slide 15)
• Revised go-to-market timeline (slide 18)

The marketing team has already approved the messaging. We just need engineering and product leads to confirm the feature list is accurate.

Let me know if you have questions!

Best,
Sarah""",
        is_unread=True, has_attachment=True,
        labels=["INBOX", "IMPORTANT", "Label_1"],
        attachments=["Q1_Launch_Deck_v3.pptx", "Pricing_Analysis.xlsx"],
    ),
    "msg_002": Email(
        message_id="msg_002", thread_id="thread_002",
        subject="Re: Dinner plans for Saturday?",
        sender="Mom", sender_email="linda.johnson@gmail.com",
        to="alex.johnson@gmail.com",
        date=_ago(minutes=45),
        body_text="""That sounds wonderful! I'll make your favorite lasagna. Dad says he'll pick up dessert from that bakery you like on Main Street.

Can you bring a bottle of wine? Red, preferably.

Also, your sister might join — she's flying in from Portland on Friday night.

Love,
Mom

P.S. Don't forget to bring your laundry if you need to! 😄""",
        is_unread=True,
        labels=["INBOX", "Label_2"],
    ),
    "msg_005": Email(
        message_id="msg_005", thread_id="thread_005",
        subject="Re: Code review: auth-service refactor",
        sender="Priya Patel", sender_email="priya.p@company.com",
        to="alex.johnson@gmail.com",
        date=_ago(hours=5),
        body_text="""LGTM! Just one minor comment on the token refresh logic — see inline.

The rest looks solid, nice work on cleaning up the middleware chain. The new error handling is much cleaner.

One thought: should we add a rate limiter to the refresh endpoint? We've seen some abuse patterns in the logs.

I'll approve once the inline comment is addressed.

—Priya""",
        is_unread=True,
        labels=["INBOX", "Label_1", "Label_3"],
    ),
}

MOCK_THREADS: dict[str, Thread] = {
    "thread_002": Thread(
        thread_id="thread_002",
        subject="Dinner plans for Saturday?",
        messages=[
            ThreadMessage(
                message_id="msg_002a",
                sender="Alex Johnson", sender_email="alex.johnson@gmail.com",
                date=_ago(hours=3),
                body_text="Hey Mom! Want to do dinner Saturday? I was thinking I could come over around 6. Miss your cooking!",
                snippet="Hey Mom! Want to do dinner Saturday?",
            ),
            ThreadMessage(
                message_id="msg_002",
                sender="Mom", sender_email="linda.johnson@gmail.com",
                date=_ago(minutes=45),
                body_text="That sounds wonderful! I'll make your favorite lasagna. Dad says he'll pick up dessert from that bakery you like on Main Street.\n\nCan you bring a bottle of wine? Red, preferably.\n\nAlso, your sister might join — she's flying in from Portland on Friday night.\n\nLove,\nMom\n\nP.S. Don't forget to bring your laundry if you need to! 😄",
                snippet="That sounds wonderful! I'll make your favorite lasagna.",
            ),
        ],
    ),
    "thread_005": Thread(
        thread_id="thread_005",
        subject="Code review: auth-service refactor",
        messages=[
            ThreadMessage(
                message_id="msg_005a",
                sender="Alex Johnson", sender_email="alex.johnson@gmail.com",
                date=_ago(days=1),
                body_text="Hi team, I've opened PR #483 for the auth-service refactor. Key changes:\n\n- Simplified middleware chain\n- Better error handling for token refresh\n- Added retry logic for transient failures\n\nPlease take a look when you get a chance.",
                snippet="Hi team, I've opened PR #483 for the auth-service refactor.",
            ),
            ThreadMessage(
                message_id="msg_005b",
                sender="Marcus Wright", sender_email="marcus.w@company.com",
                date=_ago(hours=8),
                body_text="Looks good overall! Left a few comments on the retry logic. Also, did you consider using exponential backoff instead of fixed intervals?",
                snippet="Looks good overall! Left a few comments on the retry logic.",
            ),
            ThreadMessage(
                message_id="msg_005",
                sender="Priya Patel", sender_email="priya.p@company.com",
                date=_ago(hours=5),
                body_text="LGTM! Just one minor comment on the token refresh logic — see inline.\n\nThe rest looks solid, nice work on cleaning up the middleware chain. The new error handling is much cleaner.\n\nOne thought: should we add a rate limiter to the refresh endpoint? We've seen some abuse patterns in the logs.\n\nI'll approve once the inline comment is addressed.\n\n—Priya",
                snippet="LGTM! Just one minor comment on the token refresh logic.",
            ),
        ],
    ),
}

MOCK_DRAFTS: list[Draft] = [
    Draft(
        draft_id="draft_001", message_id="dmsg_001",
        subject="Re: Q1 Product Launch — Final Review Needed",
        to="sarah.chen@company.com",
        body="Hi Sarah, I've reviewed the deck. A few notes on the pricing section:\n\n1. ",
        thread_id="thread_001",
    ),
    Draft(
        draft_id="draft_002", message_id="dmsg_002",
        subject="Vacation request: April 14-22",
        to="hr@company.com",
        cc="manager@company.com",
        body="Hi HR team,\n\nI'd like to request PTO for April 14-22 for a trip to Japan.\n\nPlease let me know if you need any additional information.\n\nBest,\nAlex",
    ),
    Draft(
        draft_id="draft_003", message_id="dmsg_003",
        subject="",
        to="",
        body="",
    ),
]


class MockGmailClient(GmailMCPClient):
    """Mock implementation for testing — never touches real Gmail."""

    async def get_profile(self) -> Profile:
        return MOCK_PROFILE

    async def list_labels(self) -> list[Label]:
        return list(MOCK_LABELS)

    async def search_messages(
        self,
        query: str = "",
        max_results: int = 20,
        page_token: Optional[str] = None,
        include_spam_trash: bool = False,
    ) -> SearchResult:
        emails = list(MOCK_EMAILS)

        if query:
            q = query.lower()
            filtered = []
            for e in emails:
                # Simple query matching
                if q.startswith("is:unread"):
                    if e.is_unread:
                        filtered.append(e)
                elif q.startswith("is:starred"):
                    if e.is_starred:
                        filtered.append(e)
                elif q.startswith("has:attachment"):
                    if e.has_attachment:
                        filtered.append(e)
                elif q.startswith("label:"):
                    label = q.split(":", 1)[1].strip()
                    if any(label.lower() in l.lower() for l in e.labels):
                        filtered.append(e)
                elif q.startswith("from:"):
                    sender = q.split(":", 1)[1].strip()
                    if sender in e.sender_email.lower() or sender in e.sender.lower():
                        filtered.append(e)
                else:
                    # Full text search
                    text = f"{e.subject} {e.sender} {e.snippet}".lower()
                    if q in text:
                        filtered.append(e)
            emails = filtered

        # Pagination
        start = 0
        if page_token:
            start = int(page_token)
        end = start + max_results
        page = emails[start:end]
        next_token = str(end) if end < len(emails) else None

        return SearchResult(
            messages=page,
            next_page_token=next_token,
            result_estimate=len(emails),
        )

    async def read_message(self, message_id: str) -> Email:
        if message_id in MOCK_FULL_EMAILS:
            return MOCK_FULL_EMAILS[message_id]
        # Generate a basic email from header data
        for header in MOCK_EMAILS:
            if header.message_id == message_id:
                return Email(
                    message_id=header.message_id,
                    thread_id=header.thread_id,
                    subject=header.subject,
                    sender=header.sender,
                    sender_email=header.sender_email,
                    to="alex.johnson@gmail.com",
                    date=header.date,
                    body_text=header.snippet + "\n\n[Full message content would appear here]",
                    is_unread=header.is_unread,
                    is_starred=header.is_starred,
                    has_attachment=header.has_attachment,
                    labels=header.labels,
                )
        raise ValueError(f"Message {message_id} not found")

    async def read_thread(self, thread_id: str) -> Thread:
        if thread_id in MOCK_THREADS:
            return MOCK_THREADS[thread_id]
        # Generate a single-message thread
        for header in MOCK_EMAILS:
            if header.thread_id == thread_id:
                return Thread(
                    thread_id=thread_id,
                    subject=header.subject,
                    messages=[
                        ThreadMessage(
                            message_id=header.message_id,
                            sender=header.sender,
                            sender_email=header.sender_email,
                            date=header.date,
                            body_text=header.snippet,
                            snippet=header.snippet,
                        )
                    ],
                )
        raise ValueError(f"Thread {thread_id} not found")

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
        draft_id = f"draft_{len(MOCK_DRAFTS) + 1:03d}"
        msg_id = f"dmsg_{len(MOCK_DRAFTS) + 1:03d}"
        draft = Draft(
            draft_id=draft_id,
            message_id=msg_id,
            subject=subject or "",
            to=to or "",
            cc=cc or "",
            bcc=bcc or "",
            body=body,
            thread_id=thread_id or "",
        )
        return draft

    async def list_drafts(
        self,
        max_results: int = 20,
        page_token: Optional[str] = None,
    ) -> DraftList:
        return DraftList(drafts=list(MOCK_DRAFTS))
