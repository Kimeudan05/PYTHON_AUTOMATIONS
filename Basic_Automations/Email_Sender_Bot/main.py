import schedule
import time
import os
import shutil
from generate_reports import load_data, generate_chart, generate_email_body
from pdf_generator import generate_pdf_report
from send_email import send_email
import yagmail

LOG_FILE = "logs/email_log.txt"
os.makedirs("logs", exist_ok=True)


def send_weekly_reports():
    """Generate, send, and clean up weekly reports."""
    data = load_data()
    recipients = data["Email"].unique()

    for recipient_email in recipients:
        recipient_df = data[data["Email"] == recipient_email]
        recipient_name = recipient_df["Name"].iloc[0]

        # --- Generate chart and reports ---
        chart_path = generate_chart(recipient_df, recipient_name)
        body_html, chart_file = generate_email_body(
            recipient_df, recipient_name, chart_path
        )
        pdf_path = generate_pdf_report(recipient_name, recipient_df, chart_path)

        # --- Send email ---
        sent = send_email(
            to=recipient_email,
            subject=f"Weekly Sales Report - {recipient_name}",
            body=[body_html, yagmail.inline(chart_file)],
            attachments=pdf_path,
        )

        # --- Log results ---
        with open(LOG_FILE, "a") as f:
            f.write(
                f"{time.ctime()}: Email to {recipient_name} ({recipient_email}) - {'Sent' if sent else 'Failed'}\n"
            )

    # --- Auto-clean temporary folders ---
    cleanup_temp_folders()


def cleanup_temp_folders():
    """Delete temporary folders used for inline charts and PDF reports."""
    temp_dirs = ["inline_charts", "pdf_reports"]
    for folder in temp_dirs:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🧹 Deleted temporary folder: {folder}")


# Schedule every Monday 8 AM
schedule.every().monday.at("08:00").do(send_weekly_reports)

print("Scheduler running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(30)
