from django.contrib import admin

from .models import Comment, CommentNotification

# Register your models here.
admin.site.register(Comment)
admin.site.register(CommentNotification)