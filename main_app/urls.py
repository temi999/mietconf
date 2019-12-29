from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send_material/', views.send_material, name='send_material'),
    path('requests/', views.requests, name='requests'),
    path('download/<path:path>/', views.download, name='download'),
    path('requests/author/<int:pk>/', views.check_author_request, name='check_author_request'),
    path('requests/material/<int:pk>/', views.check_material, name='check_material'),
    path('requests/<str:request_type>/<int:pk>/<str:decision>/', views.consider, name='consider')
    ]
