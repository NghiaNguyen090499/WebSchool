from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('', views.admission_list, name='list'),
    path('dang-ky/', views.registration_page, name='registration'),
    path('dang-ky/du-tuyen/', views.submit_registration, name='submit'),
    path('dang-ky/tu-van/', views.submit_consultation, name='submit_consultation'),
    path('documents/<int:pk>/download/', views.download_document, name='document_download'),
    path('<str:level>/', views.admission_detail, name='detail'),
]
