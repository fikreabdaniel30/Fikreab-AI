import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from io import BytesIO
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Fikreab AI | Ultimate Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CUSTOM CSS (10/10 DESIGN) ---
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: radial-gradient(circle at top right, #1e2127, #0e1117);
        color: #ffffff;
    }
    
    /* Custom Header Banner */
    .header-banner {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 201, 255, 0.2);
    }
    .header-banner h1 {
        color: #000 !important;
        margin: 0;
        font-weight: 800;
        font-size: 3rem;
    }
    
    /* Smart Card Containers */
    .css-card {
        border-radius: 15px;
        padding: 25px;
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .css-card:hover {
        border: 1px solid #00e5ff;
    }
    
    /* Better Button Design */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000 !important;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0a0c10;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. EXPORT LOGIC ---
def get_docx(text):
    doc = Document()
    doc.add_heading('Fikreab AI Study Notes', 0)
    clean_text = text.replace('**', '').replace('#', '')
    for paragraph in clean_text.split('\n'):
        if paragraph.strip():
            doc.add_paragraph(paragraph)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def get_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    safe_text = "".join(i for i in text if ord(i) < 128)
    clean_text = safe_text.replace('**', '').replace('#', '')
    for line in clean_text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 4. AI CONFIG (THE FIXED SECTION) ---
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        # .strip() handles Error 400 caused by accidental spaces in secrets
        api_key = st.secrets["GEMINI_API_KEY"].strip() 
        genai.configure(api_key=api_key)
        
        # Dynamically list and select best available model to fix Error 404
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_actions]
        # In 2026, many accounts use gemini-flash-latest or gemini-2.5-flash
        target_list = ['models/gemini-2.0-flash', 'models/gemini-1.5-flash', 'models/gemini-pro']
        selected = next((m for m in target_list if m in available_models), available_models[0])
        model = genai.GenerativeModel(selected)
    except Exception as e:
        st.error(f"⚠️ Setup Error: {e}")
else:
    st.sidebar.error("❌ GEMINI_API_KEY missing in Secrets!")

# --- 5. SIDEBAR & MODES ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("Fikreab AI")
    st.markdown("---")
    
    st.subheader("🧠 Smart AI Modes")
    ai_mode = st.selectbox(
        "Select Action:",
        ["📝 Comprehensive Notes", "🗂️ Flashcard Set", "📉 Key Points Only", "🎯 Exam Predictions"]
    )
    
    uploaded_file = st.file_uploader("Upload PDF Material", type="pdf")
    if uploaded_file:
        st.success("✅ Document Loaded")

# --- 6. MAIN INTERFACE ---
st.markdown('<div class="header-banner"><h1>🎓 FIKREAB AI STUDIO</h1><p style="color:black;">Advanced Academic Intelligence</p></div>', unsafe_allow_html=True)

if uploaded_file:
    # PDF Processing
    with st.status("🛠️ Analyzing Document...", expanded=False) as status:
        reader = PdfReader(uploaded_file)
        # Limit text to avoid "Argument too large" 400 errors
        text_content = "".join([page.extract_text() for page in reader.pages])[:30000]
        status.update(label="✅ Knowledge Base Ready", state="complete")

    tab1, tab2 = st.tabs(["🚀 Study Generator", "🧠 Interactive Quiz"])

    with tab1
