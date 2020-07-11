from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from subject.models import Subject
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    flares = (
        ('Q', 'Question'),
        ('A', 'Announcement'),
        ('I', 'Info-Share'),
        ('D', 'Discussion'),
    )
    flare = models.CharField(max_length=1, choices=flares)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    #likes =
    #dislikes =

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} --> {}'.format(str(self.user.username), self.post.title)