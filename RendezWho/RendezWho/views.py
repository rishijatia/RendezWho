from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from .models import *

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        new_user = User.objects.create_user(username,email,password)
        new_user.is_active = True
        new_user.first_name=first_name
        new_user.last_name=last_name
        new_user.save()
        user_app = UserApp()
        user_app.user=new_user
        user_app.requests=[]
        return HttpResponseRedirect("/login/")
        
def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return render(request,'newsfeed.html')
            else:
                return render(request,'signup.html')
        else:
            return  render(request,'signup.html')


@login_required
def logout(request):
    return render(request, 'logout.html')

@login_required
def my_profile(request):
    return render(request, 'myProfile.html')

@login_required
def friend_profile(request):
    return render(request, 'friendProfile.html')

@login_required
def view_newsfeed(request):
    return render(request, 'newsfeed.html')

@login_required
def view_connections(request):
    return render(request, 'connections.html')

@login_required
def send_match_request(request):
    return render(request, 'request.html')

@login_required
def search(request):
    return render(request, 'search.html')

@login_required
def settings(request):
    return render(request, 'settings.html')