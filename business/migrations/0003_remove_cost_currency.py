# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 00:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('business', '0002_tax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cost',
            name='currency',
        ),
    ]