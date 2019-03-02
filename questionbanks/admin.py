from django.contrib import admin

from .models import SingleChoice, SingleChoiceAnswer, TestPaper


@admin.register(SingleChoice)
class SingleChoiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'chapter_number', ]


@admin.register(SingleChoiceAnswer)
class SingleChoiceAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'single_choice', 'answer']


@admin.register(TestPaper)
class TestPaperAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
