import os
import zipfile

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .models import MusicFile
from .tasks import process_music_file


def spotify_auth(request):
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope='user-library-read'
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def spotify_callback(request):
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI')
    )
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    request.session['token_info'] = token_info
    return redirect('home')


def upload_files(request):
    if request.method == 'POST':
        files = request.FILES['files']
        for uploaded_file in files:
            track_name = uploaded_file.name.rsplit('.', 1)[0]
            # Save the file temporarily to get its path
            temp_file = MusicFile(file=uploaded_file, track_name=track_name)
            temp_file.save()
            # Enqueue the task
            process_music_file.delay(temp_file.file.path, track_name)
        return redirect('success')
        # track_name = request.POST['track_name']
        # genre = get_genre(track_name)
        # music_file = MusicFile(
        #     file=uploaded_file, track_name=track_name, genre=genre)
        # music_file.save()
        # return redirect('success')
    return render(request, 'upload.html')


def success(request):
    sorted_files = MusicFile.objects.all()
    context = {'sorted_files': sorted_files}
    return render(request, 'success.html', context)


def get_user_tracks(request):
    token_info = request.session.get('token_info', {})
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_saved_tracks()
    tracks = [item['track'] for item in results['items']]
    return render(request, 'tracks.html', {'tracks': tracks})



def download_all(request):
    zip_subdir = "sorted_music"
    zip_filename = f"{zip_subdir}.zip"

    # Open Httpresponse to grab in-memory ZIP contents
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    # Zip compressor
    with zipfile.ZipFile(response, 'w') as zip_file:
        # Add files to zip
        base_dir = 'sorted_music'
        for folder_name, subfolders, filenames in os.walk(base_dir):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_file.write(file_path, os.path.relpath(file_path, base_dir))

    return response
