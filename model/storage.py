"""
==========================================================
File: storage.py

Purpose:
--------
This file handles persistent storage for the DocMind AI system.

It is responsible for:
- Saving uploaded files
- Saving parsed document text
- Saving chunks for debugging
- Storing and loading chat history
- Managing document metadata

This ensures that even after restarting the app,
the system remembers previous uploads and conversations.

Author: DocMind AI Project
==========================================================
"""

import json
from pathlib import Path
from datetime import datetime

from config import (
    UPLOAD_DIR,
    PARSED_DIR,
    CHUNKS_DIR,
    HISTORY_FILE
)

# -----------------------------
# Ensure history file exists
# -----------------------------
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

if not HISTORY_FILE.exists():
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)


# ==========================================================
# FILE STORAGE
# ==========================================================

def save_uploaded_file(file) -> Path:
    """
    Save uploaded file to disk.
    Returns the saved file path.
    """
    file_path = UPLOAD_DIR / file.name

    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    return file_path


# ==========================================================
# PARSED TEXT STORAGE
# ==========================================================

def save_parsed_text(filename: str, text: str) -> Path:
    """
    Save parsed document text as a .txt file.
    """
    path = PARSED_DIR / f"{filename}.txt"

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path


def load_parsed_text(filename: str) -> str:
    """
    Load parsed document text.
    """
    path = PARSED_DIR / f"{filename}.txt"

    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")


# ==========================================================
# CHUNK STORAGE (for debugging UI)
# ==========================================================

def save_chunks(filename: str, chunks: list) -> Path:
    """
    Save chunks as JSON for inspection.
    """
    path = CHUNKS_DIR / f"{filename}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    return path


def load_chunks(filename: str) -> list:
    """
    Load saved chunks.
    """
    path = CHUNKS_DIR / f"{filename}.json"

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================================
# CHAT HISTORY
# ==========================================================

def load_history() -> list:
    """
    Load chat history from disk.
    """
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history: list):
    """
    Save chat history to disk.
    """
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def add_message(role: str, message: str):
    """
    Add a single chat message to history.
    """
    history = load_history()

    history.append({
        "role": role,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })

    save_history(history)


def clear_history():
    """
    Clear all chat history.
    """
    save_history([])