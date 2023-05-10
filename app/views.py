import os
import moviepy.editor as mp
from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import render, redirect
from PIL import Image
# Create your views here.




def index(request):

    return render(request, "compressor.html")


def compress_video_view(request):
    compressed_file = None

    if request.method == 'POST':
        percentage = int(request.POST.get('percentage'))
        video = request.FILES.get('video-file')
        global output_file
        output_file = "compressed_"+ video.name
        try:
            clip = mp.VideoFileClip(video.temporary_file_path())
        except AttributeError:
            messages.error(request, "This is Already compressed!, Please upload original video to compress!")
            return redirect('home-page')

        clip_resized = clip.resize(round(percentage/100,2))
        clip_resized.write_videofile(output_file)
        print(clip.w, clip.h)
        print(clip_resized.w, clip_resized.h)
        new_video = os.path.abspath(output_file)
        
        return render(request, "compressor.html", {'new_video':new_video})
    
    compressed_file = os.path.abspath(output_file)
    response = FileResponse(open(compressed_file, 'rb'), as_attachment=True)
    return response


def compress_image_view(request):
    compressed_file = None

    if request.method == 'POST':
        quality = int(request.POST.get('quality'))
        image = request.FILES.get('image-file')
        global output_file
        output_file = "compressed_"+ image.name
        
        with Image.open(image) as img:
            img.save(output_file, optimize=True, quality=quality)

        new_image = os.path.abspath(output_file) 

        return render(request, "compressor.html", {'new_image':new_image})
    
    compressed_file = os.path.abspath(output_file)
    response = FileResponse(open(compressed_file, 'rb'), as_attachment=True)

    return response
