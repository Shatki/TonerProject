# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0003_account_userphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='userphoto',
            field=models.FileField(upload_to='/profile/', default='/static/img/profile/defaultprofileimage.jpg'),
        ),
    ]
