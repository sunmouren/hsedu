from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.postgres.search import SearchVector

from utils.cmmon import upload_token, duration_simple_format
from resources.models import Resources
from comments.models import Comment

from .models import Course, Video, VideoWatchProgress, CourseClass
from .templatetags.course_tags import check_is_subscriber, check_is_owner
from .forms import SearchForm


class CourseDetail(View):
    """
    课程详情
    """

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=int(course_id))
        course.add_view_count()
        template_name = self.get_template_name(request, course)
        class_list = course.courseclass_set.all()
        video_list = course.course_videos.all()
        comment_list = self.get_course_video_comment_list(course)
        resource_list = course.resources.all()

        return render(request, template_name, {
            'course': course,
            'class_list': class_list,
            'video_list': video_list,
            'comment_list': comment_list,
            'resource_list': resource_list,
        })

    @staticmethod
    def get_template_name(request, course):

        if check_is_owner(course, request.user):
            return 'course/course-detail-teacher.html'

        if check_is_subscriber(course, request.user):
            return 'course/course-detail-student.html'

        return 'course/course-detail.html'

    @staticmethod
    def get_course_video_comment_list(course):
        video_ids = course.course_videos.values_list('id', flat=True)
        comment_list = Comment.objects.filter(video_id__in=video_ids).exclude(parent=None)
        return comment_list


class VideoDetail(DetailView):
    """
    视频详情
    """
    model = Video
    template_name = 'course/video-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.course
        context['comment_list'] = self.object.comment_set.order_by('-created')
        context['progress'], context['vwp'] = self.get_video_watch_progress()
        self.object.play_count += 1
        self.object.save()
        return context

    def get_video_watch_progress(self):
        """
        获取当前请求用户的视频观看进度
        :return:
        """
        if check_is_subscriber(course=self.object.course, user=self.request.user):
            vwp = self.object.videowatchprogress_set.filter(video=self.object, user=self.request.user)
            if vwp.exists():
                if vwp[0].achieve:
                    return vwp[0].progress, 100
                else:
                    return vwp[0].progress, int(vwp[0].progress / vwp[0].duration * 100)
            else:
                return 0, 0
        else:
            return None, None


class CourseList(ListView):
    """
    课程列表
    """
    model = Course
    template_name = 'course/course-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'course-list'
        return context


class AddVideoWatchProgress(LoginRequiredMixin, View):
    """
    添加学习记录
    """
    def post(self, request):
        if request.is_ajax():
            duration = request.POST.get('duration', None)
            progress = request.POST.get('progress', None)
            cid = request.POST.get('cid', None)
            vid = request.POST.get('vid', None)
            if cid and vid:
                try:
                    course = Course.objects.get(id=int(cid))
                    video = Video.objects.get(id=int(vid))
                    obj, created = VideoWatchProgress.objects.update_or_create(
                        course=course, video=video, user=request.user,
                        defaults={'progress': progress, 'duration': duration})
                    if duration == progress:
                        return JsonResponse({'msg': 'ok'})
                except (Course.DoesNotExist, Video.DoesNotExist) as e:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class SubscribeCourse(LoginRequiredMixin, View):
    """
    加入班级
    """
    def post(self, request):
        if request.is_ajax():
            class_id = request.POST.get('cgid', None)
            print(class_id)
            code = request.POST.get('code', None)
            if class_id and code:
                try:
                    class_grade = CourseClass.objects.get(id=int(class_id))
                    if code == str(class_grade.code):
                        class_grade.students.add(request.user)
                        return JsonResponse({'msg': 'ok'})
                except CourseClass.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class ClassDetail(View):
    """
    班级详情
    """

    def get(self, request, class_id):
        course_class = get_object_or_404(CourseClass, id=int(class_id))
        # template_name = self.get_template_name(request, course_class.course, class_id)
        student_list = course_class.students.all
        context = {
            'course': course_class.course,
            'course_user': course_class.course.user,
            'course_class': course_class,
            'student_list': student_list,
        }
        return render(request, 'course/class-detail.html', context=context)

    # @staticmethod
    # def get_template_name(request, course, class_id):
    #     is_subscriber = check_is_subscriber(course, request.user, class_id)
    #     return 'course/class-detail-student.html' if is_subscriber else 'course/class-detail-teacher.html'


