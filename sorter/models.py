from django.db import models


class MusicFile(models.Model):
    file = models.FileField(upload_to='music_files/')
    track_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255, blank=True, null=True)
