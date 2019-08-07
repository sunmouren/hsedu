# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/6/4 15:13
@desc: 
"""

from rest_framework import serializers

from users.api.serializers import UserProfileSerializer

from ..models import Course


class CourseSerializer(serializers.ModelSerializer):

    user = UserProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'overview', 'img_url', 'user']
