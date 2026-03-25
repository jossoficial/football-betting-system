import smtplib
from email.mime.text import MIMEText
import os

def send_email(picks):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_TO")

    if not picks:
        message = "No hay picks con valor hoy."
    else:
        message = "PICKS DEL DÍA:\n\n"
        for p in picks:
            message += (
                f"{p['match']}\n"
                f"→ {p['market']}\n"
                f"Cuota: {p['odds']}\n"
                f"Prob: {p['prob']}\n"
                f"EV: {p['ev']}\n\n"
            )

    msg = MIMEText(message)
    msg["Subject"] = "Picks IA Futbol"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
