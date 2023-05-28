from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import Profile

class SSR(models.Model):
	Rating_choices = (
	    (1, 'Bad'),
	    (2, 'Poor'),
	    (3, 'Average'),
	    (4, 'Good'),
	    (5, 'Excellent')
	)

	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
	email = models.EmailField()
	information_modules_comment = models.TextField(default='')
	information_modules_rating = models.IntegerField(choices=Rating_choices, default=3)
	markers_module_comment = models.TextField(default='')
	markers_module_rating = models.IntegerField(choices=Rating_choices, default=3)
	chatbot_comment = models.TextField(default='')
	chatbot_rating = models.IntegerField(choices=Rating_choices, default=3)
	overall_comment = models.TextField(default='')
	overall_rating = models.IntegerField(choices=Rating_choices, default=3)
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.email
	
	def get_absolute_url(self):
		return reverse('ssr-create', args=[self.profile.id])