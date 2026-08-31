"""Views for selections app"""

from rest_framework import viewsets, permissions
from .models import Selection, VerseRange, AudioSourceSuggestion, AudioOffsetSuggestion
from .serializers import (
    SelectionListSerializer,
    SelectionDetailSerializer,
    VerseRangeSerializer,
    UserSerializer,
    AudioOffsetSerializer,
    AudioSourceSesrializer,
)
from users.models import User
from django.http import HttpResponse


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class AudioSourceViewSet(viewsets.ModelViewSet):
    queryset = AudioSourceSuggestion.objects.all()
    serializer_class = AudioSourceSesrializer
    permission_classes = [permissions.IsAuthenticated]


class AudioOffsetViewSet(viewsets.ModelViewSet):
    queryset = AudioOffsetSuggestion.objects.all()
    serializer_class = AudioOffsetSerializer
    permission_classes = [permissions.IsAuthenticated]


class SelectionViewSet(viewsets.ModelViewSet):
    queryset = Selection.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SelectionDetailSerializer
        return SelectionListSerializer

    def get_queryset(self):
        return Selection.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class VerseRangeViewSet(viewsets.ModelViewSet):
    queryset = VerseRange.objects.all()
    serializer_class = VerseRangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     return HttpResponse(b"No-")
