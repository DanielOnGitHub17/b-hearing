from django.urls import path

from server.selections import views

urlpatterns = [
    path("", views.SelectionsView.as_view()),
    path("<int:id>/", views.SelectionView.as_view()),
]
