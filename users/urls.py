""" Опредляет схемы url для пользователей """

from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from . import views

app_name = 'users'

urlpatterns = [
    # регистрация пользователей
    path('register', views.register, name='register'),
    # страница выхода
    path('logout/', views.logout_view, name='logout'),
    # сраница входа
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
