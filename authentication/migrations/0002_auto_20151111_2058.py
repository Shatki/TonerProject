# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='company_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='account',
            name='is_company',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(unique=True, max_length=255, verbose_name='email field'),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(unique=True, max_length=30, validators=[
                django.core.validators.RegexValidator('^[0-9a-zA-Z]*$',
                                                      message='Only alphanumeric characters are allowed.')]),
        ),
    ]
