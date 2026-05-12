"""
URL configuration for django_music project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django_music.views import AddAlbumView, AddArtistView, AddSongView, GlobalLogoutView, MyLoginView, PublicProfileView, SongDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MyLoginView.as_view(), name='login'),
    path('logout/', GlobalLogoutView.as_view(), name='logout'),
    path('add/song/',   AddSongView.as_view(),   name='add-song'),
    path('add/album/',  AddAlbumView.as_view(),  name='add-album'),
    path('add/artist/', AddArtistView.as_view(), name='add-artist'),
    path('profile/<str:user_slug>/', PublicProfileView.as_view(), name='public_profile'),
    path('songs/<slug:slug>/', SongDetailView.as_view(), name='song-detail-view'),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += debug_toolbar_urls()

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
