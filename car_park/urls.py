from django.urls import path

from .views import index, ParkCreateView, by_user

urlpatterns = [
    path('add/', ParkCreateView.as_view(), name='add'),
    path('<int:uid_id>/', by_user, name='user'),
    path('', index, name='index'),
]
