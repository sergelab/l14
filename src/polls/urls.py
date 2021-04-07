from django.urls import path
from rest_framework.schemas import get_schema_view

from .views import QuestionAPIView, AnswerAPIView


app_name = 'polls'


urlpatterns = [
    path('', get_schema_view(
        title='Lot 14',
        description='API for polls',
        version='0.0.1'
    ), name='openapi-schema'),
    path('q/', QuestionAPIView.as_view()),
    path('q/<int:question_id>', QuestionAPIView.as_view()),
    # path('a/', AnswerAPIView.as_view()),
    path('a/<int:question_id>', AnswerAPIView.as_view()),
    path('a/<int:question_id>/<str:answer_id>', AnswerAPIView.as_view()),
]
