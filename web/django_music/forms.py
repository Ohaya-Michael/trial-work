# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Song, Album, Artist

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class SongUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['favorite_song']


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album']
        widgets = {
            'title':  forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'album':  forms.Select(attrs={'class': 'form-select'}),
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'release_year']
        widgets = {
            'title':  forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }