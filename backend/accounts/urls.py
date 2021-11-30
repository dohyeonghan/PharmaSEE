from django.urls import path,include
from . import views
#from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns =[
    path('signup/', views.SignupView.as_view(), name='login'),
    #path('token/', obtain_jwt_token),
    #path('token/refresh/', refresh_jwt_token),
    #path('token/verify/', verify_jwt_token),
    path('follow/', views.user_follow, name='user_follow'),
    path('unfollow/', views.user_unfollow, name='user_unfollow'),
    path('search/', views.UserListView.as_view(), name='user_list'),
]