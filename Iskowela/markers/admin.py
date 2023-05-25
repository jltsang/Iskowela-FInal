from django.contrib import admin

from .models import Event_Suggestions, Event_Markers, Place_Suggestions, Place_Markers

admin.site.register(Event_Suggestions)
admin.site.register(Event_Markers)
admin.site.register(Place_Suggestions)
admin.site.register(Place_Markers)