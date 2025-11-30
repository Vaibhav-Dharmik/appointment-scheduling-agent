from typing import List, Optional
from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    reply: str
    state: Optional[dict] = None


class AppointmentType(str):
    # Just aliases as strings, can be enforced tighter if needed
    pass


class AvailabilitySlot(BaseModel):
    start_time: str  # "09:00"
    end_time: str    # "09:30"
    available: bool = True


class AvailabilityResponse(BaseModel):
    date: str
    appointment_type: str
    available_slots: List[AvailabilitySlot]


class PatientInfo(BaseModel):
    name: str
    email: EmailStr
    phone: str


class BookingRequest(BaseModel):
    appointment_type: str
    date: str
    start_time: str
    patient: PatientInfo
    reason: str


class BookingResponse(BaseModel):
    booking_id: str
    status: str
    confirmation_code: str
    details: dict
