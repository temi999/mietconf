from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>/', views.readonly_profile, name='readonly_profile'),
    path('become_author/', views.become_author, name='become_author')
]