from pipeline import run_pipeline
from notifier import send_report


def main():
    picks = run_pipeline()

    if not picks:
        print("\n⚠️ No hay picks con valor hoy\n")
        return

    send_report(picks)


if __name__ == "__main__":
    main()
