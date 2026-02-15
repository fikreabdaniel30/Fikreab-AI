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

# --- 2. PREMIUM CSS (ORIGINAL 10/10 DESIGN) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e2127, #0e1117); color: #ffffff; }
    .header-banner {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 201, 255, 0.2);
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
    [data-testid="stSidebar"] { background-color: #0a0c10; border-right: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. EXPORT LOGIC ---
def get_docx(text):
    doc = Document()
    doc.add_heading('Fikreab AI Study Notes', 0)
    clean_text = text.replace('**', '').replace('#', '')
    for paragraph in clean_text.split('\n'):
        if paragraph.strip(): doc.add_paragraph(paragraph)
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

# --- 4. AI CONFIG (FIXED INDENTATION & ATTRIBUTES) ---
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        # .strip() is vital to fix the "API Key Invalid" Error 400 in your screenshots
        api_key = st.secrets["GEMINI_API_KEY"].strip()
        genai.configure(api_key=api_key)
        
        # Simplified model selection to avoid 'supported_actions' attribute error
        # Using gemini-1.5-flash as it is the most stable for free tier
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Setup Error: {e}")
else:
    st.sidebar.error("❌ GEMINI_API_KEY missing in Secrets!")

# --- 5. SIDEBAR & MODES ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("Fikreab AI")
    st.markdown("---")
    ai_mode = st.selectbox("Select Action:", ["📝 Comprehensive Notes", "🗂️ Flashcard Set", "📉 Key Points Only", "🎯 Exam Predictions"])
    uploaded_file = st.file_uploader("Upload PDF Material", type="pdf")

# --- 6. MAIN INTERFACE ---
st.markdown('<div class="header-banner"><h1>🎓 FIKREAB AI STUDIO</h1><p style="color:black;">Advanced Academic Intelligence</p></div>', unsafe_allow_html=True)

if uploaded_file:
    with st.status("🛠️ Analyzing Document...", expanded=False) as status:
        reader = PdfReader(uploaded_file)
        # Limit text to 30k chars to prevent 'Argument too large' errors
        text_content = "".join([page.extract_text() for page in reader.pages])[:30000]
        status.update(label="✅ Knowledge Base Ready", state="complete")

    tab1, tab2 = st.tabs(["🚀 Study Generator", "🧠 Interactive Quiz"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"### 📍 Mode: \n**{ai_mode}**")
            generate_btn = st.button("✨ START GENERATION")
        
        with col2:
            if generate_btn:
                if model:
                    with st.spinner(f"⏳ Generating {ai_mode}..."):
                        prompts = {
                            "📝 Comprehensive Notes": "Create structured study notes with headers and tables.",
                            "🗂️ Flashcard Set": "Create a list of Term: Definition pairs.",
                            "📉 Key Points Only": "Summarize the text into high-impact bullet points.",
                            "🎯 Exam Predictions": "Identify the 5 most likely topics and write a sample question for each."
                        }
                        try:
                            response = model.generate_content(f"{prompts[ai_mode]} Content: {text_content}")
                            st.session_state['output'] = response.text
                            st.toast("Generation Complete!", icon="✅")
                        except Exception as e:
                            st.error(f"API Error: {e}")
                else:
                    st.error("AI not initialized. Check your key.")

            if 'output' in st.session_state:
                st.markdown("<div class='css-card'>", unsafe_allow_html=True)
                st.markdown(st.session_state['output'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.write("### 📥 Export Options")
                d1, d2 = st.columns(2)
                with d1: st.download_button("📄 Export PDF", get_pdf(st.session_state['output']), "Notes.pdf")
                with d2: st.download_button("📝 Export Word", get_docx(st.session_state['output']), "Notes.docx")

    with tab2:
        st.markdown("### ❓ Quiz Engine")
        if st.button("🎯 Generate Random Quiz"):
            if model:
                with st.spinner("⏳ Crafting..."):
                    try:
                        resp = model.generate_content(f"Create a 5-question quiz for: {text_content}")
                        st.session_state['quiz'] = resp.text
                    except Exception as e: st.error(f"Quiz Error: {e}")

        if 'quiz' in st.session_state:
            st.markdown(f"<div class='css-card'>{st.session_state['quiz']}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align: center; padding: 60px;'><h2 style='color: #00e5ff;'>Ready to upgrade?</h2><p>Upload your PDF to begin.</p></div>", unsafe_allow_html=True)
