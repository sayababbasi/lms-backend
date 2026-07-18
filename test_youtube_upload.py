import requests
import os

BASE_URL = "https://api.lms.revoticai.com/api"
ADMIN_USER = "lmsadmin"
ADMIN_PASS = "lmsadmin@revoticai"

print("Authenticating...")
res = requests.post(f"{BASE_URL}/login/", json={"username": ADMIN_USER, "password": ADMIN_PASS})
if res.status_code != 200:
    print("Login failed")
    exit(1)

token = res.json().get('access')

print("Fetching a lesson ID...")
res = requests.get(f"{BASE_URL}/lessons/", headers={"Authorization": f"Bearer {token}"})
if res.status_code == 200 and len(res.json().get('results', [])) > 0:
    lesson_id = res.json()['results'][0]['id']
    print(f"Found lesson {lesson_id}")
else:
    print("No lessons found or failed to fetch. Creating a dummy lesson...")
    res_module = requests.get(f"{BASE_URL}/modules/", headers={"Authorization": f"Bearer {token}"})
    module_id = res_module.json()['results'][0]['id'] if len(res_module.json().get('results', [])) > 0 else 1
    res_lesson = requests.post(f"{BASE_URL}/lessons/", json={"title": "Test Lesson", "module_id": module_id, "order": 1}, headers={"Authorization": f"Bearer {token}"})
    lesson_id = res_lesson.json()['id']
    print(f"Created dummy lesson {lesson_id}")

print(f"Uploading video to lesson {lesson_id}...")
with open("C:/Users/saqib/.gemini/antigravity-ide/brain/18043b1a-761b-4f48-a005-4dab92a77855/scratch/test_video.mp4", "rb") as f:
    files = {'video': ('test_video.mp4', f, 'video/mp4')}
    data = {'lessonId': lesson_id, 'title': 'Test Upload', 'description': 'Testing from script'}
    try:
        res = requests.post(
            f"{BASE_URL}/youtube/upload/",
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data,
            timeout=120
        )
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"Upload request failed: {e}")
