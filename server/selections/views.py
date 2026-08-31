"""Views for selections app."""

from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from users.models import User
from .models import AudioOffsetSuggestion, AudioSourceSuggestion, Selection, VerseRange
from .serializers import (
    AudioOffsetSerializer,
    AudioSourceSerializer,
    SelectionDetailSerializer,
    SelectionSerializer,
    UserSerializer,
    VerseRangeSerializer,
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class AudioSourceViewSet(viewsets.ModelViewSet):
    """Create/list suggested audio sources for a bible/audio provider."""

    queryset = AudioSourceSuggestion.objects.all()
    serializer_class = AudioSourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class AudioOffsetViewSet(viewsets.ModelViewSet):
    """Create/list suggested verse-to-audio mappings."""

    queryset = AudioOffsetSuggestion.objects.all()
    serializer_class = AudioOffsetSerializer
    permission_classes = [permissions.IsAuthenticated]


class SelectionViewSet(viewsets.ModelViewSet):
    """Selection lifecycle.

    The queryset is limited to the current user, and the user is injected as the
    owner automatically on create.
    """

    queryset = Selection.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SelectionDetailSerializer
        return SelectionSerializer

    def get_queryset(self):
        return Selection.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class VerseRangeViewSet(viewsets.ModelViewSet):
    """Verse ranges within a selection.

    This endpoint is the main place where the selection ownership is checked.
    """

    queryset = VerseRange.objects.all()
    serializer_class = VerseRangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VerseRange.objects.filter(selection__owner=self.request.user)

    def perform_create(self, serializer):
        selection = serializer.validated_data["selection"]

        if selection.owner != self.request.user:
            raise PermissionDenied(
                "You can only create verse ranges for your own selections."
            )

        return serializer.save()

    # def list(self, request, *args, **kwargs):
    #     return HttpResponse(b"No-")
