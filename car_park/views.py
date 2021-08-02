from django.shortcuts import render, get_object_or_404, redirect
import datetime
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

from car_park.models import Park, CarHistory
# from car_park.forms import CarAddForm

# from .forms import TechInspectForm
# from .models import Park, UserUID


@user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name='')
def cars(request):
    context = {
        'title': 'Гараж',
        'cars': Park.objects.filter(user=request.user)
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


class CarDetail(DetailView):
    model = Park
    template_name = 'car_park/car_info.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super(CarDetail, self).get_context_data(**kwargs)
        context['title'] = f'{context["car"].brand} {context["car"].model}'
        return context

    @method_decorator(user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name=''))
    def dispatch(self, request, *args, **kwargs):
        return super(CarDetail, self).dispatch(request, *args, **kwargs)


class CarEdit(UpdateView):
    model = Park
    template_name = 'car_park/car_edit.html'
    context_object_name = 'car'
    fields = ['brand', 'model', 'year', 'description']

    def get_success_url(self):
        self.success_url = reverse_lazy('car_park:car_info', args=[self.kwargs['pk']])
        return str(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(CarEdit, self).get_context_data(**kwargs)
        context['title'] = f'{context["car"].brand} {context["car"].model}'
        return context

    @method_decorator(user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name=''))
    def dispatch(self, request, *args, **kwargs):
        return super(CarEdit, self).dispatch(request, *args, **kwargs)


class CarDelete(DeleteView):
    model = Park
    template_name = 'car_park/car_delete.html'
    context_object_name = 'car'
    success_url = reverse_lazy('car_park:cars')

    def get_context_data(self, **kwargs):
        context = super(CarDelete, self).get_context_data(**kwargs)
        context['title'] = f'{context["car"].brand} {context["car"].model}'
        return context

    @method_decorator(user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name=''))
    def dispatch(self, request, *args, **kwargs):
        return super(CarDelete, self).dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name='')
def car_activate(request, pk):
    car_id = int(pk)
    cars = Park.objects.filter(user=request.user)
    for car in cars:
        need_save = False
        if car.id == car_id:
            car.active = True
            need_save = True
        elif car.active == True:
            car.active = False
            need_save = True

        if need_save:
            car.save()
    return redirect(reverse('car_park:cars'))


@user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name='')
def history(request, car_id):
    car_id = int(car_id)
    car = get_object_or_404(Park, id=car_id)
    history = CarHistory.objects.filter(car_id=car_id)
    context = {
        'title': f'{car.brand} {car.model}',
        'car': car,
        'history': history,
        'car_upcoming': car_upcoming_example(),
    }
    return render(request, 'car_park/history.html', context)


class HistoryAdd(CreateView):
    model = CarHistory
    fields = ['mileage', 'type', 'comment']
    template_name = 'car_park/history_add.html'

    def get_success_url(self):
        self.success_url = reverse_lazy('car_park:history', args=[self.kwargs['car_id']])
        return str(self.success_url)

    @method_decorator(user_passes_test(lambda u: not u.is_anonymous, login_url='auth:login', redirect_field_name=''))
    def dispatch(self, request, *args, **kwargs):
        car_id = int(kwargs['car_id'])
        self.car = Park.car_by_id(car_id)
        return super(HistoryAdd, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(HistoryAdd, self).get_form(*args, **kwargs)
        if CarHistory.record_last_by_mileage(self.car.id) is None:
            form.fields['type'].initial = "INI"
            form.fields['type'].disabled = True
        else:
            form.fields['type'].widget.choices.pop(0)
        return form

    def get_context_data(self, **kwargs):
        context = super(HistoryAdd, self).get_context_data(**kwargs)
        context['title'] = 'Добавить историю авто'
        context['car'] = self.car
        return context

    def form_valid(self, form):
        car_park_carhistory = form.save(commit=False)
        car_park_carhistory.car_id = self.car.id
        return super(HistoryAdd, self).form_valid(form)



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
