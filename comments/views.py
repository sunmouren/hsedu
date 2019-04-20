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
                # 创建评论通知, 这里也可以通过信号来创建，但为了防止以后出现问题不清楚，直接在这里创建
                if parent:
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
    :param book:
    :param comment:
    :return:
    """
    cmt_html = render_to_string('course/bs-comment-item.html',
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
        unread_list = CommentNotification.unread.filter(receiver=request.user)
        ntf_list = CommentNotification.objects.filter(receiver=request.user).filter(is_read=True)
        return render(request, 'bs-notifications.html', context={
            'unread_list': unread_list,
            'ntf_list': ntf_list,
            'current_page': current_page
        })

    def post(self, request):
        if request.is_ajax():
            nid = request.POST.get('nid', None)
            if nid:
                try:
                    ntf = CommentNotification.objects.get(id=int(nid))
                    ntf.is_read = True
                    ntf.save()
                    return JsonResponse({'msg': 'ok'})
                except CommentNotification.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})
