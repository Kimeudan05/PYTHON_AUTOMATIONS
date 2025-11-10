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

### 🌟 Support & Contribution

**_If you’d like to contribute:_**

- Fork this repo

- Create a new branch (feature/my-feature)

- Commit your changes

- Open a Pull Request

- You can also star ⭐ the repo if you find it useful!
