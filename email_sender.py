import smtplib
from email.mime.text import MIMEText
import os

def send_email(picks):
    sender = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")
    receiver = os.environ.get("EMAIL_TO")

    if not sender or not password or not receiver:
        print("❌ ERROR: Secrets no cargados")
        return

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

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
            print("✅ Email enviado")
    except Exception as e:
        print("❌ ERROR EMAIL:", e)
