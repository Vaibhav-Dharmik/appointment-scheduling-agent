import httpx
from ..models.schemas import BookingRequest, BookingResponse


class BookingTool:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def book(self, payload: BookingRequest) -> BookingResponse:
        url = f"{self.base_url}/api/calendly/book"
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload.model_json())
            # .model_dump_json() in Pydantic v2 – adjust if needed
            if resp.status_code >= 400:
                # Could handle more gracefully
                resp.raise_for_status()
            data = resp.json()
        return BookingResponse(**data)
