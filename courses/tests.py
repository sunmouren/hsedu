from django.test import TestCase


import json

import requests


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



url = 'http://78re52.com1.z0.glb.clouddn.com/resource%2Fthinking-in-go.mp4?avinfo'

status, duration = duration_simple_format(url)

print(duration)

