from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User  
		fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User  
		fields = ['username', 'email']
		
class ProfileUpdateForm(forms.ModelForm):
	longitude = forms.DecimalField(widget=forms.HiddenInput())
	latitude = forms.DecimalField(widget=forms.HiddenInput())

	class Meta:
		model = Profile
		fields = ['school_name', 'logo', 'banner', 'email', 'contact_details', 'mapbox_key', 'live_chat_link', 'chatbot_tree_link', 'longitude', 'latitude']

class MainUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['school_name', 'logo', 'banner']