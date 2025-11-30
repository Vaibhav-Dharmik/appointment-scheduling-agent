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
    resp = await agent.handle_chat(req)

    assert "hour" in resp.reply.lower()
    assert resp.state["intent"] == "FAQ"
