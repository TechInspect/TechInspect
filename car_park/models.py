from django.db import models


# Create your models here.
class Park(models.Model):
    uid = models.ForeignKey('UserUID', null=True, on_delete=models.PROTECT, verbose_name='ID пользователя')
    brand = models.CharField(max_length=50, db_index=True, null=True, blank=True, verbose_name='Марка автомобиля')
    model = models.CharField(max_length=50, db_index=True, null=True, blank=False, verbose_name='Модель автомобиля')
    year = models.IntegerField(null=True, blank=True, verbose_name='Год производства автомобиля')
    mileage = models.IntegerField(null=True, blank=True, verbose_name='Пробег автомобиля')
    day_of_car_inspection = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='День осмотра авто')

    class Meta:
        verbose_name_plural = 'Парк автомобилей'
        verbose_name = 'Автомобиль'
        ordering = ['uid']


class UserUID(models.Model):
    user_uid = models.IntegerField(db_index=True, verbose_name='Пользователь')

    def __str__(self):
        """For read in admin"""
        return self.user_uid

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['user_uid']
