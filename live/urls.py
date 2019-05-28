# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/5/11 9:23
@desc: 
"""

from django.urls import path


from .views import RoomDetail


app_name = 'live'


urlpatterns = [
    path('room/<int:course_id>/', RoomDetail.as_view(), name='room-detail'),
]