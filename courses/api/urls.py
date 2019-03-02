# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/12/9 13:14
@desc: 
"""

from django.urls import path

from .views import CourseList, CourseDetail, CourseChapterList, VideoList


app_name = 'courses'

urlpatterns = [
    path('courses/', CourseList.as_view()),
    path('courses/<pk>/', CourseDetail.as_view()),
    path('course/<course_id>/videos/', VideoList.as_view()),
    path('course/chapters/<course_id>/', CourseChapterList.as_view()),
]