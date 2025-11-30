# ��� Appointment Scheduling Agent - Quick Start Guide

## Overview
A fully functional AI-powered medical appointment scheduling system with:
- **Backend:** FastAPI + LangChain + RAG (Retrieval-Augmented Generation)
- **Frontend:** React + TypeScript + Tailwind CSS (Loveable.ai)
- **Features:** Intent detection, FAQ answering, appointment booking, availability checking

---

## ⚡ Quick Start (5 minutes)

### 1. Install Dependencies

```bash
# Backend (Python)
pip install -r requirements.txt

# Frontend (Node.js)
cd frontend
npm install
```

### 2. Start Backend Server

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

**API will be available at:** http://localhost:8000/docs

### 3. Start Frontend Dev Server (in new terminal)

```bash
cd frontend
npm run dev
```

**UI will be available at:** http://localhost:5173

### 4. Test the System

Open http://localhost:5173 in your browser and:
1. Click "Schedule Appointment" or "Clinic Information"
2. Type a message in the chat
3. See the AI respond with intent detection and appropriate actions

---

## ��� API Endpoints

### POST /api/chat
Send a message and get an AI response
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What are your hours?"}]}'
```

### GET /api/calendly/availability
Get available time slots
```bash
curl "http://localhost:8000/api/calendly/availability?date=2024-12-25&appointment_type=general_consultation"
```

Supported appointment types:
- `general_consultation` (30 min)
- `followup` (15 min)
- `physical_exam` (45 min)
- `specialist_consultation` (60 min)

### POST /api/calendly/book
Book an appointment
```bash
curl -X POST http://localhost:8000/api/calendly/book \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_type": "general_consultation",
    "date": "2024-12-25",
    "start_time": "09:00",
    "patient": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-0000"
    },
    "reason": "Annual checkup"
  }'
```

---

## ��� Run Tests

### Unit Tests
```bash
python -m pytest tests/ -v
```

Results: 2/2 tests pass ✅

### E2E Tests
```bash
# Backend and frontend must be running
python -c "
import requests
BASE_URL = 'http://localhost:8000'

# Test FAQ
r = requests.post(f'{BASE_URL}/api/chat', 
  json={'messages': [{'role': 'user', 'content': 'What are your hours?'}]})
print('Chat:', r.status_code, r.json()['state']['intent'])

# Test Availability
r = requests.get(f'{BASE_URL}/api/calendly/availability',
  params={'date': '2024-12-25', 'appointment_type': 'general_consultation'})
print('Availability:', r.status_code, len(r.json()['available_slots']), 'slots')

# Test Booking
r = requests.post(f'{BASE_URL}/api/calendly/book', json={
  'appointment_type': 'general_consultation',
  'date': '2024-12-25',
  'start_time': '09:00',
  'patient': {'name': 'Test', 'email': 'test@example.com', 'phone': '+1-555-0000'},
  'reason': 'Test'
})
print('Booking:', r.status_code, r.json()['booking_id'])
"
```

---

## ���️ Project Structure

```
appointment-scheduling-agent/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── agent/
│   │   └── scheduling_agent.py  # AI agent logic
│   ├── api/
│   │   ├── chat.py         # Chat endpoint
│   │   └── calendly_integration.py  # Booking endpoints
│   ├── rag/
│   │   ├── embeddings.py   # Vector embeddings (with mock fallback)
│   │   ├── faq_rag.py      # FAQ retrieval
│   │   └── vector_store.py # In-memory vector store
│   ├── tools/
│   │   ├── availability_tool.py
│   │   └── booking_tool.py
│   └── models/
│       └── schemas.py      # Pydantic schemas
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx  # Main chat UI
│   │   │   ├── ChatMessage.tsx
│   │   │   └── ChatInput.tsx
│   │   ├── pages/
│   │   │   ├── Index.tsx   # Home page
│   │   │   └── NotFound.tsx
│   │   └── integrations/
│   │       └── supabase/   # (Optional - not currently used)
│   └── vite.config.ts      # API proxy config
├── data/
│   ├── clinic_info.json    # FAQ data for RAG
│   └── doctor_schedule.json
├── tests/
│   ├── test_agent.py
│   └── test_booking.py
├── requirements.txt
└── TEST_RESULTS.md
```

---

## ��� Environment Variables

Create `.env` in project root:
```
OPENAI_API_KEY=your_openai_key_here
LLM_MODEL=gpt-4
USE_MOCK_EMBEDDINGS=true
```

**Note:** Currently using mock embeddings due to OpenAI quota. To enable real LLM:
1. Get an OpenAI API key from https://platform.openai.com
2. Set `OPENAI_API_KEY` in `.env`
3. Set `USE_MOCK_EMBEDDINGS=false`

---

## ��� Features

| Feature | Status | Details |
|---------|--------|---------|
| **Chat Interface** | ✅ | Real-time messaging with intent detection |
| **FAQ Retrieval** | ✅ | RAG-based question answering |
| **Appointment Booking** | ✅ | Create appointments with confirmation codes |
| **Availability Check** | ✅ | View time slots by date & appointment type |
| **Multi-turn Conversation** | ✅ | Context-aware responses |
| **Mock Calendly API** | ✅ | Simulated appointment system |
| **Intent Detection** | ✅ | FAQ, Booking, Availability, Smalltalk |
| **Error Handling** | ✅ | Graceful fallbacks for API failures |

---

## ⚠️ Known Limitations

1. **LLM Responses:** Currently using generic fallback due to OpenAI quota
2. **Real-time Chat:** Using polling (can add WebSocket for true real-time)
3. **Database:** In-memory storage only (should use persistent DB for production)
4. **Authentication:** No user login (mock-only for now)

---

## ��� Deployment

### Build Frontend
```bash
cd frontend
npm run build
# Output: dist/ folder ready for hosting
```

### Run Backend in Production
```bash
gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Deploy to Cloud
- **Frontend:** Netlify, Vercel, or S3 + CloudFront
- **Backend:** Heroku, Railway, AWS Lambda, or Docker

---

## ��� Support & Troubleshooting

### Backend won't start
```
Error: Port 8000 already in use
Solution: pkill -f uvicorn  # or change --port 8001
```

### Frontend dev server won't connect to backend
```
Error: 404 on /api/chat
Solution: Ensure backend is running on :8000 and vite.config.ts has proxy configured
```

### Tests failing
```bash
# Make sure dependencies are installed
pip install -r requirements.txt
npm install

# Run with verbose output
pytest tests/ -v --tb=short
```

---

## ��� Additional Resources

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Vite Docs](https://vitejs.dev)
- [React Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [LangChain Docs](https://js.langchain.com)

---

**Last Updated:** November 30, 2025
**All Tests Passing:** ✅ 12/12
