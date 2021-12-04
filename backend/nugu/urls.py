from django.urls import path
from .views import answer_taken_pills, answer_not_taken_pills, ask_to_call, health

urlpatterns = [
    path('answer.taken_pills', answer_taken_pills, name='ans-taken-pills'),
    path('answer.not_taken_pills', answer_not_taken_pills, name='ans-not-taken-pills'),
    path('health', health, name='health')
]