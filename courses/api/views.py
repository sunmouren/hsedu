# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/12/9 13:14
@desc: 
"""

from rest_framework import generics

from ..models import Course, Chapter, Video
from .serializers import CourseSerializer, ChapterSerializer, VideoSerializer


class CourseList(generics.ListCreateAPIView):
    """
    课程列表，包涵检索、创建
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    课程详情，包涵检索、更新、删除方法
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseChapterList(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Chapter.objects.filter(course_id=course_id)


class VideoList(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Video.objects.filter(chapter__course_id=course_id)


# from .serializers import CourseDetailSerializer, \
#     CourseListSerializer, VideoDetailSerializer
#
#
# class CourseListView(generics.ListAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseListSerializer
#
#
# class CourseDetailView(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseDetailSerializer
#
#
# class VideoDetailView(generics.RetrieveAPIView):
#     queryset = Video
#     serializer_class = VideoDetailSerializer
