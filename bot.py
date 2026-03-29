import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os
import sys

print("🚀 Starting check...")

SHEET_URL = "https://opensheet.elk.sh/1wYLoyUfnPREts9WWfZwykG2Ows4Sa3XHJiOIgJMSi2E/Sheet1"

EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")

if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
    print("❌ Missing one or more email environment variables.")
    sys.exit(1)

try:
    print("📊 Fetching sheet...")
    resp = requests.get(SHEET_URL, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    now = datetime.now()
    posts_to_send = []

    # Find all pending posts that are due
    for row in data:
        status = row.get("Status", "").strip().lower()
        if status != "pending":
            continue

        date_str = row.get("Date", "").strip()
        time_str = row.get("Time", "").strip()
        if not date_str or not time_str:
            continue

        try:
            scheduled = datetime.strptime(
                f"{date_str} {time_str}",
                "%Y-%m-%d %I:%M %p"
            )
        except ValueError:
            # Skip rows with bad date/time format
            continue

        if scheduled <= now:
            posts_to_send.append(row)

    if not posts_to_send:
        print("⏳ No posts to send")
        sys.exit(0)

    for row in posts_to_send:
        post = row.get("Full LinkedIn Post", "").strip()
        if not post:
            continue

        print("📢 Sending email for post...")

        message = (
            "Time to post on LinkedIn 🚀\n\n"
            "Open: https://www.linkedin.com/feed/\n\n"
            "Copy and paste:\n\n"
            f"{post}\n"
        )

        msg = MIMEText(message)
        msg["Subject"] = "LinkedIn Post Reminder"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        try:
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
            print("✅ Email sent for one post")
        except Exception as e:
            print("❌ ERROR sending email:", str(e))

    print("✅ Run completed")

except Exception as e:
    print("❌ ERROR in main flow:", str(e))
    sys.exit(1)
