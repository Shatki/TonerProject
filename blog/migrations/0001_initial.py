# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('article_title', models.CharField(max_length=200)),
                ('article_text', models.TextField()),
                ('article_date', models.DateTimeField()),
                ('article_likes', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('comments_text', models.TextField(verbose_name='Комментарии')),
                ('comments_article', models.ForeignKey(to='blog.Article')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('likes_date', models.DateTimeField(auto_now_add=True)),
                ('likes_article', models.ForeignKey(to='blog.Article')),
                ('likes_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'likes',
            },
        ),
    ]
