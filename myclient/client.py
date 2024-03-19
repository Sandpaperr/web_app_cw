import json
import requests
import shutil
from tabulate import tabulate

# Get the size of the terminal window
terminal_width, _ = shutil.get_terminal_size()

# #TODO: Use / when interfacing to news aggregator
# #TODO: Client is a loop and take args from promt

# #login
# url = "https://sc21l2r.pythonanywhere.com/api/login"
# session = requests.Session()
# session.headers.update({'User-Agent': "login and post a story"})
# data = {"username": "gerardo", "password": "Acquarola99!"}
# response = session.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
# print(response.text)




# # login
# url = "https://sc21l2r.pythonanywhere.com/api/login"
# session.headers.update({'User-Agent': "login and post a story"})
# data = {"username": "gerardo", "password": "Acquarola99!"}
# response = session.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
# print(response.text)

# # logout
# url = "https://sc21l2r.pythonanywhere.com/api/logout"
# session.headers.update({'User-Agent': "logout"})
# response = session.post(url=url, headers={'Content-Type': 'text/plain'})
# print(response.text)

# # login
# url = "https://sc21l2r.pythonanywhere.com/api/login"
# session.headers.update({'User-Agent': "login and post a story"})
# data = {"username": "ammar", "password": "Leeds2024!"}
# response = session.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
# print(response.text)





# # post story
# data = {
#     "headline": "The leader once said..",
#     "category": "tech",
#     "region": "uk",
#     "details": "if you get hurt, you need to REST"
# }

# # Serialize the dictionary to a JSON string
# json_payload = json.dumps(data)

# url = "https://sc21l2r.pythonanywhere.com/api/stories"
# headers = {'Content-Type': 'application/json'}
# response = session.post(url, data=json_payload, headers=headers)
# print(response.text)





# # Get stories
# url = "https://sc21l2r.pythonanywhere.com/api/stories"
# payload = {
#     'story_cat': '*',
#     'story_region': '*',
#     'story_date': '',
# }
# headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# response = session.get(url, params=payload, headers=headers)
# # Check if the request was successful (status code 200)

# if response.status_code == 200:
#     
#     data = response.json()

#     # Extract the stories from the JSON response
#     stories = data.get('stories', [])
#     for story in stories:
#         print()
#         print(story)
#         print()


# # # Delete
# # url = "https://sc21l2r.pythonanywhere.com/api/stories/"
# # key = 5
# # url_with_key =  url + str(key)
# # response = session.delete(url=url_with_key)


# # for i in range (55, 67):
# #     url_with_key = url + str(i)
# #     response = session.delete(url=url_with_key)
# #     print(response.text)

URL_LIST = "https://newssites.pythonanywhere.com/api/directory/"

class ClientNews():
    def __init__(self):
        #initialise session
        session = requests.Session()
        
        #get the list of all agencies
        response = session.get(URL_LIST)
        if response.status_code == 200:
            agencies = response.json()
            if isinstance(agencies, list):
                self.agencies = agencies
            else:
                raise AssertionError("Expected a list when receiving data but it's not")
        else:
            raise RuntimeError("Could not get any data from the API. Try later")
    
    def list(self):
        table_data = []

        for agency in self.agencies:
            # take the terminal width and calculate the space the grid can occupy
            # max width per column
            max_width = (terminal_width - 4) // 3  

            # check if agencies names are longer than max_idth. If so, print the remaining next row
            split_agency_name = [agency["agency_name"][i:i+max_width] for i in range(0, len(agency["agency_name"]), max_width)]
            agency_name = '\n'.join(split_agency_name)

            url = agency["url"][:max_width] if len(agency["url"]) > max_width else agency["url"]
            agency_code = agency["agency_code"][:max_width] if len(agency["agency_code"]) > max_width else agency["agency_code"]
            table_data.append([agency_name, url, agency_code])

        # Print the tabulated data
        print(tabulate(table_data, headers=["Agency Name", "URL", "Agency Code"], tablefmt="grid"))




client = ClientNews()


client.list()
