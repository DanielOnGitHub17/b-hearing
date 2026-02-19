from django.urls import path

from selection import views

urlpatterns = [
    path("", views.SelectionView.as_view()),
]
