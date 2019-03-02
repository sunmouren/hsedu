from django.contrib import admin

from .models import Course, Chapter, Video, \
    ClassGrade, VideoWatchProgress, SignIn


# class ChapterInline(admin.StackedInline):
#     model = Chapter
#
#
# class ClassGradeInline(admin.StackedInline):
#     model = ClassGrade
#
#
# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     inlines = [ChapterInline, ClassGradeInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']


admin.site.register(Chapter)
admin.site.register(Video)
admin.site.register(ClassGrade)
admin.site.register(VideoWatchProgress)
admin.site.register(SignIn)




