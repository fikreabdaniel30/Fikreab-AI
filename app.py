import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from io import BytesIO

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Fikreab AI | Ultimate Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (PREMIUM DESIGN) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* Modern Glass Card */
    .css-card {
        border-radius: 15px;
        padding: 25px;
        background-color: rgba(30, 33, 39, 0.7);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3 {
        color: #00e5ff !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000 !important;
        font-weight: bold;
        border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    [data-testid="stSidebar"] {
        background-color: #0a0c10;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def get_docx(text):
    """Generates a clean Word document."""
    doc = Document()
    doc.add_heading('Fikreab AI Study Notes', 0)
    # Strip basic markdown for Word
    clean_text = text.replace('**', '').replace('#', '')
    for paragraph in clean_text.split('\n'):
        if paragraph.strip():
            doc.add_paragraph(paragraph)
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def get_pdf(text):
    """Generates a PDF while stripping emojis to prevent crashes."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # PDF doesn't support emojis/special chars without custom fonts
    # This filter keeps only standard text characters
    safe_text = "".join(i for i in text if ord(i) < 128)
    clean_text = safe_text.replace('**', '').replace('#', '')

    for line in clean_text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    
    return pdf.output(dest='S').encode('latin-1')

# --- AI SETUP ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ Secret Key not found in secrets.toml.")
except Exception as e:
    st.error(f"Config Error: {e}")

model = genai.GenerativeModel('gemini-2.5-flash')

# --- SESSION STATE ---
if 'generated_notes' not in st.session_state:
    st.session_state['generated_notes'] = ""
if 'generated_quiz' not in st.session_state:
    st.session_state['generated_quiz'] = ""

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("Fikreab AI")
    st.markdown("---")
    
    st.subheader("⚙️ Settings")
    note_type = st.radio(
        "Note Style:",
        ("📝 Exam Notes", "⚡ Short Notes", "📚 Detailed Notes")
    )
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload PDF Material", type="pdf")
    if uploaded_file:
        st.success("✅ File Loaded")

# --- MAIN CONTENT ---
st.title("🎓 Fikreab AI Studio")
st.markdown("#### *Your personal AI academic assistant*")
st.markdown("---")

if uploaded_file:
    # Text Extraction
    with st.status("📂 Processing Document...", expanded=False) as status:
        reader = PdfReader(uploaded_file)
        text_content = ""
        for page in reader.pages:
            text_content += page.extract_text()
        status.update(label="✅ Analysis Complete!", state="complete")

    if text_content:
        tab1, tab2 = st.tabs(["📄 Notes", "🧠 Quiz"])

        with tab1:
            if st.button("🚀 Generate Notes"):
                with st.spinner("Writing your study guide..."):
                    prompt = f"Create {note_type} from this text. Use markdown and headers: {text_content[:30000]}"
                    try:
                        response = model.generate_content(prompt)
                        st.session_state['generated_notes'] = response.text
                    except Exception as e:
                        st.error(f"Error: {e}")

            if st.session_state['generated_notes']:
                st.markdown("<div class='css-card'>", unsafe_allow_html=True)
                st.markdown(st.session_state['generated_notes'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                # --- DOWNLOAD BUTTONS ---
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download PDF",
                        data=get_pdf(st.session_state['generated_notes']),
                        file_name="Fikreab_Notes.pdf",
                        mime="application/pdf"
                    )
                with col2:
                    st.download_button(
                        label="📄 Download Word",
                        data=get_docx(st.session_state['generated_notes']),
                        file_name="Fikreab_Notes.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

        with tab2:
            if st.button("❓ Create Quiz"):
                with st.spinner("Creating questions..."):
                    prompt = f"Create 5 questions with answers based on: {text_content[:20000]}"
                    response = model.generate_content(prompt)
                    st.session_state['generated_quiz'] = response.text

            if st.session_state['generated_quiz']:
                st.markdown("<div class='css-card'>", unsafe_allow_html=True)
                st.markdown(st.session_state['generated_quiz'])
                st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("👋 Please upload a PDF in the sidebar to start.")