class AddCourse(LoginRequiredMixin, View):
    """
    添加课程
    """
    def get(self, request):
        token = upload_token()
        context = {
            'token': token,
            'username': request.user.username
        }
        return render(request, 'course/add-course.html', context=context)

    def post(self, request):
        if request.is_ajax():
            title = request.POST.get('title', None)
            overview = request.POST.get('overview', None)
            img_url = request.POST.get('imgUrl', None)
            is_pass = title and overview and img_url
            if is_pass:
                try:
                    new_course = Course(title=title, overview=overview)
                    new_course.img_url = settings.DOMAIN + img_url + '?imageView2/1/w/156/h/100/q/75'
                    new_course.user = request.user
                    new_course.save()
                    return JsonResponse({'msg': 'ok', 'id': new_course.id})
                except BaseException as e:
                    print(e)
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class AddVideo(LoginRequiredMixin, View):
    """
    添加视频
    """
    def get(self, request, course_id):
        token = upload_token()
        course = get_object_or_404(Course, id=int(course_id))
        context = {
            'token': token,
            'username': request.user.username,
            'course': course,
        }
        return render(request, 'course/add-video.html', context=context)

    def post(self, request):
        if request.is_ajax():
            title = request.POST.get('title', None)
            overview = request.POST.get('overview', None)
            video_url = request.POST.get('videoUrl', None)
            course_id = request.POST.get('courseId', None)
            is_pass = title and overview and video_url
            if is_pass:
                status, duration = duration_simple_format(settings.DOMAIN + video_url + '?avinfo')
                try:
                    course = Course.objects.get(id=int(course_id))
                    new_video = Video(title=title, overview=overview)
                    new_video.url = settings.DOMAIN + video_url
                    new_video.course = course
                    new_video.duration = duration if status else 'error'
                    new_video.save()
                    return JsonResponse({'msg': 'ok', 'id': course.id})
                except BaseException as e:
                    print(e)
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class AddClass(LoginRequiredMixin, View):
    """
    添加班级
    """
    def get(self, request, cid):
        course = get_object_or_404(Course, id=int(cid))
        return render(request, 'course/add-course-class.html', {'course': course})

    def post(self, request):
        if request.is_ajax():
            cid = request.POST.get('cid', None)
            title = request.POST.get('title', None)
            code = request.POST.get('code', None)
            is_pass = cid and title and code
            if is_pass:
                try:
                    course = Course.objects.get(id=int(cid))
                    new_class_grade = CourseClass(title=title, code=code, course=course)
                    new_class_grade.save()
                    return JsonResponse({'msg': 'ok'})
                except (Course.DoesNotExist, BaseException) as e:
                    print(e)
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class AddCourseResource(LoginRequiredMixin, View):
    """
    添加课程课件资源
    """
    def get(self, request, cid):
        token = upload_token()
        course = get_object_or_404(Course, id=int(cid))
        context = {
            'token': token,
            'username': request.user.username,
            'course': course,
        }
        return render(request, 'course/add-course-resource.html', context=context)

    def post(self, request):
        if request.is_ajax():
            title = request.POST.get('title', None)
            cid = request.POST.get('courseId', None)
            resource_url = request.POST.get('resourceUrl')
            is_pass = title and cid and resource_url
            if is_pass:
                try:
                    course = Course.objects.get(id=int(cid))
                    resource_url = settings.DOMAIN + resource_url
                    Resources(content_object=course, title=title, url=resource_url).save()
                    return JsonResponse({'msg': 'ok', 'id': course.id})
                except (Course.DoesNotExist, BaseException) as e:
                    print(e)
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


def course_search(request):
    """
    搜索课程
    :param request:
    :return:
    """
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Course.objects.annotate(
                search=SearchVector('title', 'overview'),
            ).filter(search=query)
    return render(request, 'search.html', {
        'query': query,
        'results': results,
    })


