# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/12/8 23:51
@desc: 
"""

from rest_framework import serializers

from users.api.serializers import UserProfileSerializer

from ..models import Course, Video, Chapter


class CourseSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'overview', 'created', 'user']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'url']


class ChapterSerializer(serializers.ModelSerializer):
    video_set = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'chapter_number', 'title', 'overview', 'video_set']


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['nickname', 'username']


# class VideoListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Video
#         fields = ['id', 'title', 'url']
#
#
# class ChapterSerializer(serializers.ModelSerializer):
#     video_set = VideoListSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Chapter
#         fields = ['id', 'chapter_number', 'title', 'overview', 'video_set']
#
#
# class VideoDetailSerializer(serializers.ModelSerializer):
#     chapter = ChapterSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Video
#         fields = ['id', 'title', 'url', 'chapter']
#
#
# class CourseDetailSerializer(serializers.ModelSerializer):
#     chapter_set = ChapterSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Course
#         fields = ['id', 'title', 'overview', 'image', 'chapter_set']
#
#
# class CourseListSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Course
#         fields = ['id', 'title', 'overview']



