from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('', views.admission_list, name='list'),
    path('dang-ky/', views.submit_registration, name='submit'),
    path('<str:level>/', views.admission_detail, name='detail'),
]
