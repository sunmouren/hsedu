from django.conf import settings
from django.db import models
from django.urls import reverse


class Course(models.Model):
    """
    课程表
    """
    title = models.CharField(max_length=64)
    overview = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        self.increase_view_count()
        return reverse('courses:course-detail', args=[self.pk])

    def increase_view_count(self):
        self.view_count += 1
        self.save()

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    """
    章节表
    """
    chapter_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=64)
    overview = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name
        ordering = ('chapter_number',)

    def __str__(self):
        return self.title


class Video(models.Model):
    """
    章节视频表
    """
    title = models.CharField(max_length=64)
    overview = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=256)
    minute = models.PositiveIntegerField(default=1)
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    play_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name
        ordering = ('created',)

    def get_absolute_url(self):
        self.increase_play_count()
        return reverse('courses:course-video', args=[self.pk])

    def increase_play_count(self):
        self.play_count += 1
        self.save()

    def __str__(self):
        return self.title


class ClassGrade(models.Model):
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


class SignIn(models.Model):
    """
    签到表
    """
    code = models.CharField(max_length=32, verbose_name='验证码')
    is_active = models.BooleanField(default=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='yet_sign_in', blank=True)
    students_count = models.PositiveIntegerField(default=0)
    classgrade = models.ForeignKey('ClassGrade', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='create_sign_in')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '签到'
        verbose_name_plural = verbose_name
        ordering = ('-created', )

    def __str__(self):
        return '{0}的{1}签到'.format(self.classgrade, self.created)









