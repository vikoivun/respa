# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0009_auto_20150630_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='weekday',
            field=models.IntegerField(choices=[(0, 'Maanantai'), (1, 'Tiistai'), (2, 'Keskiviikko'), (3, 'Torstai'), (4, 'Perjantai'), (5, 'Lauantai'), (6, 'Sunnuntai')], verbose_name='Day of week as a number 0-6'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='min_period',
            field=models.DurationField(default=datetime.timedelta(0, 1800)),
        ),
    ]
