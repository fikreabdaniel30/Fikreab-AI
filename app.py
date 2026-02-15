import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from io import BytesIO

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Fikreab AI | Ultimate Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e2127, #0e1117); color: #ffffff; }
    .header-banner {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px;
    }
    .header-banner h1 { color: #000 !important; margin: 0; font-weight: 800; font-size: 3rem; }
    .css-card {
        border-radius: 15px; padding: 25px; background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000 !important; font-weight: bold; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. EXPORT HELPERS ---
def get_docx(text):
    doc = Document(); doc.add_heading('Study Notes', 0)
    for p in text.split('\n'):
        if p.strip(): doc.add_paragraph(p)
    buf = BytesIO(); doc.save(buf); buf.seek(0)
    return buf

def get_pdf(text):
    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", size=12)
    for line in text.split('\n'): pdf.multi_cell(0, 10, txt=line.encode('latin-1', 'ignore').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DYNAMIC AI CONFIG (FIXES THE 404 ERROR) ---
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GEMINI_API_KEY"].strip()
        genai.configure(api_key=api_key)
        
        # This fixes the 404 by finding exactly what models your key supports
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_actions]
        
        if available_models:
            # We prefer 'flash' if it exists, otherwise we take the first available model
            best_model = next((m for m in available_models if "flash" in m.lower()), available_models[0])
            model = genai.GenerativeModel(best_model)
            st.sidebar.success(f"🤖 Connected to: {best_model}")
        else:
            st.sidebar.error("Your API key doesn't have access to any Gemini models yet.")
    except Exception as e:
        st.sidebar.error(f"Setup Error: {e}")
else:
    st.sidebar.error("Missing GEMINI_API_KEY in Secrets.")

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🎓 Fikreab AI")
    ai_mode = st.selectbox("Action:", ["📝 Comprehensive Notes", "🗂️ Flashcards", "🎯 Exam Prep"])
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# --- 6. MAIN APP ---
st.markdown('<div class="header-banner"><h1>🎓 FIKREAB AI STUDIO</h1></div>', unsafe_allow_html=True)

if uploaded_file and model:
    reader = PdfReader(uploaded_file)
    text_content = "".join([p.extract_text() for p in reader.pages])[:20000] # Limit for free tier

    if st.button("✨ GENERATE"):
        with st.spinner("Processing..."):
            try:
                response = model.generate_content(f"Mode: {ai_mode}. Content: {text_content}")
                st.session_state['out'] = response.text
            except Exception as e:
                st.error(f"Generation Error: {e}")

    if 'out' in st.session_state:
        st.markdown(f"<div class='css-card'>{st.session_state['out']}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.download_button("📄 PDF", get_pdf(st.session_state['out']), "notes.pdf")
        with col2: st.download_button("📝 Word", get_docx(st.session_state['out']), "notes.docx")
else:
    st.info("Please upload a PDF and ensure your API key is active.")
