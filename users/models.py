from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings


class UserProfile(AbstractUser):
    """
    用户表
    """
    role_choices = (('teacher', '老师'), ('student', '学生'))
    nickname = models.CharField(max_length=30, blank=True,
                                null=True, verbose_name='昵称')
    signature = models.CharField(max_length=128, blank=True,
                                 null=True, verbose_name='个性签名', default='这家伙很懒，什么都没有留下！')
    role = models.CharField(max_length=15, choices=role_choices, default='student')
    avatar_url = models.CharField(max_length=200,
                                  default=settings.DOMAIN + 'image/avatar/default.jpg')
    stu_num = models.CharField(max_length=20, blank=True, null=True)
    stu_name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('users:user-home', args=[self.id])

    def get_num_name(self):
        if self.stu_num:
            return self.stu_num
        elif self.stu_name:
            return self.stu_name
        return self.username

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username
