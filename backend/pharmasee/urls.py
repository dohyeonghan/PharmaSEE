from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('pills', views.PillViewSet)
router.register('reminders', views.ReminderViewSet)
router.urls

urlpatterns =[
    path('api/', include(router.urls)),
    path('search/', views.PillListView.as_view(), name='pill_list')
]