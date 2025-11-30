import json
from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_calendly_availability_and_booking():
    # Test availability endpoint
    date = "2024-01-15"
    resp = client.get("/api/calendly/availability", params={"date": date, "appointment_type": "general_consultation"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["date"] == date
    assert "available_slots" in data
    assert isinstance(data["available_slots"], list)

    # Pick a slot and test booking
    slot = data["available_slots"][0]
    booking_payload = {
        "appointment_type": data["appointment_type"],
        "date": data["date"],
        "start_time": slot["start_time"],
        "patient": {
            "name": "Test Patient",
            "email": "test@example.com",
            "phone": "+1-555-0000",
        },
        "reason": "Test booking",
    }

    resp2 = client.post("/api/calendly/book", json=booking_payload)
    assert resp2.status_code == 200
    booking = resp2.json()
    assert booking["status"] == "confirmed"
    assert "confirmation_code" in booking
