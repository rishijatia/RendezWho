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
import json
import logging

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 4

def home(request):
    return render(request,'home.html')

def createUser(request):
  user_exists = UserApp.objects.filter(user=request.user)
  if len(user_exists)==0:
    uapp = UserApp(user=request.user)
    uapp.save()
  user_id = request.user.social_auth.filter(provider='google-oauth2')[0]
  ##formatted_time = datetime.datetime.now().isoformat()
  ##formatted_time=formatted_time[:formatted_time.rfind('.')]
  formatted_time = "2020-01-31T23:30:00+05:30"
  #dict2 = {'start': {'dateTime':formatted_time,'timeZone':''}}
  response = requests.get(
    'https://www.googleapis.com/calendar/v3/calendars/primary/events',
    params={'access_token':user_id.extra_data['access_token'], 'minTime': formatted_time}
  )
  u_app = UserApp.objects.filter(user=request.user)[0]
  Schedule_Entry.objects.filter(owner=u_app).delete()
  todays_date = datetime.datetime.now()
  todays_date=datetime.datetime.today().strftime('%Y-%m-%d')
  todays_date=datetime.datetime.strptime(todays_date,'%Y-%m-%d')
  todays_datetime = str(datetime.datetime.now().isoformat())
  if 'Z' or '.' in todays_datetime:
    todays_datetime=todays_datetime[:todays_datetime.rfind(':')]
  todays_datetime=datetime.datetime.strptime(todays_datetime,'%Y-%m-%dT%H:%M')
  #todays_datetime = todays_datetime[:todays_datetime.rfind('.')]
  print response.json()
  for item in response.json()['items']:
    flag=True
    if 'date' in item['end']:
      event_date = item['end']['date']
      event_date = datetime.datetime.strptime(event_date,'%Y-%m-%d')
      flag = event_date > todays_date
    else:
      event_date = item['end']['dateTime']
      event_date=event_date[0:16]
      event_date= datetime.datetime.strptime(event_date,'%Y-%m-%dT%H:%M')
      flag = event_date > todays_datetime

    if flag:
      e_activity='No Description'
      if 'summary' in item:
        e_activity = item['summary']
      else:
        if 'description' in item:
          e_activity=item['description'][:50]
      start_time=None
      end_time=None
      flag1=0
      flag2=0
      if 'dateTime' in item['start']:
        start_time=item['start']['dateTime']
        f_start_time = datetime.datetime.strptime(start_time[:len(start_time)-9],'%Y-%m-%dT%H:%M')
      else:
        flag1=1
      if 'dateTime' in item['end']:
        end_time=item['end']['dateTime']
        f_end_time=datetime.datetime.strptime(end_time[:len(end_time)-9],'%Y-%m-%dT%H:%M')
      else:
        flag2=1
      date=None
      if 'date' in item['start']:
        date = item['start']['date']
      located = 'No Location'
      if 'location' in item:
        located = item['location']
      owner = UserApp.objects.filter(user=request.user)[0]
      sche_entry=None
      if flag1==0 and flag2==0 :
        query = Schedule_Entry.objects.filter(activity=e_activity,start_time=start_time,end_time=end_time,located=located,owner=owner)
        if len(query)==0:
          sche_entry = Schedule_Entry(activity=e_activity,start_time=start_time,end_time=end_time,date=date,located=located,owner=owner)
          sche_entry.save()
      elif flag1==1 and flag2==1:
        query=Schedule_Entry.objects.filter(activity=e_activity,date=date,located=located,owner=owner)
        if len(query)==0:
          sche_entry = Schedule_Entry(activity=e_activity,date=date,located=located,owner=owner)
          sche_entry.save()
      elif flag1==1:
        query=Schedule_Entry.objects.filter(activity=e_activity,end_time=end_time,located=located,owner=owner)
        if len(query)==0:
          sche_entry = Schedule_Entry(activity=e_activity,end_time=end_time,date=date,located=located,owner=owner)
          sche_entry.save()
      else:
        query=Schedule_Entry.objects.filter(activity=e_activity,start_time=start_time,located=located,owner=owner)
        if len(query)==0:
          sche_entry = Schedule_Entry(activity=e_activity,start_time=start_time,date=date,located=located,owner=owner)
          sche_entry.save()
      
  
  return HttpResponseRedirect('/newsfeed/')


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
  if request.user.is_authenticated():
    return HttpResponseRedirect('/newsfeed/')
  else:
    if request.method =='POST':
      user_name = request.POST['username']
      pass_word = request.POST['password']
      user = authenticate(username=user_name,password=pass_word)
      #print(request.path)
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
  usr = request.user
  u_app = UserApp.objects.filter(user=usr)[0]
  entries = Schedule_Entry.objects.all()
  list_to_give=[]
  for item in entries:
    val = str(item.activity) + ' ' + str(item.start_time) + ' ' + str(item.end_time)
    list_to_give.append(val)
  print list_to_give
  return render(request,'gc.html',{'items':list_to_give})

 
