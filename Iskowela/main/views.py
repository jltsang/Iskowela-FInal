from django.shortcuts import render, redirect
from users.models import Profile
from users.forms import MainUpdateForm
from .models import Toggles, Post
from django.contrib import messages
from django.urls import reverse_lazy
import requests
from datetime import datetime
from django.views.generic import (
	CreateView, 
	UpdateView, 
	DeleteView
)
from django.http import Http404
from analytics.views import get_session

class PostForm:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Post List'
		context['toggles'] = Toggles.objects.get(profile_id=self.kwargs['profile_id'])	
		context['profile_id'] = self.kwargs['profile_id']
		context['active_profile'] = Profile.objects.get(id=self.kwargs['profile_id'])

		return context

	def get_initial(self):
		initial = super().get_initial()
		initial['profile'] = self.kwargs['profile_id']

		return initial

	def get_object(self, queryset=None):
		obj = super().get_object(queryset=queryset)
		if obj.profile.id != self.kwargs['profile_id'] or obj.profile.user != self.request.user:
			raise Http404("You are not allowed to edit this place.")
		return obj

class CreateForm:
	def dispatch(self, request, *args, **kwargs):
		profile_id = self.kwargs['profile_id']
		profile = Profile.objects.get(id=profile_id)
		if profile.user != self.request.user:
			raise Http404("You are not allowed to create a new object for this profile.")
		return super().dispatch(request, *args, **kwargs)

def index(request, profile_id):
	get_session(request, profile_id, "home")

	context = {
		'active_profile': Profile.objects.get(id=profile_id),
		'title': 'Home',
		'toggles': Toggles.objects.get(profile=profile_id),
		'posts': Post.objects.filter(profile=profile_id).order_by('-date_posted'),
		'profile_id': profile_id,
		'active_profile': Profile.objects.get(id=profile_id),
	}
	return render(request, 'main/index.html', context)

def main_update(request):
	if request.method == 'POST':
		form = MainUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if form.is_valid() : 
			form.save()
			messages.success(request, f'Your profile has been updated!')
			return redirect('main-index')

	else:
		form = MainUpdateForm(instance=request.user.profile)
		
	context = {
		'form': form,
		'title': 'Profile Update',
	}
	return render(request, 'main/main_update.html', context)

class SettingsUpdateView(UpdateView):
	model = Toggles
	fields = ['processguides_toggle', 'courses_toggle', 'scholarships_toggle', 'markers_toggle', 'chatbot_toggle', 'web_analytics_toggle']
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Settings'
		context['toggles'] = Toggles.objects.get(profile_id=self.kwargs['profile_id'])
		context['profile_id'] = self.kwargs['profile_id']
		context['pk'] = self.kwargs['pk']
		context['active_profile'] = Profile.objects.get(id=self.kwargs['profile_id'])

		return context
	
	def get_object(self, queryset=None):
		obj = super().get_object(queryset=queryset)
		if obj.profile.id != self.kwargs['profile_id'] or obj.profile.user != self.request.user:
			raise Http404("You are not allowed to edit this place.")
		return obj
	
	def get_success_url(self):
		return reverse_lazy('settings', kwargs={'profile_id': self.kwargs['profile_id'], 'pk': self.kwargs['pk']})

class PostCreateView(PostForm, CreateForm, CreateView):
	model = Post
	fields = ['profile', 'title', 'content']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form
	
class PostUpdateView(PostForm, UpdateView):
	model = Post
	fields = ['profile', 'title', 'content']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

class PostDeleteView(PostForm, DeleteView):
	model = Post

	def get_success_url(self):
		return reverse_lazy("main-index", kwargs={"profile_id": self.object.profile.id})

