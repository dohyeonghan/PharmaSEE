from django.urls import path
from .views import pill_ai_identify

urlpatterns = [
    path('identify/', pill_ai_identify, name='pill-ai-indentify')
]
