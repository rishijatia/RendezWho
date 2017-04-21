# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-21 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RendezWho', '0002_auto_20170420_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='end_time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='start_time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='schedule_entry',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]