# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-05 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gps', '0002_aproved_mobile_number_activation_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='RowData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=100)),
                ('lat', models.FloatField(max_length=100)),
                ('long', models.FloatField(max_length=100)),
            ],
        ),
    ]
