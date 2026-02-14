import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from io import BytesIO
import time

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(
    page_title="Fikreab AI | The 10/10 Study Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LUXURY UI CUSTOMIZATION (CSS) ---
st.markdown("""
    <style>
    /* Dark Theme Base */
    .stApp {
        background: radial-gradient(circle at top left, #1a1c22, #07080a);
        color: #e0e0e0;
    }
    
    /* Modern Premium Header */
    .premium-header {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 20px 40px rgba(0, 242, 254, 0.15);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .premium-header h1 {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Sidebar Aesthetics */
    [data-testid="stSidebar"] {
        background-color: #0a0b0e;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        color: #000 !important;
        font-weight: 700;
        border: none;
        border-radius: 14px;
        height: 3.8rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.4);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC & EXPORTS ---
def get_docx(text):
    doc = Document()
    doc.add_heading('Fikreab AI | Professional Study Notes', 0)
    clean_text = text.replace('**', '').replace('#', '')
    for p in clean_text.split('\n'):
        if p.strip(): doc.add_paragraph(p)
    buf = BytesIO(); doc.save(buf); buf.seek(0)
    return buf

def get_pdf(text):
    pdf = FPDF()
    pdf.add_page(); pdf.set_font("Arial", size=12)
    # Filter for standard characters to avoid FPDF errors
    safe_text = "".join(i for i in text if ord(i) < 128).replace('**', '').replace('#', '')
    for line in safe_text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    return pdf.output(dest='S').encode('latin-1')

# --- 4. AI CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 5. SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=90)
    st.markdown("## **Fikreab Intelligence**")
    st.caption("Advanced Academic Engine v3.0")
    st.markdown("---")
    
    st.subheader("🛠️ Intelligence Modes")
    mode = st.selectbox(
        "Choose AI Objective:",
        ["📝 Detailed Study Guide", "🗂️ Interactive Flashcards", "🎯 Exam Predictions", "📉 Executive Summary"]
    )
    
    st.markdown("---")
    uploaded_file = st.file_uploader("📂 Drop your PDF here", type="pdf")
    if uploaded_file:
        st.success("✅ Document Ready for Analysis")
    
    st.markdown("---")
    st.info("💡 Tip: Use 'Exam Predictions' to find hidden patterns in your study material.")

# --- 6. MAIN INTERFACE ---
st.markdown("""
    <div class="premium-header">
        <h1>💎 FIKREAB AI STUDIO</h1>
        <p style="color: rgba(0,0,0,0.7); font-weight: 500;">TRANSFORMING DOCUMENTS INTO MASTERY</p>
    </div>
    """, unsafe_allow_html=True)

if uploaded_file:
    # Text Extraction with UX Status
    with st.status("🧬 Scanning Document Neurons...", expanded=False) as status:
        reader = PdfReader(uploaded_file)
        text_content = "".join([page.extract_text() for page in reader.pages])
        status.update(label="✅ Knowledge Base Synchronized", state="complete")

    tab1, tab2 = st.tabs(["🚀 Study Generator", "🧠 Quiz Engine"])

    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"### 📍 Mode: \n**{mode}**")
            st.write("Click below to start the AI synthesis engine.")
            gen_btn = st.button("✨ GENERATE CONTENT")
            
        with c2:
            if gen_btn:
                with st.spinner("🤖 AI is thinking... drafting your success."):
                    prompts = {
                        "📝 Detailed Study Guide": "Create comprehensive notes with headers and clear explanations.",
                        "🗂️ Interactive Flashcards": "Create a list of Key Concept: Definition.",
                        "🎯 Exam Predictions": "Identify 5 likely exam questions based on this text.",
                        "📉 Executive Summary": "Summarize the entire document into 5 high-impact points."
                    }
                    try:
                        response = model.generate_content(f"{prompts[mode]} Content: {text_content[:30000]}")
                        st.session_state['main_output'] = response.text
                        st.toast("Intelligence Generated!", icon="💎")
                    except Exception as e:
                        st.error(f"Engine Error: {e}")

            if 'main_output' in st.session_state:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown(st.session_state['main_output'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download Suite
                st.subheader("📥 Professional Exports")
                d1, d2 = st.columns(2)
                with d1:
                    st.download_button("📕 Download PDF", get_pdf(st.session_state['main_output']), "Fikreab_Study.pdf", "application/pdf")
                with d2:
                    st.download_button("📄 Download Word", get_docx(st.session_state['main_output']), "Fikreab_Study.docx")

    with tab2:
        st.markdown("### 🧠 Practice Quiz")
        st.write("Generate a customized quiz to test your memory retention.")
        if st.button("🎯 GENERATE QUIZ"):
            with st.spinner("⏳ Analyzing document for tricky questions..."):
                q_resp = model.generate_content(f"Create a 5 question quiz with answers for: {text_content[:20000]}")
                st.session_state['quiz_data'] = q_resp.text
        
        if 'quiz_data' in st.session_state:
            st.markdown(f'<div class="glass-card">{st.session_state["quiz_data"]}</div>', unsafe_allow_html=True)

else:
    # 10/10 Empty State Design
    st.markdown("""
    <div style='text-align: center; padding: 100px 20px;'>
        <h2 style='color: #4facfe; font-size: 2.5rem;'>Your 10/10 Journey Starts Here</h2>
        <p style='font-size: 1.2rem; opacity: 0.7;'>Upload a PDF in the left sidebar to unlock AI-powered study modes.</p>
        <div style='font-size: 6rem; margin-top: 20px;'>⚡</div>
    </div>
    """, unsafe_allow_html=True)

