---

### `architecture_diagram_explained.md`

```md
# Architecture Diagram (Explained)

Components:

1. User (Web UI)
2. FastAPI Backend
3. LLM (OpenAI)
4. Tools:
   - Availability Tool
   - Booking Tool
   - RAG FAQ Tool
5. Calendly API (or mock)
6. Vector Store (Chroma)
7. JSON Data: clinic_info.json, doctor_schedule.json

Flow:

User → Chat API → Scheduling Agent:

- Detects intent: SCHEDULING vs FAQ vs SMALLTALK
- For SCHEDULING:
  - Collects appointment type, date, time preference
  - Calls Availability Tool → Calendly
  - Suggests 3–5 slots
  - On confirmation + user details → Booking Tool → Calendly
- For FAQ:
  - Calls RAG FAQ Tool → Vector Store → Answer with context
- Context Switching:
  - Maintains conversation state
  - Can resume booking after FAQ answers

Error Paths:

- Calendly unavailable → apologizes, suggests calling clinic
- No slots → offers alternative dates / waitlist info
- Ambiguous time → clarifying questions
```
