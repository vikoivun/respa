# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-24 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0042_add_access_code_fields_and_perm'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='reservable_days_in_advance',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Reservable days in advance'),
        ),
        migrations.AddField(
            model_name='unit',
            name='reservable_days_in_advance',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Reservable days in advance'),
        ),
    ]
