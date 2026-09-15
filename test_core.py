"""
Basic unit tests for core.py.
Run with: pytest tests/

Note: requires `pip install pytest PyPDF2 fpdf2 python-docx` locally —
these weren't installable in the sandbox that generated this file
(no internet access), so run this yourself before trusting it fully.
"""

import sys
import os
from io import BytesIO
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core import get_docx, get_pdf, generate_content, GenerationError, MODES


def test_get_docx_returns_buffer_with_content():
    buffer = get_docx("# Heading\nSome text here.")
    assert buffer.getbuffer().nbytes > 0


def test_get_docx_handles_empty_text():
    buffer = get_docx("")
    assert buffer.getbuffer().nbytes > 0  # still produces a valid empty doc


def test_get_pdf_returns_bytes():
    result = get_pdf("Some plain text content.")
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_get_pdf_strips_non_latin_without_font():
    # Should not raise even with unsupported characters (falls back gracefully)
    result = get_pdf("Hello 世界")
    assert isinstance(result, bytes)


def test_generate_content_success():
    mock_model = MagicMock()
    mock_model.generate_content.return_value = MagicMock(text="Generated output")

    result = generate_content(mock_model, "📝 Notes", "some source text")
    assert result == "Generated output"
    assert mock_model.generate_content.call_count == 1


def test_generate_content_retries_then_succeeds():
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = [
        Exception("rate limited"),
        MagicMock(text="Generated on retry"),
    ]

    result = generate_content(mock_model, "📉 Summary", "text", max_retries=3)
    assert result == "Generated on retry"
    assert mock_model.generate_content.call_count == 2


def test_generate_content_raises_after_max_retries():
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("persistent failure")

    with pytest.raises(GenerationError):
        generate_content(mock_model, "🎯 Exam Questions", "text", max_retries=2)

    assert mock_model.generate_content.call_count == 2


def test_all_modes_have_prompts():
    for mode_key in MODES:
        assert isinstance(MODES[mode_key], str)
        assert len(MODES[mode_key]) > 0
