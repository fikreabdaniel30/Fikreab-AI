# Unicode font for PDF export

To enable correct rendering of non-Latin scripts (e.g. Amharic) in the
downloadable PDF, place a Unicode TTF font here named `DejaVuSans.ttf`.

Download (free, permissive license):
https://dejavu-fonts.github.io/

If this file is absent, `core.get_pdf()` automatically falls back to
Latin-1-only output (non-Latin characters are stripped) rather than crashing.

For Amharic specifically, "Noto Sans Ethiopic" is a better fit than DejaVu Sans:
https://fonts.google.com/noto/specimen/Noto+Sans+Ethiopic
(rename the downloaded .ttf to DejaVuSans.ttf, or update UNICODE_FONT_PATH in core.py)
