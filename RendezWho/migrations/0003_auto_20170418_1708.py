# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-18 22:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RendezWho', '0002_meeting_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='CRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reqReceiver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('reqSender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='crequest',
            unique_together=set([('reqSender', 'reqReceiver')]),
        ),
    ]