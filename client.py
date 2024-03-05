import requests

url = "http://127.0.0.1:8000/api/login/"

data = {"username": "Leandro", "password": "ambarabaciccicocco"}
response = requests.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
print(response.text)