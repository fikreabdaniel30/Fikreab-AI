"""
Fikreab AI | Study Companion
A Streamlit app that turns uploaded PDFs into notes, flashcards,
summaries, or exam questions using Google Gemini 1.5 Flash.
"""

import streamlit as st
import google.generativeai as genai

from core import (
    MODES,
    PDFExtractionError,
    extract_text,
    generate_study_material,
    get_docx,
    get_pdf,
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Fikreab AI | Study Companion",
    page_icon="🎓",
    layout="wide",
)

# ------------------ GEMINI SETUP ------------------
@st.cache_resource
def load_model():
    """Configure Gemini and return the model instance, or None on failure."""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(MODEL_NAME)
    except Exception as exc:
        st.error(f"❌ Gemini setup error: {exc}")
        return None


model = load_model()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🎓 Fikreab AI")
    st.caption("Turn any PDF into study material.")

    mode = st.selectbox("Choose Mode", list(MODES.keys()))
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# ---------------- HEADER ----------------
st.title("🎓 Fikreab AI Studio")

# Reset stale output if a new file is uploaded
if uploaded_file and st.session_state.get("last_file_name") != uploaded_file.name:
    st.session_state.pop("output", None)
    st.session_state["last_file_name"] = uploaded_file.name

# ---------------- EXTRACT TEXT ----------------
text_content = ""
extraction_error = None

if uploaded_file:
    try:
        text_content = extract_text(uploaded_file)
    except PDFExtractionError as exc:
        extraction_error = str(exc)

# ---------------- MAIN ----------------
if uploaded_file:
    if extraction_error:
        st.error(f"❌ {extraction_error}")
    elif not text_content.strip():
        st.warning(
            "⚠️ No readable text found in this PDF. "
            "It may be scanned/image-based — try a text-based PDF instead."
        )
    else:
else:
        st.success(f"Extracted {len(text_content):,} characters. Ready to generate.")

        if st.button("✨ Generate"):
            with st.spinner("Generating with Gemini..."):
                try:
                    selected_instructions = MODES[mode]
                    full_prompt = f"{selected_instructions}\n\nDocument Content:\n{text_content}"
                    api_key = st.secrets["GEMINI_API_KEY"]
                    
                    output_text, model_used = generate_study_material(full_prompt, api_key)
                    
                    st.session_state.output = output_text
                    st.session_state.output_mode = mode
                    st.success(f"Generated successfully using {model_used}!")
                except Exception as exc:
                    st.error(f"❌ {exc}")
    if "output" in st.session_state:
        st.markdown("---")
        st.subheader(f"Result — {st.session_state.get('output_mode', '')}")
        st.markdown(st.session_state.output)

        docx_buffer = get_docx(st.session_state.output)
        pdf_bytes = get_pdf(st.session_state.output)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Download as DOCX",
                data=docx_buffer,
                file_name="fikreab_ai_output.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="download_docx",
            )
        with col2:
            st.download_button(
                label="⬇️ Download as PDF",
                data=pdf_bytes,
                file_name="fikreab_ai_output.pdf",
                mime="application/pdf",
                key="download_pdf",
            )
else:
    st.info("👈 Upload a PDF from the sidebar to get started.")
