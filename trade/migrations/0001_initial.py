# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-19 20:09
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='статус заказа')),
                ('color', models.CharField(default='ffffff', max_length=6, validators=[django.core.validators.RegexValidator('^[0-9a-fA-F]*$', message='должен указывается в шестнадцатиричной системе.')], verbose_name='цвет пиктограммы')),
            ],
            options={
                'verbose_name_plural': 'статусы заказов',
                'verbose_name': 'статус заказа',
                'db_table': 'trade_status',
            },
        ),
    ]
