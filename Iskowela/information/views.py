from django.shortcuts import render
from users.models import Profile
from .models import ProcessGuide, Courses, Scholarships
from main.models import Toggles
from django.urls import reverse_lazy
from django.views.generic import (
	CreateView, 
	UpdateView, 
	DeleteView
)
from django.http import Http404
import requests
from analytics.views import get_session


class BaseForm:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Information'
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

def processguide_list(request, profile_id):
	get_session(request, profile_id, "process")
	context = {
		'title': 'Process Guides',
		'processguides': ProcessGuide.objects.filter(profile = profile_id),
		'toggles': Toggles.objects.get(profile = profile_id),
		'profile_id': profile_id,
		'active_profile': Profile.objects.get(id=profile_id),
	}
	return render(request, 'information/processguides.html', context)

def course_list(request, profile_id):
	get_session(request, profile_id, "course")
	context = {
		'title': 'Course List',
		'courses': Courses.objects.filter(profile = profile_id),
		'toggles': Toggles.objects.get(profile = profile_id),
		'profile_id': profile_id,
		'active_profile': Profile.objects.get(id=profile_id),
	}
	return render(request, 'information/courses.html', context)

def scholarship_list(request, profile_id):
	get_session(request, profile_id, "scholarship")
	context = {
		'title': 'Scholarships',
		'scholarships': Scholarships.objects.filter(profile = profile_id),
		'toggles': Toggles.objects.get(profile = profile_id),
		'profile_id': profile_id,
		'active_profile': Profile.objects.get(id=profile_id),
	}
	return render(request, 'information/scholarships.html', context)

class ProcessGuidesCreateView(BaseForm, CreateForm, CreateView):
	model = ProcessGuide
	fields = ['profile', 'process_name', 'description']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

class ProcessGuidesUpdateView(BaseForm, UpdateView):
	model = ProcessGuide
	fields = ['profile', 'process_name', 'description']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

class ProcessGuidesDeleteView(BaseForm, DeleteView):
	model = ProcessGuide
	
	def get_success_url(self):
		return reverse_lazy("processguides", kwargs={"profile_id": self.object.profile.id})

class ScholarshipsCreateView(BaseForm, CreateForm, CreateView):
	model = Scholarships
	fields = ['profile', 'scholarship_name', 'description']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

class ScholarshipsUpdateView(BaseForm, UpdateView):
	model = Scholarships
	fields = ['profile', 'scholarship_name', 'description']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

class ScholarshipsDeleteView(BaseForm,DeleteView):
	model = Scholarships

	def get_success_url(self):
		return reverse_lazy("scholarships", kwargs={"profile_id": self.object.profile.id})
	
class CoursesCreateView(BaseForm, CreateForm, CreateView):
	model = Courses
	fields = ['profile', 'college_group', 'course_list']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

class CoursesUpdateView(BaseForm, UpdateView):
	model = Courses
	fields = ['profile', 'college_group', 'course_list']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

class CoursesDeleteView(BaseForm, DeleteView):
	model = Courses

	def get_success_url(self):
		return reverse_lazy("courses", kwargs={"profile_id": self.object.profile.id})