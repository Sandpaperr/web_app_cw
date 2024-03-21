News Acency by Leandro Russo sc21l2r

I. Instruction for the client:
to run the client program, don't add any argments after the file.
Run it normally using client.py.

While running, you are asked to insert a command.
Commands from the coursework requirements:
    login url:
        login into the agency  at "url". The program prompts the user to enter username and password
    logout:
        logout from the logged in agency
    post: 
        the program prompts the user to insert headline, category, region and details. Client can only post to the logged in agency

    news [-id=] [-cat=] [-reg=] [-date=]: 
        retrive and print news from one or multiple agencies.
        All the flags are optional. 
        id: agency_id. if specified, retrive news from that agency, otherwise from 20 random agencies.
        cat: category. it can be art, tech, pol, trivia. If not specified, all categories are included
        reg: region. It can be uk, w, eu. If not specified all regions are included
        date: date from which the news needs to be retreived. It returns all the news written on and after the specified date. Format: dd/mm/yyyy

    list: 
        prints all the available agencies and their url and agency_code
    
    delete key: 
        delete story with "key" from the agency the user is logged in into 
Other Commands:
    flags: prints out mmore information about news flags
    show: prints out all the available commands


II. Name of my pythonanywhere doamin: 
https://sc21l2r.pythonanywhere.com

III. module leader's admin account:
username: ammar
password: Leeds2024!

Please, use requirements.txt to create a pip environment.

This app has been developed in python 3.10
