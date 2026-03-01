import os
from docx import Document
from pypdf import PdfReader


def parse_pdf(file_path: str):
    """
    Extract text from PDF file.
    """
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def parse_docx(file_path: str):
    """
    Extract text from DOCX file.
    """
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])

    return text


def parse_resume(file_path: str):
    """
    Auto-detect file type and extract text.
    Supports PDF and DOCX.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return parse_pdf(file_path)

    elif extension == ".docx":
        return parse_docx(file_path)

    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")