from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    """ Выход с сайта """
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    """ Регистрация нового пользователя """
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        """ обработка заполненной формы """
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # выполнение входа и перенаправление на домашнюю страницу
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)
