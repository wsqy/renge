# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0007_mission_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='desc',
            field=models.CharField(max_length=50, verbose_name='任务名称'),
        ),
    ]
