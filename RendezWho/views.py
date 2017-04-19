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
from django.contrib import messages
import datetime
import requests

from django.db import connection, transaction

def reset(request):

     cursor = connection.cursor()

     cursor.execute("SELECT setval('CRequest_id_seq', (SELECT MAX(id) FROM CRequest)+1)")

     success = simplejson.dumps({'success':'success',})

     return HttpResponse(success, mimetype='application/json') 

def home(request):
    return render(request,'home.html')

# TO REMOVE
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
    print(request.path)
    if user:
      if user.is_active:
        login(request,user)
        return HttpResponseRedirect('/newsfeed/')
      else:
        messages.add_message(request,messages.ERROR,"We did not recognize your username or password")
        return render(request,'error.html')
    else:
      messages.add_message(request,messages.ERROR,"We did not recognize your username or password.")
      return render(request,'error.html')
  else:
    return render(request, 'login.html')

def listCalendar(request):
  user_id = request.user.social_auth.get(provider='google-oauth2')
  response = requests.get(
    'https://www.googleapis.com/calendar/v3/calendars/primary/events',
    params={'access_token':user_id.extra_data['access_token']}
  )
  list_to_give=[]
  for item in response.json()['items']:
    list_to_give.append(item['summary'])
  return render(request,'gc.html',{'items':list_to_give})

 
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
    requests=Meeting.objects.filter(requester__user=request.user).order_by('description')
    send_list=[]
    friend_r=[]
    request_list=[]
    for req in requests:
      temp = {}
      temp['id'] = req.meetingID
      temp['title']=req.description   
      temp['time']=req.start_time
      temp['date']=req.date
      temp['requestee']=req.requester.user.username
      #temp['location']=req.located_at.name
      send_list.append(temp)
    r_requests=Meeting.objects.filter(requester__user=request.user).order_by('description')
    request_list=[]
    for req in r_requests:
      temp = {}
      temp['id'] = req.meetingID
      temp['title']=req.description
      temp['time']=req.start_time
      temp['date']=req.date
      temp['requestee']=req.participants.user.username
      #temp['location']=req.located_at.name
      request_list.append(temp)
    elems = CRequest.objects.all()
    print elems
    print request.user
    friend_requests=CRequest.objects.filter(reqReceiver__username__icontains=request.user.username)
    print friend_requests
    for req in friend_requests:
      temp={}
      temp['name']=req.reqSender.username
      friend_r.append(temp)
    if request.method=="POST":
      return render(request, 'newsfeed.html',{'ownerList':send_list,'requestList':request_list,'friendList':friend_r})
    else:
      return render(request, 'newsfeed.html',{'ownerList':send_list,'requestList':request_list,'friendList':friend_r})
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
      Meeting.objects.filter(meetingID=request_id).delete()
      return HttpResponseRedirect('/newsfeed/')
    else:
      return HttpResponseRedirect('/newsfeed/')
  else:
    return render(request,'login.html')

def editRequest(request,scheduleID):
  if request.user.is_authenticated():
    if request.method=='POST':
      unformatted_date=request.POST['date']
      formatted_date = parser.parse(unformatted_date).strftime("%Y-%m-%d")
      Meeting.objects.filter(meetingID=scheduleID).update(description=request.POST['title'],start_time=request.POST['time'],date=formatted_date)
      return HttpResponseRedirect('/newsfeed/')
    else:
      objs=Meeting.objects.filter(meetingID=scheduleID)
      schedule={}
      for entry in objs:
        schedule['title']=entry.description
        schedule['id']=entry.meetingID
        schedule['time']=entry.start_time
        schedule['date']=entry.date
        schedule['person']=entry.participants.user.username
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
      time_stuff_hr = parser.parse(request.POST['time']).hour
      time_stuff_min = parser.parse(request.POST['time']).minute
      formatted_time = datetime.time(time_stuff_hr,time_stuff_min)
      time = formatted_time
      print request.POST['time'],time,time_stuff_min,time_stuff_hr
      user=User.objects.filter(username=person_uname)
      if not user:
        messages.add_message(request,messages.ERROR,"The requestee does not exist.")
        return render(request,'error.html')
      u_app=UserApp.objects.filter(user=user)
      inst=None
      for insta in u_app:
        inst=insta
        break
      entry = Meeting(description=title_of_meeting,start_time=time,date=date)
      entry.requester=UserApp(user=request.user)
      entry.participants=inst
      entry.located_at=loc
      entry.save()
      return HttpResponseRedirect('/newsfeed/')
    else:
      return render(request,'request.html')
  else:
    return render(request,'login.html')

def create_connection(request):
  if request.user.is_authenticated():
    if request.method =='POST':
      requestee = User.objects.filter(username=request.POST['connectwith'])
      if requestee==request.user:
        return HttpResponseRedirect('/newsfeed/')
      else:
        cr = CRequest (reqSender=request.user,reqReceiver=requestee[0])
        cr.save()
        print(cr,requestee[0],requestee[0].username)
        return HttpResponseRedirect('/newsfeed/')

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
          concerned_users=User.objects.filter(first_name__icontains=f_name,last_name__icontains=second_name).order_by('first_name')
        else:
          concerned_users=User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)).order_by('first_name')
      else:
        concerned_users=User.objects.filter(username__icontains=query).order_by('first_name')
      search_list=[]
      if concerned_users:
        for ser in concerned_users:
          dictionary = {}
          dictionary['first_name']=ser.first_name
          dictionary['last_name']=ser.last_name
          dictionary['email']=ser.email
          dictionary['username']=ser.username
          search_list.append(dictionary)
      else:
        search_list=[]
      return render(request, 'search.html',{'users':search_list,'flag':1})
    else:
      return render(request, 'search.html',{'users':[],'flag':0})
  else:
    return render(request,'login.html')

 
def settings(request):
  if request.user.is_authenticated():
    return render(request, 'settings.html')
  else:
    return render(request,'login.html')