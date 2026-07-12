"""
Wayne AI Pharma - Document Processor
Extract text from PDF/DOCX and redact PHI.
"""
import re
import io
from typing import Tuple
import PyPDF2
import docx
from config import PHI_PATTERNS


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes using PyPDF2."""
    text_parts = []
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX bytes using python-docx."""
    doc = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def extract_text(file_bytes: bytes, file_type: str) -> str:
    """Extract text based on file type."""
    if file_type == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif file_type == "docx":
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def redact_phi(text: str) -> Tuple[str, dict]:
    """
    Redact Protected Health Information from text.
    Returns (redacted_text, redaction_summary)
    """
    redacted = text
    summary = {"emails_redacted": 0, "phones_redacted": 0, "names_redacted": 0}

    # Redact emails
    email_matches = re.findall(PHI_PATTERNS["email"], redacted, re.IGNORECASE)
    redacted = re.sub(PHI_PATTERNS["email"], "[EMAIL REDACTED]", redacted, flags=re.IGNORECASE)
    summary["emails_redacted"] = len(email_matches)

    # Redact phone numbers
    phone_matches = re.findall(PHI_PATTERNS["phone"], redacted)
    redacted = re.sub(PHI_PATTERNS["phone"], "[PHONE REDACTED]", redacted)
    summary["phones_redacted"] = len(phone_matches)

    # Redact name patterns
    for pattern in PHI_PATTERNS["name_patterns"]:
        name_matches = re.findall(pattern, redacted)
        redacted = re.sub(pattern, "[NAME REDACTED]", redacted)
        summary["names_redacted"] += len(name_matches)

    return redacted, summary


def get_text_preview(text: str, max_chars: int = 300) -> str:
    """Return a preview of text for display."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."
