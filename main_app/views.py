from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SendMaterialForm
from django.shortcuts import redirect, HttpResponse, Http404
from .models import Material, Section
from isconf import settings
from mimetypes import guess_type
from django.utils.http import urlquote
from users.models import AuthorApprovalRequest, UserProfile
from django.db.models import Q
import os


# Домашняя страница
def home(request):
    return render(request, 'pages/home.html', {})

def send_material(request):
    if not request.user.userprofile.can_send_material():
        return redirect('home')

    if request.method == 'POST':
        form = SendMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.status = material.TECH
            material.author = request.user
            material.section = request.user.userprofile.section
            material.save()
            return redirect('profile')
    else:
        form = SendMaterialForm()

    return render(request, 'forms/send_material.html', {'form': form})

def requests(request):
    if not request.user.userprofile.is_staff:
        return redirect('home') # TO DO: Перенаправление на страницу с ошибкой
    context = {}
    context['materials'] = Material.objects.filter(status=request.user.userprofile.status)
    context['author_requests'] = AuthorApprovalRequest.objects.all()
    return render(request, 'pages/requests.html', context)

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    file_name = os.path.basename(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=guess_type(file_name)[0])
            response['Content-Disposition'] = f'attachment; filename={urlquote(file_name)}'
            return response
    raise Http404

def consider(request, pk, request_type:str, decision:str):
    if not request.user.userprofile.is_staff:
        return redirect('home') # TO DO: Перенаправление на страницу с ошибкой
    if decision == 'accept':
        accept = True
    else:
        accept = False

    if request_type == 'author':
        obj = AuthorApprovalRequest.objects.get(pk=pk)
        obj.consider(accept)
    elif request_type == 'material':
        obj = Material.objects.get(pk=pk)
        obj.consider(accept)

    return redirect('requests')

@login_required
def material_list(request):
    sections = Section.objects.exclude(name='Нет секции')
    materials = {}
    for section in sections:
        materials[f'{section.name}'] = section.material_set.filter(show_on_materials_page=True)
    print(len(materials))
    if materials:
        print(materials)
    return render(request, 'pages/materials.html', {'materials': materials,
                                                    'sections': sections})

def management(request):
    if request.user.userprofile.status != 'head':
        return redirect('home')

    statuses = [ {'choice': i[0], 'display': i[1]} for i in UserProfile.STATUS_CHOICES]
    sections = Section.objects.filter(Q(name='Нет секции') | Q(name=request.user.section.name))

    section_filter = request.GET.get('section_filter')

    if not section_filter or section_filter == 'any':
        persons = UserProfile.objects.filter(Q(section__name='Нет секции') | Q(section__name=request.user.section.name))
    else:
        persons = UserProfile.objects.filter(section__name=section_filter)

    name_filter = request.GET.get('name_filter')
    login_filter = request.GET.get('login_filter')
    email_filter = request.GET.get('email_filter')
    status_filter = request.GET.get('status_filter')
    new_section = request.GET.get('new_section')
    new_status = request.GET.get('new_status')
    person_id = request.GET.get('person_id')

    if name_filter:
        persons = persons.filter(Q(user__last_name__icontains=name_filter) | Q(user__first_name__icontains=name_filter))

    if login_filter:
        persons = persons.filter(user__username__icontains=login_filter)

    if email_filter:
        persons = persons.filter(user__email__icontains=email_filter)

    if status_filter:
        for status in statuses:
            if status['choice'] == status_filter:
                status_filter = status
        print(status_filter)

        if status_filter !='any':
            persons = persons.filter(status=status_filter['choice'])



    if new_status:
        person = UserProfile.objects.get(pk=person_id)
        person.change_status(new_status)
        return redirect('management')

    if new_section:
        person = UserProfile.objects.get(pk=person_id)
        person.section = Section.objects.get(name=new_section)
        return redirect('management')

    context = {
        'persons': persons,
        'statuses': statuses,
        'sections': sections,
        'name_filter': name_filter,
        'login_filter': login_filter,
        'email_filter': email_filter,
        'status_filter': status_filter,
        'section_filter': section_filter
    }
    return render(request, 'pages/management.html', context)