def Logout(request):
  if request.user.is_authenticated():
    logout(request)
    request.session.flush()
    return HttpResponseRedirect('/login/')
  else:
    return render(request,'login.html')

 
def my_profile(request):
  if request.user.is_authenticated():
    connections_list=[]
    for obj in UserApp.objects.filter(user=request.user):
      for unames in obj.connections.all():
        connections_list.append(unames.user.username)
    meeting_list=[]
    for meeting in Meeting.objects.filter(Q(requester__user=request.user) | Q(participants__user=request.user)):
      temp={}
      temp['description']=meeting.description
      temp['requester']=meeting.requester.user.username
      temp['participant']=meeting.participants.all()[0].user.username
      if request.user.username==temp['requester']:
        temp['name']=temp['participant']
      else:
        temp['name']=temp['requester']
      temp['location']=meeting.is_at
      temp['date']=meeting.date
      temp['start_time']=meeting.start_time
      temp['end_time']=meeting.end_time
      meeting_list.append(temp)
    print (connections_list,meeting_list)
    return render(request, 'myProfile.html',{'connections':connections_list,'meetings':meeting_list})
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
      if req.approved==True:
        pass
      else:
        temp['id'] = req.meetingID
        temp['title']=req.description   
        temp['time']=req.start_time
        temp['date']=req.date
        temp['requestee']=req.participants.all()[0].user.username
        send_list.append(temp)
    request_list=[]
    for meeting in Meeting.objects.all():
      if any(request.user==usr.user for usr in meeting.participants.all()):
        temp = {}
        if meeting.approved ==True:
          pass
        else:
          temp['id'] = meeting.meetingID
          temp['title']=meeting.description
          temp['time']=meeting.start_time
          temp['date']=meeting.date
          temp['requestee']=meeting.requester.user.username
          request_list.append(temp)
    elems = CRequest.objects.all()
    friend_requests=CRequest.objects.filter(reqReceiver__username__icontains=request.user.username)
    for req in friend_requests:
      temp={}
      temp['name']=req.reqSender.username
      friend_r.append(temp)
    connections_list = []
    cnns = []

    top_twenty_newsfeed = []
    advanced_query = Meeting.objects.filter(Q(approved=True) & (Q(requester__in=([UserApp.objects.filter(user_id=val)[0] for val in UserApp.objects.filter(user=request.user)[0].connections.all().values_list('user',flat=True)])) 
    | Q(participants__in=([UserApp.objects.filter(user_id=val)[0] for val in UserApp.objects.filter(user=request.user)[0].connections.all().values_list('user',flat=True)])))).order_by('-start_time')[:20]
    for entry in advanced_query:
      temp = {}
      temp['name1'] = entry.participants.all()[0].user.username
      requester = entry.requester
      temp['name2'] = entry.requester.user.username
      temp['location']=entry.is_at
      temp['start_time']=entry.start_time
      temp['end_time']=entry.end_time
      temp['date']=entry.date
      top_twenty_newsfeed.append(temp)
    for obj in UserApp.objects.filter(user=request.user):
      for unames in obj.connections.all():
        connections_list.append(unames.user.username)
    if request.method=="POST":
      return render(request, 'newsfeed.html',{'ownerList':send_list,'requestList':request_list,'friendList':friend_r,'connections':connections_list,'newsfeed':top_twenty_newsfeed})
    else:
      return render(request, 'newsfeed.html',{'ownerList':send_list,'requestList':request_list,'friendList':friend_r,'connections':connections_list,'newsfeed':top_twenty_newsfeed})
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
      Meeting.objects.filter(meetingID=scheduleID).update(description=request.POST['title'],is_at=request.POST['location'])
      return HttpResponseRedirect('/newsfeed/')
    else:
      objs=Meeting.objects.filter(meetingID=scheduleID)
      schedule={}
      for entry in objs:
        schedule['title']=entry.description
        schedule['id']=entry.meetingID
        schedule['time']=entry.start_time
        schedule['date']=entry.date
        schedule['person']=entry.participants.all()[0].user.username
        schedule['location']=entry.is_at
      return render(request,'edit_page.html',{"schedule":schedule})
  else:
    return render(request,'login.html')

