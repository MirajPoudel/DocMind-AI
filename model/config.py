"""
==========================================================
File: config.py

Purpose:
--------
This file handles all global configuration settings for the
DocMind AI system.

It includes:
- Loading environment variables
- API keys (Gemini, LlamaParse if used)
- Model configurations
- Embedding model settings
- Paths for storage directories
- ChromaDB configuration

This ensures that all modules share a single source of truth
for configuration values.

Author: DocMind AI Project
==========================================================
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# API KEYS
# -----------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLAMAPARSE_API_KEY = os.getenv("LLAMAPARSE_API_KEY")

# -----------------------------
# MODEL CONFIGURATION
# -----------------------------
GEMINI_MODEL = "gemini-2.5-flash"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# -----------------------------
# CHROMA DB CONFIG
# -----------------------------
CHROMA_DB_PATH = Path("data/chromadb")

# -----------------------------
# STORAGE PATHS
# -----------------------------
UPLOAD_DIR = Path("uploads")
PARSED_DIR = Path("data/parsed")
CHUNKS_DIR = Path("data/chunks")
HISTORY_FILE = Path("data/history.json")

# Ensure directories exist
for path in [UPLOAD_DIR, PARSED_DIR, CHUNKS_DIR, CHROMA_DB_PATH]:
    path.mkdir(parents=True, exist_ok=True)

# -----------------------------
# CHUNKING CONFIGURATION
# -----------------------------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# -----------------------------
# RETRIEVAL CONFIGURATION
# -----------------------------
TOP_K = 5

# -----------------------------
# STREAMLIT CONFIG
# -----------------------------
APP_TITLE = "DocMind AI"
APP_ICON = "📚"

# Dark theme hint (used in UI)
STREAMLIT_THEME = {
    "base": "dark"
}

# -----------------------------
# VALIDATION
# -----------------------------
if not GOOGLE_API_KEY:
    print("⚠️ WARNING: GOOGLE_API_KEY is missing in .env")

if not LLAMAPARSE_API_KEY:
    print("⚠️ WARNING: LLAMAPARSE_API_KEY is missing in .env")