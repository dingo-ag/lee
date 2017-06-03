# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20170531_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered',
            field=models.DateTimeField(null=True, verbose_name='Ordered'),
        ),
    ]