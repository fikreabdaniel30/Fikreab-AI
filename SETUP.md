# Fikreab AI — Setup Guide

## 1. Install Python dependencies
From this folder, run:

```bash
pip install -r requirements.txt
```

## 2. Add your Gemini API key
Get a free key at https://aistudio.google.com/app/apikey, then:

1. Rename `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
2. Open it and replace `your-api-key-here` with your real key

The file should look like this:

```toml
GEMINI_API_KEY = "AIzaSy...your-actual-key"
```

**Do not commit this file to git** — it contains your private key.

## 3. (Optional) Add a Unicode font for Amharic/non-Latin PDF export
See `README.md` for details — drop a `DejaVuSans.ttf` (or renamed Noto Sans
Ethiopic) file into the `fonts/` folder. If you skip this, PDF export still
works but non-Latin characters get stripped.

## 4. Run the app locally
```bash
streamlit run app.py
```

This opens the app in your browser at `http://localhost:8501`.

## 5. (Optional) Deploy it for free on Streamlit Community Cloud
1. Push this folder to a GitHub repo (make sure `.streamlit/secrets.toml`
   is in your `.gitignore` and NOT pushed — only push `secrets.toml.example`)
2. Go to https://share.streamlit.io and connect your repo
3. In the app's **Settings → Secrets**, paste:
   ```toml
   GEMINI_API_KEY = "your-actual-key"
   ```
4. Deploy — Streamlit installs `requirements.txt` automatically

---

## What this app does
Upload a PDF, pick a mode (Notes / Flashcards / Summary / Exam Questions),
and it uses Gemini 1.5 Flash to turn the PDF's text into study material,
downloadable as DOCX or PDF.

## Files
- `app.py` — Streamlit UI
- `core.py` — PDF extraction, Gemini calls, DOCX/PDF export logic
- `test_core.py` — unit tests (run with `pytest test_core.py`)
- `requirements.txt` — Python dependencies
- `README.md` — notes on the optional Unicode font for PDF export
