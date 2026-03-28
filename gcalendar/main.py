#!/usr/bin/env python3
"""Entry point for Google Calendar console client."""

import argparse
import sys
import os

# Allow imports from this directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mock_client import MockCalendarClient
from app import run_app


def main() -> None:
    parser = argparse.ArgumentParser(description="Google Calendar Console Client")
    parser.add_argument("--live", action="store_true",
                        help="Use real Google Calendar MCP (not implemented yet)")
    args = parser.parse_args()

    if args.live:
        print("Live mode is not yet implemented. Using mock client.")

    client = MockCalendarClient()
    run_app(client)


if __name__ == "__main__":
    main()
