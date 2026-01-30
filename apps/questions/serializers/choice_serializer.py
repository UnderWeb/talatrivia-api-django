# apps/questions/serializers/choice_serializer.py
from rest_framework import serializers

from ..models.choice import Choice


class ChoiceAdminSerializer(serializers.ModelSerializer):
    """
    Full choice data for administrative purposes.
    """

    class Meta:
        model = Choice
        fields = ["id", "text", "is_correct"]
        read_only_fields = ["id"]


class ChoicePlayerSerializer(serializers.ModelSerializer):
    """
    Minimal choice data for players.
    Strictly omits the 'is_correct' field.
    """

    class Meta:
        model = Choice
        fields = ["id", "text"]
