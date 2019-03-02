# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/17 16:03
@desc: 
"""
from django.urls import path

from .views import ChapterTestList, SubmitSingleChoice, \
    AddNote, ChapterTestListSubmit, CreateExercises, SendExercises, MyCreated


app_name = 'questionbanks'

urlpatterns = [
    path('list/<int:course_id>/<int:chapter_number>/',
         ChapterTestList.as_view(), name='test-list'),
    path('list/submitted/<int:course_id>/<int:chapter_number>/',
         ChapterTestListSubmit.as_view(), name='test-list-submitted'),
    path('sub/sc/', SubmitSingleChoice.as_view()),
    path('add/note/', AddNote.as_view()),
    path('create/exercises/<int:course_id>/<int:chapter_number>/',
         CreateExercises.as_view(), name='create-exercises'),
    path('send/exercises/', SendExercises.as_view()),
    path('my/created/<int:course_id>/<int:chapter_number>/',
         MyCreated.as_view(), name='my-created'),
]