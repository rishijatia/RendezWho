# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-21 00:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RendezWho', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule_entry',
            name='date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='schedule_entry',
            name='end_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='schedule_entry',
            name='start_time',
            field=models.DateTimeField(blank=True),
        ),
    ]
