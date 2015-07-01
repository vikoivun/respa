# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0008_auto_20150630_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'verbose_name': 'day', 'verbose_name_plural': 'päivät'},
        ),
        migrations.AlterModelOptions(
            name='period',
            options={'verbose_name': 'aikaväli', 'verbose_name_plural': 'aikavälit'},
        ),
        migrations.AlterModelOptions(
            name='reservation',
            options={'verbose_name': 'varaus', 'verbose_name_plural': 'varaukset'},
        ),
        migrations.AlterModelOptions(
            name='resource',
            options={'verbose_name': 'resurssi', 'verbose_name_plural': 'resurssit'},
        ),
        migrations.AlterModelOptions(
            name='resourcetype',
            options={'verbose_name': 'resurssityyppi', 'verbose_name_plural': 'resurssityypit'},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'verbose_name': 'yksikkö', 'verbose_name_plural': 'yksiköt'},
        ),
        migrations.AddField(
            model_name='resource',
            name='max_period',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='min_period',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
