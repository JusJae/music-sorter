from django.conf import settings
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=settings.SPOTIPY_CLIENT_ID,
    client_secret=settings.SPOTIPY_CLIENT_SECRET
))


def get_genre(track_name):
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        artist_id = track['artists'][0]['id']
        artist = sp.artist(artist_id)
        return artist['genres']
    return None


def create_genre_directory(genre):
    base_dir = 'sorted_music'
    genre_dir = os.path.join(base_dir, genre)
    if not os.path.exists(genre_dir):
        os.makedirs(genre_dir)
    return genre_dir
