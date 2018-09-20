from pyjexl.jexl import JEXL
from rest_framework import exceptions

from . import models
from .. import serializers


class SaveFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = ("slug", "name", "description", "meta")


class ArchiveFormSerializer(serializers.ModelSerializer):
    id = serializers.GlobalIDField(source="slug")

    def update(self, instance, validated_data):
        instance.is_archived = True
        instance.save(update_fields=["is_archived"])
        return instance

    class Meta:
        fields = ("id",)
        model = models.Form


class AddFormQuestionSerializer(serializers.ModelSerializer):
    form = serializers.GlobalIDField(source="slug")
    question = serializers.GlobalIDPrimaryKeyRelatedField(
        queryset=models.Question.objects
    )

    def update(self, instance, validated_data):
        models.FormQuestion.objects.get_or_create(
            form=self.instance, question=validated_data["question"]
        )
        return instance

    class Meta:
        fields = ("form", "question")
        model = models.Form


class RemoveFormQuestionSerializer(serializers.ModelSerializer):
    form = serializers.GlobalIDField(source="slug")
    question = serializers.GlobalIDPrimaryKeyRelatedField(
        queryset=models.Question.objects
    )

    def update(self, instance, validated_data):
        models.FormQuestion.objects.filter(
            form=instance, question=validated_data["question"]
        ).delete()
        return instance

    class Meta:
        fields = ("form", "question")
        model = models.Form


class FormQuestionRelatedField(serializers.GlobalIDPrimaryKeyRelatedField):
    def get_queryset(self):
        form = self.parent.parent.instance
        return form.questions.all()


class ReorderFormQuestionsSerializer(serializers.ModelSerializer):
    form = serializers.GlobalIDField(source="slug")
    questions = FormQuestionRelatedField(many=True)

    def update(self, instance, validated_data):
        questions = validated_data["questions"]
        for sort, question in enumerate(reversed(questions)):
            models.FormQuestion.objects.filter(form=instance, question=question).update(
                sort=sort
            )

        return instance

    class Meta:
        fields = ("form", "questions")
        model = models.Form


class PublishFormSerializer(serializers.ModelSerializer):
    id = serializers.GlobalIDField(source="slug")

    def update(self, instance, validated_data):
        instance.is_published = True
        instance.save(update_fields=["is_published"])
        return instance

    class Meta:
        fields = ("id",)
        model = models.Form


class SaveQuestionSerializer(serializers.ModelSerializer):
    def _validate_jexl_expression(self, expression):
        jexl = JEXL()
        # TODO: define transforms e.g. answer
        errors = list(jexl.validate(expression))
        if errors:
            raise exceptions.ValidationError(errors)

        return expression

    def validate_is_required(self, value):
        return self._validate_jexl_expression(value)

    def validate_is_hidden(self, value):
        return self._validate_jexl_expression(value)

    # TODO: validate configuration depending on type

    class Meta:
        model = models.Question
        fields = (
            "slug",
            "label",
            "type",
            "is_required",
            "is_hidden",
            "configuration",
            "meta",
        )


class ArchiveQuestionSerializer(serializers.ModelSerializer):
    id = serializers.GlobalIDField(source="slug")

    def update(self, instance, validated_data):
        instance.is_archived = True
        instance.save(update_fields=["is_archived"])
        return instance

    class Meta:
        fields = ("id",)
        model = models.Question
