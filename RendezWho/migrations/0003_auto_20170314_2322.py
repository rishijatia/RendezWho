# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 23:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RendezWho', '0002_auto_20170314_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule_entry',
            name='has',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rqsts', to='RendezWho.UserApp'),
        ),
        migrations.AlterField(
            model_name='schedule_entry',
            name='located',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loc', to='RendezWho.Location'),
        ),
        migrations.AlterField(
            model_name='schedule_entry',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owns', to='RendezWho.UserApp'),
        ),
    ]
