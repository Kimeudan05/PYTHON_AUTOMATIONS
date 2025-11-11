# 🧹 System Cleaner Bot (CLI Version)

### Author

**Daniel Masila**  
Python Developer | Automation Enthusiast  
🌐 [savvysolvetech.com](https://savvysolvetech.com)

---

## 🧩 Overview

**System Cleaner Bot** is a Python automation tool that scans your system’s temporary and cache directories and deletes unnecessary files to free up disk space.

---

## ⚙️ Features

- Automatically cleans temporary folders such as:
  - `C:\Users\<name>\AppData\Local\Temp`
  - System `/tmp` directories (on Linux/Mac)
- Deletes files with extensions: `.tmp`, `.log`, `.bak`, `.old`
- Removes folders like `__pycache__`, `.cache`, `.temp`
- Logs every deleted file and folder in `cleanup_log.txt`

---

## 🚀 Usage

### 1. Clone the repository

```bash
git clone https://github.com/kimeudan05/PYTHON_AUTOMATIONS/system_and_web_automation.git
cd system_and_web_automation/delete_temporary_files_bot
```

### 2. Run the cleaner

```
python main.py
```

### 3. check the clean up log

```
cleanup_log.txt
```

#### Example Output

## 🧩 System Cleaner Bot v1.0.0

Cleaning: C:\Users\Daniel\AppData\Local\Temp
Completed cleaning C:\Users\Daniel\AppData\Local\Temp. Deleted 23 items.

Cleanup completed. Check cleanup_log.txt for details.

### Version

```
v1.0.0 – Initial CLI Release
```

Next version (v1.1.0) will include a Tkinter GUI with folder selection and cleaning progress.
