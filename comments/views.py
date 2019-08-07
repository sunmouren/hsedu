from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from courses.models import Video

from .models import Comment, CommentNotification


class AddComment(LoginRequiredMixin, View):
    """
    添加问答
    """
    def post(self, request):
        pid = request.POST.get('pid', None)
        vid = request.POST.get('vid', None)
        content = request.POST.get('content', None)

        if request.is_ajax() and pid and vid and content:
            try:
                video = Video.objects.get(id=int(vid))
                parent = (Comment.objects.get(id=int(pid)) if int(pid) > 0 else None)
                new_comment = Comment(user=request.user, video=video, parent=parent, content=content)
                new_comment.save()
                cmt_html = render_comment_html(request=request, comment=new_comment)
                if parent and parent.user != request.user:
                    CommentNotification(sender=request.user,
                                        receiver=parent.user,
                                        comment=new_comment).save()
                return JsonResponse({'msg': 'ok', 'cmt': cmt_html})
            except (Video.DoesNotExist, Comment.DoesNotExist, BaseException) as e:
                print(e)
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


def render_comment_html(request, comment):
    """
    render comment to string html
    :param request:
    :param comment:
    :return:
    """
    cmt_html = render_to_string('comment/item.html',
                                context={'comment': comment},
                                request=request)
    return cmt_html


class AddLike(LoginRequiredMixin, View):
    """
    添加点赞喜欢
    """
    def post(self, request):
        comment_id = request.POST.get('cid', None)
        action = request.POST.get('action', None)
        if request.is_ajax() and comment_id and action:
            try:
                comment = Comment.objects.get(id=comment_id)
                if action == 'like':
                    comment.like_user.add(request.user)
                else:
                    comment.like_user.remove(request.user)
                return JsonResponse({'msg': 'ok'})
            except Comment.DoesNotExist:
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class CommentNotificationList(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'notice'
        # 将未读消息更新为已读
        CommentNotification.objects.\
            select_for_update().\
            filter(receiver=request.user, is_read=False).\
            update(is_read=True)

        notification_list = CommentNotification.objects.filter(receiver=request.user)

        return render(request, 'comment/notifications-detail.html', {
            'notification_list': notification_list,
            'current_page': current_page
        })

