from django import forms
from .models import User
from django.contrib.auth.models import User

class Signup(forms.ModelForm):
	class Meta:
		model = User
		fields = {'username','first_name','last_name','email','password'}