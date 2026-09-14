"""Compose and send the HTML newsletter via Gmail SMTP."""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import date

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


def _build_html(content, chart_images):
    html = [
        f"<h1>Veille finance &amp; stratégie — semaine du {date.today().strftime('%d/%m/%Y')}</h1>"
    ]

    for section in content.get("sections", []):
        html.append(f"<h2>{section['theme']}</h2><ul>")
        for item in section.get("items", []):
            source = f" <i>(source : {item['source']})</i>" if item.get("source") else ""
            html.append(f"<li>{item['text']}{source}</li>")
        html.append("</ul>")

    if content.get("entrepreneurship_ideas"):
        html.append("<h2>Idées d'entrepreneuriat</h2><ul>")
        html += [f"<li>{idea}</li>" for idea in content["entrepreneurship_ideas"]]
        html.append("</ul>")

    if content.get("sectors_to_watch"):
        html.append("<h2>Secteurs à surveiller</h2><ul>")
        html += [f"<li>{s}</li>" for s in content["sectors_to_watch"]]
        html.append("</ul>")

    for img in chart_images:
        html.append(
            f"<h3>{img['title']}</h3><img src='cid:{img['cid']}' style='max-width:600px;'>"
        )

    return "\n".join(html)


def send_newsletter(content, chart_images):
    address = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("related")
    msg["Subject"] = f"Veille finance & stratégie — {date.today().strftime('%d/%m/%Y')}"
    msg["From"] = address
    msg["To"] = address

    msg.attach(MIMEText(_build_html(content, chart_images), "html", "utf-8"))

    for img in chart_images:
        with open(img["path"], "rb") as f:
            mime_img = MIMEImage(f.read())
            mime_img.add_header("Content-ID", f"<{img['cid']}>")
            msg.attach(mime_img)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(address, app_password)
        server.sendmail(address, address, msg.as_string())
