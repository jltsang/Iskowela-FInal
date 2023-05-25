from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile

class Toggles(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    info_toggle = models.BooleanField(default=False)
    processguides_toggle = models.BooleanField(default=False)
    scholarships_toggle = models.BooleanField(default=False)
    courses_toggle = models.BooleanField(default=False)
    markers_toggle = models.BooleanField(default=False)
    chatbot_toggle = models.BooleanField(default=False)
    web_analytics_toggle = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.profile.user.username}"

    def get_absolute_url(self):
        return reverse('settings', args=[self.profile.id])

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('main-index', args=[self.profile.id])



