# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0013_news_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='link',
            field=models.CharField(blank=True, max_length=100, verbose_name='链接'),
        ),
        migrations.AlterUniqueTogether(
            name='taskapply',
            unique_together=set([('student', 'task')]),
        ),
    ]
