from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import Profile

class Event_Markers(models.Model):
	class EventType(models.IntegerChoices):
		OFFLINE = 1
		ONLINE = 2
		
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
	name = models.CharField(max_length=100)
	type = models.IntegerField(choices=EventType.choices)
	description = models.CharField(max_length=100, default='')
	event_date = models.DateTimeField()
	longitude = models.DecimalField(default=0, decimal_places=20, max_digits=25)
	latitude = models.DecimalField(default=0, decimal_places=20, max_digits=25)
	last_updated = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('markers', args=[self.profile.id, 1])


class Place_Markers(models.Model):
	class PlaceType(models.IntegerChoices):
		HEALTH = 1
		FOOD = 2
		FINANCE = 3
		STORE = 4
		ETC = 5
	
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
	name = models.CharField(max_length=100)
	type = models.IntegerField(choices=PlaceType.choices)
	description = models.CharField(max_length=100, default='')
	longitude = models.DecimalField(default=0, decimal_places=20, max_digits=25)
	latitude = models.DecimalField(default=0, decimal_places=20, max_digits=25)
	last_updated = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('markers', args=[self.profile.id, 2])

class Event_Suggestions(models.Model):
	class EventType(models.IntegerChoices):
		OFFLINE = 1
		ONLINE = 2
	class Action(models.IntegerChoices):
		CREATE = 1
		UPDATE = 2
		DELETE = 3
		
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
	event_marker = models.ForeignKey(Event_Markers, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	type = models.IntegerField(choices=EventType.choices, null=True, blank=True)
	description = models.CharField(max_length=100, default='')
	event_date = models.DateTimeField(null=True, blank=True)
	cud = models.IntegerField(choices=Action.choices)
	longitude = models.DecimalField(default=0, decimal_places=20, max_digits=25, null=True, blank=True)
	latitude = models.DecimalField(default=0, decimal_places=20, max_digits=25, null=True, blank=True)
	date_posted = models.DateTimeField(default=timezone.now)
	
	def __str__(self):
		if self.name:
			return self.name
		else:
			return self.event_marker.name
			
	def get_absolute_url(self):
		return reverse('markers', args=[self.profile.id, 1])

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.event_marker is not None:
			self.name = self.event_marker.name
			if self.cud == 3:
				self.type = self.event_marker.type
				self.event_date = self.event_marker.event_date
				self.longitude = self.event_marker.longitude
				self.latitude = self.event_marker.latitude

class Place_Suggestions(models.Model):
	class PlaceType(models.IntegerChoices):
		HEALTH = 1
		FOOD = 2
		FINANCE = 3
		STORE = 4
		ETC = 5
	class Action(models.IntegerChoices):
		CREATE = 1
		UPDATE = 2
		DELETE = 3
		
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
	place_marker = models.ForeignKey(Place_Markers, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	type = models.IntegerField(choices=PlaceType.choices, null=True, blank=True)
	description = models.CharField(max_length=100, default='')
	cud = models.IntegerField(choices=Action.choices)
	longitude = models.DecimalField(default=0, decimal_places=20, max_digits=25, null=True, blank=True)
	latitude = models.DecimalField(default=0, decimal_places=20, max_digits=25, null=True, blank=True)
	date_posted = models.DateTimeField(default=timezone.now)
	
	def __str__(self):
		if self.name:
			return self.name
		else:
			return self.place_marker.name

	def get_absolute_url(self):
		return reverse('markers', args=[self.profile.id, 2])

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.place_marker is not None:
			self.name = self.place_marker.name
			if self.cud == 3:
				self.type = self.place_marker.type
				self.longitude = self.place_marker.longitude
				self.latitude = self.place_marker.latitude