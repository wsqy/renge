# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0018_addscoreapply_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='addscoreapply',
            name='desc',
            field=models.CharField(default='', max_length=50, verbose_name='任务名'),
        ),
    ]
