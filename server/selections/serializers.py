from rest_framework import serializers
from .models import Selection, VerseRange
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    selections = serializers.HyperlinkedRelatedField(
        many=True, view_name="selection-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "email", "selections"]


class SelectionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Selection
        fields = [
            "url",
            "id",
            "owner",
            "label",
            "voice",
            "repeat",
            "version",
            "read_label",
        ]


class VerseRangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VerseRange
        fields = ["url", "id", "selection", "start_verse", "end_verse"]
