from django.urls import path

from authapp.views import UserLoginView, RegisterCreateView, UserLogoutView, ProfileUpdateView, verify

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
