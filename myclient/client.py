import json
import requests
from tabulate import tabulate
import argparse
import random


URL_LIST = "https://newssites.pythonanywhere.com/api/directory/"

class ClientNews():
    # =================================================================================
    #Init
    def __init__(self):
        #initialise session
        self.session = requests.Session()
        self.available_url = []
        self.logged_in_url = None
        self.available_agencies_code = []
        
        #get the list of all agencies
        response = self.session.get(URL_LIST)
        if response.status_code == 200:
            agencies = response.json()

            if isinstance(agencies, list):
                self.agencies = agencies
                for agency in self.agencies:
                    self.available_url.append(agency["url"])
                    self.available_agencies_code.append(agency["agency_code"])

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
    # News
    def news(self, raw_flags):
        parser = argparse.ArgumentParser(description="Parse news command")
        parser.add_argument("-id", dest="id", help="ID of the news agency")
        parser.add_argument("-cat", dest="category", help="Category of the news, can be trivia, tech, art, pol")
        parser.add_argument("-reg", dest="region", help="Region of the news, can be uk, w, eu")
        parser.add_argument("-date", dest="date", help="Date of the news in dd/mm/yyyy")

        try:
            args = parser.parse_args(raw_flags.split())
        except Exception as e:
            print(e)
            return False



        id = "*" if args.id is None else args.id
        category = "*" if args.category is None else args.category
        region = "*" if args.region is None else args.region
        date = "*" if args.date is None else args.date

        print("id ", id)
        print("category ", category)
        print("region ", region)
        print("date ", date)

        agencies_to_get_news_from = []

        # if id is not given, get 20 random agencies
        if id == "*":
            agencies_to_get_news_from = random.sample(self.agencies, 20)

        elif id in self.available_agencies_code:
            for agency in self.agencies:
                if id == agency["agency_code"]:
                    agencies_to_get_news_from.append(agency)
        else:
            print("ID not found. Try again")
        
        if len(agencies_to_get_news_from) > 0:
            for agency in agencies_to_get_news_from:
                url = self.add_https(agency["url"]) + "/api/stories"
                payload = {
                    'story_cat': category,
                    'story_region': region,
                    'story_date': date,
                }
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}

                try:
                    response = self.session.get(url, params=payload, headers=headers)
                # Check if the request was successful (status code 200)
                    if response.status_code == 200:
                        table_data = []
                        
                        data = response.json()

                        # Extract the stories from the JSON response
                        try:
                            stories = data.get('stories', [])

                        except:
                            stories = data

                        for story in stories:
                            story_details = story["story_details"]
                            if len(story_details.split()) < 5:
                                # If detail has less than 3 words, split by characters
                                details_formatted = ''
                                for i, char in enumerate(story_details):
                                    details_formatted += char
                                    if (i + 1) % 16 == 0:
                                        details_formatted += '\n'
                            else:
                                # If detail has 3 or more words, split by words
                                words = story_details.split()
                                details_formatted = ''
                                for i, word in enumerate(words):
                                    details_formatted += word
                                    if (i + 1) % 5 == 0:
                                        details_formatted += '\n'
                                    else:
                                        details_formatted += ' '

                            headline = story["headline"]
                            if len(headline.split()) < 3:
                                # If title has less than 3 words, split by characters
                                headline_formatted = ''
                                for i, char in enumerate(headline):
                                    headline_formatted += char
                                    if (i + 1) % 16 == 0:
                                        headline_formatted += '\n'
                            else:
                                # If title has 3 or more words, split by words
                                words = headline.split()
                                headline_formatted = ''
                                for i, word in enumerate(words):
                                    headline_formatted += word
                                    if (i + 1) % 3 == 0:
                                        headline_formatted += '\n'
                                    else:
                                        headline_formatted += ' '
                            table_data.append([story["key"], headline_formatted,story["story_cat"],story["story_region"], story["author"], story["story_date"], details_formatted])
        
                        print()
                        print(f"News from {agency['agency_name']}")
                        print(tabulate(table_data, headers=["Key", "Headline", "Category", "Region", "Author", "Date", "Details"], tablefmt="heavy_grid"))
                        print()
                        table_data = []

                    else:
                        print(f"Could not get news from {agency['agency_name']}. Status code: {response.status_code}")

                except:
                    print(f"Could not get in contact with {url}")





            
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
    # Delete
    def delete(self, possible_key:str):
        if self.logged_in_url:
            key = possible_key.split()[0]
            url_with_key =  self.logged_in_url + "/api/stories/" + str(key)
            response = self.session.delete(url=url_with_key)

            if response.status_code == 200:
                print(response.text)
                print(f"Story n {key} from {self.logged_in_url} has been deleted")
            else:
                print(f"Unable to process the request. Status code: {response.status_code}")
            
        else:
            print("You need to be logged in in order to delete a story")

            
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
        if not url.startswith("https://") and not url.startswith("http://"):
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
        
    elif "news" in user_prompt:
        client.news(user_prompt[5:])
        
    elif user_prompt == "list":
        client.list()

    elif "delete " in user_prompt:

        client.delete(user_prompt[7:])

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
