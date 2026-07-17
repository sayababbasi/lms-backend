import requests
import json
import random

BASE_URL = "http://localhost:8000/api"

# Generate random suffix to avoid unique constraint errors
def get_random_suffix():
    return str(random.randint(1000, 9999))

def get_token():
    try:
        response = requests.post(f"{BASE_URL}/login/", data={'username': 'admin', 'password': 'adminpassword'})
        if response.status_code == 200:
            return response.json()['access']
        print("Login failed:", response.text)
        return None
    except Exception as e:
        print("Connection failed:", e)
        return None

def test_create_student(token):
    suffix = get_random_suffix()
    payload = {
        "user": {
            "username": f"student_{suffix}",
            "email": f"student_{suffix}@example.com",
            "first_name": "Test",
            "last_name": "Student",
            "phone": "1234567890",
            "address": "123 Test St",
            "gender": "M",
            "date_of_birth": "2000-01-01",
            "cnic": f"12345-{suffix}-1"
        },
        "roll_number": f"BSCS-{suffix}",
        "department": "Computer Science",
        "program": "BSCS",
        "semester": "1",
        "section": "A",
        "admission_date": "2024-01-01",
        "guardian_name": "Guardian Test",
        "guardian_contact": "03001234567"
    }
    
    print(f"\n--- Testing Student Creation ({payload['user']['username']}) ---")
    response = requests.post(f"{BASE_URL}/students/", json=payload, headers={'Authorization': f'Bearer {token}'})
    if response.status_code == 201:
        print("✅ Success")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

def test_create_teacher(token):
    suffix = get_random_suffix()
    payload = {
        "user": {
            "username": f"teacher_{suffix}",
            "email": f"teacher_{suffix}@example.com",
            "first_name": "Test",
            "last_name": "Teacher",
            "phone": "1234567890",
            "address": "456 Teacher Ln",
            "gender": "F",
            "date_of_birth": "1985-01-01",
            "cnic": f"12345-{suffix}-2"
        },
        "department": "Mathematics",
        "designation": "Lecturer",
        "qualification": "PhD",
        "specialization": "Algebra",
        "joining_date": "2020-01-01"
    }

    print(f"\n--- Testing Teacher Creation ({payload['user']['username']}) ---")
    response = requests.post(f"{BASE_URL}/teachers/", json=payload, headers={'Authorization': f'Bearer {token}'})
    if response.status_code == 201:
        print("✅ Success")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

def test_create_staff(token):
    suffix = get_random_suffix()
    payload = {
        "user": {
            "username": f"staff_{suffix}",
            "email": f"staff_{suffix}@example.com",
            "first_name": "Test",
            "last_name": "Staff",
            "phone": "1234567890",
            "address": "789 Staff Rd",
            "gender": "O",
            "date_of_birth": "1990-01-01",
            "cnic": f"12345-{suffix}-3"
        },
        "role": "Accountant",
        "designation": "Junior Accountant",
        "joining_date": "2022-01-01"
    }

    print(f"\n--- Testing Staff Creation ({payload['user']['username']}) ---")
    response = requests.post(f"{BASE_URL}/staff/", json=payload, headers={'Authorization': f'Bearer {token}'})
    if response.status_code == 201:
        print("✅ Success")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    token = get_token()
    if token:
        test_create_student(token)
        test_create_teacher(token)
        test_create_staff(token)
