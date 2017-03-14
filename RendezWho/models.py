from django.db import models
from django.contrib.auth.models import User

class UserApp(models.Model):
    DEFAULT_PK = 1
    requests = models.CharField(max_length=1000)
    user= models.OneToOneField(User,primary_key=True)
    connections = models.ManyToManyField('self',related_name='connection')

class Location(models.Model):
    DEFAULT_PK = 1
    coordinate = models.CharField(primary_key=True,max_length=50)
    name = models.CharField(max_length=50)

class Schedule_Entry(models.Model):
    entryID = models.BigAutoField(primary_key=True)
    activity = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=True,blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    has = models.ForeignKey(UserApp,related_name='has_entry',default=UserApp.DEFAULT_PK)
    schedule= models.ForeignKey(Location,related_name='located_at',default=Location.DEFAULT_PK)

class Meeting(models.Model):
    DEFAULT_PK = 1
    privacy = models.BooleanField()
    purpose = models.CharField(max_length=50)
    meetingID = models.BigAutoField(primary_key=True)
    time = models.TimeField(auto_now_add=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    participant = models.ManyToManyField(UserApp, related_name = 'meeting_with')
    location= models.ForeignKey(Location,related_name='located_at_also',default=Location.DEFAULT_PK)