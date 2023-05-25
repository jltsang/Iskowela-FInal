from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import Profile

# Create your models here.

class ProcessGuide(models.Model):
    class Application(models.IntegerChoices):
        OTHERS = 1
        APPLY = 2
                
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    process_name = models.TextField(default='')
    description = models.TextField(default='')
    last_updated = models.DateTimeField(default=timezone.now)
    apply = models.IntegerField(choices=Application.choices, default=1)
    
    def __str__(self):
        return self.process_name
    
    def get_absolute_url(self):
        return reverse('processguides', args=[self.profile.id])

class Courses(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    college_group = models.TextField(default='')
    course_list = models.JSONField(default=dict)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.college_group

    def get_absolute_url(self):
        return reverse('courses', args=[self.profile.id])

class Scholarships(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    scholarship_name = models.TextField(default='')
    description = models.TextField(default='')
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.scholarship_name

    def get_absolute_url(self):
        return reverse('scholarships', args=[self.profile.id])
