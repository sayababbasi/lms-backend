import requests
import json
import os

BASE_URL = "http://localhost:8000"
USERNAME = "qa_admin"
PASSWORD = "QAPassword123!"

print("Logging in...")
login_resp = requests.post(f"{BASE_URL}/api/login/", json={"username": USERNAME, "password": PASSWORD})
access_token = login_resp.json().get("access")
headers = {"Authorization": f"Bearer {access_token}"}

print("Fetching Teachers...")
teachers_resp = requests.get(f"{BASE_URL}/api/users/?is_teacher=true", headers=headers)
teachers = teachers_resp.json().get("results", [])
teacher_id = teachers[0]["id"] if teachers else None

print(f"Creating Course with Teacher ID: {teacher_id}")

course_data = {
    'title': 'Advanced Software Engineering',
    'code': 'SE401',
    'description': 'A comprehensive course on building scalable enterprise applications.',
    'credit_hours': 4,
    'passing_percentage': 60,
    'status': 'PUBLISHED',
    'semester': 'Spring 2027',
    'category': 'Computer Science',
    'prerequisites': 'SE301, Data Structures',
    'teacher_id': teacher_id,
    'teacher_ids': [teacher_id] if teacher_id else []
}

# Emulate frontend multipart/form-data
from requests_toolbelt.multipart.encoder import MultipartEncoder

# We don't have a thumbnail for this test, but we can send it as form-data
m = MultipartEncoder(fields={
    k: (str(v) if not isinstance(v, list) else str(v[0])) for k, v in course_data.items()
})
headers['Content-Type'] = m.content_type

create_resp = requests.post(f"{BASE_URL}/api/courses/", headers=headers, data=m)

if create_resp.status_code == 201:
    print("SUCCESS: Course Created!")
    print(json.dumps(create_resp.json(), indent=2))
    
    # Clean up
    requests.delete(f"{BASE_URL}/api/courses/{create_resp.json().get('id')}/", headers={"Authorization": f"Bearer {access_token}"})
else:
    print(f"FAILED: {create_resp.status_code}")
    print(create_resp.text)
