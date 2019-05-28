# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/11/21 13:29
@desc: 
"""
from django.urls import path

from .views import CourseDetail, VideoDetail, CourseList, \
    AddVideoWatchProgress, SubscribeCourse, \
    ClassDetail, AddVideo, AddCourse, AddClass, course_search, AddCourseResource


app_name = 'courses'

urlpatterns = [
    path('add/', AddCourse.as_view(), name='add-course'),
    path('<int:course_id>/video/add/', AddVideo.as_view(), name='add-video'),
    path('video/add/', AddVideo.as_view()),
    path('detail/<int:course_id>/', CourseDetail.as_view(), name='course-detail'),
    path('list/', CourseList.as_view(), name='course-list'),
    path('video/<int:pk>/', VideoDetail.as_view(), name='course-video'),
    path('addvwp/', AddVideoWatchProgress.as_view()),
    path('subscribe/', SubscribeCourse.as_view()),
    path('class/detail/<int:class_id>/', ClassDetail.as_view(), name='class-detail'),
    path('add/class/<int:cid>/', AddClass.as_view(), name='add-class'),
    path('add/class/', AddClass.as_view()),
    path('add/resource/<int:cid>', AddCourseResource.as_view(), name='add-course-resource'),
    path('add/resource/', AddCourseResource.as_view()),
    path('search/', course_search, name='course-search'),
]