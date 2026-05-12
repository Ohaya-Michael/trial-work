from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Q 

from .models import UserProfile, Song, Album, Artist
from .forms import SongForm, AlbumForm, ArtistForm


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


class HelloWorldView(LoginRequiredMixin, TemplateView):
    template_name = 'hello_world.html'


class MyLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your list items here
        context['features'] = Song.objects.all()  # Beispiel: die ersten 5 Songs aus der Datenbank
        return context
    
    def get_success_url(self):
        return reverse('public_profile', kwargs={'user_slug': self.request.user.username})


# class PublicProfileView(TemplateView):
#     template_name = 'public_profile.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Suche nach 'slug', um den FieldError zu vermeiden
#         profile = get_object_or_404(UserProfile, slug=self.kwargs.get('user_slug'))

#         context['user_profile'] = profile
#         # Wir holen beispielhaft die ersten 5 Songs aus der Datenbank
#         from .models import Song
#         context['top_songs'] = Song.objects.filter(artist=profile.favorite_song.artist)[:5]
#         return context
class PublicProfileView(TemplateView):
    template_name = 'public_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Profil laden
        profile = get_object_or_404(UserProfile, slug=self.kwargs.get('user_slug'))
        context['user_profile'] = profile

        # Basis-Queryset für die Songs dieses Profils
        songs_queryset = Song.objects.filter(artist=profile.favorite_song.artist)

        # Suchbegriff aus der URL abfangen (?q=suchbegriff)
        search_query = self.request.GET.get('q', '').strip()
        
        if search_query:
            # Filtert, wenn der Suchbegriff im Songtitel ODER Künstlernamen vorkommt (case-insensitive)
            songs_queryset = songs_queryset.filter(
                Q(title__icontains=search_query) | 
                Q(artist__name__icontains=search_query)
            )
            # Suchbegriff im Kontext speichern, um ihn im Suchfeld anzuzeigen
            context['search_query'] = search_query

        # Die gefilterten Top 5 Songs an das Template übergeben
        context['top_songs'] = songs_queryset[:5]
        return context

class SongDetailView(TemplateView):
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