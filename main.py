"""Orchestrates the weekly finance/strategy watch newsletter."""
from fetch_emails import fetch_recent_emails
from summarize import generate_newsletter_content
from charts import build_charts
from send_email import send_newsletter
from memory import load_previous_items, save_current_content


def main():
    print("Fetching emails from the last 7 days...")
    emails = fetch_recent_emails(days=7)
    print(f"{len(emails)} emails found.")

    previous_items = load_previous_items()
    print(f"{len(previous_items)} items from last week loaded as history.")

    print("Summarizing with Gemini...")
    content = generate_newsletter_content(emails, previous_items=previous_items)

    print("Building charts...")
    chart_images = build_charts(content.get("chart_data", []))

    print("Sending newsletter...")
    send_newsletter(content, chart_images)

    print("Saving history for next week...")
    save_current_content(content)

    print("Done.")


if __name__ == "__main__":
    main()
