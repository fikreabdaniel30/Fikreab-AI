"""
Fikreab AI — core logic.
Kept separate from app.py (Streamlit UI) so it can be unit tested
without needing a running Streamlit session.
"""

import os
import time
from io import BytesIO

from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF

MODEL_NAME = "gemini-2.5-flash"
MAX_CHARS = 30000
MAX_FILE_SIZE_MB = 15
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
UNICODE_FONT_PATH = os.path.join(FONT_DIR, "DejaVuSans.ttf")

MODES = {
    "📝 Notes": "Create detailed, well-structured study notes with clear headings and subheadings, based only on the content below.",
    "🗂 Flashcards": "Create a set of flashcards in 'Front: ... / Back: ...' format, based only on the content below.",
    "📉 Summary": "Summarize the content below into clear, concise bullet points covering the key ideas.",
    "🎯 Exam Questions": "Create 5 exam-style questions with model answers, based only on the content below.",
}


class PDFExtractionError(Exception):
    """Raised when a PDF can't be read or decrypted."""


class GenerationError(Exception):
    """Raised when the Gemini API call ultimately fails after retries."""


def check_file_size(uploaded_file) -> None:
    """Raise if the uploaded file exceeds the size limit."""
    size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise PDFExtractionError(
            f"File is {size_mb:.1f}MB, which exceeds the {MAX_FILE_SIZE_MB}MB limit."
        )


def extract_text(uploaded_file) -> str:
    """Extract up to MAX_CHARS of text from an uploaded PDF file-like object."""
    check_file_size(uploaded_file)

    try:
        reader = PdfReader(uploaded_file)
    except Exception as exc:
        raise PDFExtractionError(f"Couldn't open this PDF: {exc}") from exc

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise PDFExtractionError(
                "This PDF is password-protected and can't be read."
            ) from exc

    try:
        text = "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise PDFExtractionError(f"Couldn't extract text: {exc}") from exc

    return text[:MAX_CHARS]


def generate_content(model, mode: str, text_content: str, max_retries: int = 3):
    """
    Call the Gemini model with retry + exponential backoff.
    Retries on transient errors (rate limits, timeouts); raises GenerationError
    if all attempts fail.

    `model` is a `genai.GenerativeModel` instance (see app.py's load_model()).
    """
    prompt = f"{MODES[mode]}\n\n---\n\n{text_content}"
    last_error = None

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if not getattr(response, "text", None):
                raise GenerationError("Model returned an empty response.")
            return response.text
        except Exception as exc:
            last_error = exc
            is_last_attempt = attempt == max_retries - 1
            if is_last_attempt:
                break
            time.sleep(2 ** attempt)  # 1s, 2s, 4s backoff

    raise GenerationError(f"Generation failed after {max_retries} attempts: {last_error}")


def get_docx(text: str) -> BytesIO:
    """Convert markdown-ish text into a downloadable DOCX buffer."""
    doc = Document()
    doc.add_heading("Fikreab AI Notes", level=0)

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("### "):
            doc.add_heading(line[4:], level=3)
        elif line.startswith("## "):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("# "):
            doc.add_heading(line[2:], level=1)
        else:
            doc.add_paragraph(line)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def _unicode_font_available() -> bool:
    return os.path.isfile(UNICODE_FONT_PATH)


def get_pdf(text: str) -> bytes:
    """
    Convert text into a downloadable PDF.
    Uses a bundled Unicode TTF font if available (fonts/DejaVuSans.ttf),
    so non-Latin scripts (e.g. Amharic) render correctly. Falls back to
    Latin-1-only output if no font is bundled.
    """
    pdf = FPDF()
    pdf.add_page()

    if _unicode_font_available():
        pdf.add_font("DejaVu", "", UNICODE_FONT_PATH)
        pdf.set_font("DejaVu", size=12)
        safe_text = text
    else:
        pdf.set_font("Helvetica", size=12)
        safe_text = text.encode("latin-1", "ignore").decode("latin-1")

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 10, text=line if line.strip() else " ")

    raw = pdf.output(dest="S")
    if isinstance(raw, str):
        return raw.encode("latin-1", "ignore")
    return bytes(raw)
