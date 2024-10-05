from django.shortcuts import render, redirect
from .models import MusicFile
from .spotify_client import get_genre


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        track_name = request.POST['track_name']
        genre = get_genre(track_name)
        music_file = MusicFile(
            file=uploaded_file, track_name=track_name, genre=genre)
        music_file.save()
        return redirect('success')
    return render(request, 'upload.html')


def success(request):
    return render(request, 'success.html')
