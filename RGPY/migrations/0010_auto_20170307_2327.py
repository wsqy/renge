# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0009_auto_20170305_2309'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cos',
            options={'verbose_name': '任务类别', 'verbose_name_plural': '任务类别'},
        ),
        migrations.AlterModelOptions(
            name='mission',
            options={'verbose_name': '任务', 'verbose_name_plural': '任务'},
        ),
        migrations.AddField(
            model_name='mission',
            name='flag',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
    ]
