# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-06 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truckDriverPair', '0005_shipment_ids_invoice_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment_ids',
            name='end_shipment',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='shipment_ids',
            name='start_shipment',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
