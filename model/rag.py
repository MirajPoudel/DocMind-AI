"""
==========================================================
File: rag.py

Purpose:
--------
This file implements the Retrieval-Augmented Generation (RAG)
pipeline for DocMind AI.

It is responsible for:
- Taking user queries
- Retrieving relevant chunks from vectorstore
- Building a prompt with context
- Generating answers using Gemini
- Returning both answer + retrieved chunks

This is the "brain reasoning layer" of the system.

Author: DocMind AI Project
==========================================================
"""

import google.generativeai as genai

from config import GOOGLE_API_KEY, GEMINI_MODEL
from vectorstore import search

# -----------------------------
# Configure Gemini
# -----------------------------
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(GEMINI_MODEL)


# ==========================================================
# MAIN RAG FUNCTION
# ==========================================================

def get_answer(query: str):
    """
    Complete RAG pipeline:
    1. Retrieve relevant chunks
    2. Build context
    3. Ask Gemini
    4. Return answer + sources
    """

    # -----------------------------
    # STEP 1: Retrieve chunks
    # -----------------------------
    results = search(query)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return {
            "answer": "I couldn't find relevant information in the documents.",
            "chunks": []
        }

    # -----------------------------
    # STEP 2: Build context
    # -----------------------------
    context = "\n\n".join(
        [f"[Chunk {i+1}]\n{doc}" for i, doc in enumerate(documents)]
    )

    # -----------------------------
    # STEP 3: Prompt engineering
    # -----------------------------
    prompt = f"""
You are an intelligent document assistant.

You MUST answer ONLY using the provided context below.

If the answer is not in the context, say:
"I couldn't find that information in the uploaded documents."

---

CONTEXT:
{context}

---

QUESTION:
{query}

---

Answer clearly and concisely:
"""

    # -----------------------------
    # STEP 4: Generate response
    # -----------------------------
    response = model.generate_content(prompt)

    answer = response.text

    # -----------------------------
    # STEP 5: Format output
    # -----------------------------
    return {
        "answer": answer,
        "chunks": [
            {
                "text": doc,
                "metadata": meta
            }
            for doc, meta in zip(documents, metadatas)
        ]
    }