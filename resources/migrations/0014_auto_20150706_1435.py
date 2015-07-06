# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0013_auto_20150706_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='description',
            field=models.CharField(verbose_name='description', null=True, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='authentication',
            field=models.CharField(max_length=20, choices=[('none', 'None'), ('weak', 'Weak'), ('strong', 'Strong')], default='none'),
        ),
    ]
