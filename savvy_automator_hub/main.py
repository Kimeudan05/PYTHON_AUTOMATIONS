import tkinter as tk
from tkinter import ttk, messagebox
import threading
from utils.logger import setup_logger
from modules import file_organizer, temp_cleaner, system_manager, pdf_tools

logger = setup_logger()


class SavvyAutomatorHub(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Savvy Automator Hub - Desktop Edition v1.0")
        self.geometry("900x600")
        self.configure(bg="#1E1E1E")

        self.create_widgets()

    def create_widgets(self):
        # ---------------- Toolbar ----------------
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=10)

        buttons = [
            ("Organize Files", self.run_file_organizer),
            ("Clean Temp", self.run_temp_cleaner),
            ("PDF Tools", self.run_pdf_tools),
            ("Send Email", self.run_email_sender),
            ("System Manager", self.run_system_manager),
        ]

        for text, cmd in buttons:
            ttk.Button(toolbar, text=text, command=cmd).pack(side="left", padx=5)

        # ---------------- Output Area ----------------
        self.output = tk.Text(self, height=20, bg="#121212", fg="white", wrap="word")
        self.output.pack(fill="both", expand=True, padx=10, pady=10)
        self.output.insert("end", "Welcome to Savvy Automator Hub!\n\n")

        # ---------------- Logger Area ----------------
        ttk.Label(
            self,
            text="Activity Log",
            foreground="white",
            background="#1E1E1E",
            anchor="w",
        ).pack(fill="x", padx=10)
        self.logger_box = tk.Text(
            self, height=8, bg="#000000", fg="#00FF00", wrap="word"
        )
        self.logger_box.pack(fill="x", padx=10, pady=5)

        self.log("Savvy Automator Hub initialized ✅")

    # ---------------- Logging ----------------
    def log(self, message):
        logger.info(message)
        self.logger_box.insert("end", message + "\n")
        self.logger_box.see("end")

    # ---------------- Placeholder ----------------
    def placeholder_action(self):
        self.log("[INFO] Placeholder feature.")
        self.output.insert("end", "Feature not yet implemented.\n")
        self.output.see("end")

    # ---------------- File Organizer ----------------
    def run_file_organizer(self):
        self.log("🧩 Starting File Organizer...")
        self.output.insert("end", "Organizing your files...\n")
        self.output.see("end")
        threading.Thread(target=self._run_file_organizer_task).start()

    def _run_file_organizer_task(self):
        file_organizer.run(self.log)
        self.output.insert("end", "✅ File organization complete.\n")
        self.output.see("end")

    # ---------------- Temp Cleaner ----------------
    def run_temp_cleaner(self):
        self.log("🧹 Starting Temp Cleaner...")
        self.output.insert("end", "Cleaning temporary files...\n")
        self.output.see("end")
        threading.Thread(target=self._run_temp_cleaner_task).start()

    def _run_temp_cleaner_task(self):
        temp_cleaner.run(self.log)
        self.output.insert("end", "✅ Temp cleaning complete.\n")
        self.output.see("end")

    # ---------------- System Manager ----------------
    def run_system_manager(self):
        self.log("⚙️ Opening System Manager...")
        sm_window = tk.Toplevel(self)
        sm_window.title("System Manager")
        sm_window.geometry("300x200")
        sm_window.configure(bg="#1E1E1E")

        buttons = [
            (
                "Restart",
                lambda: self._confirm_system_action(system_manager.restart, "restart"),
            ),
            (
                "Shutdown",
                lambda: self._confirm_system_action(
                    system_manager.shutdown, "shutdown"
                ),
            ),
            ("Lock", lambda: self._run_system_action_thread(system_manager.lock)),
            ("Sleep", lambda: self._run_system_action_thread(system_manager.sleep)),
        ]

        for text, cmd in buttons:
            ttk.Button(sm_window, text=text, command=cmd).pack(
                fill="x", padx=20, pady=5
            )

    def _confirm_system_action(self, func, action_name):
        result = messagebox.askyesno(
            "Confirm", f"Are you sure you want to {action_name}?"
        )
        if result:
            self._run_system_action_thread(func)

    def _run_system_action_thread(self, func):
        threading.Thread(target=lambda: func(self.log)).start()

        # ---------------- PDF Tools ----------------

    def run_pdf_tools(self):
        self.log("📄 Opening PDF Tools...")
        pdf_window = tk.Toplevel(self)
        pdf_window.title("PDF Tools")
        pdf_window.geometry("350x180")
        pdf_window.configure(bg="#1E1E1E")

        ttk.Button(
            pdf_window,
            text="Merge PDFs",
            command=lambda: threading.Thread(target=self._merge_pdfs).start(),
        ).pack(fill="x", padx=20, pady=10)
        ttk.Button(
            pdf_window,
            text="Convert PDF to Word",
            command=lambda: threading.Thread(target=self._convert_pdf_to_word).start(),
        ).pack(fill="x", padx=20, pady=10)

    def _merge_pdfs(self):
        from modules import pdf_tools

        pdf_tools.merge_pdfs(self.log)

    def _convert_pdf_to_word(self):
        from modules import pdf_tools

        pdf_tools.convert_pdf_to_word(self.log)

    # ---------------- Email Sender ----------------

    def run_email_sender(self):
        self.log("✉️ Opening Email Sender...")
        threading.Thread(target=self._run_email_sender_task).start()

    def run_email_sender(self):
        self.log("✉️ Opening Email Sender...")

        # Run Tkinter dialogs in main thread
        from tkinter import simpledialog, messagebox, filedialog
        from modules import email_sender

        sender_email = simpledialog.askstring(
            "Sender Email", "Enter your Gmail address:"
        )
        if not sender_email:
            return

        app_password = simpledialog.askstring(
            "App Password", "Enter your Gmail app password:", show="*"
        )
        if not app_password:
            return

        recipient = simpledialog.askstring("Recipient", "Enter recipient email:")
        subject = simpledialog.askstring("Subject", "Enter subject:")
        body = simpledialog.askstring("Message", "Enter your message:")

        attach = messagebox.askyesno("Attachment", "Would you like to attach a file?")
        attachment = None
        if attach:
            attachment = filedialog.askopenfilename(title="Select file to attach")

        # Now run email sending (network I/O) in a thread
        threading.Thread(
            target=email_sender.send_email,
            args=(
                sender_email,
                app_password,
                recipient,
                subject,
                body,
                attachment,
                self.log,
            ),
        ).start()


# ---------------- Main ----------------
if __name__ == "__main__":
    app = SavvyAutomatorHub()
    app.mainloop()
