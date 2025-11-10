### PDF & Word Automation Tool 🧩

A desktop utility built with Python & Tkinter to automate common PDF and Word operations. Merge, split, and convert files easily with a user-friendly GUI.

#### Features

- Merge PDFs – Combine multiple PDF files into one.

- Split PDFs – Extract specific pages from a PDF.

- Word ↔ PDF Conversion – Convert Word documents to PDF and vice versa.

- Drag-and-Drop Support – Easily drag files into the app to select them.

- Progress & Logging – Track task completion with a progress bar and logs.

- Open Output Folder – Quickly access processed files.

### Project Structure

```bash
pdf_utility_bot/
│
├── main.py              # Tkinter GUI main application
├── pdf_tools.py         # PDF merge & split backend functions
├── converter_tool.py    # Word ↔ PDF conversion backend functions
├── output/              # Default folder where processed files are saved
├── README.md  # project documentation
```

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/pdf_utility_bot.git
cd pdf_utility_bot
```

2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:

```
tkinterdnd2, PyPDF2, docx2pdf, pdf2docx, python-docx
```

#### Usage

1. Run the GUI:

```bash
python main.py
```

2. Merge PDFs

- Browse or drag-and-drop PDF files.

- Click Merge to combine them into a single file in output/.

3. Split PDFs

- Select a PDF.

- Enter start and end pages.

- Click Split to save the extracted pages in output/.

4. Word ↔ PDF Conversion

- Select a Word document to convert to PDF.

- Select a PDF to convert to Word.

5. Open Output Folder

- Click to quickly access your processed files.
