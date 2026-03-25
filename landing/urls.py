from django.urls import path

from . import views

app_name = "landing"

urlpatterns = [
    path("<slug:slug>/", views.landing_detail, name="detail"),
]

