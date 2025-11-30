from fastapi import APIRouter, Depends
from ..models.schemas import ChatRequest, ChatResponse
from ..agent.scheduling_agent import SchedulingAgent

router = APIRouter(prefix="/api", tags=["chat"])

# Global reference to agent - will be set by main.py
_agent_instance: SchedulingAgent = None


def get_agent() -> SchedulingAgent:
    global _agent_instance
    if _agent_instance is None:
        raise RuntimeError("Agent instance not initialized")
    return _agent_instance


def set_agent(agent: SchedulingAgent):
    """Set the global agent instance from main.py"""
    global _agent_instance
    _agent_instance = agent


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    payload: ChatRequest,
    agent: SchedulingAgent = Depends(get_agent),
):
    return await agent.handle_chat(payload)
