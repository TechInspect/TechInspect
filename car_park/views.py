from django.shortcuts import render
import datetime
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test

from car_park.models import Park
# from car_park.forms import CarAddForm

# from .forms import TechInspectForm
# from .models import Park, UserUID


@user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name='')
def cars(request):
    # park = Park.objects.all()
    # user_uid = UserUID.objects.all()
    context = {
        'title': 'Гараж',
        'cars': Park.objects.filter(user=request.user)
        # 'cars': cars_example(),
        # 'cars': [],
        # 'user_uid': user_uid
    }
    return render(request, 'car_park/cars.html', context)


class CarAdd(CreateView):
    model = Park
    fields = ['brand', 'model', 'year']
    template_name = 'car_park/car_add.html'
    success_url = reverse_lazy('car_park:cars')

    def get_context_data(self, **kwargs):
        context = super(CarAdd, self).get_context_data(**kwargs)
        context['title'] = 'Добавить авто в свой автопарк'
        return context

    def form_valid(self, form):
        car = form.save(commit=False)
        car.user = self.request.user
        return super(CarAdd, self).form_valid(form)


@user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name='')
def car_info(request, car_id):
    car_id = int(car_id)
    car = cars_example()[car_id - 1]
    # car = None
    car_info = car_info_example()
    # car_info = None
    print(car_info)
    context = {
        'title': f'{car["brand"]} {car["model"]} ({car["year"]})',
        'car': car,
        'car_info': car_info,
        'car_upcoming': car_upcoming_example(),
    }
    return render(request, 'car_park/car_info.html', context)


@user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name='')
def history(request, car_id):
    car_id = int(car_id)
    car = cars_example()[car_id - 1]
    # car = None
    car_info = car_info_example()
    # car_info = None
    print(car_info)
    context = {
        'title': f'{car["brand"]} {car["model"]} ({car["year"]})',
        'car': car,
        'car_info': car_info,
        'car_upcoming': car_upcoming_example(),
    }
    return render(request, 'car_park/history.html', context)


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
            'user_id': 1,
            'brand': 'Skoda',
            'model': 'Yeti',
            'year': 2012,
            'description': 'Основная семейная машина (она же единственная)',
            'created_at': 1623531600,
            'deleted_at': 0,
            'active': True,
            # 'mileage': 155000,
        }
    ]


def car_info_example():
    return [
        {
            'id': 1,
            'car_id': 1,
            'type': 'Заправка',
            'mileage': 155030,
            'created_at': '05.06.2021',
            'comment': 'Заправил 30 литров'
        },
        {
            'id': 2,
            'car_id': 1,
            'type': 'ТО',
            'mileage': 155040,
            'created_at': '10.06.2021',
            'comment': 'Замена моторного масла и фильтра'
        },
    ]


def car_upcoming_example():
    return [
        {
            'id': 1,
            'car_id': 1,
            'type': 'ТО',
            'name': 'Замена моторного масла и фильтра',
            'mileage_period': 155040,
            'time_period': '01.07.2021',
            'completed_at': '10.06.2021',
        },
        {
            'id': 2,
            'car_id': 1,
            'type': 'ТО',
            'name': 'Замена свечей',
            'mileage_period': 155250,
            'time_period': '15.07.2021',
            'completed_at': 0,
        },
    ]
