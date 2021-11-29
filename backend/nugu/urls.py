from django.urls import path
from .views import get_nugu_request

urlpatterns = [
    path('', get_nugu_request, name='nugu_response')
]
