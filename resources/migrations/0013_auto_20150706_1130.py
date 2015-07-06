# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0012_auto_20150706_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='length',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(verbose_name='Range between opens and closes', blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='period',
            name='duration',
            field=django.contrib.postgres.fields.ranges.DateRangeField(verbose_name='Length of period', blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='duration',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(verbose_name='Length of reservation', blank=True, db_index=True, null=True),
        ),
    ]
