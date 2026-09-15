"""Fetch recent finance/strategy newsletters from Gmail via IMAP."""
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import os
from bs4 import BeautifulSoup

IMAP_SERVER = "imap.gmail.com"


def _decode(value):
    if value is None:
        return ""
    parts = decode_header(value)
    decoded = ""
    for text, enc in parts:
        if isinstance(text, bytes):
            decoded += text.decode(enc or "utf-8", errors="ignore")
        else:
            decoded += text
    return decoded


def _extract_text(msg):
    """Return plain text content of an email.message.Message, stripping HTML if needed."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disp = str(part.get("Content-Disposition") or "")
            if content_type == "text/plain" and "attachment" not in disp:
                try:
                    return part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", errors="ignore"
                    )
                except Exception:
                    continue
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                try:
                    html = part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", errors="ignore"
                    )
                    return BeautifulSoup(html, "html.parser").get_text(separator="\n")
                except Exception:
                    continue
        return ""
    else:
        try:
            payload = msg.get_payload(decode=True).decode(
                msg.get_content_charset() or "utf-8", errors="ignore"
            )
        except Exception:
            return ""
        if msg.get_content_type() == "text/html":
            return BeautifulSoup(payload, "html.parser").get_text(separator="\n")
        return payload


def fetch_recent_emails(days=7, max_chars_per_email=6000):
    """Connect to Gmail via IMAP and return a list of dicts for emails received
    in the last `days` days. Reads credentials from environment variables
    GMAIL_ADDRESS and GMAIL_APP_PASSWORD (never hard-code them)."""
    address = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]

    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    print(f"DEBUG address={address!r} (len={len(address)})") 
    print(f"DEBUG app_password length={len(app_password)}")
    imap.login(address, app_password)
    imap.select("INBOX")

    since_date = (datetime.utcnow() - timedelta(days=days)).strftime("%d-%b-%Y")
    status, data = imap.search(None, f'(SINCE "{since_date}")')

    emails = []
    if status == "OK":
        for num in data[0].split():
            status, msg_data = imap.fetch(num, "(RFC822)")
            if status != "OK":
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            text = _extract_text(msg).strip()
            if not text:
                continue
            emails.append(
                {
                    "sender": _decode(msg.get("From")),
                    "subject": _decode(msg.get("Subject")),
                    "date": msg.get("Date"),
                    "text": text[:max_chars_per_email],
                }
            )

    imap.logout()
    return emails
