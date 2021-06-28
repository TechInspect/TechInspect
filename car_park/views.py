from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import TechInspectForm
from .models import Park, UserUID


def index(request):
    park = Park.objects.all()
    user_uid = UserUID.objects.all()
    context = {'parks': park, 'user_uid': user_uid}
    return render(request, 'car_park/index.html', context)


class ParkCreateView(CreateView):
    template_name = 'car_park/create.html'
    form_class = TechInspectForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parks'] = Park.objects.all()
        return context
