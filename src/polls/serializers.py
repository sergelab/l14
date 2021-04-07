from rest_framework import serializers

from .handlers import PollsApi


class ListLinksField(serializers.ListField):
    question_id = serializers.IntegerField(required=True)
    next_question_id = serializers.IntegerField(required=True)
    answer_id = serializers.CharField(allow_null=True)


class ListAnswers(serializers.ListField):
    answer_id = serializers.CharField(required=True)
    title = serializers.CharField(required=True)


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    links = ListLinksField(allow_empty=True, required=False)
    answers = ListAnswers(allow_empty=True, required=False)


class NewQuestion(serializers.Serializer):
    title = serializers.CharField(required=True)
    next = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return validated_data


class AnswerSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    next_question_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return validated_data
