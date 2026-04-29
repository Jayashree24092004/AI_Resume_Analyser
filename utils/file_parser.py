# ─────────────────────────────────────────────────────────────────────────────
# utils/file_parser.py  ·  Extract plain text from uploaded resume files
# ─────────────────────────────────────────────────────────────────────────────

import io
import base64
import pdfplumber
import docx


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF file using pdfplumber."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text.strip())
    return "\n\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract all text from a DOCX file."""
    doc = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode plain text file."""
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1")


def pdf_to_base64(file_bytes: bytes) -> str:
    """Convert PDF bytes to base64 string for Claude document API."""
    return base64.standard_b64encode(file_bytes).decode("utf-8")


def parse_uploaded_file(uploaded_file) -> dict:
    """
    Parse a Streamlit UploadedFile object.

    Returns:
        {
            "text":      str  — extracted plain text,
            "base64":    str  — base64 PDF (only for PDF files, else None),
            "is_pdf":    bool,
            "num_pages": int  — page count (PDF only),
            "file_size": int  — bytes,
            "filename":  str,
        }
    """
    file_bytes = uploaded_file.read()
    ext        = uploaded_file.name.split(".")[-1].lower()
    result     = {
        "text":      "",
        "base64":    None,
        "is_pdf":    False,
        "num_pages": 1,
        "file_size": len(file_bytes),
        "filename":  uploaded_file.name,
        "ext":       ext,
    }

    if ext == "pdf":
        result["text"]      = extract_text_from_pdf(file_bytes)
        result["base64"]    = pdf_to_base64(file_bytes)
        result["is_pdf"]    = True
        # Count pages
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            result["num_pages"] = len(pdf.pages)

    elif ext == "docx":
        result["text"] = extract_text_from_docx(file_bytes)

    elif ext == "txt":
        result["text"] = extract_text_from_txt(file_bytes)

    return result