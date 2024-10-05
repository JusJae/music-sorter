from celery import shared_task
from .models import MusicFile
from .utils import get_genre


@shared_task
def process_music_file(file_path, track_name):
    genre = get_genre(track_name)
    music_file = MusicFile(file=file_path, track_name=track_name, genre=genre)
    music_file.save()
