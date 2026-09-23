import urllib.request
import json

users = [
    ("ananya.rao@mospi.gov.in", "Password123", "Government"),
    ("neha.sharma@datatech.io", "Password123", "Industry"),
    ("arjun.mehta@univ.edu.in", "Password123", "Academia"),
    ("admin@statskill.gov.in", "Password123", "Admin")
]

print("Testing all 4 Demo Logins via Port 3000 Reverse Proxy:")
for email, pwd, role in users:
    payload = json.dumps({"email": email, "password": pwd}).encode()
    req = urllib.request.Request(
        "http://localhost:3000/api/v1/auth/login",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode())
        print(f"  [200 OK] {res['display_name']} ({res['email']}) -> Track: {res['track']} | Role: {res['role']}")

print("All 4 demo profiles successfully verified through port 3000!")
