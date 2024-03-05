from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from news_agency.models import NewsStory




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

            if username:
                if password:
                    user = authenticate(username=username, password=password)

                    if user is not None:
                        login(request, user)
                        return HttpResponse("Login successful, welcome", status=200, content_type='text/plain')
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
                LogOut(request=request)
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
@login_required # TODO: implement this log in and delete the inner one and teste it.
def PostAStory(request):
    """
    API endpoint to post a story.

    Precondition:
        - the user must be logged in before posting stories.

    Parameters:
    - client sends a POST request to /api/stories with the following
    data in an JSON payload with these items:
        - Story headline ("headline", string)
        - Story category ("category", string)
        - Story region ("region", string)
        - Story details ("details", string)
    
    Upon receipt of this request the server checks that the user is logged in, and if they are the story is added to the
    stories table (with the name of the logged in user) and a time stamp.



    Returns:
        - if successful it returns 201 and a payload "CREATED"
        - If the story cannot be added for any reason (e.g. unauthenticated author), the server should respond with 503
        Service Unavailable with text/plain payload giving reason.    
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    return HttpResponse("Service Unavailable: invalid JSON payload", status=503, content_type='text/plain')
                
                if "headline" not in data or \
                    "category" not in data or \
                    "region" not in data or \
                    "details" not in data:
                    return HttpResponse("Service Unavailable: the payload has one or more missing field", status=503, content_type='text/plain')
                else:
                    story = NewsStory(headline=data["headline"], 
                                      category=data["category"], 
                                      region=data["region"], 
                                      details=data["details"], 
                                      author=request.user)
                    story.save()
                    if story.pk is not None: #primary key
                        return HttpResponse("CREATED", status=201)
                    else:
                        return HttpResponse("Service Unavailable: story could not be added to database. Make sure the data is of the right format", status=503, content_type='text/plain')

            else:
                return HttpResponse("Bad request. The payload needs to be application/json", status=503, content_type='text/plain')

        else:
            return HttpResponse("Unsupported request method. Use POST method", status=503, content_type='text/plain')
    else:
        return HttpResponse("Unauthorized. You need to log-in before posting a story", status=503, content_type='text/plain')

def GetStories(request):
    return HttpResponse("Get Stories not yet implemented", status=501)

def DeleteStory(request):
    return HttpResponse("Delete story not yet implemented", status=501)