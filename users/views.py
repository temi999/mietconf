from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from main_app import models
from .models import UserProfile
from django.contrib.auth.models import User
from .forms import UserForm, UserProfileForm, AuthorApprovalRequestForm


# Страница регистрации
def register(request):
    # Если форма заполнена правильно - регистрируем пользователя,
    # входим под ним и переходим на главную
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# Страница профиля, требуется аутентификация, иначе редирект на страницу логина
@login_required
def profile(request):
    context = {}

    # Получаем объекты пользователя и профиля
    user = request.user
    userprofile = user.userprofile

    # Задаем стандартные значения для формы пользователя
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    user_form_initial = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }

    # Задаем стандартные значения для формы профиля пользователя
    location = userprofile.location
    birth_date = userprofile.birth_date
    userprofile_form_initial = {
        'location': location,
        'birth_date': birth_date
    }

    # Если форма заполнена и отправлена - сохраняем ее
    # Если нет - открываем страницу профиля
    if request.method == 'POST':
        # Получаем объекты нужных форм и указываем, что изменяем именно их
        user_form_instance = get_object_or_404(User, id=user.id)
        user_form = UserForm(request.POST or None, instance=user_form_instance)
        userprofile_form_instance = get_object_or_404(UserProfile, user=user)
        userprofile_form = UserProfileForm(request.POST or None,
                                           instance=userprofile_form_instance)

        # Проверяем правильность заполнения формы
        if user_form.is_valid() and userprofile_form.is_valid():
            update = user_form.save(commit=False)
            update.id = user.id
            update.save()
            update = userprofile_form.save(commit=False)
            update.user = user
            update.save()
    else:
        # Задаем формы со стандартными значениями
        user_form = UserForm(initial=user_form_initial)
        userprofile_form = UserProfileForm(initial=userprofile_form_initial)

    context['user_form'] = user_form
    context['userprofile_form'] = userprofile_form

    if user.userprofile.status == 'author':
        context['material_approval_requests'] = \
            models.MaterialApprovalRequest.objects.get(author=user)
        context['materials'] = models.Material.objects.get(author=user)

    return render(request, 'users/profile.html', context=context)


# Страница создания запроса на получения статуса автора
def become_author(request):
    context = {}
    # Если форма правильно заполнена - сохраняем запрос и меняем статус юзера
    # и направляем на страницу профиля.Иначе - перезагружаем страницу
    if request.method == 'POST':
        form = AuthorApprovalRequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.author = request.user
            new_request.save()
            request.user.userprofile.status = 'approving'
            request.user.userprofile.save()
            return redirect('profile')
    else:
        context['form'] = AuthorApprovalRequestForm()
    return render(request, 'users/become_author.html', context=context)
