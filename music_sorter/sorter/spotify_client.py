import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET'))


def get_genre(track_name):
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        artist_id = track['artists'][0]['id']
        artist = sp.artist(artist_id)
        return artist['genres']
    return None
