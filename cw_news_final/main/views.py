from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import NewsStory, Author
import json
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
            # Authorization not required for Log-in but I put it to make sure nothing breaks
            if request.user.is_authenticated:
                return HttpResponse("Unauthorized: You are already logged in. Try logging put first", status=401, content_type='text/plain')
            else:
                username = request.POST.get('username')
                password = request.POST.get('password')
                if username and not username=="" and not len(username) == 0:
                    if password and not password=="" and not len(password) == 0:

                        try:
                            user = authenticate(request=request, username=username, password=password)
                        except:
                            return HttpResponse("An Error has occured while creating the user", status=500, content_type='text/plain')

                        if user is not None:
                            login(request, user)
                            if user.is_authenticated:
                                request.session.save()
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
            # Authorization not required for Log-out but I put it to make sure nothing breaks 
            if request.user.is_authenticated:
                if not request.body:
                    logout(request)
                    if not request.user.is_authenticated:
                        request.session.flush()
                        return HttpResponse("Adios. you're logged out", status=200, content_type='text/plain')
                else:
                    return HttpResponse("Bad request. the payload has to be empty", status=400, content_type='text/plain')
            else:
                return HttpResponse("You need to log in before being able to log out", status=400, content_type="text/plain")
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
                    author_instance = Author.objects.get(user=request.user)
                except Author.DoesNotExist:
                    return HttpResponse("Service Unavailable: The user you logged in with is not an author", status=503, content_type="text/plain")

                except Author.MultipleObjectsReturned:
                    return HttpResponse("Service Unavailable: there are multiple instances of the author you are logged in with. Contact the customer service", status=503, content_type="text/plain")

                
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


        #     Get Stories
        # Service Aim: to get news stories

        # Service Specifications:
        # The client sends a GET request to /api/stories with the following data in an application/x-www-formurlencoded payload with 3 items:
        # 1. Story category ("story_cat", string). For any category this should be "*".
        # 2. Story region ("story_region", string). For any region this should be "*".
        # 3. Story date ("story_date", string). For any date this should be "*".

        # When the request is received the server retrieves all stories, having the given category and region published at
        # or after the given date. If the request is processed successfully, the server responds with 200 OK and a list of
        # stories in a JSON payload (“stories”, array). For each story in the list, the following data must be provided:

        # 1. The story’s unique key (“key”, string)
        # 2. The story headline ("headline", string)
        # 3. The story category ("story_cat" , string)
        # 4. The story region ("story_region", string)
        # 5. The story author name ("author", string)
        # 6. The story date ("story_date", string)
        # 7. The story details ("story_details", string)

        # If no stories are found, the server should respond with 404 status code with text/plain payload giving more
        # information.   
    elif request.method == "GET":
        if request.content_type == 'application/x-www-form-urlencoded':
            try:
                category_raw = request.GET.get("story_cat", None)
            except:
                return HttpResponse("Missing story category. Use story_cat. If you don't want to specify it, set it to *", status=400, content_type='text/plain')
            
            try:
                region_raw = request.GET.get("story_region", None)
            except:
                return HttpResponse("Missing story region. Use story_region. If you don't want to specify it, set it to *", status=400, content_type='text/plain')
            try:
                date_raw = request.GET.get("story_date", None)
            except:
                return HttpResponse("Missing date. Use story_date. If you don't want to specify it, set it to *", status=400, content_type='text/plain')


            

            filter_category = []
            filter_region = []

            #safety check on category
            if category_raw == "*" or category_raw is None or len(category_raw) == 0 or category_raw == "":
                filter_category = ALLOWED_CATEGORIES
            else:
                for category in ALLOWED_CATEGORIES:
                    if category in category_raw:
                        filter_category.append(category)

            if len (filter_category) == 0:
                return HttpResponse("Service Unavailable: Invalid category. Available categories:\npol (Politics)\nart (Art)\ntech (Technology)\ntrivia (Trivial)", status=400, content_type='text/plain')
            
            if region_raw == "*" or region_raw is None or len(region_raw) == 0 or region_raw == "":
                filter_region = ALLOWED_REGIONS
            else:
                for region in ALLOWED_REGIONS:
                    if region in region_raw:
                        filter_region.append(region)

            if len(filter_region) == 0:
                return HttpResponse("Service Unavailable: Invalid region. valid regions are:\nuk (United Kingdom)\neu (European Union)\nw (World)", status=400, content_type='text/plain' )

            if date_raw is None or date_raw == "*" or len(date_raw) == 0 or date_raw == "":
                stories = NewsStory.objects.filter(category__in=filter_category, region__in=filter_region)
            else:
                try:
                    datetime = parse(date_raw, fuzzy=True, dayfirst=True)
                except Exception as e:
                    return HttpResponse("Date format not compatible. Use one of following:\ndd/mm/yyyy\ndd-mm-yyyy ", status=400, content_type='text/plain')


                # if only sent partial date
                if not datetime.date():
                    datetime = datetime.replace(year=now().year, month=now().month, day=now().day)
                if not datetime.time():
                    datetime = datetime.replace(hour=0, minute=0, second=0)
                
                
                    
                try:
                    stories = NewsStory.objects.filter(category__in=filter_category, region__in=filter_region, date__gte=datetime)
                except:
                    return HttpResponse("something went wrong while filtering the data. Make sure your data is formatted properly")
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
                    'story_date': story.date.strftime(f"%d-%m-%Y"),  # Format the date as string
                    'story_details': story.details
                })
            # Return the JSON response
            return JsonResponse({'stories': json_stories}, status=200)
        else:
            return HttpResponse("Bad request. the payload has to be of type application/x-www-form-urlencoded", status=400, content_type='text/plain')
    else:
        return HttpResponse("Unsupported request method. Use POST or GET method", status=503, content_type='text/plain')


@csrf_exempt
def DeleteStory(request, key):
    if request.method == "DELETE":
        if request.user.is_authenticated:
            if key is not None:
                story_keys = list(NewsStory.objects.values_list('pk', flat=True))
                if key in story_keys:
                    # if it is present, delete and print out the deleted story
                    try:
                        story_to_delete = NewsStory.objects.get(pk=key)
                    except:
                        return HttpResponse("Error while trying to get the story using the key", status=503, content_type="text/plain")

                    # Retrieve the Author instance
                    try:
                        authenticated_author = Author.objects.get(user=request.user)
                    except Author.DoesNotExist:
                        # Handle the case where there is no associated Author instance for the user
                        return HttpResponse("No author with your name found", status=503, content_type="text/plain")

                    if story_to_delete.author.authorname == authenticated_author.authorname:
                        story_to_delete.delete()
                        return HttpResponse (f"Story with id: {key} has been deleted")
                    else:
                        return HttpResponse("Denied, you are trying to delete stories written by someone else.", status=503, content_type="text/plain")
                else:
                    try:
                        pk_available = list(NewsStory.objects.values_list("pk", flat=True))
                        primary_keys_str = ", ".join(map(str, pk_available))
                        return HttpResponse (f"Service Unavailable: No story found with the key: {key}\n Available keys -> {primary_keys_str}", status=503, content_type='text/plain')


                    except:
                        return HttpResponse (f"Service Unavailable: No story found with the key: {key}", status=503, content_type='text/plain')
            else:
                return HttpResponse ("Service Unavailable: you must pass a key in the url. \n Example: .api/stories/2/\n2 is the key number", status=503, content_type='text/plain')
        else:
            return HttpResponse("Unauthorized. You need to log-in before deleting a story", status=503, content_type='text/plain')
    else:
        return HttpResponse("Unsupported request method. Use DELETE method", status=503, content_type='text/plain')
