# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-10 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('system', '0007_auto_20161210_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='belongs',
            field=models.ManyToManyField(to='system.Category', verbose_name='Принадлежность к категории товаров:'),
        ),
    ]