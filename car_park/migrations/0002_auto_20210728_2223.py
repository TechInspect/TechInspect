# Generated by Django 3.2.4 on 2021-07-28 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_park', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='park',
            options={'ordering': ['user', '-id', '-active'], 'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Парк автомобилей'},
        ),
        migrations.AddField(
            model_name='park',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления авто. Полностью не удаляем'),
        ),
        migrations.AlterField(
            model_name='park',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Активность или текущее авто в парке'),
        ),
        migrations.CreateModel(
            name='CarHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('INI', 'первичная запись'), ('F', 'заправка авто'), ('RGL', 'то'), ('RPR', 'ремонт')], default='F', max_length=3, verbose_name='Статус заказа')),
                ('mileage', models.PositiveIntegerField(verbose_name='Пробег авто на момент записи')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к записи')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_park.park', verbose_name='ID авто')),
            ],
            options={
                'verbose_name': 'Запись истории',
                'verbose_name_plural': 'История обслуживания',
                'ordering': ['mileage', 'created_at'],
            },
        ),
    ]
