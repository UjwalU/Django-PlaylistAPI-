from rest_framework import serializers
from .models import Playlist, Song, PlaylistSong

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'name', 'artist', 'release_year']

class PlaylistSongSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)

    class Meta:
        model = PlaylistSong
        fields = ['id', 'song', 'position']

class PlaylistSerializer(serializers.ModelSerializer):
    songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True, write_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs']

    def create(self, validated_data):
        songs_data = validated_data.pop('songs')
        playlist = Playlist.objects.create(**validated_data)
        for idx, song_data in enumerate(songs_data):
            PlaylistSong.objects.create(playlist=playlist, song=song_data, position=idx + 1)
        return playlist