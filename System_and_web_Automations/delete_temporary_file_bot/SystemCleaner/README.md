## 🧹 System Cleaner GUI

```
Version: 1.0
Author: Daniel Masila
```

A lightweight desktop application to clean temporary files and unused cache folders. Built with Python and Tkinter, it helps you free up disk space quickly and safely.

### 🚀 Features

- Select one or multiple folders to clean.

- Automatically delete temporary/cache files.

- Real-time logs displayed directly in the GUI.

- Standalone Windows executable (.exe) — no Python installation needed.

- Fast, safe, and easy-to-use interface.

## 📦 Download & Install

✅ Pre-built Executable

1. Go to the Releases page

[releases](https://github.com/kimeudan05/PYTHON_AUTOMATIONS/system_and_web_automations/releases)

2. Download the latest release:

- SystemCleaner_GUI_v1.0.zip (contains SystemCleaner_GUI.exe).

3. Extract the zip file to any folder.

4. Double-click SystemCleaner_GUI.exe to launch the app.

`💡 Tip: Pin the .exe to Start Menu or Desktop for quick access.`

### 🐍 Run from Source (Optional, for developers)

---

### 1. Clone the repository:

```bash
git clone https://github.com/kimeudan05/PYTHON_AUTOMATIONS/system_and_web_automations/delete_temporary_file_bot.git

cd delete_temporary_files_bot
```

### 2. Create a virtual environment and install dependencies:

```
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Launch the GUI:

python gui_cleaner.py

## ⚡ How It Works

- Open the application.

- Click Browse to select one or multiple folders.

- Click Start Cleaning.

- Temporary/cache files will be deleted. Logs are displayed in real-time.

- ⚠️ Caution: Only delete files you are sure are temporary. Deleted files cannot be recovered.

## 🛠️ Built With

- Python 3.x

- Tkinter – GUI

- os & shutil – File operations

- threading – Background task execution

---

### 🤝 Contributing

1. Fork the repository

2. Create a branch (`git checkout -b feature-name`)

3. Make your changes (`git commit -m 'Add feature'`)

4. Push to the branch (`git push origin feature-name`)

5. Open a Pull Request
