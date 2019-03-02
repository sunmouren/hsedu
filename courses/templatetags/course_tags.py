# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/9 11:04
@desc: 
"""

from django import template

from ..models import ClassGrade, SignIn, Video, VideoWatchProgress, Course



register = template.Library()


@register.simple_tag
def check_is_subscriber(course, user, class_id=None):
    """
    检查是否为课程订阅者
    :param course:
    :param user:
    :param class_id: 班级 id
    :return:
    """
    if user.is_authenticated:
        if class_id:
            return ClassGrade.objects.filter(id=class_id, course=course, students=user).exists()
        return ClassGrade.objects.filter(course=course, students=user).exists()
    return False


@register.simple_tag
def check_is_sign(user, sign_id):
    if user.is_authenticated:
        return SignIn.objects.filter(id=sign_id, students=user).exists()
    return False


@register.simple_tag
def analyze_sign(sign, classgrade):
    """
    分析签到情况
    :param sign:
    :param stduent:
    :return:
    """
    sign_ins = sign.students.values_list('id', flat=True)
    return classgrade.students.exclude(id__in=sign_ins)


@register.simple_tag
def get_course_progress(course, user):
    """
    获取课程完成进度，主要是统计视频光看进度为100%的数量，再该课程总的视频数量去获取百分比。
    内心独白：
        由于数据库课程结构是这样的（不想在重构了）：
        course
            - chapter
                - video
        所以如果想要获取这门课程吃的(不是吃的，是视频）的数量，
        可以先获取chapter的全部ids, 然后在根据ids去查找。
    :param course:
    :param user:
    :return:
    """
    chapter_ids = course.chapter_set.values_list('id', flat=True)
    video_count = Video.objects.filter(chapter_id__in=chapter_ids).count()
    achieve_count = VideoWatchProgress.objects.filter(course=course, user=user).count()
    return int(achieve_count / video_count * 100) if video_count != 0 else 0


@register.simple_tag
def get_video_progress(video, user):
    if VideoWatchProgress.objects.filter(video=video, user=user).exists():
        vwg = VideoWatchProgress.objects.get(video=video, user=user)
        return int(vwg.progress / vwg.duration * 100)
    else:
        return 0


@register.simple_tag
def is_owner(course, user):
    """
    判断是否为课程所属者
    :param course:
    :param user:
    :return:
    """
    return course.user == user


@register.simple_tag
def get_hot_course(count=5):
    return Course.objects.order_by('-view_count')[:count]


@register.simple_tag
def get_hot_video(count=5):
    return Video.objects.order_by('-play_count')[:count]




