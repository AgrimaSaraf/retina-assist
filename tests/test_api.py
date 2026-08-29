from fastapi.testclient import TestClient
from backend.main import app

client=TestClient(app)

def test_health():
    r=client.get("/health")
    assert r.status_code==200
    assert r.json()["research_only"] is True

def test_followup():
    r=client.post("/followup/risk",json={
        "age_band":"40-59",
        "previous_missed_visits":1,
        "lead_time_days":14,
        "recommended_followup_days":30,
        "visit_type":"retina",
        "contact_available":True,
    })
    assert r.status_code==200
    assert 0 <= r.json()["probability"] <= 1
