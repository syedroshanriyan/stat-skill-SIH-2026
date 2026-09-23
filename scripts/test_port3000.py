import urllib.request
import json

print("Testing Port 3000 Unified Platform:")

# 1. Landing Page
with urllib.request.urlopen("http://localhost:3000/") as r:
    print(f"1. Landing Page: {r.status} OK")

# 2. Login Gateway
with urllib.request.urlopen("http://localhost:3000/login") as r:
    print(f"2. Login Gateway: {r.status} OK")

# 3. Proxied Health
with urllib.request.urlopen("http://localhost:3000/api/v1/health") as r:
    data = json.loads(r.read().decode())
    print(f"3. Health via Port 3000: {r.status} - {data}")

# 4. Proxied Docs
with urllib.request.urlopen("http://localhost:3000/docs") as r:
    print(f"4. Swagger Docs via Port 3000: {r.status} OK")

# 5. Proxied Live Auth (JSON body)
auth_payload = json.dumps({"email": "ananya.rao@mospi.gov.in", "password": "Password123"}).encode()
req = urllib.request.Request(
    "http://localhost:3000/api/v1/auth/login",
    data=auth_payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode())
    print(f"5. Live Auth via Port 3000: {r.status} - User: {data['display_name']} ({data['email']})")
    print(f"   Track: {data['track']} | Role: {data['role']}")
    print(f"   JWT Token: {data['access_token'][:35]}...")

print("\nALL PORT 3000 UNIFIED ENDPOINTS VERIFIED AND WORKING!")
