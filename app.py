import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Fikreab AI | Study Companion",
    page_icon="🎓",
    layout="wide"
)

# ---------------- GEMINI SETUP (STABLE) ----------------
model = None

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    # Use stable model directly (no auto-detect errors)
    model = genai.GenerativeModel("gemini-1.5-flash")

except Exception as e:
    st.error(f"❌ Gemini Setup Error: {e}")

# ---------------- EXPORT FUNCTIONS ----------------
def get_docx(text):
    doc = Document()
    doc.add_heading("Fikreab AI Notes", 0)

    for line in text.split("\n"):
        doc.add_paragraph(line)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def get_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    safe_text = "".join(i for i in text if ord(i) < 128)

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 10, txt=line)

    return pdf.output(dest="S").encode("latin-1", "ignore")


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("Fikreab AI")

    mode = st.selectbox(
        "Choose Mode",
        [
            "📝 Notes",
            "🗂 Flashcards",
            "📉 Summary",
            "🎯 Exam Questions"
        ]
    )

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")


# ---------------- HEADER ----------------
st.title("🎓 Fikreab AI Studio")

# ---------------- PROCESS FILE ----------------
text_content = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)

    text_content = "".join(
        [page.extract_text() or "" for page in reader.pages]
    )[:30000]


# ---------------- MAIN ----------------
if uploaded_file:

    if st.button("✨ Generate"):

        if not model:
            st.error("Model not loaded")
        else:

            prompts = {
                "📝 Notes":
                    "Create detailed study notes with headings.",

                "🗂 Flashcards":
                    "Create flashcards: Front / Back format.",

                "📉 Summary":
                    "Summarize into key bullet points.",

                "🎯 Exam Questions":
                    "Create 5 exam questions with answers."
            }

            with st.spinner("Generating..."):
                try:
                    response = model.generate_content(
                        prompts[mode] + "\n\n" + text_content
                    )

                    st.session_state.output = response.text

                except Exception as e:
                    st.error(f"Error: {e}")

    if "output" in st.session_state:

        st.write(st.session_state.output)

        col1, col2 = st.columns(2)
