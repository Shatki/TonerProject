# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('authentication', '0004_auto_20151112_0147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='userphoto',
            new_name='user_photo',
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(
                help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                related_name='user_set', blank=True, related_query_name='user', verbose_name='groups', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='account',
            name='is_superuser',
            field=models.BooleanField(
                help_text='Designates that this user has all permissions without explicitly assigning them.',
                verbose_name='superuser status', default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', related_name='user_set',
                                         blank=True, related_query_name='user', verbose_name='user permissions',
                                         to='auth.Permission'),
        ),
    ]
