from fastapi.testclient import TestClient
from backend.main import app
c=TestClient(app)
def test_health(): assert c.get('/health').json()['simulation_supported'] is True
def test_followup():
    r=c.post('/followup/risk',json={'age_band':'40-59','previous_missed_visits':1,'lead_time_days':14,'recommended_followup_days':30,'visit_type':'retina','contact_available':True}); assert r.status_code==200
