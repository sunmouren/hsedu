# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/10 13:34
@desc: 
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import ClassGrade, SignIn


@receiver(m2m_changed, sender=ClassGrade.students.through)
def class_grade_students_changed(sender, instance, **kwargs):
    """
    当课程订阅数据发送变化时，更新其对应的人数
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.students_count = instance.students.count()
    instance.save()


@receiver(m2m_changed, sender=SignIn.students.through)
def sign_students_changed(sender, instance, **kwargs):
    """
    当签到订阅数据发送变化时，更新其对应的人数
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.students_count = instance.students.count()
    instance.save()
