# Agentic AI

> A hands-on journey from raw LLM calls to working agents — one concept, one folder, one script at a time.

[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?style=flat-square)](https://docs.astral.sh/uv/)

---

## Progress

| Module | Status | Details |
|--------|:------:|---------|
| [**Basics**](Basics/README.md) | ✅ Complete | Build an agent from scratch — no framework |
| **LangChain** | 🚧 In progress | *README coming when the folder is done* |
| *Next up* | 📋 Planned | TBD — new folder when LangChain is done |

---

## Getting started

**Prerequisites:** Python 3.14+, [uv](https://docs.astral.sh/uv/)

```bash
git clone <your-repo-url>
cd Agentic_AI
uv sync
```

Create a `.env` file in the project root with at least one API key:

```env
# Free providers (recommended to start)
GROQ_API_KEY=...
OPENROUTER_API_KEY=...

# Paid providers (optional)
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
```

Each module folder has its own `README.md` with the full learning path, run instructions, and file-by-file breakdown.

---

## Modules

### [Basics](Basics/README.md) · ✅ Complete

Build a working agent from scratch — no framework, just Python.

Covers the full arc from first principles to a chat UI: model vs chatbot vs agent, calling real LLMs, structured extraction with Pydantic, manual and model-driven tool use, the agent loop, and a Streamlit capstone.

| Scripts | 7 |
| Approach | Hand-rolled — you own every line |
| Capstone | Terminal REPL + Streamlit chat app |

→ [Full details in Basics/README.md](Basics/README.md)

---

### LangChain · 🚧 In progress

Learn the same ideas through LangChain — abstractions for models, tools, and agents instead of wiring everything yourself.

Currently exploring LangChain chat models, streaming, and how framework primitives map back to the hand-rolled patterns from Basics.

| Scripts | 1 (growing) |
| Approach | LangChain + provider integrations |
| Focus | `ChatXAI`, streaming, agent abstractions |

→ *Detailed README when this folder is complete*

---

## Project structure

```
Agentic_AI/
├── Basics/                  ✅ Complete — see Basics/README.md
├── LangChain/               🚧 In progress
├── pyproject.toml
└── README.md                ← you are here
```

---

<p align="center">
  <sub>Built incrementally — one folder at a time.</sub>
</p>
