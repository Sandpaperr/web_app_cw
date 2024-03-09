import requests
import json
url = "http://127.0.0.1:8000/api/login/"

data = {"username": "gerardo", "password": "Acquarola99!"}
response = requests.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
print(response.text)

# Create a dictionary representing your data
data = {
    "headline": "Sunday Sabroso Academy",
    "category": "trivia",
    "region": "uk",
    "details": "sabroso is back with salsa on 2 in Leeds. Join us"
}

# Serialize the dictionary to a JSON string
json_payload = json.dumps(data)

url = "http://127.0.0.1:8000/api/stories/"
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json_payload, headers=headers)
print(response.text)
