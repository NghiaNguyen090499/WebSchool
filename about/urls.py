from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('mission/', views.mission, name='mission'),
    path('vision/', views.vision, name='vision'),
    path('principal/', views.principal_message, name='principal'),
]



