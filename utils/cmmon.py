# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/7 16:55
@desc: 
"""

from courses.models import ClassGrade


def is_subscriber(user, course):
    if user.is_authenticated:
        return ClassGrade.objects.filter(course=course, students=user).exists()
    return False


