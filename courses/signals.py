# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/10 13:34
@desc: 
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import CourseClass, Course


@receiver(m2m_changed, sender=CourseClass.students.through)
def course_class_students_changed(sender, instance, **kwargs):
    """
    当课程班级加入人数发送变化时，更新其对应的人数
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.students_count = instance.students.count()
    instance.save()


@receiver(m2m_changed, sender=Course.study_users.through)
def course_study_users_changed(sender, instance, **kwargs):
    """
    当课程学习加入人数发送变化时，更新其对应的人数
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.study_count = instance.study_users.count()
    instance.save()
