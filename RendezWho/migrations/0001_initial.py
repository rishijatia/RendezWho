# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 23:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('privacy', models.BooleanField()),
                ('approved', models.BooleanField(default=False)),
                ('meetingID', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('end_time', models.TimeField(auto_now_add=True)),
                ('is_at', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='at', to='RendezWho.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule_Entry',
            fields=[
                ('entryID', models.BigAutoField(primary_key=True, serialize=False)),
                ('activity', models.CharField(max_length=50)),
                ('start_time', models.TimeField(auto_now_add=True)),
                ('end_time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('located', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loc', to='RendezWho.Location')),
            ],
        ),
        migrations.CreateModel(
            name='UserApp',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('connections', models.ManyToManyField(related_name='_userapp_connections_+', to='RendezWho.UserApp')),
            ],
        ),
        migrations.AddField(
            model_name='schedule_entry',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owns', to='RendezWho.UserApp'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='participants',
            field=models.ManyToManyField(related_name='participants', to='RendezWho.UserApp'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rqsts', to='RendezWho.UserApp'),
        ),
    ]
