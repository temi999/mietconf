from django.forms import ModelForm, Textarea, TextInput, FileInput
from . import models


class SendMaterialForm(ModelForm):
    class Meta:
        model = models.Material
        fields = ['title', 'description', 'document', 'presentation']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'id': 'title',
                'placeholder': 'Название статьи'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Краткое описание'
            }),
            'document': FileInput(attrs={
                'class': 'form-control-file',
                'id': 'document'
            }),
            'presentation': FileInput(attrs={
                'class': 'form-control-file',
                'id': 'presentation'
            })
        }