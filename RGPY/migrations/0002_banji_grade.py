# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banji',
            name='grade',
            field=models.CharField(default='2013', max_length=10, verbose_name='年级'),
        ),
    ]
