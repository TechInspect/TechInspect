from django.urls import path, re_path

# from .views import index, ParkCreateView, by_user
from car_park.views import cars, car_info, CarAdd, CarDetail, history, HistoryAdd

app_name = 'car_park'

urlpatterns = [
    # path('add/', ParkCreateView.as_view(), name='add'),
    # path('<int:uid_id>/', by_user, name='user'),
    # path('', index, name='index'),

    re_path(r'^$', cars, name='cars'),
    re_path(r'^add/$', CarAdd.as_view(), name='add'),
    # re_path(r'^(?P<car_id>\d+)/$', car_info, name='car_info'),
    re_path(r'^history_add/$', HistoryAdd.as_view(), name='history_add'),
    re_path(r'^(?P<pk>\d+)/$', CarDetail.as_view(), name='car_info'),
    re_path(r'^history/(?P<car_id>\d+)/$', history, name='history'),
]
