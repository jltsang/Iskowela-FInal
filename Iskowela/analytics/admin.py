from django.contrib import admin

# Register your models here.
from .models import Monitor, TimeTracking
admin.site.register(Monitor)
admin.site.register(TimeTracking)
