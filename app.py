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

# --- CUSTOM CSS (DESIGN UPGRADE) ---
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Custom Card Style */
    .css-card {
        border-radius: 15px;
        padding: 20px;
        background-color: #1e2127;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        border: 1px solid #30333d;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #00e5ff !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000;
        font-weight: bold;
        border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        color: #000;
    }

    /* Sidebar aesthetics */
    [data-testid="stSidebar"] {
        background-color: #161920;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def get_docx(text):
    """Converts markdown text to a simplified DOCX file in memory."""
    doc = Document()
    doc.add_heading('Fikreab AI Study Notes', 0)
    # Simple cleanup to remove markdown bolding for the doc (optional refinement)
    clean_text = text.replace('**', '').replace('##', '')
    for paragraph in clean_text.split('\n'):
        if paragraph.strip():
            doc.add_paragraph(paragraph)
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- AI SETUP ---
try:
    # Attempt to load from secrets, otherwise ask user
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        # Fallback for local testing without secrets.toml
        st.warning("⚠️ Secret Key not found via secrets.toml.")
except Exception as e:
    st.error(f"Configuration Error: {e}")

# Use a standard stable model
model = genai.GenerativeModel('gemini-2.5-flash')

# --- SESSION STATE MANAGEMENT ---
if 'generated_notes' not in st.session_state:
    st.session_state['generated_notes'] = ""
if 'generated_quiz' not in st.session_state:
    st.session_state['generated_quiz'] = ""

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("Fikreab AI")
    st.markdown("---")
    
    st.subheader("⚙️ Configuration")
    
    # 1. Output Quality Control
    note_type = st.radio(
        "Choose Output Style:",
        ("📝 Exam Notes", "⚡ Short Notes", "📚 Detailed Notes"),
        index=0,
        help="Select how you want your notes structured."
    )
    
    st.markdown("---")
    
    # 2. File Upload
    st.subheader("📂 Upload Material")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file:
        st.success("File Loaded Successfully!")
    
    st.markdown("---")
    st.info("💡 Pro Tip: Use 'Detailed Notes' for first-time learning and 'Exam Notes' for revision.")

# --- MAIN PAGE LAYOUT ---

# Hero Section
st.title("🎓 Fikreab AI Studio")
st.markdown("#### *Transform your PDFs into powerful study guides in seconds.*")
st.markdown("---")

# Main Logic
if uploaded_file:
    # Extract Text
    with st.spinner("⏳ Analyzing document structure..."):
        try:
            reader = PdfReader(uploaded_file)
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text()
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            text_content = ""

    if text_content:
        # Create Tabs for different features
        tab1, tab2 = st.tabs(["📄 Study Notes", "🧠 Interactive Quiz"])

        # --- TAB 1: GENERATE NOTES ---
        with tab1:
            st.markdown(f"### Generate {note_type}")
            
            if st.button("🚀 Generate Notes", key="btn_notes"):
                with st.spinner("🤖 Reading, Understanding, and Writing..."):
                    # Dynamic Prompting based on selection
                    if "Short" in note_type:
                        system_instruction = "Create ultra-concise short notes. Use only bullet points, keywords, and simple definitions. Ignore fluff."
                    elif "Detailed" in note_type:
                        system_instruction = "Create a comprehensive study guide. Explain concepts in depth, provide examples, use analogies, and cover all chapters thoroughly."
                    else: # Exam Notes
                        system_instruction = "Create high-yield Exam Notes. Focus on definitions, formulas, dates, and commonly asked questions. Use bold headers and strict formatting."

                    prompt = f"{system_instruction}\n\nAnalyze this text and format the output using clear Markdown, tables, and emojis:\n{text_content[:40000]}"
                    
                    try:
                        response = model.generate_content(prompt)
                        st.session_state['generated_notes'] = response.text
                    except Exception as e:
                        st.error(f"API Error: {e}")

            # Display Notes Result
            if st.session_state['generated_notes']:
                st.markdown("<div class='css-card'>", unsafe_allow_html=True)
                st.markdown(st.session_state['generated_notes'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Download Options
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        label="📥 Download as Text",
                        data=st.session_state['generated_notes'],
                        file_name="Fikreab_Notes.txt",
                        mime="text/plain"
                    )
                with col_d2:
                    # Generate DOCX in memory
                    docx_file = get_docx(st.session_state['generated_notes'])
                    st.download_button(
                        label="📄 Download as Word (DOCX)",
                        data=docx_file,
                        file_name="Fikreab_Notes.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

        # --- TAB 2: QUIZ MODE ---
        with tab2:
            st.markdown("### 🧠 Test Your Knowledge")
            st.write("Generate a quiz based on the uploaded document to test your retention.")
            
            if st.button("❓ Generate Quiz", key="btn_quiz"):
                with st.spinner("🎯 Crafting tricky questions..."):
                    prompt = f"""
                    Create a quiz from this text. 
                    Format it exactly like this for 5 questions:
                    
                    **Q1:** [Question text]
                    **A:** [Hidden Answer]
                    
                    **Q2:** [Question text]
                    **A:** [Hidden Answer]
                    
                    (Do this for 5 questions)
                    
                    Content: {text_content[:30000]}
                    """
                    try:
                        response = model.generate_content(prompt)
                        st.session_state['generated_quiz'] = response.text
                    except Exception as e:
                        st.error(f"API Error: {e}")

            # Display Quiz Result
            if st.session_state['generated_quiz']:
                st.markdown("<div class='css-card'>", unsafe_allow_html=True)
                
                # Simple logic to make it look like a real quiz (Text splitting)
                # This splits the AI response by "Q" to separate questions visually
                quiz_sections = st.session_state['generated_quiz'].split("**Q")
                
                for section in quiz_sections:
                    if section.strip():
                        # We reconstruct the "Q" that was removed by split
                        st.markdown(f"**Q{section}")
                        st.markdown("---")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                with st.expander("👀 View Answer Key / Full Output"):
                    st.write(st.session_state['generated_quiz'])

else:
    # Empty State (No file uploaded)
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <h2>👋 Welcome to Fikreab AI</h2>
        <p>Please upload a PDF document in the sidebar to begin.</p>
        <p style='font-size: 0.8em; color: gray;'>Supports PDF files up to 200MB</p>
    </div>
    """, unsafe_allow_html=True)



