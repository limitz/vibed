# Gmail Console Client

**Prompt:**
> `Make a gmail client for the console using the gmail MCP. Make it really user friendly, clean, well designed. Think menus, full rgb, emoji's. Make a few iterations in the design process to get it just right. *Never ever test with the actual mcp*`

![Screenshot](screenshot.png)

## Features

- **Full inbox view** with sender, subject, snippet, date, star, and attachment indicators
- **Message view** with complete email headers, body text, and attachment list
- **Thread/conversation view** showing all messages in a thread chronologically
- **Compose & reply** with To/Cc/Bcc/Subject/Body fields and draft saving
- **Search** using Gmail query syntax (from:, is:unread, has:attachment, etc.)
- **Drafts management** — view, edit, and create drafts
- **Sidebar navigation** with system labels (Inbox, Starred, Sent, etc.) and user labels
- **RGB color theme** — Gmail-inspired dark palette with 30 custom color pairs
- **Emoji throughout** — 📥 📤 📝 ⭐ 🔶 📎 🔍 ✏️ and more
- **Keyboard-driven** — j/k navigation, /, c, r, t, s, Tab, number keys for quick jumps
- **Mock client** for safe development and testing (never touches real Gmail)
- **Real MCP client** ready for production use with Gmail MCP tools

## Architecture

| Module | Purpose |
|---|---|
| `models.py` | Data classes (Profile, Label, EmailHeader, Email, Thread, Draft) |
| `mcp_client.py` | Abstract Gmail MCP interface |
| `mock_client.py` | Mock implementation with 20 realistic emails |
| `real_client.py` | Production MCP client with response parsing |
| `colors.py` | RGB color theme with 30 curses color pairs |
| `components.py` | Reusable UI widgets (sidebar, email list, message view, compose, etc.) |
| `app.py` | Application controller with state machine and key handling |
| `main.py` | Entry point |

## Usage

```bash
python main.py          # Demo mode with mock data (safe, no MCP calls)
python main.py --live   # Live mode (requires MCP runtime)
```

## Keyboard Shortcuts

| Key | Action |
|---|---|
| ↑/↓, j/k | Navigate up/down |
| Enter | Open email |
| Esc, q | Go back / quit |
| Tab | Toggle sidebar focus |
| c | Compose new email |
| / | Search messages |
| r | Reply (create draft) |
| t | View thread |
| s | Toggle star |
| d | View drafts |
| R | Refresh |
| 1-9 | Quick jump to sidebar item |
| ? | Help |

## Tests

```bash
python -m pytest test_models.py test_mock_client.py test_components.py test_app.py -v
```

79 tests covering models, mock client, UI components, and app controller.

## Built with

Claude Opus 4.6 (`claude-opus-4-6`) via [Claude Code](https://claude.com/claude-code)
