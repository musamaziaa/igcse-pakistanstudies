import fitz  # PyMuPDF
import re


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract full text from PDF bytes, preserving Arabic."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    for page in doc:
        text = page.get_text("text")
        pages.append(text)
    doc.close()
    return "\n".join(pages)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract full text from DOCX bytes."""
    import io
    from docx import Document
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {filename}")


def contains_arabic(text: str) -> bool:
    return bool(re.search(r'[\u0600-\u06FF]', text))


def extract_arabic_segments(text: str) -> list:
    """Return list of Arabic text segments found in text."""
    pattern = r'[\u0600-\u06FF][^\u0000-\u05FF\u0700-\uFFFF]*'
    return re.findall(pattern, text)
