# modules/email_sender.py
import yagmail
from tkinter import simpledialog, filedialog, messagebox


def run(log_func):
    try:
        log_func("✉️ [Email] Preparing to send email...")

        # Collect details from user
        sender_email = simpledialog.askstring(
            "Sender Email", "Enter your Gmail address:"
        )
        app_password = simpledialog.askstring(
            "App Password", "Enter your Gmail app password:", show="*"
        )
        recipient = simpledialog.askstring("Recipient", "Enter recipient email:")
        subject = simpledialog.askstring("Subject", "Enter subject:")
        body = simpledialog.askstring("Message", "Enter your message:")

        attach = messagebox.askyesno("Attachment", "Would you like to attach a file?")
        attachment = None
        if attach:
            attachment = filedialog.askopenfilename(title="Select file to attach")

        if not (sender_email and app_password and recipient):
            log_func("❌ [Email] Missing required fields.")
            messagebox.showerror("Error", "Email not sent — missing required details.")
            return

        # Connect to Gmail
        log_func("[Email] Connecting to Gmail...")
        yag = yagmail.SMTP(sender_email, app_password)

        # Send message
        yag.send(
            to=recipient,
            subject=subject,
            contents=body,
            attachments=attachment if attachment else None,
        )
        log_func(f"✅ [Email] Sent successfully to {recipient}")
        messagebox.showinfo("Success", f"Email sent successfully to {recipient}")

    except Exception as e:
        log_func(f"❌ [Email] Failed to send email: {e}")
        messagebox.showerror("Error", f"Failed to send email:\n{e}")


def send_email(
    sender_email, app_password, recipient, subject, body, attachment, log_func
):
    try:
        log_func("[Email] Connecting to Gmail...")
        yag = yagmail.SMTP(sender_email, app_password)
        yag.send(
            to=recipient,
            subject=subject,
            contents=body,
            attachments=attachment if attachment else None,
        )
        log_func(f"✅ [Email] Sent successfully to {recipient}")
    except Exception as e:
        log_func(f"❌ [Email] Failed to send email: {e}")
