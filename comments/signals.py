# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/11 17:21
@desc: 
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Comment


@receiver(m2m_changed, sender=Comment.like_user.through)
def class_grade_students_changed(sender, instance, **kwargs):
    """
    当评论喜欢数据发送变化时，更新其对应的人数
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.like_number = instance.like_user.count()
    instance.save()
