from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import NewsStory, Author
import json
from django.core import serializers
from django.http import JsonResponse
from dateutil.parser import parse
from django.utils.timezone import now

ALLOWED_CATEGORIES = ['pol', 'art', 'tech', 'trivia']
ALLOWED_REGIONS = ['uk', 'eu', 'w']




#============================================================
#LOG-IN
@csrf_exempt
def LogIn(request):
    """
    API endpoint to log in to an author's account 
    in order to be able to post or delete news stories.

    Parameters:
    - client sends a POST request to /api/login with the following
    data in an application/x-www-formurlencoded payload with two items:
        - Username ("username", string)
        - Password ("password", string)

    Returns:
        - if successful it returns 200 and a text/plain payload
        - if fails, it returns error code and text/plain with more details
    
    """
    if request.method == "POST":
        if request.content_type == 'application/x-www-form-urlencoded':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username)
            print(password)

            if username:
                if password:
                    user = authenticate(request=request, username=username, password=password)
                    print(user)

                    if user is not None:
                        login(request, user)
                        print(user.is_authenticated)
                        print(user.is_active)
                        if user.is_authenticated:
                            request.session.save()
                            print(request.session)
                            return HttpResponse(f"Login successful, welcome {user}", status=200, content_type='text/plain')
                    else:
                        return HttpResponse("Unauthorized", status=401, content_type='text/plain')
                else:
                    return HttpResponse("password missing or bad request", status=400, content_type='text/plain')
            else:
                return HttpResponse("username missing or bad request", status=400, content_type='text/plain')
        else:
            return HttpResponse("Bad request. the payload has to be of type application/x-www-form-urlencoded", status=400, content_type='text/plain')
    else:
        return HttpResponse("Unsupported request method. Use POST method", status=405, content_type='text/plain')

#============================================================
#LOG-OUT
@csrf_exempt
def LogOut(request):
    """
    API endpoint to log out from an author's account.
    
    Parameters:
    - client sends a POST request to /api/logout with an empty payload

    Returns:
        - if successful it returns 200 and a text/plain payload
        - if fails, it returns error code and text/plain with more details
    
    """
    if request.method == "POST":
        if request.content_type == 'text/plain':
            if not request.body:
                logout(request)
                request.session.flush()
                return HttpResponse("Adios", status=200, content_type='text/plain')
            else:
                return HttpResponse("Bad request. the payload has to be an empty text/plain", status=400, content_type='text/plain')
        else:
            return HttpResponse("Bad request. the payload has to be an empty text/plain", status=400, content_type='text/plain')

    else:
        return HttpResponse("Unsupported request method. Use POST method", status=405, content_type='text/plain')
     

