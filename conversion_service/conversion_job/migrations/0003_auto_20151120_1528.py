# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversion_job', '0002_auto_20151119_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversionjob',
            name='status',
            field=models.CharField(max_length=20, verbose_name='job status', default='new', choices=[('error', 'error'), ('new', 'new'), ('queued', 'queued'), ('started', 'started'), ('done', 'done')]),
        ),
        migrations.AlterField(
            model_name='gisformat',
            name='progress',
            field=models.CharField(max_length=20, verbose_name='progress', default='new', choices=[('error', 'error'), ('new', 'new'), ('received', 'received'), ('started', 'started'), ('successful', 'successful')]),
        ),
    ]
