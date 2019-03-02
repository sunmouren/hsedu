# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/10 19:59
@desc: 
"""

from django.urls import path

from .views import AddComment, AddLike, CommentNotificationList


app_name = 'comments'

urlpatterns = [
    path('add/', AddComment.as_view()),
    path('like/', AddLike.as_view()),
    path('notifications/', CommentNotificationList.as_view(), name='notifications')
]