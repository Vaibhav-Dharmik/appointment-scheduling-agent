import random
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, HTTPException, Query
from ..models.schemas import (
    AvailabilityResponse,
    AvailabilitySlot,
    BookingRequest,
    BookingResponse,
)

router = APIRouter(prefix="/api/calendly", tags=["calendly"])


def generate_mock_slots(date: str, duration_minutes: int) -> List[AvailabilitySlot]:
    # Simple fixed working hours: 9:00–17:00
    start_hour = 9
    end_hour = 17
    slots: List[AvailabilitySlot] = []

    dt_date = datetime.fromisoformat(date)
    current = dt_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end = dt_date.replace(hour=end_hour, minute=0, second=0, microsecond=0)

    while current + timedelta(minutes=duration_minutes) <= end:
        end_time = current + timedelta(minutes=duration_minutes)
        slots.append(
            AvailabilitySlot(
                start_time=current.strftime("%H:%M"),
                end_time=end_time.strftime("%H:%M"),
                available=random.random() > 0.2,  # 80% chance available
            )
        )
        current = end_time

    return slots


APPOINTMENT_DURATIONS = {
    "general_consultation": 30,
    "followup": 15,
    "physical_exam": 45,
    "specialist_consultation": 60,
}


@router.get("/availability", response_model=AvailabilityResponse)
async def get_availability(
    date: str = Query(..., example="2024-01-15"),
    appointment_type: str = Query(..., example="general_consultation"),
):
    if appointment_type not in APPOINTMENT_DURATIONS:
        raise HTTPException(status_code=400, detail="Unsupported appointment type")

    duration = APPOINTMENT_DURATIONS[appointment_type]
    slots = generate_mock_slots(date, duration_minutes=duration)

    return AvailabilityResponse(
        date=date,
        appointment_type=appointment_type,
        available_slots=slots,
    )


@router.post("/book", response_model=BookingResponse)
async def book_appointment(payload: BookingRequest):
    # In real integration, call Calendly API here
    booking_id = f"APPT-{random.randint(1000, 9999)}"
    confirmation_code = f"CONF-{random.randint(100000, 999999)}"

    return BookingResponse(
        booking_id=booking_id,
        status="confirmed",
        confirmation_code=confirmation_code,
        details={
            "appointment_type": payload.appointment_type,
            "date": payload.date,
            "start_time": payload.start_time,
            "patient": payload.patient.dict(),
            "reason": payload.reason,
        },
    )
