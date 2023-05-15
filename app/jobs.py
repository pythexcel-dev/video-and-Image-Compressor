import os
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, timezone
from app.models import SaveFile

 

def delete_files():
    file_count = 0
    files = SaveFile.objects.all()
    if files:
        for file in files:
            file_path = os.path.join(settings.STATIC_ROOT, file.file_name)
            time_difference = datetime.now(timezone.utc) - file.add_time
            if time_difference.total_seconds() >= 7200:
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    print("file is already deleted")    
                file.delete()
                file_count += 1 
    else:
        print("No files to delete at this time") 
  
    print(f"{file_count} files deleted")


def start(request):
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_files, 'interval', seconds=10)
    scheduler.start()
    return HttpResponse("Scheduler started successfully!")
