from io import BytesIO

import pdfplumber
from docx import Document

def extract_text_from_text_resume(file_content: bytes, file_extension: str) -> str:
    if file_extension == ".pdf":
        with pdfplumber.open(BytesIO(file_content)) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text
    elif file_extension == ".docx":
        doc = Document(BytesIO(file_content))
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
        return text
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX files are allowed.")