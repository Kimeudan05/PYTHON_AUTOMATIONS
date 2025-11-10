"""
File Organizer Bot
----------------------
Automates the process of organizing files in a selected directory
Moves files into  categoried folders based on their extentions

Author: Daniel Masila
Version : 1.0.0
Date : 2025-11-10
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# 1. --  Configuration --

# Directory to organize -> Here we are organizing the download folder
DOWNLOADS_DIR = Path.home() / "Downloads"

"""
same as  -> Path(os.path.join(Path.home(), "Downloads"))
-> Path.home()  # -> C:\Users\dante
-> Path.home() / "Downloads"  # -> C:\Users\dante\Downloads

"""


# folder categories and file extensions

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv", ".pptx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".dmg"],
    "Others": [],
}

# create a log file to track operations
LOG_FILE = DOWNLOADS_DIR / "file_organizer_log.txt"


# 2. --- Helper functions ---
def create_folder(folder_path: Path):
    """Create a folder if it does not exist"""

    if not folder_path.exists():
        folder_path.mkdir()
        print(f"Created folder :{folder_path.name}")


def move_file(file_path: Path, target_folder: Path):
    """Move a file into target folder."""
    try:
        shutil.move(str(file_path), str(target_folder / file_path.name))
        log_action(f"Moved : {file_path.name} -> {target_folder.name}")
    except Exception as e:
        log_action(f"Failed to move {file_path.name}: {e}")


def log_action(message: str):
    """log action with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


# 3 -- Main logic --
def organize_files():
    """Organize files in the target directory"""
    print(f"Organizing files in {DOWNLOADS_DIR}\n")

    for file in DOWNLOADS_DIR.iterdir():
        if file.is_file():
            moved = False
            for category, extensions in FILE_CATEGORIES.items():
                if file.suffix.lower() in extensions:
                    target_folder = DOWNLOADS_DIR / category
                    create_folder(target_folder)
                    move_file(file, target_folder)
                    moved = True
                    break
            if not moved:
                # Move unkonwn file types to others
                target_folder = DOWNLOADS_DIR / "Others"
                create_folder(target_folder)
                move_file(file, target_folder)

    print("\n File Organization complete")
    log_action("Orgabization completed successifully. \n")


# 4. ----- Run the script ---
if __name__ == "__main__":
    organize_files()
