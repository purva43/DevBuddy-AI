# 🤖 DevBuddy AI

DevBuddy AI is a personal programming mentor agent, built from scratch (no agent frameworks) to understand how AI agents actually work under the hood — memory, tool use, retrieval, and multi-step reasoning — rather than just wiring together a library.

It runs both as a terminal chat and a Streamlit web app, remembers conversations across sessions, and can search the web, do exact math, read local files and PDFs, run sandboxed Python code, and answer questions from its own knowledge base using retrieval-augmented generation (RAG).

---

## Features

- 💬 **Conversational chat** with a friendly mentor persona, streamed word-by-word
- 🧠 **Persistent memory** — remembers past conversations across restarts (SQLite)
- 🧮 **Calculator tool** — exact arithmetic instead of LLM guesswork
- 🌐 **Web search tool** — real-time info for current events, versions, dates
- 📂 **File & PDF reading** — summarizes local documents, with safe truncation limits
- 🐍 **Sandboxed Python execution** — runs AI-generated code safely, with keyword-blocking and a restricted builtins environment
- 📚 **RAG knowledge base** — answers project-specific questions using semantic search (ChromaDB) over stored notes, instead of guessing
- 🖥️ **Web UI** (Streamlit) alongside the terminal version
- 🪵 **Logging** to `devbuddy.log` for persistent error tracking

---

## Architecture

```
                     User
                       │
                       ▼
              app.py / streamlit_app.py   ← entry points
                       │
                       ▼
                llm_client.py             ← talks to Gemini, retry logic, tool registration
                       │
        ┌──────────────┼──────────────────────┐
        ▼              ▼                      ▼
   tools.py      memory_db.py           vector_store.py
   (calculator,   (SQLite —              (ChromaDB —
   web_search,    persistent chat        semantic search
   read_file,     history across         over stored
   read_pdf,      sessions)              knowledge)
   run_python_code,
   search_knowledge_base)
        │
        ▼
   config.py   ← single source of truth for model name, file limits, etc.
```

**Design principles behind this structure:**
- `app.py` doesn't know *how* the AI works — it just calls `ask()`. All AI-specific logic (retries, tool registration, prompts) lives in `llm_client.py`.
- Every tool is a plain, independently testable Python function with a clear docstring — the model chooses which to call based on that docstring alone, so descriptions matter as much as the code.
- Memory (SQLite) and knowledge (ChromaDB) are separate systems: memory is *what was said*, knowledge is *what's true/known*. Conflating them would make both harder to reason about.
- Config values (model name, file size limits) live in one file (`config.py`) so a future model deprecation — which happened multiple times during development — requires changing one line, not hunting across files.

---

## How to Run It

**1. Clone and install dependencies:**
```bash
git clone https://github.com/YOUR_USERNAME/devbuddy-ai.git
cd devbuddy-ai
pip install -r requirements.txt
```

**2. Set up your API key:**
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```
Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

**3. Load the knowledge base (optional, for RAG questions):**
```bash
python load_knowledge.py
```

**4. Run it — terminal version:**
```bash
python app.py
```

**Or the web UI:**
```bash
streamlit run streamlit_app.py
```

---

## What This Project Is Not

Being upfront about limitations, since that's part of understanding a system honestly:
- The Python execution sandbox is a beginner-safe guardrail (keyword blocklist + restricted builtins), **not** production-grade isolation. A real deployment would need container-level sandboxing.
- The web search tool depends on a scraping-based library that can be rate-limited or CAPTCHA-blocked by search engines — it's reliable for learning, not for production traffic.
- Tool-calling reliability can be sensitive to how a question is phrased; this was tested and partially mitigated with explicit system prompt instructions, but isn't perfectly robust.

---

## What I Learned

This project was built as a 30-day, day-by-day learning bootcamp — from "an LLM only predicts text" all the way to a working multi-tool RAG agent. Full detailed notes, written for anyone new to agentic AI, are in [`MY_LEARNING.md`](./MY_LEARNING.md).

---

## Tech Stack

Python · Google Gemini API (`gemini-3.1-flash-lite`) · SQLite · ChromaDB · Streamlit · `ddgs` (web search) · `pypdf`
