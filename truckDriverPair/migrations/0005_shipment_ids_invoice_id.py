# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-05 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truckDriverPair', '0004_auto_20170703_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment_ids',
            name='invoice_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
