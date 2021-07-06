from django.urls import path

from authapp.views import UserLoginView, RegisterCreateView, UserLogoutView, ProfileUpdateView

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
]
