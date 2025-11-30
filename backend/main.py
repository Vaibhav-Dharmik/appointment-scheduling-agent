import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

from .api import chat as chat_router_module
from .api import calendly_integration
from .agent.scheduling_agent import SchedulingAgent
from .rag.vector_store import SimpleVectorStore
from .rag.faq_rag import FAQRAG
from .tools.availability_tool import AvailabilityTool
from .tools.booking_tool import BookingTool


app = FastAPI(title="Medical Appointment Scheduling Agent")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global singletons
faq_store = SimpleVectorStore(data_path=os.path.join("data", "clinic_info.json"))
faq_rag = FAQRAG(store=faq_store)

availability_tool = AvailabilityTool(base_url="http://localhost:8000")
booking_tool = BookingTool(base_url="http://localhost:8000")

agent_instance = SchedulingAgent(
    faq_rag=faq_rag,
    availability_tool=availability_tool,
    booking_tool=booking_tool,
)


@app.on_event("startup")
async def startup_event():
    # Preload RAG data
    await faq_store.load()


def get_agent() -> SchedulingAgent:
    return agent_instance


def get_agent() -> SchedulingAgent:
    return agent_instance


# Set agent instance in chat router
chat_router_module.set_agent(agent_instance)

# Now include the router
app.include_router(chat_router_module.router)
app.include_router(calendly_integration.router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Medical Scheduling Agent Backend"}
