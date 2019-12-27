from django.forms import ModelForm
from .models import UserProfile, AuthorApprovalRequest
from django.contrib.auth.models import User


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['location', 'birth_date']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AuthorApprovalRequestForm(ModelForm):
    class Meta:
        model = AuthorApprovalRequest
        fields = ['cover_letter', 'section']
