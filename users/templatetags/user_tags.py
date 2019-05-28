# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/3/2 16:07
@desc: 
"""

from django import template

from ..models import UserProfile


register = template.Library()


@register.simple_tag
def get_user_count():
    """
    获取用户数量
    :return:
    """
    return UserProfile.objects.count()


@register.simple_tag
def get_recent_users(count=5):
    """
    获取最近加入的用户
    :param count: 返回数量 默认8
    :return:
    """
    return UserProfile.objects.order_by('-date_joined')[:count]
