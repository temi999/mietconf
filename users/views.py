from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from main_app.models import Section, Material
from .models import UserProfile, AuthorApprovalRequest
from django.contrib.auth.models import User
from .forms import UserForm, UserProfileForm, AuthorApprovalRequestForm


def register_view(request):
    """ Страница регистрации, использует стандартную форму django (UserCreationForm)
        TO DO: Доработать неправильное заполнение и если пользователь уже вошел """
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

    return render(request, 'forms/register.html', {'form': form})

def login_view(request):
    """ Страница входа, использует стандартную форму django (AuthenticationForm)
        TO DO: Доработать неправильное заполнение """
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

        Требуется вход в аккаунт. Если вход не выполнен - перенаправляет на страницу входа

        TO DO: для авторов дополнительно передавать список его материалов и заявок """
    context = {}

    # Задаем начальные значения передаваемых переменных
    show_request = False
    is_request_exist = False
    is_material_sent = False

    # Получаем объекты пользователя и профиля
    user = request.user
    userprofile = user.userprofile

    # Задаем статус и текст статуса пользователя
    user_status = userprofile.status
    if user_status in ('participant', 'approving'):
        user_status_text = 'Участник'
    else:
        user_status_text = userprofile.get_status_display()

    # Показывать ли сакцию со статусом заявки
    if not (userprofile.is_staff() or userprofile.is_author()):
        show_request = True

    # Проверяем, существует ли запрос на получение статуса автора
    # Если да - задаем его
    if AuthorApprovalRequest.objects.filter(author=user).exists():
        is_request_exist = True
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
        context['user_status_text'] = user_status_text
        context['is_request_exist'] = is_request_exist
        context['show_request'] = show_request
        context['is_material_sent'] = is_material_sent
        if is_material_sent:
            context['material_status'] = Material.objects.get(author=user).get_status_display()

    return render(request, 'pages/profile.html', context=context)

def readonly_profile(request, pk):
    profile = User.objects.get(pk=pk)
    return render(request, 'pages/readonly_profile.html', {'profile': profile})


def become_author(request):
    """ Форма для создания запроса на получение статуса автора """
    if AuthorApprovalRequest.objects.filter(author=request.user).exists():
        return redirect('profile') #TO DO: Направлять на страницу с ошибкой
    context = {}
    # Задаем список секций
    section_list = Section.objects.all()
    # Если форма правильно заполнена - сохраняем запрос и меняем статус юзера
    # и направляем на страницу профиля. Иначе - перезагружаем страницу
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
            return redirect('become_author')
    else:
        context['form'] = AuthorApprovalRequestForm()
        context['section_list'] = section_list

    return render(request, 'forms/become_author.html', context=context)
