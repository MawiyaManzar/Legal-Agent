# WakeelSahab — AI-Powered Legal Assistant for Indian Lawyers

---

## 🧩 The Problem

Indian lawyers waste enormous time on two deeply repetitive tasks:

1. **Legal Research** — manually searching case databases like Indian Kanoon, reading through hundreds of judgements, and writing up research memos by hand.
2. **Document Drafting** — writing contracts, petitions, and legal memos from scratch every time, even when the structure is largely the same across cases.

There is no single tool that handles both. Lawyers are forced to juggle legal databases, Word documents, and generic AI tools that don't understand Indian law, Indian courts, or their personal drafting style.

---

## 💡 The Solution

**WakeelSahab** is one workspace that does both.

- **Ask a legal question** → get a structured, formatted answer with relevant case citations from Indian courts (via the Indian Kanoon API)
- **Research mode** → the agent fetches real cases from Indian Kanoon, summarizes them, and produces a full legal analysis report — with applicable laws, precedents, arguments, counter-arguments, and a recommended strategy
- **PDF upload** → upload a legal document and ask questions about it (prototype stage)

The interface is minimal and professional — black background, yellow accents — built to feel like a lawyer's tool, not a toy.

---

## ✨ Features

| Feature | Status |
|---|---|
| Direct legal Q&A (Gemini 2.0 Flash) | ✅ Working |
| Research mode — fetches & analyzes real Indian Kanoon cases | ✅ Working |
| Structured legal report (laws, precedents, arguments, strategy) | ✅ Working |
| PDF upload endpoint | ✅ Backend ready, not yet wired to agent |
| Research mode toggle from UI | ⚠️ Backend supports it, UI toggle pending |
| Real-time streaming (token-by-token like ChatGPT) | ❌ Not yet |
| User authentication | ❌ Placeholder only |
| Document drafting with style learning | ❌ Planned |

---

## 🛠️ Tech Stack

### Frontend

| Layer | Technology |
|---|---|
| Framework | React 18 |
| Language | TypeScript |
| Build Tool | Vite 5 |
| Styling | Tailwind CSS 3 |
| Routing | React Router v7 |
| Icons | Lucide React |

### Backend

| Layer | Technology |
|---|---|
| API Server | FastAPI |
| AI Orchestration | LangGraph (StateGraph) |
| LLM | Google Gemini 2.0 Flash (via `langchain-google-genai`) |
| Case Law Data | Indian Kanoon REST API |
| Environment | Python + `uv` package manager |

---

## 🏗️ How It Works Under the Hood

The backend is a **LangGraph state machine** with two paths depending on the mode:

```
User Query
    │
    ▼
[Conditional Entry Point]
    │
    ├── Direct Mode ──────────────────────────────► [direct_answer node]
    │                                                    │ Gemini 2.0 Flash answers directly
    │                                                    ▼
    │                                                   END
    │
    └── Research Mode ──► [retriever node]
                              │ Calls Indian Kanoon API
                              ▼
                          [summarizer node]
                              │ Gemini summarizes fetched cases
                              ▼
                          [formatter node]
                              │ Gemini formats full legal report
                              ▼
                             END
```

The frontend calls `POST /ask` with `{ query, research_mode }` and renders the response in the chat window.

---

## 📁 Repository Structure

```
ogWakeelSahab/
├── backend/                  # ← Production backend
│   ├── main.py               # LangGraph agent (state machine, nodes, graph)
│   └── fastserver.py         # FastAPI server — exposes /ask endpoint
│
├── Frontend/                 # ← Production frontend
│   └── src/
│       ├── App.tsx           # Router (/ and /chat)
│       └── components/
│           ├── LandingPage.tsx   # Home page — hero, features, how it works
│           └── ChatPage.tsx      # Chat UI — PDF upload + Q&A
│
└── messyLearningBackend/     # ← Learning sandbox (not production)
    │   Personal lab notebooks used while building this product.
    │   LangGraph experiments, RAG prototypes, agent loops, etc.
    │   Safe to skip entirely.
    │
    ├── learning Langraph/    # Jupyter notebooks — LangGraph, RAG, ReAct agents
    └── smallRetriever/       # PDF chatbot prototype (FastAPI + ChromaDB + BM25 + Gemini)
```

> `messyLearningBackend/` is a personal learning archive. It contains all the experiments and prototypes that led to the current product — not production code, but useful for reference.

---

## 🚀 Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt   # or: uv sync
uvicorn fastserver:app --reload --port 8000
```

### Frontend

```bash
cd Frontend
npm install
npm run dev
```

Frontend opens at **http://localhost:5173**. Backend must be running at **http://localhost:8000**.

---

## 🔮 Future Upgrades Needed

1. **Streaming responses** — Stream tokens in real-time instead of waiting for the full answer. The architecture doc (`messyLearningBackend/old_backedn/STREAMING_INTEGRATION.md`) already has a blueprint for a `/ask-stream` SSE endpoint.

2. **Wire up PDF upload to the agent** — The `/upload_pdf` endpoint exists in the prototype (`smallRetriever/`). It needs to be integrated into the main agent so uploaded PDFs become part of the context.

3. **Research mode toggle in the UI** — The backend already supports `research_mode: true/false`. The frontend just needs a toggle button in `ChatPage.tsx`.

4. **Document drafting** — The most requested feature. AI drafts petitions, contracts, and memos based on the lawyer's inputs and learns their personal style over time. Early prototype exists in `messyLearningBackend/learning Langraph/drafter.ipynb`.

5. **User authentication** — The Login button is a placeholder. Needs proper auth so each lawyer has their own session, document history, and style profile.

6. **Conversation memory** — Currently stateless. Adding LangGraph checkpointing (already experimented with in `chatbot_memory.py`) would let the agent remember previous turns in the same session.

7. **Deployment** — No deployment pipeline yet. Needs containerization (Docker) and a cloud host for both the FastAPI backend and the React frontend.
