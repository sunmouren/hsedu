# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/7 16:55
@desc: 
"""

import json
import requests

from django.conf import settings

from courses.models import CourseClass

from qiniu import Auth
from qiniu.auth import QiniuMacAuth


def is_subscriber(user, course):
    if user.is_authenticated:
        return CourseClass.objects.filter(course=course, students=user).exists()
    return False


def upload_token():
    """
    生成七牛云上传token
    :return:
    """
    q = Auth(settings.ACCESS_KEY, settings.SECRET_KEY)
    token = q.upload_token(bucket=settings.BUCKET_NAME, key=None, expires=3600)
    return token


def get_qiniu_request_auth():
    """
    :return: 七牛云用户认证
    """
    return QiniuMacAuth(settings.ACCESS_KEY, settings.SECRET_KEY)


def duration_simple_format(url):
    """
    检查格式化 duration
    :param url: 视频 url info
    :return:
    """
    status = True
    duration = ''
    try:
        response = requests.get(url)
        if response.status_code is 200:
            duration = json.loads(response.text)['format']['duration']
            total_seconds = float(duration)
            h = int(total_seconds // 3600)
            m = int(total_seconds % 3600 // 60)
            s = int(total_seconds % 60)
            h = '0' + str(h) if h < 10 else str(h)
            m = '0' + str(m) if m < 10 else str(m)
            s = '0' + str(s) if s < 10 else str(s)
            duration = h + ':' + m + ':' + s
    except BaseException as e:
        print(e)
        status = False
    return status, duration
