# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0014_auto_20170313_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='time',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='时间'),
        ),
    ]