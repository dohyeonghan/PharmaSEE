from django.urls import path
from .views import answer_taken_pills

urlpatterns = [
    path('answer.taken_pills', answer_taken_pills, name='ans_taken_pills')
]
