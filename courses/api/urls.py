# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/6/4 15:13
@desc: 
"""

from django.urls import path

from . import views


app_name = 'courses'


urlpatterns = [
    path('list/', views.CourseListView.as_view(), name='api-course-list'),
    path('detail/<pk>/', views.CourseDetailView.as_view(), name='api-course-detail'),
]