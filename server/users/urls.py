from django.urls import path

from server.users import views

urlpatterns = [
    path("", views.profile),
]
