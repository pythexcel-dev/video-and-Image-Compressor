from django.urls import path

from . import views

urlpatterns = [
    path("home", views.index, name="home-page"),
    path("video-compress", views.compress_video_view, name="video-compress"),
    path("image-compress", views.compress_image_view, name="image-compress"),
]