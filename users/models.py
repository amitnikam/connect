from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)
    profession = models.CharField(max_length=30, null=True, blank=True)
    full_name = models.CharField(max_length=30, null=True, blank=True)
    contact_me_at = models.TextField(null=True, blank=True)
    skill_1 = models.CharField(max_length=30, null=True, blank=True)
    skill_2 = models.CharField(max_length=30, null=True, blank=True)
    skill_3 = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic)

        if img.height > 300 or img.width > 300:
            from django.core.files.base import ContentFile
            from io import BytesIO
            output_size = (300, 300)
            img.thumbnail(output_size)
            thumb_io = BytesIO()
            img.save(thumb_io, img.format)
            file_name = self.profile_pic.name
            self.profile_pic.save(
                       file_name,
                        ContentFile(
                                    thumb_io.getvalue()),
                        save=False)
            super().save(*args, **kwargs)

