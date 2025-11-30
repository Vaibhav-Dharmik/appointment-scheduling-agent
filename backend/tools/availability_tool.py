from typing import List
import httpx
from ..models.schemas import AvailabilitySlot


class AvailabilityTool:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def get_slots(self, date: str, appointment_type: str) -> List[AvailabilitySlot]:
        url = f"{self.base_url}/api/calendly/availability"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params={"date": date, "appointment_type": appointment_type})
            resp.raise_for_status()
            data = resp.json()
        return [AvailabilitySlot(**slot) for slot in data["available_slots"]]
