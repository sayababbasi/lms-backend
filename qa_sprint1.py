import requests
import json
import time

BASE_URL = "https://api.lms.revoticai.com"
USERNAME = "qa_admin"
PASSWORD = "QAPassword123!"

print(f"--- STARTING QA SPRINT 1 API AUDIT against {BASE_URL} ---")

# 1. Environment & SSL Audit
try:
    print("Testing SSL/HTTPS and CORS headers on API Root...")
    resp = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"API Root Status: {resp.status_code}")
    print(f"Server Header: {resp.headers.get('Server', 'Unknown')}")
    print(f"CORS Origin: {resp.headers.get('Access-Control-Allow-Origin', 'Missing!')}")
except requests.exceptions.SSLError:
    print("SSL Error! HTTPS is broken.")
except Exception as e:
    print(f"Connection Error: {e}")

# 2. Authentication & JWT
print("\nTesting Authentication (Login & JWT)...")
login_data = {"username": USERNAME, "password": PASSWORD}
login_resp = requests.post(f"{BASE_URL}/api/login/", json=login_data)

access_token = None
refresh_token = None

if login_resp.status_code == 200:
    print("Login SUCCESS (200 OK)")
    data = login_resp.json()
    access_token = data.get("access")
    refresh_token = data.get("refresh")
    print(f"Access Token retrieved: {bool(access_token)}")
    
    # Test Unauthorized Access
    print("\nTesting Unauthorized Access...")
    users_resp = requests.get(f"{BASE_URL}/api/users/")
    if users_resp.status_code == 401:
        print("Unauthorized Access Blocked (401 OK)")
    else:
        print(f"SECURITY VULNERABILITY! Unauthorized access allowed: {users_resp.status_code}")
        
    # Test Authorized Access
    print("\nTesting Authorized Access (Admin Route)...")
    headers = {"Authorization": f"Bearer {access_token}"}
    users_auth_resp = requests.get(f"{BASE_URL}/api/users/", headers=headers)
    print(f"Authorized Access Status: {users_auth_resp.status_code}")

    # Test Refresh Token
    print("\nTesting Token Refresh...")
    refresh_resp = requests.post(f"{BASE_URL}/api/token/refresh/", json={"refresh": refresh_token})
    print(f"Refresh Token Status: {refresh_resp.status_code}")
    
else:
    print(f"Login FAILED: {login_resp.status_code}")
    print(login_resp.text)

# 3. Security (Phase 11) - Basic Injection Tests
print("\nTesting SQL Injection & XSS (Phase 11)...")
sqli_payload = {"username": "admin' OR '1'='1", "password": "password"}
sqli_resp = requests.post(f"{BASE_URL}/api/login/", json=sqli_payload)
print(f"SQL Injection Login Status (Expect 400/401): {sqli_resp.status_code}")

xss_payload = {"username": "<script>alert('xss')</script>", "password": "password"}
xss_resp = requests.post(f"{BASE_URL}/api/login/", json=xss_payload)
print(f"XSS Login Status (Expect 400/401): {xss_resp.status_code}")

print("\n--- SPRINT 1 QA SCRIPT COMPLETE ---")
