# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-03 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truckDriverPair', '0003_shipment_ids'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment_ids',
            name='contact',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shipment_ids',
            name='name_of_customer',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shipment_ids',
            name='ship_form',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shipment_ids',
            name='ship_to',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
