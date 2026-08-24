import os
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        return ""
    return text.strip()


def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        text = "\n".join(
            [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
        )
        return text.strip()
    except Exception:
        return ""


def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return ""