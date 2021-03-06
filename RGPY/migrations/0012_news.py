# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 13:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RGPY', '0011_auto_20170311_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='NEWS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(verbose_name='消息')),
                ('link', models.CharField(max_length=100, verbose_name='链接')),
                ('is_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RGPY.OurUser', verbose_name='读者')),
            ],
        ),
    ]
