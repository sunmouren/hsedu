from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404

from courses.models import Course
from courses.templatetags.course_tags import check_is_subscriber

from .models import SingleChoice, TestPaper, SingleChoiceAnswer


class ChapterTestList(View):
    """
    章节习题
    """
    def get(self, request, course_id, chapter_number):
        course = get_object_or_404(Course, id=int(course_id))
        single_choices = SingleChoice.objects.filter(course=course, chapter_number=chapter_number)

        is_subscriber = check_is_subscriber(course=course, user=request.user)
        is_had_test_paper = self.check_is_had_test_paper(course, chapter_number)

        if not is_had_test_paper and is_subscriber:
            self.generate_test_paper(course, chapter_number)

        if is_had_test_paper and is_subscriber:
            ids = self.get_had_sc_submitted_ids(course=course, chapter_number=chapter_number)
            single_choices = single_choices.exclude(id__in=ids)

        return render(request, 'test/bs-chapter-test-list.html', {
            'course': course,
            'single_choices': single_choices,
            'chapter_number': chapter_number,
            'is_subscriber': is_subscriber,
        })

    def check_is_had_test_paper(self, course, chapter_number):
        """
        检查当前用户是否已经生成章节测试试卷
        :param course:
        :param chapter_number:
        :return:
        """
        if self.request.user.is_authenticated:
            return TestPaper.objects.filter(user=self.request.user, course=course,
                                            chapter_number=chapter_number).exists()
        else:
            return False

    def generate_test_paper(self, course, chapter_number):
        """
        生成试卷
        :param course:
        :param chapter_number:
        :return:
        """
        new_test_paper = TestPaper(user=self.request.user, course=course, chapter_number=chapter_number)
        new_test_paper.save()

    def get_had_sc_submitted_ids(self, course, chapter_number):
        """
        获取已经提交的 单选题 ids
        :param course:
        :param chapter_number:
        :return:
        """
        test_pager = get_object_or_404(TestPaper, user=self.request.user, course=course, chapter_number=chapter_number)
        return test_pager.single_choices.values_list('single_choice_id', flat=True)


class SubmitSingleChoice(LoginRequiredMixin, View):
    """
    提交作答的单选题
    """
    def post(self, request):
        if request.is_ajax():
            scid = request.POST.get('scid', None)
            answer = request.POST.get('answer', None)
            if scid and answer:
                try:
                    single_choice = SingleChoice.objects.get(id=int(scid))
                    course = single_choice.course
                    chapter_number = single_choice.chapter_number
                    single_choice_answer = SingleChoiceAnswer(user=request.user,
                                                              single_choice=single_choice, answer=answer)
                    test_paper = TestPaper.objects.get(user=request.user, course=course,
                                                       chapter_number=chapter_number)
                    single_choice_answer.save()
                    test_paper.single_choices.add(single_choice_answer)
                    test_paper.save()
                    return JsonResponse({'msg': 'ok'})
                except (SingleChoice.DoesNotExist, TestPaper.DoesNotExist, BaseException) as e:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class ChapterTestListSubmit(LoginRequiredMixin, View):
    """
    已提交的章节的测试列表
    """
    def get(self, request, course_id, chapter_number):
        course = get_object_or_404(Course, id=int(course_id))

        is_subscriber = check_is_subscriber(course=course, user=request.user)

        if not is_subscriber:
            return JsonResponse({'msg': 'unsubscriber'})

        if is_subscriber:
            test_pager = get_object_or_404(TestPaper, user=request.user,
                                           course=course, chapter_number=chapter_number)
            single_choice_answer = test_pager.single_choices.all()
            return render(request, 'test/bs-chapter-test-list-submitted.html', {
                'single_choice_answers': single_choice_answer,
                'course': course,
                'chapter_number': chapter_number,
            })


class AddNote(LoginRequiredMixin, View):
    """
    添加笔记
    """
    def post(self, request):
        msg = 'ko'
        if request.is_ajax():
            item_id = request.POST.get('id', None)
            item_type = request.POST.get('type', None)
            content = request.POST.get('content', None)
            if item_id and item_type and content:
                if item_type == 'sc':
                    msg = self.add_single_choice_note(item_id=item_id, content=content)
                return JsonResponse({'msg': msg})
        return JsonResponse({'msg': msg})

    @staticmethod
    def add_single_choice_note(item_id, content):
        try:
            single_choice_answer = SingleChoiceAnswer.objects.get(id=int(item_id))
            single_choice_answer.note = content
            single_choice_answer.save()
            return 'ok'
        except SingleChoiceAnswer.DoesNotExist:
            return 'ko'


class CreateExercises(LoginRequiredMixin, View):
    """
    获取创作习题页面
    """
    def get(self, request, course_id, chapter_number):
        course = get_object_or_404(Course, id=int(course_id))
        is_subscriber = check_is_subscriber(course=course, user=request.user)

        if not is_subscriber:
            return JsonResponse({'msg': 'unsubscriber'})

        if is_subscriber or request.user == course.user:
            return render(request, 'test/bs-chapter-test-create-exercises.html', {
                'course': course,
                'chapter_number': chapter_number,
            })


class SendExercises(LoginRequiredMixin, View):
    """
    发布习题, 说真的，这里写的代码一点都不优雅
    """
    def post(self, request):
        msg = 'ko'
        if request.is_ajax():
            item_type = request.POST.get('type', None)
            if item_type and item_type == 'sc':
                msg = self.create_sc_exercises()
            return JsonResponse({'msg': msg})
        return JsonResponse({'msg': msg})

    def create_sc_exercises(self):
        """
        创建单选题
        :return:
        """
        cid = self.request.POST.get('cid', None)
        chnum = self.request.POST.get('chnum', None)
        sc_title = self.request.POST.get('scTitle', None)
        sc_a = self.request.POST.get('scA', None)
        sc_b = self.request.POST.get('scB', None)
        sc_c = self.request.POST.get('scC', None)
        sc_d = self.request.POST.get('scD', None)
        sc_answer = self.request.POST.get('scAnswer', None)
        sc_img = self.request.POST.get('url', None)
        is_empty = cid and chnum and sc_title and sc_a and sc_b and sc_c and sc_d and sc_answer
        if is_empty:
            try:
                course = Course.objects.get(id=int(cid))
                new_sc = SingleChoice(course=course, title=sc_title, option_a=sc_a,
                                      option_b=sc_b, option_c=sc_c, option_d=sc_d,
                                      answer=sc_answer, chapter_number=chnum, user=self.request.user)
                if sc_img:
                    new_sc.img = settings.DOMAIN + sc_img
                new_sc.save()
                return 'ok'
            except (Course.DoesNotExist, BaseException) as e:
                return 'ko'
        return 'ko'


class MyCreated(LoginRequiredMixin, View):
    """
    我的创作习题
    """
    def get(self, request, course_id, chapter_number):
        course = get_object_or_404(Course, id=int(course_id))

        if not check_is_subscriber(course=course, user=request.user):
            return JsonResponse({'msg': 'unsubscriber'})

        single_choices = SingleChoice.objects.filter(course=course,
                                                     chapter_number=chapter_number,
                                                     user=request.user)
        return render(request, 'test/bs-chapter-test-my-created.html', {
            'single_choices': single_choices,
            'course': course,
            'chapter_number': chapter_number,
        })



