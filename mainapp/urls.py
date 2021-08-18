from django.urls import re_path

from mainapp import views as mainapp


app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.index, name='index'),
]
