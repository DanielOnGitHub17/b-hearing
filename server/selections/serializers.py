from django.db import models
from rest_framework import serializers

from users.models import User
from .models import (
    AudioOffsetSuggestion,
    AudioSource,
    AudioSourceSuggestion,
    Selection,
    Verse,
    VerseRange,
)


class VerseSerializer(serializers.ModelSerializer):
    """Minimal verse representation used when embedding a verse range."""

    class Meta:
        model = Verse
        fields = ["book", "chapter", "verse", "kjv"]


class AudioSourceSerializer(serializers.ModelSerializer):
    """Serializer for suggested audio sources.

    This is the create/update serializer used by the `/audiosources/` endpoint.
    It intentionally mirrors the real fields on `AudioSourceSuggestion`, which
    inherits from `AudioSource`.
    """

    class Meta:
        model = AudioSourceSuggestion
        fields = ["url_template", "name", "version", "version_abbr"]


class AudioOffsetSerializer(serializers.ModelSerializer):
    """Serializer for suggested verse-to-audio alignment values."""

    class Meta:
        model = AudioOffsetSuggestion
        fields = ["source", "verse"]

    def validate(self, attrs):
        """Guard against invalid relationships before saving the suggestion."""
        source = attrs.get("source")
        verse = attrs.get("verse")

        if source is None or verse is None:
            raise serializers.ValidationError(
                "Both 'source' and 'verse' are required for an audio offset suggestion."
            )

        return attrs


class VerseRangeSerializer(serializers.ModelSerializer):
    """Serializer for a verse range within a selection.

    The model stores a start and end verse, and the serializer also expands the
    inclusive range into a list of full verse rows for easier API usage.
    """

    verses = serializers.SerializerMethodField()

    class Meta:
        model = VerseRange
        fields = ["id", "position", "selection", "start_verse", "end_verse", "verses"]

    def validate(self, attrs):
        """Ensure the range is internally consistent before creating it."""
        start_verse = attrs.get("start_verse")
        end_verse = attrs.get("end_verse")

        if start_verse is not None and end_verse is not None:
            if start_verse.id > end_verse.id:
                raise serializers.ValidationError(
                    "'start_verse' must be less than or equal to 'end_verse'."
                )

        return attrs

    def get_verses(self, obj):
        verses_start_to_end = Verse.objects.filter(
            id__range=(obj.start_verse.id, obj.end_verse.id)
        ).order_by("id")
        return VerseSerializer(verses_start_to_end, many=True).data


class SelectionSerializer(serializers.ModelSerializer):
    """Create/update serializer for a Selection."""

    owner = serializers.ReadOnlyField(source="owner.email")
    audio_source = serializers.PrimaryKeyRelatedField(
        queryset=AudioSource.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Selection
        fields = [
            "id",
            "owner",
            "label",
            "browser_voice",
            "audio_source",
            "repeat",
            "version",
            "read_label",
        ]
        read_only_fields = ["id", "owner"]


class SelectionDetailSerializer(SelectionSerializer):
    """Detailed selection payload including all nested verse ranges."""

    verse_ranges = VerseRangeSerializer(many=True, read_only=True)

    class Meta(SelectionSerializer.Meta):
        fields = SelectionSerializer.Meta.fields + ["verse_ranges"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    selections = serializers.HyperlinkedRelatedField(
        many=True, view_name="selection-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "email", "selections"]
