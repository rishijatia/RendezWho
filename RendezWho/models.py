from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserApp(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    connections = models.ManyToManyField('self',related_name='friends')

class CRequest(models.Model):
    reqID = models.BigAutoField(primary_key=True)
    reqSender = models.ForeignKey(User,related_name="sender")
    reqReceiver = models.ForeignKey(User,related_name="receiver")
    class Meta:
        unique_together = ['reqSender','reqReceiver']

class Schedule_Entry(models.Model):
    entryID = models.BigAutoField(primary_key=True)
    activity = models.CharField(max_length=50)
    start_time = models.TimeField(auto_now_add=True,blank=True)
    end_time = models.TimeField(auto_now_add=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    located = models.CharField(max_length=50)
    owner = models.ForeignKey(UserApp,related_name="owns")

class Meeting(models.Model):
    meetingID = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=50,blank=True)
    privacy = models.BooleanField()
    approved = models.BooleanField(default=False)
    requester = models.ForeignKey(UserApp, related_name="rqsts")
    start_time = models.TimeField(auto_now_add=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    participants = models.ManyToManyField(UserApp,related_name="participants")
    is_at = models.CharField(max_length=50)
    end_time = models.TimeField(auto_now_add=True, blank=True)