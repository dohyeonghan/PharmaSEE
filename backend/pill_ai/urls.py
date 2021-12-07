from django.urls import path, include

from .views import DnnImageView

urlpatterns = [
    path('img_upload/', DnnImageView.as_view(), name='img-upload')
]
