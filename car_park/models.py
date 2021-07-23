from django.db import models
from django.conf import settings


class Park(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ID пользователя')
    brand = models.CharField(max_length=50, db_index=True, verbose_name='Марка автомобиля')
    model = models.CharField(max_length=128, db_index=True, verbose_name='Модель автомобиля')
    year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Год производства автомобиля')
    description = models.TextField(null=True, blank=True, verbose_name='Пользовательское описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления авто в парк')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления данных авто')
    active = models.BooleanField(default=True, verbose_name='Активность или текущее авто в парке')

    class Meta:
        verbose_name_plural = 'Парк автомобилей'
        verbose_name = 'Автомобиль'
        ordering = ['user', 'id']
