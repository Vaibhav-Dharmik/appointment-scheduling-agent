# Medical Appointment Scheduling Agent

An intelligent conversational agent to schedule medical appointments via Calendly and answer clinic FAQs using RAG.

## Tech Stack

## Setup

````bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # fill in keys

# Medical Appointment Scheduling Agent

An intelligent conversational agent to schedule medical appointments via Calendly (or a mock) and answer clinic FAQs using a Retrieval-Augmented Generation (RAG) pipeline.

## Tech Stack

- Backend: FastAPI (Python 3.10+)
- LLM: OpenAI (configurable via env)
- Vector Store: Local in-memory (adapter-friendly; can swap to ChromaDB)
- Calendar: Calendly API (real or mock)
- Frontend: React (minimal chat UI)

## Quick Setup

1. Create and activate a Python virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
````

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Copy and fill environment variables

```bash
cp .env.example .env
# Edit .env to add real API keys if you want to use OpenAI / Calendly (or keep mocks enabled)
```

4. Run backend

```bash
uvicorn backend.main:app --port 8000
```

5. (Optional) Run frontend dev server

```bash
cd frontend
npm install
npm start
```

## Important Environment Variables

See `.env.example`. Key flags:

- `USE_MOCK_CALENDLY=true` — use a built-in mock Calendly API (default for testing)
- `USE_MOCK_EMBEDDINGS=true` — use deterministic mock embeddings to avoid OpenAI quota
- `OPENAI_API_KEY` — real OpenAI key (required if using real embeddings / LLM calls)

## System Design (brief)

- User -> Frontend chat UI -> `POST /api/chat`
- `SchedulingAgent` detects intent: `FAQ`, `SCHEDULING`, `SMALLTALK`
- For FAQ: RAG pipeline (`faq_rag` -> `vector_store`) retrieves context from `data/clinic_info.json` and returns summarized answer
- For Scheduling: `AvailabilityTool` calls Calendly mock endpoints (`/api/calendly/availability`) and `BookingTool` calls `/api/calendly/book` to create bookings
- LLM calls are used to generate user-facing text; fallbacks are in place when API calls fail

## Scheduling Logic

- Appointment durations are mapped per type (consultation = 30m, follow-up = 15m, physical = 45m, specialist = 60m)
- Agent offers 3–5 slots based on user preference and availability
- Basic conflict prevention is implemented using the mock schedule; consider adding real overlap checks for production

## Testing

- Unit tests live in `tests/`.
- Run tests with:

```bash
pytest -q
```

## Notes & Next Steps

- Frontend: a minimal React UI is included; extend styling and flows as needed.
- Vector DB: production deployments should use a persistent vector DB (Chroma/Pinecone/etc.)
- Remove real API keys from the repository and rely on environment variables. `.env` is excluded via `.gitignore`.

If you'd like, I can: implement a richer frontend, add more unit tests for booking flows, or swap in ChromaDB for embeddings — tell me which.
