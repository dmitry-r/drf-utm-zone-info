# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0029_remove_extractionorder_country_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='export',
            name='file_format',
            field=models.CharField(choices=[('fgdb', 'ESRI File Geodatabase (without coastlines, land and sea polygons)'), ('shapefile', 'ESRI Shapefile'), ('gpkg', 'GeoPackage'), ('spatialite', 'SpatiaLite'), ('garmin', 'Garmin navigation & map data')], max_length=10, verbose_name='file format / data format'),
        ),
    ]
