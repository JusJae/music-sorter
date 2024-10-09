from celery import shared_task
from .models import MusicFile
from .utils import get_genre, create_genre_directory
import shutil
import os


@shared_task
def process_music_file(file_path, track_name):
    genre = get_genre(track_name)
    music_file = MusicFile(file=file_path, track_name=track_name, genre=genre)
    music_file.save()

    genre_dir = create_genre_directory(genre)
    destination_path = os.path.join(genre_dir, os.path.basename(file_path))
    shutil.move(file_path, destination_path)
