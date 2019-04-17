from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # index
    path('', TemplateView.as_view(template_name='index.html', extra_context={'current_page': 'index'}), name='index'),
    # course
    path('course/', include('courses.urls', namespace='courses')),
    # user
    path('user/', include('users.urls', namespace='users')),
    # comment
    path('comment/', include('comments.urls', namespace='comments')),
    path('test/', include('questionbanks.urls', namespace='questionbanks')),
    # course api
    path('api/', include('courses.api.urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
