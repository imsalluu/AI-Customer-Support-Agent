# SupportIQ AI - Enterprise AI Customer Support SaaS Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js 14](https://img.shields.io/badge/Next.js-14+-black.svg?logo=next.js)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791.svg?logo=postgresql)](https://www.postgresql.org/)

**SupportIQ AI** is an omnichannel, autonomous B2B customer support SaaS platform. It combines LangGraph-powered stateful agents, strict zero-hallucination controlled tool execution, pgvector knowledge retrieval (RAG) with exact source citations, automated intent and sentiment analysis, support ticket lifecycle management, human-in-the-loop (HITL) handoff, and executive support intelligence.

---

## Key Capabilities

- **Omnichannel Automation**: Native WebChat widget, WhatsApp Cloud API, Messenger, and Email architectures.
- **pgvector Knowledge Base & RAG**: Multi-format ingestion (PDF, DOCX, TXT, Markdown, FAQ, Policies) with chunking, pgvector similarity search, and source citations (Document, Page, Section).
- **Controlled Business Tools**: 11 deterministic tools for order tracking, inventory lookup, customer search, shipping validation, and ticket creation.
- **Stateful AI Support Agent**: LangGraph state machine with intent classification, sentiment analysis, confidence thresholding, and safety fallback.
- **Human-in-the-Loop (HITL)**: Seamless real-time agent handoff (`AI_ACTIVE` ↔ `WAITING_HUMAN` ↔ `HUMAN_ACTIVE` ↔ `RESOLVED`), agent takeover, and rolling conversation summaries.
- **Customer CRM & Support Tickets**: Multi-tier customer profiles, SLA tracking, Kanban and table ticket views, and automatic escalation.
- **Executive Analytics & AI Insights**: CSAT reporting, AI resolution rates, escalation metrics, and proactive AI weekly support intelligence.
- **Embeddable Chat Widget**: Drop-in JavaScript widget with quick replies, citation viewer, typing indicator, and CSAT rating.
- **Multi-Tenant B2B Architecture**: Strict organization-level isolation, RBAC (Owner, Admin, Agent, Viewer), and subscription tier tracking.

---

## Quickstart

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- PostgreSQL with pgvector extension (or built-in fallback)
- Redis

### Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` for the dashboard and landing page.

---

## License
MIT
