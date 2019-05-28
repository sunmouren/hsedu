# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/1/14 17:29
@desc: 
"""
from django.urls import path

from .views import UserLogin, UserLogout, NoLogin, \
    UserRegister, UserHome, EditProfile, UpdateProfile, UpdateAvatar


app_name = 'users'

urlpatterns = [
    path('login/', UserLogin.as_view()),
    path('logout/', UserLogout.as_view()),
    path('no/login/', NoLogin.as_view(), name='no-login'),
    path('register/', UserRegister.as_view()),
    path('home/<int:uid>/', UserHome.as_view(), name='user-home'),
    path('edit/profile/<int:uid>/', EditProfile.as_view(), name='edit-profile'),
    path('update/profile/', UpdateProfile.as_view()),
    path('update/avatar/', UpdateAvatar.as_view()),
]