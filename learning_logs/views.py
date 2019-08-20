from django.shortcuts import render, reverse
from .models import Topic, Entry
from .forms import TopicForm, EntyForm
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    """ Домашняя странциа приложения """
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """ Вывод списка всех тем """
    topics = Topic.objects.filter(owner=request.user).order_by('date_add')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # Проверка того что тема принадлежит текущему пользователю
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-data_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """ Определяет новую тему """
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """ Добавляет новыую запись к конкретной теме """
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntyForm()
    else:
        form = EntyForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """ Редактирует запись """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # Форма заполняет данными из текущей записи.
        form = EntyForm(instance=entry)
    else:
        form = EntyForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
