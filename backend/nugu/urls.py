from django.urls import path
from .views import answer_taken_pills, answer_not_taken_pills, ask_to_call

urlpatterns = [
    path('answer.taken_pills', answer_taken_pills, name='ans-taken-pills'),
    path('answer.not_taken_pills', answer_not_taken_pills, name='ans-not-taken-pills'),
    path('ask_to_call', ask_to_call, name='ask-to-call')
]