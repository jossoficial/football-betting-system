from pipeline import run_pipeline
from notifier import send_report
from email_sender import send_email

def main():
    picks = run_pipeline()

    send_report(picks)
    send_email(picks)

if __name__ == "__main__":
    main()
