# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/11/21 13:29
@desc: 
"""
from django.urls import path

from .views import CourseDetail, CourseVideoDetail, CourseList, \
    AddVideoWatchProgress, SubscribeCourse, \
    ClassGradeDetail, SubSignIn, CosSign, AddSignIn, \
    UploadVideo, UploadToken, AddChapter, AddCourse, AddClassGrade, course_search


app_name = 'courses'

urlpatterns = [
    path('add/', AddCourse.as_view(), name='add-course'),
    path('detail/<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    path('list/', CourseList.as_view(), name='course-list'),
    path('video/<int:pk>/', CourseVideoDetail.as_view(), name='course-video'),
    path('addvwp/', AddVideoWatchProgress.as_view()),
    path('subscribe/', SubscribeCourse.as_view()),
    path('class/detail/<int:pk>/', ClassGradeDetail.as_view(), name='class-detail'),
    path('add/sign/', AddSignIn.as_view()),
    path('sub/sign/', SubSignIn.as_view()),
    path('cos/sign/', CosSign.as_view()),
    path('upload/video/<int:cid>/<int:chapter_id>/', UploadVideo.as_view(), name='upload-video'),
    path('upload/video/', UploadVideo.as_view()),
    path('upload/token/', UploadToken.as_view()),
    path('add/chapter/<int:cid>', AddChapter.as_view(), name='add-chapter'),
    path('add/chapter/', AddChapter.as_view()),
    path('add/class/<int:cid>/', AddClassGrade.as_view(), name='add-classgrade'),
    path('add/class/', AddClassGrade.as_view()),
    path('search/', course_search, name='course-search'),
]