from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('consultation/', views.submit_consultation, name='submit_consultation'),
]

