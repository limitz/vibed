#!/usr/bin/env python3
"""Gmail Console Client — Entry point.

Usage:
    python main.py          # Run with mock data (default, safe)
    python main.py --live   # Run with real Gmail MCP (requires MCP runtime)
"""

import sys


def main():
    # Always default to mock client (safe, no real MCP calls)
    use_mock = "--live" not in sys.argv

    if use_mock:
        from mock_client import MockGmailClient
        client = MockGmailClient()
    else:
        # Real client would require MCP tool injection
        print("Live mode requires MCP runtime integration.")
        print("Use without --live flag for demo mode with mock data.")
        sys.exit(1)

    from app import run_app
    run_app(client)


if __name__ == "__main__":
    main()
