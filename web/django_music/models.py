# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True) # Optionales Feld für die Biografie des Künstlers

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    release_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.artist.name})"


class Song(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)  
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def average_rating(self):
        result = self.ratings.aggregate(avg=Avg('score'))['avg']
        return round(result, 1) if result else None

    def user_rating(self, user):
        try:
            return self.ratings.get(user=user).score
        except SongRating.DoesNotExist:
            return None
        
    def __str__(self):
        return f"{self.title} - {self.artist.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    # Hier speichern wir den aktuellen Lieblingssong
    favorite_song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile of {self.user.username}"
    

class SongRating(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('song', 'user')  # one rating per user per song

    def __str__(self):
        return f"{self.user.username} → {self.song.title}: {self.score}/10"