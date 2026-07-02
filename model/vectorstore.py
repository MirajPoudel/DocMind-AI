"""
==========================================================
File: vectorstore.py

Purpose:
--------
This module provides a lightweight in-memory vector store
for DocMind AI.

It exposes the functions expected by the app:
- add_documents(filename, chunks)
- search(query)

The implementation uses simple keyword matching so the app
can run even without a full external vector database.
==========================================================
"""

from __future__ import annotations

from typing import Any, Dict, List


_INDEX: List[Dict[str, Any]] = []


def add_documents(filename: str, chunks: list) -> None:
    """
    Store document chunks in the in-memory index without duplicating
    the same content multiple times.
    """
    seen_texts = {item["text"] for item in _INDEX}

    for chunk in chunks:
        text = chunk.get("text", "")
        if not text or text in seen_texts:
            continue

        _INDEX.append({
            "filename": filename,
            "chunk_id": chunk.get("chunk_id"),
            "text": text,
            "metadata": {
                "start": chunk.get("start"),
                "end": chunk.get("end"),
                "source": filename,
            },
        })
        seen_texts.add(text)


def search(query: str, top_k: int = 5) -> dict:
    """
    Retrieve the most relevant stored chunks using simple
    keyword overlap matching.
    """
    query_terms = {term.lower() for term in query.split() if term}

    if not query_terms:
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

    scored_items = []
    for item in _INDEX:
        text = item["text"].lower()
        score = sum(1 for term in query_terms if term in text)
        if score > 0:
            scored_items.append((score, item))

    scored_items.sort(key=lambda entry: entry[0], reverse=True)
    top_items = scored_items[:top_k]

    documents = [[item["text"] for _, item in top_items]]
    metadatas = [[item["metadata"] for _, item in top_items]]
    distances = [[0.0 for _ in top_items]]

    return {
        "documents": documents,
        "metadatas": metadatas,
        "distances": distances,
    }