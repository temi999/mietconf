from django.shortcuts import render
from . import models


def home(request):
    context = {}
    section_list = models.Section.objects.all()

    context['section_list'] = section_list
    return render(request, 'main_app/home.html', context=context)

