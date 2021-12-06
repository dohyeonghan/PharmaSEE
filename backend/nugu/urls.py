from django.urls import path
from .views import answer_taken_pills, answer_not_taken_pills, answer_total_status, health

urlpatterns = [
    path('answer.taken_pills', answer_taken_pills, name='answer-taken-pills'),
    path('answer.not_taken_pills', answer_not_taken_pills, name='answer-not-taken-pills'),
    path('answer.total_status', answer_total_status, name='answer-total-status'),
    path('health', health, name='health')
]