import os
import moviepy.editor as mp
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from app.models import SaveFile
from django.conf import settings
from django.shortcuts import render, redirect
from PIL import Image
# Create your views here.




def index(request):

    return render(request, "compressor.html")


def compress_video_view(request):

    if request.method == 'POST':
        percentage = int(request.POST.get('percentage'))
        video = request.FILES.get('video-file')
        output_file = f"compressed_{video.name}"
        try:
            clip = mp.VideoFileClip(video.temporary_file_path())
        except AttributeError:
            messages.error(request, "This is Already compressed!, Please upload original video to compress!")
            return redirect('home-page')

        clip_resized = clip.resize(round(percentage/100,2))
        saved_file = FileSystemStorage(location=settings.STATIC_ROOT)
        output_path = os.path.join(settings.STATIC_ROOT, output_file)
        clip_resized.write_videofile(output_path)
        video_url = saved_file.url(output_file)
        file = SaveFile(file_name=output_file, file_url=f"media{video_url}")
        file.save()
        return render(request, "compressor.html", {'video_url':video_url})



def compress_image_view(request):

    if request.method == 'POST':
        quality = int(request.POST.get('quality'))
        image = request.FILES.get('image-file')
        output_file = f"compressed_{image.name}"
        saved_file = FileSystemStorage(location=settings.STATIC_ROOT)
        with Image.open(image) as img:
            img.save(os.path.join(settings.STATIC_ROOT, output_file), optimize=True, quality=quality)

        image_url = saved_file.url(output_file)
        file = SaveFile(file_name=output_file, file_url=f"media{image_url}")
        file.save()
        return render(request, "compressor.html", {'image_url':image_url})
