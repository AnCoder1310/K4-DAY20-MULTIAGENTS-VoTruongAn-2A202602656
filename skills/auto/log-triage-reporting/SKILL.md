---
name: log-triage-reporting
description: Use when parsing server logs to extract errors and generate structured JSON triage reports.
---
# Log Triage Reporting Checklist

1. Populate top-level metadata in the triage JSON with `"schema_version": 2` and `"generated_by": "log-triage"`.
2. Normalize all extracted service names to lower-case with hyphens replaced by underscores (e.g., convert `payment-service` to `payment_service`).
3. Standardize all log entry timestamps to UTC in `YYYY-MM-DDTHH:MM:SSZ` format.
4. Handle repeated log indicators (e.g., `-- last message repeated N times --`) by incrementing the `repeat_count` of the preceding error entry.
5. Sort the output `errors` list primarily by `service` ascending, and secondarily by `timestamp_utc` ascending.