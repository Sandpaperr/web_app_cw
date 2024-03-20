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
        self.available_url = []
        
        #get the list of all agencies
        response = session.get(URL_LIST)
        if response.status_code == 200:
            agencies = response.json()
            if isinstance(agencies, list):
                self.agencies = agencies
                for agency in self.agencies:
                    self.available_url.append(agency["url"])

            else:
                raise AssertionError("Expected a list when receiving data but it's not")
        else:
            raise RuntimeError("Could not get any data from the API. Try later")
    
    def login(self, possible_url: str) -> str:
        #log-in into a news agency
        #TODO: can I login in more than one agency at the time
        if possible_url in self.available_url:
            username = input("Username: ")
            password = input("Password: ")
        

    
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
    
    def print_commands(self):
        print("Available commands:")
        print("-" * 40)
        
        commands = [
            ("login url", "Log-in into a specific news agency. Substitute url with the URL of the service."),
            ("logout", "Log out from the current session."),
            ("post", "Post a new story."),
            ("news -id= -cat= -reg= -date=", "Request news stories from one or multiple news agencies."),
            ("flags", "Print out more details about news flags."),
            ("list", "List all the agencies stored in the main directory."),
            ("delete key", "Delete news story. Substitute key with the story key."),
            ("quit", "Quit the program.")
        ]
        
        for command, description in commands:
            print(f"{command:<30} {description}")




client = ClientNews()

client.print_commands()
while True:

    user_prompt = input("Insert command: ")

    if "login " in user_prompt:
        words = user_prompt.split()

        if len(words) == 2:
            if words[0] == "login":
                if "pythonanywhere.com" in words[1]:
                    answer = login(words[1])
                    print(answer)
                else:
                    print("Only allowed to use url from pythonanywhere.com for this coursework")
            else:
                print("bad argument when checking login. try again. e.g. login sre31r.pythonanywhere.com")
        else:
            print("login bad argument, try again. e.g. login sre31r.pythonanywhere.com")


        
    elif user_prompt == "logout":
        print("in logout")
        
    elif user_prompt == "post":
        print("in post")
        
    elif "news " in user_prompt:
        print("in news")
        
    elif user_prompt == "list":
        client.list()

    elif "delete " in user_prompt:
        print("in delete")

    elif user_prompt == "flags":
        print()
        print("All flags are optional")
        print("(id flag) id is the id of the news agency e.g. -id='JAD05'")
        print("(cat flag) cat is the news category. if specified e.g. -cat='tech' returns results from that category")
        print("(reg flag) the region of the required stories, e.g -reg='uk'")
        print("(date flag) the date in dd/mm/yyyy after which a story has been added. e.g. -date='12/2/2019'")
        print()
    elif user_prompt == "show":
        client.print_commands()

    elif user_prompt == "quit":
        break

    else:
        print("invalid command, try again")
    
    print()
    print("use command 'show' to show all the available commands")

    
