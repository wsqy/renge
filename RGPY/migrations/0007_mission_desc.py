# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0006_auto_20170305_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='desc',
            field=models.CharField(default='无名称', max_length=50, verbose_name='任务名称'),
        ),
    ]