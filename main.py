"""Orchestrates the weekly finance/strategy watch newsletter."""
from fetch_emails import fetch_recent_emails
from summarize import generate_newsletter_content
from charts import build_charts
from send_email import send_newsletter


def main():
    print("Fetching emails from the last 7 days...")
    emails = fetch_recent_emails(days=7)
    print(f"{len(emails)} emails found.")

    print("Summarizing with Gemini...")
    content = generate_newsletter_content(emails)

    print("Building charts...")
    chart_images = build_charts(content.get("chart_data", []))

    print("Sending newsletter...")
    send_newsletter(content, chart_images)
    print("Done.")


if __name__ == "__main__":
    main()
