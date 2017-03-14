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
    user_name = request.POST['username']
    pass_word = request.POST['password']
    user = authenticate(username=user_name,password=pass_word)
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
def Logout(request):
  if request.user.is_authenticated():
    logout(request)
    return HttpResponseRedirect('/login/')
  else:
    return render(request,'login.html')

@login_required
def my_profile(request):
  if request.user.is_authenticated():
    return render(request, 'myProfile.html')
  else:
    return render(request,'login.html')

@login_required
def friend_profile(request):
  if request.user.is_authenticated():
    return render(request, 'friendProfile.html')
  else:
    return render(request,'login.html')

@login_required
def view_newsfeed(request):
  if request.user.is_authenticated():
    return render(request, 'newsfeed.html')
  else:
    return render(request,'login.html')

@login_required
def view_connections(request):
  if request.user.is_authenticated():
    return render(request, 'connections.html')
  else:
    return render(request,'login.html')

@login_required
def send_match_request(request):
  if request.user.is_authenticated():
    return render(request, 'request.html')
  else:
    return render(request,'login.html')

def search(request):
  if request.user.is_authenticated():
    if request.method=='POST':
      query = request.POST['searchquery']
      isName = request.POST.get('name_type')
      isEmail = request.POST.get('email_type')
      isUsername = request.POST.get('username_type')
      concerned_users=None
      if isName:
        f_name=query.split(' ')[0]
        second_name=query.split(' ')[1]
        concerned_users=User.objects.get(first_name=f_name,last_name=second_name)
      elif isEmail:
        concerned_user=User.objects.get(email=query)
      else:
        concerned_users=User(username=query)
      print concerned_users
      search_list=[]
      for ser in concerned_users:
        dictionary = {}
        dictionary['first_name']=ser.first_name
        dictionary['last_name']=ser.last_name
        search_list.append(dictionary)
      print search_list
      return render(request, 'search.html',{'users':search_list})
    else:
      return render(request, 'search.html',{'users':[]})
  else:
    return render(request,'login.html')

@login_required
def settings(request):
  if request.user.is_authenticated():
    return render(request, 'settings.html')
  else:
    return render(request,'login.html')