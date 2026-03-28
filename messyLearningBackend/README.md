# messyLearningBackend — Personal Reference Guide

> **What is this folder?**
> This is your learning sandbox. Nothing here is production code.
> It's where you experimented with LangGraph, RAG, agents, and backends
> while building WakeelSahab. Think of it as your personal lab notebook.

---

## 📁 Folder-by-Folder Breakdown

---

### 🧪 `learning Langraph/` — Your Main Experiment Zone

This is the most important folder here. It contains all the Jupyter notebooks
and scripts you wrote while learning LangGraph and building the AI pipeline.

| File | What it is |
|---|---|
| `chatbot.ipynb` | First experiment — querying a **Pinecone** vector DB with Llama embeddings for legal case search |
| `learnRag.ipynb` | Early RAG experiments (learning how retrieval-augmented generation works) |
| `Langchatbot.ipynb` | Learning LangGraph's `StateGraph` — basic chatbot with message state |
| `loopingAgent.ipynb` | Experimenting with looping/conditional agents in LangGraph |
| `chatbot_memory.py` | A chatbot that has **persistent memory** across conversations |
| `chatbot_with_tools.py` | A chatbot that can call **external tools** (e.g., search, APIs) |
| `React.ipynb` | Building a **ReAct agent** (Reasoning + Acting) — LLM decides when to use tools |
| `rag_AGENT.py` | A full RAG agent script — retrieves docs then answers questions |
| `drafter.ipynb` | First attempt at an **AI document drafter** — human gives feedback in a loop |
| `mawi_drafter.ipynb` | Your personal version of the drafter — same concept, your own tweaks |
| `caseRag.ipynb` | RAG over legal case PDFs — early version |
| `caseRag_final.ipynb` | **Final version** of the case RAG — loads a PDF, embeds it in ChromaDB, answers questions + can search Indian Kanoon API |
| `checkpoint.sqlite` | LangGraph saves conversation checkpoints here (memory persistence storage) |
| `chroma.sqlite3` | Local ChromaDB vector store for this folder |
| `pdf/` | Contains the PDF used in `caseRag_final.ipynb` ("Fundamentals of Building Autonomous LLM") + its embedded ChromaDB vectors |

**→ The most useful file here:** `caseRag_final.ipynb` — this is the most complete experiment, closest to what became the actual product.

---

### 🔍 `smallRetriever/` — The PDF Chatbot Prototype

A working **mini-product** you built: upload a legal PDF, ask questions about it.

This was a real feature prototype — it has its own FastAPI server and frontend.

| File | What it is |
|---|---|
| `fastserverRAG.py` | FastAPI server with `/upload_pdf` and `/ask` endpoints |
| `Rag_chatbot.py` | The RAG logic — embeds PDF, stores in ChromaDB, uses BM25 + vector hybrid search |
| `mychatbot.py` | A simpler standalone chatbot script |
| `uploads/` | Where uploaded PDFs get saved (`Techathon 6 Statements.pdf` is still in here from a past test) |
| `vectorstore/` | ChromaDB storage for embedded PDFs — the indexed data lives here |
| `README.md` | Has a good description of how this mini-product works |

**Tech stack:** FastAPI + Jina embeddings + ChromaDB + BM25 + Gemini 2.0 Flash

**→ Note:** The `smallRetriever` is where the `/upload_pdf` endpoint lives. The current main frontend (`frontend/Wakeel-Sahab/`) calls this endpoint but it's not wired up yet.

---

### 🗂️ `old_backedn/` — The Previous Backend (Before the Clean Version)

The backend that existed before you refactored into `frontend/Wakeel-Sahab/backend/`.

| File | What it is |
|---|---|
| `main.py` | The LangGraph agent — same logic as the current production `main.py` (direct answer + research mode with Indian Kanoon API) |
| `fastserver.py` | The FastAPI server — older version of the current backend |
| `1agent.ipynb` | Notebook version of the agent for quick testing |
| `STREAMING_INTEGRATION.md` | Detailed docs on how to add **streaming (SSE)** to the backend — a `/ask-stream` endpoint that streams tokens in real-time like ChatGPT. Worth reading if you want to implement streaming. |
| `llms-full.txt` | A big text dump of LLM documentation (reference material) |
| `trash/` | Old throwaway files: early `main.py`, `embedding.py`, `index.html`, `legal_cases.json`, CSVs |

**→ The `STREAMING_INTEGRATION.md` is actually useful** — it documents exactly how to add real-time streaming to the `/ask` endpoint. Don't delete it.

---

### 📦 `src/legal_agent/` — Empty Placeholder

Just a folder with an empty `__init__.py`. Was probably intended to become a proper Python package for the agent. Nothing is in it.

---

### 📄 Root-Level Files

| File | What it is |
|---|---|
| `requirements.txt` | Python dependencies (has duplicates — `langchain_google_genai` listed 3 times) |
| `pyproject.toml` | `uv` project config (you used `uv` as your package manager here) |
| `uv.lock` | Lockfile for `uv` — exact pinned versions of all packages |
| `.python-version` | Specifies which Python version `uv` should use |
| `Task.md` | 3-line note to yourself: read wordPlugin wrapper, make a PRD, start building |
| `a.html` | A small HTML test page — probably used to test the backend API manually |
| `cases_with_summary.csv` | Dataset of legal cases with AI-generated summaries (~7.8MB) |
| `cases_with_summaries.csv` | Same as above, slightly different version (~7.8MB) |
| `.gitignore` | Ignores `.venv`, `__pycache__`, `.env`, etc. |
| `.venv/` | Your Python virtual environment (created by `uv`) |

---

## 🗺️ The Learning Journey (Chronological)

Reading the notebooks in order, here's what you were building towards:

```
1. chatbot.ipynb          → "Can I query legal cases from a vector DB?"
2. learnRag.ipynb         → "How does RAG actually work?"
3. Langchatbot.ipynb      → "How do I use LangGraph StateGraph?"
4. loopingAgent.ipynb     → "Can the agent loop and make decisions?"
5. React.ipynb            → "Can the agent decide when to use tools?"
6. chatbot_with_tools.py  → "Full tool-calling chatbot"
7. drafter.ipynb          → "Can AI draft documents with human feedback?"
8. caseRag.ipynb          → "Can I do RAG over case law PDFs?"
9. caseRag_final.ipynb    → "Full pipeline: PDF + Indian Kanoon API + LangGraph"
        ↓
   smallRetriever/        → Turned it into a real FastAPI server
        ↓
   old_backedn/           → Cleaned up into a proper backend
        ↓
   frontend/Wakeel-Sahab/backend/  ← PRODUCTION (not in this folder)
```

---

## ⚠️ Important Notes

- **Do NOT run any of this as production.** It's all experimental.
- The **API keys** (Pinecone, Google Gemini) used in some notebooks may be hardcoded — do not commit those to git.
- The `cases_with_summary.csv` files are large (7.8MB each) — don't add them to git.
- `smallRetriever/` is the most "finished" thing in here — if you ever want the PDF upload feature in the main app, the logic lives there.
