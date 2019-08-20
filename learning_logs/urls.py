""" Определяет схемы URL для learning_logs """


from django.urls import path
from . import views

app_name = 'learning_logs'

urlpatterns = [
    # сраница добавления новой темы
    path('new_topic/', views.new_topic, name='new_topic'),
    # редактирование записей
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
    # страница добавления новых записей
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # страница с подробной информацией по отдельным темам
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    # страница со всеми темами
    path('topics/', views.topics, name='topics'),
    # домашняя страница
    path('', views.index, name='index'),
]