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

# --- 2. UNIQUE BRANDING & COLOR IDENTITY (CSS) ---
st.markdown("""
    <style>
    /* Global Brand Identity */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 0% 0%, #111418 0%, #050505 100%);
        color: #f0f0f0;
        font-family: 'Inter', sans-serif;
    }

    /* Premium Header Banner */
    .brand-banner {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
        padding: 50px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0, 210, 255, 0.15);
    }
    .brand-banner h1 {
        font-weight: 800;
        font-size: 3.5rem;
        letter-spacing: -2px;
        color: #ffffff !important;
        margin: 0;
        text-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .brand-banner p {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
        margin-top: 10px;
    }

    /* Glassmorphism Containers */
    .content-card {
        background: rgba(20, 23, 28, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }

    /* Interactive Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white !important;
        font-weight: 800;
        border-radius: 16px;
        height: 4rem;
        border: none;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 210, 255, 0.4);
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #08090b;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Section Icons & Spacing */
    .section-label {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2rem;
        font-weight: 700;
        color: #00d2ff;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def get_docx(text):
    doc = Document()
    doc.add_heading('Fikreab AI | Study Notes', 0)
    clean = text.replace('**', '').replace('#', '')
    for p in clean.split('\n'):
        if p.strip(): doc.add_paragraph(p)
    buf = BytesIO(); doc.save(buf); buf.seek(0)
    return buf

def get_pdf(text):
    """Converts markdown text to a PDF while handling special characters safely."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 1. Remove Markdown symbols
    clean_text = text.replace('**', '').replace('#', '').replace('___', '')
    
    # 2. Filter out Emojis/Special chars that crash FPDF
    safe_text = "".join(i for i in clean_text if ord(i) < 128)
    
    # 3. Write to PDF
    for line in safe_text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    
    # 4. Return as bytes
    return pdf.output(dest='S').encode('latin-1', 'ignore')
# --- 4. AI ENGINE SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 5. SIDEBAR (LOGO & CONFIG) ---
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding-bottom: 20px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' width='80'>
            <h1 style='font-size: 1.5rem; margin-top: 10px;'>FIKREAB <span style='color:#00d2ff;'>AI</span></h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<div class='section-label'>⚙️ Strategy</div>", unsafe_allow_html=True)
    mode = st.selectbox(
        "AI Output Mode:",
        ["📝 Structured Notes", "🗂️ Flashcard Set", "🎯 Exam Predictions", "⚡ Fast Review"]
    )
    
    st.markdown("---")
    st.markdown("<div class='section-label'>📂 Input</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Lecture PDF", type="pdf")
    if uploaded_file:
        st.success("✅ Document Synchronized")

# --- 6. MAIN CONTENT ---
st.markdown("""
    <div class="brand-banner">
        <h1>FIKREAB AI STUDIO</h1>
        <p>The Future of Academic Excellence</p>
    </div>
    """, unsafe_allow_html=True)

if uploaded_file:
    # Status UX Refinement
    with st.status("🔍 Analyzing Document Patterns...", expanded=False) as status:
        reader = PdfReader(uploaded_file)
        text_content = "".join([page.extract_text() for page in reader.pages])
        status.update(label="✨ Analysis Complete", state="complete")

    tab1, tab2 = st.tabs(["🚀 Generation Hub", "🧠 Mastery Quiz"])

    with tab1:
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f"### 📍 Current Objective:\n**{mode}**")
            st.info("The AI will prioritize key concepts, definitions, and logical flow based on your selection.")
            gen_btn = st.button("RUN ENGINE")
        
        with c2:
            if gen_btn:
                with st.spinner("🤖 Processing Intelligence..."):
                    prompts = {
                        "📝 Structured Notes": "Generate high-level academic notes with headers and summaries.",
                        "🗂️ Flashcard Set": "Generate a Term: Definition list for flashcards.",
                        "🎯 Exam Predictions": "Identify high-yield exam topics and provide 5 sample questions.",
                        "⚡ Fast Review": "Create an ultra-concise summary for last-minute revision."
                    }
                    try:
                        response = model.generate_content(f"{prompts[mode]} Content: {text_content[:30000]}")
                        st.session_state['f_output'] = response.text
                        st.toast("Success: Intelligence Generated", icon="⚡")
                    except Exception as e:
                        st.error(f"Error: {e}")

            if 'f_output' in st.session_state:
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown(st.session_state['f_output'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Refined Download Section
                st.markdown("<div class='section-label'>📥 Professional Export</div>", unsafe_allow_html=True)
                dc1, dc2 = st.columns(2)
                with dc1:
                    st.download_button("📕 Export as PDF", get_pdf(st.session_state['f_output']), "Study_Guide.pdf")
                with dc2:
                    st.download_button("📄 Export as DOCX", get_docx(st.session_state['f_output']), "Study_Guide.docx")

    with tab2:
        st.markdown("<div class='section-label'>🧠 Knowledge Check</div>", unsafe_allow_html=True)
        if st.button("🎯 GENERATE ADAPTIVE QUIZ"):
            with st.spinner("⏳ Synthesizing questions..."):
                q_resp = model.generate_content(f"Create a 5 question quiz with answers for: {text_content[:20000]}")
                st.session_state['f_quiz'] = q_resp.text
        
        if 'f_quiz' in st.session_state:
            st.markdown(f'<div class="content-card">{st.session_state["f_quiz"]}</div>', unsafe_allow_html=True)

else:
    # 10/10 Splash State
    st.markdown("""
    <div style='text-align: center; padding: 80px;'>
        <div style='font-size: 5rem; margin-bottom: 20px;'>🎓</div>
        <h2 style='color: #00d2ff;'>Welcome to Fikreab AI Studio</h2>
        <p style='opacity: 0.7;'>Upload a PDF to unlock the ultimate study experience.</p>
    </div>
    """, unsafe_allow_html=True)
