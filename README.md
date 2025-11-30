# Medical Appointment Scheduling Agent

An intelligent conversational agent to schedule medical appointments via Calendly and answer clinic FAQs using RAG.

## Tech Stack

- Backend: FastAPI (Python)
- LLM: OpenAI (configurable via env)
- Vector Store: Local ChromaDB (can be swapped)
- Calendar: Calendly API (real or mock)
- Frontend: React (simple chat UI)

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # fill in keys
