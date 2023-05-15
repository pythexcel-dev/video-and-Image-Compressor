from django.db import models


class SaveFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_url = models.CharField(max_length=255)
    add_time = models.DateTimeField(auto_now_add=True)

