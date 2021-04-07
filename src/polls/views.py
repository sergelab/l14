from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import QuestionSerializer, NewQuestion, AnswerSerializer
from .handlers import PollsApi


class PollAPIView(APIView):
    def __init__(self, *args, **kwargs):
        self.storage = PollsApi()
        super(PollAPIView, self).__init__(*args, **kwargs)


class QuestionAPIView(PollAPIView):
    def get(self, request, question_id=None):
        """
        Возвращает все вопросы или вопрос с указанным id.
        """
        if question_id:
            return Response(QuestionSerializer(self.storage.get_question(question_id)).data)

        return Response({"questions": QuestionSerializer(self.storage.get_all_questions(), many=True).data})

    def post(self, request):
        serializer = NewQuestion(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(QuestionSerializer(self.storage.add_question(serializer.save())).data)

        return Response(status=422)

    def put(self, request, question_id):
        serializer = NewQuestion(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(QuestionSerializer(self.storage.update_question(question_id, serializer.save())).data)

        return Response(status=422)


class AnswerAPIView(PollAPIView):
    def post(self, request, question_id):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.storage.add_answer(question_id, serializer.save())
            return Response(QuestionSerializer(self.storage.get_question(question_id)).data)
        return Response(status=422)

    def put(self, request, question_id, answer_id):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.storage.update_answer(question_id, answer_id, serializer.save())
            return Response(QuestionSerializer(self.storage.get_question(question_id)).data)
        return Response(status=422)
