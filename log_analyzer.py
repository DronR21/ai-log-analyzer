import os
import sys
import re
from google import genai

def extract_error_lines(log_path):
    """Pull out ERROR and WARNING lines from a log file."""
    error_lines = []
    with open(log_path, "r") as f:
        for line in f:
            if re.search(r"\b(ERROR|WARNING)\b", line):
                error_lines.append(line.strip())
    return error_lines

def analyze_with_ai(error_lines):
    """Send error lines to Gemini and get back a plain-English triage summary."""
    if not error_lines:
        return "No errors or warnings found in this log file."

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set."

    try:
        client = genai.Client(api_key=api_key)
        log_text = "\n".join(error_lines)
        prompt = f"""You are a support engineer's assistant. Below are ERROR and 
WARNING lines extracted from a server log file. For each distinct issue:
1. Give it a short title
2. Explain the likely root cause in plain English
3. Suggest one concrete next troubleshooting step

Log lines:
{log_text}
"""
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI analysis failed: {e}"
    
def main():
    if len(sys.argv) != 2:
        print("Usage: python log_analyzer.py <path_to_logfile>")
        sys.exit(1)

    log_path = sys.argv[1]
    if not os.path.exists(log_path):
        print(f"Error: file not found: {log_path}")
        sys.exit(1)

    print(f"Analyzing {log_path}...\n")
    error_lines = extract_error_lines(log_path)
    print(f"Found {len(error_lines)} error/warning line(s).\n")

    summary = analyze_with_ai(error_lines)
    print("=" * 60)
    print("AI TRIAGE SUMMARY")
    print("=" * 60)
    print(summary)

if __name__ == "__main__":
    main()