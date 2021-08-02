from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404

from datetime import datetime


class Park(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ID пользователя')
    brand = models.CharField(max_length=50, db_index=True, verbose_name='Марка автомобиля')
    model = models.CharField(max_length=128, db_index=True, verbose_name='Модель автомобиля')
    year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Год производства автомобиля')
    description = models.TextField(null=True, blank=True, verbose_name='Пользовательское описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления авто в парк')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления данных авто')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления авто. Полностью не удаляем')
    active = models.BooleanField(default=False, verbose_name='Активность или текущее авто в парке')

    class Meta:
        verbose_name_plural = 'Парк автомобилей'
        verbose_name = 'Автомобиль'
        ordering = ['user', '-active', '-id']

    def delete(self, using=None, keep_parents=False):
        self.active = False
        self.deleted_at = datetime.now()
        self.save()

    @property
    def mileage_last(self):
        event = CarHistory.record_last_by_mileage(self.id)
        if event:
            return event.mileage
        else:
            return None

    @staticmethod
    def car_by_id(car_id):
        return get_object_or_404(Park, id=car_id)


class CarHistory(models.Model):
    # Типы записей для истории
    INITIATION = "INI"
    FUEL = "F"
    REGLAMENT = "RGL"
    REPAIR = "RPR"

    HISTORY_TYPES_CHOICES_DICT = {
        INITIATION: "Первичная запись",
        FUEL: "Заправка авто",
        REGLAMENT: "ТО",
        REPAIR: "Ремонт",
    }

    HISTORY_TYPES_CHOICES = tuple((k, v) for k, v in HISTORY_TYPES_CHOICES_DICT.items())

    car = models.ForeignKey(Park, on_delete=models.CASCADE, verbose_name='ID авто')
    type = models.CharField(max_length=3, choices=HISTORY_TYPES_CHOICES, default=FUEL, verbose_name='Тип записи')
    mileage = models.PositiveIntegerField(verbose_name='Пробег авто на момент записи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий к записи')

    class Meta:
        verbose_name_plural = 'История обслуживания'
        verbose_name = 'Запись истории'
        ordering = ['mileage', 'created_at']

    @property
    def type_decode(self):
        if self.type in self.HISTORY_TYPES_CHOICES_DICT:
            return self.HISTORY_TYPES_CHOICES_DICT[self.type]
        else:
            return None

    @staticmethod
    def record_last_by_mileage(car_id):
        return CarHistory.objects.filter(car_id=car_id).order_by('-mileage').first()
