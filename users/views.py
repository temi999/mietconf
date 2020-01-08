from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from main_app.models import Material
from .models import UserProfile
from django.contrib.auth.models import User
from .forms import UserForm, UserProfileForm, AuthorApprovalRequestForm


def register_view(request):
    """ Страница регистрации, использует стандартную форму django (UserCreationForm)"""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()

    return render(request, 'forms/register.html', {'form': form})

def login_view(request):
    """ Страница входа, использует стандартную форму django (AuthenticationForm)"""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request, 'forms/login.html', {'form': form})

def logout_view(request):
    """ Перенаправляет на главную страницу после выхода из аккаунта """
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    """ Страница профиля

        Передается форма для изменения данных профиля и необходимая информация
        о пользователе: статус, статусы заявок, данные профиля

        Требуется вход в аккаунт. Если вход не выполнен - перенаправляет на страницу входа"""
    context = {}

    is_material_sent = False

    # Получаем объекты пользователя и профиля
    user = request.user
    userprofile = user.userprofile

    if Material.objects.filter(author=user).exists():
        is_material_sent = True

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
            return redirect('profile')
    else:
        # Задаем формы со стандартными значениями
        user_form = UserForm(initial=user_form_initial)
        userprofile_form = UserProfileForm(initial=userprofile_form_initial)

        # Заполняем контекстные данные
        context['user_form'] = user_form
        context['userprofile_form'] = userprofile_form
        context['author_form'] = AuthorApprovalRequestForm()
        if is_material_sent:
            context['material_status'] = Material.objects.get(author=user).get_status_display()

    return render(request, 'pages/profile.html', context=context)

def become_author(request):
    if not request.user.userprofile.is_request_allowed():
        return redirect('profile')

    if request.method == 'POST':
        form = AuthorApprovalRequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.author = request.user
            new_request.save()
            request.user.userprofile.status = 'approving'
            request.user.userprofile.save()

    return redirect('profile')
