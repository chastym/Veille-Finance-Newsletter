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
    h1_style = "font-family:Arial,sans-serif;font-size:16pt;font-weight:bold;"
    h2_style = "font-family:Arial,sans-serif;font-size:14pt;font-weight:bold;margin-top:24px;"
    li_style = "font-family:Arial,sans-serif;font-size:10pt;line-height:1.5;margin-bottom:6px;"
    ul_style = "margin:4px 0 12px 0;padding-left:20px;"
    source_style = "color:#555555;"

    html = [
        f"<h1 style='{h1_style}'>Veille finance &amp; stratégie — semaine du "
        f"{date.today().strftime('%d/%m/%Y')}</h1>"
    ]

    for section in content.get("sections", []):
        html.append(f"<h2 style='{h2_style}'>{section['theme']}</h2><ul style='{ul_style}'>")
        for item in section.get("items", []):
            source = (
                f" <i style='{source_style}'>(source : {item['source']})</i>"
                if item.get("source")
                else ""
            )
            html.append(f"<li style='{li_style}'>{item['text']}{source}</li>")
        html.append("</ul>")

    if content.get("entrepreneurship_ideas"):
        html.append(f"<h2 style='{h2_style}'>Idées d'entrepreneuriat</h2><ul style='{ul_style}'>")
        html += [f"<li style='{li_style}'>{idea}</li>" for idea in content["entrepreneurship_ideas"]]
        html.append("</ul>")

    if content.get("sectors_to_watch"):
        html.append(f"<h2 style='{h2_style}'>Secteurs à surveiller</h2><ul style='{ul_style}'>")
        html += [f"<li style='{li_style}'>{s}</li>" for s in content["sectors_to_watch"]]
        html.append("</ul>")

    for img in chart_images:
        html.append(
            f"<h3 style='font-family:Arial,sans-serif;font-size:12pt;font-weight:bold;'>"
            f"{img['title']}</h3><img src='cid:{img['cid']}' style='max-width:600px;'>"
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
