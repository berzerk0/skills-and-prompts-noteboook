"""
UTC Timestamp Skill for AI Agents

Provides the current UTC time in YYYY-MM-DD-HHMM format.
Example: 2024-01-15-1430
"""

from datetime import datetime, timezone


def get_utc_timestamp() -> str:
    """
    Get the current UTC timestamp in YYYY-MM-DD-HHMM format.

    Returns:
        str: Current UTC time as YYYY-MM-DD-HHMM (24-hour format).
    """
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d-%H%M")


if __name__ == "__main__":
    # Example usage
    timestamp = get_utc_timestamp()
    print(f"Current UTC timestamp: {timestamp}")
