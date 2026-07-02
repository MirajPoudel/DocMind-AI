"""
==========================================================
File: chunker.py

Purpose:
--------
This file is responsible for splitting large documents
into smaller, meaningful chunks for embeddings and retrieval.

Key features:
- Token/character-based chunking
- Overlap between chunks (to preserve context)
- Clean metadata tracking
- Debug-friendly output (viewable in Streamlit UI)

Output:
-------
A list of chunks with metadata:
[
    {
        "chunk_id": 1,
        "text": "...",
        "start": 0,
        "end": 500
    }
]

Author: DocMind AI Project
==========================================================
"""

from config import CHUNK_SIZE, CHUNK_OVERLAP


# ==========================================================
# MAIN CHUNKING FUNCTION
# ==========================================================

def chunk_text(text: str) -> list:
    """
    Split text into overlapping chunks.

    Args:
        text (str): Full document text

    Returns:
        list: List of chunk dictionaries
    """

    if not text:
        return []

    chunks = []
    start = 0
    chunk_id = 0
    text_length = len(text)

    while start < text_length:
        end = start + CHUNK_SIZE

        chunk = text[start:end]

        # Clean whitespace
        chunk = chunk.strip()

        if chunk:
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk,
                "start": start,
                "end": end
            })

            chunk_id += 1

        # Move window with overlap
        start = end - CHUNK_OVERLAP

        # Safety check to avoid infinite loops
        if start < 0:
            start = 0

    return chunks


# ==========================================================
# OPTIONAL UTILITY FUNCTION
# ==========================================================

def get_chunk_texts(chunks: list) -> list:
    """
    Extract only text from chunk objects.
    Useful for embedding models.
    """
    return [chunk["text"] for chunk in chunks]