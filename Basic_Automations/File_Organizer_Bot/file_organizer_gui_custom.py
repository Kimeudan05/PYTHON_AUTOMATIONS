"""
File Organizer Bot (Tkinter GUI) - Version 1.3.1
-------------------------------------------------
Version: 1.3.1
Author: Daniel Masila
Description:
Enhanced GUI version of File Organizer Bot with:
- Progress bar and completion percentage
- Custom category configuration
- Undo last organization run
- Optional upload to Google Drive or Dropbox
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import tkinter as tk
from tkinter import (
    filedialog,
    messagebox,
    scrolledtext,
    simpledialog,
    ttk,
    BooleanVar,
    Checkbutton,
)

# --- Cloud SDKs ---
try:
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive
except ImportError:
    print("PyDrive2 not installed. Google Drive upload will be disabled.")

try:
    import dropbox
except ImportError:
    print("Dropbox SDK not installed. Dropbox upload will be disabled.")

# --- 1. File Categories (default) ---
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv", ".pptx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".html", ".css", ".php"],
    "Installers": [".exe", ".msi", ".dmg"],
    "Others": [],
}

# --- 2. Temp file to store last run ---
UNDO_FILE = "last_run.json"


# --- 3. Helper functions ---
def create_folder(folder_path: Path):
    folder_path.mkdir(exist_ok=True)


def move_file(file_path: Path, target_folder: Path):
    try:
        shutil.move(str(file_path), str(target_folder / file_path.name))
        return f"Moved: {file_path.name} → {target_folder.name}", str(
            target_folder / file_path.name
        )
    except Exception as e:
        return f"Failed to move {file_path.name}: {e}", None


def log_action(log_widget, message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_widget.insert(tk.END, f"[{timestamp}] {message}\n")
    log_widget.see(tk.END)
    log_widget.update()


def save_last_run(mapping):
    with open(UNDO_FILE, "w") as f:
        json.dump(mapping, f)


def load_last_run():
    if Path(UNDO_FILE).exists():
        with open(UNDO_FILE) as f:
            return json.load(f)
    return {}


def undo_last_run(log_widget):
    mapping = load_last_run()
    if not mapping:
        messagebox.showinfo("Undo", "No previous run found")
        return
    for src, dest in mapping.items():
        try:
            shutil.move(dest, src)
            log_action(
                log_widget, f"Restored: {Path(dest).name} → {Path(src).parent.name}"
            )
        except Exception as e:
            log_action(log_widget, f"Failed to restore {dest}: {e}")
    messagebox.showinfo("Undo", "Undo complete")


# --- 4. Cloud Upload Functions ---
def upload_to_google_drive(file_path, log_widget):
    """Upload a file to Google Drive"""
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Opens browser for authentication
        drive = GoogleDrive(gauth)
        f = drive.CreateFile({"title": Path(file_path).name})
        f.SetContentFile(file_path)
        f.Upload()
        log_action(log_widget, f"Uploaded {Path(file_path).name} to Google Drive")
    except Exception as e:
        log_action(log_widget, f"Google Drive upload failed: {e}")


def upload_to_dropbox(file_path, log_widget, access_token):
    """Upload a file to Dropbox"""
    try:
        dbx = dropbox.Dropbox(access_token)
        with open(file_path, "rb") as f:
            dbx.files_upload(
                f.read(),
                f"/{Path(file_path).name}",
                mode=dropbox.files.WriteMode.overwrite,
            )
        log_action(log_widget, f"Uploaded {Path(file_path).name} to Dropbox")
    except Exception as e:
        log_action(log_widget, f"Dropbox upload failed: {e}")


# --- 5. Organize files with progress ---
def organize_files_gui(
    folder_path: str,
    log_widget,
    progress_bar=None,
    custom_categories=None,
    upload=False,
):
    folder = Path(folder_path)
    if not folder.exists():
        messagebox.showerror("Error", "Selected folder does not exist")
        return

    log_action(log_widget, f"Organizing files in: {folder}\n")
    categories = custom_categories if custom_categories else FILE_CATEGORIES
    moved_files = {}
    files = [f for f in folder.iterdir() if f.is_file()]
    total_files = len(files)

    # Ask cloud service if upload is enabled
    cloud_service = None
    dropbox_token = None
    if upload:
        service_choice = simpledialog.askstring(
            "Upload to Cloud", "Choose cloud service: Google or Dropbox"
        )
        if service_choice.lower() == "dropbox":
            dropbox_token = simpledialog.askstring(
                "Dropbox Access Token", "Enter your Dropbox Access Token"
            )
            cloud_service = "dropbox"
        elif service_choice.lower() == "google":
            cloud_service = "google"
        else:
            messagebox.showwarning(
                "Cloud Upload", "Invalid cloud choice. Skipping upload."
            )
            upload = False

    for i, file in enumerate(files, start=1):
        moved = False
        for category, extensions in categories.items():
            if file.suffix.lower() in extensions:
                target_folder = folder / category
                create_folder(target_folder)
                msg, dest = move_file(file, target_folder)
                log_action(log_widget, msg)
                if dest:
                    moved_files[str(file)] = str(dest)
                    if upload:
                        if cloud_service == "google":
                            upload_to_google_drive(dest, log_widget)
                        elif cloud_service == "dropbox":
                            upload_to_dropbox(dest, log_widget, dropbox_token)
                moved = True
                break
        if not moved:
            target_folder = folder / "Others"
            create_folder(target_folder)
            msg, dest = move_file(file, target_folder)
            log_action(log_widget, msg)
            if dest:
                moved_files[str(file)] = str(dest)
                if upload:
                    if cloud_service == "google":
                        upload_to_google_drive(dest, log_widget)
                    elif cloud_service == "dropbox":
                        upload_to_dropbox(dest, log_widget, dropbox_token)
        if progress_bar:
            progress_bar["value"] = int((i / total_files) * 100)
            log_widget.update()

    save_last_run(moved_files)
    log_action(log_widget, "\nFile organization complete!")
    messagebox.showinfo("Success", "File organization complete!")


# --- 6. GUI Functions ---
def open_folder_dialog(entry_widget):
    folder = filedialog.askdirectory(title="Select folder to organize")
    if folder:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder)


def configure_categories():
    config_window = tk.Toplevel()
    config_window.title("Configure Categories")
    config_window.geometry("400x400")

    tk.Label(config_window, text="Add/Edit categories (JSON format)").pack(pady=5)
    text_box = scrolledtext.ScrolledText(config_window, width=50, height=20)
    text_box.pack(padx=10, pady=5)
    text_box.insert(tk.END, json.dumps(FILE_CATEGORIES, indent=4))

    def save_config():
        try:
            new_categories = json.loads(text_box.get("1.0", tk.END))
            global FILE_CATEGORIES
            FILE_CATEGORIES = new_categories
            messagebox.showinfo("Success", "Categories updated")
            config_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid JSON: {e}")

    tk.Button(config_window, text="Save", command=save_config).pack(pady=5)


# --- 7. Build GUI ---
def build_gui():
    root = tk.Tk()
    root.title("File Organizer Bot v1.3.1")
    root.geometry("700x550")
    root.resizable(False, False)

    tk.Label(
        root, text="🗂️ File Organizer Bot v1.3.1", font=("Segoe UI", 14, "bold")
    ).pack(pady=10)

    tk.Label(root, text="Select a folder to organize:", font=("Segoe UI", 10)).pack(
        pady=(10, 0)
    )
    frame = tk.Frame(root)
    frame.pack(pady=5)
    folder_entry = tk.Entry(frame, width=50, font=("Segoe UI", 10))
    folder_entry.pack(side=tk.LEFT, padx=5)
    tk.Button(
        frame, text="Browse", command=lambda: open_folder_dialog(folder_entry)
    ).pack(side=tk.LEFT)

    # Upload checkbox
    upload_var = BooleanVar()
    Checkbutton(root, text="Upload organized files to cloud", variable=upload_var).pack(
        pady=5
    )

    # Progress bar
    progress_bar = ttk.Progressbar(
        root, orient="horizontal", length=550, mode="determinate"
    )
    progress_bar.pack(pady=10)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    tk.Button(
        button_frame,
        text="Start Organizing",
        bg="#4CAF50",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=lambda: organize_files_gui(
            folder_entry.get(), log_box, progress_bar, upload=upload_var.get()
        ),
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(
        button_frame,
        text="Undo Last Run",
        bg="#f44336",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=lambda: undo_last_run(log_box),
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(
        button_frame,
        text="Configure Categories",
        bg="#2196F3",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=configure_categories,
    ).pack(side=tk.LEFT, padx=5)

    # Log box
    log_box = scrolledtext.ScrolledText(
        root, width=90, height=25, wrap=tk.WORD, font=("Consolas", 9)
    )
    log_box.pack(padx=10, pady=5)

    # Footer
    tk.Label(
        root, text="Created by Daniel Masila", font=("Segoe UI", 8), fg="#555"
    ).pack(pady=5)
    root.mainloop()


# --- 8. Run GUI ---
if __name__ == "__main__":
    build_gui()
