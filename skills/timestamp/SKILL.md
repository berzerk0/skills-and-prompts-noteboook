---
name: timestamp
description: Get current UTC timestamp in YYYY-MM-DD-HHMM format. Use when user requests current time, timestamp, or date/time.
license: MIT
compatibility: [claude, pi, vibe]
allowed-tools: []
---

Return the current UTC time in YYYY-MM-DD-HHMM format (24-hour clock).

Do not add any additional text, explanations, or formatting. Return only the timestamp string.

Implementation: Use `from timestamp_skill import get_utc_timestamp`
