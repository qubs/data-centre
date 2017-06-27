# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-23 02:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('climate_data', '0021_auto_20170619_2053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stationsensorlink',
            options={'ordering': ('station_order',), 'verbose_name': 'station-sensor link'},
        ),
        migrations.AlterField(
            model_name='message',
            name='goes_id',
            field=models.CharField(db_index=True, max_length=8, verbose_name='GOES ID'),
        ),
        migrations.AlterField(
            model_name='message',
            name='recorded_message_length',
            field=models.PositiveSmallIntegerField(verbose_name='Message Length'),
        ),
        migrations.AlterField(
            model_name='reading',
            name='qc_processed',
            field=models.BooleanField(default=False, verbose_name='QC Processed'),
        ),
    ]