# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/11 17:04
@desc: 
"""

from django import template
from django.utils.safestring import mark_safe

import markdown

from ..models import CommentNotification, Comment


register = template.Library()


@register.simple_tag
def check_is_liked(user, comment):
    """
    检查当前用户是否在喜欢书评列表中
    :param request:
    :param comment:
    :return:
    """
    return user in comment.like_user.all()


@register.filter(name='markdown')
def markdown_format(text, is_review=False):
    """
    Markdown 语法filter ,
    name='markdown'表明使用时可以直接使用markdown作为filter名。
    :param is_review:
    :param text:
    :return:
    """
    if is_review:
        text = '@' + text
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def get_unread_count(user):
    """
    获取评论未读通知数量
    :param user:
    :return:
    """
    return CommentNotification.unread.filter(receiver=user).count() if user.is_authenticated else None


@register.simple_tag
def get_hot_comment(count=5):
    return Comment.objects.order_by

