from django.urls import include, path
from selections import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"selections", views.SelectionViewSet, basename="selection")
router.register(r"verseranges", views.VerseRangeViewSet, basename="verserange")
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"audiosources", views.AudioSourceViewSet, basename="audiosource")
router.register(r"audiooffsets", views.AudioOffsetViewSet, basename="audiooffset")

urlpatterns = [path("", include(router.urls))]
