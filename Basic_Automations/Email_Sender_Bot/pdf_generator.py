from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os
import pandas as pd

PDF_DIR = "pdf_reports"
os.makedirs(PDF_DIR, exist_ok=True)


def generate_pdf_report(recipient_name, df, chart_path):
    pdf_path = os.path.join(PDF_DIR, f"{recipient_name}_report.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # --- Title section ---
    def draw_header(page_num):
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Weekly Sales Report - {recipient_name}")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 50, height - 50, f"Page {page_num}")

    # --- Draw a table page ---
    def draw_table(start_index, page_num):
        c.setFont("Helvetica", 10)
        draw_header(page_num)

        # Prepare table data
        end_index = min(start_index + 25, len(df))  # ~25 rows per page
        page_df = df.iloc[start_index:end_index]
        data = [["Product", "Sales"]] + page_df[["Product", "Sales"]].values.tolist()

        # Add total on last page
        if end_index == len(df):
            total = df["Sales"].sum()
            data.append(["Total", f"{total:,}"])

        # Create table
        table = Table(data, colWidths=[300, 100])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ]
            )
        )

        # Draw table
        table.wrapOn(c, width, height)
        table.drawOn(c, 50, height - 200 - (len(data) * 15))

        # Draw chart on last page only
        if end_index == len(df):
            chart_y = height - 450 - (len(data) * 5)
            c.drawImage(chart_path, 50, max(chart_y, 100), width=500, height=200)

        c.showPage()
        return end_index

    # --- Handle multi-page generation ---
    start = 0
    page_num = 1
    while start < len(df):
        start = draw_table(start, page_num)
        page_num += 1

    c.save()
    return pdf_path
