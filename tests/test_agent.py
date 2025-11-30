import pytest
from backend.rag.vector_store import SimpleVectorStore
from backend.rag.faq_rag import FAQRAG
from backend.agent.scheduling_agent import SchedulingAgent
from backend.tools.availability_tool import AvailabilityTool
from backend.tools.booking_tool import BookingTool
from backend.models.schemas import ChatRequest, Message


@pytest.mark.asyncio
async def test_faq_intent():
    store = SimpleVectorStore(data_path="data/clinic_info.json")
    await store.load()
    faq_rag = FAQRAG(store)
    agent = SchedulingAgent(
        faq_rag=faq_rag,
        availability_tool=AvailabilityTool(),
        booking_tool=BookingTool(),
    )

    req = ChatRequest(messages=[Message(role="user", content="What are your hours of operation?")])
    # Validate RAG retrieval directly
    faq_answer = await faq_rag.answer("What are your hours of operation?")
    assert "hour" in faq_answer.lower()

    # Agent should detect FAQ intent and return a ChatResponse with intent set
    resp = await agent.handle_chat(req)
    assert resp.state["intent"] == "FAQ"
