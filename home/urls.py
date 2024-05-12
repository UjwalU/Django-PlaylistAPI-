from django.urls import path
from . import views

urlpatterns = [
    path('api/songs/', views.SongCreateView.as_view(), name='create_song'),
    path('api/songs/list/', views.SongListView.as_view(), name='list_songs'),
    path('api/playlists/', views.PlaylistCreateView.as_view(), name='create_playlist'),
    path('api/playlists/list/', views.PlaylistListView.as_view(), name='list_playlists'),
    path('api/playlists/<int:pk>/', views.PlaylistUpdateDeleteView.as_view(), name='update_delete_playlist'),
    path('api/playlists/<int:pk>/', views.PlaylistUpdateDeleteView.as_view(), name='update_delete_playlist'),
    path('api/playlists/<int:playlist_id>/songs/', views.PlaylistSongListView.as_view(), name='list_playlist_songs'),
    path('api/playlists/<int:playlist_id>/songs/<int:song_id>/', views.PlaylistSongUpdateView.as_view(), name='update_playlist_song'),
    path('api/playlists/<int:playlist_id>/songs/<int:song_id>/delete/', views.PlaylistSongDeleteView.as_view(), name='delete_playlist_song'),

  
    ]