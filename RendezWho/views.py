from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse

def signup(request):
    return render(request,'signup.html')

def login(request):
    return render(request,'login.html')

@login_required
def logout(request):
    return render(request,'logout.html')

@login_required
def my_profile(request):
    return render(request,'myProfile.html')

@login_required
def friend_profile(request):
    return render(request,'friendProfile.html')

@login_required
def view_newsfeed(request):
    return render(request,'newsfeed.html')

@login_required
def view_connections(request):
    return render(request,'connections.html')

@login_required
def send_match_request(request):
    return render(request,'request.html')

@login_required
def search(request):
    return render(request,'search.html')

@login_required
def settings(request):
    return render(request,'settings.html')