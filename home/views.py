from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Playlist, Song, PlaylistSong, models
from .serializers import PlaylistSerializer, PlaylistSongSerializer, SongSerializer
from django.db.models import F
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SongCreateView(generics.CreateAPIView):
    serializer_class = SongSerializer

class SongListView(generics.ListAPIView):
    serializer_class = SongSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = Song.objects.all().order_by('id')
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

class PlaylistCreateView(generics.CreateAPIView):
    serializer_class = PlaylistSerializer

class PlaylistListView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = Playlist.objects.all().order_by('id')
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset


class PlaylistUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class PlaylistSongListView(generics.ListAPIView):
    serializer_class = PlaylistSongSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        playlist_id = self.kwargs['playlist_id']
        playlist = get_object_or_404(Playlist, id=playlist_id)
        return PlaylistSong.objects.filter(playlist=playlist)

class PlaylistSongUpdateView(generics.UpdateAPIView):
    queryset = PlaylistSong.objects.all()
    lookup_url_kwarg = 'song_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_position = request.data.get('position')

        if new_position is None:
            return Response({'error': 'Missing position parameter'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_position = int(new_position)
        except ValueError:
            return Response({'error': 'Invalid position value'}, status=status.HTTP_400_BAD_REQUEST)

        playlist = instance.playlist
        existing_positions = list(PlaylistSong.objects.filter(playlist=playlist).values_list('position', flat=True))

        if new_position < 1 or new_position > len(existing_positions):
            return Response({'error': 'Invalid position value'}, status=status.HTTP_400_BAD_REQUEST)

        old_position = instance.position
        instance.position = new_position

        if old_position < new_position:
            for position in existing_positions[old_position:new_position]:
                playlist_song = PlaylistSong.objects.get(playlist=playlist, position=position)
                playlist_song.position -= 1
                playlist_song.save()
        else:
            for position in existing_positions[new_position:old_position]:
                playlist_song = PlaylistSong.objects.get(playlist=playlist, position=position)
                playlist_song.position += 1
                playlist_song.save()

        instance.save()
        return Response({'position': instance.position}, status=status.HTTP_200_OK)

class PlaylistSongUpdateView(generics.UpdateAPIView):
    queryset = PlaylistSong.objects.all()
    serializer_class = PlaylistSongSerializer  # Specify the serializer class here
    lookup_url_kwarg = 'song_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_position = request.data.get('position')

        if new_position is None:
            return Response({'error': 'Missing position parameter'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_position = int(new_position)
        except ValueError:
            return Response({'error': 'Invalid position value'}, status=status.HTTP_400_BAD_REQUEST)

        playlist = instance.playlist
        existing_positions = list(PlaylistSong.objects.filter(playlist=playlist).values_list('position', flat=True))

        if new_position < 1 or new_position > len(existing_positions):
            return Response({'error': 'Invalid position value'}, status=status.HTTP_400_BAD_REQUEST)

        old_position = instance.position
        instance.position = new_position

        if old_position < new_position:
            for position in existing_positions[old_position:new_position]:
                playlist_song = PlaylistSong.objects.get(playlist=playlist, position=position)
                playlist_song.position -= 1
                playlist_song.save()
        else:
            for position in existing_positions[new_position:old_position]:
                playlist_song = PlaylistSong.objects.get(playlist=playlist, position=position)
                playlist_song.position += 1
                playlist_song.save()

        instance.save()
        return Response({'position': instance.position}, status=status.HTTP_200_OK)
class PlaylistSongDeleteView(generics.DestroyAPIView):
    queryset = PlaylistSong.objects.all()
    lookup_url_kwarg = 'song_id'  # Assuming 'song_id' is the URL parameter name

    def delete(self, request, *args, **kwargs):
        playlist_id = self.kwargs['playlist_id']
        song_id = self.kwargs['song_id']  # Use the correct lookup field name

        try:
            # Get the playlist song object
            playlist_song = PlaylistSong.objects.get(playlist_id=playlist_id, song_id=song_id)
        except PlaylistSong.DoesNotExist:
            return Response({'error': 'Playlist song not found'}, status=status.HTTP_404_NOT_FOUND)

        old_position = playlist_song.position
        playlist = playlist_song.playlist

        # Delete the playlist song
        playlist_song.delete()

        # Update positions of songs after the deleted song
        PlaylistSong.objects.filter(playlist=playlist, position__gt=old_position).update(position=models.F('position') - 1)

        return Response({'message': 'Song has been removed from the playlist'}, status=status.HTTP_200_OK)