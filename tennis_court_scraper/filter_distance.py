import math

from tennis_court_scraper.models import Slot
from tennis_court_scraper.venues import load_venues

_EARTH_RADIUS_KM = 6371


def _haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return _EARTH_RADIUS_KM * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def filter_by_distance(
    slots: list[Slot],
    centers: list[tuple[float, float]],
    radius_km: float,
) -> list[Slot]:
    venues = load_venues()
    result: list[Slot] = []
    for slot in slots:
        vid = slot.venue_id
        if vid not in venues:
            slot.venue_name = f"Unknown ({vid})"
            result.append(slot)
            continue
        venue = venues[vid]
        slot.venue_name = str(venue["name"])
        vlat, vlng = float(venue["lat"]), float(venue["lng"])
        dists = [_haversine(clat, clng, vlat, vlng) for clat, clng in centers]
        if all(d <= radius_km for d in dists):
            slot.distance_km = round(max(dists), 1)
            result.append(slot)
    return result
