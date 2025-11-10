import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from pdf_tools import merge_pdfs, split_pdf
from converter_tools import word_to_pdf, pdf_to_word
import os
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD

# Output folder
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- Tkinter GUI ----------
root = TkinterDnD.Tk()
root.title("🧩 PDF & Word Automation Tool")
root.geometry("750x600")
root.resizable(False, False)

# ---------- Variables ----------
pdf_paths = tk.StringVar()
start_page_entry = tk.StringVar()
end_page_entry = tk.StringVar()


# ---------- Logging ----------
def log(message):
    """Append message to the log text widget"""
    txt_log.config(state="normal")
    txt_log.insert(tk.END, message + "\n")
    txt_log.see(tk.END)
    txt_log.config(state="disabled")


# ---------- Task Handling ----------
def start_task(task_name, func, *args):
    """Run a task in a separate thread with progress and logs"""
    log(f"🚀 Starting task: {task_name} ...")
    progress.start(10)
    threading.Thread(
        target=task_wrapper, args=(task_name, func, args), daemon=True
    ).start()


def task_wrapper(task_name, func, args):
    """Execute task safely in a thread"""
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
        progress["value"] = 0


# ---------- Drag-and-Drop ----------
def drop(event):
    files = root.tk.splitlist(event.data)
    pdf_paths.set(";".join(files))
    log(f"📥 Files dropped: {len(files)} file(s) selected")


# ---------- File Selection ----------
def select_pdfs():
    files = filedialog.askopenfilenames(
        title="Select PDF files", filetypes=[("PDF Files", "*.pdf")]
    )
    if files:
        pdf_paths.set(";".join(files))
        log(f"📂 Selected {len(files)} PDFs")


# ---------- Actions ----------
def merge_action():
    files = pdf_paths.get().split(";")
    if not files or files == [""]:
        messagebox.showwarning("No files", "Select PDFs first.")
        return
    start_task("Merge PDFs", merge_pdfs, files)


def split_action():
    pdf = filedialog.askopenfilename(
        title="Select PDF to split", filetypes=[("PDF Files", "*.pdf")]
    )
    if not pdf:
        return
    try:
        start = int(start_page_entry.get())
        end = int(end_page_entry.get())
        start_task(f"Split PDF ({os.path.basename(pdf)})", split_pdf, pdf, start, end)
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter valid page numbers.")


def word_to_pdf_action():
    file = filedialog.askopenfilename(
        title="Select Word file", filetypes=[("Word Documents", "*.docx")]
    )
    if not file:
        return
    start_task("Word → PDF", word_to_pdf, file)


def pdf_to_word_action():
    file = filedialog.askopenfilename(
        title="Select PDF file", filetypes=[("PDF Files", "*.pdf")]
    )
    if not file:
        return
    start_task("PDF → Word", pdf_to_word, file)


def open_output_folder():
    os.startfile(os.path.abspath(OUTPUT_DIR))
    log("📂 Opened output folder.")


# ---------- GUI Layout ----------
tk.Label(root, text="PDF & Word Automation Tool", font=("Segoe UI", 16, "bold")).pack(
    pady=10
)

# Merge PDFs
frame_merge = tk.LabelFrame(root, text="Merge PDFs", padx=10, pady=10)
frame_merge.pack(padx=10, pady=5, fill="x")
tk.Entry(frame_merge, textvariable=pdf_paths, width=70).pack(side=tk.LEFT, padx=5)
tk.Button(frame_merge, text="Browse", command=select_pdfs).pack(side=tk.LEFT, padx=5)
tk.Button(
    frame_merge, text="Merge", bg="#4CAF50", fg="white", command=merge_action
).pack(side=tk.LEFT, padx=5)

# Split PDFs
frame_split = tk.LabelFrame(root, text="Split PDF", padx=10, pady=10)
frame_split.pack(padx=10, pady=5, fill="x")
tk.Label(frame_split, text="Start Page:").pack(side=tk.LEFT, padx=5)
tk.Entry(frame_split, textvariable=start_page_entry, width=5).pack(side=tk.LEFT)
tk.Label(frame_split, text="End Page:").pack(side=tk.LEFT, padx=5)
tk.Entry(frame_split, textvariable=end_page_entry, width=5).pack(side=tk.LEFT)
tk.Button(
    frame_split, text="Split", bg="#2196F3", fg="white", command=split_action
).pack(side=tk.LEFT, padx=10)

# Conversion
frame_convert = tk.LabelFrame(root, text="File Conversion", padx=10, pady=10)
frame_convert.pack(padx=10, pady=5, fill="x")
tk.Button(
    frame_convert,
    text="Word → PDF",
    bg="#9C27B0",
    fg="white",
    command=word_to_pdf_action,
).pack(side=tk.LEFT, padx=10)
tk.Button(
    frame_convert,
    text="PDF → Word",
    bg="#FF9800",
    fg="white",
    command=pdf_to_word_action,
).pack(side=tk.LEFT, padx=10)

# Open Output Folder
tk.Button(
    root,
    text="Open Output Folder",
    bg="#607D8B",
    fg="white",
    command=open_output_folder,
).pack(pady=5)

# Progress Bar
progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=700, mode="indeterminate")
progress.pack(pady=5)

# Log output
txt_log = scrolledtext.ScrolledText(
    root, width=85, height=15, wrap=tk.WORD, state="disabled"
)
txt_log.pack(padx=10, pady=10)

tk.Label(root, text="Created by Daniel Masila", font=("Segoe UI", 9), fg="#555").pack(
    pady=5
)

# ---------- Drag-and-Drop Registration ----------
frame_merge.drop_target_register(DND_FILES)
frame_merge.dnd_bind("<<Drop>>", drop)

# Run the GUI
root.mainloop()
