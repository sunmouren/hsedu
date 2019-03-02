from django.db import models
from django.conf import settings

from courses.models import Course, Chapter


class SingleChoice(models.Model):
    """
    单选题
    """
    title = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    answer = models.CharField(max_length=2)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter_number = models.CharField(max_length=4, null=True, blank=True)
    img = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = '单选题'
        verbose_name_plural = verbose_name
        ordering = ('chapter_number', )

    def __str__(self):
        return '{0} {1}'.format(self.course, self.title)


class SingleChoiceAnswer(models.Model):
    """
    单选择题答题卡
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    single_choice = models.ForeignKey('SingleChoice', on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    answer = models.CharField(max_length=2)

    class Meta:
        verbose_name = '单选题答题卡'
        verbose_name_plural = verbose_name
        ordering = ('user', )

    def __str__(self):
        return '{0} {1}'.format(self.user, self.single_choice)


class TestPaper(models.Model):
    """
    测试试卷
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter_number = models.CharField(max_length=4, null=True, blank=True)
    single_choices = models.ManyToManyField('SingleChoiceAnswer', blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '测试试卷'
        verbose_name_plural = verbose_name
        ordering = ('-created', )

    def __str__(self):
        if self.chapter_number:
            return '{0} {1} {2}章节测试'.format(self.user, self.course, self.chapter_number)
        else:
            return '{0} {1} 测试'.format(self.user, self.course)
