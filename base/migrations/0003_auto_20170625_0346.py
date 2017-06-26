# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-25 03:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_add_user_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_user',
            name='user_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='base_add_user_related', to=settings.AUTH_USER_MODEL),
        ),
    ]
