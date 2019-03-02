# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/2/19 12:27
@desc: 
"""

from rest_framework import serializers

from ..models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar_url']
