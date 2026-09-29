import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("=" * 70)
print("RECALL-OPS PHASE 2: FASTAPI BACKEND & HINDSIGHT VERIFICATION")
print("=" * 70)

# 1. Test GET /
print("\n[1/6] Testing GET / ...")
res_root = client.get("/")
print(f"Status Code: {res_root.status_code}")
print(f"Response: {res_root.json()}")
assert res_root.status_code == 200
assert res_root.json() == {"name": "Recall-Ops", "status": "running"}

# 2. Test GET /health
print("\n[2/6] Testing GET /health ...")
res_health = client.get("/health")
print(f"Status Code: {res_health.status_code}")
print(f"Response: {res_health.json()}")
assert res_health.status_code == 200
assert res_health.json() == {"status": "healthy"}

# 3. Test POST /api/incidents/analyze (Primary Incident)
print("\n[3/6] Testing POST /api/incidents/analyze (payment-api HTTP 503) ...")
payload_1 = {
    "service": "payment-api",
    "severity": "HIGH",
    "error": "HTTP 503 Service Unavailable",
    "logs": "Database connection pool exhausted.",
    "deployment_version": "payment-service v2.4.1"
}
res_1 = client.post("/api/incidents/analyze", json=payload_1)
print(f"Status Code: {res_1.status_code}")
data_1 = res_1.json()
print(f"Success: {data_1.get('success')}")
print(f"Memories Retrieved from Hindsight: {len(data_1.get('memories', []))}")
if data_1.get('memories'):
    print(f"   -> Top Hindsight Memory snippet: {data_1['memories'][0].get('text', '')[:120]}...")
print(f"AI Analysis Root Cause: {data_1.get('analysis', {}).get('likely_root_cause')}")
print(f"AI Recommended Actions: {data_1.get('analysis', {}).get('recommended_actions')}")
assert res_1.status_code == 200
assert data_1["success"] is True

# 4. Test POST /api/incidents/analyze (Semantically Similar Incident)
print("\n[4/6] Testing POST /api/incidents/analyze (order-api differently worded query) ...")
payload_2 = {
    "service": "order-api",
    "severity": "HIGH",
    "error": "HTTP 503",
    "logs": "Unable to obtain database connection. Connection pool timeout.",
    "deployment_version": "order-service v3.1.0"
}
res_2 = client.post("/api/incidents/analyze", json=payload_2)
print(f"Status Code: {res_2.status_code}")
data_2 = res_2.json()
print(f"Success: {data_2.get('success')}")
print(f"Memories Retrieved: {len(data_2.get('memories', []))}")
assert res_2.status_code == 200

# 5. Test POST /api/incidents/resolve (Hindsight Retain)
print("\n[5/6] Testing POST /api/incidents/resolve (Retain in Hindsight) ...")
payload_resolve = {
    "incident_id": "INC-1042",
    "service": "payment-api",
    "error": "HTTP 503",
    "root_cause": "Connection leak introduced in v2.4.1 pool handler",
    "resolution": "Rolled back to v2.4.0 and restarted instances",
    "outcome": "Service recovered",
    "resolution_time": 11
}
res_resolve = client.post("/api/incidents/resolve", json=payload_resolve)
print(f"Status Code: {res_resolve.status_code}")
print(f"Response: {res_resolve.json()}")
assert res_resolve.status_code == 200
assert res_resolve.json()["success"] is True

# 6. Test GET /api/incidents/history
print("\n[6/6] Testing GET /api/incidents/history ...")
res_hist = client.get("/api/incidents/history")
print(f"Status Code: {res_hist.status_code}")
print(f"Total Stored Memories: {len(res_hist.json().get('memories', []))}")
assert res_hist.status_code == 200

print("\n" + "=" * 70)
print("PHASE 2 BACKEND VERIFICATION PASSED ALL 6 TESTS END-TO-END!")
print("=" * 70)