#============================================================
#POST A STORY
@csrf_exempt
def Story(request):
    if request.method == "POST":
        #         """
        # API endpoint to post a story.

        # Precondition:
        #     - the user must be logged in before posting stories.

        # Parameters:
        # - client sends a POST request to /api/stories with the following
        # data in an JSON payload with these items:
        #     - Story headline ("headline", string)
        #     - Story category ("category", string)
        #     - Story region ("region", string)
        #     - Story details ("details", string)
        
        # Upon receipt of this request the server checks that the user is logged in, and if they are the story is added to the
        # stories table (with the name of the logged in user) and a time stamp.



        # Returns:
        #     - if successful it returns 201 and a payload "CREATED"
        #     - If the story cannot be added for any reason (e.g. unauthenticated author), the server should respond with 503
        #     Service Unavailable with text/plain payload giving reason.    
        # """
        if request.user.is_authenticated:
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    return HttpResponse("Service Unavailable: invalid JSON payload", status=503, content_type='text/plain')#
                
                # check if user is author
                try:
                    # TODO:use get and handle the errors of no data or too much data 
                    author_instance = Author.objects.filter(user=request.user).first()
                except Author.DoesNotExist:
                    return HttpResponse("Service Unavailable: The user you logged in with is not an author", status=503, content_type="text/plain")
                
                # check if all the details exist. 
                if "headline" not in data or \
                    "category" not in data or \
                    "region" not in data or \
                    "details" not in data:
                    return HttpResponse("Service Unavailable: the payload has one or more missing field", status=503, content_type='text/plain')
                else:
                    # Check data types and handle errors separately
                    headline = data.get("headline")
                    category = data.get("category")
                    region = data.get("region")
                    details = data.get("details")

                    # Validate headline
                    if not isinstance(headline, str):
                        return HttpResponse("Service Unavailable: headline must be a string", status=503, content_type='text/plain')
                    
                    if len (headline) > 64:
                        return HttpResponse ("Service Unavailable: headline can be maximun 64 characters", status=503, content_type='text/plain')

                    
                    # Validate category
                    if category not in ALLOWED_CATEGORIES:
                        return HttpResponse("Service Unavailable: Invalid category. Available categories:\npol (Politics)\nart (Art)\ntech (Technology)\ntrivia (Trivial)", status=503, content_type='text/plain')

                    # Validate region
                    if region not in ALLOWED_REGIONS:
                        return HttpResponse("Service Unavailable: Invalid region. valid regions are:\nuk (United Kingdom)\neu (European Union)\nw (World)", status=503, content_type='text/plain' )

                    if len (category) > 30:
                        return HttpResponse ("Service Unavailable: category can be maximun 30 characters", status=503, content_type='text/plain')
                    
                    if len (region) > 30:
                        return HttpResponse ("Service Unavailable: region can be maximun 30 characters", status=503, content_type='text/plain')
                    

                    if not isinstance(details, str):
                        return HttpResponse("Service Unavailable: details must be a string", status=503, content_type='text/plain')
                    
                    if len (details) > 128:
                        return HttpResponse ("Service Unavailable: details can be maximun 128 characters", status=503, content_type='text/plain')

                    story = NewsStory(headline=headline, 
                                      category=category, 
                                      region=region, 
                                      details=details, 
                                      author=author_instance)
                    story.save()
                    if story.pk is not None: #primary key
                        return HttpResponse("CREATED", status=201)
                    else:
                        return HttpResponse("Service Unavailable: story could not be added to database. Make sure the data is of the right format", status=503, content_type='text/plain')

            else:
                return HttpResponse("Bad request. The payload needs to be application/json", status=503, content_type='text/plain')

        else:
            return HttpResponse("Unauthorized. You need to log-in before posting a story", status=503, content_type='text/plain')
        
    elif request.method == "GET":
        if request.content_type == 'application/x-www-form-urlencoded':
            try:
                category_raw = request.GET.get("story_cat")
                region_raw = request.GET.get("story_region")
                date_raw = request.GET.get("story_date")
            except:
                category_raw = None
                region_raw = None
                date_raw = None

            filter_category = []
            filter_region = []

            #safety check on category
            # TODO: ask teacher if we need to give error if not all the variables are given in client
            # TODO: ask teacher if can use dateutil
            if category_raw == "*" or category_raw is None:
                filter_category = ALLOWED_CATEGORIES
            else:
                for category in ALLOWED_CATEGORIES:
                    if category in category_raw:
                        filter_category.append(category)

            if len (filter_category) == 0:
                return HttpResponse("Service Unavailable: Invalid category. Available categories:\npol (Politics)\nart (Art)\ntech (Technology)\ntrivia (Trivial)", status=400, content_type='text/plain')
            
            if region_raw == "*" or region_raw is None:
                filter_region = ALLOWED_REGIONS
            else:
                for region in ALLOWED_REGIONS:
                    if region in region_raw:
                        filter_region.append(region)

            if len(filter_region) == 0:
                return HttpResponse("Service Unavailable: Invalid region. valid regions are:\nuk (United Kingdom)\neu (European Union)\nw (World)", status=400, content_type='text/plain' )

            if date_raw is None or date_raw == "*":
                stories = NewsStory.objects.filter(category__in=filter_category, region__in=filter_region)
            else:
                try:
                    datetime = parse(date_raw, fuzzy=True)
                except Exception as e:
                    return HttpResponse("Date format not compatible. Use either:\nYYYY-MM-DD hh:mm:ss\nhh:mm:ss\nYYYY-MM-DD", status=400, content_type='text/plain')


                if not datetime.date():
                    datetime = datetime.replace(year=now().year, month=now().month, day=now().day)
                if not datetime.time():
                    datetime = datetime.replace(hour=0, minute=0, second=0)
                    
                stories = NewsStory.objects.filter(category__in=filter_category, region__in=filter_region, date__gte=datetime)
            
            if stories is None:
                return HttpResponse("No stories with these variables", status=404, content_type='text/plain')
            
            # Convert the list of dictionaries into JSON format
            json_stories = []
            for story in stories:
                json_stories.append({
                    'key': str(story.id),  # Assuming the story's unique key is its ID
                    'headline': story.headline,
                    'story_cat': story.category,
                    'story_region': story.region,
                    'author': story.author.authorname,
                    'story_date': story.date.strftime("%Y-%m-%d %H:%M:%S"),  # Format the date as string
                    'story_details': story.details
                })
            # Return the JSON response
            return JsonResponse({'stories': json_stories}, status=200)
        else:
            return HttpResponse("Bad request. the payload has to be of type application/x-www-form-urlencoded", status=400, content_type='text/plain')
    else:
        return HttpResponse("Unsupported request method. Use POST or GET method", status=503, content_type='text/plain')

def DeleteStory(request, key):
    # TODO: can an author delete a story from another author?
    if request.method == "DELETE":
        if request.user.is_authenticated:
            if key is not None:
                story_keys = list(NewsStory.objects.values_list('pk', flat=True))
                if key in story_keys:
                    pass
                    # if it is present, delete and print out the deleted story
                else:
                    return HttpResponse (f"Service Unavailable: No story found with the key: {key}", status=503, content_type='text/plain')
            else:
                return HttpResponse ("Service Unavailable: you must pass a key in the url. \n Example: .api/stories/2/\n2 is the key number", status=503, content_type='text/plain')
        else:
            return HttpResponse("Unauthorized. You need to log-in before deleting a story", status=503, content_type='text/plain')
    else:
        return HttpResponse("Unsupported request method. Use DELETE method", status=503, content_type='text/plain')
