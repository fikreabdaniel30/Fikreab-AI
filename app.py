import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from io import BytesIO
import time

# --- 1. PAGE & HISTORY INITIALIZATION ---
st.set_page_config(page_title="Fikreab AI Studio", page_icon="⚡", layout="wide")

# This creates the "History" storage in your app's memory
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'f_output' not in st.session_state:
    st.session_state['f_output'] = ""

# --- 2. LUXURY UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 0% 0%, #111418 0%, #050505 100%); color: #f0f0f0; }
    .brand-banner { background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; }
    .content-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); }
    .stButton>button { background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white !important; border-radius: 12px; height: 3.5rem; font-weight: bold; }
    .history-item { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 5px; cursor: pointer; border-left: 4px solid #00d2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FIXING EXPORT FUNCTIONS ---
def get_docx(text):
    doc = Document()
    doc.add_heading('Fikreab AI Study Guide', 0)
    for p in text.replace('**', '').split('\n'):
        if p.strip(): doc.add_paragraph(p)
    buf = BytesIO(); doc.save(buf); buf.seek(0)
    return buf

def get_pdf(text):
    pdf = FPDF()
    pdf.add_page(); pdf.set_font("Arial", size=12)
    # The 'ignore' flag prevents the 404/crash on special AI characters
    safe_text = "".join(i for i in text if ord(i) < 128).replace('**', '')
    for line in safe_text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 4. AI SETUP (FIXED MODEL NAME) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # FIXED: Using gemini-2.5-flash as 1.5 versions are often deprecated
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("Missing GEMINI_API_KEY!")

# --- 5. SIDEBAR & HISTORY ---
with st.sidebar:
    st.title("FIKREAB AI")
    mode = st.selectbox("Mode:", ["📝 Notes", "🎯 Exam Prep", "🗂️ Flashcards"])
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    st.markdown("---")
    st.subheader("🕒 History")
    if not st.session_state['history']:
        st.write("No saved sessions.")
    else:
        # Show history items - clicking one restores it
        for i, entry in enumerate(reversed(st.session_state['history'])):
            if st.button(f"{entry['mode']} ({entry['time']})", key=f"hist_{i}"):
                st.session_state['f_output'] = entry['content']

# --- 6. MAIN APP LOGIC ---
st.markdown('<div class="brand-banner"><h1>FIKREAB AI STUDIO</h1></div>', unsafe_allow_html=True)

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text_content = "".join([p.extract_text() for p in reader.pages])

    if st.button("RUN ENGINE"):
        try:
            with st.spinner("🤖 Synthesizing..."):
                response = model.generate_content(f"Generate {mode} for: {text_content[:20000]}")
                st.session_state['f_output'] = response.text
                
                # SAVE TO HISTORY
                st.session_state['history'].append({
                    "mode": mode,
                    "time": time.strftime("%H:%M:%S"),
                    "content": response.text
                })
                st.toast("Success!", icon="✨")
        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state['f_output']:
        st.markdown(f'<div class="content-card">{st.session_state["f_output"]}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.download_button("📕 Download PDF", get_pdf(st.session_state['f_output']), "Study.pdf")
        with c2: st.download_button("📄 Download Word", get_docx(st.session_state['f_output']), "Study.docx")
else:
    st.info("Upload a PDF to start.")
