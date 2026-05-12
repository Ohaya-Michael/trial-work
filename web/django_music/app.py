# django_music/apps.py
from django.apps import AppConfig


class DjangoMusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_music'  # <--- Ensure this is exactly 'django_music'
