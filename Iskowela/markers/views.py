from django.shortcuts import render
from users.models import Profile
from .models import Event_Markers, Event_Suggestions, Place_Markers, Place_Suggestions
from main.models import Toggles
from django.urls import reverse_lazy
from django.views.generic import (
	CreateView, 
	UpdateView, 
	DeleteView
)
from django.forms import DateTimeInput
from django.http import Http404
from analytics.views import get_session

class BaseForm:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Markers'
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

class EventForm:
	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['latitude'].widget = form.fields['latitude'].hidden_widget()
		form.fields['longitude'].widget = form.fields['longitude'].hidden_widget()
		form.fields['event_date'].widget = DateTimeInput(attrs={'type': 'datetime-local'})

		return form
	
class PlaceForm:
	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['latitude'].widget = form.fields['latitude'].hidden_widget()
		form.fields['longitude'].widget = form.fields['longitude'].hidden_widget()

		return form
	
class CreateForm:
	def dispatch(self, request, *args, **kwargs):
		profile_id = self.kwargs['profile_id']
		profile = Profile.objects.get(id=profile_id)
		if profile.user != self.request.user:
			raise Http404("You are not allowed to create a new object for this profile.")
		return super().dispatch(request, *args, **kwargs)

def markers(request, profile_id, mtype):
	get_session(request, profile_id, "markers")
	
	context = {
		'title': 'Markers',
		'mtype': mtype,
		'places': Place_Markers.objects.filter(profile = profile_id),
		'events' : Event_Markers.objects.filter(profile = profile_id),
		'event_suggestions' : Event_Suggestions.objects.filter(profile = profile_id),
		'place_suggestions' : Place_Suggestions.objects.filter(profile = profile_id),
		'toggles': Toggles.objects.get(profile = profile_id),
		'profile_id': profile_id,
		'place_types': Place_Markers.PlaceType.choices,
		'event_types': Event_Markers.EventType.choices,
		'active_profile': Profile.objects.get(id=profile_id),
	}
	return render(request, 'markers/map.html', context)
	
class EventCreateView(BaseForm, CreateForm, EventForm, CreateView):
	model = Event_Markers
	fields = ['profile', 'name', 'type', 'description', 'event_date', 'latitude', 'longitude'] 

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form
	
	def get_initial(self):
		initial = super().get_initial()
		initial.update(self.request.GET.dict())
		return initial

class EventUpdateView(BaseForm, EventForm, UpdateView):
	model = Event_Markers
	fields = ['profile', 'name', 'type', 'description', 'event_date', 'longitude', 'latitude']
	
	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

	def get_initial(self):
		initial = super().get_initial()
		initial.update(self.request.GET.dict())
		return initial

class EventDeleteView(BaseForm, DeleteView):
	model = Event_Markers

	def get_success_url(self):
		return reverse_lazy("markers", kwargs={"profile_id": self.object.profile.id, "mtype": 1})


class PlaceCreateView(BaseForm, CreateForm, PlaceForm, CreateView):
	model = Place_Markers
	fields = ['profile', 'name', 'type', 'description', 'latitude', 'longitude']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

	def get_initial(self):
		initial = super().get_initial()
		initial.update(self.request.GET.dict())
		return initial

class PlaceUpdateView(BaseForm, PlaceForm, UpdateView):
	model = Place_Markers
	fields = ['profile', 'name', 'type', 'description', 'longitude', 'latitude']
	
	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()

		return form

	def get_initial(self):
		initial = super().get_initial()
		initial.update(self.request.GET.dict())
		return initial
	
class PlaceDeleteView(BaseForm, DeleteView):
	model = Place_Markers

	def get_success_url(self):
		return reverse_lazy("markers", kwargs={"profile_id": self.object.profile.id, "mtype": 2})
	
class DeletePopup(BaseForm, DeleteView):
	model = Place_Markers

	def get_success_url(self):
		return reverse_lazy("markers", kwargs={"profile_id": self.object.profile.id, "mtype": 2})
	
class SuggestEventCreateView(BaseForm, EventForm, CreateView):
	model = Event_Suggestions
	fields = ['profile', 'cud', 'event_marker', 'name', 'type', 'description', 'event_date', 'longitude', 'latitude']
	
	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()
		form.fields['event_marker'].queryset = Event_Markers.objects.filter(profile=self.kwargs['profile_id'])

		return form

class SuggestPlaceCreateView(BaseForm, PlaceForm, CreateView):
	model = Place_Suggestions
	fields = ['profile', 'cud', 'place_marker', 'name', 'type', 'description', 'longitude', 'latitude']
	
	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['profile'].widget = form.fields['profile'].hidden_widget()
		form.fields['place_marker'].queryset = Place_Markers.objects.filter(profile=self.kwargs['profile_id'])

		return form

class SuggestEventDeleteView(BaseForm, DeleteView):
	model = Event_Suggestions
	
	def get_success_url(self):
		return reverse_lazy("markers", kwargs={"profile_id": self.object.profile.id, "mtype": 3})

class SuggestPlaceDeleteView(BaseForm, DeleteView):
	model = Place_Suggestions

	def get_success_url(self):
		return reverse_lazy("markers", kwargs={"profile_id": self.object.profile.id, "mtype": 3})


""" Extra Views
class SuggestEventUpdateView(BaseForm, EventForm, UpdateView):
	model = Event_Suggestions
	fields = ['cud', 'name', 'type', 'description', 'event_date', 'longitude', 'latitude']
	success_url = "/markers/3"

class SuggestPlaceUpdateView(BaseForm, PlaceForm, UpdateView):
	model = Place_Suggestions
	fields = ['cud', 'name', 'type', 'description', 'longitude', 'latitude']
	success_url = "/markers/3
"""