from django.urls import path
from .views import answer_taken_pills, answer_not_taken_pills, answer_total_status, health

urlpatterns = [
    path('answer.taken_pills', answer_taken_pills, name='ans-taken-pills'),
    path('answer.not_taken_pills', answer_not_taken_pills, name='ans-not-taken-pills'),
    path('answer.total_stauts', answer_total_status, name='answer-total-status'),
    path('health', health, name='health')
]