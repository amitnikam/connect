from django.contrib import admin
from .models import Post, Comment

admin.site.site_header = 'CONNECT BACKEND'
admin.site.site_title = "Connect Admin Portal"
admin.site.index_title = "Welcome to Connect's Admin Portal"

admin.site.register(Post)
admin.site.register(Comment)
