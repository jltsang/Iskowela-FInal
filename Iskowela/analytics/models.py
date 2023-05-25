from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone


class Monitor(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    page_visited = models.CharField(max_length=50, blank=True, null=True)
    continent = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    datetime = models.DateTimeField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    time_spent = models.IntegerField(default=0)

    def __str__(self):
        return self.ip
    
    


class TimeTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.CharField(max_length=255)
    start_time = models.DateTimeField(default=timezone.now())
    last_update = models.DateTimeField()
    time_spent = models.IntegerField(default=0)

    def __str__(self):
        return self.page