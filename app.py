import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from io import BytesIO

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Fikreab AI | Professional Study Suite",
    page_icon="⚡",
    layout="wide"
)

# ==============================
# GEMINI SETUP
# ==============================
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")


# ==============================
# PDF TEXT EXTRACTOR
# ==============================
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text[:40000]  # prevent overload


# ==============================
# AI ENGINE
# ==============================
def run_ai(mode, content):

    system_prompt = """
    You are an expert academic assistant.
    Produce clear, structured, high-quality educational material.

    Always:
    - Use headers
    - Use bullet points
    - Highlight key concepts
    - Keep logical flow
    - Focus on exam usefulness
    """

    mode_prompts = {
        "📝 Structured Notes":
        "Create comprehensive structured study notes with headings, summaries, and key points.",

        "🗂️ Flashcard Set":
        "Create flashcards in the format Term: Definition. Focus on memorization.",

        "🎯 Exam Predictions":
        "Identify high-yield topics and generate 5 likely exam questions with answers.",

        "⚡ Fast Review":
        "Create an ultra concise revision sheet with only critical points."
    }

    prompt = f"""
    {system_prompt}

    TASK:
    {mode_prompts[mode]}

    CONTENT:
    {content}
    """

    response = model.generate_content(prompt)
    return response.text


# ==============================
# EXPORT FUNCTIONS
# ==============================
def export_docx(text):
    doc = Document()
    doc.add_heading("Fikreab AI Study Notes", 0)

    for line in text.split("\n"):
        doc.add_paragraph(line)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer


def export_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    safe_text = text.encode("latin-1", "ignore").decode("latin-1")

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1")


# ==============================
# SIDEBAR
# ==============================
with st.sidebar:

    st.title("⚡ Fikreab AI")

    mode = st.selectbox(
        "Select Mode",
        [
            "📝 Structured Notes",
            "🗂️ Flashcard Set",
            "🎯 Exam Predictions",
            "⚡ Fast Review"
        ]
    )

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])


# ==============================
# MAIN UI
# ==============================
st.title("🎓 Fikreab AI Studio")
st.caption("The Future of Academic Excellence")

if uploaded_file:

    with st.status("Analyzing document...", expanded=False):

        text_content = extract_pdf_text(uploaded_file)

        st.write("✅ Document processed successfully")

    if st.button("🚀 Generate"):

        with st.spinner("AI is generating content..."):

            try:
                output = run_ai(mode, text_content)
                st.session_state["output"] = output

            except Exception as e:
                st.error(f"Error: {e}")

if "output" in st.session_state:

    st.subheader("📘 Generated Content")
    st.write(st.session_state["output"])

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "📕 Download PDF",
            export_pdf(st.session_state["output"]),
            "study_notes.pdf"
        )

    with col2:
        st.download_button(
            "📄 Download DOCX",
            export_docx(st.session_state["output"]),
            "study_notes.docx"
        )

else:

    st.info("Upload a PDF to begin.")
