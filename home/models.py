from django.db import models

class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    release_year = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song, through='PlaylistSong')

    def __str__(self):
        return self.name

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('playlist', 'position')
        ordering = ['position']

    def __str__(self):
        return f"{self.song.name} (Position: {self.position})"