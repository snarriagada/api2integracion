from django.urls import path

from . import views


urlpatterns = [
    path('artists', views.ListArtist.as_view()),
    path('artists/<str:pk>', views.ArtistbyID.as_view()),
    path('artists/<str:pk>/albums', views.AlbumbyID.as_view()),
    path('albums', views.ListAlbum.as_view()),
    path('albums/<str:pk>', views.OneAlbum.as_view()),

    path('albums/<str:pk>/tracks', views.TrackbyId.as_view()),
    path('tracks', views.ListTrack.as_view()),
    path('tracks/<str:pk>', views.OneTrack.as_view()),
    path('artists/<str:pk>/tracks', views.TracksArtists.as_view()),
    path('tracks/<str:pk>/play', views.PlayTrack.as_view()),
    path('albums/<str:pk>/tracks/play', views.PlayAlbum.as_view()),
    path('artists/<str:pk>/albums/play', views.PlayArtist.as_view()),



]