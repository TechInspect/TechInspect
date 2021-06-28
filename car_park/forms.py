from django.forms import ModelForm
from .models import Park


class TechInspectForm(ModelForm):
    class Meta:
        model = Park
        fields = ('userUID', 'brand', 'model', 'year', 'mileage', 'day_of_car_inspection')
