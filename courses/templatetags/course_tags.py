# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/9 11:04
@desc: 
"""

from django import template
from django.conf import settings

from utils.cmmon import get_qiniu_request_auth
from live.rtc_server_manager import RtcServer

from ..models import CourseClass, Video, VideoWatchProgress, Course


register = template.Library()


@register.simple_tag
def check_is_subscriber(course, user, class_id=None):
    """
    检查是否为已经加入班级
    :param course:
    :param user:
    :param class_id: 班级 id
    :return:
    """
    if user.is_authenticated:
        if class_id:
            return CourseClass.objects.filter(id=class_id, course=course, students=user).exists()
        return CourseClass.objects.filter(course=course, students=user).exists()
    return False


@register.simple_tag
def get_video_progress(video, user):
    if VideoWatchProgress.objects.filter(video=video, user=user).exists():
        vwg = VideoWatchProgress.objects.get(video=video, user=user)
        return int(vwg.progress / vwg.duration * 100)
    else:
        return 0


@register.simple_tag
def get_course_progress(course, user):
    """
    获取课程完成进度，主要是统计视频光看进度为100%的数量，再该课程总的视频数量去获取百分比。
    :param course:
    :param user:
    :return:
    """
    video_count = course.course_videos.count()
    achieve_count = VideoWatchProgress.objects.filter(course=course, user=user).count()
    return int(achieve_count / video_count * 100) if video_count != 0 else 0


@register.simple_tag
def check_is_owner(course, user):
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


@register.simple_tag
def get_course_banner_list(count=3):
    course_list = Course.objects.order_by('-view_count')[:count]
    banner_list = []
    for course in course_list:
        img_url = course.img_url.split('?')[0] + '?imageView2/1/w/755/h/280/q/100'
        absolute_url = course.get_absolute_url()
        banner = {'img_url': img_url, 'absolute_url': absolute_url}
        banner_list.append(banner)
    return banner_list


@register.simple_tag
def check_is_live_room_active(course):
    """
    检测课程直播激活
    :param course:
    :return: True or False
    """
    room = 'room' + str(course.user.id) + str(course.id)
    q = get_qiniu_request_auth()
    rtc = RtcServer(q)
    response = rtc.list_active_rooms(app_id=settings.QINIU_RTN_APPID, room_name_prefix=room)[0]
    return True if response['rooms'] else False
