# WakeelSahab — Frontend

The user-facing interface for WakeelSahab, an AI-powered legal assistant built for Indian lawyers.

---

## 🧩 The Problem It Solves

Lawyers in India waste enormous time on two repetitive tasks:

1. **Legal Research** — manually searching case databases like Indian Kanoon, reading through hundreds of judgements, and then writing up a research memo by hand.
2. **Document Drafting** — writing contracts, petitions, and legal memos from scratch every time, even when the structure is the same.

There's no single tool that does both — lawyers switch between legal databases, Word documents, and generic AI tools that don't understand Indian law or their personal drafting style.

**WakeelSahab fixes this.** One workspace. Ask a legal question, get a structured research report with case citations from Indian courts. Upload a document, get AI-assisted drafting that learns your style.

---

## 💡 The Solution

A clean, fast web interface that connects to a LangGraph AI backend. Two things it lets you do:

- **Ask legal questions** → get structured answers with relevant case law from Indian Kanoon
- **Upload a legal PDF** → ask questions about that specific document

The UI is intentionally minimal — black background, yellow accents — built to feel professional, not like a toy.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | React 18 |
| Language | TypeScript |
| Build Tool | Vite 5 |
| Styling | Tailwind CSS 3 |
| Routing | React Router v7 |
| Icons | Lucide React |
| Backend API | FastAPI at `http://localhost:8000` |

---

## 📁 Project Structure

```
src/
├── App.tsx                  # Router — two routes: / and /chat
└── components/
    ├── LandingPage.tsx      # Home page — hero, features, how it works
    └── ChatPage.tsx         # Chat interface — PDF upload + Q&A
```

### `LandingPage.tsx`
The public-facing home page. Has:
- Hero section with 4 CTA buttons (Legal Research, AutoReview, Legal Memo Generator, Drafting) — all route to `/chat` for now
- Demo video placeholder with a screenshot
- 3 benefit cards (Integrated Research, Style Preservation, Enterprise Security)
- A 5-step "How It Works" workflow section
- Responsive navbar with mobile hamburger menu

### `ChatPage.tsx`
The core product UI. Has:
- Chat window with user and bot message bubbles + timestamps
- Typing indicator (animated dots) while waiting for the AI
- PDF upload section — select a file, upload it, status badge shows progress
- Text input — press Enter or click Send to ask a question
- Connects to two backend endpoints:
  - `POST /upload_pdf` — uploads the selected PDF
  - `POST /ask` — sends the query, expects `{ answer: string }` back

---

## 🚀 Running It

Make sure you have Node.js installed, then:

```bash
# Install dependencies (already done if node_modules/ exists)
npm install

# Start the dev server
npm run dev
```

Opens at **http://localhost:5173**

> The backend (FastAPI) needs to be running separately at port 8000 for the chat to work.

---

## ⚠️ Known Limitations (as of now)

- The `/upload_pdf` backend endpoint is not yet connected to the main agent — PDF uploads will show success but the agent doesn't use the PDF content yet
- Research mode (fetches cases from Indian Kanoon) exists in the backend but isn't togglable from the UI yet
- No authentication — the Login button is a placeholder
- No streaming — the AI response appears all at once after the full answer is ready
