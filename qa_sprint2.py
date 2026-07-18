import requests
import json
import io

BASE_URL = "https://api.lms.revoticai.com"
USERNAME = "qa_admin"
PASSWORD = "QAPassword123!"

print(f"--- STARTING QA SPRINT 2 API AUDIT against {BASE_URL} ---")

# Login to get token
login_resp = requests.post(f"{BASE_URL}/api/login/", json={"username": USERNAME, "password": PASSWORD})
access_token = login_resp.json().get("access")
headers = {"Authorization": f"Bearer {access_token}"}

# 1. Phase 3: Email System (Test Admin Email Log API)
print("\nTesting Email System Admin API...")
emails_resp = requests.get(f"{BASE_URL}/api/notifications/email-logs/statistics/", headers=headers)
if emails_resp.status_code == 200:
    stats = emails_resp.json()
    print(f"Email System OK! Success Rate: {stats.get('success_rate')}% | Total: {stats.get('total')}")
else:
    print(f"Email System Admin API failed: {emails_resp.status_code}")

# 2. Phase 4: File Storage (Upload test)
print("\nTesting Supabase S3 File Storage...")
# Create a dummy image file in memory
dummy_file = io.BytesIO(b'dummy pdf content')
dummy_file.name = 'qa_test_file.pdf'
files = {'profile_picture': ('qa_test_file.pdf', dummy_file, 'application/pdf')}

# Since we don't have a direct file upload endpoint, we can test by creating a course with a thumbnail
print("Testing File Upload to Supabase (Creating Course with Thumbnail)...")
course_data = {
    'title': 'QA Storage Test Course',
    'code': 'QA101',
    'description': 'Test upload to Supabase',
}
upload_resp = requests.post(f"{BASE_URL}/api/courses/", headers=headers, data=course_data, files={'thumbnail': ('test.jpg', b'fake_image_data', 'image/jpeg')})
if upload_resp.status_code in [200, 201]:
    print("Storage Upload SUCCESS!")
    course_id = upload_resp.json().get('id')
    # Cleanup
    requests.delete(f"{BASE_URL}/api/courses/{course_id}/", headers=headers)
else:
    print(f"Storage Upload FAILED: {upload_resp.status_code} - {upload_resp.text}")

# 3. Phase 14: Error Testing
print("\nTesting Phase 14 Error Handling...")
print("Triggering 404...")
resp_404 = requests.get(f"{BASE_URL}/api/non_existent_route/", headers=headers)
print(f"404 Handled: {resp_404.status_code == 404}")

print("Triggering 403 (Student attempting to access admin route)...")
# Note: we need a student token to test this, skipping for now in automated script

print("Triggering Expired JWT...")
bad_headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjF9.signature"}
resp_exp = requests.get(f"{BASE_URL}/api/users/", headers=bad_headers)
print(f"Expired JWT Handled: {resp_exp.status_code == 401}")

print("\n--- SPRINT 2 QA SCRIPT COMPLETE ---")
