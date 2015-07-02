# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0008_auto_20150701_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='description',
            field=models.CharField(default=False, verbose_name='description', max_length=200),
        ),
        migrations.AddField(
            model_name='period',
            name='exception',
            field=models.BooleanField(default=False, verbose_name='Exceptional period'),
        ),
        migrations.AddField(
            model_name='period',
            name='parent',
            field=models.ForeignKey(blank=True, verbose_name='period', null=True, to='resources.Period'),
        ),
    ]
