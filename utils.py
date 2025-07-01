# utils.py

import fitz  # PyMuPDF
import docx
from fpdf import FPDF
import io

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

class StyledPDF(FPDF):
    def __init__(self, style="Classic"):
        super().__init__()
        self.style = style

    def header(self):
        self.set_font("Helvetica", "B", 16)
        if self.style == "Modern":
            self.set_text_color(100, 100, 255)
        elif self.style == "Minimal":
            self.set_text_color(50, 50, 50)
        else:  # Classic
            self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Resume", ln=True, align="C")
        self.ln(5)

    def add_section(self, title, content):
        if self.style == "Modern":
            self.set_font("Helvetica", "B", 13)
            self.set_text_color(30, 30, 200)
            self.cell(0, 10, title, ln=True)
            self.set_font("Helvetica", "", 11)
            self.set_text_color(50, 50, 50)
        elif self.style == "Minimal":
            self.set_font("Arial", "", 12)
            self.set_text_color(0, 0, 0)
            self.cell(0, 8, f"{title.upper()}", ln=True)
        else:  # Classic
            self.set_font("Times", "B", 12)
            self.set_text_color(0, 0, 128)
            self.cell(0, 10, title, ln=True)
            self.set_font("Times", "", 11)
            self.set_text_color(0, 0, 0)

        self.multi_cell(0, 8, content)
        self.ln(4)

def generate_pdf_resume(content, filename="resume.pdf", style="Classic"):
    """
    Generates a stylized multi-page PDF resume based on selected style.
    Returns the PDF as a BytesIO buffer for download.
    """
    pdf = StyledPDF(style=style)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    sections = content.strip().split("###")
    for section in sections:
        if ":" in section:
            title, body = section.strip().split(":", 1)
            pdf.add_section(title.strip(), body.strip())
        else:
            pdf.add_section("Details", section.strip())

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
