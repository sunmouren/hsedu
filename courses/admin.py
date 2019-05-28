from django.contrib import admin

from .models import Course, Video, \
    CourseClass, VideoWatchProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']


admin.site.register(Video)
admin.site.register(CourseClass)
admin.site.register(VideoWatchProgress)




