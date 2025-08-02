import requests

# Test the login endpoint directly
url = "http://localhost:5001/api/login"
data = {
    "username": "admin",
    "password": "admin123"
}

response = requests.post(url, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")