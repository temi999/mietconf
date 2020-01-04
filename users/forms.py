from django.forms import ModelForm, TextInput, ModelChoiceField, Textarea
from .models import UserProfile, AuthorApprovalRequest
from django.contrib.auth.models import User
from main_app.models import Section


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['location', 'birth_date']
        widgets = {
            'location': TextInput(attrs={
                'class': 'form-control',
                'id': 'city',
                'placeholder': 'Город'
            }),
            'birth_date': TextInput(attrs={
                'class': 'form-control',
                'id': 'birth_date',
                'placeholder': 'Дата рождения'
            }),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'id': 'first_name',
                'placeholder': 'Имя'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'id': 'last_name',
                'placeholder': 'Фамилия'
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Email'
            })
        }


class AuthorApprovalRequestForm(ModelForm):
    class Meta:
        model = AuthorApprovalRequest
        fields = ['cover_letter', 'section']
        widgets = {
            'cover_letter': Textarea(attrs={
                'class': 'form-control',
                'id': 'about',
                'rows': '10',
                'placeholder': 'О себе'
            })
        }

    def __init__(self, *args, **kwargs):
        super(AuthorApprovalRequestForm, self).__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.objects.exclude(name='Нет секции')
