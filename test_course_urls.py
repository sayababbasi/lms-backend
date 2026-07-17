import requests
import json

# Read token from browser localStorage (you'll need to get this from browser dev tools)
# For now, let's just test if the endpoint exists

# Try without auth first to see the error
response = requests.get('http://localhost:8000/api/student/courses/')
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {response.headers}")
print(f"Response Content: {response.text[:500]}")

# Also try the stats endpoint that works
stats_response = requests.get('http://localhost:8000/api/student/dashboard-stats/')
print(f"\n\nStats Status Code: {stats_response.status_code}")
print(f"Stats Response: {stats_response.text[:200]}")

# List all registered URLs
print("\n\nTesting URL existence...")
urls_to_test = [
    '/api/student/courses/',
    '/api/courses/student/courses/',
    '/api/student/stats/',
    '/api/student/dashboard-stats/',
]

for url in urls_to_test:
    try:
        r = requests.get(f'http://localhost:8000{url}')
        print(f"{url}: {r.status_code}")
    except Exception as e:
        print(f"{url}: ERROR - {e}")