def suggestions_algorithm(request):
  if request.user.is_authenticated():
    if request.method == 'POST':
      title_of_meeting = request.POST['title']
      radio = request.POST['type']
      person_uname = request.POST['person']
      p_user = User.objects.filter(username=person_uname)[0]
      location_m = request.POST['location']
      d1=request.POST['date1']
      d2=request.POST['date2']
      d3=request.POST['date3']
      dates_arr = [d1,d2,d3]
      time_list=[]
      time_list_morning = ['T06:00','T06:30','T07:00','T07:30','T08:00','T08:30','T09:00','T09:30','T10:00',
        'T10:30','T11:00','T11:30']
      time_list_afternoon = ['T12:00','T12:30','T13:00','T13:30','T14:00','T14:30','T15:00','T15:30','T16:00','T16:30']
      time_list_evening = ['T17:00','T17:30','T18:00','T18:30','T19:00','T19:30','T20:00','T20:30','T21:00','T21:30','T22:00']
      time_list_all = time_list_morning+time_list_afternoon+time_list_evening
      available_times={}
      flag=1
      for date in dates_arr:
        if len(date)<5:
          available_times[date]=''
          flag+=1
          continue
        var = 'time' + str(flag)
        t_d=request.POST[var]
        if t_d == 'morning':
          time_list=time_list_morning
        elif t_d == 'afternoon':
          time_list=time_list_afternoon
        elif t_d == 'evening':
          time_list=time_list_evening
        else:
          time_list=time_list_all
        flag+=1
        temp_arr=[]
        formatted_date = date.split('/')
        formatted_date=formatted_date[2]+'-'+formatted_date[0]+'-'+formatted_date[1]
        spl=formatted_date.split('-')
        date_in_date=datetime.date(int(spl[0]),int(spl[1]),int(spl[2]))  
        whole_day_gone=Schedule_Entry.objects.filter(owner__user=request.user,start_time__isnull=True,end_time__isnull=True,date=date_in_date)
        whole_day_gone2=Schedule_Entry.objects.filter(owner__user=p_user,start_time__isnull=True,end_time__isnull=True,date=date_in_date)
        if len(whole_day_gone)==0 and len(whole_day_gone2)==0:
          for times in time_list:
            date_time=formatted_date+times
            date_time=datetime.datetime.strptime(date_time,'%Y-%m-%dT%H:%M')
            date_time=date_time+datetime.timedelta(hours=5)
            print("DT",date_time)
            query = Schedule_Entry.objects.filter((Q(owner__user=request.user) | Q(owner__user=p_user)) & 
              (Q(start_time__lte=date_time) & Q(end_time__gte=date_time)))
            if len(query)==0:
              temp_arr.append(str(times)[1:])
        available_times[date]=temp_arr
      #print "Available at: " , available_times
      return render(request,'suggestions.html',{'requesting_user':person_uname,'date1':d1,'times1':available_times[d1],'date2':d2,'times2':available_times[d2],'date3':d3,'times3':available_times[d3],'location':location_m,'title':title_of_meeting})

