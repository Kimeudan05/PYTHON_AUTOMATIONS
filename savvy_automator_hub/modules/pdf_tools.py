# modules/pdf_tools.py
import os
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
from pdf2docx import Converter


def merge_pdfs(log_func):
    log_func("📄 [PDF] Selecting PDF files to merge...")
    files = filedialog.askopenfilenames(
        title="Select PDF files to merge", filetypes=[("PDF Files", "*.pdf")]
    )
    if not files:
        log_func("[PDF] No files selected.")
        return

    output_path = filedialog.asksaveasfilename(
        title="Save merged PDF as",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
    )
    if not output_path:
        log_func("[PDF] Merge canceled by user.")
        return

    merger = PdfMerger()
    for pdf in files:
        log_func(f"Adding: {os.path.basename(pdf)}")
        merger.append(pdf)

    merger.write(output_path)
    merger.close()
    log_func(f"✅ Merged PDF saved to: {output_path}")
    messagebox.showinfo("Success", f"Merged PDF saved to:\n{output_path}")


def convert_pdf_to_word(log_func):
    log_func("📄 [PDF] Selecting PDF file to convert...")
    file = filedialog.askopenfilename(
        title="Select PDF file", filetypes=[("PDF Files", "*.pdf")]
    )
    if not file:
        log_func("[PDF] No file selected.")
        return

    output_path = filedialog.asksaveasfilename(
        title="Save as Word file",
        defaultextension=".docx",
        filetypes=[("Word Files", "*.docx")],
    )
    if not output_path:
        log_func("[PDF] Conversion canceled by user.")
        return

    try:
        log_func(
            f"Converting {os.path.basename(file)} → {os.path.basename(output_path)} ..."
        )
        cv = Converter(file)
        cv.convert(output_path)
        cv.close()
        log_func(f"✅ Conversion complete: {output_path}")
        messagebox.showinfo("Success", f"Word file saved to:\n{output_path}")
    except Exception as e:
        log_func(f"❌ Conversion failed: {e}")
        messagebox.showerror("Error", f"Failed to convert PDF:\n{e}")


def run(log_func):
    log_func("[PDF] Module loaded successfully.")
