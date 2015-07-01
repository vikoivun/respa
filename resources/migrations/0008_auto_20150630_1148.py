# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0007_auto_20150630_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='weekday',
            field=models.IntegerField(choices=[(0, 'Maanantai'), (1, 'Tiistai'), (2, 'Keskiviikko'), (3, 'Torstai'), (4, 'Perjantai'), (5, 'Lauantai'), (6, 'Sunnuntai')], verbose_name='Day of week as a number 1-7'),
        ),
        migrations.AlterField(
            model_name='resourcetype',
            name='main_type',
            field=models.CharField(choices=[('space', 'Tila'), ('person', 'Henkilö'), ('item', 'Esine')], max_length=20),
        ),
    ]
