from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from main_app.models import Section, MaterialApprovalRequest, Material
from .models import UserProfile, AuthorApprovalRequest
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

    # Задаем начальные значения передаваемых переменных
    is_firstname_exist = False
    is_lastname_exist = False
    is_author = False
    is_staff = False
    user_status = ''
    user_status_text = ''
    request_status = ''
    is_request_exist = False
    is_userdata_set = False
    is_request_allowed = False

    # Получаем объекты пользователя и профиля
    user = request.user
    userprofile = user.userprofile
    profile_name = user.username

    # Проверяем, заполнены ли имя и фамилия
    if user.first_name:
        is_firstname_exist = True
    if user.last_name:
        is_lastname_exist = True

    if user.first_name and user.last_name:
        profile_name += ' ({0} {1})'.format(user.first_name, user.last_name)
    elif user.first_name and not user.last_name:
        profile_name += f' ({user.first_name})'

    # Задаем статус и текст статуса пользователя
    user_status = userprofile.status
    if user_status in ('participant', 'approving'):
        user_status_text = 'Участник'
    else:
        user_status_text = userprofile.get_status_display()
        # if user_status == 'author':
        #     is_author = True
        if not is_author:
            is_staff = True

    # Проверяем, существует ли запрос на получение статуса автора
    # Если да - задаем его
    if AuthorApprovalRequest.objects.filter(author=user).exists():
        is_request_exist = True
        request_status = 'На проверке'

    # Проверяем, полностью ли заполнен профиль
    if user.first_name and user.last_name and user.email \
        and userprofile.location and userprofile.birth_date:
        is_userdata_set = True

    # Проверяем, можно ли отправить запрос
    if is_userdata_set and not is_request_exist:
        is_request_allowed = True

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

    # Задаем список секций
    section_list = Section.objects.all()

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
        context['section_list'] = section_list
        context['user_status'] = user_status
        context['user_status_text'] = user_status_text
        context['request_status'] = request_status
        context['is_request_exist'] = is_request_exist
        context['is_userdata_set'] = is_userdata_set
        context['is_request_allowed'] = is_request_allowed
        context['is_staff'] = is_staff
        context['is_author'] = is_author
        context['profile_name'] = profile_name

    return render(request, 'users/profile.html', context=context)


# Страница создания запроса на получения статуса автора
def become_author(request):
    context = {}
    # Задаем список секций
    section_list = Section.objects.all()
    # Если форма правильно заполнена - сохраняем запрос и меняем статус юзера
    # и направляем на страницу профиля. Иначе - перезагружаем страницу
    if request.method == 'POST':
        form = AuthorApprovalRequestForm(request.POST)
        if form.is_valid():
            print('VALID')
            new_request = form.save(commit=False)
            new_request.author = request.user
            new_request.save()
            request.user.userprofile.status = 'approving'
            request.user.userprofile.save()
            return redirect('profile')
        else:
            print('NE VALID')
            return redirect('become_author')
    else:
        context['form'] = AuthorApprovalRequestForm()
        context['section_list'] = section_list

    return render(request, 'users/become_author.html', context=context)
