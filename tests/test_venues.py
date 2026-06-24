from tennis_court_scraper.venues import load_venues


def test_load_returns_dict():
    venues = load_venues()
    assert isinstance(venues, dict)


def test_load_has_venues():
    venues = load_venues()
    assert len(venues) > 80


def test_load_known_venue():
    venues = load_venues()
    assert "ABTS" in venues
    abts = venues["ABTS"]
    assert abts["name"] == "Abbotts Park"
    assert abs(float(abts["lat"]) - 51.5712) < 0.001
    assert abs(float(abts["lng"]) - -0.0068) < 0.001


def test_venue_structure():
    venues = load_venues()
    for vid, v in venues.items():
        assert "name" in v
        assert "lat" in v
        assert "lng" in v
        assert isinstance(v["name"], str)
        assert isinstance(v["lat"], float)
        assert isinstance(v["lng"], float)
