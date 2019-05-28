import time

from django.shortcuts import render, get_object_or_404, Http404
from django.views.generic import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from courses.models import Course

from . import rtc_server_manager as rtc_server


class RoomDetail(LoginRequiredMixin, View):
    """
    加入房间,
    """
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=int(course_id))
        room_name = 'room' + str(course.user.id) + str(course.id)
        user_name = request.user.username
        room_token = self.get_room_token(room_name, user_name)
        context = {
            'room_token': room_token,
            'course': course,
        }
        if request.user == course.user:
            return render(request, 'live/room-detail-teacher.html', context=context)
        else:
            return render(request, 'live/room-detail-student.html', context=context)

    @staticmethod
    def get_room_token(room_name, user_name):
        """
        返回用户要加入的房间的token
        :param room_name: 房间名
        :param user_name: 用户名
        :return:
        """
        roomAccess = {
            "appId": settings.QINIU_RTN_APPID,  # AppID: 房间所属帐号的 app 。
            "roomName": room_name,  # RoomName: 房间名称，需满足规格 ^[a-zA-Z0-9_-]{3,64}$
            "userId": user_name,  # UserID: 请求加入房间的用户 ID，需满足规格 ^[a-zA-Z0-9_-]{3,50}$
            # ExpireAt: int64 类型，鉴权的有效时间，传入以秒为单位的64位Unix绝对时间，
            "expireAt": int(time.time()) + 3600,
            # token 将在该时间后失效。
            "permission": "user"  # 该用户的房间管理权限，"admin" 或 "user"，默认为 "user" 。当权限角色为 "admin" 时，
            # 拥有将其他用户移除出房间等特权.
        }
        try:
            room_token = rtc_server.get_room_token(settings.ACCESS_KEY, settings.SECRET_KEY, roomAccess)
        except BaseException as e:
            print(e)
            raise Http404
        return room_token
