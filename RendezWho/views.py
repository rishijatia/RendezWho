from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from forms import Signup
from models import *
from dateutil import parser
from django.db.models import Q

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
        return HttpResponseRedirect('/newsfeed/')
      else:
        return HttpResponse("Sorry something went wrong")
    else:
      return HttpResponse("Sorry something went wrong 2")
  else:
    return render(request, 'login.html')


  

 
def Logout(request):
  if request.user.is_authenticated():
    logout(request)
    return HttpResponseRedirect('/login/')
  else:
    return render(request,'login.html')

 
def my_profile(request):
  if request.user.is_authenticated():
    return render(request, 'myProfile.html')
  else:
    return render(request,'login.html')

 
def friend_profile(request):
  if request.user.is_authenticated():
    return render(request, 'friendProfile.html')
  else:
    return render(request,'login.html')

 
def view_newsfeed(request):
  if request.user.is_authenticated():
    requests=Schedule_Entry.objects.filter(owner__user=request.user)
    send_list=[]
    for req in requests:
      temp = {}
      temp['id'] = req.entryID
      temp['title']=req.activity
      temp['time']=req.time
      temp['date']=req.date
      temp['requestee']=req.has.user.username
      #temp['location']=req.located_at.name
      send_list.append(temp)
    if request.method=="POST":
      return render(request, 'newsfeed.html',{'requestList':send_list})
    else:
      return render(request, 'newsfeed.html',{'requestList':send_list})
  else:
    return render(request,'login.html')

def view_connections(request):
  if request.user.is_authenticated():
    return render(request, 'connections.html')
  else:
    return render(request,'login.html')

def deleteRequest(request):
  if request.user.is_authenticated():
    if request.method=='POST':
      request_id=request.POST['requestID']
      Schedule_Entry.objects.filter(entryID=request_id).delete()
      return HttpResponseRedirect('/newsfeed/')
    else:
      return HttpResponseRedirect('/newsfeed/')
  else:
    return render(request,'login.html')

def editRequest(request,scheduleID):
  if request.user.is_authenticated():
    if request.method=='POST':
      unformatted_date=request.POST['date']
      formatted_date= parser.parse(unformatted_date).strftime('%Y-%m-%d')
      print formatted_date
      Schedule_Entry.objects.filter(entryID=scheduleID).update(activity=request.POST['title'],time=request.POST['time'],date=formatted_date)
      return HttpResponseRedirect('/newsfeed/')
    else:
      objs=Schedule_Entry.objects.filter(entryID=scheduleID)
      schedule={}
      for entry in objs:
        schedule['title']=entry.activity
        schedule['id']=entry.entryID
        schedule['time']=entry.time
        schedule['date']=entry.date
        schedule['person']=entry.has.user.username
        schedule['location']="UIUC"
      print schedule
      return render(request,'edit_page.html',{"schedule":schedule})
  else:
    return render(request,'login.html')

def send_match_request(request):
  if request.user.is_authenticated():
    if request.method=='POST':
      title_of_meeting = request.POST['title']
      radio = request.POST['type']
      person_uname = request.POST['person']
      location_m = request.POST['location']
      date= request.POST['date']
      time = request.POST['time']
      user=User.objects.filter(username=person_uname)
      if not user:
        return HttpResponse("User does not exist.")
      u_app=UserApp.objects.filter(user=user)
      inst=None
      for insta in u_app:
        inst=insta
        break
      loc = Location(coordinate=location_m,name=location_m)
      loc.save()
      entry = Schedule_Entry(activity=title_of_meeting,time=time,date=date)
      entry.owner=UserApp(user=request.user)
      entry.has=inst
      entry.located_at=loc
      entry.save()
      return HttpResponseRedirect('/newsfeed/')
    else:
      return render(request,'request.html')
  else:
    return render(request,'login.html')

def search(request):
  if request.user.is_authenticated():
    if request.method=='POST':
      query = request.POST['searchquery']
      radio = request.POST['type']
      concerned_users=None
      if radio=='name_type':
        if ' ' in query:
          f_name=query.split(' ')[0]
          second_name=query.split(' ')[1]
          concerned_users=User.objects.filter(first_name__icontains=f_name,last_name__icontains=second_name)
        else:
          concerned_users=User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
      else:
        concerned_users=User.objects.filter(username__icontains=query)
      search_list=[]
      if concerned_users:
        for ser in concerned_users:
          dictionary = {}
          dictionary['first_name']=ser.first_name
          dictionary['last_name']=ser.last_name
          search_list.append(dictionary)
      else:
        search_list=[{'first_name':'No User','last_name':'Found'}]
      return render(request, 'search.html',{'users':search_list})
    else:
      return render(request, 'search.html',{'users':[]})
  else:
    return render(request,'login.html')

 
def settings(request):
  if request.user.is_authenticated():
    return render(request, 'settings.html')
  else:
    return render(request,'login.html')