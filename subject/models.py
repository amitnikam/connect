from django.db import models
from django.utils import timezone
from PIL import Image

class Subject(models.Model):
    code = models.CharField(max_length=21, primary_key=True)
    name = models.CharField(max_length=100)
    sub_icon = models.ImageField(default='sub_default.jpg', upload_to='sub_icons')
    keywords = models.CharField(max_length=100)
    bio = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    #follow =


    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.sub_icon)

        if img.height > 300 or img.width > 300:
            from django.core.files.base import ContentFile
            from io import BytesIO
            output_size = (300, 300)
            img.thumbnail(output_size)
            thumb_io = BytesIO()
            img.save(thumb_io, img.format)
            file_name = self.sub_icon.name
            self.sub_icon.save(
                       file_name,
                        ContentFile(
                                    thumb_io.getvalue()),
                        save=False)
            super().save(*args, **kwargs)
