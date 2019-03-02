from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.postgres.search import SearchVector

from qiniu import Auth

from .models import Course, Video, VideoWatchProgress, ClassGrade, SignIn, Chapter
from .templatetags.course_tags import check_is_subscriber
from .forms import SearchForm


class CourseDetail(DetailView):
    """
    课程详情
    """

    model = Course
    template_name = 'course/bs-course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapter_list'] = self.object.chapter_set.all()
        context['class_grade_list'] = self.object.classgrade_set.all()
        return context


class CourseVideoDetail(DetailView):
    """
    视频详情
    """
    model = Video
    template_name = 'course/bs-course-video-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.chapter.course
        context['chapter'] = self.object.chapter
        context['comments'] = self.object.comment_set.order_by('-created')
        context['progress'], context['vwp'] = self.get_video_watch_progress()
        return context

    def get_video_watch_progress(self):
        """
        获取当前请求用户的视频观看进度
        :return:
        """
        if check_is_subscriber(course=self.object.chapter.course, user=self.request.user):
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
    template_name = 'course/bs-course-list.html'

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
    订阅课程
    """
    def post(self, request):
        if request.is_ajax():
            class_id = request.POST.get('cgid', None)
            print(class_id)
            code = request.POST.get('code', None)
            if class_id and code:
                try:
                    class_grade = ClassGrade.objects.get(id=int(class_id))
                    if code == str(class_grade.code):
                        class_grade.students.add(request.user)
                        return JsonResponse({'msg': 'ok'})
                except ClassGrade.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class ClassGradeDetail(View):
    """
    班级详情
    """

    def get(self, request, pk):
        classgrade = get_object_or_404(ClassGrade, id=int(pk))
        is_subscriber = check_is_subscriber(course=classgrade.course, user=request.user, class_id=classgrade.id)
        students = classgrade.students.all
        sign_ins = classgrade.signin_set.all
        context = {'classgrade': classgrade,
                   'students': students,
                   'sign_ins': sign_ins,
                   'is_subscriber': is_subscriber}
        if request.user == classgrade.course.user:
            return render(request, 'course/bs-class-grade-detail-teacher.html', context=context)
        return render(request, 'course/bs-class-grade-detail-student.html', context=context)


class AddSignIn(LoginRequiredMixin, View):
    """
    添加签到
    """
    def post(self, request):
        if request.is_ajax():
            cgid = request.POST.get('cgid')
            code = request.POST.get('code')
            if cgid and code:
                try:
                    classgrade = ClassGrade.objects.get(id=int(cgid))
                    new_sign_in = SignIn(code=code, classgrade=classgrade, user=request.user)
                    new_sign_in.save()
                    return JsonResponse({'msg': 'ok'})
                except ClassGrade.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class SubSignIn(LoginRequiredMixin, View):
    """
    订阅者进行签到
    """
    def post(self, request):
        if request.is_ajax():
            sid = request.POST.get('sid')
            code = request.POST.get('code')
            if sid and code:
                try:
                    sign_in = SignIn.objects.get(id=int(sid))
                    if code == str(sign_in.code):
                        sign_in.students.add(request.user)
                        return JsonResponse({'msg': 'ok'})
                except SignIn.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class CosSign(LoginRequiredMixin, View):
    """
    Cos: changes of state
    改变签到状态
    """
    def post(self, request):
        if request.is_ajax():
            sid = request.POST.get('sid')
            action = request.POST.get('action')
            if sid and action:
                try:
                    sign_in = SignIn.objects.get(id=int(sid))
                    if action == 'activate':
                        sign_in.is_active = True
                    else:
                        sign_in.is_active = False
                    sign_in.save()
                    return JsonResponse({'msg': 'ok'})
                except SignIn.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class UploadVideo(LoginRequiredMixin, View):
    """
    上传视频
    """
    def get(self, request, cid, chapter_id):
        course = get_object_or_404(Course, id=int(cid))
        chapter = get_object_or_404(Chapter, id=int(chapter_id))
        context = {
            'course': course,
            'chapter': chapter,
        }
        return render(request, 'course/bs-add-video.html', context=context)

    def post(self, request):
        if request.is_ajax():
            video_title = request.POST.get('title', None)
            chapter_id = request.POST.get('chid', None)
            video_url = request.POST.get('url', None)
            if video_title and chapter_id and video_url:
                try:
                    chapter = Chapter.objects.get(id=int(chapter_id))
                    video = Video(title=video_title, chapter=chapter)
                    video.url = settings.DOMAIN + video_url
                    video.save()
                    return JsonResponse({'msg': 'ok'})
                except Chapter.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class UploadToken(LoginRequiredMixin, View):
    """
    生成七牛云上传 token
    """
    def get(self, request):
        try:
            q = Auth(settings.ACCESS_KEY, settings.SECRET_KEY)
            token = q.upload_token(bucket=settings.BUCKET_NAME, key=None, expires=3600)
            domain = settings.DOMAIN
            return JsonResponse({'msg': 'ok', 'token': token, 'domain': domain,
                                 'username': request.user.username})
        except:
            return JsonResponse({'msg': 'ko', 'token': token, 'domain': domain,
                                 'username': request.user.username})


class AddChapter(LoginRequiredMixin, View):
    """
    添加章节
    """
    def get(self, request, cid):
        course = get_object_or_404(Course, id=int(cid))
        return render(request, 'course/bs-add-chapter.html', {
            'course': course
        })

    def post(self, request):
        if request.is_ajax():
            cid = request.POST.get('cid', None)
            chapter_num = request.POST.get('cnum', None)
            chapter_title = request.POST.get('title', None)
            chapter_overview = request.POST.get('overview', None)
            is_pass = cid and chapter_num and chapter_title and chapter_overview
            if is_pass:
                try:
                    course = Course.objects.get(id=int(cid))
                    if Chapter.objects.filter(course=course, chapter_number=chapter_num).exists():
                        return JsonResponse({'msg': 'repeat'})

                    new_chapter = Chapter(chapter_number=chapter_num,
                                          title=chapter_title,
                                          overview=chapter_overview,
                                          course=course)
                    new_chapter.save()
                    return JsonResponse({'msg': 'ok'})
                except (Course.DoesNotExist, BaseException) as e:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class AddCourse(LoginRequiredMixin, View):
    """
    添加课程
    """
    def get(self, request):
        return render(request, 'course/bs-add-course.html')

    def post(self, request):
        if request.is_ajax():
            title = request.POST.get('title', None)
            overview = request.POST.get('overview', None)
            is_pass = title and overview
            if is_pass:
                try:
                    new_course = Course(title=title, overview=overview)
                    new_course.user = request.user
                    new_course.save()
                    return JsonResponse({'msg': 'ok', 'id': new_course.id})
                except BaseException:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class AddClassGrade(LoginRequiredMixin, View):
    """
    添加班级
    """
    def get(self, request, cid):
        course = get_object_or_404(Course, id=int(cid))
        return render(request, 'course/bs-add-classgrade.html', {'course': course})

    def post(self, request):
        if request.is_ajax():
            cid = request.POST.get('cid', None)
            title = request.POST.get('title', None)
            code = request.POST.get('code', None)
            is_pass = cid and title and code
            if is_pass:
                try:
                    course = Course.objects.get(id=int(cid))
                    new_class_grade = ClassGrade(title=title, code=code, course=course)
                    new_class_grade.save()
                    return JsonResponse({'msg': 'ok'})
                except (Course.DoesNotExist, BaseException) as e:
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
    return render(request, 'bs-search.html', {
        'query': query,
        'results': results,
    })

