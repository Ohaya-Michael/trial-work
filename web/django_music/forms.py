# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import SongRating, UserProfile, Song, Album, Artist

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'password':   forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class SongUpdateForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album'] # 'rating' könnte hier hinzu
        widgets = {
            'title':  forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'album':  forms.Select(attrs={'class': 'form-select'}),
            # 'rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RatingForm(forms.ModelForm):
    score = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'max-width: 80px;',
        })
    )

    class Meta:
        model = SongRating
        fields = ['score']


class FavoriteSongForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['favorite_song']
        widgets = {
            'favorite_song': forms.Select(attrs={'class': 'form-select'}),
        }


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album'] # 'rating' könnte hier hinzugefügt werden, wenn gewünscht
        widgets = {
            'title':  forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'album':  forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
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