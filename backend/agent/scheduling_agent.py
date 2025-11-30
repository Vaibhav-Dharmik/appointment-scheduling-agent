from typing import Dict, Any
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables from .env file
load_dotenv()

from ..rag.faq_rag import FAQRAG
from ..tools.availability_tool import AvailabilityTool
from ..tools.booking_tool import BookingTool
from ..models.schemas import (
    ChatRequest,
    ChatResponse,
    BookingRequest,
    PatientInfo,
)
from .prompts import SYSTEM_PROMPT

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")


class SchedulingAgent:
    """
    Orchestrates conversation:
    - Light intent detection
    - Calls FAQ or scheduling tools
    - Delegates language generation to LLM
    """

    def __init__(
        self,
        faq_rag: FAQRAG,
        availability_tool: AvailabilityTool,
        booking_tool: BookingTool,
    ):
        self.faq_rag = faq_rag
        self.availability_tool = availability_tool
        self.booking_tool = booking_tool

    async def _call_llm(self, messages):
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                # Return mock response if no API key
                return "I'm an AI assistant. Due to API limitations, I'm providing a demo response. In a production environment, I would use GPT to generate more personalized responses."
            
            client = AsyncOpenAI(api_key=api_key)
            resp = await client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
            )
            return resp.choices[0].message.content
        except Exception as e:
            # Fallback for API errors
            print(f"LLM call error: {e}")
            return "I apologize for the temporary issue. Please try again in a moment."

    def _detect_intent(self, last_user_message: str) -> str:
        msg = last_user_message.lower()
        if any(k in msg for k in ["insurance", "billing", "location", "where", "hours", "open", "close", "parking", "cancelation policy", "covid"]):
            return "FAQ"
        if any(k in msg for k in ["book", "schedule", "appointment", "see doctor", "reschedule", "cancel"]):
            return "SCHEDULING"
        return "SMALLTALK"

    async def handle_chat(self, payload: ChatRequest) -> ChatResponse:
        if not payload.messages:
            return ChatResponse(reply="How can I help you today?")

        last_user_msg = payload.messages[-1].content
        intent = self._detect_intent(last_user_msg)

        # In a full solution: track state via a store or token.
        # Here we keep it simple.

        if intent == "FAQ":
            faq_answer = await self.faq_rag.answer(last_user_msg)
            # Let LLM wrap it nicely
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": last_user_msg},
                {"role": "assistant", "content": faq_answer},
                {"role": "user", "content": "Please respond naturally using the above information."},
            ]
            reply = await self._call_llm(messages)
            return ChatResponse(reply=reply, state={"intent": "FAQ"})

        if intent == "SCHEDULING":
            # Very simplified booking logic:
            # 1. Ask for date + time preference if not mentioned
            # 2. Get availability
            # 3. Offer slots
            # In a real app, you'd parse entities properly.
            # For the assessment, you can keep a guided flow on frontend.

            # We just tell the user what we can do and wait for more info.
            guidance = (
                "I can help you with scheduling.\n"
                "Please tell me:\n"
                "1) The type of appointment (general consultation, follow-up, physical exam, specialist consultation)\n"
                "2) Your preferred date (YYYY-MM-DD)\n"
                "3) Whether you prefer morning or afternoon.\n"
            )
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": last_user_msg},
                {"role": "assistant", "content": guidance},
            ]
            reply = await self._call_llm(messages)
            return ChatResponse(reply=reply, state={"intent": "SCHEDULING"})

        # SMALLTALK / default
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for m in payload.messages:
            messages.append({"role": m.role, "content": m.content})
        reply = await self._call_llm(messages)
        return ChatResponse(reply=reply, state={"intent": "SMALLTALK"})

    async def finalize_booking(
        self,
        appointment_type: str,
        date: str,
        start_time: str,
        patient_name: str,
        patient_email: str,
        patient_phone: str,
        reason: str,
    ) -> ChatResponse:
        patient = PatientInfo(name=patient_name, email=patient_email, phone=patient_phone)
        booking_req = BookingRequest(
            appointment_type=appointment_type,
            date=date,
            start_time=start_time,
            patient=patient,
            reason=reason,
        )
        booking_resp = await self.booking_tool.book(booking_req)
        text = (
            f"Your appointment is confirmed!\n\n"
            f"- Type: {booking_resp.details['appointment_type']}\n"
            f"- Date: {booking_resp.details['date']}\n"
            f"- Time: {booking_resp.details['start_time']}\n"
            f"- Confirmation code: {booking_resp.confirmation_code}\n\n"
            f"You’ll also receive details on {booking_resp.details['patient']['email']}."
        )
        return ChatResponse(reply=text, state={"intent": "BOOKED"})
