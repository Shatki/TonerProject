# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-17 22:50
from __future__ import unicode_literals

import TonerProject.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(help_text='пожалуйста используйте следующий формат: AA-xxxxxxx', max_length=10, validators=[TonerProject.validators.validator_numerator], verbose_name='номер заказа')),
                ('date', models.DateField(auto_now_add=True, verbose_name='дата заказа')),
                ('cost', models.IntegerField(default=0, verbose_name='стоимость')),
                ('comments', models.TextField(blank=True, max_length=100, verbose_name='комментарий')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='system.Product', verbose_name='устройство')),
            ],
            options={
                'db_table': 'order',
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='статус заказа')),
                ('color', models.CharField(default='ffffff', max_length=6, validators=[django.core.validators.RegexValidator('^[0-9a-fA-F]*$', message='должен указывается в шестнадцатиричной системе.')], verbose_name='цвет пиктограммы')),
            ],
            options={
                'db_table': 'service_status',
                'verbose_name': 'статус выполненной работы',
                'verbose_name_plural': 'статусы выполенных работ',
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='вид работы')),
            ],
            options={
                'db_table': 'work',
                'verbose_name': 'вид работы',
                'verbose_name_plural': 'виды работ',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Status', verbose_name='статус заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='клиент'),
        ),
        migrations.AddField(
            model_name='order',
            name='work',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='service.Work', verbose_name='вид работ'),
        ),
    ]
