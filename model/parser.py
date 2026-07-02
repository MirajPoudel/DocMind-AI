"""
==========================================================
File: parser.py

Purpose:
--------
This file is responsible for parsing uploaded documents
into clean raw text.

Supported formats:
- PDF:
    • First tries LlamaParse (if API key is available)
    • Falls back to PyMuPDF if LlamaParse fails

- Markdown (.md):
    • Reads file directly as text

- JSON (.json):
    • Converts structured JSON into readable text format

Output:
-------
Returns a single clean string that will be passed to:
→ chunker.py

Author: DocMind AI Project
==========================================================
"""

import json
from pathlib import Path

import fitz  # PyMuPDF

from config import LLAMAPARSE_API_KEY

# Optional LlamaParse import (safe fallback)
try:
    from llama_parse import LlamaParse
    LLAMA_AVAILABLE = True
except Exception:
    LLAMA_AVAILABLE = False


# ==========================================================
# MAIN PARSER FUNCTION
# ==========================================================

def parse_file(file_path: Path) -> str:
    """
    Detect file type and parse accordingly.
    Returns extracted text.
    """

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return parse_pdf(file_path)

    elif suffix == ".md":
        return parse_markdown(file_path)

    elif suffix == ".json":
        return parse_json(file_path)

    else:
        raise ValueError(f"Unsupported file type: {suffix}")


# ==========================================================
# PDF PARSING
# ==========================================================

def parse_pdf(file_path: Path) -> str:
    """
    Parse PDF using LlamaParse first, fallback to PyMuPDF.
    """

    # -----------------------------
    # Try LlamaParse (best quality)
    # -----------------------------
    if LLAMA_AVAILABLE and LLAMAPARSE_API_KEY:
        try:
            parser = LlamaParse(api_key=LLAMAPARSE_API_KEY)

            documents = parser.load_data(str(file_path))

            text = "\n\n".join([doc.text for doc in documents])

            if text.strip():
                return text

        except Exception as e:
            print(f"[LlamaParse failed, using fallback] {e}")

    # -----------------------------
    # Fallback: PyMuPDF
    # -----------------------------
    text = ""

    try:
        doc = fitz.open(file_path)

        for page in doc:
            text += page.get_text("text") + "\n"

    except Exception as e:
        print(f"[PDF parsing error] {e}")

    return text.strip()


# ==========================================================
# MARKDOWN PARSING
# ==========================================================

def parse_markdown(file_path: Path) -> str:
    """
    Read markdown file directly.
    """
    return file_path.read_text(encoding="utf-8")


# ==========================================================
# JSON PARSING
# ==========================================================

def parse_json(file_path: Path) -> str:
    """
    Convert JSON into readable text format.
    """

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as e:
        return f"Invalid JSON file: {e}"

    def flatten(obj, prefix=""):
        text = ""

        if isinstance(obj, dict):
            for k, v in obj.items():
                text += flatten(v, prefix + f"{k}.")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                text += flatten(item, prefix + f"[{i}].")
        else:
            text += f"{prefix}: {str(obj)}\n"

        return text

    return flatten(data)