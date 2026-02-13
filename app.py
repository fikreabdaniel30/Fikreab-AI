import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- PAGE CONFIG & STYLE ---
st.set_page_config(page_title="Fikreab AI", page_icon="🎓", layout="wide")

# Custom CSS for the "Turbo AI" premium dark mode look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextArea>div>div>textarea { background-color: #262730; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- AI SETUP ---
# This uses the secure secret method we discussed
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.warning("⚠️ Secret Key not found. If testing locally, ensure .streamlit/secrets.toml exists.")

# --- APP UI ---
st.title("🎓 Fikreab AI")
st.subheader("The Most Powerful Free Study Tool for Students")

# Initialize memory so results don't vanish on download
if 'result' not in st.session_state:
    st.session_state['result'] = ""

# Sidebar for Uploading
with st.sidebar:
    st.header("📂 Upload Center")
    uploaded_file = st.file_uploader("Upload your Lesson (PDF)", type="pdf")
    st.info("Fikreab AI reads your whole file to create master notes.")

# Main Logic
if uploaded_file:
    reader = PdfReader(uploaded_file)
    text_content = ""
    for page in reader.pages:
        text_content += page.extract_text()
    
    st.success("✅ File analyzed! What should Fikreab AI do?")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📝 Generate Master Notes"):
            with st.spinner("Writing professional notes..."):
                # Using 30,000 chars instead of 15,000 to use more of Gemini's power
                prompt = f"Create high-level study notes from this: {text_content[:30000]}. Use bold headers, bullet points, and a summary table."
                response = model.generate_content(prompt)
                st.session_state['result'] = response.text

    with col2:
        if st.button("❓ Create Exam Quiz"):
            with st.spinner("Generating exam questions..."):
                prompt = f"Create 5 difficult exam questions with answers from this: {text_content[:30000]}."
                response = model.generate_content(prompt)
                st.session_state['result'] = response.text

    # Display Result & Export
    if st.session_state['result']:
        st.markdown("---")
        st.markdown(st.session_state['result'])
        
        st.download_button(
            label="📥 Download as Study Guide",
            data=st.session_state['result'],
            file_name="Fikreab_AI_Notes.txt",
            mime="text/plain"
        )
else:

    st.write("👋 Hello student! Upload a PDF on the left to start generating notes for free.")
