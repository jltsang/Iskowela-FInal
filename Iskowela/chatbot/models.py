from django.db import models
from django.utils import timezone
from users.models import Profile

# Create your models here.
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    user_id = models.IntegerField()
    date = models.DateTimeField(default=timezone.now, blank=True)
    is_bot = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)