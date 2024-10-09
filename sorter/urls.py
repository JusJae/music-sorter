from django.urls import path
from . import views

urlpatterns = [
    path('spotify_auth/', views.spotify_auth, name='spotify_auth'),
    path('spotify_callback/', views.spotify_callback, name='spotify_callback'),
    path('upload/', views.upload_files, name='upload'),
    path('success/', views.success, name='success'),
]
