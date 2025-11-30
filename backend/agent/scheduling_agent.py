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

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-mini")


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
        """Call OpenAI LLM with fallback to mock responses."""
        # Check USE_MOCK_LLM dynamically (not at import time)
        use_mock_llm = os.getenv("USE_MOCK_LLM", "true").lower() == "true"
        
        if use_mock_llm:
            # Use intelligent mock responses
            return self._generate_mock_response(messages)
        
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("Warning: OPENAI_API_KEY not set, using mock responses")
                return self._generate_mock_response(messages)
            
            client = AsyncOpenAI(api_key=api_key)
            resp = await client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
                max_tokens=500,
            )
            return resp.choices[0].message.content
        except Exception as e:
            # Fallback for API errors (quota, network, etc)
            print(f"LLM call error: {e}, using mock response")
            return self._generate_mock_response(messages)
    
    def _generate_mock_response(self, messages: list) -> str:
        """Generate intelligent mock responses based on conversation context."""
        if not messages:
            return "Hello! How can I assist you with scheduling an appointment?"
        
        # Get the FIRST substantive user message (skip system prompts and instructions)
        last_user_msg = None
        for msg in messages:
            if isinstance(msg, dict):
                if msg.get("role") == "user":
                    content = msg.get("content", "").lower()
                    # Skip instructions like "please respond naturally"
                    if not content.startswith("please "):
                        last_user_msg = content
                        break
        
        if not last_user_msg:
            return "I'm here to help. What would you like to do?"
        
        # Intelligent fallback responses based on detected patterns
        if any(k in last_user_msg for k in ["hours", "open", "close", "when", "location", "address"]):
            return "Our clinic is open Monday-Friday, 9 AM - 5 PM, and Saturday 10 AM - 2 PM. We're located at 123 Healthcare Ave. Is there anything else I can help you with?"
        
        if any(k in last_user_msg for k in ["insurance", "billing", "payment", "cost", "price", "fee"]):
            return "We accept most major insurance plans. You're welcome to contact our billing department at (555) 123-4567 for specific coverage questions. Would you like to schedule an appointment?"
        
        if any(k in last_user_msg for k in ["book", "schedule", "appointment", "date", "time", "reschedule"]):
            return "I can help you schedule an appointment! Please let me know:\n1) Type of appointment (general consultation, follow-up, physical exam, specialist consultation)\n2) Your preferred date (YYYY-MM-DD)\n3) Time preference (morning or afternoon)\n\nWhich appointment type interests you?"
        
        if any(k in last_user_msg for k in ["cancel", "reschedule", "change", "modify"]):
            return "I can help you modify your appointment. Please provide your confirmation code or appointment ID so I can look it up. Then let me know what changes you'd like to make."
        
        if any(k in last_user_msg for k in ["doctor", "physician", "specialist", "staff", "qualifications"]):
            return "Our team consists of experienced healthcare professionals. For detailed information about specific doctors and their specialties, please visit our website or call our main office."
        
        # Default friendly response
        return "Thank you for reaching out! I'm here to help with appointment scheduling, answer clinic questions, and provide support. What can I assist you with today?"

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
