import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from io import BytesIO
import time

# --- 1. PRESTIGE CONFIGURATION ---
st.set_page_config(
    page_title="Fikreab AI | Professional Study Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. INITIALIZE SESSION STATE (HISTORY) ---
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'f_output' not in st.session_state:
    st.session_state['f_output'] = ""

# --- 3. UNIQUE BRANDING & LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background: radial-gradient(circle at 0% 0%, #111418 0%, #050505 100%); color: #f0f0f0; font-family: 'Inter', sans-serif; }
    .brand-banner { background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%); padding: 40px 20px; border-radius: 24px; text-align: center; margin-bottom: 30px; box-shadow: 0 20px 50px rgba(0, 210, 255, 0.15); }
    .brand-banner h1 { font-weight: 800; font-size: 3rem; color: #ffffff !important; margin: 0; }
    .content-card { background: rgba(20, 23, 28, 0.6); backdrop-filter: blur(20px); border-radius: 20px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white !important; font-weight: 800; border-radius: 14px; height: 3.5rem; border: none; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0, 210, 255, 0.3); }
    .history-item { padding: 10px; border-radius: 10px; background: rgba(255,255,255,0.05); margin-bottom: 5px; cursor: pointer; border: 1px solid rgba(255,255,255,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HELPER FUNCTIONS ---
def get_docx(text):
    doc = Document()
    doc.add_heading('Fikreab AI | Study Notes', 0)
    clean = text.replace('**', '').replace('#', '')
    for p in clean.split('\n'):
        if p.strip(): doc.add_paragraph(p)
    buf = BytesIO(); doc.save(buf); buf.seek(0)
    return buf

def get_pdf(text):
    pdf = FPDF()
    pdf.add_page(); pdf.set_font("Arial", size=12)
    # The 'ignore' flag prevents crashes on special characters
    safe_text = "".join(i for i in text if ord(i) < 128).replace('**', '').replace('#', '')
    for line in safe_text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 5. AI ENGINE SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# Using the specific full path to avoid 404 errors
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- 6. SIDEBAR (LOGO, CONFIG & HISTORY) ---
with st.sidebar:
    st.markdown("<div style='text-align: center;'><h1 style='color:#00d2ff;'>FIKREAB AI</h1></div>", unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Strategy")
    mode = st.selectbox("AI Output Mode:", ["📝 Structured Notes", "🗂️ Flashcard Set", "🎯 Exam Predictions", "⚡ Fast Review"])
    
    uploaded_file = st.file_uploader("Upload Lecture PDF", type="pdf")
    
    st.markdown("---")
    st.markdown("### 🕒 Session History")
    if st.session_state['history']:
        for i, item in enumerate(reversed(st.session_state['history'])):
            if st.button(f"📄 {item['mode']} - {item['time']}", key=f"hist_{i}"):
                st.session_state['f_output'] = item['content']
    else:
        st.write("No history yet.")
    
    if st.button("🗑️ Clear History"):
        st.session_state['history'] = []
        st.rerun()

# --- 7. MAIN CONTENT ---
st.markdown('<div class="brand-banner"><h1>FIKREAB AI STUDIO</h1><p>The Future of Academic Excellence</p></div>', unsafe_allow_html=True)

if uploaded_file:
    with st.status("🔍 Analyzing PDF Patterns...", expanded=False) as status:
        reader = PdfReader(uploaded_file)
        text_content = "".join([page.extract_text() for page in reader.pages])
        status.update(label="✨ Analysis Complete", state="complete")

    tab1, tab2 = st.tabs(["🚀 Generation Hub", "🧠 Mastery Quiz"])

    with tab1:
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f"### 📍 Objective: **{mode}**")
            gen_btn = st.button("RUN ENGINE")
        
        with c2:
            if gen_btn:
                with st.spinner("🤖 Processing Intelligence..."):
                    prompts = {
                        "📝 Structured Notes": "Provide high-level academic notes with headers.",
                        "🗂️ Flashcard Set": "Create a Term: Definition list.",
                        "🎯 Exam Predictions": "Identify 5 high-yield topics and sample questions.",
                        "⚡ Fast Review": "Create an ultra-concise summary."
                    }
                    try:
                        response = model.generate_content(f"{prompts[mode]} Content: {text_content[:25000]}")
                        # Save to State and History
                        st.session_state['f_output'] = response.text
                        new_entry = {
                            "mode": mode,
                            "time": time.strftime("%H:%M:%S"),
                            "content": response.text
                        }
                        st.session_state['history'].append(new_entry)
                        st.toast("Intelligence Generated!", icon="⚡")
                    except Exception as e:
                        st.error(f"Error: {e}")

            if st.session_state['f_output']:
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown(st.session_state['f_output'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("### 📥 Professional Export")
                dc1, dc2 = st.columns(2)
                with dc1:
                    st.download_button("📕 Export PDF", get_pdf(st.session_state['f_output']), "Study_Guide.pdf")
                with dc2:
                    st.download_button("📄 Export DOCX", get_docx(st.session_state['f_output']), "Study_Guide.docx")

    with tab2:
        st.markdown("### 🧠 Knowledge Check")
        if st.button("🎯 GENERATE QUIZ"):
            q_resp = model.generate_content(f"Create a 5 question quiz for: {text_content[:20000]}")
            st.write(q_resp.text)
else:
    st.info("👋 Welcome! Please upload a PDF in the sidebar to start your session.")
