from pydantic import BaseModel


class Slot(BaseModel):
    venue_id: str
    court_name: str
    date: str
    start_minute: int
    duration_minutes: int
    lit: bool
    full_size: bool
    outdoor: bool
    price: float | None
    booking_url: str
    venue_name: str = ""
    distance_km: float = 0.0
