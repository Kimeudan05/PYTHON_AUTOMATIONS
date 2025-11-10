# 🗂️ File Organizer Bot

**Version:** 1.0.0  
**Author:** Daniel Masila  
**Date:** November 10, 2025

---

## 📖 Overview

The **File Organizer Bot** is a Python automation tool that automatically sorts and organizes files into categorized folders based on file types.

It’s designed to clean up messy folders like your `Downloads` directory by moving files into properly labeled folders (e.g., `Images`, `Documents`, `Videos`, etc.).  
This version (v1.0.0) runs directly in the **terminal (CLI)** — simple, fast, and effective.

> 💡 _Version 1.2.0 will include a Tkinter GUI where users can visually select a folder and organize files with a single click._

---

## 🧱 Project Structure

```
PYTHON_AUTOMATIONS/
│
├── Basic_Automations/
│ ├── File_Organizer_Bot/
│ │ ├── file_organizer.py
│ │ └── README.md
│ │
│ ├── Bulk_File_Renamer/
│ ├── Email_Reminder_Bot/
│ └── ...
│
└── README.md ← general overview of all automation projects
```

---

## ⚙️ Features

✅ Automatically organizes files by type  
✅ Creates destination folders if missing  
✅ Logs all actions to `file_organizer_log.txt`  
✅ Works on Windows, macOS, and Linux  
✅ Fully customizable folder mappings

---

## 🗂️ Folder Categories

| Category   | File Extensions                          |
| ---------- | ---------------------------------------- |
| Images     | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`  |
| Documents  | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv` |
| Videos     | `.mp4`, `.mkv`, `.mov`, `.avi`           |
| Music      | `.mp3`, `.wav`, `.aac`, `.flac`          |
| Archives   | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`     |
| Scripts    | `.py`, `.js`, `.html`, `.css`, `.php`    |
| Installers | `.exe`, `.msi`, `.dmg`                   |
| Others     | Any file type not matched above          |

---

## 🧠 How It Works

1. Scans the target directory (default: your `Downloads` folder)
2. Identifies each file’s extension
3. Moves it into the corresponding categorized folder (creates one if it doesn’t exist)
4. Logs every action in a `file_organizer_log.txt` file

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Kimeudan05/PYTHON_AUTOMATIONS.git
cd PYTHON_AUTOMATIONS/Basic_Automations/File_Organizer_Bot
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate       # On Windows
# or
source venv/bin/activate    # On macOS/Linux
```

### 3. dependencies

No external libraries are required for this version — it uses only built-in Python modules:

- os
- shutil
- pathlib
- datetime

### ▶️ Usage

```bash
python file_organizer.py
```

### Example output

```
📁 Organizing files in: C:\Users\Daniel\Downloads

Created folder: Images
Created folder: Documents
Moved: photo1.jpg → Images
Moved: notes.pdf → Documents

File organization complete!
```

### Version History

| Version                | Description                                                        |
| ---------------------- | ------------------------------------------------------------------ |
| **1.0.0**              | CLI version of File Organizer Bot                                  |
| **1.2.0** _(Upcoming)_ | Tkinter GUI interface for folder selection and visual progress bar |

### Roadmap

🧭 Roadmap

Add GUI version with Tkinter (v1.2.0)

- Add scheduling feature (auto-clean every day/week)

- Add folder selection via file explorer
- Add dark mode interface
- Add notification popup upon completion

### 🧑‍💻 Author

**Daniel Masila**  
_Python Developer | Automation Enthusiast_

🌐 **Upcoming Website:** [savvysolvetech.com](https://savvysolvetech.com)  
💻 **GitHub:** [GitHub Profile](https://github.com/kimeudan05)

## 🆕 Version 1.2.0 — Tkinter GUI Release

🎨 Overview

This release introduces a Graphical User Interface (GUI) built with Tkinter, transforming the File Organizer Bot from a terminal-only tool into a clean, user-friendly desktop app.

Now, you can easily select a folder, click “Start Organizing”, and watch your files neatly sorted into categories — all without touching the command line.

### Whats new

_🪟 GUI Interface_

- Added Tkinter-based user interface

- Allows folder selection via file explorer

- “Start Organizing” button triggers the process instantly

_💬 Real-Time Log Window_

- Displays all moved files live as the script runs

- Scrollable text box for long logs

_✅ Success Popup_

- A small popup appears after organization is complete

_🗂️ Dual Version Support_

- Retained file_organizer.py (CLI)

- Added file_organizer_gui.py (GUI)

- Both share the same core logic and folder mapping

### folder structure

```ini
Basic Automations/
└── File Organizer Bot/
    ├── file_organizer.py         # CLI version (v1.0.0)
    ├── file_organizer_gui.py     # GUI version (v1.2.0)
    ├── README.md
```

### How to run

#### 1. Run the gui

```bash
python file_organizer_gui.py
```

#### 2. select folder

pick the folder you want to organize(eg download, desktop, etc)

#### 3. Start organizing

click the 'Start Organizing' button - your files will move into categorized folders

#### Supported Categories

| Category   | File Types                               |
| ---------- | ---------------------------------------- |
| Images     | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`  |
| Documents  | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv` |
| Videos     | `.mp4`, `.mkv`, `.mov`, `.avi`           |
| Music      | `.mp3`, `.wav`, `.aac`, `.flac`          |
| Archives   | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`     |
| Scripts    | `.py`, `.js`, `.html`, `.css`, `.php`    |
| Installers | `.exe`, `.msi`, `.dmg`                   |
| Others     | Uncategorized files                      |

**How does version 1 compare to version 2?**
| Feature | CLI (v1.0.0) | GUI (v1.2.0) |
| ------------------------- | ------------ | --------------- |
| Organize by file type | ✅ | ✅ |
| Automatic folder creation | ✅ | ✅ |
| Log progress | ✅ | ✅ (visual log) |
| GUI window | ❌ | ✅ |
| Folder selection | ❌ | ✅ |
| Success popup | ❌ | ✅ |

##### Example

- Before

```
Downloads/
├── report.pdf
├── photo.jpg
├── setup.exe
├── script.py
```

- After

```
Downloads/
├── Documents/
│   └── report.pdf
├── Images/
│   └── photo.jpg
├── Installers/
│   └── setup.exe
├── Scripts/
│   └── script.py
```

### Next Planned Features (v1.3.x+)

- Progress bar with completion percentage

- Custom category configuration

- Undo last organization run

- Convert to standalone .exe using pyinstaller

- Optional upload to cloud (Google Drive or Dropbox integration)

### 🌟 Support & Contribution

**_If you’d like to contribute:_**

- Fork this repo

- Create a new branch (feature/my-feature)

- Commit your changes

- Open a Pull Request

- You can also star ⭐ the repo if you find it useful!
