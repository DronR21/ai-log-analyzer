# AI-Powered Log Analyzer

A CLI tool that scans a log file for errors and warnings, then uses
Google's Gemini API to generate a plain-English triage summary with
likely root causes and suggested next steps.

## Why
Manually scanning logs for the "real" issue among hundreds of lines is
slow. This automates the first pass of triage.

## Usage
\`\`\`
setx GEMINI_API_KEY "your-key-here"
python log_analyzer.py sample.log
\`\`\`

## Tech Stack
Python, Google Gemini API (gemini-3.8-flash)

## Example output
Analyzing sample.log...

Found 4 error/warning line(s).

Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.
============================================================
AI TRIAGE SUMMARY
============================================================
Here is an analysis of the distinct issues identified in the log snippet:

---

### Issue 1: High Response Latency on `/api/orders`
* **Log:** `WARNING Response time exceeded 2000ms for /api/orders`
* **Likely Root Cause:** The endpoint was taking longer than normal to process, likely serving as an early indicator that the database was slowing down, experiencing high load, or holding locks before it failed completely.
* **Next Troubleshooting Step:** Inspect the query execution times and server resource metrics (CPU/memory) on the database around 10:14 to identify slow-running queries triggered by `/api/orders`.

---

### Issue 2: Primary Database Unreachable
* **Logs:**
  * `ERROR Database connection timeout after 30s: could not connect to host db-primary:5432`
  * `ERROR Failed to process request /api/orders - Connection refused`
* **Likely Root Cause:** The database service on `db-primary` became completely unavailable (e.g., the service crashed, the host went down, or a network issue blocked communication on port 5432).
* **Next Troubleshooting Step:** Log into the `db-primary` server or check the database hosting console to see if the PostgreSQL service is running (`systemctl status postgresql`) and inspect the database error logs.

---

### Issue 3: Connection Pool Exhaustion
* **Log:** `ERROR Retry failed: connection pool exhausted (max_connections=20, active=20)`
* **Likely Root Cause:** Because the database stopped responding, existing requests hung while waiting on timeouts, keeping all 20 connections in an "active" state and blocking any new requests from acquiring a connection.
* **Next Troubleshooting Step:** Review the application’s database configuration to ensure connection timeouts and query timeouts are set aggressively enough to prevent hung connections from consuming the entire pool during an outage.
