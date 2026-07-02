"""
==========================================================
File: app.py

Purpose:
--------
This is the main Streamlit application for DocMind AI.

It provides:
- Dark-themed UI
- Left sidebar navigation
- File upload (PDF, Markdown, JSON)
- Tabs for:
    • Parsed Data
    • Chunks
    • Retrieved Chunks
    • Chat Interface

It connects all backend modules:
parser → chunker → vectorstore → rag → storage

This is the user-facing system.

Author: DocMind AI Project
==========================================================
"""

import streamlit as st

from parser import parse_file
from chunker import chunk_text
from vectorstore import add_documents
from rag import get_answer

from storage import (
    save_uploaded_file,
    save_parsed_text,
    save_chunks,
    load_history,
    add_message
)

from config import APP_TITLE, APP_ICON


# ==========================================================
# STREAMLIT CONFIG
# ==========================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme styling (simple override)
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.title("📚 DocMind AI")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF / Markdown / JSON",
    type=["pdf", "md", "json"]
)

if st.sidebar.button("🧹 Clear Chat History"):
    from storage import clear_history
    clear_history()
    st.sidebar.success("History cleared!")

history = load_history()

# ==========================================================
# SESSION STATE
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = history

# ==========================================================
# MAIN TITLE
# ==========================================================
st.title("📚 DocMind AI - RAG Document Assistant")

# ==========================================================
# FILE PROCESSING PIPELINE
# ==========================================================
if uploaded_file:

    # Save file
    file_path = save_uploaded_file(uploaded_file)

    with st.spinner("Parsing document..."):
        text = parse_file(file_path)

    st.success("Document parsed successfully!")

    # Save parsed text
    save_parsed_text(uploaded_file.name, text)

    # Chunking
    with st.spinner("Chunking document..."):
        chunks = chunk_text(text)

    st.success(f"Created {len(chunks)} chunks")

    # Save chunks
    save_chunks(uploaded_file.name, chunks)

    # Embedding + Vector DB
    with st.spinner("Indexing into vector database..."):
        add_documents(uploaded_file.name, chunks)

    st.success("Document indexed successfully!")

    # ======================================================
    # TABS
    # ======================================================
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 Parsed Data", "✂ Chunks", "🔍 Retrieved Chunks", "💬 Chat"]
    )

    # -------------------------
    # TAB 1: Parsed Data
    # -------------------------
    with tab1:
        st.subheader("Parsed Document")
        st.text_area("Content", text, height=400)

    # -------------------------
    # TAB 2: Chunks
    # -------------------------
    with tab2:
        st.subheader("Document Chunks")

        for c in chunks:
            st.markdown(f"### Chunk {c['chunk_id']}")
            st.write(c["text"])
            st.markdown("---")

    # -------------------------
    # TAB 3: Retrieved Chunks
    # -------------------------
    with tab3:
        st.subheader("Test Retrieval")

        query = st.text_input("Enter query to test retrieval")

        if query:
            result = get_answer(query)

            st.markdown("### Answer")
            st.write(result["answer"])

            st.markdown("### Retrieved Chunks")

            for i, chunk in enumerate(result["chunks"]):
                st.markdown(f"**Chunk {i+1}**")
                st.write(chunk["text"])
                st.caption(str(chunk["metadata"]))
                st.markdown("---")

    # -------------------------
    # TAB 4: CHAT
    # -------------------------
    with tab4:
        st.subheader("Chat with Documents")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["message"])

        user_input = st.chat_input("Ask something from your documents...")

        if user_input:

            # Save user message
            st.session_state.messages.append({
                "role": "user",
                "message": user_input
            })

            add_message("user", user_input)

            # Get AI response
            result = get_answer(user_input)

            answer = result["answer"]

            st.session_state.messages.append({
                "role": "assistant",
                "message": answer
            })

            add_message("assistant", answer)

            st.rerun()