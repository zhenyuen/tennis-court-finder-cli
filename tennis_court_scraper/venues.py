import json
from pathlib import Path

_VENUES_JSON_PATH = Path(__file__).parent / "venues.json"


def load_venues() -> dict[str, dict[str, str | float]]:
    with open(_VENUES_JSON_PATH) as f:
        return json.load(f)
