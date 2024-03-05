from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse


@csrf_exempt
def LogIn(request):
    if request.method == "POST":
        if request.content_type == 'application/x-www-form-urlencoded':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if username:
                if password:
                    user = authenticate(username, password)

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

@csrf_exempt
def LogOut(request):
    return HttpResponse("log-out not yet implemented", status=501 )

@csrf_exempt
def PostAStory(request):
    return HttpResponse("post a story not yet implemented", status=501)

def GetStories(request):
    return HttpResponse("Get Stories not yet implemented", status=501)

def DeleteStory(request):
    return HttpResponse("Delete story not yet implemented", status=501)