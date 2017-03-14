from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from forms import Signup
from models import *
def home(request):
    return render(request,'home.html')

def signup(request):
  if request.method == 'POST':
    """
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
    print new_user.first_name,new_user.password
    """
    signup_form = Signup(data=request.POST)
    user = signup_form.save()
    user.set_password(user.password)
    user.save()
    user_app = UserApp()
    user_app.user=user
    user_app.requests=[]
    user_app.save()
    return HttpResponseRedirect("/login/")
  else:
    signup_form = Signup()
    return render(request, "signup.html", {'form': signup_form})
          
def Login(request):
  if request.method =='POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    if user:
      if user.is_active:
        login(request,user)
        return render(request,'newsfeed.html')
      else:
        return HttpResponse("Sorry something went wrong")
    else:
      return HttpResponse("Sorry something went wrong 2")
  else:
    return render(request, 'login.html')


  

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

def search(request):
  if request.user.is_authenticated():
    return render(request, 'search.html')
  else:
    return render(request,'login.html')

@login_required
def settings(request):
    return render(request, 'settings.html')