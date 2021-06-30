from django.shortcuts import render
import datetime
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import TechInspectForm
from .models import Park, UserUID


def index(request):
    # park = Park.objects.all()
    # user_uid = UserUID.objects.all()
    context = {
        'title': 'Гараж',
        'cars': cars_example(),
        # 'user_uid': user_uid
    }
    return render(request, 'car_park/index.html', context)


def car_info(request, car_id):
    car_id = int(car_id)
    car = cars_example()[car_id - 1]
    car_info = car_info_example()
    print(car_info)
    context = {
        'title': f'{car["brand"]} {car["model"]} ({car["year"]})',
        'car': car,
        'car_info': car_info,
        'car_upcoming': car_upcoming_example(),
    }
    return render(request, 'car_park/car_info.html', context)


#
#
# def by_user(request, user_uid):
#     parks = Park.objects.filter(user=user_uid)
#     users = UserUID.objects.all()
#     current_user = UserUID.objects.get(pk=user_uid)
#     context = {'parks': parks, 'users': users, 'current_user': current_user}
#     return render(request, 'car_park/by_user.html', context)
#
#
# class ParkCreateView(CreateView):
#     template_name = 'car_park/create.html'
#     form_class = TechInspectForm
#     success_url = reverse_lazy('index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['parks'] = Park.objects.all()
#         return context


def cars_example():
    return [
        {
            'id': 1,
            'brand': 'Skoda',
            'model': 'Yeti',
            'year': 2012,
            'mileage': 155000,
            'uid': 1,
        }
    ]


def car_info_example():
    return [
        {
            'id': 1,
            'cid': 1,
            'mileage': 155030,
            'type': 'Заправка',
            'date': '05.06.2021',
            'comment': 'Заправил 30 литров'
        },
        {
            'id': 2,
            'cid': 1,
            'mileage': 155040,
            'type': 'ТО',
            'date': '10.06.2021',
            'comment': 'Замена масла'
        },
    ]


def car_upcoming_example():
    return [
        {
            'id': 1,
            'cid': 1,
            'mileage': 155250,
            'type': 'ТО',
            'date': '15.07.2021',
            'comment': 'Замена свечей'
        },
    ]
