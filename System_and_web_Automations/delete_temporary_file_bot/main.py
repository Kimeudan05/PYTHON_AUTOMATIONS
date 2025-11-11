"""
System Cleaner Bot - Delete Temporary Files v1.0.0
-------------------------------------------------
Author: Daniel Masila
Description:
A simple Python automation script that scans and deletes
temporary or cache files to free up disk space.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# 1. --  Configuration --
DEFAULT_PATHS = [
    Path(os.getenv("TEMP", "/tmp")),
    Path.home() / "AppData" / "Local" / "Temp",
]

LOG_FILE = "cleaner_log.txt"
os.makedirs("logs", exist_ok=True)

TEMP_EXTENSIONS = [".tmp", ".log", ".bak", ".old"]
CACHE_FOLDERS = [
    "__pycache__",
    ".cache",
    ".npm",
    ".yarn",
    ".gradle",
    ".m2",
    ".gradle",
    ".temp",
    ".idea",
]


# 2. --  Helper Functions --
def log_action(message: str):
    """log action with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def delete_file(file_path: Path):
    """This function deletes a file"""
    try:
        os.remove(file_path)
        log_action(f"Deleted file: {file_path}")
    except Exception as e:
        log_action(f"Failed to delete file {file_path}: {e}")


def delete_folder(folder_path: Path):
    """This function deletes a folder"""
    try:
        shutil.rmtree(folder_path)
        log_action(f"Deleted folder: {folder_path}")
    except Exception as e:
        log_action(f"Failed to delete folder {folder_path}: {e}")


def clean_directory(directory_path: Path):
    """This function scans and deletes temp files in the provided directory"""
    print(f"Cleaning directory: {directory_path}")
    if not directory_path.exists():
        print("path does not exist")
        return

    delete_count = 0

    for root, dirs, files in os.walk(directory_path, topdown=False):
        for name in files:
            file_path = Path(root) / name
            if file_path.suffix.lower() in TEMP_EXTENSIONS:
                delete_file(file_path)
                delete_count += 1

        for name in dirs:
            folder_path = Path(root) / name
            if folder_path.name in CACHE_FOLDERS:
                delete_folder(folder_path)
                delete_count += 1
    print(f"Completed cleaning {directory_path} - Deleted {delete_count} items")
    log_action(f"Completed cleaning {directory_path} . Deleted {delete_count} items")


# -- 3. Run the cleaner--

if __name__ == "__main__":
    print("System Cleaner Bot v1.0.0")
    print("-" * 30)

    unique_paths = list(set(DEFAULT_PATHS))
    for folder in unique_paths:
        clean_directory(folder)

    print("\n Clean up completed. Check 'cleanup_log.txt for details")
