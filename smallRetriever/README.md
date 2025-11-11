🧠 PDF Legal Chatbot

A simple prototype that allows you to chat with your legal case PDFs.
This is an early version aimed at building a larger legal document understanding system.

🚀 Overview

Upload a legal PDF

Automatically embed and index it for retrieval

Ask natural-language questions and get context-based answers

🧩 Tech Stack

Backend: FastAPI

Embeddings: Jina AI Embeddings

Vector Store: ChromaDB

Retrieval: BM25 + Vector search (Ensemble Retriever)

Frontend: Simple HTML + JS interface

LLM: Gemini 2.0-flash

⚙️ How It Works

Upload PDF → The PDF is split into chunks and embedded using Jina API.

Indexing → Data is stored in ChromaDB and cached for faster retrieval.

Query → User inputs a question, which is answered using combined retrieval from BM25 + vector search and an LLM response.

📂 Project Structure
├── fastserverRag.py               # FastAPI backend  
├── uploads/             # Uploaded PDFs  
├── vectorstore/         # ChromaDB storage  
├── bm25_retriever.pkl   # Cached BM25 index  
└── README.md

🧰 Setup
pip install fastapi uvicorn chromadb jina langchain_google_genai langchain
uvicorn app:app --reload

💡 Future Scope

Multi-PDF retrieval

Better UI/UX with persistent chat

Fine-tuned legal LLMs for improved accuracy

🧑‍💻 Authors

Built by Mawiya Manzar, Irfan Zaki — exploring applied AI in legal tech.

<img width="1844" height="773" alt="image" src="https://github.com/user-attachments/assets/82ad745d-5929-4ef0-9dbc-801176f7c73b" />
