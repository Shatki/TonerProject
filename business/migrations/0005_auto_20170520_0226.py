# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 23:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('business', '0004_cost_currency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'налог', 'verbose_name_plural': 'налоги'},
        ),
    ]
