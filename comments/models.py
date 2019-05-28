from django.conf import settings
from django.db import models

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from courses.models import Video


class Comment(MPTTModel):
    """
    问答评论
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True, null=True, verbose_name='视频')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                            related_name='replies', verbose_name='父级评论')
    content = models.TextField(verbose_name='评论内容', default=None)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments',
                                       blank=True)
    like_number = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='评论时间')

    class MPTTMeta:
        order_insertion_by = ('created', )

    class Meta:
        verbose_name = '问答'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.parent is not None:
            return '{0} 回复 {1}'.format(self.user.username, self.parent.user.username)
        else:
            return '{0} 评论了 {1}'.format(self.user.username, self.video)


class UnreadManger(models.Manager):
    """
    评论通知未读manger
    """
    def get_queryset(self):
        return super(UnreadManger, self).get_queryset().filter(is_read=False)


class CommentNotification(models.Model):
    """
    简单实现评论通知，如果需要第三方的通知模块，不想要重复造轮子，可以去看看你django-notifications
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_reader_set',
                               on_delete=models.CASCADE, verbose_name='发送者')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_receiver_set',
                                 on_delete=models.CASCADE, verbose_name='接收者')
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    # The default manger
    objects = models.Manager()
    # Our custom manger
    unread = UnreadManger()

    class Meta:
        verbose_name = '评论通知'
        verbose_name_plural = verbose_name
        ordering = ('-created', )
