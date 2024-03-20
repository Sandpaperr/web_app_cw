import json
import requests
import shutil
from tabulate import tabulate
from bs4 import BeautifulSoup
from prettytable import PrettyTable, ALL



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
    # =================================================================================
    #Init
    def __init__(self):
        #initialise session
        self.session = requests.Session()
        self.available_url = []
        self.logged_in_url = None
        
        #get the list of all agencies
        response = self.session.get(URL_LIST)
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
    # =================================================================================
        
    # =================================================================================
    # Log-in
    def login(self, possible_url: str):

        #log-in into a news agency
        # check if logged in already
        # check if url is in list of available url
        if self.logged_in_url is None:
            #add https if missing and cut everything after .com
            url = self.add_https(possible_url)
            if url in self.available_url:
                #setting the path
                log_in_url = url + "/api/login"

                username = input("Username: ")
                password = input("Password: ")

                self.session.headers.update({'User-Agent': "python"})
                data = {"username": str(username), "password": str(password)}
                response = self.session.post(url=log_in_url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})                
                print(response.text)
                if response.status_code == 200:
                    self.logged_in_url = url
                    print(f"logged in into {url}. Welcome")
                    
                else:
                    print(f"Can't log in. Status code: {response.status_code}")
                    # I tried to also print the response.text, but it's an html so I cannot
            else:
                print("url not present in the list")
        else:
            print("You need to log out before you can log in into another news agency")
    
    # =================================================================================
    
    # =================================================================================
    # Logout
    def logout(self):
        if self.logged_in_url:
            url = self.logged_in_url + "api/logout"

            self.session.headers.update({'User-Agent': "logout"})
            response = self.session.post(url=url, headers={'Content-Type': 'text/plain'})

            if response.status_code == 200:
                self.logged_in_url = None
                print(response.text)
            else:
                (f"Error while logging out: {response.status_code}")

        else:
            print("You need to log in first")
    # =================================================================================
   
    # =================================================================================
    #Post   
    def post(self):
        if self.logged_in_url:
            url = self.logged_in_url + "/api/stories"
            headline = input("Headline: ")
            category = input("Category: ")
            region = input("Region: ")
            details = input("Details: ")
            data = {
                "headline": headline,
                "category": category,
                "region": region,
                "details": details,
            }

            # Serialize the dictionary to a JSON string
            json_payload = json.dumps(data)

            
            headers = {'Content-Type': 'application/json'}
            response = self.session.post(url, data=json_payload, headers=headers)
            if response.status_code == 201:
                print(response.text)
            else:
                print(f"Something went wrong while posting. Status code: {response.status_code}")
            
        else:
            print("You need to log in first")
    # =================================================================================
            
    # =================================================================================
    # list
    def list(self):
        table_data = []
        fragmented_entries = []
        fragmented_size = len(self.agencies) // 10

        #I tried to print all at once but if I print the agencies at once with the grid and 
        #fancy formats, it print only 40 of them
        #probably the print statement has a limit of how many character it can print at once
        fragmented_entries.append(self.agencies[:fragmented_size])
        fragmented_entries.append(self.agencies[fragmented_size: 2*fragmented_size])
        fragmented_entries.append(self.agencies[2*fragmented_size: 3*fragmented_size])
        fragmented_entries.append(self.agencies[3*fragmented_size: 4*fragmented_size])
        fragmented_entries.append(self.agencies[4*fragmented_size: 5*fragmented_size])
        fragmented_entries.append(self.agencies[5*fragmented_size: 6*fragmented_size])
        fragmented_entries.append(self.agencies[6*fragmented_size: 7*fragmented_size])
        fragmented_entries.append(self.agencies[7*fragmented_size: 8*fragmented_size])
        fragmented_entries.append(self.agencies[8*fragmented_size: 9*fragmented_size])
        fragmented_entries.append(self.agencies[9*fragmented_size:])

        colalign = ["right", "left", "left"]
        page = 1
        for frag_agencies in fragmented_entries:

            for agency in frag_agencies:
                table_data.append([agency["agency_name"], agency["url"], agency["agency_code"]])
            
            print()
            print(f"page {page}")
            print(tabulate(table_data, headers=["Agency Name", "URL", "Agency Code"], tablefmt="heavy_grid", colalign=colalign))
            print()
            table_data = []
            page += 1
    # =================================================================================
            
    # =================================================================================
    # Print Commands
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
    
    def add_https(self, url):
        if not url.startswith("https://"):
            url = "https://" + url
        index = url.find('.com')
        if index != -1:  # If '.com' is found
            return str(url[:index + 4])
        else:
            return None




client = ClientNews()

client.print_commands()
while True:

    user_prompt = input("Insert command: ")

    if "login " in user_prompt:
        words = user_prompt.split()

        if len(words) == 2:
            if words[0] == "login":
                if "pythonanywhere.com" in words[1]:
                    client.login(words[1])
                else:
                    print("Only allowed to use url from pythonanywhere.com for this coursework")
            else:
                print("bad argument when checking login. try again. e.g. login sre31r.pythonanywhere.com")
        else:
            print("login bad argument, try again. e.g. login sre31r.pythonanywhere.com")


        
    elif user_prompt == "logout":
        client.logout()
        
    elif user_prompt == "post":
        client.post()
        
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

    

# url = URL_LIST

# # TODO: method for checking and adding "https//"

# data = {"agency_name": "Leandro's News Agency", "url":"https://sc21l2r.pythonanywhere.com", "agency_code": "LER99"}
# data_j = json.dumps(data)
# headers = {'Content-Type': 'application/json'}
# response = requests.post(url=url,data=data_j, headers=headers)
# if response.status_code == 201:
#     print("Created, oleeeee")
# else:
#     print(response.status_code)