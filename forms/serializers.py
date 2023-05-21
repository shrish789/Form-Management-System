# serializers.py
from rest_framework import serializers

from forms.constants import MULTIPLE_CHOICE, FormStateChoice

from .models import Form, Option, Question


class FormCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    state = serializers.IntegerField(default=FormStateChoice.CREATED)
    commands = serializers.CharField(allow_blank=True, allow_null=True)
    author_id = serializers.IntegerField(default=1)

    class Meta:
        model = Form
        fields = ["title", "description", "state", "commands", "author_id"]


class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = [
            "uid",
            "title",
            "description",
            "state",
            "author",
            "commands",
            "created_at",
            "updated_at",
        ]


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["text"]


class QuestionBaseSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            "uid",
            "title",
            "description",
            "rank",
            "type",
            "options",
            "metadata",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["type"] != MULTIPLE_CHOICE:
            data.pop("options")
        return data

    def get_options(qs):
        pass
