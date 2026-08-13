"""
Optional email notifications, sent over plain smtplib (no extra
dependency). Fully opt-in: notify_new_message() is a no-op unless
SMTP_HOST and NOTIFY_EMAIL are both configured, so local dev needs no
mail setup at all.
"""

import smtplib
from email.message import EmailMessage

from flask import current_app


def _mail_configured():
    cfg = current_app.config
    return bool(cfg.get("SMTP_HOST") and cfg.get("NOTIFY_EMAIL"))


def notify_new_message(message):
    """
    Best-effort email alert to the site owner when a new contact
    message comes in. Any failure is logged and swallowed — a broken
    mail server must never block the contact form from working.
    """

    if not _mail_configured():
        return

    cfg = current_app.config

    email = EmailMessage()
    email["Subject"] = f"New portfolio message: {message.subject}"
    email["From"] = cfg.get("SMTP_FROM") or cfg["SMTP_USERNAME"]
    email["To"] = cfg["NOTIFY_EMAIL"]
    email.set_content(
        f"From: {message.name} <{message.email}>\n"
        f"Subject: {message.subject}\n\n"
        f"{message.message}"
    )

    try:
        with smtplib.SMTP(cfg["SMTP_HOST"], cfg.get("SMTP_PORT", 587), timeout=10) as smtp:
            smtp.starttls()
            if cfg.get("SMTP_USERNAME"):
                smtp.login(cfg["SMTP_USERNAME"], cfg.get("SMTP_PASSWORD", ""))
            smtp.send_message(email)
    except Exception:
        current_app.logger.exception("Failed to send new-message notification email")
