from django.urls import path

from . import views

app_name = "staff"

urlpatterns = [
    path("", views.staff_list, name="list"),
    path("<slug:slug>/", views.staff_detail, name="detail"),
]
