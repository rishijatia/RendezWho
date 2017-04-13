from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserApp(models.Model):
    DEFAULT_PK=1
    user = models.OneToOneField(User,primary_key=True)
    connections = models.ManyToManyField('self',related_name='friends')

class Location(models.Model):
    DEFAULT_PK=1
    name = models.CharField(primary_key=True,max_length=50)

class Schedule_Entry(models.Model):
    entryID = models.BigAutoField(primary_key=True)
    activity = models.CharField(max_length=50)
    start_time = models.TimeField(auto_now_add=True,blank=True)
    end_time = models.TimeField(auto_now_add=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    located = models.ForeignKey(Location,related_name='loc')
    owner = models.ForeignKey(UserApp,related_name="owns")

class Meeting(models.Model):
    privacy = models.BooleanField()
    approved = models.BooleanField(default=False)
    requester = models.ForeignKey(UserApp, related_name="rqsts")
    meetingID = models.BigAutoField(primary_key=True)
    start_time = models.TimeField(auto_now_add=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    participants = models.ManyToManyField(UserApp,related_name="participants")
    is_at = models.ForeignKey(Location,related_name='at',default=Location.DEFAULT_PK)
    end_time = models.TimeField(auto_now_add=True, blank=True)