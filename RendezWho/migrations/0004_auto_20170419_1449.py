# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-19 19:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RendezWho', '0003_auto_20170418_1708'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='crequest',
            unique_together=set([]),
        ),
    ]
