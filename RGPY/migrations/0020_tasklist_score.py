# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0019_addscoreapply_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='score',
            field=models.PositiveSmallIntegerField(default=2, verbose_name='获得时长'),
        ),
    ]