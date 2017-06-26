# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-26 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aproved_mobile_number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GPS_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=100)),
                ('licen_number', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('altitude', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=100)),
                ('timestamp', models.CharField(max_length=100)),
                ('driver_name', models.CharField(max_length=100)),
                ('ping_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
