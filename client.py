import requests
import json

#login
url = "http://127.0.0.1:8000/api/login/"
session = requests.Session()
session.headers.update({'User-Agent': "login and post a story"})
data = {"username": "gerardo", "password": "Acquarola99!"}
response = session.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
print(response.text)


# logout
url = "http://127.0.0.1:8000/api/logout/"
session.headers.update({'User-Agent': "logout"})
response = session.post(url=url)
print(response.text)


# login
url = "http://127.0.0.1:8000/api/login/"
session = requests.Session()
session.headers.update({'User-Agent': "login and post a story"})
data = {"username": "gerardo", "password": "Acquarola99!"}
response = session.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
print(response.text)


# post story
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
response = session.post(url, data=json_payload, headers=headers)
print(response.text)



# Get stories
url = "http://127.0.0.1:8000/api/stories/"
payload = {
    'story_cat': '*',
    'story_region': '*',
    'story_date': '',
}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = session.get(url, params=payload, headers=headers)
# Check if the request was successful (status code 200)
print(response.status_code)
print(response.text)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    
    # Extract the stories from the JSON response
    stories = data.get('stories', [])
    print(stories)
    for story in stories:
        print()
        print(story)
        print()


# # Delete
# url = "http://127.0.0.1:8000/api/stories/"
# key = 5
# url_with_key =  url + str(key)
# response = session.delete(url=url_with_key)
# print(response.text)

# for i in range (1, 13):
#     url_with_key = url + str(i)
#     response = session.delete(url=url_with_key)
#     print(response.text)


