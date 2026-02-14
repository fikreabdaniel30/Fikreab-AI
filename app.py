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

# --- CUSTOM CSS (DESIGN UPGRADE) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Glassmorphism Card Style */
    .css-card {
        border-radius: 15px;
        padding: 25px;
        background-color: rgba(30, 33, 39, 0.7);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Section Boxes */
    .section-box {
        border-left: 5px solid #00e5ff;
        padding-left: 15px;
        margin: 20px 0;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #00e5ff !important;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000 !important;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 201, 255, 0.5);
    }

    /* Sidebar aesthetics */
    [data-testid="stSidebar"] {
        background-color: #0a0c10;
        border-right: 1px solid #30333d;
    }
    
    /* Status indicators */
    .status-text {
        font-size: 0.9rem;
        color: #92FE9D;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def get_pdf(text):
    """Converts markdown text to a PDF while handling special characters safely."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 1. Remove Markdown symbols that look messy in a plain PDF
    clean_text = text.replace('**', '').replace('#', '').replace('___', '')
    
    # 2. IMPORTANT: Filter out Emojis/Special chars that crash FPDF
    # This keeps only standard keyboard characters
    safe_text = "".join(i for i in clean_text if ord(i) < 128)
    
    # 3. Write to PDF
    for line in safe_text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    
    # 4. Return as bytes
    return pdf.output(dest='S').encode('latin-1', 'ignore')
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def get_pdf(text):
    """Converts markdown text to a basic PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Remove emojis and MD for basic PDF compatibility
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    
    pdf.multi_cell(0, 10, txt=clean_text)
    
    return pdf.output(dest='S').encode('latin-1')

# --- AI SETUP ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ API Key not found. Please check your secrets.toml.")
except Exception as e:
    st.error(f"Configuration Error: {e}")

# Stable Gemini 1.5 Model
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SESSION STATE ---
if 'generated_notes' not in st.session_state:
    st.session_state['generated_notes'] = ""
if 'generated_quiz' not in st.session_state:
    st.session_state['generated_quiz'] = ""

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("Fikreab AI")
    st.caption("v2.0 | Advanced Learning Engine")
    st.markdown("---")
    
    st.subheader("🛠️ Customization")
    note_type = st.radio(
        "Output Style:",
        ("📝 Exam Notes", "⚡ Short Notes", "📚 Detailed Notes"),
        help="Exam: High-yield | Short: Quick scan | Detailed: Deep dive"
    )
    
    st.markdown("---")
    st.subheader("📂 Source Material")
    uploaded_file = st.file_uploader("Upload Study PDF", type="pdf")
    
    if uploaded_file:
        st.success("✅ Document Ready")
    
    st.markdown("---")
    st.info("💡 **Pro Tip:** For technical subjects, use 'Detailed Notes' to ensure formulas are captured.")

# --- MAIN PAGE ---

# Custom Logo Header
col_header1, col_header2 = st.columns([1, 5])
with col_header1:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
with col_header2:
    st.title("Fikreab AI Studio")
    st.markdown("<p style='font-size:1.2rem; opacity:0.8;'>Precision AI for the modern student.</p>", unsafe_allow_html=True)

st.markdown("---")

if uploaded_file:
    # 1. Text Extraction with Progress
    with st.status("🛠️ Processing PDF...", expanded=False) as status:
        st.write("Extracting text from pages...")
        reader = PdfReader(uploaded_file)
        text_content = ""
        for i, page in enumerate(reader.pages):
            text_content += page.extract_text()
        st.write(f"Analyzing {len(reader.pages)} pages of content...")
        status.update(label="✅ Extraction Complete", state="complete")

    if text_content:
        tab1, tab2 = st.tabs(["📄 Structured Notes", "🧠 Quiz Engine"])

        # --- TAB 1: NOTES ---
        with tab1:
            st.markdown(f"### {note_type}")
            
            if st.button("✨ Generate Study Guide", key="btn_notes"):
                with st.spinner("🤖 AI is synthesizing your notes... this takes about 10 seconds."):
                    # Specific instructions for better formatting
                    instructions = {
                        "📝 Exam Notes": "High-yield summary, key dates, formulas, and 3 possible exam questions.",
                        "⚡ Short Notes": "Bullet points only, bold keywords, maximum 1 page equivalent.",
                        "📚 Detailed Notes": "Full explanations, hierarchical headers, and a summary conclusion."
                    }
                    
                    prompt = f"""
                    SYSTEM: {instructions[note_type]}
                    TASK: Create notes from the text below. Use Markdown, emojis, and clear headers.
                    CONTENT: {text_content[:40000]}
                    """
                    
                    try:
                        response = model.generate_content(prompt)
                        st.session_state['generated_notes'] = response.text
                        st.toast("Notes generated successfully!", icon="✅")
                    except Exception as e:
                        st.error(f"API Error: {e}")

            if st.session_state['generated_notes']:
                # UI Card for Notes
                st.markdown("<div class='css-card'>", unsafe_allow_html=True)
                st.markdown(st.session_state['generated_notes'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                # --- DOWNLOAD SECTION ---
                st.markdown("### 📥 Export Your Learning")
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    docx_data = get_docx(st.session_state['generated_notes'])
                    st.download_button(
                        label="📄 Word (.docx)",
                        data=docx_data,
                        file_name="Fikreab_Study_Notes.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                with c2:
                    pdf_data = get_pdf(st.session_state['generated_notes'])
                    st.download_button(
                        label="📕 PDF (.pdf)",
                        data=pdf_data,
                        file_name="Fikreab_Study_Notes.pdf",
                        mime="application/pdf"
                    )
                with c3:
                    st.download_button(
                        label="🗒️ Text (.txt)",
                        data=st.session_state['generated_notes'],
                        file_name="Fikreab_Notes.txt",
                        mime="text/plain"
                    )

        # --- TAB 2: QUIZ ---
        with tab2:
            st.markdown("### 🧠 Knowledge Check")
            if st.button("❓ Create Interactive Quiz", key="btn_quiz"):
                with st.spinner("🎯 Analyzing key concepts for questions..."):
                    prompt = f"Create 5 multiple choice questions based on this text. Format: Q1, then options A,B,C,D, then the answer hidden in an expander. Text: {text_content[:30000]}"
                    response = model.generate_content(prompt)
                    st.session_state['generated_quiz'] = response.text

            if st.session_state['generated_quiz']:
                st.markdown("<div class='css-card'>", unsafe_allow_html=True)
                st.markdown(st.session_state['generated_quiz'])
                st.markdown("</div>", unsafe_allow_html=True)

else:
    # Beautiful Empty State
    st.markdown("""
    <div style='text-align: center; padding: 100px 20px;'>
        <h2 style='font-size: 2.5rem;'>🚀 Ready to dominate your exams?</h2>
        <p style='font-size: 1.2rem; color: #888;'>Upload your lecture PDF in the sidebar to generate custom notes instantly.</p>
        <div style='margin-top: 20px; color: #00e5ff;'>Upload PDF → Choose Style → Study Better</div>
    </div>
    """, unsafe_allow_html=True)

