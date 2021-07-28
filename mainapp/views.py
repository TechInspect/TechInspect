from django.shortcuts import render


def index(request):
    context = {
        'title': 'Главная',
    }
    return render(request, 'mainapp/cars.html', context=context)
