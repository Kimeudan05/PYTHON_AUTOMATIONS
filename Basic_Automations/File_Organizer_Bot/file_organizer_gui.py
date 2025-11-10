"""
File Organizer Bot (Tkinter GUI)
--------------------------------
Version: 1.2.0
Author: Daniel Masila
Description:
A GUI version of the File Organizer Bot that lets you select a folder,
organize files by category, and display progress in a Tkinter interface.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


#  --- 1. File Categories --
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


# 2. --- Helper functions ---
def create_folder(folder_path: Path):
    """Create folder if it doesn’t exist."""
    folder_path.mkdir(exist_ok=True)


def move_file(file_path: Path, target_folder: Path):
    """Move file into the target folder."""
    try:
        shutil.move(str(file_path), str(target_folder / file_path.name))
        return f"Moved: {file_path.name} → {target_folder.name}"
    except Exception as e:
        return f"Failed to move {file_path.name}: {e}"


def log_action(log_widget, message: str):
    """Append message to the GUI log area"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_widget.insert(tk.END, f"[{timestamp}] {message}\n")
    log_widget.see(tk.END)
    log_widget.update()


# 3. --- The main logic script ---
def organize_files_gui(folder_path: str, log_widget):
    """Organize files from selected folder"""
    folder = Path(folder_path)
    if not folder.exists():
        messagebox.showerror("Error", "Selected folder does not exist")
        return

    log_action(log_widget, f"Organizing files in : {folder}\n")

    for file in folder.iterdir():
        if file.is_file():
            moved = False
            for category, extensions in FILE_CATEGORIES.items():
                if file.suffix.lower() in extensions:
                    target_folder = folder / category
                    create_folder(target_folder)
                    msg = move_file(file, target_folder)
                    log_action(log_widget, msg)
                    moved = True
                    break
            if not moved:
                target_folder = folder / "Others"
                create_folder(target_folder)
                msg = move_file(file, target_folder)
                log_action(log_widget, msg)

    log_action(log_widget, "\n File organization complete!")
    messagebox.showinfo("Success", "File Organization complete")


# 4. --- GUI setup --


def open_folder_dialog(entry_widget):
    """Open file dialog to choose folder"""
    folder = filedialog.askdirectory(title="select folder to organize")
    if folder:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder)


def build_gui():
    """Build and display the Tkinter interface"""

    root = tk.Tk()
    root.title("File Organizer Bot")
    root.geometry("600x400")
    root.resizable(False, False)

    # --- Title ---
    tk.Label(
        root, text="🗂️  File Organizer Bot", font=("Segoe UI", 14, "bold"), fg="#333"
    ).pack(pady=10)

    # --- Folder selection ---
    tk.Label(root, text="Select a folder to organize:", font=("Segoe UI", 10)).pack(
        pady=(10, 0)
    )

    frame = tk.Frame(root)
    frame.pack(pady=5)
    folder_entry = tk.Entry(frame, width=50, font=("Segoe UI", 10))
    folder_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(
        frame,
        text="Browse",
        command=lambda: open_folder_dialog(folder_entry),
    ).pack(side=tk.LEFT)

    # --- Start button ---
    tk.Button(
        root,
        text="Start Organizing",
        bg="#4CAF50",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=lambda: organize_files_gui(folder_entry.get(), log_box),
    ).pack(pady=10)

    # --- Log box ---
    log_box = scrolledtext.ScrolledText(
        root, width=70, height=15, wrap=tk.WORD, font=("Consolas", 9)
    )
    log_box.pack(padx=10, pady=5)

    # --- Footer ---
    tk.Label(
        root,
        text="Version 1.2.0 • Created by Daniel Masila",
        font=("Segoe UI", 8),
        fg="#555",
    ).pack(pady=5)

    root.mainloop()


# 5. ----- RUN the GUI
if __name__ == "__main__":
    build_gui()
