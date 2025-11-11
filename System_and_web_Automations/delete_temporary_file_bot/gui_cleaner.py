import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import threading

# 🧩 Folders & file types to clean
UNWANTED_EXTENSIONS = (".tmp", ".log", ".bak", ".old")
UNWANTED_FOLDERS = ("__pycache__", ".cache", ".temp")

# ----------------------------- GUI SETUP -----------------------------
root = tk.Tk()
root.title("🧹 System Cleaner Bot")
root.geometry("750x550")
root.resizable(False, False)

selected_folders = []


# ----------------------------- LOGGING AREA -----------------------------
def log(message):
    """Display log messages in the GUI"""
    txt_log.config(state="normal")
    txt_log.insert(tk.END, message + "\n")
    txt_log.see(tk.END)
    txt_log.config(state="disabled")


# ----------------------------- CLEANER LOGIC -----------------------------
def scan_folder(folder_path):
    """Scan a folder and count removable items"""
    removable_items = []
    for root_dir, dirs, files in os.walk(folder_path):
        # Check for unwanted folders
        for d in dirs:
            if d in UNWANTED_FOLDERS:
                removable_items.append(os.path.join(root_dir, d))

        # Check for unwanted files
        for f in files:
            if f.endswith(UNWANTED_EXTENSIONS):
                removable_items.append(os.path.join(root_dir, f))
    return removable_items


def clean_folder(folder_path):
    """Delete unwanted files and folders"""
    removed_count = 0
    for root_dir, dirs, files in os.walk(folder_path, topdown=False):
        for f in files:
            if f.endswith(UNWANTED_EXTENSIONS):
                try:
                    os.remove(os.path.join(root_dir, f))
                    removed_count += 1
                except Exception as e:
                    log(f"⚠️ Could not delete file: {f} ({e})")

        for d in dirs:
            if d in UNWANTED_FOLDERS:
                try:
                    shutil.rmtree(os.path.join(root_dir, d), ignore_errors=True)
                    removed_count += 1
                except Exception as e:
                    log(f"⚠️ Could not remove folder: {d} ({e})")
    return removed_count


# ----------------------------- THREAD WRAPPERS -----------------------------
def start_task(task_name, func, *args):
    log(f"\n🚀 {task_name} started...")
    progress.start(10)
    threading.Thread(
        target=task_wrapper, args=(task_name, func, args), daemon=True
    ).start()


def task_wrapper(task_name, func, args):
    try:
        result = func(*args)
        if isinstance(result, str):
            log(f"✅ {task_name} completed: {result}")
        else:
            log(f"✅ {task_name} completed successfully")
    except Exception as e:
        log(f"❌ {task_name} failed: {e}")
    finally:
        progress.stop()


# ----------------------------- TASK ACTIONS -----------------------------
def select_folders():
    """Select multiple folders for cleaning"""
    folders = filedialog.askdirectory(mustexist=True, title="Select Folder to Clean")
    if folders:
        selected_folders.append(folders)
        folder_list.insert(tk.END, folders)
        log(f"📁 Added: {folders}")


def scan_action():
    """Scan selected folders for removable items"""
    if not selected_folders:
        messagebox.showwarning("No Folders", "Please select at least one folder.")
        return

    total_found = 0
    for folder in selected_folders:
        log(f"\n🔍 Scanning {folder} ...")
        items = scan_folder(folder)
        total_found += len(items)
        log(f"🧩 Found {len(items)} removable items in {folder}")

    log(f"\n📊 Total removable items found: {total_found}")


def clean_action():
    """Clean selected folders"""
    if not selected_folders:
        messagebox.showwarning("No Folders", "Please select at least one folder.")
        return

    total_removed = 0
    for folder in selected_folders:
        log(f"\n🧹 Cleaning {folder} ...")
        removed = clean_folder(folder)
        total_removed += removed
        log(f"✅ Removed {removed} items from {folder}")

    log(f"\n✨ Cleanup complete! Total removed: {total_removed}")


def clear_selection():
    selected_folders.clear()
    folder_list.delete(0, tk.END)
    log("🗑️ Cleared selected folders.")


# ----------------------------- GUI LAYOUT -----------------------------
tk.Label(root, text="🧹 System Cleaner Bot", font=("Segoe UI", 16, "bold")).pack(
    pady=10
)

# Folder selection
frame_select = tk.LabelFrame(root, text="Select Folders", padx=10, pady=10)
frame_select.pack(padx=10, pady=5, fill="x")

tk.Button(
    frame_select, text="Add Folder", command=select_folders, bg="#4CAF50", fg="white"
).pack(side=tk.LEFT, padx=10)
tk.Button(
    frame_select, text="Clear List", command=clear_selection, bg="#F44336", fg="white"
).pack(side=tk.LEFT, padx=10)

folder_list = tk.Listbox(frame_select, height=4, width=80)
folder_list.pack(padx=10, pady=10)

# Action buttons
frame_actions = tk.LabelFrame(root, text="Actions", padx=10, pady=10)
frame_actions.pack(padx=10, pady=5, fill="x")

tk.Button(
    frame_actions,
    text="🔍 Scan",
    width=15,
    bg="#2196F3",
    fg="white",
    command=scan_action,
).pack(side=tk.LEFT, padx=10)
tk.Button(
    frame_actions,
    text="🧹 Clean",
    width=15,
    bg="#9C27B0",
    fg="white",
    command=clean_action,
).pack(side=tk.LEFT, padx=10)

# Progress bar
progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=700, mode="indeterminate")
progress.pack(pady=10)

# Log area
txt_log = scrolledtext.ScrolledText(
    root, width=85, height=15, wrap=tk.WORD, state="disabled"
)
txt_log.pack(padx=10, pady=10)

tk.Label(root, text="Created by SavvySolveTech", font=("Segoe UI", 9), fg="#555").pack(
    pady=5
)

root.mainloop()
