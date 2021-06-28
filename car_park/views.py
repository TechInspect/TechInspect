from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import BbForm
from .models import Park, UserUID


def index(request):
    park = Park.objects.all()
    user_uid = UserUID.objects.all()
    context = {'bbs': park, 'rubrics': user_uid}
    return render(request, 'car_park/index.html', context)

