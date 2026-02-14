import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from io import BytesIO
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Fikreab AI | Ultimate Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED CUSTOM CSS (10/10 DESIGN) ---
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

# --- EXPORT LOGIC ---
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
    return pdf.output(dest='S').encode('latin-1')

# --- AI CONFIG ---
if "GEMINI_API_KEY" in st.secrets:
    # .strip() removes any accidental spaces you might have pasted
    api_key = st.secrets["GEMINI_API_KEY"].strip() 
    genai.configure(api_key=api_key)
    
    # Try the most stable model name
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Model Error: {e}")
else:
    st.error("❌ GEMINI_API_KEY not found in Streamlit Secrets!")

# --- SIDEBAR & MODES ---
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

# --- MAIN INTERFACE ---
st.markdown('<div class="header-banner"><h1>🎓 FIKREAB AI STUDIO</h1><p style="color:black;">Advanced Academic Intelligence</p></div>', unsafe_allow_html=True)

if uploaded_file:
    # PDF Processing
    with st.status("🛠️ Analyzing Document...", expanded=False) as status:
        reader = PdfReader(uploaded_file)
        text_content = "".join([page.extract_text() for page in reader.pages])
        status.update(label="✅ Knowledge Base Ready", state="complete")

    tab1, tab2 = st.tabs(["🚀 Study Generator", "🧠 Interactive Quiz"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"### 📍 Current Mode: \n**{ai_mode}**")
            generate_btn = st.button("✨ START GENERATION")
        
        with col2:
            if generate_btn:
                # Speed Feedback Loop
                with st.spinner(f"⏳ Generating {ai_mode}... please wait."):
                    prompts = {
                        "📝 Comprehensive Notes": "Create structured study notes with headers, tables, and explanations.",
                        "🗂️ Flashcard Set": "Create a list of Front: [Term] and Back: [Definition] pairs.",
                        "📉 Key Points Only": "Summarize the text into high-impact bullet points only.",
                        "🎯 Exam Predictions": "Identify the 5 most likely exam topics and write a sample question for each."
                    }
                    
                    try:
                        response = model.generate_content(f"{prompts[ai_mode]} Content: {text_content[:30000]}")
                        st.session_state['output'] = response.text
                        st.toast("Generation Complete!", icon="✅")
                    except Exception as e:
                        st.error(f"API Error: {e}")

            if 'output' in st.session_state:
                st.markdown("<div class='css-card'>", unsafe_allow_html=True)
                st.markdown(st.session_state['output'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Professional Download Section
                st.write("### 📥 Export Options")
                d_col1, d_col2 = st.columns(2)
                with d_col1:
                    st.download_button("📄 Export PDF", get_pdf(st.session_state['output']), "Fikreab_AI_Notes.pdf", "application/pdf")
                with d_col2:
                    st.download_button("📝 Export Word", get_docx(st.session_state['output']), "Fikreab_AI_Notes.docx")

    with tab2:
        st.markdown("### ❓ Quiz Engine")
        if st.button("🎯 Generate Random Quiz"):
            with st.spinner("⏳ Crafting questions..."):
                resp = model.generate_content(f"Create a 5-question multiple choice quiz with answers at the end for: {text_content[:20000]}")
                st.session_state['quiz'] = resp.text
        
        if 'quiz' in st.session_state:
            st.markdown(f"<div class='css-card'>{st.session_state['quiz']}</div>", unsafe_allow_html=True)

else:
    # 10/10 Empty State
    st.markdown("""
    <div style='text-align: center; padding: 60px;'>
        <h2 style='color: #00e5ff;'>Ready to upgrade your grades?</h2>
        <p>Upload your PDF in the sidebar to begin the AI transformation.</p>
        <div style='font-size: 5rem;'>📚</div>
    </div>
    """, unsafe_allow_html=True)

