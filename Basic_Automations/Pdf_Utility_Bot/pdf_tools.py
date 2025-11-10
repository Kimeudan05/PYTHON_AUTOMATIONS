from PyPDF2 import PdfMerger, PdfWriter, PdfReader
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def merge_pdfs(pdf_list, output_name="merged.pdf"):
    output_path = OUTPUT_DIR / output_name
    merger = PdfMerger()

    for pdf in pdf_list:
        merger.append(pdf)

    merger.write(output_path)
    merger.close()
    return output_path


def split_pdf(input_pdf, start_page, end_page, output_name="split.pdf"):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # pypdf2 is 0-indexed
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])

    output_path = OUTPUT_DIR / output_name
    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path
