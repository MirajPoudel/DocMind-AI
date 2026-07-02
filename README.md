# 📚 DocMind AI

A **multi-format AI document assistant** powered by **Retrieval-Augmented Generation (RAG)**.  
Upload PDFs, Markdown, or JSON files and chat with your documents using **Google Gemini AI + ChromaDB vector search**.

---

## 🚀 Features

- 📄 Supports multiple formats:
  - PDF (LlamaParse + PyMuPDF fallback)
  - Markdown (.md)
  - JSON (.json)

- ✂️ Intelligent text chunking with overlap
- 🧠 Embedding-based semantic search (SentenceTransformers)
- 🗄️ Persistent vector database (ChromaDB)
- 💬 Chat with your documents (RAG pipeline)
- 🔍 View retrieved chunks used for answering
- 📑 Inspect parsed documents and chunks
- 💾 Persistent chat history
- 🌙 Dark-themed Streamlit UI
- 📂 Sidebar navigation with document controls

---

## 🧠 Tech Stack

- Python 🐍
- Streamlit 🎈
- Google Gemini 2.5 Flash 🤖
- ChromaDB 🗄️
- SentenceTransformers 🔎
- PyMuPDF 📄
- LlamaParse 📑
- dotenv 🔐

---

# 🚀 Run Locally

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install streamlit python-dotenv PyMuPDF google-generativeai
streamlit run model/app.py
