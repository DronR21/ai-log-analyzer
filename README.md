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
(paste a real example of the tool's output here — the DB timeout one you just saw is a great example)