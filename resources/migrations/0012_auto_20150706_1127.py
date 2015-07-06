# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0011_auto_20150706_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='description',
            field=models.CharField(max_length=200, verbose_name='description', default=False),
        ),
        migrations.AddField(
            model_name='period',
            name='exception',
            field=models.BooleanField(verbose_name='Exceptional period', default=False),
        ),
        migrations.AddField(
            model_name='period',
            name='parent',
            field=models.ForeignKey(to='resources.Period', blank=True, null=True, verbose_name='period'),
        ),
    ]
