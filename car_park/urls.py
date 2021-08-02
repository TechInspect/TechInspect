from django.urls import path, re_path

# from .views import index, ParkCreateView, by_user
from car_park.views import cars, CarAdd, CarDetail, CarEdit, CarDelete, car_activate, history, HistoryAdd

app_name = 'car_park'

urlpatterns = [
    # path('add/', ParkCreateView.as_view(), name='add'),
    # path('<int:uid_id>/', by_user, name='user'),
    # path('', index, name='index'),

    re_path(r'^$', cars, name='cars'),
    re_path(r'^add/$', CarAdd.as_view(), name='add'),
    re_path(r'^(?P<pk>\d+)/$', CarDetail.as_view(), name='car_info'),
    re_path(r'^(?P<pk>\d+)/activate$', car_activate, name='activate'),
    re_path(r'^(?P<pk>\d+)/edit', CarEdit.as_view(), name='edit'),
    re_path(r'^(?P<pk>\d+)/delete', CarDelete.as_view(), name='delete'),

    re_path(r'^(?P<car_id>\d+)/history/$', history, name='history'),
    re_path(r'^(?P<car_id>\d+)/history/add/$', HistoryAdd.as_view(), name='history_add'),
]
