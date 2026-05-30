import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import RECIPIENT_EMAIL, DIGEST_SUBJECT

def send_email(body: str):
    sender   = os.environ["GMAIL_USER"]
    password = os.environ["GMAIL_PASS"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = DIGEST_SUBJECT
    msg["From"]    = sender
    msg["To"]      = RECIPIENT_EMAIL

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, RECIPIENT_EMAIL, msg.as_string())

    print(f"Digest sent to {RECIPIENT_EMAIL}")
