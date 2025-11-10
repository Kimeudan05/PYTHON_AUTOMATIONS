import os
from docx import Document
from docx2pdf import convert
from pathlib import Path
from pdf2docx import Converter

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def word_to_pdf(word_path):
    try:
        output_path = OUTPUT_DIR / (Path(word_path).stem + "_converted.pdf")
        convert(word_path, output_path)
        return output_path
    except Exception as e:
        return f"error converting word -> PDF: {e}"


def pdf_to_word(pdf_path):
    try:
        output_path = OUTPUT_DIR / (Path(pdf_path).stem + "_converted.docx")
        cv = Converter(pdf_path)
        cv.convert(output_path)
        cv.close()
        return output_path
    except Exception as e:
        return f"error converting PDF -> Word: {e}"
