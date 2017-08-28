# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 23:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('system', '0001_initial'),
        ('document', '0002_auto_20170520_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='consignmenttable',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='system.Country',
                                    verbose_name='страна происхождения'),
            preserve_default=False,
        ),
    ]
