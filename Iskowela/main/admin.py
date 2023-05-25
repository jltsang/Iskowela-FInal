from django.contrib import admin

from .models import Toggles
from .models import Post

admin.site.register(Toggles)
admin.site.register(Post)

