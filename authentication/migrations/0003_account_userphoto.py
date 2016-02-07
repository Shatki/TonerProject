# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0002_auto_20151111_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='userphoto',
            field=models.FileField(upload_to='uploads', default='/static/images/defaultprofileimage.png'),
        ),
    ]
