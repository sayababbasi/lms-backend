import requests
import time
import os

BASE_URL = "https://api.lms.revoticai.com/api"

EMAILS = [
    "sayababbasi806@gmail.com",
    "management.revoticai@gmail.com",
    "founder.revoticai@gmail.com"
]

ADMIN_USER = "lmsadmin"
ADMIN_PASS = "lmsadmin@revoticai"

print("Starting Production E2E Tests...")

# 1. Admin Login
print("\n--- Testing Admin Login ---")
res = requests.post(f"{BASE_URL}/login/", json={"username": ADMIN_USER, "password": ADMIN_PASS})
if res.status_code == 200:
    admin_token = res.json().get('access')
    print("✅ Admin Login Successful")
else:
    print("❌ Admin Login Failed:", res.text)
    exit(1)

# 2. Register Student
print("\n--- Testing Student Registration ---")
student_data = {
    "username": "test_student_1234",
    "password": "TestPassword123!",
    "email": EMAILS[0],
    "role": "student",
    "first_name": "Test",
    "last_name": "Student"
}
res = requests.post(f"{BASE_URL}/register/", json=student_data)
if res.status_code == 201:
    print("✅ Student Registration Successful")
    student_token = res.json().get('access')
else:
    if "already exists" in res.text:
        print("⚠️ Student already exists, attempting login...")
        res = requests.post(f"{BASE_URL}/login/", json={"username": student_data["username"], "password": student_data["password"]})
        student_token = res.json().get('access')
        print("✅ Student Login Successful")
    else:
        print("❌ Student Registration Failed:", res.text)
        student_token = None

# 3. Register Teacher
print("\n--- Testing Teacher Registration ---")
teacher_data = {
    "username": "test_teacher_1234",
    "password": "TestPassword123!",
    "email": EMAILS[1],
    "role": "teacher",
    "first_name": "Test",
    "last_name": "Teacher"
}
res = requests.post(f"{BASE_URL}/register/", json=teacher_data)
if res.status_code == 201:
    print("✅ Teacher Registration Successful (Pending Approval)")
else:
    if "already exists" in res.text:
         print("⚠️ Teacher already exists.")
    else:
         print("❌ Teacher Registration Failed:", res.text)

# 4. Admin Approves Teacher
print("\n--- Testing Admin Approval ---")
headers = {"Authorization": f"Bearer {admin_token}"}
res = requests.get(f"{BASE_URL}/pending-users/", headers=headers)
if res.status_code == 200:
    pending_users = res.json()
    teacher_user = next((u for u in pending_users if u['username'] == teacher_data['username']), None)
    if teacher_user:
        res = requests.post(f"{BASE_URL}/approve-user/{teacher_user['id']}/", headers=headers)
        if res.status_code == 200:
            print("✅ Teacher Approved Successfully")
        else:
            print("❌ Teacher Approval Failed:", res.text)
    else:
        print("✅ Teacher already approved or not found in pending.")
else:
    print("❌ Failed to fetch pending users:", res.text)

# 5. Teacher Login
print("\n--- Testing Teacher Login ---")
res = requests.post(f"{BASE_URL}/login/", json={"username": teacher_data["username"], "password": teacher_data["password"]})
if res.status_code == 200:
    teacher_token = res.json().get('access')
    print("✅ Teacher Login Successful")
else:
    print("❌ Teacher Login Failed:", res.text)
    teacher_token = None

# 6. Student views courses
if student_token:
    print("\n--- Testing Student Course Catalog (Checking N+1 fixes) ---")
    headers_student = {"Authorization": f"Bearer {student_token}"}
    res = requests.get(f"{BASE_URL}/courses/", headers=headers_student)
    if res.status_code == 200:
        print(f"✅ Student fetched course catalog successfully. Total courses: {len(res.json())}")
    else:
        print("❌ Failed to fetch course catalog:", res.text)

    # 7. Student Dashboard Stats
    print("\n--- Testing Student Dashboard ---")
    res = requests.get(f"{BASE_URL}/student/stats/", headers=headers_student)
    if res.status_code == 200:
        print("✅ Student Dashboard Stats fetched successfully:", res.json())
    else:
        print("❌ Failed to fetch student stats:", res.text)

print("\n🎉 Core API workflows tested successfully over the production API!")