def rejectRequest(request):
  if request.user.is_authenticated():
    if request.method=='POST':
      mid = request.POST['other_name']
      Meeting.objects.filter(meetingID=mid).delete()
      return HttpResponseRedirect('/newsfeed/')
  else:
    return HttpResponseRedirect('/login/')
def acceptRequest(request):
  if request.user.is_authenticated():
    if request.method=='POST':
      mid = request.POST['other_name']
      meeting = Meeting.objects.filter(meetingID=mid)[0]
      user2 = meeting.requester.user
      url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
      user_id = request.user.social_auth.filter(provider='google-oauth2')[0]
      user_id2 = user2.social_auth.filter(provider='google-oauth2')[0]
      s_time = meeting.start_time
      e_time = meeting.end_time
      date = meeting.date
      str_start_time = str(date)+"T"+str(s_time)
      str_end_time = str(date)+"T"+str(e_time)
      start_time=str_start_time
      end_time=str_end_time
      start = {
      'dateTime':str_start_time,
      'timeZone':'America/Chicago'
      }
      end = {
      'dateTime':str_end_time,
      'timeZone':'America/Chicago'
      }
      headers={'Content-Type':'application/json; charset=UTF-8'}
      d={'end':end,'start':start,'summary':meeting.description,'description':meeting.description,'location' : meeting.is_at}
      logging.basicConfig()
      logging.getLogger().setLevel(logging.DEBUG)
      requests_log = logging.getLogger("requests.packages.urllib3")
      requests_log.setLevel(logging.DEBUG)
      requests_log.propagate = True
      response = requests.post(url,data=json.dumps(d),params={'access_token':user_id.extra_data['access_token']},headers=headers)
      response2 = requests.post(url,data=json.dumps(d),params={'access_token':user_id2.extra_data['access_token']},headers=headers)
      Meeting.objects.filter(meetingID=mid).update(approved=True)
      return HttpResponseRedirect('/newsfeed/')

def send_match_request(request):
  if request.user.is_authenticated():
    if request.method=='POST':
      title_of_meeting = request.POST['title']
      person_uname = request.POST['requesting_user']
      location_m = request.POST['location']
      dateTime= request.POST['dateTime']
      date = dateTime.split('T')[0]
      formatted_date = date.split('/')
      date_in_date=datetime.date(int(formatted_date[2]),int(formatted_date[0]),int(formatted_date[1])) 
      startTime= datetime.datetime.strptime(dateTime,'%m/%d/%YT%H:%M')
      endTime= startTime + datetime.timedelta(hours=1)
      user=User.objects.filter(username=person_uname)
      if not user:
        messages.add_message(request,messages.ERROR,"The requestee does not exist.")
        return render(request,'error.html')
      entry = Meeting(description=title_of_meeting,start_time=startTime,end_time=endTime,date=date_in_date,approved=0,requester=UserApp.objects.filter(user=request.user)[0],is_at=location_m,privacy=False)
      entry.save()
      value=UserApp.objects.filter(user__username=person_uname)[0]
      print(value,person_uname,"SDASD")
      entry.participants.add(value)
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
        return HttpResponseRedirect('/newsfeed/')

def accept(request):
  if request.user.is_authenticated():
    if request.method=='POST':
      username1=request.POST['other_name']
      curr_user=request.user.username
      userapp1 = UserApp.objects.filter(user__username=curr_user)[0]
      userapp2=UserApp.objects.filter(user__username=username1)[0]
      userapp1.connections.add(userapp2)
      userapp2.connections.add(userapp1)
      userapp1.save()
      userapp2.save()
      CRequest.objects.filter(reqSender=User.objects.filter(username=username1)[0],reqReceiver=request.user).delete()
      return HttpResponseRedirect('/newsfeed/')

def reject(request):
  if request.user.is_authenticated():
    if request.method=='POST':
      username1=request.POST['other_name']
      CRequest.objects.filter(reqSender=User.objects.filter(username=username1)[0],reqReceiver=request.user).delete()
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