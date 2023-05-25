from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	PUBLIC = 'Public'
	PRIVATE = 'Private'
	TYPE_CHOICES = [
		(PUBLIC, 'Public'),
		(PRIVATE, 'Private'),
    ]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	school_name = models.CharField(max_length=40)
	logo = models.ImageField(default='default.jpg', upload_to='logo_pics')
	banner = models.ImageField(upload_to='media', default='banner.jpg')
	location = models.CharField(max_length=200, default='')
	type = models.CharField(max_length=7, choices=TYPE_CHOICES, default=PUBLIC)
	email = models.EmailField(default = '')
	contact_details = models.TextField()
	mapbox_key = models.CharField(max_length=100)
	live_chat_link = models.CharField(max_length=50)
	chatbot_tree_link = models.CharField(max_length=50)
	longitude = models.DecimalField(default=0, decimal_places=20, max_digits=25, null=True, blank=True)
	latitude = models.DecimalField(default=0, decimal_places=20, max_digits=25, null=True, blank=True)
	
	def __str__(self):
		return self.school_name

	# Resize the logo
	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img = Image.open(self.logo.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.logo.path)

	