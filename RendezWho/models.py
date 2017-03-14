from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserApp(models.Model):
    DEFAULT_PK=1
    user = models.OneToOneField(User,primary_key=True)
    connections = models.ManyToManyField('self',related_name='friends')

class Location(models.Model):
    DEFAULT_PK=1
    coordinate = models.CharField(primary_key=True,max_length=50)
    name = models.CharField(max_length=50)

class Schedule_Entry(models.Model):
    entryID = models.BigAutoField(primary_key=True)
    activity = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=True,blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    located = models.ForeignKey(Location,related_name='loc')
    approved = models.BooleanField(default=False)
    owner = models.ForeignKey(UserApp,related_name="owns")
    has = models.ForeignKey(UserApp,related_name="rqsts")

class Meeting(models.Model):
    privacy = models.BooleanField()
    meetingID = models.BigAutoField(primary_key=True)
    time = models.TimeField(auto_now_add=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    participants = models.ManyToManyField(UserApp,related_name="participants")
    is_at = models.ForeignKey(Location,related_name='at',default=Location.DEFAULT_PK)