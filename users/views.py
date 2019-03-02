from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password

from django.db.models import Q
from django.http import JsonResponse, Http404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from courses.models import Course

from .models import UserProfile


class UserRegister(View):
    """
    注册
    """
    def post(self, request):
        if request.is_ajax():
            email = request.POST.get('email', None)
            password1 = request.POST.get('password1', None)
            password2 = request.POST.get('password2', None)
            if email and password1 and password2:
                username = email.split('@')[0]
                if UserProfile.objects.filter(username=username).exists():
                    return JsonResponse({'msg': 'exists'})
                if not password1 == password2:
                    return JsonResponse({'msg': 'mismatch'})
                new_user = UserProfile(username=username, email=email)
                new_user.password = make_password(password2)
                new_user.save()
                return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': 'ko'})


class CustomBackend(ModelBackend):
    """
    增加邮箱登录
    继承ModelBackend类，覆盖authenticate方法, 增加邮箱认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 使用get是因为不希望用户存在两个, Q：使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # 判断密码是否匹配时，django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有check_password(self, raw_password)方法
            if user.check_password(password):
                return user
        except BaseException as e:
            return None


class UserLogin(View):
    """
    登录
    """
    def post(self, request):
        if request.is_ajax():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': 'ko'})


class UserLogout(View):
    """
    注销
    """
    def get(self, request):
        logout(request)
        return JsonResponse({'msg': 'ok'})


class NoLogin(View):
    """
    如果还没有登录，就进行操作，就定向到这里
    """
    def get(self, request):
        return render(request, 'bs-no-login.html')


class UserHome(View):
    """
    个人主页
    """
    def get(self, request, uid):
        user = get_object_or_404(UserProfile, id=int(uid))
        courses = Course.objects.filter(user=user)
        subscribed_courses = Course.objects.filter(classgrade__students=user)
        context = {
            'user': user,
            'courses': courses,
            'subscribed_courses': subscribed_courses,
        }
        return render(request, 'user/bs-user-home.html', context=context)


class EditProfile(LoginRequiredMixin, View):
    """
    编辑资料
    """
    def get(self, request, uid):
        user = get_object_or_404(UserProfile, id=int(uid))
        if user != request.user:
            raise Http404
        return render(request, 'user/bs-edit-profile.html', {'user': user})


class UpdateProfile(LoginRequiredMixin, View):
    """
    更新资料
    """
    def post(self, request):
        if request.is_ajax():
            stu_num = request.POST.get('snum', None)
            stu_name = request.POST.get('sname', None)
            nickname = request.POST.get('nickname', None)
            signature = request.POST.get('signature', None)
            uid = request.POST.get('uid', None)
            if uid:
                try:
                    user = UserProfile.objects.get(id=int(uid))
                    if user != request.user:
                        raise Http404
                    user.stu_num = stu_num
                    user.stu_name = stu_name
                    user.nickname = nickname
                    user.signature = signature
                    user.save()
                    return JsonResponse({'msg': 'ok'})
                except (UserProfile.DoesNotExist, BaseException) as e:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class UpdateAvatar(LoginRequiredMixin, View):
    """
    更新头像，这里采用上传到七牛云
    因为是通过Ajax模仿表单进行传图片过来，原先的ajax csrf token 失效了，
    所以可以继承CsrfViewMiddleware来忽略中间件的crsf防御
    """
    def post(self, request):
        if request.is_ajax():
            uid = request.POST.get('uid', None)
            avatar_url = request.POST.get('url', None)
            is_pass = uid and avatar_url
            if is_pass:
                try:
                    user = UserProfile.objects.get(id=int(uid))
                    if user != request.user:
                        raise Http404
                    user.avatar_url = settings.DOMAIN + avatar_url
                    user.save()
                    return JsonResponse({'msg': 'ok', 'url': avatar_url})
                except (UserProfile.DoesNotExist, BaseException) as e:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})

