from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
    
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Q 

from .models import UserProfile, Song, Album, Artist, SongRating
from .forms import SongForm, AlbumForm, ArtistForm, RatingForm


class GlobalLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_id = request.user.id
            # Get all non-expired sessions
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            
            for session in sessions:
                data = session.get_decoded()
                # Check if the user's ID matches the session data
                if str(user_id) == data.get('_auth_user_id'):
                    session.delete()
            
            # Perform the standard Django logout
            logout(request)
            
        return redirect('login')


class MyRegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class MyLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your list items here
        context['features'] = Song.objects.all() 
        return context
    
    def get_success_url(self):
        return reverse('public_profile', kwargs={'user_slug': self.request.user.username})


class PublicProfileView(TemplateView):
    template_name = 'public_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Profil laden
        try:
            profile = UserProfile.objects.get(slug=self.kwargs.get('user_slug'))
        except UserProfile.DoesNotExist:
            # If the missing profile belongs to the logged-in user, create it on the fly
            if self.request.user.is_authenticated and self.request.user.username == self.kwargs.get('user_slug'):
                profile = UserProfile.objects.create(user=self.request.user, slug=self.request.user.username)
            else:
                raise Http404("No UserProfile matches the given query.")
        context['user_profile'] = profile

        if profile.favorite_song and profile.favorite_song.artist:
            songs_queryset = Song.objects.filter(artist=profile.favorite_song.artist)
        else:
            songs_queryset = Song.objects.none()

        search_query = self.request.GET.get('q', '').strip()
        
        if search_query:
            songs_queryset = songs_queryset.filter(
                Q(title__icontains=search_query) | 
                Q(artist__name__icontains=search_query)
            )
            context['search_query'] = search_query

        # Die gefilterten Top 5 Songs an das Template übergeben
        context['top_songs'] = songs_queryset[:5]
        return context


class SongDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'song_detail.html'

    def get_object(self):
        return get_object_or_404(
            Song.objects.select_related('artist', 'album'),
            slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song'] = self.get_object()
        return context


class RateSongView(LoginRequiredMixin, View):
    def post(self, request, slug):
        song = get_object_or_404(Song, slug=slug)
        form = RatingForm(request.POST)
        if form.is_valid():
            SongRating.objects.update_or_create(
                song=song,
                user=request.user,
                defaults={'score': form.cleaned_data['score']}
            )
        return redirect('song-detail-view', slug=slug)


class EditSongView(LoginRequiredMixin, UpdateView):
    model = Song
    form_class = SongForm
    template_name = 'edit_song.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('song-detail-view', kwargs={'slug': self.object.slug})


class AddSongView(LoginRequiredMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = 'add_content.html'
    success_url = reverse_lazy('add-song')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Song'
        return context


class AddAlbumView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'add_content.html'
    success_url = reverse_lazy('add-album')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Album'
        return context


class AddArtistView(LoginRequiredMixin, CreateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'add_content.html'
    success_url = reverse_lazy('add-artist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Artist'
        return context