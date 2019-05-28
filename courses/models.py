from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation

from resources.models import Resources


class Course(models.Model):
    """
    课程表
    """
    title = models.CharField(max_length=64)
    overview = models.TextField(blank=True, null=True)
    img_url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user_courses')
    view_count = models.PositiveIntegerField(default=0)
    study_count = models.PositiveIntegerField(default=0)
    study_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='study_users', blank=True)
    resources = GenericRelation(Resources)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('courses:course-detail', args=[self.pk])

    def add_view_count(self):
        self.view_count += 1
        self.save()

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Video(models.Model):
    """
    课程视频表
    """
    title = models.CharField(max_length=64)
    overview = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name='course_videos')
    play_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name
        ordering = ('created',)

    def get_absolute_url(self):

        return reverse('courses:course-video', args=[self.pk])

    def __str__(self):
        return self.title


class CourseClass(models.Model):
    """
    班级表
    """
    title = models.CharField(max_length=32)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    students_count = models.PositiveIntegerField(default=0)
    code = models.CharField(max_length=32, blank=True, null=True, verbose_name='邀请码')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('courses:class-detail', args=[self.pk])

    def __str__(self):
        return self.title


class VideoWatchProgress(models.Model):
    """
    视频观看进度
    """
    progress = models.PositiveSmallIntegerField()
    duration = models.PositiveSmallIntegerField()
    achieve = models.BooleanField(default=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '视频观看进度'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if self.progress == self.duration:
            self.achieve = True
        super().save(*args, **kwargs)

    def __str__(self):
        return '{0}观看<<{1}>>进度为:{2}%'.format(self.user, self.video, int(self.progress / self.duration * 100))


class ClassWork(models.Model):
    """
    班级作业表
    """
    title = models.CharField(max_length=64)
    course_class = models.ForeignKey('CourseClass', on_delete=models.CASCADE)
    resources = GenericRelation(Resources)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_class


class WorkItem(models.Model):
    """
    学生作业表
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resources = GenericRelation(Resources)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user




