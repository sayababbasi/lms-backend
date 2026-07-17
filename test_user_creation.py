import requests
import json

BASE_URL = "http://localhost:8000/api"

def get_token():
    try:
        # Assuming admin credentials from previous sessions or default
        response = requests.post(f"{BASE_URL}/login/", data={'username': 'admin', 'password': 'adminpassword'})
        if response.status_code == 200:
            return response.json()['access']
        print("Login failed:", response.text)
        return None
    except Exception as e:
        print("Connection failed:", e)
        return None

def create_student(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Payload matching the structure sent by Frontend UserModal
    payload = {
        "user": {
            "username": "teststudent101",
            "email": "student101@example.com",
            "first_name": "Test",
            "last_name": "Student",
            "phone": "1234567890",
            "address": "123 Campus Rd",
            "gender": "M",
            "date_of_birth": "2000-01-01",
            "cnic": "12345-6789012-3"
        },
        # Profile fields
        "roll_number": "BSCS-2024-101",
        "department": "Computer Science",
        "program": "BSCS",
        "semester": "1st",
        "section": "A",
        "guardian_name": "Test Guardian",
        "guardian_contact": "0987654321"
    }

    print("Creating student...")
    response = requests.post(f"{BASE_URL}/students/", headers=headers, json=payload)
    
    if response.status_code == 201:
        print("SUCCESS: Student created successfully!")
        print(json.dumps(response.json(), indent=2))
        return True
    else:
        print(f"FAILED: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    token = get_token()
    if token:
        create_student(token)
