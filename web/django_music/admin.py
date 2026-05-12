from django.contrib import admin
from .models import Artist, Album, Song, UserProfile

admin.site.register([Artist, Album, Song, UserProfile])
