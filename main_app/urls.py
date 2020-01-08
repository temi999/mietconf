from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send_material/', views.send_material, name='send_material'),
    path('requests/', views.requests, name='requests'),
    path('download/<path:path>/', views.download, name='download'),
    path('requests/<str:request_type>/<int:pk>/<str:decision>/', views.consider, name='consider'),
    path('materials/', views.material_list, name='material_list'),
    path('management/', views.management, name='management')
    ]
