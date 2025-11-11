import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from core import system_actions, update_manager, auth_manager, logger as core_logger
import threading

APP_TITLE = "SavvySystem Manager"
VERSION = "v1.2.0"


def launch_gui():
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("640x480")
    root.configure(bg="#0B132B")

    # --- Top frame (controls) ---
    top = tk.Frame(root, bg="#0B132B")
    top.pack(fill="x", padx=12, pady=(12, 6))

    title = tk.Label(
        top, text=APP_TITLE, fg="#FFFFFF", bg="#0B132B", font=("Segoe UI", 18, "bold")
    )
    title.pack(anchor="w")

    subtitle = tk.Label(
        top,
        text="Secure system control — shutdown, restart, rename, update",
        fg="#CFCFCF",
        bg="#0B132B",
        font=("Segoe UI", 10),
    )
    subtitle.pack(anchor="w", pady=(2, 8))

    # --- Controls frame ---
    controls = tk.Frame(root, bg="#0B132B")
    controls.pack(fill="x", padx=12, pady=6)

    def append_log(msg, level="info"):
        """Append to UI log and to disk log."""
        timestamped = f"{msg}"
        log_text.configure(state="normal")
        log_text.insert(tk.END, timestamped + "\n")
        log_text.see(tk.END)
        log_text.configure(state="disabled")
        core_logger.log_action(msg, level=level)

    def authorize_and_run(fn, *args, **kwargs):
        """Prompt for authorization on main thread, then run system action in background."""

        append_log("Requesting authorization...")

        # Run the password dialog in the main thread (safe)
        ok = auth_manager.verify_user(gui_mode=True)

        if not ok:
            append_log("Authorization failed.", level="warning")
            messagebox.showerror("Auth Failed", "Incorrect password or canceled.")
            return

        append_log("Authorization successful.")

        # Now launch the actual command in a background thread
        def worker():
            try:
                append_log(f"Running: {fn.__name__} ...")
                result = fn(*args, **kwargs)
                append_log(f"Command launched: {fn.__name__} (result={result})")
                messagebox.showinfo(
                    "Done", f"Command launched: {fn.__name__}. Check logs for details."
                )
            except Exception as e:
                append_log(f"Error running {fn.__name__}: {e}", level="error")
                messagebox.showerror("Error", f"{e}")

        threading.Thread(target=worker, daemon=True).start()

    # Buttons
    btn_shutdown = ttk.Button(
        controls,
        text="🔻 Shutdown",
        command=lambda: authorize_and_run(system_actions.shutdown_computer),
    )
    btn_restart = ttk.Button(
        controls,
        text="🔁 Restart",
        command=lambda: authorize_and_run(system_actions.restart_computer),
    )
    btn_rename_restart = ttk.Button(
        controls, text="🖥 Rename + Restart", command=lambda: on_rename_restart()
    )
    btn_update = ttk.Button(
        controls,
        text="⬆️ Check & Install Updates",
        command=lambda: authorize_and_run(on_update_wrapper),
    )

    # --- Controls frame (additional) ---
    clear_log_button = ttk.Button(
        controls,
        text="🧹 Clear Logs",
        command=lambda: clear_log(),
    )
    clear_log_button.grid(row=1, column=0, padx=6, pady=6, sticky="ew")

    # Layout buttons in grid
    btn_shutdown.grid(row=0, column=0, padx=6, pady=6, sticky="ew")
    btn_restart.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
    btn_rename_restart.grid(row=0, column=2, padx=6, pady=6, sticky="ew")
    btn_update.grid(row=0, column=3, padx=6, pady=6, sticky="ew")

    for i in range(4):
        controls.grid_columnconfigure(i, weight=1)

    # --- Middle area (info) ---
    mid = tk.Frame(root, bg="#0B132B")
    mid.pack(fill="both", expand=False, padx=12, pady=(6, 6))

    info_label = tk.Label(
        mid,
        text="Note: Administrative (UAC) prompts will appear for restart/rename actions.\nRename takes effect after reboot.",
        fg="#E0E0E0",
        bg="#0B132B",
        font=("Segoe UI", 9),
    )
    info_label.pack(anchor="w")

    # --- Bottom area: log viewer ---
    log_frame = tk.Frame(root)
    log_frame.pack(fill="both", expand=True, padx=12, pady=(6, 12))

    log_text = scrolledtext.ScrolledText(
        log_frame, state="disabled", wrap="word", height=10, font=("Consolas", 10)
    )
    log_text.pack(fill="both", expand=True)

    def clear_log():
        log_text.configure(state="normal")
        log_text.delete(1.0, tk.END)  # Clears the log viewer
        log_text.configure(state="disabled")
        append_log("Logs cleared by user.", level="info")  # Optionally log the action

    # Helper actions that combine UI behavior
    def on_rename_restart():
        name = simpledialog.askstring(
            "Rename PC", "Enter new computer name:", parent=root
        )
        if not name:
            append_log("Rename canceled by user.", level="warning")
            return
        # Warn user UAC will appear
        if not messagebox.askyesno(
            "Confirm",
            f"Rename PC to '{name}'? This will require elevation and a reboot to take effect. Continue?",
        ):
            append_log("Rename aborted by user.")
            return
        append_log(f"User requested rename to '{name}'")
        # Launch rename in background after auth
        authorize_and_run(system_actions.rename_computer, name)

    def on_update_wrapper():
        # Running update check and install on background thread (no admin prompt here since PS modules may require elevated)
        append_log("Checking for updates (may require elevation)...")
        # We do the check and show results in the log
        try:
            updates = update_manager.check_updates()
            append_log("Update check output (truncated):")
            # show first 500 chars to avoid huge logs
            append_log(updates[:2000] if updates else "No output returned")
            # Ask user if they want to install
            if messagebox.askyesno(
                "Install updates",
                "Install available updates now? This may reboot the machine.",
            ):
                append_log("User confirmed install. Launching installer (elevated).")
                update_manager.install_updates()
                append_log("Install command launched.")
            else:
                append_log("User canceled install.")
        except Exception as e:
            append_log(f"Update check/install failed: {e}", level="error")

    # Preload last N lines of log file to UI
    try:
        with open(core_logger.LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()[-200:]
            log_text.configure(state="normal")
            log_text.insert(tk.END, "".join(lines))
            log_text.configure(state="disabled")
            log_text.see(tk.END)
    except Exception:
        pass

    # Footer
    footer = tk.Label(
        root,
        text=f"{VERSION} • SavvySolveTech",
        fg="#AAAAAA",
        bg="#0B132B",
        font=("Segoe UI", 9),
    )
    footer.pack(side="bottom", pady=6)

    root.mainloop()
