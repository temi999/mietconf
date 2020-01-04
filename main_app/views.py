from django.shortcuts import render
from . import models
from .forms import SendMaterialForm
from django.shortcuts import redirect, HttpResponse, Http404
from .models import Material, Section
from isconf import settings
from mimetypes import guess_type
from django.utils.http import urlquote
from users.models import AuthorApprovalRequest
import os


# Домашняя страница
def home(request):
    context = {}
    section_list = models.Section.objects.exclude(name='Нет секции')

    context['section_list'] = section_list
    return render(request, 'pages/home.html', context)

def send_material(request):
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

def material_list(request):
    sections = Section.objects.exclude(name="Нет секции")
    materials = Material.objects.all()
    return render(request, 'pages/materials.html', {'materials': materials,
                                                    'sections': sections})

