from rest_framework import serializers

from media_app.models import *


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model, including the reviewer's username as a string.
    """

    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class MediaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Media model.
    """

    class Meta:
        model = Media
        fields = "__all__"


class StreamingPlatformSerializer(serializers.ModelSerializer):
    """
    Serializer for the StreamingPlatform model, including related media objects.
    """

    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"