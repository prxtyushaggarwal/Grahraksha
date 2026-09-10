import sys
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("1. Testing root endpoint...")
res = client.get("/")
assert res.status_code == 200, f"Root failed: {res.text}"
print("   Response:", res.json()["service"])

print("2. Testing live hazards...")
res = client.get("/api/hazards/live")
assert res.status_code == 200
hazards = res.json()["hazards"]
print(f"   Loaded {len(hazards)} hazards. First: {hazards[0]['title']} (Score: {hazards[0]['risk_score']})")

print("3. Testing multi-model ML risk prediction (RF + XGBoost + CNN + LSTM)...")
pred_data = {
    "lat": 30.2451,
    "lon": 78.8920,
    "slope_deg": 52.4,
    "rainfall_3d_mm": 140.0,
    "rainfall_forecast_24h_mm": 60.0,
    "soil_moisture_pct": 88.0,
    "elevation_m": 1200.0
}
res = client.post("/api/ml/predict", json=pred_data)
assert res.status_code == 200
pred = res.json()
print(f"   Predicted Risk Score: {pred['risk_score']}/100, Level: {pred['risk_level']}, FS: {pred['factor_of_safety']}")
print(f"   Model Breakdown: {pred['model_breakdown']}")

print("4. Testing route corridor 25-point sampling...")
corridor_req = {
    "corridor_id": "NH-58",
    "route_name": "Rishikesh to Badrinath",
    "waypoints": [
        {"name": "Rishikesh", "lat": 30.0869, "lon": 78.2676, "elevation_m": 372, "slope_deg": 12},
        {"name": "Devprayag", "lat": 30.1459, "lon": 78.5989, "elevation_m": 610, "slope_deg": 35},
        {"name": "Sirobagarh", "lat": 30.2451, "lon": 78.8920, "elevation_m": 720, "slope_deg": 52},
        {"name": "Joshimath", "lat": 30.5566, "lon": 79.5667, "elevation_m": 1890, "slope_deg": 46},
        {"name": "Badrinath", "lat": 30.7433, "lon": 79.4938, "elevation_m": 3133, "slope_deg": 30}
    ]
}
res = client.post("/api/ml/corridor-sample", json=corridor_req)
assert res.status_code == 200
corridor_res = res.json()
print(f"   Corridor points sampled: {corridor_res['total_sampled_points']}, Safety Score: {corridor_res['safety_score_pct']}%, Verdict: {corridor_res['verdict_badge']}")

print("5. Testing alert subscription & SHA-256 OTP...")
sub_req = {
    "email": "mountain.responder@sih2026.gov.in",
    "phone": "+91-9876543210",
    "lat": 30.2450,
    "lon": 78.8900,
    "location_name": "Sirobagarh Outpost",
    "radius_km": 25.0
}
res = client.post("/api/alerts/subscribe", json=sub_req)
assert res.status_code == 200
sub_res = res.json()
otp_code = sub_res["dev_otp_preview"]
print(f"   Subscription OTP issued: {otp_code}")

print("6. Testing OTP verification...")
verify_req = {
    "email": "mountain.responder@sih2026.gov.in",
    "code": otp_code
}
res = client.post("/api/alerts/verify-otp", json=verify_req)
assert res.status_code == 200
print("   OTP verified successfully:", res.json()["status"])

print("7. Testing Geofenced 25km Alert Dispatch...")
dispatch_req = {
    "lat": 30.2451,
    "lon": 78.8920,
    "radius_km": 25.0
}
res = client.post("/api/alerts/dispatch-check", json=dispatch_req)
assert res.status_code == 200
d_res = res.json()
print(f"   Geofenced matched subscribers: {d_res['matched_count']}")

print("8. Testing Assam & North-East Regional Geospatial Pipeline...")
res = client.get("/api/geospatial/assam/analytics")
assert res.status_code == 200
geo_data = res.json()
print(f"   Cataloged Landslides: {geo_data['total_cataloged_landslides']}, High-Risk Districts: {list(geo_data['high_risk_districts'].keys())[:3]}")

res = client.get("/api/geospatial/assam/hotspots")
assert res.status_code == 200
print(f"   Assam Live Hotspots: {res.json()['total']}")

print("9. Testing Weather Timeline Scrubber...")
res = client.get("/api/weather/timeline")
assert res.status_code == 200
print(f"   Timeline intervals: {len(res.json()['steps'])}")

print("10. Testing AI Advisor response...")
ai_req = {"user_query": "What is the evacuation protocol for NH-58 near Sirobagarh?"}
res = client.post("/api/ai/advisor", json=ai_req)
assert res.status_code == 200
print("   AI Advisor Provider:", res.json()["provider"])

print("\n[SUCCESS] ALL 10 BACKEND TESTS PASSED WITH 100% SUCCESS!")
