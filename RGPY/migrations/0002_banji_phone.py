# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banji',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='用户手机'),
        ),
    ]
