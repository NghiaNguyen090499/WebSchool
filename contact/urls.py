from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('consultation/', views.submit_consultation, name='submit_consultation'),
    path('chatbot/lead-info/', views.submit_chatbot_lead_info, name='submit_chatbot_lead_info'),
    path('chatbot/', views.submit_chatbot_lead, name='submit_chatbot_lead'),
]





