from rest_framework import serializers
from .models import Selection, VerseRange, Verse
from users.models import User


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ["book", "chapter", "verse", "kjv"]


class VerseRangeSerializer(serializers.ModelSerializer):
    verses = serializers.SerializerMethodField()

    class Meta:
        model = VerseRange
        fields = ["id", "selection", "start_verse", "end_verse", "verses"]

    def get_verses(self, obj):
        verses_start_to_end = Verse.objects.filter(
            id__range=(obj.start_verse.id, obj.end_verse.id)
        ).order_by("id")
        return VerseSerializer(verses_start_to_end, many=True).data


class SelectionListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")
    verse_ranges_length = serializers.SerializerMethodField()

    def get_verse_ranges_length(self, obj):
        return obj.verse_ranges.count()

    class Meta:
        model = Selection
        fields = [
            "id",
            "owner",
            "label",
            "voice",
            "repeat",
            "version",
            "read_label",
            "verse_ranges_length",
        ]


class SelectionDetailSerializer(SelectionListSerializer):
    verse_ranges = VerseRangeSerializer(many=True, read_only=True)

    class Meta:
        model = Selection
        fields = SelectionListSerializer.Meta.fields + ["verse_ranges"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    selections = serializers.HyperlinkedRelatedField(
        many=True, view_name="selection-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "email", "selections"]
